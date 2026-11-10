from stage import *
from episodes.colador_sol_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'colador_sol'
Z0 = 0.08
auto_dress(EID, ENV)
SUNC = (1.0, 0.62, 0.25)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    if l.type == 'SUN':
        for o in bpy.data.objects:
            if o.data == l:
                o.rotation_euler = (math.radians(6), math.radians(-4), 0)
        l.angle = math.radians(2)
        hi, lo = 1.9, 1.35
    else:
        hi, lo = 0.7, 0.62
    for f, c, k in ((0, SUNC, hi), (80, SUNC, hi), (92, base, lo)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (1.0, 0.7, 0.3, 1)), (80, (1.0, 0.7, 0.3, 1)), (92, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

SX, SY = 0.0, -1.75
snail = C.empty('snail', None, (SX, SY, Z0), (0, 0, math.radians(30)))
BODY = M((0.98, 0.82, 0.55), rough=0.5, coat=0.3)
SHELL = M((0.95, 0.45, 0.35), rough=0.35, coat=0.8)
SPIR = M((1.0, 0.85, 0.6), rough=0.35, coat=0.8)
EYE = M((1, 1, 1), rough=0.3, coat=0.6)
PUP = M((0.12, 0.1, 0.16), rough=0.3, coat=0.8)
C.sphere('foot', (0.02, 0, 0.05), (0.27, 0.085, 0.055), BODY, snail, 40)
C.sphere('head', (-0.2, 0, 0.12), (0.075, 0.07, 0.09), BODY, snail, 32)
RSH = 0.135
SHC = Vector((0.06, 0, 0.19))
C.sphere('shell', tuple(SHC), (RSH, RSH * 0.82, RSH), SHELL, snail, 48)
pts = []
for k in range(70):
    t = k / 69
    a = t * 6.2832 * 2.2
    rr = RSH * 0.92 * (1 - t * 0.85)
    pts.append((SHC.x + math.cos(a) * rr, -RSH * 0.82 - 0.004 + t * 0.012, SHC.z + math.sin(a) * rr))
C.tube('spiral', pts, 0.011, SPIR, snail)
C.tube('spiral2', [(x, -y, z) for x, y, z in pts], 0.011, SPIR, snail)
LIDS = []
for sy in (-1, 1):
    C.tube('stalk', [(-0.22, sy * 0.025, 0.17), (-0.25, sy * 0.04, 0.25), (-0.26, sy * 0.05, 0.3)], 0.012, BODY, snail)
    e = C.empty('eye', snail, (-0.26, sy * 0.05, 0.31))
    C.sphere('ball', (0, 0, 0), (0.036, 0.036, 0.036), EYE, e, 24)
    C.sphere('pupil', (-0.026, 0, 0.0), (0.014, 0.018, 0.018), PUP, e, 16)
    lid = C.empty('lid', e, (0, 0, 0))
    C.sphere('lidm', (0, 0, 0.0), (0.039, 0.039, 0.039), BODY, lid, 24)
    LIDS.append(lid)
C.tube('smile', [(-0.274, -0.03, 0.105), (-0.282, 0, 0.095), (-0.274, 0.03, 0.105)], 0.006, PUP, snail)
for sy in (-1, 1):
    C.sphere('blush', (-0.255, sy * 0.05, 0.12), (0.012, 0.02, 0.014), M((1.0, 0.55, 0.55), rough=0.5), snail, 12)


def lids(f, k):
    for lid in LIDS:
        K(lid, 'location', f, (0, 0, 0.04 * (1 - k) + 0.0))
        K(lid, 'scale', f, (1, 1, 1))


lids(0, 0.55)
for f in (86, 300, 466):
    lids(f, 0.55)
lids(492, 0.0)
lids(800, 0.0)
lids(822, 1.0)
for f in range(0, 470, 16):
    K(snail, 'scale', f, (1, 1, 1))
    K(snail, 'scale', f + 8, (1.02, 1.02, 0.97))

drop = C.empty('sweat', snail, (-0.17, -0.07, 0.24))
C.sphere('dr', (0, 0, 0), (0.016, 0.016, 0.024), MA((0.55, 0.85, 1.0), 0.8, rough=0.1, emit=0.2), drop, 16)
K(drop, 'location', 0, (-0.17, -0.07, 0.24))
K(drop, 'location', 40, (-0.18, -0.08, 0.14))
K(drop, 'scale', 0, (1, 1, 1))
K(drop, 'scale', 40, (1, 1, 1))
K(drop, 'scale', 46, (0, 0, 0))

sun = C.empty('sun', None, (-0.55, -0.4, 2.45))
sm = M((1.0, 0.82, 0.25), rough=0.3, coat=0.6, emit=2.2)
C.sphere('disc', (0, 0, 0), (0.24, 0.06, 0.24), sm, sun, 40)
for k in range(10):
    a = k * 6.2832 / 10
    C.sphere('ray', (0.36 * math.cos(a), 0, 0.36 * math.sin(a)), (0.06, 0.03, 0.06), sm, sun, 16)
for f in range(0, TOTAL, 24):
    K(sun, 'rotation_euler', f, (0, math.radians(f * 0.4), 0))

moki = make('moki', 1.25)
bolita = make('bolita', 1.1)
MK, BL0 = Vector((-0.66, -1.42, Z0)), Vector((0.66, -1.42, Z0))
T.place(moki, 0, MK)
T.turn(moki, 0, 25)
T.place(bolita, 0, BL0)
T.turn(bolita, 0, -25)

col = spawn('colander', 0, 5801, (0.55, 0.8, 1.0), (0, 0, 0), 1.6, 0)
col.rotation_euler = (math.radians(180), 0, 0)
CR = 0.2 * 1.6
CH = 0.2 * 1.6
CREST = Vector((-0.3, -1.92, Z0 + 0.4))
COVER = Vector((SX, SY, Z0 + 0.86))
CEXP = Vector((-0.62, -1.86, Z0 + 0.5))


def colpos(f, p, s=1.0):
    K(col, 'location', f, tuple(p))
    K(col, 'scale', f, (1.6 * s, 1.6 * s, 1.6 * s))


colpos(0, CREST, 0.0)
colpos(104, CREST, 0.0)
colpos(110, CREST, 1.15)
colpos(116, CREST, 1.0)
colpos(304, CREST)
colpos(326, COVER)
colpos(468, COVER)
colpos(486, CREST)
colpos(600, CREST)
colpos(618, CEXP)

umb = C.empty('umbrella', None, (0, 0, 0))
UC = M((0.35, 0.55, 1.0), rough=0.35, coat=0.7)
UW = M((1.0, 0.95, 0.6), rough=0.35, coat=0.7)
UR = 0.42
C.lathe('canopy', [(0.32, 0.0), (0.31, 0.12), (0.26, 0.25), (0.17, 0.35), (0.06, 0.41), (0.0, UR), (0.01, UR - 0.02), (0.065, 0.39), (0.17, 0.33), (0.25, 0.24), (0.3, 0.11), (0.305, 0.0)], UC, umb, segs=64)
for k in range(8):
    a = k * 6.2832 / 8
    C.tube('rib', [(math.cos(a) * r0, math.sin(a) * r0, z0) for z0, r0 in ((0.32, 0.02), (0.29, 0.16), (0.2, 0.31), (0.06, 0.405), (0.0, UR + 0.006))], 0.011, UW, umb)
    C.sphere('tipb', (math.cos(a) * (UR + 0.006), math.sin(a) * (UR + 0.006), -0.004), (0.02, 0.02, 0.02), UW, umb, 12)
C.sphere('top', (0, 0, 0.34), (0.03, 0.03, 0.04), UW, umb, 16)
C.tube('shaft', [(0, 0, 0.32), (0, 0, -0.42)], 0.014, M((0.98, 0.97, 0.94), rough=0.35, coat=0.6), umb)
C.tube('hook', [(0, 0, -0.42), (0, 0, -0.5), (0.03, 0, -0.56), (0.08, 0, -0.56), (0.1, 0, -0.5)], 0.024, UW, umb)
UREST = Vector((0.36, -1.6, Z0 + 1.0))
UCOV = Vector((SX + 0.02, SY, Z0 + 1.02))


def umbpos(f, p, s=1.0, tilt=0.0):
    K(umb, 'location', f, tuple(p))
    K(umb, 'scale', f, (s, s, s))
    K(umb, 'rotation_euler', f, (0, math.radians(tilt), 0))


umbpos(0, UREST, 0.0)
umbpos(200, UREST, 0.0)
umbpos(206, UREST, 1.15, 10)
umbpos(212, UREST, 1.0, 10)
umbpos(470, UREST, 1.0, 10)
umbpos(494, UCOV)

bpy.context.view_layer.update()
DOT = M((1.0, 0.92, 0.5), rough=0.4, emit=2.5)
rnd = random.Random(5802)
DOTS = []
for row, rr in enumerate((0.0, 0.1, 0.19, 0.27)):
    n = 1 if rr == 0 else 6 + row * 4
    for k in range(n):
        a = k * 6.2832 / n + row * 0.3
        x, y = SX + math.cos(a) * rr, SY + math.sin(a) * rr * 0.95
        sl = Vector((x, y, 0)) - Vector((SX, SY, 0))
        p = Vector((x, y, Z0 + 0.004))
        loc_s = snail.matrix_world.inverted() @ Vector((x, y, Z0))
        dx, dy = loc_s.x - SHC.x, loc_s.y
        if (dx / RSH) ** 2 + (dy / (RSH * 0.82)) ** 2 < 0.95:
            hz = RSH * math.sqrt(max(0.0, 1 - (dx / RSH) ** 2 - (dy / (RSH * 0.82)) ** 2))
            p = Vector((x, y, Z0 + SHC.z + hz + 0.004))
        elif abs(loc_s.y) < 0.08 and -0.28 < loc_s.x < 0.29:
            p = Vector((x, y, Z0 + 0.105))
        d = C.sphere('lightdot', tuple(p), (0.024, 0.024, 0.006), DOT, None, 12)
        DOTS.append(d)
for d in DOTS:
    for f, s in ((0, 0), (329, 0), (334, 1.15), (338, 1.0), (468, 1.0), (474, 0)):
        K(d, 'scale', f, (0.024 * s, 0.024 * s, 0.006 * s))
EDOTS = []
for d in DOTS:
    p = Vector(d.location)
    q = C.sphere('expdot', (p.x - SX + CEXP.x, p.y - SY + CEXP.y, Z0 + 0.004), (0.024, 0.024, 0.006), DOT, None, 12)
    for f, s in ((0, 0), (621, 0), (626, 1.15), (630, 1.0), (TOTAL - 1, 1.0)):
        K(q, 'scale', f, (0.024 * s, 0.024 * s, 0.006 * s))

RAYM = MA((1.0, 0.9, 0.4), 0.45, rough=0.5, emit=1.6)


def ray(p0, p1, f_in, f_out):
    o = C.tube('sunray', [tuple(p0), tuple(p1)], 0.014, RAYM, None)
    T.pop_in(o, f_in, 1.0, 8)
    T.pop_out(o, f_out, 1.0, 6)


for k, (dx, dy) in enumerate(((0.0, 0.0), (0.19, 0.0), (-0.19, 0.0), (0.1, 0.06), (-0.1, -0.06))):
    ray((CEXP.x + dx, CEXP.y + dy, 2.2), (CEXP.x + dx, CEXP.y + dy, Z0 + 0.01), 640 + k * 3, 764)
for k, dx in enumerate((-0.3, -0.15, 0.0, 0.15, 0.3)):
    ray((UCOV.x + dx, UCOV.y, 2.2), (UCOV.x + dx, UCOV.y, UCOV.z + 0.32 - 0.6 * (dx / UR) ** 2), 700 + k * 3, 764)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, BC, RC = (0.05, 0.42, 0.15), (0.1, 0.3, 0.8), (0.8, 0.35, 0.05)
label('¿COLADOR?', RC, (-0.55, -1.0, 1.85), 1.15, 216, 296, 0.32, 0.22)
label('¿PARAGUAS?', BC, (0.55, -0.75, 2.05), 1.25, 224, 296, 0.32, 0.22)
label('PASA LA LUZ', RC, (-0.38, -2.3, 1.9), 1.1, 648, 764, 0.28, 0.19)
label('SOMBRA', BC, (0.42, -2.35, 0.32), 0.9, 708, 764, 0.26, 0.19)
zz = C.empty('zzz', None, (SX - 0.25, SY - 0.2, Z0 + 0.42))
glyph('Zzz', 0.14, 0.01, M((0.25, 0.3, 0.75), rough=0.4, emit=0.3), zz)
T.pop_in(zz, 828, 1.0, 10)
K(zz, 'location', 828, (SX - 0.25, SY - 0.2, Z0 + 0.42))
K(zz, 'location', TOTAL - 1, (SX - 0.3, SY - 0.2, Z0 + 0.62))

OP = ((-0.35, -2.85, 0.34), (-0.06, -1.75, 0.24), 40)
W = ((0.0, -4.7, 1.95), (0.0, -1.55, 0.72), 28)
CU = ((-0.1, -2.95, 0.32), (-0.05, -1.75, 0.2), 50)
EXP = ((-0.05, -4.95, 2.1), (-0.05, -1.55, 0.72), 28)
FIN = ((-0.05, -4.6, 1.35), (-0.05, -1.6, 0.62), 28)
for a, b, pose in ((0, 44, OP), (46, 328, W), (330, 466, CU), (468, 594, W), (596, 766, EXP), (768, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

T.arm(bolita, 'L', 12, 0, None)
T.arm(bolita, 'L', 18, fwd=-80, out=45)
T.arm(bolita, 'L', 70, fwd=-80, out=45)
T.rest_arm(bolita, 'L', 78)
for f0, f1 in ((104, 300), (304, 468), (600, 766)):
    T.arm(moki, 'L', f0, 0, None) if f0 == 104 else None
    T.arm(moki, 'L', f0 + 6, fwd=-60, out=25)
    T.arm(moki, 'L', f1, fwd=-60, out=25)
T.rest_arm(moki, 'L', 776)
T.arm(bolita, 'R', 200, 0, None)
T.arm(bolita, 'R', 206, fwd=-125, out=20)
T.arm(bolita, 'R', 780, fwd=-125, out=20)
T.rest_arm(bolita, 'R', 790)
T.place(moki, 304, MK)
T.place(moki, 326, MK + Vector((0.2, -0.05, 0)))
T.place(moki, 468, MK + Vector((0.2, -0.05, 0)))
T.place(moki, 486, MK)
T.place(bolita, 470, BL0)
T.place(bolita, 494, BL0 + Vector((-0.24, -0.05, 0)))
gesture(bolita, 'hops', 530)
gesture(moki, 'breathe', 600)
C.wave(moki, 'R', 846, cycles=2, period=10)
C.wave(bolita, 'L', 846, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(moki, (50, 170, 320, 450, 580, 720, 860))
T.blinks(bolita, (60, 180, 340, 480, 640, 760))
