import json, os, sys, subprocess, glob, importlib.util, unicodedata, re
from datetime import datetime, timedelta, timezone
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
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
    r = subprocess.run(["yt-dlp", "--extractor-args", "youtube:lang=es", "--flat-playlist", "-J", URL], capture_output=True, text=True, timeout=600)
    data = json.loads(r.stdout)
    out = []
    for e in data.get("entries", []):
        vid = e["id"]
        if e.get("view_count") is None:
            j = subprocess.run(["yt-dlp", "--extractor-args", "youtube:lang=es", "-j", "--skip-download", f"https://www.youtube.com/shorts/{vid}"],
                               capture_output=True, text=True, timeout=120)
            try:
                e = {**e, **json.loads(j.stdout)}
            except Exception:
                pass
        out.append({"id": vid, "title": e.get("title"), "views": e.get("view_count"),
                    "likes": e.get("like_count"), "date": e.get("upload_date") or e.get("timestamp")})
    return out


def audit(db, now):
    seen = {i: r for i, r in db.items() if r["hist"] and max(r["hist"]) == now}
    groups = {}
    for i, r in seen.items():
        groups.setdefault(r.get("episode") or norm(r["title"].split("#")[0]), []).append((i, list(r["hist"].values())[-1][0] or 0))
    lines = []
    for k, g in sorted(groups.items()):
        if len(g) > 1:
            g.sort(key=lambda x: -x[1])
            lines.append(f"- Duplicado `{k}`: conservar **{g[0][0]}** ({g[0][1]} vis.); poner en privado o borrar: "
                         + ", ".join(f"{i} ({v} vis.)" for i, v in g[1:]))
    for i, r in seen.items():
        if norm(r["title"]) == "unknown":
            lines.append(f"- Vídeo `unknown` público: {i} — revisar")
    sched = json.load(open(os.path.join(ROOT, "state", "schedule.json")))
    have = {r.get("episode") for r in seen.values()}
    for e, t in sorted(sched.items()):
        try:
            due = datetime.fromisoformat(t.replace("Z", "+00:00")) < datetime.now(timezone.utc) - timedelta(days=2)
        except ValueError:
            continue
        if due and e not in have and not e.startswith(("hola_", "intro")):
            lines.append(f"- Programado y no visible en el canal: `{e}` ({t[:10]})")
    open(os.path.join(ROOT, "audit.md"), "w").write("\n".join(lines))
    print("AUDIT", len(lines))


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    db = json.load(open(OUT)) if os.path.exists(OUT) else {}
    tm = titles()
    vp = os.path.join(ROOT, "state", "videos.json")
    byid = {i: e for e, ids in (json.load(open(vp)) if os.path.exists(vp) else {}).items() for i in ids}
    for v in fetch():
        if not v["title"]:
            continue
        k = norm(v["title"].split("#")[0])[:40]
        eid, chars = tm.get(k, (None, []))
        if v["id"] in byid:
            eid = byid[v["id"]]
            chars = next((c for e, c in tm.values() if e == eid), chars)
        rec = db.setdefault(v["id"], {"title": v["title"], "episode": eid, "chars": chars, "hist": {}})
        rec.update({"title": v["title"], "episode": byid.get(v["id"]) or rec.get("episode") or eid, "chars": rec.get("chars") or chars})
        if v.get("date"):
            rec["date"] = str(v["date"])
        if v["views"] is not None:
            rec["hist"][now] = [v["views"], v.get("likes")]
    json.dump(db, open(OUT, "w"), ensure_ascii=False, indent=1)
    audit(db, now)
    rows = sorted(db.values(), key=lambda r: -(list(r["hist"].values())[-1][0] if r["hist"] else 0))
    for r in rows[:50]:
        h = list(r["hist"].values())[-1] if r["hist"] else [None, None]
        print(h[0], h[1], r.get("episode"), ",".join(r.get("chars") or []), r["title"][:60])


if __name__ == "__main__":
    main()
