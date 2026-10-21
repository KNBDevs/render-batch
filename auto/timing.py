import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 24
GAP = 8


def _dur(eid, key, text):
    try:
        m = json.load(open(os.path.join(ROOT, "assets", "vo", "manifest.json")))
        d = m.get(f"ep_{eid}_{key}", {}).get("dur")
        if d:
            return d
    except Exception:
        pass
    return max(1.0, len(text) / 12.0)


def sfx(m, win, order, t0, f4, f6):
    out = [(6, "pop", 0.25)]
    for k, kind in enumerate(order):
        f = t0 + k * (80 if m == "pesa" else 100)
        w = kind == win
        if m == "flota":
            out += [(f + 16, "boing_up", 0.15), (f + 31, "splat", 0.22), (f + 44, "bip", 0.12) if w else (f + 64, "clonk", 0.25)]
        elif m == "rueda":
            out.append((f - 30, "boing_up", 0.12))
            out += [(f + 12, "whistle_down", 0.12), (f + 58, "tock", 0.2)] if w else [(f + 12, "tock", 0.2), (f + 22, "bip", 0.12)]
        elif m == "iman":
            out += [(f + 20, "bip", 0.15), (f + 28, "clonk", 0.3) if w else (f + 30, "whistle_down", 0.08)]
        else:
            out += [(f, "boing_up", 0.12), (f + 12, "clonk", 0.22)]
    if m == "pesa":
        out.append((t0 + 102, "whistle_down", 0.1))
    out += [(f4, "sparkle", 0.22), (f6 + 6, "popper", 0.25)]
    return sorted(out)


def layout(eid, base, auto):
    d = [_dur(eid, k, t) * FPS for k, c, t, mx in base]
    f = [10]
    f.append(max(66, int(f[0] + d[0] + GAP)))
    f.append(max(152, int(f[1] + d[1] + GAP)))
    t0 = max(205, int(f[2] + d[2] + 12))
    f.append(max(t0 + 235, int(f[2] + d[2] + GAP)))
    f.append(max(f[3] + 82, int(f[3] + d[3] + GAP)))
    f.append(max(f[4] + 90, int(f[4] + d[4] + GAP)))
    total = max(720, int(f[5] + d[5] + 40))
    auto["t0"] = t0
    lines = [(k, c, t, fr, mx) for (k, c, t, mx), fr in zip(base, f)]
    return total, lines, sfx(auto["mech"], auto["win"], auto["order"], t0, f[3], f[5])
