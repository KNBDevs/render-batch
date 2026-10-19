import math, random
from stage import *
import ep_tools as T
from props.lib import spawn, auto_dress
from episode_lib import plan
from auto import objects as O

Z0 = 0.08
A_POS = Vector((-0.9, -0.2, Z0))
B_POS = Vector((0.9, -0.2, Z0))
APP = Vector((0.0, -1.6, Z0))
PED_H = 0.5
WIDE = ((0.0, -7.7, 1.8), (0.0, -1.0, 1.15), 33)
DEMO = ((0.0, -5.7, 1.4), (0.0, -1.75, 0.7), 33)


def look(kind, rnd):
    bg = sc.world.node_tree.nodes['Background']
    sky = bpy.data.materials.get('Sky')
    ramp = next(n for n in sky.node_tree.nodes if n.type == 'VALTORGB') if sky else None
    if kind == 'atardecer':
        bg.inputs[0].default_value = (1.0, 0.7, 0.5, 1)
        if ramp:
            ramp.color_ramp.elements[0].color = (1.0, 0.55, 0.3, 1)
            ramp.color_ramp.elements[1].color = (0.45, 0.3, 0.75, 1)
        for l in bpy.data.lights:
            if l.type == 'SUN':
                l.color = (1.0, 0.75, 0.5)
                l.energy = 2.4
    elif kind == 'foco':
        bg.inputs[1].default_value = 0.18
        for l in bpy.data.lights:
            l.energy *= 0.25
        bpy.ops.object.light_add(type='SPOT', location=(0.0, -3.2, 3.6))
        sp = bpy.context.object
        sp.data.energy = 900
        sp.data.spot_size = math.radians(55)
        sp.data.spot_blend = 0.5
        sp.data.color = (1.0, 0.95, 0.85)
        tr = sp.constraints.new('TRACK_TO')
        tr.target = C.empty('foco_aim', None, tuple(APP + Vector((0, 0, 0.4))))
        tr.track_axis = 'TRACK_NEGATIVE_Z'
        tr.up_axis = 'UP_Y'
    elif kind == 'fresco':
        bg.inputs[0].default_value = (0.55, 0.85, 1.0, 1)
        if ramp:
            ramp.color_ramp.elements[0].color = (0.75, 1.0, 0.9, 1)
            ramp.color_ramp.elements[1].color = (0.1, 0.55, 0.95, 1)
        g = bpy.data.materials.get('ground')
        if g:
            g.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.45, 0.85, 0.75, 1)


def obj(kind, loc, s=0.34):
    root = C.empty(f'o_{kind}', None, tuple(loc))
    h = O.build(kind, root, s)
    return root, h


def pedestal(x, y):
    m = C.mat('ped', (1.0, 0.85, 0.55), rough=0.4, coat=0.5)
    r = C.empty('ped', None, (x, y, Z0))
    C.lathe('col', [(0.0, 0.0), (0.0, 0.2), (0.04, 0.2), (0.07, 0.13), (PED_H - 0.06, 0.12), (PED_H - 0.03, 0.18), (PED_H, 0.18), (PED_H, 0.0)], m, r, segs=40)
    return Vector((x, y, Z0 + PED_H))


def hop(o, f, a, b, dur=14, apex=0.45):
    for t in range(0, dur + 1, 2):
        u = t / dur
        p = a.lerp(b, u)
        p.z += apex * 4 * u * (1 - u)
        K(o, 'location', f + t, tuple(p))


def pop(o, f, d=8):
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f - 1, (0, 0, 0))
    K(o, 'scale', f + int(d * 0.6), (1.2, 1.2, 1.2))
    K(o, 'scale', f + d, (1, 1, 1))


SIZE = {"clavo": 0.75, "tornillo": 0.75, "clip": 0.7, "hoja": 0.8, "pluma": 1.0, "libro": 0.6, "canica": 0.5}
FRONT_Y = -0.6


