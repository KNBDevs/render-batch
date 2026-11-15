from stage import *
from episodes.bola_barquito_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'bola_barquito'
Z0 = 0.08
auto_dress(EID, ENV)
GOLDL = (1.0, 0.82, 0.4)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, GOLDL, 0.68), (80, GOLDL, 0.68), (94, base, 0.6)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.95, 0.7, 0.2, 1)), (80, (0.95, 0.7, 0.2, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

rnd = random.Random(7201)
JY = -1.55
TX = -0.1
TW, TD, TH = 1.2, 0.5, 0.55
WL = 0.4
BOT = Z0 + 0.06
WT = BOT + WL
CORAL = M((1.0, 0.55, 0.5), rough=0.35, coat=0.7)
MINT = M((0.5, 0.86, 0.72), rough=0.4, coat=0.6)
SUN = M((1.0, 0.82, 0.38), rough=0.4, coat=0.6)

tank = C.empty('glass_tank', None, (TX, JY, Z0))
C.rounded_box('base', (0, 0, 0.03), (TW + 0.1, TD + 0.1, 0.06), 0.3, MINT, tank)
for sx in (-1, 1):
    for sy in (-1, 1):
        C.sphere('foot', (sx * (TW / 2), sy * (TD / 2), 0.0), (0.05, 0.05, 0.03), SUN, tank, 16)
C.rounded_box('glass', (0, 0, 0.06 + TH / 2), (TW, TD, TH), 0.03, MA((0.92, 0.97, 1.0), 0.04), tank)
C.rounded_box('water', (0, 0, 0.06 + WL / 2), (TW - 0.03, TD - 0.03, WL), 0.02, MA((0.2, 0.55, 1.0), 0.4, rough=0.05, emit=0.08), tank)


def rect(z, inset, rad, m, name):
    hx, hy = TW / 2 - inset, TD / 2 - inset
    C.tube(name, [(-hx, -hy, z), (hx, -hy, z), (hx, hy, z), (-hx, hy, z), (-hx, -hy, z)], rad, m, tank)


rect(0.06 + TH, 0.0, 0.016, CORAL, 'rim')
rect(0.06 + WL, 0.018, 0.007, MA((0.3, 0.65, 1.0), 0.75, rough=0.05, emit=0.3), 'surface')
for k in range(7):
    x = -TW / 2 + 0.12 + k * (TW - 0.24) / 6
    C.sphere('bead', (x, -TD / 2 - 0.01, 0.06 + TH + 0.0), (0.02, 0.014, 0.02), M([(0.55, 0.8, 0.98), (1.0, 0.85, 0.45)][k % 2], rough=0.35, coat=0.7), tank, 12)

FOIL = M((0.6, 0.64, 0.74), rough=0.15, coat=1.0)
FOIL2 = M((0.88, 0.9, 0.96), rough=0.2, coat=0.9, emit=0.08)


def foil_ball(name):
    o = C.empty(name, None, (0, JY, 2.0))
    C.sphere('core', (0, 0, 0), (0.1, 0.1, 0.095), FOIL, o, 20)
    for k in range(14):
        a, b = rnd.uniform(0, 6.2832), rnd.uniform(-1.2, 1.2)
        d = Vector((math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b))) * 0.085
        C.sphere('facet', tuple(d), (0.035, 0.035, 0.022), FOIL2 if k % 2 else FOIL, o, 6, rot=(rnd.uniform(0, 3), rnd.uniform(0, 3), 0))
    return o


BA = foil_ball('foil_ball_a')
BB = foil_ball('foil_ball_b')
SR = 0.1

sheet = C.empty('foil_sheet', None, (0, JY, 2.0))
C.rounded_box('s', (0, 0, 0), (0.36, 0.3, 0.008), 0.3, FOIL, sheet)
for k in range(5):
    C.tube('crease', [(-0.17, -0.13 + k * 0.065, 0.006), (0.17, -0.13 + k * 0.065 + rnd.uniform(-0.02, 0.02), 0.006)], 0.003, FOIL2, sheet)

boat = C.empty('foil_boat', None, (0, JY, 2.0))
C.lathe('hull', [(0.0, 0.0), (0.0, 0.13), (0.015, 0.15), (0.09, 0.18), (0.1, 0.178), (0.026, 0.135), (0.014, 0.0)], FOIL, boat, segs=40, sx=1.45, sy=0.95)
C.tube('lip', [(math.cos(k * 6.2832 / 40) * 0.18 * 1.45, math.sin(k * 6.2832 / 40) * 0.18 * 0.95, 0.095 + 0.006 * math.sin(k * 2.3)) for k in range(41)], 0.009, FOIL2, boat)
for k in range(6):
    a = k * 6.2832 / 6 + 0.3
    C.tube('fold', [(math.cos(a) * 0.13 * 1.45, math.sin(a) * 0.13 * 0.95, 0.02), (math.cos(a) * 0.175 * 1.45, math.sin(a) * 0.175 * 0.95, 0.09)], 0.005, FOIL2, boat)

SX0, SY0 = 0.05, JY - 0.62
stool = spawn('low_table', 1, 7202, 'candy', (SX0, SY0, Z0), 0.55, 0)
K(stool, 'scale', 0, (0, 0, 0))
T.pop_in(stool, 118, 0.55, 8)
K(stool, 'scale', 378, (0.55,) * 3)
K(stool, 'scale', 386, (0, 0, 0))
SP = Vector((SX0, SY0, Z0 + 0.62 * 0.55 + SR))


def at(o, f, p):
    K(o, 'location', f, tuple(p))


XA, XB = TX - 0.3, TX + 0.2
BZ = BOT + SR
at(BA, 0, (XA, JY, WT + 0.36))
at(BA, 12, (XA, JY, WT + 0.36))
at(BA, 22, (XA, JY, WT - 0.02))
at(BA, 38, (XA, JY, BZ + 0.01))
at(BA, 42, (XA, JY, BZ - 0.004))
at(BA, 46, (XA, JY, BZ))
K(BB, 'scale', 0, (0, 0, 0))
at(BB, 0, SP)
T.pop_in(BB, 122, 1.0, 8)
K(BB, 'scale', 262, (1, 1, 1))
K(BB, 'scale', 270, (1.3, 1.3, 0.6))
K(BB, 'scale', 278, (0, 0, 0))
K(sheet, 'scale', 0, (0, 0, 0))
at(sheet, 0, SP + Vector((0, 0, -SR + 0.01)))
K(sheet, 'scale', 270, (0, 0, 0))
K(sheet, 'scale', 282, (1.1, 1.1, 1.0))
K(sheet, 'scale', 288, (1, 1, 1))
for f in (292, 316):
    K(sheet, 'rotation_euler', f, (0, 0, 0))
    K(sheet, 'rotation_euler', f + 6, (math.radians(14), 0, 0))
    K(sheet, 'rotation_euler', f + 12, (0, 0, 0))
K(sheet, 'scale', 334, (1, 1, 1))
K(sheet, 'scale', 342, (0, 0, 0))
BP0 = SP + Vector((0, 0, -SR + 0.01))
K(boat, 'scale', 0, (0, 0, 0))
at(boat, 0, BP0)
T.pop_in(boat, 340, 1.0, 8)
at(boat, 376, BP0)
BF = Vector((XB, JY, WT - 0.035))
at(boat, 392, (XB + 0.2, JY, WT + 0.45))
at(boat, 402, BF + Vector((0, 0, 0.12)))
at(boat, 408, BF - Vector((0, 0, 0.025)))
at(boat, 414, BF + Vector((0, 0, 0.012)))
at(boat, 420, BF)
for f in range(426, TOTAL - 1, 18):
    at(boat, f, BF + Vector((0, 0, 0.01 if (f // 18) % 2 else -0.008)))
    K(boat, 'rotation_euler', f, (math.radians(3 if (f // 18) % 2 else -3), 0, 0))

RIP = MA((0.85, 0.95, 1.0), 0.7, rough=0.05, emit=0.4)
for k in range(3):
    r = C.empty('ripple', None, (XB, JY, WT + 0.004))
    C.tube('r', [(math.cos(a * 6.2832 / 40) * 0.2, math.sin(a * 6.2832 / 40) * 0.12, 0) for a in range(41)], 0.006, RIP, r)
    f0 = 408 + k * 8
    K(r, 'scale', 0, (0, 0, 0))
    K(r, 'scale', f0, (0.9, 0.9, 1))
    K(r, 'scale', f0 + 22, (1.9, 1.7, 1))
    K(r, 'scale', f0 + 24, (0, 0, 0))

BUB = MA((0.95, 0.98, 1.0), 0.6, rough=0.05, emit=0.3)
for k in range(9):
    b = C.empty('bubble', None, (XA + rnd.uniform(-0.08, 0.08), JY + rnd.uniform(-0.1, 0.04), WT - 0.05))
    C.sphere('bub', (0, 0, 0), (0.015, 0.015, 0.015), BUB, b, 12)
    f0 = 22 + k * 3
    K(b, 'scale', 0, (0, 0, 0))
    K(b, 'scale', f0, (0, 0, 0))
    K(b, 'scale', f0 + 2, (1, 1, 1))
    K(b, 'location', f0, (b.location.x, b.location.y, BOT + 0.15))
    K(b, 'location', f0 + 20, (b.location.x, b.location.y, WT - 0.02))
    K(b, 'scale', f0 + 20, (1, 1, 1))
    K(b, 'scale', f0 + 24, (0, 0, 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, BC, RC = (0.05, 0.42, 0.15), (0.1, 0.3, 0.8), (0.8, 0.3, 0.1)
label('¿FLOTA?', GC, (-0.5, -1.3, 1.62), 1.0, 196, 266, 0.34, 0.24)
label('¿SE HUNDE?', RC, (0.55, -1.3, 1.62), 1.3, 204, 266, 0.34, 0.24)
label('MISMO PAPEL', BC, (SX0, SY0 - 0.12, 0.88), 0.44, 272, 344, 0.11, 0.055)
label('¡FLOTA!', GC, (XB, -1.95, 1.0), 0.62, 430, 580, 0.24, 0.15)
label('AL FONDO', RC, (XA - 0.12, -1.95, 1.0), 0.72, 508, 580, 0.24, 0.14)

exp = C.empty('diagram', None, (0.0, -2.45, 1.12))
C.rounded_box('panel', (0, 0.04, 0.42), (1.24, 0.03, 0.9), 0.4, M((0.66, 0.8, 0.98), rough=0.6, coat=0.2), exp)
WAT = M((0.15, 0.45, 0.95), rough=0.5, coat=0.3)
GLS = M((0.98, 0.99, 1.0), rough=0.4, coat=0.4)
UP = M((0.05, 0.55, 0.2), rough=0.4, coat=0.5)
SIL = M((0.8, 0.82, 0.88), rough=0.3, coat=0.7)
for x, wide in ((-0.3, False), (0.3, True)):
    C.rounded_box('cup', (x, 0.0, 0.32), (0.44, 0.02, 0.56), 0.3, GLS, exp)
    C.rounded_box('wat', (x, -0.012, 0.27), (0.38, 0.02, 0.4), 0.3, WAT, exp)
    if wide:
        C.rounded_box('hull', (x, -0.05, 0.5), (0.3, 0.014, 0.1), 0.5, M((0.45, 0.48, 0.58), rough=0.3, coat=0.7), exp)
        C.rounded_box('bump', (x, -0.026, 0.46), (0.36, 0.014, 0.04), 0.5, M((0.35, 0.7, 1.0), rough=0.4, emit=0.3), exp)
        L, rad, z0 = 0.22, 0.026, 0.16
    else:
        C.sphere('ball', (x, -0.04, 0.13), (0.07, 0.014, 0.07), SIL, exp, 20)
        L, rad, z0 = 0.1, 0.012, 0.2
    xs = (x - 0.08, x + 0.08) if wide else (x,)
    for xx in xs:
        C.tube('shaft', [(xx, -0.05, z0), (xx, -0.05, z0 + L - 0.03)], rad, UP, exp)
        C.lathe('tip', [(0.0, 0.0), (0.0, rad * 2.4), (0.06, 0.0)], UP, C.empty('t', exp, (xx, -0.05, z0 + L - 0.035)), segs=20)
T.pop_in(exp, 590, 1.2, 10)
T.pop_out(exp, 770, 1.2, 6)
label('BOLA', RC, (-0.3, -2.55, 2.0), 0.5, 600, 770, 0.19, 0.12)
label('BARQUITO', BC, (0.3, -2.55, 2.0), 0.66, 612, 770, 0.19, 0.1)
label('¡EMPUJA!', GC, (0.3, -2.55, 1.08), 0.74, 660, 770, 0.19, 0.12)

label('AL FONDO', RC, (XA - 0.12, -1.95, 1.05), 0.86, 790, TOTAL + 10, 0.27, 0.16)
label('¡FLOTA!', GC, (XB + 0.1, -1.95, 1.05), 0.8, 826, TOTAL + 10, 0.27, 0.17)
confetti(856, (0, -1.6, 1.3), n=26, spread=1.5)

OP = ((XA + 0.1, -2.75, 0.8), (XA + 0.1, JY, 0.42), 24)
W = ((0.0, -4.65, 1.5), (0.0, -1.45, 0.7), 17)
FOLD = ((SX0, -3.0, 1.0), (SX0, SY0, 0.55), 30)
CU = ((-0.07, -3.55, 1.05), (-0.07, JY, 0.45), 22)
EXP = ((0.0, -4.7, 1.62), (0.0, -2.45, 1.52), 30)
for a, b, pose in ((0, 52, OP), (54, 262, W), (264, 376, FOLD), (378, 424, CU), (426, 584, W), (586, 772, EXP), (774, TOTAL - 1, W)):
    camkey(a, pose)
    camkey(b, pose)

luma = make('luma', 1.1)
ruki = make('ruki', 1.1)
LM, RK = Vector((-1.04, -1.3, Z0)), Vector((1.08, -1.15, Z0))
T.turn(luma, 0, 25)
T.turn(ruki, 0, -25)
for ch, p0, dx in ((luma, LM, -0.6), (ruki, RK, 0.6)):
    for fa, fb in ((0, 52), (376, 424)):
        T.place(ch, fa, p0 + Vector((dx, 0, 0)))
        T.place(ch, fb, p0 + Vector((dx, 0, 0)))
        T.place(ch, fb + 2, p0)
    T.place(ch, 584, p0)
    T.place(ch, 586, p0 + Vector((dx * 1.6, 0, 0)))
    T.place(ch, 772, p0 + Vector((dx * 1.6, 0, 0)))
    T.place(ch, 774, p0)

T.arm(luma, 'L', 4, 0, None)
T.arm(luma, 'L', 12, fwd=-75, out=20)
T.arm(luma, 'L', 30, fwd=-75, out=20)
T.rest_arm(luma, 'L', 40)
T.arm(ruki, 'R', 106, 0, None)
T.arm(ruki, 'R', 116, fwd=-80, out=25)
T.arm(ruki, 'R', 140, fwd=-80, out=25)
T.rest_arm(ruki, 'R', 150)
for ch, side, f0 in ((luma, 'L', 188), (ruki, 'R', 380), (luma, 'L', 506), (luma, 'L', 786), (luma, 'L', 822)):
    T.arm(ch, side, f0, 0, None)
    T.arm(ch, side, f0 + 6, fwd=-85, out=30)
    T.arm(ch, side, f0 + 20, fwd=-85, out=30)
    T.rest_arm(ch, side, f0 + 28)
gesture(luma, 'hops', 58)
gesture(ruki, 'hops', 432)
C.wave(luma, 'R', 860, cycles=2, period=10)
C.wave(ruki, 'L', 856, cycles=2, period=10)
gesture(ruki, 'hops', 846)

T.lines(EID, LINES)
T.blinks(luma, (60, 170, 330, 470, 620, 740, 880))
T.blinks(ruki, (70, 200, 360, 500, 650, 790))
