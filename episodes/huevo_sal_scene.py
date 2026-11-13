from stage import *
from episodes.huevo_sal_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'huevo_sal'
Z0 = 0.08
auto_dress(EID, ENV)
LILA = (0.95, 0.6, 1.0)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, LILA, 1.05), (80, LILA, 1.05), (94, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.62, 0.36, 0.86, 1)), (80, (0.62, 0.36, 0.86, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

JY = -1.55
JA, JB = -0.4, 0.4
R, TH, H, WL = 0.28, 0.012, 0.6, 0.5
WT = Z0 + 0.055 + WL
BOT = Z0 + 0.055 + 0.03
RI = R - TH - 0.006
rnd = random.Random(9201)


def jar(name, x, ring, bead):
    base = C.empty(name + '_base', None, (x, JY, Z0))
    C.lathe('coaster', [(0, 0.0), (0, R + 0.08), (0.02, R + 0.1), (0.05, R + 0.07), (0.055, 0.0)], M(ring, rough=0.4, coat=0.6), base, segs=56)
    for k in range(9):
        a = k * 6.2832 / 9
        C.sphere('bead', (math.cos(a) * (R + 0.075), math.sin(a) * (R + 0.075), 0.056), (0.018, 0.018, 0.014), M(bead, rough=0.35, coat=0.7), base, 12)
    j = C.empty(name, None, (x, JY, Z0 + 0.055))
    out = [(0, 0.0), (0, R - 0.02), (0.02, R), (H - 0.04, R), (H, R + 0.02), (H + 0.012, R + 0.02)]
    inn = [(H + 0.012, R - TH + 0.02), (H - 0.03, R - TH), (0.03, R - TH), (0.03, 0.0)]
    C.lathe('glass', out + inn, MA((0.92, 0.97, 1.0), 0.035), j, segs=64)
    C.tube('rim', [(math.cos(k * 6.2832 / 64) * (R + 0.02), math.sin(k * 6.2832 / 64) * (R + 0.02), H + 0.012) for k in range(65)], 0.013, M(ring, rough=0.35, coat=0.7), j)
    C.lathe('water', [(0, 0.0), (0.03, RI), (WL, RI), (WL, 0.0)], MA((0.3, 0.62, 1.0), 0.2, rough=0.05), j, segs=56)
    C.tube('surface', [(math.cos(k * 6.2832 / 64) * (RI - 0.004), math.sin(k * 6.2832 / 64) * (RI - 0.004), WL) for k in range(65)], 0.008, MA((0.3, 0.65, 1.0), 0.75, rough=0.05, emit=0.3), j)
    return j


jar('jar_a', JA, (0.55, 0.85, 0.7), (1.0, 0.85, 0.45))
jar('jar_b', JB, (1.0, 0.62, 0.55), (0.55, 0.8, 0.98))

SHELL = M((1.0, 0.62, 0.32), rough=0.45, coat=0.5, emit=0.3)
SPECK = M((0.75, 0.45, 0.25), rough=0.6, coat=0.2)


def egg(name):
    o = C.empty(name, None, (0, JY, 2.0))
    C.sphere('shell', (0, 0, 0), (0.1, 0.078, 0.078), SHELL, o, 40)
    C.sphere('tip', (-0.035, 0, 0), (0.07, 0.074, 0.074), SHELL, o, 32)
    for k in range(7):
        a, b = rnd.uniform(0, 6.2832), rnd.uniform(-0.6, 0.6)
        C.sphere('sp', (0.06 * math.cos(a) * 0.9, 0.077 * math.cos(b) * math.sin(a), 0.077 * math.sin(b)), (0.007, 0.007, 0.007), SPECK, o, 8)
    o.rotation_euler = (0, math.radians(-12), math.radians(8))
    o.scale = (1.25, 1.25, 1.25)
    return o


ea = egg('egg_a')
eb = egg('egg_b')


def at(o, f, p):
    K(o, 'location', f, tuple(p))


def bob(o, f0, f1, z, x, amp=0.01, per=30):
    for f in range(f0, f1, per // 2):
        at(o, f, (x, JY, z + (amp if (f - f0) // (per // 2) % 2 else -amp)))


EB = BOT + 0.095
EF = WT - 0.045
at(ea, 0, (JA, JY, WT + 0.32))
at(ea, 14, (JA, JY, WT + 0.32))
at(ea, 24, (JA, JY, WT - 0.02))
at(ea, 40, (JA, JY, EB + 0.01))
at(ea, 44, (JA, JY, EB - 0.004))
at(ea, 48, (JA, JY, EB))
K(eb, 'scale', 0, (0, 0, 0))
at(eb, 386, (JB, JY, WT + 0.3))
T.pop_in(eb, 388, 1.0, 6)
at(eb, 394, (JB, JY, WT + 0.3))
at(eb, 402, (JB, JY, WT - 0.04))
at(eb, 410, (JB, JY, WT - 0.17))
at(eb, 426, (JB, JY, EF + 0.02))
at(eb, 432, (JB, JY, EF))
bob(eb, 440, TOTAL - 1, EF, JB, 0.008, 32)

BUB = MA((0.95, 0.98, 1.0), 0.6, rough=0.05, emit=0.3)
for x, f00 in ((JA, 24), (JB, 404)):
    for k in range(8):
        b = C.empty('bubble', None, (x + rnd.uniform(-0.09, 0.09), JY + rnd.uniform(-0.08, 0.04), WT - 0.05))
        C.sphere('bub', (0, 0, 0), (0.015, 0.015, 0.015), BUB, b, 12)
        f0 = f00 + k * 3
        K(b, 'scale', 0, (0, 0, 0))
        K(b, 'scale', f0, (0, 0, 0))
        K(b, 'scale', f0 + 2, (1, 1, 1))
        K(b, 'location', f0, (b.location.x, b.location.y, BOT + 0.15))
        K(b, 'location', f0 + 20, (b.location.x, b.location.y, WT - 0.02))
        K(b, 'scale', f0 + 20, (1, 1, 1))
        K(b, 'scale', f0 + 24, (0, 0, 0))

BODY = M((0.55, 0.8, 0.98), rough=0.35, coat=0.75)
LID = M((1.0, 0.97, 0.93), rough=0.3, coat=0.8)
CORAL = M((1.0, 0.55, 0.5), rough=0.35, coat=0.7)
shaker = C.empty('salt_shaker', None, (0.9, -1.72, 0.62))
C.lathe('body', [(0, 0.0), (0, 0.072), (0.012, 0.086), (0.16, 0.086), (0.19, 0.074), (0.2, 0.06), (0.2, 0.0)], BODY, shaker, segs=48)
C.sphere('lid', (0, 0, 0.2), (0.074, 0.074, 0.05), LID, shaker, 32)
C.tube('band', [(math.cos(k * 6.2832 / 48) * 0.088, math.sin(k * 6.2832 / 48) * 0.088, 0.03) for k in range(49)], 0.01, CORAL, shaker)
C.tube('lidring', [(math.cos(k * 6.2832 / 48) * 0.075, math.sin(k * 6.2832 / 48) * 0.075, 0.198) for k in range(49)], 0.008, CORAL, shaker)
for k in range(7):
    a = k * 6.2832 / 6
    rr = 0.0 if k == 6 else 0.03
    C.sphere('hole', (rr * math.cos(a), rr * math.sin(a), 0.248), (0.007, 0.007, 0.004), M((0.25, 0.3, 0.45), rough=0.6), shaker, 8)
glyph('SAL', 0.07, 0.008, CORAL, shaker, (0, -0.088, 0.095))
SS = 1.6
K(shaker, 'scale', 0, (0, 0, 0))
T.pop_in(shaker, 112, SS, 8)
K(shaker, 'rotation_euler', 262, (0, 0, 0))
at(shaker, 262, (0.9, -1.72, 0.62))
PO = (JB + 0.24, JY - 0.02, WT + 0.5)
at(shaker, 276, PO)
K(shaker, 'rotation_euler', 276, (0, math.radians(-135), 0))
for k, f in enumerate((282, 302, 322)):
    at(shaker, f, (PO[0], PO[1], PO[2] + 0.06))
    at(shaker, f + 8, PO)
at(shaker, 336, PO)
K(shaker, 'rotation_euler', 336, (0, math.radians(-135), 0))
at(shaker, 350, (0.95, -1.95, Z0 + 0.0))
K(shaker, 'rotation_euler', 350, (0, 0, 0))

GRAIN = M((1.0, 1.0, 1.0), rough=0.3, coat=0.5, emit=0.2)
SP = Vector(PO) + Vector((-0.28, 0, -0.28))
for k in range(36):
    g = C.empty('grain', None, tuple(SP))
    C.sphere('g', (0, 0, 0), (0.012, 0.012, 0.012), GRAIN, g, 8)
    f0 = 280 + k * 1.5
    end = (JB + rnd.uniform(-0.1, 0.1), JY + rnd.uniform(-0.08, 0.06), BOT + 0.012)
    K(g, 'scale', 0, (0, 0, 0))
    K(g, 'scale', int(f0), (0, 0, 0))
    K(g, 'scale', int(f0) + 1, (1, 1, 1))
    at(g, int(f0), (SP.x + rnd.uniform(-0.02, 0.02), SP.y, SP.z))
    at(g, int(f0) + 6, (end[0] * 0.5 + SP.x * 0.5, end[1], WT))
    at(g, int(f0) + 18, end)
    K(g, 'scale', int(f0) + 18, (1, 1, 1))
    K(g, 'scale', int(f0) + 20, (0, 0, 0))
pile = C.empty('salt_pile', None, (JB, JY, BOT))
C.sphere('p', (0, 0, 0), (0.15, 0.13, 0.05), GRAIN, pile, 32)
K(pile, 'scale', 0, (0, 0, 0))
K(pile, 'scale', 290, (0, 0, 0))
K(pile, 'scale', 340, (1, 1, 1))
K(pile, 'scale', 352, (1, 1, 1))
K(pile, 'scale', 384, (0, 0, 0))
cloud = C.empty('salt_cloud', None, (JB, JY, BOT + 0.17))
C.sphere('c', (0, 0, 0), (RI * 0.9, RI * 0.9, 0.16), MA((1.0, 1.0, 1.0), 0.35, rough=0.2, emit=0.2), cloud, 32)
K(cloud, 'scale', 0, (0, 0, 0))
K(cloud, 'scale', 344, (0, 0, 0))
K(cloud, 'scale', 360, (1, 1, 1))
K(cloud, 'scale', 372, (1, 1, 1))
K(cloud, 'scale', 388, (0, 0, 0))

spv = C.empty('spoon_piv', None, (0.92, -1.85, 0.6))
spawn('big_spoon', 1, 9202, 'candy', (0, 0, 0), 1.45, 0, parent=spv)
K(spv, 'scale', 0, (0, 0, 0))
K(spv, 'rotation_euler', 0, (0, math.radians(-80), 0))
T.pop_in(spv, 340, 1.0, 6)
at(spv, 340, (0.92, -1.85, 0.6))
for k, f in enumerate(range(350, 386, 4)):
    a = k * 6.2832 / 4
    at(spv, f, (JB + 0.07 * math.cos(a), JY + 0.07 * math.sin(a), WT + 0.2))
at(spv, 392, (0.92, -1.85, 0.6))
T.pop_out(spv, 394, 1.0, 6)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, BC, RC = (0.05, 0.42, 0.15), (0.1, 0.3, 0.8), (0.8, 0.3, 0.1)
label('¿FLOTA?', GC, (-0.5, -1.3, 1.62), 1.0, 190, 264, 0.34, 0.24)
label('¿SE HUNDE?', RC, (0.55, -1.3, 1.62), 1.3, 198, 264, 0.34, 0.24)
label('¡FLOTA!', GC, (JB, -1.95, 1.08), 0.8, 440, 592, 0.27, 0.19)
label('AL FONDO', RC, (JA, -1.95, 1.08), 0.96, 520, 592, 0.27, 0.18)

exp = C.empty('diagram', None, (0.0, -2.45, 1.12))
C.rounded_box('panel', (0, 0.04, 0.42), (1.24, 0.03, 0.9), 0.4, M((0.9, 0.94, 1.0), rough=0.5, coat=0.3), exp)
WAT = M((0.45, 0.72, 1.0), rough=0.4, coat=0.4, emit=0.15)
GLS = M((0.98, 0.99, 1.0), rough=0.4, coat=0.4)
UP = M((0.2, 0.75, 0.35), rough=0.3, coat=0.6, emit=0.4)
for x, salty in ((-0.3, False), (0.3, True)):
    C.rounded_box('cup', (x, 0.0, 0.32), (0.4, 0.02, 0.56), 0.3, GLS, exp)
    C.rounded_box('wat', (x, -0.012, 0.29), (0.34, 0.02, 0.44), 0.3, WAT, exp)
    ez = 0.43 if salty else 0.13
    ic = C.empty('iegg', exp, (x, -0.04, ez))
    C.sphere('e', (0, 0, 0), (0.1, 0.012, 0.08), SHELL, ic, 24)
    if salty:
        for k in range(10):
            C.sphere('dot', (x + rnd.uniform(-0.14, 0.14), -0.026, rnd.uniform(0.12, 0.34)), (0.012, 0.006, 0.012), GLS, exp, 8)
    L, rad = (0.1, 0.012) if not salty else (0.24, 0.026)
    z0 = ez - 0.07 - L
    C.tube('shaft', [(x, -0.04, z0), (x, -0.04, z0 + L - 0.03)], rad, UP, exp)
    C.lathe('tip', [(0.0, 0.0), (0.0, rad * 2.4), (0.06, 0.0)], UP, C.empty('t', exp, (x, -0.04, z0 + L - 0.035)), segs=20)
T.pop_in(exp, 598, 1.2, 10)
T.pop_out(exp, 768, 1.2, 6)
label('AGUA', BC, (-0.3, -2.55, 2.0), 0.5, 606, 768, 0.19, 0.12)
label('CON SAL', RC, (0.3, -2.55, 2.0), 0.6, 616, 768, 0.19, 0.11)
label('¡EMPUJA!', GC, (0.0, -2.55, 1.08), 0.74, 660, 768, 0.19, 0.12)

label('SIN SAL', BC, (JA, -1.95, 1.1), 0.8, 784, TOTAL + 10, 0.27, 0.18)
label('CON SAL', RC, (JB, -1.95, 1.1), 0.86, 820, TOTAL + 10, 0.27, 0.18)
confetti(850, (0, -1.6, 1.3), n=26, spread=1.5)

OP = ((0.05, -2.4, 1.75), (-0.4, -1.55, 0.4), 42)
OM = ((-0.72, -3.45, 1.65), (-0.72, -1.45, 0.6), 27)
W = ((0.0, -4.9, 1.85), (0.0, -1.45, 0.75), 23)
POUR = ((0.42, -3.7, 1.35), (0.45, -1.5, 0.66), 25)
CU = ((0.0, -4.0, 1.1), (0.0, -1.5, 0.58), 24)
EXP = ((0.0, -4.7, 1.62), (0.0, -2.45, 1.52), 30)
FIN = ((0.0, -4.7, 1.6), (0.0, -1.45, 0.75), 23)
for a, b, pose in ((0, 46, OP), (48, 92, OM), (94, 268, W), (270, 434, POUR), (436, 596, CU), (598, 770, EXP), (772, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

luma = make('luma', 1.1)
tuki = make('tuki', 1.1)
LM, TK = Vector((-1.15, -1.3, Z0)), Vector((1.16, -1.28, Z0))
T.place(luma, 0, LM)
T.turn(luma, 0, 25)
T.place(tuki, 0, TK)
T.turn(tuki, 0, -25)

T.arm(luma, 'L', 4, 0, None)
T.arm(luma, 'L', 12, fwd=-75, out=20)
T.arm(luma, 'L', 20, fwd=-75, out=20)
T.rest_arm(luma, 'L', 30)
T.arm(tuki, 'R', 106, 0, None)
T.arm(tuki, 'R', 116, fwd=-80, out=25)
T.arm(tuki, 'R', 340, fwd=-80, out=25)
T.rest_arm(tuki, 'R', 352)
for f0 in (184, 514):
    T.arm(luma, 'L', f0, 0, None)
    T.arm(luma, 'L', f0 + 6, fwd=-85, out=30)
    T.arm(luma, 'L', f0 + 24, fwd=-85, out=30)
    T.rest_arm(luma, 'L', f0 + 32)
gesture(tuki, 'hops', 438)
gesture(luma, 'hops', 40)
gesture(tuki, 'breathe', 610)
T.arm(luma, 'L', 780, 0, None)
T.arm(luma, 'L', 788, fwd=-60, out=50)
T.arm(luma, 'L', 830, fwd=-60, out=50)
T.rest_arm(luma, 'L', 840)
C.wave(luma, 'R', 856, cycles=2, period=10)
C.wave(tuki, 'L', 852, cycles=2, period=10)
gesture(tuki, 'hops', 846)

T.lines(EID, LINES)
T.blinks(luma, (60, 170, 330, 470, 620, 740, 880))
T.blinks(tuki, (70, 200, 360, 500, 650, 790))