def starts(order):
    return {order[0]: Vector((-0.48, APP.y + FRONT_Y, Z0)), order[1]: Vector((0.48, APP.y + FRONT_Y, Z0))}


def place_objs(order):
    st = starts(order)
    objs = {}
    for k, kind in enumerate(order):
        o, h = obj(kind, st[kind], SIZE.get(kind, 0.5))
        objs[kind] = o
        pop(o, 3 + 6 * k)
        K(o, 'location', 3, tuple(st[kind]))
    return objs, st


def jiggle(o, f, base_rot=(0, 0, 0), n=3, amp=6):
    for j in range(n):
        K(o, 'rotation_euler', f + j * 5, (base_rot[0], base_rot[1], base_rot[2] + math.radians(amp if j % 2 else -amp)))
    K(o, 'rotation_euler', f + n * 5, base_rot)


def mech_flota(win, lose, order, t0, sfx):
    W, D, H, Hw = 1.5, 0.66, 0.8, 0.58
    glass = C.mat('glass', (0.92, 0.97, 1.0), rough=0.05, coat=1.0)
    gb = glass.node_tree.nodes.get('Principled BSDF')
    if gb:
        gb.inputs['Alpha'].default_value = 0.06
    frame = C.mat('tankframe', (0.95, 0.45, 0.65), rough=0.35, coat=0.6)
    water = C.mat('water', (0.15, 0.5, 1.0), rough=0.05, coat=0.8, emit=0.15)
    wb = water.node_tree.nodes.get('Principled BSDF')
    if wb:
        wb.inputs['Alpha'].default_value = 0.38
    root = C.empty('tank', None, tuple(APP))
    t = 0.02
    for x in (-W / 2, W / 2):
        C.rounded_box('wall', (x, 0, H / 2), (t, D, H), 0.006, glass, root)
    for y in (-D / 2, D / 2):
        C.rounded_box('wall', (0, y, H / 2), (W, t, H), 0.006, glass, root)
    C.rounded_box('floor', (0, 0, t / 2), (W, D, t), 0.006, glass, root)
    for x in (-W / 2, W / 2):
        for y in (-D / 2, D / 2):
            C.tube('post', [(x, y, 0), (x, y, H)], 0.022, frame, root)
    C.tube('rim', [(-W / 2, -D / 2, H), (W / 2, -D / 2, H), (W / 2, D / 2, H), (-W / 2, D / 2, H), (-W / 2, -D / 2, H)], 0.024, frame, root)
    C.rounded_box('base', (0, 0, -0.01), (W + 0.08, D + 0.08, 0.04), 0.012, frame, root)
    C.rounded_box('water', (0, 0, Hw / 2 + t), (W - 0.05, D - 0.05, Hw), 0.01, water, root)
    surf = APP.z + t + Hw
    objs, st = place_objs(order)
    xs = {order[0]: -0.38, order[1]: 0.38}
    bub_m = C.mat('bubble', (0.85, 0.95, 1), rough=0.05, coat=1.0)
    for k, kind in enumerate(order):
        x, o = xs[kind], objs[kind]
        f = t0 + k * 100
        K(o, 'location', f + 16, tuple(st[kind]))
        hop(o, f + 16, st[kind], Vector((x, APP.y, surf + 0.3)), 14, 0.5)
        cz = O.center_z(kind, SIZE.get(kind, 0.5))
        z_hit = surf - 0.05
        K(o, 'location', f + 31, (x, APP.y, z_hit))
        if kind == win:
            z_end = surf - cz * 1.1
            K(o, 'location', f + 40, (x, APP.y, z_end - 0.1))
            for j, fr in enumerate(range(f + 48, f + 90, 8)):
                K(o, 'location', fr, (x, APP.y, z_end + (0.03 if j % 2 else -0.025)))
            K(o, 'location', t0 + 330, (x, APP.y, z_end))
        else:
            z_end = APP.z + t
            for fr in range(f + 34, f + 66, 3):
                u = (fr - f - 34) / 32
                K(o, 'location', fr, (x, APP.y, z_hit + (z_end - z_hit) * (1 - (1 - u) ** 2)))
            K(o, 'location', f + 66, (x, APP.y, z_end))
            for bi in range(5):
                p0 = (x + 0.06 * (bi - 2), APP.y - 0.1, z_end + 0.15)
                bub = C.sphere('bub', p0, (1, 1, 1), bub_m, None, 12)
                z = (0.04, 0.04, 0.04)
                K(bub, 'scale', 0, (0, 0, 0))
                K(bub, 'scale', f + 36 + bi * 5, (0, 0, 0))
                K(bub, 'scale', f + 40 + bi * 5, z)
                K(bub, 'location', f + 36 + bi * 5, p0)
                K(bub, 'location', f + 72 + bi * 5, (p0[0], p0[1], surf - 0.04))
                K(bub, 'scale', f + 72 + bi * 5, z)
                K(bub, 'scale', f + 76 + bi * 5, (0, 0, 0))
    return objs


