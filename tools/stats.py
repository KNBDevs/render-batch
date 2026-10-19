import json, os, sys, subprocess, glob, importlib.util, unicodedata, re
from datetime import datetime, timezone
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "state", "stats.json")
URL = os.environ.get("CHANNEL_URL", "https://www.youtube.com/@Pimoruki/shorts")


def norm(t):
    t = "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def titles():
    m = {}
    for p in glob.glob(os.path.join(ROOT, "episodes", "*_plan.py")):
        eid = os.path.basename(p)[:-8]
        try:
            spec = importlib.util.spec_from_file_location(eid, p)
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            t = mod.META.get("title", "")
            chars = sorted({l[1] for l in getattr(mod, "LINES", []) if len(l) > 1})
            m[norm(t.split("#")[0])[:40]] = (eid, chars)
        except Exception:
            pass
    return m


def fetch():
    r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", URL], capture_output=True, text=True, timeout=600)
    data = json.loads(r.stdout)
    out = []
    for e in data.get("entries", []):
        vid = e["id"]
        if e.get("view_count") is None:
            j = subprocess.run(["yt-dlp", "-j", "--skip-download", f"https://www.youtube.com/shorts/{vid}"],
                               capture_output=True, text=True, timeout=120)
            try:
                e = {**e, **json.loads(j.stdout)}
            except Exception:
                pass
        out.append({"id": vid, "title": e.get("title"), "views": e.get("view_count"),
                    "likes": e.get("like_count"), "date": e.get("upload_date") or e.get("timestamp")})
    return out


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    db = json.load(open(OUT)) if os.path.exists(OUT) else {}
    tm = titles()
    for v in fetch():
        if not v["title"]:
            continue
        k = norm(v["title"].split("#")[0])[:40]
        eid, chars = tm.get(k, (None, []))
        rec = db.setdefault(v["id"], {"title": v["title"], "episode": eid, "chars": chars, "hist": {}})
        rec.update({"title": v["title"], "episode": rec.get("episode") or eid, "chars": rec.get("chars") or chars})
        if v.get("date"):
            rec["date"] = str(v["date"])
        if v["views"] is not None:
            rec["hist"][now] = [v["views"], v.get("likes")]
    json.dump(db, open(OUT, "w"), ensure_ascii=False, indent=1)
    rows = sorted(db.values(), key=lambda r: -(list(r["hist"].values())[-1][0] if r["hist"] else 0))
    for r in rows[:50]:
        h = list(r["hist"].values())[-1] if r["hist"] else [None, None]
        print(h[0], h[1], r.get("episode"), ",".join(r.get("chars") or []), r["title"][:60])


if __name__ == "__main__":
    main()
