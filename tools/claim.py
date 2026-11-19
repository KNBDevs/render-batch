import json, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "state", "published.json")
SCHED = os.path.join(ROOT, "state", "schedule.json")
VIDS = os.path.join(ROOT, "state", "videos.json")


def sh(*a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True)


def load(p, d):
    return json.load(open(p)) if os.path.exists(p) else d


def save(p, v):
    json.dump(v, open(p, "w"), ensure_ascii=False, indent=1)


def commit(msg, change):
    for _ in range(8):
        sh("git", "fetch", "-q", "origin", "main")
        sh("git", "reset", "-q", "--hard", "origin/main")
        r = change()
        if r is None:
            return 2
        sh("git", "add", "state")
        if sh("git", "diff", "--cached", "--quiet").returncode == 0:
            return 0
        sh("git", "commit", "-qm", msg)
        if sh("git", "push", "-q", "origin", "HEAD:main").returncode == 0:
            return 0
        time.sleep(5)
    return 1


def main():
    op, ep = sys.argv[1], sys.argv[2]
    if op == "claim":
        def ch():
            pub = load(PUB, [])
            if ep in pub:
                return None
            save(PUB, sorted(set(pub + [ep])))
            return True
        sys.exit(commit("update state", ch))
    if op == "release":
        def ch():
            save(PUB, [x for x in load(PUB, []) if x != ep])
            return True
        sys.exit(commit("update state", ch))
    if op == "record":
        vid, pa = sys.argv[3], (sys.argv[4] if len(sys.argv) > 4 else "")
        def ch():
            v = load(VIDS, {})
            if vid:
                v.setdefault(ep, [])
                if vid not in v[ep]:
                    v[ep].append(vid)
                save(VIDS, v)
            if pa:
                s = load(SCHED, {})
                s[ep] = pa
                save(SCHED, s)
            return True
        sys.exit(commit("update state", ch))


if __name__ == "__main__":
    main()
