import json, os, sys, time, urllib.request, urllib.parse, urllib.error


def token():
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data, timeout=60))["access_token"]


def main(video, meta_p, spec_p):
    meta = json.load(open(meta_p))
    spec = json.load(open(spec_p))
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": True, "embeddable": True}
    if spec.get("publishAt"):
        status["publishAt"] = spec["publishAt"]
    body = {
        "snippet": {
            "title": meta["title"][:100],
            "description": meta.get("description", ""),
            "tags": meta.get("tags", []),
            "categoryId": str(meta.get("categoryId", "27")),
            "defaultLanguage": "es",
            "defaultAudioLanguage": "es-ES",
        },
        "status": status,
    }
    size = os.path.getsize(video)
    tok = token()
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                data=json.dumps(body).encode(), method="POST",
                headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                         "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
            loc = urllib.request.urlopen(req, timeout=60).headers["Location"]
            up = urllib.request.Request(loc, data=open(video, "rb").read(), method="PUT",
                                        headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
            res = json.load(urllib.request.urlopen(up, timeout=600))
            vid = res["id"]
            print("uploaded", vid, res.get("status", {}).get("publishAt", ""), flush=True)
            out = os.environ.get("GITHUB_OUTPUT")
            if out:
                open(out, "a").write(f"video_id={vid}\n")
            return
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")
            print("http", e.code, msg[:800], flush=True)
            last = e
            if e.code in (400, 401, 403) and "quota" not in msg.lower():
                break
            if "quota" in msg.lower():
                break
        except Exception as e:
            print("err", e, flush=True)
            last = e
        time.sleep(30 * (attempt + 1))
    sys.exit(f"upload failed: {last}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
