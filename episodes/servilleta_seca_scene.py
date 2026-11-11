from stage import *
from episodes.servilleta_seca_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'servilleta_seca'
Z0 = 0.08
auto_dress(EID, ENV)
TINT = (0.55, 1.0, 0.6)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, TINT, 1.1), (80, TINT, 1.1), (94, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.3, 0.8, 0.45, 1)), (80, (0.3, 0.8, 0.45, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

rnd = random.Random(6401)
TS = 0.8
spawn('low_table', 0, 6402, 'pastel', (0.0, -1.6, Z0), TS, 0)
ZT = Z0 + 0.62 * TS
BX, BY = 0.0, -1.64
RB, HB, WL = 0.36, 0.3, 0.23
WT = ZT + WL
basin = C.empty('basin', None, (BX, BY, ZT))
C.lathe('tub', [(0, 0.0), (0, RB - 0.06), (0.03, RB - 0.03), (HB - 0.02, RB), (HB, RB + 0.03), (HB + 0.02, RB + 0.03), (HB + 0.02, RB - 0.005), (HB - 0.02, RB - 0.025), (0.04, RB - 0.07), (0.035, 0.0)], MA((0.75, 0.9, 1.0), 0.18, rough=0.1), basin, segs=64)
C.tube('rim', [(math.cos(k * 6.2832 / 64) * (RB + 0.03), math.sin(k * 6.2832 / 64) * (RB + 0.03), HB + 0.02) for k in range(65)], 0.016, M((0.45, 0.75, 1.0), rough=0.35, coat=0.7), basin)
for sx in (-1, 1):
    C.tube('handle', [(sx * (RB + 0.02), -0.09, HB - 0.03), (sx * (RB + 0.08), -0.06, HB - 0.03), (sx * (RB + 0.08), 0.06, HB - 0.03), (sx * (RB + 0.02), 0.09, HB - 0.03)], 0.018, M((0.45, 0.75, 1.0), rough=0.35, coat=0.7), basin)
C.lathe('water', [(0.04, 0.0), (0.04, RB - 0.075), (WL, RB - 0.035), (WL, 0.0)], MA((0.3, 0.62, 1.0), 0.2, rough=0.05), basin, segs=56)
C.tube('surface', [(math.cos(k * 6.2832 / 64) * (RB - 0.04), math.sin(k * 6.2832 / 64) * (RB - 0.04), WL) for k in range(65)], 0.007, MA((0.3, 0.65, 1.0), 0.75, rough=0.05, emit=0.3), basin)

R, TH, H = 0.15, 0.011, 0.34
GL = MA((0.85, 0.95, 1.0), 0.14, rough=0.05, emit=0.05)
cup = C.empty('cup', None, (BX, BY, WT + 0.14))
C.lathe('glass', [(H + 0.025, 0.0), (H + 0.025, R - 0.02), (H + 0.01, R), (0.02, R + 0.008), (0.0, R + 0.008), (0.0, R - TH), (0.03, R - TH), (H - 0.01, R - TH - 0.004), (H - 0.01, 0.0)], GL, cup, segs=56)
for zz, rr, cc in ((H * 0.55, R + 0.008, (1.0, 0.6, 0.3)), (0.006, R + 0.01, (1.0, 0.45, 0.6)), (H + 0.012, R - 0.006, (1.0, 0.45, 0.6))):
    C.tube('ring', [(math.cos(k * 6.2832 / 56) * rr, math.sin(k * 6.2832 / 56) * rr, zz) for k in range(57)], 0.011, M(cc, rough=0.35, coat=0.7), cup)
air = C.empty('air', cup, (0, 0, 0.035))
C.lathe('pocket', [(0, 0.0), (0, R - TH - 0.012), (H - 0.13, R - TH - 0.012), (H - 0.13, 0.0)], MA((1.0, 1.0, 1.0), 0.6, rough=0.2, emit=0.9), air, segs=40)
C.tube('inner_line', [(math.cos(k * 6.2832 / 40) * (R - TH - 0.01), math.sin(k * 6.2832 / 40) * (R - TH - 0.01), 0.0) for k in range(41)], 0.006, MA((0.3, 0.65, 1.0), 0.8, emit=0.3), air)
K(air, 'scale', 0, (0, 0, 0))

NA = M((1.0, 0.92, 0.5), rough=0.6, coat=0.2)
ND = M((0.4, 0.7, 1.0), rough=0.5, coat=0.3)
NB = M((1.0, 0.68, 0.8), rough=0.6, coat=0.2)
NW = M((0.72, 0.36, 0.52), rough=0.15, coat=0.9)


def napkin(name, mat, dots, s=1.0, soggy=False):
    n = C.empty(name, None, (0, 0, 0))
    for k in range(6):
        a = k * 1.05 + rnd.uniform(-0.2, 0.2)
        rr = 0.045 * s
        C.sphere('fold', (math.cos(a) * rr, math.sin(a) * rr, rnd.uniform(-0.015, 0.015) * s), ((0.055 if not soggy else 0.06) * s, 0.04 * s, (0.035 if not soggy else 0.022) * s), mat, n, 16, (rnd.uniform(-0.5, 0.5), rnd.uniform(-0.5, 0.5), a))
    for k in range(5):
        a = k * 1.26
        C.sphere('dot', (math.cos(a) * 0.075 * s, math.sin(a) * 0.075 * s - 0.01, 0.01 * s), (0.011 * s, 0.011 * s, 0.011 * s), dots, n, 8)
    return n


nap1 = napkin('napkin_yellow', NA, ND, 1.25)
nap1.parent = cup
nap1.location = (0, 0, H - 0.065)
nap2 = napkin('napkin_pink', NB, M((1.0, 0.95, 0.9), rough=0.5), 1.25)
nap2.parent = cup
nap2.location = (0, 0, H - 0.065)
nap2.scale = (0, 0, 0)
nap3 = napkin('napkin_wet', NW, M((0.85, 0.75, 0.8), rough=0.3), 1.15, True)
nap3.parent = cup
nap3.location = (0, 0, H - 0.08)
nap3.scale = (0, 0, 0)

BUB = MA((1.0, 1.0, 1.0), 0.75, rough=0.05, emit=0.7)


def at(o, f, p):
    K(o, 'location', f, tuple(p))


UP = (BX, BY, WT + 0.14)
DN = (BX, BY, ZT + 0.07)
at(cup, 0, UP)
for f in (10, 40, 70):
    at(cup, f, (BX, BY, WT + 0.11))
    at(cup, f + 15, (BX, BY, WT + 0.17))
at(cup, 296, UP)
at(cup, 316, DN)
K(air, 'scale', 314, (0, 0, 0))
K(air, 'scale', 318, (1, 1, 1))
K(air, 'scale', 338, (1, 1, 1))
K(air, 'scale', 342, (0, 0, 0))
at(cup, 338, DN)
at(cup, 356, UP)
K(nap1, 'location', 356, (0, 0, H - 0.065))
K(nap1, 'scale', 356, (1, 1, 1))
DRY = (0.3, -2.0, ZT + 0.56)
K(nap1, 'scale', 360, (0, 0, 0))
dry = napkin('napkin_dry_out', NA, ND, 2.0)
dry.location = DRY
T.pop_in(dry, 360, 1.0, 8)

T.pop_in(nap2, 464, 1.0, 8)
at(cup, 470, UP)
at(cup, 488, DN)
K(air, 'scale', 486, (0, 0, 0))
K(air, 'scale', 490, (1, 1, 1))
K(air, 'scale', 500, (1, 1, 1))
K(cup, 'rotation_euler', 498, (0, 0, 0))
K(cup, 'rotation_euler', 512, (0, math.radians(38), 0))
K(cup, 'rotation_euler', 548, (0, math.radians(38), 0))
K(cup, 'rotation_euler', 560, (0, 0, 0))
K(air, 'scale', 512, (1, 1, 1))
K(air, 'scale', 540, (1, 1, 0.02))
K(air, 'scale', 542, (0, 0, 0))
at(cup, 560, DN)
for k, (f0, s) in enumerate(((512, 0.085), (524, 0.065), (536, 0.05))):
    b = C.empty('big_bubble', None, (BX - 0.13, BY, ZT + 0.16))
    C.sphere('b', (0, 0, 0), (s, s, s * 0.85), BUB, b, 16)
    K(b, 'scale', 0, (0, 0, 0))
    K(b, 'scale', f0, (0, 0, 0))
    K(b, 'scale', f0 + 3, (1, 1, 1))
    at(b, f0, (BX - 0.13, BY, ZT + 0.16))
    at(b, f0 + 16, (BX - 0.19, BY, WT - 0.02))
    K(b, 'scale', f0 + 16, (1, 1, 1))
    K(b, 'scale', f0 + 20, (1.5, 1.5, 0.2))
    K(b, 'scale', f0 + 22, (0, 0, 0))
K(nap2, 'scale', 534, (1, 1, 1))
K(nap2, 'scale', 538, (0, 0, 0))
K(nap3, 'scale', 0, (0, 0, 0))
K(nap3, 'scale', 534, (0, 0, 0))
K(nap3, 'scale', 538, (1, 1, 1))
at(cup, 562, DN)
at(cup, 580, UP)
K(nap3, 'scale', 584, (1, 1, 1))
K(nap3, 'scale', 588, (0, 0, 0))
WET = (-0.3, -2.0, ZT + 0.56)
wet = napkin('napkin_wet_out', NW, M((0.85, 0.75, 0.8), rough=0.3), 1.9, True)
wet.location = WET
T.pop_in(wet, 588, 1.0, 8)
DROP = MA((0.3, 0.62, 1.0), 0.7, rough=0.05, emit=0.3)
for k in range(5):
    d = C.empty('drop', None, (WET[0] + rnd.uniform(-0.05, 0.05), WET[1], WET[2] - 0.06))
    C.sphere('d', (0, 0, 0), (0.014, 0.014, 0.02), DROP, d, 10)
    K(d, 'scale', 0, (0, 0, 0))
    f = 592 + k * 9
    while f < TOTAL - 20:
        K(d, 'scale', f, (0, 0, 0))
        K(d, 'scale', f + 1, (1, 1, 1))
        K(d, 'location', f, (d.location.x, d.location.y, WET[2] - 0.06))
        K(d, 'location', f + 14, (d.location.x, d.location.y, ZT + 0.03))
        K(d, 'scale', f + 14, (1, 1, 1))
        K(d, 'scale', f + 15, (0, 0, 0))
        f += 44


tuki = make('tuki', 1.1)
moki = make('moki', 1.1)
TP, MP = Vector((-1.03, -1.6, Z0)), Vector((1.03, -1.6, Z0))
T.place(tuki, 0, TP)
T.turn(tuki, 0, 25)
T.place(moki, 0, MP)
T.turn(moki, 0, -25)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, BC, RC = (0.05, 0.42, 0.15), (0.1, 0.3, 0.8), (0.8, 0.35, 0.05)
label('¿SE MOJA?', RC, (-0.45, -1.1, 2.0), 0.9, 216, 296, 0.32, 0.19)
label('¿SECA?', GC, (0.5, -0.9, 2.15), 0.8, 224, 296, 0.32, 0.2)
label('¡SECA!', GC, (0.45, -2.05, ZT + 1.02), 0.7, 364, 464, 0.26, 0.17)

exp = C.empty('diagram', None, (0.0, -2.0, 1.32))
C.rounded_box('panel', (0, 0.04, 0.35), (1.1, 0.03, 0.95), 0.4, M((1.0, 0.7, 0.5), rough=0.5, coat=0.3), exp)
C.rounded_box('water', (0, 0.0, 0.08), (0.94, 0.03, 0.42), 0.3, M((0.35, 0.62, 1.0), rough=0.3, coat=0.5, emit=0.2), exp)
GLD = M((0.25, 0.35, 0.5), rough=0.4, coat=0.5)
for x in (-0.2, 0.2):
    C.rounded_box('wall', (x, -0.03, 0.4), (0.035, 0.03, 0.66), 0.4, GLD, exp)
C.rounded_box('top', (0, -0.03, 0.73), (0.435, 0.03, 0.04), 0.4, GLD, exp)
C.rounded_box('air', (0, -0.025, 0.36), (0.36, 0.02, 0.48), 0.3, M((1.0, 1.0, 1.0), rough=0.4, coat=0.3, emit=0.4), exp)
dn = napkin('napkin_diagram', NA, ND, 1.3)
dn.parent = exp
dn.location = (0, -0.06, 0.63)
T.pop_in(exp, 604, 1.25, 10)
T.pop_out(exp, 764, 1.25, 6)
label('AIRE', BC, (0.0, -2.12, 1.8), 0.5, 624, 764, 0.22, 0.16)
label('AGUA', BC, (0.42, -2.12, 1.3), 0.5, 640, 764, 0.2, 0.13)
label('¡SECA!', GC, (0.5, -2.05, ZT + 1.02), 0.7, 790, TOTAL + 10, 0.26, 0.17)
label('¡MOJADA!', RC, (-0.5, -2.05, ZT + 1.02), 0.86, 804, TOTAL + 10, 0.26, 0.17)
confetti(846, (0, -1.6, 1.6), n=30, spread=1.6)

OP = ((-0.36, -4.3, 1.15), (-0.36, -1.6, 1.0), 30)
W = ((0.0, -5.5, 1.8), (0.0, -1.6, 0.95), 28)
CU = ((0.0, -3.3, 1.08), (0.0, -1.64, 1.02), 30)
EXP = ((0.0, -4.85, 1.85), (0.0, -1.9, 1.66), 28)
FIN = ((0.0, -5.3, 1.7), (0.0, -1.6, 1.02), 28)
for a, b, pose in ((0, 88, OP), (90, 290, W), (292, 372, CU), (374, 462, W), (464, 598, CU), (600, 766, EXP), (768, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

T.arm(tuki, 'R', 0, fwd=-70, out=30)
T.arm(tuki, 'R', 84, fwd=-70, out=30)
T.rest_arm(tuki, 'R', 96)
gesture(moki, 'hops', 104)
T.arm(tuki, 'R', 290, 0, None)
T.arm(tuki, 'R', 300, fwd=-75, out=25)
T.arm(tuki, 'R', 350, fwd=-75, out=25)
T.rest_arm(tuki, 'R', 362)
gesture(moki, 'hops', 364)
T.arm(tuki, 'R', 462, 0, None)
T.arm(tuki, 'R', 474, fwd=-75, out=25)
T.arm(tuki, 'R', 576, fwd=-75, out=25)
T.rest_arm(tuki, 'R', 588)
gesture(moki, 'breathe', 604)
T.arm(tuki, 'R', 770, 0, None)
T.arm(tuki, 'R', 780, fwd=-60, out=60)
T.arm(tuki, 'R', 830, fwd=-60, out=60)
T.rest_arm(tuki, 'R', 840)
C.wave(tuki, 'L', 850, cycles=2, period=10)
C.wave(moki, 'R', 846, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(tuki, (50, 170, 320, 450, 580, 720, 860))
T.blinks(moki, (60, 180, 340, 480, 640, 760))
