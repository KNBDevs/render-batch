from stage import *
from episodes.pasas_bailan_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'pasas_bailan'
Z0 = 0.08
auto_dress(EID, ENV)
TINT = (0.9, 0.5, 1.0)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, TINT, 1.1), (80, TINT, 1.1), (94, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.62, 0.3, 0.85, 1)), (80, (0.62, 0.3, 0.85, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

rnd = random.Random(6301)
TS = 0.8
spawn('low_table', 0, 6303, 'pastel', (0.0, -1.6, Z0), TS, 0)
ZT = Z0 + 0.62 * TS
GL = MA((0.92, 0.97, 1.0), 0.035)
R, TH, H, WL = 0.23, 0.012, 0.5, 0.41
RI = R - TH - 0.006
BOT = ZT + 0.03
WT = ZT + WL


def glass(name, x, y, water_rgb, band_rgb):
    g = C.empty(name, None, (x, y, ZT))
    out = [(0, 0.0), (0, R - 0.02), (0.02, R), (H - 0.04, R + 0.01), (H, R + 0.03), (H + 0.012, R + 0.03)]
    inn = [(H + 0.012, R - TH + 0.03), (H - 0.03, R - TH + 0.01), (0.03, R - TH), (0.03, 0.0)]
    C.lathe('glass', out + inn, GL, g, segs=64)
    C.tube('band', [(math.cos(k * 6.2832 / 64) * (R + 0.006), math.sin(k * 6.2832 / 64) * (R + 0.006), 0.06) for k in range(65)], 0.012, M(band_rgb, rough=0.35, coat=0.7), g)
    C.lathe('water', [(0.03, 0.0), (0.03, RI), (WL, RI + 0.008), (WL, 0.0)], MA(water_rgb, 0.18, rough=0.05), g, segs=56)
    C.tube('surface', [(math.cos(k * 6.2832 / 64) * (RI + 0.004), math.sin(k * 6.2832 / 64) * (RI + 0.004), WL) for k in range(65)], 0.007, MA(water_rgb, 0.75, rough=0.05, emit=0.3), g)
    return g


GA, GB = Vector((-0.29, -1.64, 0)), Vector((0.29, -1.64, 0))
glass('fizzy', GA.x, GA.y, (0.55, 0.85, 1.0), (1.0, 0.55, 0.75))
glass('still', GB.x, GB.y, (0.35, 0.62, 1.0), (0.55, 0.85, 0.7))

bottle = C.empty('bottle', None, (0.0, -1.42, ZT))
bottle.scale = (0.8, 0.8, 0.8)
C.lathe('body', [(0, 0.0), (0, 0.12), (0.03, 0.135), (0.42, 0.135), (0.52, 0.09), (0.6, 0.05), (0.66, 0.05), (0.66, 0.0)], MA((0.6, 0.95, 0.85), 0.3, rough=0.08), bottle, segs=48)
C.lathe('cap', [(0.64, 0.0), (0.64, 0.058), (0.72, 0.058), (0.73, 0.04), (0.735, 0.0)], M((1.0, 0.55, 0.75), rough=0.35, coat=0.7), bottle, segs=32)
C.lathe('label', [(0.16, 0.139), (0.34, 0.139)], M((1.0, 0.97, 0.9), rough=0.5, coat=0.3), bottle, segs=48)
for k in range(9):
    a = math.radians(-60 + k * 15)
    zz = 0.2 + 0.11 * ((k * 5) % 3) / 2
    C.sphere('dot', (math.sin(a) * 0.142, -math.cos(a) * 0.142, zz), (0.014, 0.014, 0.014), M((0.4, 0.7, 1.0), rough=0.3, coat=0.8, emit=0.2), bottle, 10)

RAI = M((0.36, 0.12, 0.3), rough=0.55, coat=0.35)
RAI2 = M((0.26, 0.07, 0.22), rough=0.6, coat=0.2)
BUB = MA((0.95, 0.98, 1.0), 0.55, rough=0.05, emit=0.35)


def raisin(name, s=1.0):
    r = C.empty(name, None, (0, 0, 0))
    C.sphere('r', (0, 0, 0), (0.05 * s, 0.038 * s, 0.034 * s), RAI, r, 20, (0, 0, rnd.uniform(0, 3)))
    for k in range(4):
        a = rnd.uniform(0, 6.28)
        C.tube('w', [(math.cos(a + t) * 0.046 * s, math.sin(a + t) * 0.034 * s, (t - 0.3) * 0.03 * s) for t in (0, 0.3, 0.6)], 0.006 * s, RAI2, r)
    return r


def stick_bubbles(r, n, s, f_grow, f_pop):
    out = []
    for k in range(n):
        a = k * 6.2832 / n + 0.4
        b = C.empty('sbe', r, (math.cos(a) * 0.05 * s, math.sin(a) * 0.04 * s, 0.025 * s + 0.01 * (k % 2)))
        C.sphere('sb', (0, 0, 0), (0.017 * s, 0.017 * s, 0.017 * s), BUB, b, 12)
        out.append(b)
    return out


def dance(r, bubs, x, y, f0, f1, ph, dz=0.0):
    per = 64
    zb, zt = BOT + 0.04 + dz, WT - 0.03
    for b in bubs:
        K(b, 'scale', 0, (0, 0, 0))
    f = f0 + ph
    K(r, 'location', f0, (x, y, zb))
    while f + per < f1:
        for i, b in enumerate(bubs):
            K(b, 'scale', f, (0, 0, 0))
            K(b, 'scale', f + 6 + 3 * i, (1, 1, 1))
            K(b, 'scale', f + 38, (1, 1, 1))
            K(b, 'scale', f + 42, (0, 0, 0))
        K(r, 'location', f + 14, (x, y, zb))
        K(r, 'location', f + 34, (x + 0.01, y, zt))
        K(r, 'location', f + 42, (x - 0.01, y, zt + 0.01))
        K(r, 'location', f + 58, (x, y, zb))
        f += per


fizzy_r = []
for k, (dx, dy, ph) in enumerate(((-0.08, 0.02, 0), (0.07, -0.04, 22), (0.0, 0.07, 42))):
    r = raisin('raisin_a%d' % k, 1.7)
    bubs = stick_bubbles(r, 3, 1.7, 0, 0)
    dance(r, bubs, GA.x + dx, GA.y + dy, 0, TOTAL, ph, 0.01 * k)
    fizzy_r.append(r)

for k in range(16):
    b = C.empty('fizz', None, (GA.x + rnd.uniform(-0.13, 0.13), GA.y + rnd.uniform(-0.1, 0.08), BOT))
    C.sphere('b', (0, 0, 0), (0.011, 0.011, 0.011), BUB, b, 10)
    per = rnd.randint(30, 46)
    f = -rnd.randint(0, per)
    while f < TOTAL:
        K(b, 'location', max(f, 0), (b.location.x, b.location.y, BOT + 0.02))
        K(b, 'location', f + per - 1, (b.location.x + 0.01, b.location.y, WT - 0.01))
        K(b, 'scale', f + per - 2, (1, 1, 1))
        K(b, 'scale', f + per - 1, (0, 0, 0))
        K(b, 'scale', f + per, (1, 1, 1))
        f += per

still_r = []
for k, (dx, dy) in enumerate(((-0.08, 0.03), (0.07, -0.03), (0.0, 0.07))):
    r = raisin('raisin_b%d' % k, 1.7)
    px, py, pz = 0.72 + 0.04 * k, -1.9, ZT + 0.12 + 0.03 * k
    K(r, 'location', 0, (px, py, pz))
    f = 296 + 8 * k
    T.pop_in(r, 284, 1.0, 6)
    K(r, 'location', f, (px, py, pz))
    K(r, 'location', f + 12, (GB.x + dx, GB.y + dy, WT + 0.3))
    K(r, 'location', f + 18, (GB.x + dx, GB.y + dy, WT))
    K(r, 'location', f + 34, (GB.x + dx, GB.y + dy, BOT + 0.035))
    K(r, 'location', f + 38, (GB.x + dx, GB.y + dy, BOT + 0.04))
    K(r, 'location', f + 42, (GB.x + dx, GB.y + dy, BOT + 0.035))
    still_r.append(r)


def at(o, f, p):
    K(o, 'location', f, tuple(p))


pimo = make('pimo', 1.1)
bol = make('bolita', 1.1)
PP, BP = Vector((-1.03, -1.6, Z0)), Vector((1.03, -1.6, Z0))
T.place(pimo, 0, PP)
T.turn(pimo, 0, 25)
T.place(bol, 0, BP)
T.turn(bol, 0, -25)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, BC, RC = (0.05, 0.42, 0.15), (0.1, 0.3, 0.8), (0.8, 0.35, 0.05)
label('SIN GAS', BC, (GB.x, -1.95, ZT + 0.62), 0.62, 120, 296, 0.22, 0.13)
label('CON GAS', RC, (GA.x, -1.95, ZT + 0.62), 0.62, 128, 296, 0.22, 0.13)
label('¿SUBEN?', GC, (-0.45, -1.1, 2.0), 0.8, 216, 296, 0.32, 0.2)
label('¿ABAJO?', RC, (0.5, -0.9, 2.15), 0.8, 224, 296, 0.32, 0.2)
label('¡QUIETAS!', BC, (GB.x + 0.1, -2.0, ZT + 0.66), 0.86, 362, 466, 0.26, 0.17)

exp = C.empty('zoom', None, (0.0, -2.0, 1.3))
C.rounded_box('panel', (0, 0.04, 0.35), (1.1, 0.03, 0.95), 0.4, MA((0.55, 0.85, 1.0), 0.55, rough=0.1, emit=0.2), exp)
big = C.empty('big_raisin', exp, (0, -0.02, 0.0))
big.scale = (1.6, 1.6, 1.6)
C.sphere('r', (0, 0, 0), (0.15, 0.11, 0.1), RAI, big, 32)
for k in range(5):
    a = k * 1.25
    C.tube('w', [(math.cos(a + t) * 0.14, -0.06, math.sin(a + t) * 0.08) for t in (0, 0.35, 0.7)], 0.012, RAI2, big)
bigb = []
for k, (bx, bz) in enumerate(((-0.17, 0.06), (0.17, 0.05), (-0.07, 0.12), (0.08, 0.12), (0.0, -0.11))):
    b = C.empty('bbe', big, (bx, -0.06, bz))
    C.sphere('bb', (0, 0, 0), (0.055, 0.055, 0.055), BUB, b, 16)
    bigb.append(b)
T.pop_in(exp, 600, 1.0, 10)
T.pop_out(exp, 764, 1.0, 6)
for b in bigb:
    K(b, 'scale', 0, (0, 0, 0))
for i, b in enumerate(bigb):
    for c0 in (612, 690):
        K(b, 'scale', c0 + 4 * i, (0, 0, 0))
        K(b, 'scale', c0 + 6 + 4 * i, (1, 1, 1))
        K(b, 'scale', c0 + 46, (1, 1, 1))
        K(b, 'scale', c0 + 50, (0, 0, 0))
for c0 in (612, 690):
    K(big, 'location', c0 + 24, (0, -0.02, 0.0))
    K(big, 'location', c0 + 44, (0, -0.02, 0.5))
    K(big, 'location', c0 + 52, (0, -0.02, 0.5))
    K(big, 'location', c0 + 72, (0, -0.02, 0.0))
label('¡COMO GLOBOS!', BC, (0.0, -2.1, 2.22), 1.1, 640, 764, 0.24, 0.15)
label('¡A BAILAR!', GC, (GA.x - 0.12, -2.0, ZT + 0.66), 0.86, 790, TOTAL + 10, 0.26, 0.17)
label('¡QUIETAS!', BC, (GB.x + 0.12, -2.0, ZT + 0.98), 0.86, 806, TOTAL + 10, 0.26, 0.17)
confetti(846, (0, -1.6, 1.6), n=30, spread=1.6)

OP = ((-0.62, -4.15, 1.08), (-0.62, -1.6, 0.86), 30)
W = ((0.0, -5.5, 1.8), (0.0, -1.6, 0.95), 28)
CB = ((0.62, -4.15, 1.08), (0.62, -1.6, 0.86), 30)
CA = ((-0.55, -4.2, 1.12), (-0.55, -1.6, 0.86), 30)
EXP = ((0.0, -4.7, 1.75), (0.0, -1.8, 1.45), 28)
FIN = ((0.0, -5.6, 1.72), (0.0, -1.6, 1.0), 28)
for a, b, pose in ((0, 88, OP), (90, 290, W), (292, 462, CB), (464, 594, CA), (596, 766, EXP), (768, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

T.arm(pimo, 'R', 8, 0, None)
T.arm(pimo, 'R', 18, fwd=-70, out=30)
T.arm(pimo, 'R', 60, fwd=-70, out=30)
T.rest_arm(pimo, 'R', 72)
gesture(pimo, 'hops', 30)
T.arm(bol, 'L', 96, 0, None)
T.arm(bol, 'L', 108, fwd=-70, out=30)
T.arm(bol, 'L', 140, fwd=-70, out=30)
T.rest_arm(bol, 'L', 152)
T.arm(bol, 'R', 288, 0, None)
T.arm(bol, 'R', 300, fwd=-80, out=20)
T.arm(bol, 'R', 336, fwd=-80, out=20)
T.rest_arm(bol, 'R', 348)
gesture(bol, 'hops', 362)
gesture(pimo, 'hops', 478)
gesture(bol, 'breathe', 600)
T.arm(pimo, 'R', 770, 0, None)
T.arm(pimo, 'R', 780, fwd=-60, out=60)
T.arm(pimo, 'R', 830, fwd=-60, out=60)
T.rest_arm(pimo, 'R', 840)
C.wave(pimo, 'L', 850, cycles=2, period=10)
C.wave(bol, 'R', 846, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(pimo, (50, 170, 320, 450, 580, 720, 860))
T.blinks(bol, (60, 180, 340, 480, 640, 760))
