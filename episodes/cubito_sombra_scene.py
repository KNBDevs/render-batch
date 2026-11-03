from stage import *
from episodes.cubito_sombra_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'cubito_sombra'
Z0 = 0.08
auto_dress(EID, ENV)
LI = (1.0, 0.62, 0.25)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, LI), (50, LI), (64, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (1.0, 0.7, 0.32, 1)), (50, (1.0, 0.7, 0.32, 1)), (64, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

YS = -2.12
YH = -1.3
XS, XE = -0.55, 0.32
XH0, XH1 = XS + 0.05, XE + 0.06
XS0, XS1 = XS - 0.22, XE - 0.3
LW = 0.44


def lane(name, y, rgb):
    C.rounded_box(name, ((XS + XE) / 2 + 0.02, y, Z0 + 0.006), (XE - XS + 0.7, LW, 0.012), 0.4, M(rgb, rough=0.55, coat=0.3), None)
    for k in range(9):
        x = XS - 0.2 + k * (XE - XS + 0.4) / 8
        C.rounded_box('dash', (x, y, Z0 + 0.0135), (0.06, 0.014, 0.004), 0.4, M((1, 1, 1), rough=0.5, emit=0.1), None)


lane('sun_lane', YS, (1.0, 0.74, 0.4))
lane('shade_lane', YH, (0.55, 0.7, 0.95))
C.rounded_box('sun_glow', ((XS + XE) / 2, YS, Z0 + 0.016), (XE - XS + 0.64, LW + 0.08, 0.003), 0.5,
              MA((1.0, 0.9, 0.35), 0.45, rough=0.2, emit=1.1), None)
C.rounded_box('shade_patch', ((XS + XE) / 2, YH, Z0 + 0.016), (XE - XS + 0.64, LW + 0.1, 0.003), 0.5,
              MA((0.2, 0.28, 0.55), 0.35, rough=0.6), None)

sun = C.empty('sun', None, (-0.85, -0.6, 2.35))
sm = M((1.0, 0.85, 0.25), rough=0.3, emit=2.2)
C.sphere('disc', (0, 0, 0), (0.24, 0.06, 0.24), sm, sun, 40)
for k in range(10):
    a = k * math.pi / 5
    C.sphere('ray', (0.36 * math.cos(a), 0, 0.36 * math.sin(a)), (0.06, 0.03, 0.06), sm, sun, 16)
for f in range(0, TOTAL, 48):
    K(sun, 'rotation_euler', f, (0, math.radians(f * 0.4), 0))
for f in range(0, TOTAL, 24):
    K(sun, 'scale', f, (1, 1, 1) if (f // 24) % 2 else (1.06, 1.06, 1.06))

spawn('toy_parasol', 0, 905, 'candy', ((XS + XE) / 2, YH + 0.5, Z0), 1.0, 0, R=0.95, h=1.05)

PH = 0.12
VX, VY = 0.86, -1.7
C.rounded_box('vaso_ped', (VX, VY, Z0 + PH / 2), (0.5, 0.5, PH), 0.3, M((0.62, 0.86, 0.66), rough=0.5, coat=0.4), None)
VS = 2.4
cup = spawn('clear_cup', 0, 906, 'fresh', (VX, VY, Z0 + PH), VS, 200)
JM = MA((1.0, 0.6, 0.12), 0.8, rough=0.08, emit=0.2)
for o in cup.children_recursive:
    if o.name.startswith('water') and o.type == 'MESH':
        o.data.materials.clear()
        o.data.materials.append(JM)
VTOP = Z0 + PH + 0.2 * VS
VIN = Z0 + PH + 0.1 * VS

ice = MA((0.3, 0.68, 1.0), 0.85, rough=0.15, emit=0.3)
edge = M((0.85, 0.97, 1.0), rough=0.2, coat=0.8, emit=0.6)
hi = M((1, 1, 1), rough=0.2, emit=1.2)
wat = MA((0.3, 0.6, 1.0), 0.85, rough=0.3, emit=0.15)
CS_ = 0.27
CZ = 0.64 * CS_ + 0.002


def cube(parent, s=1.5):
    o = C.empty('cube', parent, (0, 0, CZ))
    C.rounded_box('ice', (0, 0, 0.07), (0.14, 0.14, 0.14), 0.03, ice, o)
    C.sphere('shine', (-0.035, -0.072, 0.11), (0.014, 0.004, 0.03), hi, o, 10)
    C.tube('rim', [(-0.06, -0.071, 0.135), (0.06, -0.071, 0.135), (0.071, 0.06, 0.135)], 0.006, edge, o)
    o.scale = (s, s, s)
    return o


def puddle(parent):
    o = C.empty('pud', parent, (0, 0, CZ + 0.001))
    C.sphere('pw', (0, 0, 0), (0.22, 0.14, 0.01), wat, o, 32)
    o.scale = (0.001, 0.001, 1)
    return o


def melt(c, p, f0, f1, s0=1.5, steps=8):
    K(c, 'scale', f0 - 1, (s0, s0, s0))
    K(p, 'scale', 0, (0.001, 0.001, 1))
    K(p, 'scale', f0 - 1, (0.001, 0.001, 1))
    for k in range(steps + 1):
        u = k / steps
        f = round(f0 + (f1 - f0) * u)
        s = 1 - u
        K(c, 'scale', f, (max(0.001, s0 * s ** 0.6), max(0.001, s0 * s ** 0.6), max(0.001, s0 * s)))
        K(p, 'scale', f, (0.25 + 0.75 * u, 0.25 + 0.75 * u, 1))


def car(seed, style=2):
    e = C.empty('carrier', None, (0, 0, -5))
    spawn('toy_car', style, seed, 'candy', (0, 0, 0), CS_, 0, parent=e)
    return e


def drive(e, f0, f1, x0, x1, y):
    K(e, 'location', f0, (x0, y, Z0 + 0.013))
    n = max(2, (f1 - f0) // 6)
    for i in range(1, n + 1):
        u = i / n
        K(e, 'location', f0 + round(u * (f1 - f0)), (x0 + (x1 - x0) * u, y, Z0 + 0.013 + (0.006 if i % 2 else 0)))


def trail(y, xs, fs):
    for x, f in zip(xs, fs):
        d = C.empty('wet', None, (x, y, Z0 + 0.019))
        C.sphere('w', (0, 0, 0), (0.06, 0.045, 0.003), wat, d, 16)
        T.pop_in(d, f, 1.0, 6)


def drips(e, fs):
    for f in fs:
        d = C.empty('drip', e, (-0.17, -0.1, CZ))
        C.sphere('dr', (0, 0, 0), (0.02, 0.02, 0.03), wat, d, 10)
        K(d, 'scale', 0, (0, 0, 0))
        K(d, 'scale', f - 1, (0, 0, 0))
        K(d, 'scale', f, (1, 1, 1))
        K(d, 'location', f, (-0.17, -0.1, CZ))
        K(d, 'location', f + 8, (-0.22, -0.14, 0.0))
        K(d, 'scale', f + 9, (0, 0, 0))


A = car(901, 2)
ca = cube(A)
pa = puddle(A)
drive(A, 0, 90, -0.6, 0.1, YS)
K(A, 'location', 91, (0.1, YS, Z0 + 0.013))
melt(ca, pa, 18, 80)
drips(A, (26, 38, 50, 62, 72))
trail(YS, (-0.68, -0.56, -0.44, -0.3, -0.18), (30, 42, 54, 66, 76))
T.pop_out(A, 156, 1.0, 6)

S1 = car(902, 2)
S2 = car(903, 1)
cs = cube(S1)
ps = puddle(S1)
ch_ = cube(S2)
ph_ = puddle(S2)
for e, y, x0, x1 in ((S1, YS, XS0, XS1), (S2, YH, XH0, XH1)):
    K(e, 'location', 0, (x0, y, -5))
    K(e, 'location', 199, (x0, y, -5))
    K(e, 'location', 200, (x0, y, Z0 + 0.013))
    T.pop_in(e, 200, 1.0, 8)
    drive(e, 342, 520, x0, x1, y)
melt(cs, ps, 380, 470, steps=10)
drips(S1, (392, 406, 420, 434, 448, 460))
trail(YS, (-0.82, -0.72, -0.62, -0.52, -0.42, -0.34), (396, 410, 424, 438, 452, 464))
K(ch_, 'scale', 0, (1.5, 1.5, 1.5))
K(ch_, 'scale', 722, (1.5, 1.5, 1.5))
for f in (300, 360, 440, 520):
    K(ch_, 'location', f, (0, 0, CZ))

J0 = Vector((0, 0, CZ))
K(ch_, 'location', 722, tuple(J0))
for i in range(1, 9):
    u = i / 8
    p = Vector((XH1 + (VX - XH1) * u, YH + (VY - YH) * u, Z0 + CZ + (VTOP + 0.06 - Z0 - CZ) * u + 0.4 * math.sin(math.pi * u * 0.92)))
    if i == 8:
        p.z = VIN
    K(ch_, 'location', 722 + round(u * 20), tuple(p - Vector((XH1, YH, Z0 + 0.013))))
K(ch_, 'scale', 742, (1.15, 1.15, 1.15))
splash = C.empty('splash', None, (VX, VY, VIN + 0.06))
C.tube('r', [(math.cos(k * 6.2832 / 24) * 0.15, math.sin(k * 6.2832 / 24) * 0.15, 0) for k in range(25)], 0.012, JM, splash)
K(splash, 'scale', 0, (0, 0, 0))
K(splash, 'scale', 741, (0, 0, 0))
K(splash, 'scale', 743, (0.5, 0.5, 1))
K(splash, 'scale', 752, (1.3, 1.3, 1))
K(splash, 'scale', 755, (0, 0, 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.18, sz=0.13):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


OR = (0.8, 0.3, 0.0)
BL = (0.0, 0.2, 0.7)
label('¿SOL?', OR, (-0.12, YS - 0.25, Z0 + 0.42), 0.7, 238, 336, h=0.22, sz=0.16)
label('¿SOMBRA?', BL, (0.3, YH - 0.3, Z0 + 1.38), 1.06, 244, 336, h=0.22, sz=0.16)
label('SOL', OR, (-0.12, YS - 0.25, Z0 + 0.42), 0.56, 618, 712, h=0.22, sz=0.16)
label('SOMBRA', BL, (0.3, YH - 0.3, Z0 + 1.38), 0.96, 622, 712, h=0.22, sz=0.16)

OP = ((-0.5, YS - 1.15, 0.5), (-0.45, YS, 0.2), 30)
OP2 = ((-0.12, YS - 1.15, 0.5), (-0.08, YS, 0.2), 30)
W = ((0.05, -4.9, 2.15), (0.08, -1.72, 0.18), 24)
WQ = ((0.05, -4.6, 2.05), (0.08, -1.75, 0.2), 23)
CSN = ((-0.45, YS - 1.3, 0.66), (-0.52, YS, 0.2), 30)
CH = ((XH1 - 0.7, -3.2, 1.2), (XH1, YH, 0.22), 30)
WE = ((0.5, -4.0, 1.25), (0.6, -1.6, 0.5), 26)
camkey(0, OP)
camkey(58, OP2)
for a, b, pose in ((60, 200, W), (202, 340, WQ), (342, 396, W), (398, 470, CSN), (472, 522, W),
                   (524, 606, CH), (608, 716, WQ), (718, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

tuki = make('tuki', 1.4)
ruki = make('ruki', 1.45)
TK0 = Vector((-1.05, -1.45, Z0))
RK0 = Vector((1.25, -1.0, Z0))
T.place(tuki, 0, TK0)
T.turn(tuki, 0, 30)
for side in ('L', 'R'):
    T.arm(tuki, side, 6, 0, None)
    T.arm(tuki, side, 12, fwd=-120, out=50)
    T.arm(tuki, side, 60, fwd=-120, out=50)
    T.rest_arm(tuki, side, 70)
T.turn(tuki, 120, 45)
TK1 = Vector((-1.03, -1.55, Z0))
hop_to(tuki, 164, TK0, TK1, 10, 0.3)
for side in ('L', 'R'):
    T.arm(tuki, side, 168, 0, None)
    T.arm(tuki, side, 174, fwd=-150, out=20)
    T.arm(tuki, side, 210, fwd=-150, out=20)
    T.rest_arm(tuki, side, 220)
T.turn(tuki, 226, 20)
T.turn(tuki, 330, 60)
T.arm(tuki, 'R', 332, 0, None)
T.arm(tuki, 'R', 338, fwd=-70, out=10)
T.arm(tuki, 'R', 352, fwd=-70, out=10)
T.rest_arm(tuki, 'R', 362)
T.turn(tuki, 400, 45)
gesture(tuki, 'hops', 478)
T.arm(tuki, 'L', 476, 0, None)
T.arm(tuki, 'L', 482, fwd=-80, out=40)
T.arm(tuki, 'L', 520, fwd=-80, out=40)
T.rest_arm(tuki, 'L', 530)
T.turn(tuki, 600, 25)
TK2 = Vector((-0.5, -0.95, Z0))
T.turn(tuki, 700, 50)
hop_to(tuki, 706, TK1, TK2, 12, 0.35)
T.turn(tuki, 722, 35)
for side in ('L', 'R'):
    T.arm(tuki, side, 744, 0, None)
    T.arm(tuki, side, 750, fwd=-150, out=25)
    T.arm(tuki, side, 796, fwd=-150, out=25)
    T.rest_arm(tuki, side, 806)
gesture(tuki, 'hops', 760)
C.wave(tuki, 'L', 816, cycles=2, period=8)

T.place(ruki, 0, RK0)
T.turn(ruki, 0, -30)
T.turn(ruki, 90, -45)
T.arm(ruki, 'L', 96, 0, None)
T.arm(ruki, 'L', 102, fwd=-80, out=40)
T.arm(ruki, 'L', 150, fwd=-80, out=40)
T.rest_arm(ruki, 'L', 160)
gesture(ruki, 'breathe', 240)
T.turn(ruki, 228, -35)
T.turn(ruki, 340, -60)
T.turn(ruki, 526, -45)
for side in ('L', 'R'):
    T.arm(ruki, side, 530, 0, None)
    T.arm(ruki, side, 536, fwd=-150, out=20)
    T.arm(ruki, side, 580, fwd=-150, out=20)
    T.rest_arm(ruki, side, 590)
T.turn(ruki, 608, -30)
T.arm(ruki, 'R', 614, 0, None)
T.arm(ruki, 'R', 620, fwd=-150, out=35)
T.arm(ruki, 'R', 672, fwd=-150, out=35)
T.rest_arm(ruki, 'R', 682)
T.turn(ruki, 716, -50)
for side in ('L', 'R'):
    T.arm(ruki, side, 750, 0, None)
    T.arm(ruki, side, 756, fwd=-140, out=30)
    T.arm(ruki, side, 800, fwd=-140, out=30)
    T.rest_arm(ruki, side, 810)
C.wave(ruki, 'R', 812, cycles=2, period=8)
confetti(746, (VX - 0.3, VY, Z0 + 1.0), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(tuki, (44, 150, 300, 460, 580, 690, 830))
T.blinks(ruki, (70, 190, 340, 480, 640, 780))