def mech_rueda(win, lose, order, t0, sfx):
    wood = C.mat('ramp', (1.0, 0.8, 0.45), rough=0.5, coat=0.4)
    rail = C.mat('rail', (0.45, 0.55, 1.0), rough=0.35, coat=0.6)
    x0, z0, x1, z1 = -0.75, 0.95, 0.7, 0.14
    ang = math.atan2(z0 - z1, x1 - x0)
    L = math.hypot(x1 - x0, z0 - z1)
    root = C.empty('ramp', None, (0, APP.y, Z0))
    pl = C.empty('plank', root, ((x0 + x1) / 2, 0, (z0 + z1) / 2), (0, ang, 0))
    C.rounded_box('board', (0, 0, -0.03), (L + 0.1, 1.0, 0.06), 0.02, wood, pl)
    for y in (-0.5, 0.0, 0.5):
        C.rounded_box('rail', (0, y, 0.02), (L + 0.1, 0.035, 0.06), 0.014, rail, pl)
    C.rounded_box('leg', (x0 + 0.06, 0, (z0 - 0.06) / 2), (0.12, 0.9, z0 - 0.06), 0.03, rail, root)
    C.rounded_box('stop', (x0 - 0.03, 0, z0 + 0.08), (0.05, 1.0, 0.18), 0.015, rail, root)
    objs, st = place_objs(order)
    lanes = {order[0]: -0.25, order[1]: 0.25}
    d = Vector((math.cos(ang), 0, -math.sin(ang)))
    for k, kind in enumerate(order):
        o = objs[kind]
        y = APP.y + lanes[kind]
        top = Vector((x0 + 0.2, y, Z0 + z0 - 0.03))
        f = t0 + k * 100
        K(o, 'location', f - 30, tuple(st[kind]))
        hop(o, f - 30, st[kind], top, 16, 0.8)
        K(o, 'rotation_euler', f - 14, (0, ang if kind != win else 0, 0))
        if kind == win:
            K(o, 'location', f + 10, tuple(top))
            end = Vector((x1 + 0.6, y - 0.2, Z0))
            for fr in range(f + 12, f + 62, 2):
                u = ((fr - f - 12) / 50) ** 1.5
                if u < 0.7:
                    p = top + d * (L * 0.95 * u / 0.7)
                else:
                    v = (u - 0.7) / 0.3
                    a = top + d * (L * 0.95)
                    p = a.lerp(end, v)
                K(o, 'location', fr, tuple(p))
                K(o, 'rotation_euler', fr, (0, (fr - f - 12) * 0.3, 0))
        else:
            K(o, 'location', f + 10, tuple(top))
            K(o, 'location', f + 22, tuple(top + d * 0.06))
            jiggle(o, f + 12, (0, ang, 0))
    return objs


