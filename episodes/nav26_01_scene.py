from stage import *
from episodes.nav26_01_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
from props.costumes import dress
from episodes.nav_look import winter, snow
EID = 'nav26_01'
Z0 = 0.08
auto_dress(EID, ENV)
winter()
snow(TOTAL, n=70)
F = {l[0]: l[3] for l in LINES}
D = {l[0]: int(T.dur(f'ep_{EID}_{l[0]}', l[2]) * FPS) for l in LINES}
ICE = (0.55, 0.75, 1.0)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c in ((0, ICE), (60, ICE), (76, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.35, 0.55, 0.95, 1)), (60, (0.35, 0.55, 0.95, 1)), (76, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

rnd = random.Random(1201)
JY = -1.55
JA, JB = -0.42, 0.42
R, H = 0.2, 0.36
WARM = M((1.0, 0.55, 0.25), rough=0.4, coat=0.5, emit=0.2)
COLD = M((0.25, 0.5, 0.95), rough=0.4, coat=0.5, emit=0.15)
STEAM = MA((0.55, 0.65, 0.85), 0.75, rough=0.2, emit=0.2)


def mug(name, x, col):
    m = C.empty(name, None, (x, JY, Z0))
    C.lathe('coaster', [(0, 0.0), (0, R + 0.1), (0.02, R + 0.12), (0.04, R + 0.09), (0.045, 0.0)], M((0.95, 0.93, 0.88), rough=0.5), m, segs=48)
    out = [(0.04, 0.0), (0.04, R - 0.02), (0.06, R), (H, R), (H + 0.01, R - 0.005)]
    inn = [(H + 0.01, R - 0.03), (0.08, R - 0.03), (0.08, 0.0)]
    C.lathe('body', out + inn, M(col, rough=0.3, coat=0.8), m, segs=56)
    C.lathe('water', [(0.08, 0.0), (0.08, R - 0.032), (H - 0.06, R - 0.032), (H - 0.06, 0.0)], MA((0.6, 0.8, 1.0), 0.6, rough=0.05, emit=0.1), m, segs=48)
    C.tube('handle', [(R - 0.01, 0, 0.1), (R + 0.1, 0, 0.12), (R + 0.12, 0, 0.2), (R + 0.1, 0, 0.28), (R - 0.01, 0, 0.3)], 0.025, M(col, rough=0.3, coat=0.8), m)
    m.scale = (1.4, 1.4, 1.4)
    return m


ma = mug('mug_a', JA, (0.98, 0.45, 0.45))
mb = mug('mug_b', JB, (0.45, 0.7, 0.98))
for o in (ma, mb):
    K(o, 'scale', 0, (0, 0, 0))
    T.pop_in(o, F['t2'] + 10, 1.4, 8)


def steam(x, f_on, f_off):
    out = []
    for k in range(3):
        s = C.empty('steam', None, (x + (k - 1) * 0.09, JY, Z0 + H * 1.4 + 0.02))
        pts = [(0.03 * math.sin(t * 0.9 + k), 0, t * 0.07) for t in range(6)]
        C.tube('w', pts, 0.03, STEAM, s)
        K(s, 'scale', 0, (0, 0, 0))
        K(s, 'scale', f_on + 4 * k, (0, 0, 0))
        for f in range(f_on + 4 * k + 8, f_off, 16):
            K(s, 'scale', f, (1, 1, 1.25))
            K(s, 'scale', f + 8, (1, 1, 0.8))
        K(s, 'scale', f_off, (1, 1, 1))
        K(s, 'scale', f_off + 16, (0, 0, 0))
        out.append(s)
    return out


CLK0 = F['t2'] + D['t2'] + 6
CLK1 = F['p3'] - 6
steam(JA, F['t2'] + 20, TOTAL + 40)
steam(JB, F['t2'] + 20, CLK0 + (CLK1 - CLK0) // 2)

WRAP = F['t2'] + int(D['t2'] * 0.55)
wrap = C.empty('wrap', None, (JA, JY, Z0))
RED = M((0.78, 0.12, 0.16), rough=0.8)
CREAM = M((0.97, 0.95, 0.9), rough=0.8)
for k in range(5):
    z = 0.09 + k * 0.085
    pts = [((R * 1.4 + 0.045) * math.cos(a * 6.2832 / 40), (R * 1.4 + 0.045) * math.sin(a * 6.2832 / 40), z) for a in range(41)]
    C.tube(f'band{k}', pts, 0.045, RED if k % 2 == 0 else CREAM, wrap)
C.sphere('knot', (0.05, -(R * 1.4 + 0.08), 0.3), (0.07, 0.05, 0.06), RED, wrap, 16)
C.sphere('tail', (0.1, -(R * 1.4 + 0.08), 0.14), (0.05, 0.035, 0.13), RED, wrap, 16)
K(wrap, 'scale', 0, (0, 0, 0))
K(wrap, 'scale', WRAP, (0, 0, 0))
K(wrap, 'scale', WRAP + 8, (1.08, 1.08, 1.08))
K(wrap, 'scale', WRAP + 12, (1, 1, 1))

clock = C.empty('clock', None, (0, -2.3, 1.45))
clock.rotation_euler = (math.radians(90), 0, 0)
C.lathe('face', [(0, 0.0), (0, 0.26), (0.03, 0.28), (0.06, 0.26), (0.06, 0.0)], M((1.0, 0.98, 0.94), rough=0.4, coat=0.5, emit=0.15), clock, segs=48)
C.tube('rim', [(0.28 * math.cos(a * 6.2832 / 48), 0.28 * math.sin(a * 6.2832 / 48), 0.06) for a in range(49)], 0.025, M((0.3, 0.55, 0.95), rough=0.4), clock)
hand = C.empty('hand', clock, (0, 0, 0.075))
C.tube('h', [(0, 0, 0), (0, 0.2, 0)], 0.018, M((0.8, 0.2, 0.2), rough=0.4), hand)
K(clock, 'scale', 0, (0, 0, 0))
T.pop_in(clock, CLK0, 1.0, 8)
K(hand, 'rotation_euler', CLK0, (0, 0, 0))
K(hand, 'rotation_euler', CLK1 - 8, (0, 0, math.radians(-720)))
set_interp(hand, 'LINEAR')
T.pop_out(clock, CLK1 - 6, 1.0, 6)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


OR, BL, GR = (0.7, 0.2, 0.02), (0.04, 0.14, 0.55), (0.05, 0.42, 0.15)
label('¡BRRR!', BL, (-0.55, -2.2, 1.35), 0.7, 14, 70, 0.27, 0.19)
label('¿DA CALOR?', OR, (0.0, -1.75, 1.75), 1.0, F['p2'] + 20, F['t2'] - 4, 0.3, 0.2)
label('UN RATO DESPUÉS', BL, (0, -2.3, 1.95), 1.1, CLK0 + 4, CLK1 - 4, 0.22, 0.13)
label('CALENTITA', OR, (JA, -2.0, 1.12), 0.72, F['p3'] + 8, F['t3'] - 4, 0.22, 0.13)
label('FRÍA', BL, (JB, -2.0, 1.12), 0.46, F['t2b'] + 8, F['t3'] - 4, 0.22, 0.14)

EX0 = F['t3'] - 2
EX1 = F['p4'] - 4
exp = C.empty('diagram', None, (0.0, -2.45, 1.12))
C.rounded_box('panel', (0, 0.04, 0.42), (1.3, 0.03, 0.92), 0.4, M((0.3, 0.45, 0.78), rough=0.6, coat=0.2), exp)
CUPM = M((0.98, 0.99, 1.0), rough=0.4, coat=0.4)
ARR = M((1.0, 0.45, 0.1), rough=0.4, coat=0.4, emit=0.3)
for x, wrapped in ((-0.32, True), (0.32, False)):
    C.rounded_box('cup', (x, 0.0, 0.3), (0.34, 0.02, 0.4), 0.3, CUPM, exp)
    C.rounded_box('wat', (x, -0.012, 0.28), (0.28, 0.02, 0.32), 0.3, M((1.0, 0.7, 0.4) if wrapped else (0.5, 0.7, 1.0), rough=0.5), exp)
    if wrapped:
        for k in range(3):
            C.rounded_box('band', (x, -0.03, 0.16 + k * 0.12), (0.42, 0.02, 0.07), 0.3, RED if k % 2 == 0 else CREAM, exp)
        for k, dx in enumerate((-0.08, 0.08)):
            C.tube('loop', [(x + dx, -0.05, 0.36), (x + dx * 1.6, -0.05, 0.5), (x + dx * 0.4, -0.05, 0.6), (x - dx * 0.4, -0.05, 0.5), (x + dx * 0.2, -0.05, 0.4)], 0.016, ARR, exp)
    else:
        for k, dx in enumerate((-0.12, 0.0, 0.12)):
            a = C.empty('arr', exp, (x + dx, -0.05, 0.52))
            C.tube('s', [(0, 0, 0), (dx * 0.6, 0, 0.1), (dx * 1.2, 0, 0.2)], 0.016, ARR, a)
            tip = C.empty('t', a, (dx * 1.2, 0, 0.2))
            tip.rotation_euler = (0, math.atan2(dx * 0.6, 0.1), 0)
            C.lathe('tip', [(0.0, 0.0), (0.0, 0.04), (0.06, 0.0)], ARR, tip, segs=16)
            K(a, 'location', EX0 + 20 + 8 * k, (x + dx, -0.05, 0.36))
            K(a, 'location', EX0 + 44 + 8 * k, (x + dx, -0.05, 0.5))
T.pop_in(exp, EX0, 1.2, 10)
T.pop_out(exp, EX1, 1.2, 6)
label('SE QUEDA', OR, (-0.32, -2.55, 2.0), 0.6, EX0 + 10, EX1, 0.19, 0.11)
label('SE ESCAPA', BL, (0.32, -2.55, 2.0), 0.66, EX0 + 20, EX1, 0.19, 0.11)

GLOW = MA((1.0, 0.6, 0.25), 0.18, rough=0.3, emit=0.6)

pimo = make('pimo', 1.1)
tuki = make('tuki', 1.1)
dress(tuki, 'tuki', COSTUME, 1)
scarf = dress(pimo, 'pimo', COSTUME, 0)
GIVE = F['t1'] + int(D['t1'] * 0.7)
K(scarf, 'scale', 0, (0, 0, 0))
K(scarf, 'scale', GIVE, (0, 0, 0))
K(scarf, 'scale', GIVE + 8, (1.1, 1.1, 1.1))
K(scarf, 'scale', GIVE + 12, (1, 1, 1))
PM, TK = Vector((-1.15, -1.3, Z0)), Vector((1.16, -1.28, Z0))
T.place(pimo, 0, PM)
T.turn(pimo, 0, 25)
T.place(tuki, 0, TK)
T.turn(tuki, 0, -25)
for f in range(0, 76, 4):
    K(pimo['spin'], 'rotation_euler', f, (0, 0, math.radians(5 if (f // 4) % 2 else -5)))
K(pimo['spin'], 'rotation_euler', 80, (0, 0, 0))
for ch, p0, dx in ((pimo, PM, -0.6), (tuki, TK, 0.6)):
    T.place(ch, EX0 - 2, p0)
    T.place(ch, EX0, p0 + Vector((dx, 0, 0)))
    T.place(ch, EX1, p0 + Vector((dx, 0, 0)))
    T.place(ch, EX1 + 2, p0)

glow = C.sphere('glow', (0, 0, 0), (0.55, 0.55, 0.6), GLOW, None, 32)
K(glow, 'location', 0, tuple(PM + Vector((0, 0, 0.55))))
K(glow, 'scale', 0, (0, 0, 0))
K(glow, 'scale', F['p4'] + 10, (0, 0, 0))
for k, f in enumerate(range(F['p4'] + 18, TOTAL, 18)):
    K(glow, 'scale', f, (1.05, 1.05, 1.05) if k % 2 else (0.92, 0.92, 0.92))
label('GUARDA EL CALOR', OR, (0.0, -1.95, 1.62), 1.2, F['p4'] + 20, TOTAL + 10, 0.25, 0.15)

T.arm(tuki, 'R', F['t1'], 0, None)
T.arm(tuki, 'R', F['t1'] + 8, fwd=-80, out=25)
T.arm(tuki, 'R', GIVE + 10, fwd=-80, out=25)
T.rest_arm(tuki, 'R', GIVE + 20)
T.arm(tuki, 'L', WRAP - 14, 0, None)
T.arm(tuki, 'L', WRAP - 6, fwd=-80, out=25)
T.arm(tuki, 'L', WRAP + 20, fwd=-80, out=25)
T.rest_arm(tuki, 'L', WRAP + 30)
gesture(pimo, 'hops', GIVE + 14)
gesture(pimo, 'hops', F['p3'] + 4)
for side in ('L', 'R'):
    T.arm(pimo, side, F['p4'], 0, None)
    T.arm(pimo, side, F['p4'] + 8, fwd=-70, out=-10)
    T.arm(pimo, side, F['p4'] + 60, fwd=-70, out=-10)
    T.rest_arm(pimo, side, F['p4'] + 70)
gesture(tuki, 'breathe', F['t3'] + 10)
C.wave(pimo, 'R', TOTAL - 40, cycles=2, period=10)
C.wave(tuki, 'L', TOTAL - 44, cycles=2, period=10)

OP = ((-1.0, -2.9, 1.7), (-1.1, -1.35, 0.6), 24)
W = ((0.0, -4.9, 1.85), (0.0, -1.45, 0.75), 23)
CU = ((0.0, -3.95, 1.45), (0.0, -1.55, 0.6), 27)
CLK = ((0.0, -4.4, 1.6), (0.0, -1.8, 1.0), 25)
EXP = ((0.0, -4.7, 1.62), (0.0, -2.45, 1.52), 30)
FIN = ((-0.3, -4.2, 1.6), (-0.4, -1.45, 0.8), 25)
for a, b, pose in ((0, F['t1'] - 2, OP), (F['t1'], F['t2'] - 2, W), (F['t2'], CLK0 - 2, CU), (CLK0, CLK1 - 2, CLK),
                   (CLK1, EX0 - 2, CU), (EX0, EX1, EXP), (EX1 + 2, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

T.lines(EID, LINES)
T.blinks(pimo, (60, 170, 330, 470, 620, 740, 880, 1000))
T.blinks(tuki, (70, 200, 360, 500, 650, 790, 950))
