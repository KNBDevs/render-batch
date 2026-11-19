import glob, importlib.util, json, os, re, sys, unicodedata, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yt_upload import token

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.googleapis.com/youtube/v3/"
APPLY = os.environ.get("APPLY") == "true"


def norm(t):
    t = "".join(c for c in unicodedata.normalize("NFD", (t or "").lower()) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def call(tok, path, params=None, body=None, method="GET"):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method=method,
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def episodes():
    m = {}
    for p in glob.glob(os.path.join(ROOT, "episodes", "*_plan.py")):
        eid = os.path.basename(p)[:-8]
        try:
            spec = importlib.util.spec_from_file_location(eid, p)
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            m[norm(mod.META["title"][:100])] = eid
        except Exception:
            pass
    return m


def main():
    tok = token()
    up = call(tok, "channels", {"part": "contentDetails", "mine": "true"})["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    while True:
        p = {"part": "contentDetails", "playlistId": up, "maxResults": 50}
        if page:
            p["pageToken"] = page
        r = call(tok, "playlistItems", p)
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        page = r.get("nextPageToken")
        if not page:
            break
    vids = []
    for i in range(0, len(ids), 50):
        r = call(tok, "videos", {"part": "snippet,status,statistics", "id": ",".join(ids[i:i + 50])})
        vids += r["items"]
    eps = episodes()
    groups, unknown = {}, []
    for v in vids:
        t = v["snippet"]["title"]
        rec = {"id": v["id"], "title": t, "privacy": v["status"]["privacyStatus"],
               "publishAt": v["status"].get("publishAt"), "views": int(v["statistics"].get("viewCount", 0)),
               "created": v["snippet"]["publishedAt"], "episode": eps.get(norm(t))}
        if norm(t) in ("unknown", ""):
            unknown.append(rec)
        else:
            groups.setdefault(norm(t), []).append(rec)
    report = {"total": len(vids), "unknown": unknown, "duplicates": [], "actions": [], "missing": []}
    vmap = {}
    for k, g in groups.items():
        for r in g:
            if r["episode"]:
                vmap.setdefault(r["episode"], []).append(r["id"])
        if len(g) < 2:
            continue
        g.sort(key=lambda r: (r["privacy"] != "public", -r["views"], r["created"]))
        keep, extra = g[0], g[1:]
        report["duplicates"].append({"title": keep["title"], "episode": keep["episode"], "keep": keep["id"],
                                     "extra": [r["id"] for r in extra], "views": [r["views"] for r in g]})
        for r in extra:
            report["actions"].append({"id": r["id"], "why": "duplicate of " + keep["id"], "was": r["privacy"]})
    for r in unknown:
        report["actions"].append({"id": r["id"], "why": "unknown", "was": r["privacy"]})
    pub = json.load(open(os.path.join(ROOT, "state", "published.json")))
    have = {r["episode"] for g in groups.values() for r in g if r["episode"]}
    report["missing"] = sorted(e for e in pub if e not in have and e in set(eps.values()))
    for a in report["actions"]:
        if a["was"] == "private" and not next((r for r in unknown + [x for g in groups.values() for x in g] if r["id"] == a["id"] and r.get("publishAt")), None):
            a["done"] = "already private"
            continue
        if APPLY:
            call(tok, "videos", {"part": "status"}, {"id": a["id"], "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": True, "embeddable": True}}, "PUT")
            a["done"] = "set private"
    if APPLY and report["missing"]:
        json.dump(sorted(e for e in pub if e not in report["missing"]), open(os.path.join(ROOT, "state", "published.json"), "w"), indent=1)
    vp = os.path.join(ROOT, "state", "videos.json")
    old = json.load(open(vp)) if os.path.exists(vp) else {}
    for e, l in vmap.items():
        old[e] = sorted(set(old.get(e, []) + l))
    json.dump(old, open(vp, "w"), ensure_ascii=False, indent=1)
    json.dump(report, open(os.path.join(ROOT, "state", "dedupe.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: (v if k != "unknown" else [(u["id"], u["privacy"], u["views"]) for u in v]) for k, v in report.items()}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