def mech_iman(win, lose, order, t0, sfx):
    objs, st = place_objs(order)
    mag = spawn('toy_magnet', 0, 5, 'pastel', (0, APP.y + FRONT_Y, 2.9), 2.4, 0)
    hi = Z0 + 1.6
    lo = {k: Z0 + 0.66 for k in order}
    K(mag, 'location', 0, (0, APP.y + FRONT_Y, 3.0))
    K(mag, 'location', t0 - 20, (0, APP.y + FRONT_Y, 3.0))
    for k, kind in enumerate(order):
        f = t0 + k * 100
        x = st[kind].x
        yy = st[kind].y
        K(mag, 'location', f, (x, yy, hi))
        K(mag, 'location', f + 22, (x, yy, lo[kind]))
        o = objs[kind]
        if kind == win:
            K(o, 'location', f + 22, tuple(st[kind]))
            K(o, 'location', f + 28, (x, yy, lo[kind] - 0.2))
            K(mag, 'location', f + 46, (x, yy, lo[kind]))
            K(mag, 'location', f + 70, (x, yy, hi))
            K(o, 'location', f + 46, (x, yy, lo[kind] - 0.2))
            K(o, 'location', f + 70, (x, yy, hi - 0.2))
            K(o, 'location', t0 + 330, (x, yy, hi - 0.2))
        else:
            jiggle(o, f + 24)
            K(mag, 'location', f + 50, (x, yy, lo[kind]))
            K(mag, 'location', f + 72, (x, yy, hi))
    xw = st[win].x
    K(mag, 'location', t0 + 330, (xw, st[win].y, hi))
    return objs


def mech_pesa(win, lose, order, t0, sfx):
    base_m = C.mat('scalebase', (0.45, 0.55, 1.0), rough=0.35, coat=0.6)
    beam_m = C.mat('beam', (1.0, 0.75, 0.3), rough=0.4, coat=0.5)
    pan_m = C.mat('pan', (1.0, 0.5, 0.65), rough=0.35, coat=0.6)
    piv_h = 0.62
    APPP = APP + Vector((0, -0.3, 0))
    C.lathe('base', [(0.0, 0.0), (0.0, 0.4), (0.05, 0.4), (0.1, 0.15), (piv_h - 0.05, 0.08), (piv_h, 0.0)], base_m, C.empty('sb', None, tuple(APPP)), segs=48)
    beam = C.empty('beam', None, tuple(APPP + Vector((0, 0, piv_h))))
    C.rounded_box('bar', (0, 0, 0.02), (2.1, 0.16, 0.07), 0.03, beam_m, beam)
    C.sphere('hub', (0, 0, 0.02), (0.08, 0.1, 0.08), base_m, beam, 24)
    pans = {}
    for side, x in (('L', -0.92), ('R', 0.92)):
        p = C.empty('panroot', beam, (x, 0, 0.06))
        C.lathe('pan', [(0.0, 0.0), (0.0, 0.36), (0.06, 0.38), (0.08, 0.36), (0.035, 0.0)], pan_m, p, segs=40)
        pans[side] = p
    sides = {order[0]: 'L', order[1]: 'R'}
    objs, st = place_objs(order)
    ang = math.radians(16)
    for k, kind in enumerate(order):
        o = objs[kind]
        f = t0 + k * 80
        px = -0.92 if sides[kind] == 'L' else 0.92
        dest = APPP + Vector((px, 0, piv_h + 0.1))
        K(o, 'location', f, tuple(st[kind]))
        hop(o, f, st[kind], dest, 12, 0.7)
        o2 = o
        K(o2, 'location', f + 13, tuple(dest))
    tilt = -ang if sides[win] == 'L' else ang
    K(beam, 'rotation_euler', t0 + 80, (0, 0, 0))
    K(beam, 'rotation_euler', t0 + 80 + 12, (0, 0, 0))
    K(beam, 'rotation_euler', t0 + 80 + 22, (0, tilt * 1.15, 0))
    K(beam, 'rotation_euler', t0 + 80 + 28, (0, tilt * 0.92, 0))
    K(beam, 'rotation_euler', t0 + 80 + 34, (0, tilt, 0))
    for kind in order:
        o = objs[kind]
        px = -0.92 if sides[kind] == 'L' else 0.92
        f = t0 + 80 + 12
        for fr, tt in ((f, 0), (f + 10, 1.15), (f + 16, 0.92), (f + 22, 1.0)):
            a = tilt * tt
            dz = -px * math.sin(a)
            dx = px * math.cos(a) - px
            K(o, 'location', fr, tuple(APPP + Vector((px + dx, 0, piv_h + 0.1 + dz))))
    return objs


