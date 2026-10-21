import math
from stage import C


def M(rgb, rough=0.45, coat=0.4, metal=0.0, emit=0.0):
    return C.mat("ao", rgb, rough=rough, coat=coat, metal=metal, emit=emit)


def build(kind, root, s=0.32):
    r = s / 2
    if kind == "pelota":
        C.sphere("ball", (0, 0, r), (r, r, r), M((0.2, 0.55, 1.0), 0.3, 0.7), root, 48)
        C.tube("band", [(math.cos(a / 24 * 6.2832) * r * 1.005, 0, r + math.sin(a / 24 * 6.2832) * r * 1.005) for a in range(25)], r * 0.12, M((1, 0.85, 0.2), 0.3, 0.7), root)
        C.tube("band2", [(0, math.cos(a / 24 * 6.2832) * r * 1.005, r + math.sin(a / 24 * 6.2832) * r * 1.005) for a in range(25)], r * 0.12, M((1, 0.3, 0.4), 0.3, 0.7), root)
        return r * 2
    if kind == "corcho":
        cm = M((0.82, 0.6, 0.36), 0.85, 0.05)
        C.lathe("cork", [(0.0, 0.0), (0.0, r * 0.75), (r * 0.08, r * 0.8), (r * 1.5, r * 0.88), (r * 1.6, r * 0.8), (r * 1.6, 0.0)], cm, root, segs=40)
        pm = M((0.55, 0.36, 0.2), 0.9, 0.0)
        for k in range(16):
            a = k * 2.39
            C.sphere("pore", (math.cos(a) * r * 0.82, math.sin(a) * r * 0.82, r * (0.2 + 1.2 * ((k * 7) % 10) / 10)), (r * 0.07,) * 3, pm, root, 8)
        return r * 1.6
    if kind == "piedra":
        C.sphere("stone", (0, 0, r * 0.62), (r * 1.1, r * 0.9, r * 0.62), M((0.55, 0.55, 0.6), 0.6, 0.2), root, 40)
        C.sphere("bump", (r * 0.4, -r * 0.2, r * 0.85), (r * 0.5, r * 0.45, r * 0.35), M((0.5, 0.5, 0.56), 0.6, 0.2), root, 24)
        C.sphere("fleck", (r * 0.2, -r * 0.75, r * 0.75), (r * 0.12, r * 0.05, r * 0.08), M((0.8, 0.8, 0.85), 0.4, 0.3), root, 10)
        return r * 1.25
    if kind in ("manzana", "naranja"):
        if kind == "manzana":
            C.lathe("apple", [(0.0, 0.0), (0.0, r * 0.3), (r * 0.1, r * 0.7), (r * 0.4, r), (r * 0.9, r * 1.05), (r * 1.4, r * 0.95), (r * 1.7, r * 0.65), (r * 1.82, r * 0.3), (r * 1.75, 0.0)], M((0.92, 0.18, 0.15), 0.3, 0.8), root, segs=48)
            top = r * 1.75
        else:
            C.sphere("orange", (0, 0, r), (r, r, r * 0.95), M((1.0, 0.55, 0.1), 0.55, 0.4), root, 40)
            top = r * 1.9
        C.tube("stem", [(0, 0, top - r * 0.1), (r * 0.06, 0, top + r * 0.3)], r * 0.06, M((0.4, 0.25, 0.12), 0.7, 0.0), root)
        C.leaf("leaf", r * 0.45, r * 0.22, 0.2, M((0.3, 0.68, 0.25), 0.5, 0.3), C.empty("lf", root, (r * 0.1, 0, top + r * 0.15), (0, math.radians(-60), math.radians(20))))
        return top
    if kind == "madera":
        C.rounded_box("block", (0, 0, r * 0.7), (r * 2, r * 1.3, r * 1.4), r * 0.15, M((0.92, 0.72, 0.45), 0.6, 0.2), root)
        gm = M((0.75, 0.52, 0.3), 0.7, 0.0)
        for z in (0.35, 0.7, 1.05):
            C.tube("grain", [(-r * 0.9, -r * 0.66, r * z), (-r * 0.3, -r * 0.66, r * z + r * 0.06), (r * 0.3, -r * 0.66, r * z - r * 0.04), (r * 0.9, -r * 0.66, r * z)], r * 0.035, gm, root)
        return r * 1.4
    if kind == "caja":
        C.rounded_box("box", (0, 0, r * 0.8), (r * 1.8, r * 1.6, r * 1.6), r * 0.12, M((0.95, 0.6, 0.35), 0.6, 0.2), root)
        C.rounded_box("tape", (0, 0, r * 1.6), (r * 0.4, r * 1.62, r * 0.04), r * 0.01, M((0.98, 0.85, 0.55), 0.5, 0.2), root)
        return r * 1.6
    if kind == "libro":
        C.rounded_box("cover", (0, 0, r * 0.35), (r * 1.9, r * 1.4, r * 0.7), r * 0.06, M((0.25, 0.45, 0.9), 0.4, 0.5), root)
        C.rounded_box("pages", (r * 0.05, 0, r * 0.35), (r * 1.82, r * 1.3, r * 0.56), r * 0.03, M((0.98, 0.96, 0.9), 0.6, 0.1), root)
        C.rounded_box("label", (0, -r * 0.71, r * 0.35), (r * 0.9, r * 0.02, r * 0.2), r * 0.01, M((1, 0.85, 0.3), 0.4, 0.4), root)
        return r * 0.7
    if kind == "hoja":
        C.leaf("leaf", r * 1.8, r * 0.9, 0.15, M((0.35, 0.75, 0.3), 0.5, 0.3), C.empty("lf", root, (-r * 0.9, 0, r * 0.08), (math.radians(90), 0, 0)))
        return r * 0.2
    if kind == "pluma":
        e = C.empty("pl", root, (-r * 0.9, 0, r * 0.1), (math.radians(90), 0, math.radians(8)))
        C.leaf("vane", r * 1.9, r * 0.6, 0.25, M((1.0, 0.45, 0.7), 0.5, 0.3), e)
        C.tube("quill", [(-r * 0.95, 0, r * 0.1), (r * 0.9, 0, r * 0.16)], r * 0.035, M((0.95, 0.85, 0.7), 0.5, 0.2), root)
        return r * 0.25
    if kind == "canica":
        C.sphere("marble", (0, 0, r * 0.7), (r * 0.7,) * 3, M((0.35, 0.8, 0.95), 0.05, 1.0), root, 40)
        C.sphere("swirl", (r * 0.15, -r * 0.35, r * 0.85), (r * 0.25, r * 0.08, r * 0.45), M((1, 0.4, 0.6), 0.1, 0.8), root, 16)
        return r * 1.4
    if kind in ("clavo", "tornillo"):
        mm = M((0.72, 0.74, 0.8), 0.25, 0.6, metal=1.0)
        C.tube("shaft", [(-r * 0.9, 0, r * 0.18), (r * 0.8, 0, r * 0.18)], r * 0.13, mm, root)
        C.lathe("head", [(0.0, 0.0), (0.0, r * 0.4), (r * 0.12, r * 0.42), (r * 0.18, 0.0)], mm, C.empty("h", root, (-r * 0.95, 0, r * 0.18), (0, math.radians(90), 0)), segs=32)
        C.sphere("tip", (r * 0.85, 0, r * 0.18), (r * 0.16, r * 0.1, r * 0.1), mm, root, 12)
        if kind == "tornillo":
            for k in range(7):
                x = -r * 0.6 + k * r * 0.2
                C.tube("thread", [(x, -r * 0.15, r * 0.06), (x + r * 0.08, r * 0.15, r * 0.3)], r * 0.035, mm, root)
        return r * 0.4
    if kind == "clip":
        mm = M((0.75, 0.78, 0.85), 0.25, 0.6, metal=1.0)
        pts = [(-r * 0.6, 0, r * 0.05), (r * 0.8, 0, r * 0.05), (r * 0.95, 0, r * 0.12), (r * 0.8, 0, r * 0.2), (-r * 0.8, 0, r * 0.2), (-r * 0.95, 0, r * 0.13), (-r * 0.8, 0, r * 0.08), (r * 0.6, 0, r * 0.08)]
        C.tube("wire", [(x, z * 2.4, r * 0.05) for x, _, z in pts], r * 0.045, mm, root)
        return r * 0.12
    if kind == "rueda":
        e = C.empty("w", root, (0, 0, r), (math.radians(90), 0, 0))
        C.lathe("tyre", [(-r * 0.35, r * 0.55), (-r * 0.4, r * 0.8), (-r * 0.3, r), (r * 0.3, r), (r * 0.4, r * 0.8), (r * 0.35, r * 0.55)], M((0.15, 0.15, 0.18), 0.6, 0.2), e, segs=48)
        C.lathe("hub", [(-r * 0.36, 0.0), (-r * 0.36, r * 0.6), (r * 0.36, r * 0.6), (r * 0.36, 0.0)], M((1.0, 0.75, 0.2), 0.3, 0.7), e, segs=40)
        return r * 2
    raise KeyError(kind)


def center_z(kind, s=0.32):
    return {"pelota": 1.0, "canica": 0.7, "naranja": 1.0, "rueda": 1.0, "manzana": 0.9}.get(kind, 0.5) * s / 2
