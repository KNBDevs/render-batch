import json, os, sys, time, urllib.request, urllib.parse, urllib.error


def token():
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"],
        "grant_type": "refresh_token",
    }).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data, timeout=60))["access_token"]


def done(res):
    vid = res["id"]
    print("uploaded", vid, res.get("status", {}).get("publishAt", ""), flush=True)
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        open(out, "a").write(f"video_id={vid}\n")


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
    loc = None
    for attempt in range(5):
        try:
            if loc is None:
                req = urllib.request.Request(
                    "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                    data=json.dumps(body).encode(), method="POST",
                    headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                             "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
                loc = urllib.request.urlopen(req, timeout=60).headers["Location"]
                start = 0
            else:
                st = urllib.request.Request(loc, data=b"", method="PUT",
                                            headers={"Authorization": f"Bearer {tok}", "Content-Range": f"bytes */{size}"})
                try:
                    res = json.load(urllib.request.urlopen(st, timeout=60))
                    return done(res)
                except urllib.error.HTTPError as e:
                    if e.code != 308:
                        raise
                    rng = e.headers.get("Range")
                    start = int(rng.split("-")[1]) + 1 if rng else 0
            data = open(video, "rb").read()[start:]
            hdr = {"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"}
            if start:
                hdr["Content-Range"] = f"bytes {start}-{size - 1}/{size}"
            up = urllib.request.Request(loc, data=data, method="PUT", headers=hdr)
            return done(json.load(urllib.request.urlopen(up, timeout=600)))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "ignore")
            print("http", e.code, msg[:800], flush=True)
            last = e
            if e.code < 500:
                break
        except Exception as e:
            print("err", e, flush=True)
            last = e
        time.sleep(30 * (attempt + 1))
    sys.exit(f"upload failed: {last}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
