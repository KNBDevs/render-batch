from stage import *
from episodes.edu_01_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
from props.costumes import dress
from episodes.nav_look import winter, snow
EID = 'edu_01'
Z0 = 0.08
auto_dress(EID, ENV)
winter()
snow(TOTAL, n=50, speed=0.008)
F = {l[0]: l[3] for l in LINES}
D = {l[0]: int(T.dur(f'ep_{EID}_{l[0]}', l[2]) * FPS) for l in LINES}
rnd = random.Random(1101)

IN0 = F['r1'] + 10
IN1 = F['t2'] - 4
ICE = (0.55, 0.75, 1.0)
WARMC = (1.0, 0.72, 0.45)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, ICE), (50, ICE), (64, base), (IN0 - 8, base), (IN0, WARMC), (IN1, WARMC), (IN1 + 8, ICE), (F['r2'] - 10, ICE), (F['r2'], base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
for f, c in ((0, (0.35, 0.55, 0.95, 1)), (50, (0.35, 0.55, 0.95, 1)), (64, b0), (IN0 - 8, b0), (IN0, (0.95, 0.65, 0.4, 1)), (IN1, (0.95, 0.65, 0.4, 1)), (IN1 + 8, (0.35, 0.55, 0.95, 1)), (F['r2'] - 10, (0.35, 0.55, 0.95, 1)), (F['r2'], b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

PUFF = MA((0.97, 0.98, 1.0), 0.7, rough=0.3, emit=0.35)


def puff(f0, src, dirv, n=6, size=0.07):
    for k in range(n):
        o = C.empty('puff', None, tuple(src))
        C.sphere('p', (0, 0, 0), (size, size, size * 0.85), PUFF, o, 16)
        a = f0 + k * 2
        end = src + dirv * rnd.uniform(0.8, 1.1) + Vector((rnd.uniform(-0.05, 0.05), 0, rnd.uniform(0.0, 0.12)))
        K(o, 'scale', 0, (0, 0, 0))
        K(o, 'scale', a, (0, 0, 0))
        K(o, 'location', a, tuple(src))
        K(o, 'scale', a + 6, (1, 1, 1))
        K(o, 'location', a + 26, tuple(end))
        K(o, 'scale', a + 26, (1.8, 1.8, 1.8))
        K(o, 'scale', a + 40, (0, 0, 0))


ruki = make('ruki', 1.15)
tuki = make('tuki', 1.1)
dress(ruki, 'ruki', COSTUME, 2)
dress(tuki, 'tuki', COSTUME, 0)
RK = Vector((-0.75, -1.35, Z0))
TK = Vector((0.85, -1.3, Z0))
TW = Vector((0.32, -1.25, Z0))
T.place(ruki, 0, RK)
T.turn(ruki, 0, 30)
T.place(tuki, 0, TK)
T.turn(tuki, 0, -30)
MOUTH = RK + Vector((0.24, -0.46, 0.64))
DIRV = Vector((0.45, -0.25, 0.1))
puff(4, MOUTH, DIRV)
puff(30, MOUTH, DIRV, 5)
for f in (4, 30):
    K(ruki['spin'], 'rotation_euler', f - 4, (0, 0, 0))
    K(ruki['spin'], 'rotation_euler', f, (math.radians(-8), 0, 0))
    K(ruki['spin'], 'rotation_euler', f + 12, (0, 0, 0))
OUT0 = F['t2'] + int(D['t2'] * 0.55)
gesture(ruki, 'breathe', IN0 + 30)
for f in (OUT0, OUT0 + 34):
    puff(f, MOUTH, DIRV, 6)
    K(ruki['spin'], 'rotation_euler', f - 4, (0, 0, 0))
    K(ruki['spin'], 'rotation_euler', f, (math.radians(-8), 0, 0))
    K(ruki['spin'], 'rotation_euler', f + 12, (0, 0, 0))

GY = -1.62
win = C.empty('window', None, (0.32, GY, Z0))
WOOD = M((0.72, 0.5, 0.32), rough=0.5, coat=0.4)
W2, HZ = 0.95, 1.3
for pts in (((-W2 / 2, 0, 0.15), (W2 / 2, 0, 0.15)), ((-W2 / 2, 0, HZ), (W2 / 2, 0, HZ)), ((-W2 / 2, 0, 0.15), (-W2 / 2, 0, HZ)), ((W2 / 2, 0, 0.15), (W2 / 2, 0, HZ))):
    C.tube('fr', list(pts), 0.04, WOOD, win)
for sx in (-1, 1):
    C.tube('leg', [(sx * W2 / 2, 0, 0.0), (sx * W2 / 2, 0, 0.15)], 0.035, WOOD, win)
    C.sphere('foot', (sx * W2 / 2, 0, 0.0), (0.09, 0.12, 0.03), WOOD, win, 16)
C.rounded_box('glass', (0, 0, (HZ + 0.15) / 2), (W2 - 0.04, 0.012, HZ - 0.19), 0.05, MA((0.75, 0.88, 1.0), 0.18, rough=0.03), win)
WIN0 = F['r2'] + 4
K(win, 'scale', 0, (0, 0, 0))
T.pop_in(win, WIN0, 1.0, 10)

fog = C.empty('fog', win, (0.0, -0.03, 0.86))
C.sphere('f', (0, 0, 0), (0.3, 0.008, 0.17), MA((0.95, 0.97, 1.0), 0.62, rough=0.5, emit=0.15), fog, 32)
DROPM = MA((0.8, 0.9, 1.0), 0.9, rough=0.05, emit=0.3)
for k in range(26):
    a, r = rnd.uniform(0, 6.2832), 0.24 * math.sqrt(rnd.random())
    C.sphere('d', (r * math.cos(a) * 1.1, -0.012, r * math.sin(a) * 0.62), (0.012, 0.008, 0.012), DROPM, fog, 8)
FOG0 = F['t3'] - 18
K(fog, 'scale', 0, (0, 0, 0))
K(fog, 'scale', FOG0, (0, 0, 0))
K(fog, 'scale', FOG0 + 16, (1, 1, 1))
HEART = M((0.85, 0.2, 0.35), rough=0.4, emit=0.3)
heart = C.empty('heart', fog, (0, -0.016, 0.0))
hp = []
for k in range(41):
    t = k / 40 * 6.2832
    hp.append((0.0085 * 16 * math.sin(t) ** 3, 0, 0.0085 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))))
C.tube('h', hp, 0.012, HEART, heart)
HT = F['t4'] + int(D['t4'] * 0.6)
K(heart, 'scale', 0, (0, 0, 0))
K(heart, 'scale', HT, (0, 0, 0))
K(heart, 'scale', HT + 10, (1, 1, 1))

T.place(tuki, WIN0 + 6, TK)
hop_to(tuki, WIN0 + 10, TK, TW, 14, apex=0.15)
T.turn(tuki, WIN0 + 24, 0)
for f in (FOG0 - 6,):
    K(tuki['spin'], 'rotation_euler', f - 4, (0, 0, 0))
    K(tuki['spin'], 'rotation_euler', f + 4, (math.radians(-8), 0, 0))
    K(tuki['spin'], 'rotation_euler', f + 18, (0, 0, 0))
T.arm(tuki, 'R', HT - 10, 0, None)
T.arm(tuki, 'R', HT - 2, fwd=-95, out=10)
for k, f in enumerate(range(HT, HT + 16, 4)):
    T.arm(tuki, 'R', f, fwd=-95 + (8 if k % 2 else -8), out=10 + (10 if k % 2 else -5))
T.rest_arm(tuki, 'R', HT + 24)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


BC, OC, GC = (0.04, 0.14, 0.55), (0.7, 0.2, 0.02), (0.05, 0.42, 0.15)
label('¿HUMO?', OC, (0.1, -2.0, 1.72), 0.66, F['t1'] + 8, F['r1'] + 20, 0.27, 0.18)
label('DENTRO: CALOR', OC, (0.0, -2.0, 1.72), 1.1, IN0 + 6, IN1, 0.25, 0.15)
label('NO SE VE', OC, (-0.3, -2.0, 1.4), 0.9, IN0 + 50, IN1, 0.25, 0.16)
label('FUERA: FRÍO', BC, (0.0, -2.0, 1.72), 0.98, IN1 + 6, F['r2'] - 4, 0.25, 0.15)
label('¡SE VE!', BC, (0.25, -2.0, 1.4), 0.72, OUT0 + 10, F['r2'] - 4, 0.25, 0.16)
label('¡GOTITAS!', BC, (0.32, -2.0, 1.72), 0.8, F['t3'] + 10, F['r3'] - 4, 0.25, 0.16)

EX0, EX1 = F['r3'] - 2, F['t4'] - 4
exp = C.empty('diagram', None, (0.0, -2.45, 1.12))
C.rounded_box('panel', (0, 0.04, 0.42), (1.34, 0.03, 0.92), 0.4, M((0.3, 0.45, 0.78), rough=0.6, coat=0.2), exp)
INV = MA((0.75, 0.85, 1.0), 0.45, rough=0.2, emit=0.1)
WD = M((0.97, 0.99, 1.0), rough=0.3, emit=0.3)
for k in range(8):
    C.sphere('v', (-0.5 + (k % 4) * 0.08, -0.04, 0.32 + (k // 4) * 0.14 + (k % 2) * 0.05), (0.014, 0.01, 0.014), INV, exp, 10)
ar = C.empty('arrow', exp, (-0.12, -0.04, 0.42))
C.tube('s', [(-0.08, 0, 0), (0.08, 0, 0)], 0.02, M((1.0, 0.85, 0.3), rough=0.4, emit=0.3), ar)
tip = C.empty('t', ar, (0.08, 0, 0), (0, math.radians(90), 0))
C.lathe('tip', [(0.0, 0.0), (0.0, 0.045), (0.07, 0.0)], M((1.0, 0.85, 0.3), rough=0.4, emit=0.3), tip, segs=16)
for k in range(14):
    C.sphere('g', (0.22 + rnd.uniform(-0.12, 0.2), -0.04, 0.42 + rnd.uniform(-0.15, 0.15)), (0.035, 0.02, 0.035), WD, exp, 12)
T.pop_in(exp, EX0, 1.2, 10)
T.pop_out(exp, EX1, 1.2, 6)
label('AGUA INVISIBLE', BC, (0.0, -2.55, 2.0), 1.0, EX0 + 10, EX0 + 70, 0.21, 0.12)
label('CON FRÍO: GOTITAS', BC, (0.0, -2.55, 2.0), 1.15, EX0 + 76, EX1, 0.21, 0.12)
label('VAHO', OC, (0.32, -2.0, 1.72), 0.58, F['t4'] + 6, TOTAL + 10, 0.25, 0.17)

for ch, p0, dx in ((ruki, RK, -0.6),):
    T.place(ch, EX0 - 2, p0)
    T.place(ch, EX0, p0 + Vector((dx, 0, 0)))
    T.place(ch, EX1, p0 + Vector((dx, 0, 0)))
    T.place(ch, EX1 + 2, p0)
T.place(tuki, EX0 - 2, TW)
T.place(tuki, EX0, TW + Vector((0.9, 0, 0)))
T.place(tuki, EX1, TW + Vector((0.9, 0, 0)))
T.place(tuki, EX1 + 2, TW)
gesture(tuki, 'hops', F['t1'] + 4)
gesture(tuki, 'hops', F['t3'] + 8)
T.arm(ruki, 'R', F['r2'], 0, None)
T.arm(ruki, 'R', F['r2'] + 8, fwd=-80, out=30)
T.arm(ruki, 'R', F['r2'] + 40, fwd=-80, out=30)
T.rest_arm(ruki, 'R', F['r2'] + 50)
C.wave(ruki, 'L', TOTAL - 44, cycles=2, period=9)
C.wave(tuki, 'L', TOTAL - 40, cycles=2, period=9)

OP = ((-0.4, -2.95, 1.35), (-0.45, -1.4, 0.75), 24)
W = ((0.0, -4.7, 1.7), (0.0, -1.45, 0.8), 23)
WN = ((0.2, -3.9, 1.45), (0.25, -1.5, 0.85), 24)
EXP = ((0.0, -4.7, 1.62), (0.0, -2.45, 1.52), 30)
for a, b, pose in ((0, F['t1'] + 30, OP), (F['t1'] + 32, F['r2'] - 2, W), (F['r2'], EX0 - 2, WN), (EX0, EX1, EXP), (EX1 + 2, TOTAL - 1, WN)):
    camkey(a, pose)
    camkey(b, pose)

T.lines(EID, LINES)
T.blinks(ruki, (60, 170, 330, 470, 620, 740, 900))
T.blinks(tuki, (70, 200, 360, 500, 650, 790, 930))
