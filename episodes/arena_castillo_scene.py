from stage import *
from episodes.arena_castillo_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'arena_castillo'
Z0 = 0.08
auto_dress(EID, ENV)
TINT = (1.0, 0.72, 0.38)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, TINT, 1.1), (80, TINT, 1.1), (94, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.95, 0.6, 0.3, 1)), (80, (0.95, 0.6, 0.3, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

rnd = random.Random(6501)
CX, CY = 0.0, -1.6
SW, SD, SH = 1.1, 0.82, 0.15
WOOD = M((0.2, 0.5, 0.95), rough=0.4, coat=0.6)
WOOD2 = M((0.95, 0.35, 0.3), rough=0.4, coat=0.6)
box = C.empty('sandbox', None, (CX, CY, Z0))
for x, y, w, d, m in ((0, -SD / 2, SW + 0.1, 0.09, WOOD), (0, SD / 2, SW + 0.1, 0.09, WOOD), (-SW / 2, 0, 0.09, SD, WOOD2), (SW / 2, 0, 0.09, SD, WOOD2)):
    C.rounded_box('plank', (x, y, SH / 2), (w, d, SH), 0.35, m, box)
for sx in (-1, 1):
    for sy in (-1, 1):
        C.sphere('knob', (sx * SW / 2, sy * SD / 2, SH + 0.01), (0.06, 0.06, 0.04), WOOD2 if sx == sy else WOOD, box, 20)
DRY = M((0.85, 0.6, 0.3), rough=0.9, coat=0.05)
WET = M((0.36, 0.2, 0.09), rough=0.35, coat=0.5)
C.rounded_box('sand', (0, 0, 0.06), (SW - 0.06, SD - 0.06, 0.12), 0.5, DRY, box)
for k in range(10):
    C.sphere('ripple', (rnd.uniform(-0.42, 0.42), rnd.uniform(-0.3, 0.3), 0.12), (rnd.uniform(0.04, 0.07),) * 2 + (0.012,), DRY, box, 12)
ZS = Z0 + 0.12
XD, XW = -0.25, 0.25


def tower(name, mat, x, h=0.3):
    t = C.empty(name, None, (CX + x, CY, ZS))
    C.lathe('body', [(0, 0.0), (0, 0.185), (0.02, 0.185), (h, 0.14), (h, 0.0)], mat, t, segs=40)
    for k in range(6):
        a = k * 6.2832 / 6
        C.rounded_box('merlon', (math.cos(a) * 0.11, math.sin(a) * 0.11, h + 0.03), (0.06, 0.06, 0.06), 0.4, mat, t)
    C.tube('band', [(math.cos(k * 6.2832 / 40) * 0.176, math.sin(k * 6.2832 / 40) * 0.176, 0.07) for k in range(41)], 0.006, mat, t)
    return t


def flag(parent, z, f):
    fl = C.empty('flag', parent, (0, 0, z))
    C.tube('pole', [(0, 0, 0), (0, 0, 0.2)], 0.007, M((1.0, 1.0, 1.0), rough=0.4, coat=0.5), fl)
    C.rounded_box('cloth', (0.045, 0, 0.165), (0.08, 0.012, 0.055), 0.4, M((1.0, 0.35, 0.45), rough=0.5, coat=0.4), fl)
    C.sphere('tip', (0, 0, 0.205), (0.014,) * 3, M((1.0, 0.85, 0.2), rough=0.4, coat=0.6), fl, 12)
    T.pop_in(fl, f, 1.0, 6)
    return fl


def mound(name, mat, x, f):
    m = C.empty(name, None, (CX + x, CY, ZS))
    C.sphere('pile', (0, 0, 0), (0.24, 0.2, 0.08), mat, m, 24)
    for k in range(6):
        a = k * 1.05 + rnd.uniform(-0.3, 0.3)
        C.sphere('lump', (math.cos(a) * 0.16, math.sin(a) * 0.13, 0.01), (0.045, 0.04, 0.03), mat, m, 12)
    T.pop_in(m, f, 1.0, 6)
    return m


def collapse(t, f0):
    K(t, 'scale', f0, (1, 1, 1))
    K(t, 'scale', f0 + 4, (1.08, 1.08, 0.86))
    K(t, 'scale', f0 + 10, (1.35, 1.35, 0.3))
    K(t, 'scale', f0 + 12, (0, 0, 0))
    for k in range(5):
        g = C.empty('grain', None, (t.location.x, CY, ZS + 0.2))
        C.sphere('g', (0, 0, 0), (0.025,) * 3, DRY, g, 10)
        K(g, 'scale', 0, (0, 0, 0))
        K(g, 'scale', f0 + 2, (0, 0, 0))
        K(g, 'scale', f0 + 3, (1, 1, 1))
        dx = (k - 2) * 0.07
        K(g, 'location', f0 + 3, (t.location.x + dx * 0.4, CY - 0.05, ZS + 0.2))
        K(g, 'location', f0 + 14, (t.location.x + dx * 1.6, CY - 0.1, ZS + 0.02))
        K(g, 'scale', f0 + 16, (1, 1, 1))
        K(g, 'scale', f0 + 18, (0, 0, 0))


d1 = tower('dry_tower', DRY, XD)
flag(d1, 0.33, 12)
K(d1, 'scale', 0, (1, 1, 1))
collapse(d1, 30)
m1 = mound('dry_mound', DRY, XD, 40)
T.pop_out(m1, 474, 1.0, 4)

wp = C.empty('wet_patch', None, (CX + XW, CY, ZS - 0.002))
C.sphere('p', (0, 0, 0), (0.27, 0.25, 0.014), WET, wp, 32)
K(wp, 'scale', 0, (0, 0, 0))
K(wp, 'scale', 304, (0.2, 0.2, 1))
K(wp, 'scale', 340, (1, 1, 1))

CAN = M((0.1, 0.65, 0.45), rough=0.35, coat=0.7)
CAN2 = M((1.0, 0.7, 0.1), rough=0.35, coat=0.7)
can = C.empty('watering_can', None, (0.66, -1.78, ZS + 0.42))
C.lathe('body', [(0, 0.0), (0, 0.1), (0.015, 0.11), (0.15, 0.105), (0.17, 0.085), (0.18, 0.0)], CAN, can, segs=40)
C.tube('stripe', [(math.cos(k * 6.2832 / 40) * 0.112, math.sin(k * 6.2832 / 40) * 0.112, 0.07) for k in range(41)], 0.01, CAN2, can)
C.tube('spout', [(-0.08, 0, 0.04), (-0.17, 0, 0.12), (-0.25, 0, 0.2)], 0.018, CAN, can, radii=[0.022, 0.017, 0.014])
C.sphere('rose', (-0.265, 0, 0.21), (0.022, 0.045, 0.045), CAN2, can, 20, (0, 0, 0))
C.tube('handle', [(0.06, 0, 0.17), (0.08, 0, 0.27), (0.0, 0, 0.29), (-0.05, 0, 0.18)], 0.014, CAN2, can)
C.sphere('cap', (0, 0, 0.18), (0.04, 0.04, 0.015), CAN2, can, 16)
T.pop_in(can, 98, 1.0, 8)
K(can, 'rotation_euler', 296, (0, 0, 0))
K(can, 'rotation_euler', 306, (0, math.radians(-32), 0))
K(can, 'rotation_euler', 338, (0, math.radians(-32), 0))
K(can, 'rotation_euler', 346, (0, 0, 0))
T.pop_out(can, 372, 1.0, 6)
DROP = MA((0.35, 0.65, 1.0), 0.7, rough=0.05, emit=0.35)
for k in range(8):
    x0 = CX + XW + 0.06 + rnd.uniform(-0.05, 0.05)
    d = C.empty('drop', None, (x0, CY + rnd.uniform(-0.04, 0.04), ZS + 0.5))
    C.sphere('d', (0, 0, 0), (0.014, 0.014, 0.022), DROP, d, 10)
    K(d, 'scale', 0, (0, 0, 0))
    f = 306 + k * 3
    while f < 338:
        K(d, 'scale', f, (0, 0, 0))
        K(d, 'scale', f + 1, (1, 1, 1))
        K(d, 'location', f, (x0, d.location.y, ZS + 0.5))
        K(d, 'location', f + 8, (x0 - 0.08, d.location.y, ZS + 0.01))
        K(d, 'scale', f + 8, (1, 1, 1))
        K(d, 'scale', f + 9, (0, 0, 0))
        f += 12

BK = M((0.95, 0.28, 0.25), rough=0.35, coat=0.75)
BK2 = M((1.0, 0.8, 0.15), rough=0.35, coat=0.7)
bucket = C.empty('bucket', None, (CX + XW, CY, ZS + 0.6))
bk = C.empty('bucket_inv', bucket, (0, 0, 0.31), (math.pi, 0, 0))
C.lathe('pail', [(0, 0.0), (0, 0.14), (0.012, 0.146), (0.3, 0.192), (0.31, 0.2), (0.315, 0.192), (0.31, 0.182), (0.02, 0.132), (0.014, 0.0)], BK, bk, segs=48)
for zz, rr in ((0.31, 0.2), (0.14, 0.168)):
    C.tube('ring', [(math.cos(k * 6.2832 / 48) * rr, math.sin(k * 6.2832 / 48) * rr, zz) for k in range(49)], 0.011, BK2, bk)
C.tube('bail', [(math.cos(a) * 0.205, 0, 0.29 + math.sin(a) * 0.15) for a in [k * math.pi / 12 for k in range(13)]], 0.009, BK2, bk)
for k in range(5):
    a = k * 6.2832 / 5
    C.sphere('star', (math.cos(a) * 0.172, math.sin(a) * 0.172, 0.22), (0.024, 0.024, 0.024), BK2, bk, 10)
K(bucket, 'scale', 0, (0, 0, 0))


def bucket_go(x, f_in, f_land, f_lift, f_out):
    K(bucket, 'scale', f_in - 1, (0, 0, 0))
    K(bucket, 'location', f_in - 1, (CX + x, CY, ZS + 0.6))
    K(bucket, 'scale', f_in + 5, (1, 1, 1))
    K(bucket, 'location', f_in + 5, (CX + x, CY, ZS + 0.6))
    K(bucket, 'location', f_land, (CX + x, CY, ZS - 0.005))
    K(bucket, 'location', f_lift, (CX + x, CY, ZS - 0.005))
    K(bucket, 'location', f_lift + 8, (CX + x, CY, ZS + 0.55))
    K(bucket, 'scale', f_out, (1, 1, 1))
    K(bucket, 'scale', f_out + 6, (0, 0, 0))


bucket_go(XW, 340, 346, 350, 372)
w1 = tower('wet_tower', WET, XW)
K(w1, 'scale', 0, (0, 0, 0))
K(w1, 'scale', 349, (0, 0, 0))
K(w1, 'scale', 350, (1, 1, 1))
flag(w1, 0.33, 384)
bucket_go(XD, 474, 482, 488, 500)
d2 = tower('dry_tower2', DRY, XD)
K(d2, 'scale', 0, (0, 0, 0))
K(d2, 'scale', 487, (0, 0, 0))
K(d2, 'scale', 488, (1, 1, 1))
collapse(d2, 500)
mound('dry_mound2', DRY, XD, 510)

luma = make('luma', 1.1)
ruki = make('ruki', 1.1)
LP, RP = Vector((-0.97, -1.6, Z0)), Vector((0.97, -1.6, Z0))
T.place(luma, 0, LP)
T.turn(luma, 0, 25)
T.place(ruki, 0, RP)
T.turn(ruki, 0, -25)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, BC, RC = (0.05, 0.42, 0.15), (0.1, 0.3, 0.8), (0.8, 0.3, 0.05)
label('¿AGUANTA?', GC, (-0.45, -1.1, 1.75), 0.98, 216, 296, 0.32, 0.18)
label('¿SE CAE?', RC, (0.5, -0.9, 1.9), 0.86, 224, 296, 0.32, 0.18)
label('¡AGUANTA!', GC, (XW - 0.1, -1.35, ZS + 0.56), 0.56, 376, 464, 0.2, 0.12)
label('¡SE CAE!', RC, (XD + 0.12, -1.35, ZS + 0.56), 0.5, 516, 598, 0.2, 0.12)

exp = C.empty('diagram', None, (0.0, -2.05, 1.12))
C.rounded_box('panel', (0, 0.04, 0.35), (1.14, 0.03, 0.9), 0.4, M((1.0, 0.8, 0.55), rough=0.5, coat=0.3), exp)
C.rounded_box('divider', (0, 0.0, 0.3), (0.025, 0.03, 0.7), 0.4, M((1.0, 1.0, 1.0), rough=0.5, coat=0.3), exp)
GR = M((0.95, 0.72, 0.38), rough=0.6, coat=0.25)
GRW = M((0.62, 0.42, 0.24), rough=0.4, coat=0.4)
BR = M((0.3, 0.6, 1.0), rough=0.2, coat=0.6, emit=0.3)
pts = [(-0.08, 0), (0.08, 0), (0.0, 0.13), (-0.16, 0.13), (0.16, 0.13), (-0.08, 0.26), (0.08, 0.26), (0.0, 0.39)]
for k, (px, pz) in enumerate(pts):
    g = C.empty('dgrain', exp, (-0.28 + px * 1.15, -0.03, 0.05 + pz))
    C.sphere('g', (0, 0, 0), (0.055,) * 3, GR, g, 16)
    if pz > 0.0:
        K(g, 'location', 660, tuple(g.location))
        K(g, 'location', 676, (-0.28 + px * 2.2 + (0.05 if k % 2 else -0.05), -0.03, 0.02 + (0.03 if k % 3 else 0.0)))
for px, pz in pts:
    C.sphere('wgrain', (0.28 + px * 0.95, -0.03, 0.05 + pz * 0.88), (0.055,) * 3, GRW, exp, 16)
for a, b in ((0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 5), (4, 6), (5, 6), (5, 7), (6, 7), (0, 3), (1, 4)):
    xa, za = pts[a]
    xb, zb = pts[b]
    C.sphere('bridge', (0.28 + (xa + xb) / 2 * 0.95, -0.06, 0.05 + (za + zb) / 2 * 0.88), (0.03, 0.02, 0.03), BR, exp, 10)
T.pop_in(exp, 604, 1.2, 10)
T.pop_out(exp, 764, 1.2, 6)
label('SECA', RC, (-0.34, -2.14, 1.86), 0.5, 618, 764, 0.2, 0.13)
label('CON AGUA', BC, (0.34, -2.14, 1.86), 0.62, 632, 764, 0.2, 0.12)
label('¡SE CAE!', RC, (-0.5, -1.9, 1.55), 0.86, 790, TOTAL + 10, 0.32, 0.2)
label('¡AGUANTA!', GC, (0.5, -1.9, 1.55), 0.9, 804, TOTAL + 10, 0.32, 0.19)
confetti(846, (0, -1.6, 1.5), n=30, spread=1.6)

OP = ((-0.62, -3.75, 1.05), (-0.58, -1.6, 0.48), 30)
W = ((0.0, -5.6, 1.35), (0.0, -1.6, 0.62), 28)
CU = ((0.0, -2.85, 1.15), (0.0, -1.6, 0.46), 30)
EXP = ((0.0, -4.95, 1.62), (0.0, -2.05, 1.45), 28)
FIN = ((0.0, -5.6, 1.35), (0.0, -1.6, 0.95), 28)
for a, b, pose in ((0, 88, OP), (90, 290, W), (292, 420, CU), (422, 462, W), (464, 598, CU), (600, 766, EXP), (768, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

T.arm(luma, 'R', 0, fwd=-60, out=35)
T.arm(luma, 'R', 26, fwd=-60, out=35)
T.rest_arm(luma, 'R', 40)
gesture(luma, 'hops', 44)
T.arm(ruki, 'R', 94, 0, None)
T.arm(ruki, 'R', 104, fwd=-70, out=30)
T.arm(ruki, 'R', 364, fwd=-70, out=30)
T.rest_arm(ruki, 'R', 376)
T.arm(luma, 'R', 334, 0, None)
T.arm(luma, 'R', 342, fwd=-70, out=30)
T.arm(luma, 'R', 356, fwd=-70, out=30)
T.rest_arm(luma, 'R', 366)
gesture(ruki, 'hops', 380)
T.arm(luma, 'R', 466, 0, None)
T.arm(luma, 'R', 474, fwd=-70, out=30)
T.arm(luma, 'R', 494, fwd=-70, out=30)
T.rest_arm(luma, 'R', 504)
gesture(luma, 'hops', 520)
gesture(ruki, 'breathe', 604)
T.arm(luma, 'R', 770, 0, None)
T.arm(luma, 'R', 780, fwd=-60, out=60)
T.arm(luma, 'R', 830, fwd=-60, out=60)
T.rest_arm(luma, 'R', 840)
C.wave(luma, 'L', 850, cycles=2, period=10)
C.wave(ruki, 'R', 846, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(luma, (50, 170, 320, 450, 580, 720, 860))
T.blinks(ruki, (60, 180, 340, 480, 640, 760))