MECHS = {'flota': mech_flota, 'rueda': mech_rueda, 'iman': mech_iman, 'pesa': mech_pesa}
WORD = {'flota': '¿FLOTA?', 'rueda': '¿RUEDA?', 'iman': '¿SE PEGA?', 'pesa': '¿PESA MÁS?'}


def holiday(theme, rnd):
    if not theme:
        return
    spots = [(-2.6, 0.9), (2.5, 1.1), (-1.9, 2.6), (2.0, 2.9), (-3.2, 3.6), (3.3, 3.8), (-0.9, 3.4), (1.0, 3.9)]
    if theme in ('navidad', 'invierno', 'reyes'):
        green = C.mat('pine', (0.15, 0.6, 0.35), rough=0.5, coat=0.3)
        gold = C.mat('gold', (1.0, 0.8, 0.25), rough=0.25, coat=0.8, metal=0.6)
        snow = C.mat('snow', (0.98, 0.98, 1.0), rough=0.8)
        cols = [(1, 0.2, 0.25), (0.2, 0.5, 1), (1, 0.8, 0.2), (0.7, 0.3, 1)]
        for i, (x, y) in enumerate(spots[:6]):
            r0 = C.empty('xm', None, (x, y, 0))
            s = rnd.uniform(0.8, 1.2)
            for k, (z, rr) in enumerate([(0.25, 0.5), (0.65, 0.38), (1.0, 0.25)]):
                C.lathe('tier', [(0.0, 0.0), (0.0, rr * s), (0.42 * s, 0.0)], green, C.empty('t', r0, (0, 0, z * s)), segs=24)
                for j in range(4):
                    a = j * 1.57 + k
                    C.sphere('orn', (math.cos(a) * rr * s * 0.8, math.sin(a) * rr * s * 0.8, (z + 0.05) * s), (0.06 * s,) * 3, C.mat('orn', cols[(i + j + k) % 4], rough=0.2, coat=0.9), r0, 12)
            C.sphere('star', (0, 0, 1.5 * s), (0.1 * s, 0.04 * s, 0.1 * s), gold, r0, 12)
            C.sphere('snowball', (0.4, -0.3, 0.1), (0.12, 0.12, 0.1), snow, r0, 16)
        if theme == 'reyes':
            for x, y in spots[6:]:
                r0 = C.empty('crown', None, (x, y, 0.0))
                C.lathe('c', [(0.0, 0.3), (0.25, 0.3), (0.25, 0.26), (0.0, 0.26)], gold, r0, segs=40)
                for j in range(6):
                    a = j * 1.047
                    C.sphere('pt', (math.cos(a) * 0.28, math.sin(a) * 0.28, 0.32), (0.04, 0.04, 0.08), gold, r0, 10)
    elif theme == 'sanvalentin':
        for i, (x, y) in enumerate(spots):
            m = C.mat('heart', [(1, 0.3, 0.5), (1, 0.55, 0.7), (0.9, 0.2, 0.35)][i % 3], rough=0.25, coat=0.8)
            r0 = C.empty('heart', None, (x, y, 0.9 + 0.3 * (i % 3)), (math.radians(90), 0, 0))
            for sx in (-1, 1):
                C.sphere('lobe', (sx * 0.14, 0.12, 0), (0.18, 0.18, 0.12), m, r0, 20)
            C.lathe('tip', [(-0.05, 0.0), (-0.05, 0.25), (0.0, 0.25), (0.0, 0.0)], m, C.empty('tp', r0, (0, 0.02, 0), (math.radians(180), 0, 0)), segs=24, sx=1.0, sy=0.5)
            C.tube('string', [(0, -0.2, 0), (0, -0.9, 0)], 0.008, C.mat('str', (1, 1, 1)), r0)
    elif theme in ('pascua', 'carnaval', 'verano'):
        for i, (x, y) in enumerate(spots):
            col = [(0.4, 0.75, 1), (1, 0.6, 0.75), (1, 0.85, 0.3), (0.55, 0.9, 0.5), (0.8, 0.55, 1)][i % 5]
            if theme == 'pascua':
                e = C.sphere('egg', (x, y, 0.2), (0.16, 0.16, 0.22), C.mat('egg', col, rough=0.3, coat=0.7), None, 24)
                C.tube('stripe', [(x + math.cos(a / 16 * 6.283) * 0.161, y + math.sin(a / 16 * 6.283) * 0.161, 0.22) for a in range(17)], 0.02, C.mat('st', (1, 1, 1), rough=0.3), None)
            else:
                z = 1.2 + 0.4 * (i % 3)
                C.sphere('balloon', (x, y, z), (0.25, 0.25, 0.3), C.mat('bal', col, rough=0.2, coat=0.9), None, 24)
                C.tube('str', [(x, y, z - 0.3), (x + 0.05, y, 0.0)], 0.006, C.mat('str', (1, 1, 1)), None)


