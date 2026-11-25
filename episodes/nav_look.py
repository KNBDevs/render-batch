import math, random
import bpy
from stage import sky_m, sun, w, C, K, set_interp

TREES = [(0.86, 0.93, 0.98), (0.2, 0.5, 0.36), (0.93, 0.96, 1.0), (0.16, 0.42, 0.32), (0.8, 0.88, 0.97), (0.26, 0.55, 0.4)]


def _base(m, rgb):
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (*rgb, 1)


def winter(dusk=False):
    k = 0
    for m in bpy.data.materials:
        if m.name.startswith('tree'):
            _base(m, TREES[k % len(TREES)])
            k += 1
        elif m.name.startswith('ground'):
            _base(m, (0.66, 0.76, 0.9) if not dusk else (0.5, 0.56, 0.75))
        elif m.name.startswith('stage_ring'):
            _base(m, (0.62, 0.78, 0.95))
        elif m.name == 'stage':
            _base(m, (0.86, 0.9, 0.97))
    r = sky_m.node_tree.nodes['Color Ramp'].color_ramp
    if dusk:
        r.elements[0].color = (0.45, 0.42, 0.75, 1)
        r.elements[1].color = (0.08, 0.1, 0.3, 1)
        sun.data.energy = 1.4
        sun.data.color = (0.75, 0.8, 1.0)
        w.node_tree.nodes['Background'].inputs[0].default_value = (0.3, 0.35, 0.6, 1)
    else:
        r.elements[0].color = (0.9, 0.95, 1.0, 1)
        r.elements[1].color = (0.5, 0.68, 0.95, 1)
        sun.data.energy = 2.2
        sun.data.color = (0.95, 0.97, 1.0)
        w.node_tree.nodes['Background'].inputs[0].default_value = (0.6, 0.7, 0.88, 1)


def snow(total, n=60, box=(-2.6, 2.6, -4.2, 2.5), top=3.6, seed=7, speed=0.012, f0=0):
    rnd = random.Random(seed)
    mt = C.mat('snowflake', (1.0, 1.0, 1.0), rough=0.4, emit=0.35)
    for k in range(n):
        x, y = rnd.uniform(box[0], box[1]), rnd.uniform(box[2], box[3])
        o = C.sphere('flake', (x, y, top), (0.022, 0.022, 0.022), mt, None, 8)
        per = int(top / speed)
        ph = rnd.randrange(per)
        f = f0 - ph
        while f < total + per:
            K(o, 'location', max(f, f0 - per), (x, y, top))
            K(o, 'location', f + per - 1, (x + rnd.uniform(-0.2, 0.2), y, 0.0))
            f += per
        set_interp(o, 'LINEAR')
    return mt
