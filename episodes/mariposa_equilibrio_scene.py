from stage import *
from episodes.mariposa_equilibrio_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'mariposa_equilibrio'
Z0 = 0.08
auto_dress(EID, ENV)
TINT = (0.6, 1.0, 0.5)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, TINT, 1.1), (80, TINT, 1.1), (94, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.45, 0.8, 0.35, 1)), (80, (0.45, 0.8, 0.35, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

rnd = random.Random(6701)
TS = 0.8
spawn('low_table', 2, 6703, 'pastel', (0.0, -1.6, Z0), TS, 0)
ZT = Z0 + 0.62 * TS
PX, PY = 0.0, -1.6
BASE = M((0.95, 0.45, 0.6), rough=0.4, coat=0.6)
bs = C.empty('stand', None, (PX, PY, ZT))
C.lathe('disk', [(0, 0.0), (0, 0.15), (0.015, 0.16), (0.05, 0.155), (0.06, 0.14), (0.06, 0.0)], BASE, bs, segs=48)
C.sphere('clay', (0, 0, 0.08), (0.07, 0.07, 0.05), M((1.0, 0.8, 0.3), rough=0.6, coat=0.2), bs, 24)
PL = 0.62
PT = ZT + 0.06 + PL
pe = C.empty('pencil_holder', None, (PX, PY, PT), (math.pi, 0, 0))
spawn('big_pencil', 1, 6705, 'pastel', (0, 0, 0), 1.0, 0, parent=pe, L=PL)

W1 = M((1.0, 0.55, 0.15), rough=0.45, coat=0.5)
W2 = M((0.35, 0.3, 0.95), rough=0.45, coat=0.5)
DOT = M((1.0, 0.95, 0.4), rough=0.4, coat=0.6, emit=0.15)
BODY = M((0.25, 0.2, 0.45), rough=0.4, coat=0.6)


def butterfly(name, parent=None, loc=(0, 0, 0), s=1.0):
    b = C.empty(name, parent, loc)
    C.sphere('head', (0, -0.01 * s, 0.012 * s), (0.032 * s,) * 3, BODY, b, 20)
    C.sphere('thorax', (0, 0.07 * s, 0.0), (0.03 * s, 0.07 * s, 0.026 * s), BODY, b, 20)
    C.sphere('abdomen', (0, 0.17 * s, -0.006 * s), (0.024 * s, 0.07 * s, 0.02 * s), BODY, b, 20)
    for sx in (-1, 1):
        C.tube('antenna', [(0, -0.02 * s, 0.03 * s), (sx * 0.03 * s, -0.06 * s, 0.07 * s), (sx * 0.05 * s, -0.08 * s, 0.09 * s)], 0.005 * s, BODY, b)
        C.sphere('knob', (sx * 0.05 * s, -0.08 * s, 0.09 * s), (0.012 * s,) * 3, DOT, b, 10)
        fw = C.empty('fwing', b, (sx * 0.15 * s, -0.06 * s, -0.04 * s), (math.radians(-12), sx * math.radians(24), sx * math.radians(30)))
        C.sphere('w', (0, 0, 0), (0.17 * s, 0.11 * s, 0.01 * s), W1, fw, 28)
        C.sphere('d', (sx * 0.04 * s, 0.0, 0.009 * s), (0.04 * s, 0.035 * s, 0.006 * s), DOT, fw, 16)
        bw = C.empty('bwing', b, (sx * 0.11 * s, 0.13 * s, -0.01 * s), (0, sx * math.radians(10), sx * math.radians(-25)))
        C.sphere('w', (0, 0, 0), (0.1 * s, 0.075 * s, 0.009 * s), W2, bw, 24)
        C.sphere('d', (0, 0, 0.008 * s), (0.03 * s, 0.025 * s, 0.005 * s), DOT, bw, 14)
    return b


TIPS = [(-0.27, -0.17, -0.11), (0.27, -0.17, -0.11)]
CL = M((0.2, 0.7, 0.95), rough=0.35, coat=0.7)
CL2 = M((0.15, 0.55, 0.85), rough=0.35, coat=0.7)


def clip(parent, p, s=1.0, g=1.0):
    c = C.empty('clip', parent, tuple(v * s for v in p))
    s = s * g
    C.rounded_box('jaw1', (0, 0, 0.022 * s), (0.05 * s, 0.03 * s, 0.035 * s), 0.4, CL, c)
    C.rounded_box('jaw2', (0, 0, -0.022 * s), (0.05 * s, 0.03 * s, 0.035 * s), 0.4, CL, c)
    C.rounded_box('arm1', (0, -0.05 * s, 0.03 * s), (0.04 * s, 0.09 * s, 0.024 * s), 0.4, CL2, c)
    C.rounded_box('arm2', (0, -0.05 * s, -0.03 * s), (0.04 * s, 0.09 * s, 0.024 * s), 0.4, CL2, c)
    C.tube('spring', [(0.026 * s * math.cos(t * 1.3), -0.03 * s, 0.026 * s * math.sin(t * 1.3)) for t in range(12)], 0.004 * s, M((0.9, 0.9, 0.95), rough=0.25, coat=0.9), c)
    return c


bf = butterfly('butterfly', None, (PX, PY, PT + 0.012))
clips = [clip(bf, p, 1.0, 2.0) for p in TIPS]
TIP = (PX, PY, PT + 0.012)
LAND = (0.2, -1.42, ZT + 0.02)


def at_tip(f):
    K(bf, 'location', f, TIP)
    K(bf, 'rotation_euler', f, (0, 0, 0))


def fall(f0):
    at_tip(f0)
    K(bf, 'rotation_euler', f0 + 8, (math.radians(-55), 0, 0))
    K(bf, 'location', f0 + 8, (PX, PY + 0.03, PT - 0.02))
    K(bf, 'location', f0 + 18, LAND)
    K(bf, 'rotation_euler', f0 + 18, (math.radians(-8), 0, math.radians(30)))
    K(bf, 'location', f0 + 21, (LAND[0], LAND[1], LAND[2] + 0.04))
    K(bf, 'location', f0 + 24, LAND)


def lift(f0, f1):
    K(bf, 'location', f0, LAND)
    K(bf, 'rotation_euler', f0, (math.radians(-8), 0, math.radians(30)))
    K(bf, 'location', f0 + 8, (PX + 0.1, PY - 0.05, PT + 0.15))
    K(bf, 'rotation_euler', f0 + 8, (0, 0, 0))
    K(bf, 'location', f1, (PX, PY, PT + 0.15))
    at_tip(f1 + 6)


def sway(f0, f1, a0=14.0):
    f, a, sgn = f0, a0, 1
    while f < f1:
        K(bf, 'rotation_euler', f, (math.radians(sgn * a * 0.6), math.radians(sgn * a), 0))
        f += 12
        a = max(2.5, a * 0.8)
        sgn = -sgn
    K(bf, 'rotation_euler', f1, (0, 0, 0))


at_tip(0)
for c in clips:
    K(c, 'scale', 0, (0, 0, 0))
fall(22)
lift(104, 140)
for k, c in enumerate(clips):
    K(c, 'scale', 298 + k * 12, (0, 0, 0))
    K(c, 'scale', 304 + k * 12, (1.2, 1.2, 1.2))
    K(c, 'scale', 308 + k * 12, (1, 1, 1))
at_tip(330)
sway(334, 466)
for k, c in enumerate(clips):
    K(c, 'scale', 474 + k * 6, (1, 1, 1))
    K(c, 'scale', 480 + k * 6, (0, 0, 0))
fall(494)
lift(540, 570)
for k, c in enumerate(clips):
    K(c, 'scale', 576 + k * 6, (0, 0, 0))
    K(c, 'scale', 582 + k * 6, (1, 1, 1))
sway(600, 800, 6.0)
sway(812, TOTAL - 20, 10.0)

bolita = make('bolita', 1.1)
bopi = make('bopi', 1.1)
OP_, BP_ = Vector((-1.03, -1.6, Z0)), Vector((1.03, -1.6, Z0))
T.place(bolita, 0, OP_)
T.turn(bolita, 0, 25)
T.place(bopi, 0, BP_)
T.turn(bopi, 0, -25)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, RC, BC = (0.05, 0.42, 0.15), (0.8, 0.3, 0.05), (0.1, 0.3, 0.8)
label('¿SE CAE?', RC, (-0.45, -1.1, 2.0), 0.86, 290, 364, 0.32, 0.18)
label('¿SE QUEDA?', GC, (0.5, -0.9, 2.15), 1.0, 298, 364, 0.32, 0.18)
label('PINZAS', BC, (0.0, -1.95, PT + 0.42), 0.66, 372, 420, 0.2, 0.13)
label('¡SE QUEDA!', GC, (0.0, -1.95, PT + 0.5), 0.9, 424, 466, 0.26, 0.16)
label('¡SE CAE!', RC, (0.0, -1.95, PT + 0.5), 0.8, 502, 590, 0.26, 0.16)

exp = C.empty('diagram', None, (0.0, -2.1, 1.12))
C.rounded_box('panel', (0, 0.04, 0.4), (1.16, 0.03, 0.86), 0.4, M((0.92, 1.0, 0.85), rough=0.5, coat=0.3), exp)
C.rounded_box('divider', (0, 0.0, 0.38), (0.025, 0.03, 0.72), 0.4, M((1.0, 1.0, 1.0), rough=0.5, coat=0.3), exp)
RED = M((1.0, 0.15, 0.2), rough=0.3, coat=0.6, emit=0.35)
for side in (-1, 1):
    cx = side * 0.28
    C.lathe('peak', [(0.0, 0.0), (0.0, 0.06), (0.32, 0.004), (0.325, 0.0)], M((0.6, 0.5, 0.4), rough=0.5, coat=0.3), C.empty('pk', exp, (cx, -0.02, 0.05), (math.pi / 2, 0, 0)), segs=24)
    pv = C.empty('mini_pivot', exp, (cx, -0.06, 0.38))
    mb = butterfly('mini', pv, (0, 0, 0.01), 0.75)
    mb.rotation_euler = (math.radians(90), 0, 0)
    if side > 0:
        for p in TIPS:
            clip(mb, p, 0.75, 2.0)
    wd = C.empty('weight', pv, (0, -0.07, 0.12) if side < 0 else (0, -0.07, -0.08))
    C.sphere('w', (0, 0, 0), (0.035,) * 3, RED, wd, 16)
    if side < 0:
        K(pv, 'rotation_euler', 620, (0, 0, 0))
        K(pv, 'rotation_euler', 640, (0, math.radians(-40), 0))
        K(pv, 'rotation_euler', 700, (0, 0, 0))
        K(pv, 'rotation_euler', 720, (0, math.radians(-40), 0))
    else:
        f, sg = 620, 1
        while f < 770:
            K(pv, 'rotation_euler', f, (0, math.radians(sg * 10), 0))
            f += 14
            sg = -sg
T.pop_in(exp, 604, 1.2, 10)
T.pop_out(exp, 800, 1.2, 6)
label('SIN PINZAS', RC, (-0.28, -2.18, 1.92), 0.62, 618, 800, 0.2, 0.11)
label('CON PINZAS', GC, (0.28, -2.18, 1.92), 0.64, 632, 800, 0.2, 0.11)
label('PESO', RC, (0.0, -2.2, 1.28), 0.42, 650, 800, 0.16, 0.1)
label('¡SE CAE!', RC, (-0.5, -1.9, 1.95), 0.8, 812, TOTAL + 10, 0.3, 0.17)
label('¡SE QUEDA!', GC, (0.5, -1.9, 1.95), 0.92, 826, TOTAL + 10, 0.3, 0.17)
confetti(880, (0, -1.6, 1.6), n=30, spread=1.6)

OP = ((-0.1, -3.7, 1.6), (-0.52, -1.6, 1.0), 27)
W = ((0.0, -5.5, 1.8), (0.0, -1.6, 1.05), 28)
CU = ((0.0, -3.4, 1.45), (0.0, -1.6, 1.15), 32)
EXP = ((0.0, -4.75, 1.75), (0.0, -1.85, 1.48), 28)
FIN = ((0.0, -5.6, 1.8), (0.0, -1.6, 1.1), 28)
for a, b, pose in ((0, 88, OP), (90, 368, W), (370, 470, CU), (472, 594, CU), (596, 804, EXP), (806, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

gesture(bolita, 'hops', 50)
T.arm(bopi, 'L', 100, 0, None)
T.arm(bopi, 'L', 108, fwd=-75, out=25)
T.arm(bopi, 'L', 150, fwd=-75, out=25)
T.rest_arm(bopi, 'L', 162)
T.arm(bopi, 'L', 290, 0, None)
T.arm(bopi, 'L', 300, fwd=-80, out=20)
T.arm(bopi, 'L', 326, fwd=-80, out=20)
T.rest_arm(bopi, 'L', 338)
gesture(bopi, 'hops', 380)
T.arm(bolita, 'R', 466, 0, None)
T.arm(bolita, 'R', 474, fwd=-80, out=20)
T.arm(bolita, 'R', 490, fwd=-80, out=20)
T.rest_arm(bolita, 'R', 500)
gesture(bolita, 'hops', 512)
gesture(bopi, 'breathe', 600)
T.arm(bolita, 'R', 816, 0, None)
T.arm(bolita, 'R', 826, fwd=-60, out=60)
T.arm(bolita, 'R', 876, fwd=-60, out=60)
T.rest_arm(bolita, 'R', 886)
C.wave(bolita, 'L', 896, cycles=2, period=10)
C.wave(bopi, 'R', 892, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(bolita, (50, 170, 320, 450, 580, 720, 860, 920))
T.blinks(bopi, (60, 180, 340, 480, 640, 760))