def build(eid):
    P = plan(eid)
    A = P.AUTO
    rnd = random.Random(A['seed'])
    random.seed(A['seed'])
    auto_dress(eid, A['env'])
    holiday(A.get('holiday'), rnd)
    look(A['look'], rnd)
    a, b = A['chars']
    ca = make(a, A['heights'][0])
    cb = make(b, A['heights'][1])
    T.place(ca, 0, A_POS)
    T.place(cb, 0, B_POS)
    T.turn(ca, 0, 25)
    T.turn(cb, 0, -25)
    t0 = A['t0']
    sfx = []
    objs = MECHS[A['mech']](A['win'], A['lose'], A['order'], t0, sfx)
    word3d(WORD[A['mech']], (1.0, 0.45, 0.2), (0, -2.4, 1.55), 6, 120, size=0.5, max_w=1.6)
    CU = ((0.0, -5.4, 0.9), (0.0, -1.9, 0.5), 30)
    camkey(0, CU)
    camkey(30, CU)
    camkey(64, WIDE)
    camkey(t0 - 12, WIDE)
    camkey(t0 + 8, DEMO)
    camkey(t0 + 210, DEMO)
    camkey(t0 + 236, WIDE)
    camkey(P.TOTAL - 1, WIDE)
    fr = [l[3] for l in P.LINES]
    T.turn(ca, fr[0], 10)
    C.wave(ca, 'R', fr[0] + 2, cycles=2, period=8)
    T.turn(cb, fr[1] - 4, -40)
    gesture(cb, 'bounce', fr[1] + 4)
    T.turn(ca, fr[2] - 4, 40)
    gesture(ca, 'hops', fr[2] + 6)
    T.turn(ca, t0 - 6, 55)
    T.turn(cb, t0 - 6, -55)
    T.turn(ca, t0 + 214, 20)
    T.turn(cb, t0 + 214, -20)
    gesture(cb, 'hops', fr[3])
    sfx.append((fr[3], 'sparkle', 0.22))
    T.turn(cb, fr[3] + 30, -10)
    T.turn(ca, fr[4] - 4, 30)
    C.wave(ca, 'L', fr[4] + 10, cycles=2, period=8)
    gesture(ca, 'hops', fr[5] - 2)
    gesture(cb, 'bounce', fr[5] + 4)
    confetti(fr[5] + 6, (0, -1.4, 2.2), 30, 2.4)
    sfx.append((fr[5] + 6, 'popper', 0.25))
    T.lines(eid, P.LINES)
    T.blinks(ca, range(40, P.TOTAL, 130))
    T.blinks(cb, range(85, P.TOTAL, 140))
    return sfx
