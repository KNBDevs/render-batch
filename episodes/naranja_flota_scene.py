from stage import *
from episodes.naranja_flota_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'naranja_flota'
Z0 = 0.08
auto_dress(EID, ENV)
BLUE = (0.45, 0.62, 1.0)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, BLUE, 1.1), (80, BLUE, 1.1), (94, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.25, 0.42, 0.95, 1)), (80, (0.25, 0.42, 0.95, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

JX, JY = 0.0, -1.55
R, TH, H = 0.32, 0.012, 0.56
base = C.empty('jar_base', None, (JX, JY, Z0))
C.lathe('coaster', [(0, 0.0), (0, R + 0.08), (0.02, R + 0.1), (0.05, R + 0.07), (0.055, 0.0)], M((0.55, 0.85, 0.7), rough=0.4, coat=0.6), base, segs=56)
for k in range(10):
    a = k * 6.2832 / 10
    C.sphere('bead', (math.cos(a) * (R + 0.075), math.sin(a) * (R + 0.075), 0.056), (0.018, 0.018, 0.014), M((1.0, 0.85, 0.45), rough=0.35, coat=0.7), base, 12)
jar = C.empty('jar', None, (JX, JY, Z0 + 0.055))
GL = MA((0.92, 0.97, 1.0), 0.035)
out = [(0, 0.0), (0, R - 0.02), (0.02, R), (H - 0.04, R), (H, R + 0.02), (H + 0.012, R + 0.02)]
inn = [(H + 0.012, R - TH + 0.02), (H - 0.03, R - TH), (0.03, R - TH), (0.03, 0.0)]
C.lathe('glass', out + inn, GL, jar, segs=64)
C.tube('rim', [(math.cos(k * 6.2832 / 64) * (R + 0.02), math.sin(k * 6.2832 / 64) * (R + 0.02), H + 0.012) for k in range(65)], 0.013, M((0.55, 0.85, 0.7), rough=0.35, coat=0.7), jar)
C.tube('band', [(math.cos(k * 6.2832 / 64) * (R + 0.004), math.sin(k * 6.2832 / 64) * (R + 0.004), 0.07) for k in range(65)], 0.011, M((1.0, 0.85, 0.45), rough=0.35, coat=0.7), jar)
RI = R - TH - 0.006
WL = 0.46
C.lathe('water', [(0, 0.0), (0.03, RI), (WL, RI), (WL, 0.0)], MA((0.25, 0.6, 1.0), 0.2, rough=0.05), jar, segs=56)
WT = Z0 + 0.055 + WL
C.tube('surface', [(math.cos(k * 6.2832 / 64) * (RI - 0.004), math.sin(k * 6.2832 / 64) * (RI - 0.004), WL) for k in range(65)], 0.008, MA((0.3, 0.65, 1.0), 0.75, rough=0.05, emit=0.3), jar)
BOT = Z0 + 0.055 + 0.03

PEEL = M((1.0, 0.45, 0.03), rough=0.5, coat=0.3, emit=0.25)
PORE = M((0.9, 0.4, 0.04), rough=0.6, coat=0.2)
PITH = M((1.0, 0.93, 0.78), rough=0.6, coat=0.2)
FLESH = M((1.0, 0.55, 0.12), rough=0.4, coat=0.4, emit=0.25)
LEAF = M((0.3, 0.7, 0.3), rough=0.4, coat=0.5)
RO, RP = 0.15, 0.13
rnd = random.Random(8101)
orange = C.empty('orange', None, (JX, JY, WT + 0.03))
C.sphere('o', (0, 0, 0), (RO, RO, RO * 0.95), PEEL, orange, 48)
for k in range(46):
    u, v = rnd.uniform(-1, 1), rnd.uniform(0, 6.2832)
    s = math.sqrt(1 - u * u)
    C.sphere('pore', (RO * 0.985 * s * math.cos(v), RO * 0.985 * s * math.sin(v), RO * 0.94 * u), (0.008, 0.008, 0.008), PORE, orange, 8)
C.tube('stem', [(0, 0, RO * 0.93), (0.005, 0, RO * 1.05)], 0.008, M((0.45, 0.35, 0.2), rough=0.5), orange)
lf = C.leaf('leaf', 0.09, 0.045, 0.2, LEAF, orange)
lf.location = (0.01, 0, RO * 1.02)
lf.rotation_euler = (math.radians(70), 0, math.radians(30))

peeled = C.empty('peeled', None, (0.5, -1.55, 0.95))
C.sphere('p', (0, 0, 0), (RP, RP, RP * 0.96), FLESH, peeled, 48)
for k in range(10):
    a = k * 6.2832 / 10
    C.tube('seg', [(RP * 1.005 * math.sin(t * 3.1416) * math.cos(a), RP * 1.005 * math.sin(t * 3.1416) * math.sin(a), RP * 0.965 * math.cos(t * 3.1416)) for t in [i / 16 for i in range(17)]], 0.0045, PITH, peeled)
peeled.scale = (0, 0, 0)

peel = C.empty('peel', None, (0.62, -1.9, Z0 + 0.1))
pts = []
for k in range(80):
    t = k / 79
    a = t * 6.2832 * 2.4
    rr = 0.13 * (1 - 0.25 * t)
    pts.append((math.cos(a) * rr, math.sin(a) * rr, 0.012 + 0.025 * math.sin(t * 9)))
C.tube('strip', pts, 0.024, PEEL, peel, res=8)
C.tube('strip_in', [(x * 0.97, y * 0.97, z - 0.012) for x, y, z in pts], 0.02, PITH, peel, res=8)
peel.scale = (0, 0, 0)
plate = spawn('snack_plate', 1, 8102, 'pastel', (0.62, -1.9, Z0), 1.0, 0)


def bob(o, f0, f1, z, amp=0.012, per=28):
    for f in range(f0, f1, per // 2):
        K(o, 'location', f, (o.location.x, o.location.y, z + (amp if (f - f0) // (per // 2) % 2 else -amp)))


def at(o, f, p):
    K(o, 'location', f, tuple(p))


bopi = make('bopi', 1.1)
luma = make('luma', 1.1)
BP, LM = Vector((-0.66, -1.45, Z0)), Vector((0.7, -1.45, Z0))
T.place(bopi, 0, BP)
T.turn(bopi, 0, 25)
T.place(luma, 0, LM)
T.turn(luma, 0, -25)

FL = (JX, JY, WT + 0.04)
at(orange, 0, FL)
for f0 in (12, 50):
    at(orange, f0, FL)
    at(orange, f0 + 12, (JX, JY, WT - 0.16))
    at(orange, f0 + 18, (JX, JY, WT - 0.16))
    at(orange, f0 + 24, (JX, JY, WT + 0.09))
    at(orange, f0 + 30, FL)
bob(orange, 82, 100, WT + 0.04)
at(orange, 104, FL)
LH = (0.36, -1.78, 0.74)
at(orange, 118, LH)
K(orange, 'scale', 136, (1, 1, 1))
K(orange, 'scale', 142, (0, 0, 0))
at(peeled, 136, LH)
T.pop_in(peeled, 138, 1.0, 8)
T.pop_in(peel, 140, 1.0, 8)
at(peel, 140, (0.62, -1.9, Z0 + 0.1))
at(peeled, 300, LH)
at(peeled, 318, (JX, JY, WT + 0.25))
at(peeled, 326, (JX, JY, WT))
at(peeled, 344, (JX, JY, BOT + RP))
at(peeled, 352, (JX, JY, BOT + RP + 0.012))
at(peeled, 358, (JX, JY, BOT + RP))
at(peel, 470, (0.62, -1.9, Z0 + 0.1))
at(peel, 492, (JX, JY, WT + 0.25))
at(peel, 500, (JX, JY, WT - 0.02))
at(peel, 508, (JX, JY, WT + 0.01))
bob(peel, 512, TOTAL - 1, WT, 0.008, 32)

BUB = MA((0.95, 0.98, 1.0), 0.6, rough=0.05, emit=0.3)
for k in range(9):
    b = C.empty('bubble', None, (JX + rnd.uniform(-0.1, 0.1), JY + rnd.uniform(-0.1, 0.05), WT - 0.05))
    C.sphere('bub', (0, 0, 0), (0.016, 0.016, 0.016), BUB, b, 12)
    f0 = 328 + k * 3
    K(b, 'scale', 0, (0, 0, 0))
    K(b, 'scale', f0, (0, 0, 0))
    K(b, 'scale', f0 + 2, (1, 1, 1))
    K(b, 'location', f0, (b.location.x, b.location.y, BOT + 0.15))
    K(b, 'location', f0 + 22, (b.location.x, b.location.y, WT - 0.02))
    K(b, 'scale', f0 + 22, (1, 1, 1))
    K(b, 'scale', f0 + 26, (0, 0, 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, BC, RC = (0.05, 0.42, 0.15), (0.1, 0.3, 0.8), (0.8, 0.35, 0.05)
label('¿SÍ?', GC, (-0.5, -1.0, 1.75), 0.7, 216, 296, 0.32, 0.22)
label('¿NO?', RC, (0.5, -0.8, 1.9), 0.7, 224, 296, 0.32, 0.22)

exp = C.empty('peel_zoom', None, (0.0, -2.0, 1.56))
C.rounded_box('slab_out', (0, 0, 0.1), (1.0, 0.06, 0.09), 0.4, PEEL, exp)
C.rounded_box('slab_in', (0, 0, -0.06), (0.98, 0.055, 0.22), 0.3, PITH, exp)
AIR = M((0.3, 0.62, 1.0), rough=0.15, coat=0.8, emit=0.3)
for k, (x, z, s) in enumerate(((-0.38, -0.04, 0.045), (-0.24, -0.1, 0.036), (-0.1, -0.03, 0.05), (0.05, -0.11, 0.038), (0.2, -0.04, 0.046), (0.36, -0.1, 0.036), (-0.31, -0.13, 0.026), (0.28, -0.14, 0.026))):
    C.sphere('air', (x, -0.034, z), (s, 0.012, s), AIR, exp, 16)
T.pop_in(exp, 606, 1.0, 10)
T.pop_out(exp, 764, 1.0, 6)
label('AIRE', BC, (0.0, -2.0, 1.93), 0.62, 618, 764, 0.26, 0.19)
ring = C.empty('swim_ring', None, (0.7, -1.9, 1.52))
RING = M((1.0, 0.45, 0.55), rough=0.35, coat=0.8)
RW = M((1.0, 0.97, 0.92), rough=0.35, coat=0.8)
for k in range(8):
    a0, a1 = k * 6.2832 / 8, (k + 1) * 6.2832 / 8
    C.tube('ring_seg', [(0.12 * math.cos(a0 + (a1 - a0) * i / 6), 0, 0.12 * math.sin(a0 + (a1 - a0) * i / 6)) for i in range(7)], 0.05, RING if k % 2 == 0 else RW, ring, res=10)
T.pop_in(ring, 680, 1.0, 10)
T.pop_out(ring, 764, 1.0, 6)
label('¡FLOTA!', GC, (0.1, -1.75, 1.12), 0.8, 790, TOTAL + 10, 0.28, 0.19)
label('¡AL FONDO!', RC, (0.3, -2.1, 0.3), 1.05, 806, TOTAL + 10, 0.28, 0.19)
confetti(846, (0, -1.6, 1.3), n=30, spread=1.6)

OP = ((-0.28, -3.3, 0.85), (-0.28, -1.5, 0.62), 34)
W = ((0.0, -4.7, 1.9), (0.0, -1.55, 0.72), 28)
CU = ((0.0, -4.3, 1.0), (0.0, -1.55, 0.55), 26)
EXP = ((0.0, -5.0, 2.15), (0.0, -1.55, 0.88), 28)
FIN = ((0.1, -4.45, 1.4), (0.0, -1.55, 0.66), 28)
for a, b, pose in ((0, 88, OP), (90, 322, W), (324, 466, CU), (468, 594, W), (596, 766, EXP), (768, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

for f0 in (12, 50):
    T.arm(bopi, 'L', f0 - 2, 0, None)
    T.arm(bopi, 'L', f0 + 10, fwd=-70, out=20)
    T.arm(bopi, 'L', f0 + 20, fwd=-70, out=20)
    T.rest_arm(bopi, 'L', f0 + 28)
T.arm(luma, 'R', 100, 0, None)
T.arm(luma, 'R', 112, fwd=-80, out=20)
T.arm(luma, 'R', 318, fwd=-80, out=20)
T.rest_arm(luma, 'R', 332)
T.arm(luma, 'R', 466, 0, None)
T.arm(luma, 'R', 480, fwd=-80, out=20)
T.arm(luma, 'R', 500, fwd=-80, out=20)
T.rest_arm(luma, 'R', 512)
gesture(bopi, 'hops', 360)
gesture(luma, 'hops', 530)
gesture(luma, 'breathe', 600)
T.arm(bopi, 'R', 770, 0, None)
T.arm(bopi, 'R', 780, fwd=-60, out=60)
T.arm(bopi, 'R', 830, fwd=-60, out=60)
T.rest_arm(bopi, 'R', 840)
C.wave(bopi, 'R', 850, cycles=2, period=10)
C.wave(luma, 'L', 846, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(bopi, (50, 170, 320, 450, 580, 720, 860))
T.blinks(luma, (60, 180, 340, 480, 640, 760))
