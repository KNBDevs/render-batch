from stage import *
from episodes.vaso_suda_plan import *
import ep_tools as T
import random
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'vaso_suda'
Z0 = 0.08
auto_dress(EID, ENV)
ICE = (0.62, 0.9, 1.0)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, ICE), (52, ICE), (66, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (0.78, 0.95, 1.0, 1)), (52, (0.78, 0.95, 1.0, 1)), (66, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

TC = Vector((0.0, -2.0, Z0))
spawn('low_table', 2, 5521, 'candy', tuple(TC), 1.0, 0)
TOP = Z0 + 0.62
CS = 2.0
CO = 1.3
LIFT = 0.024 * CO
XA, XB, YC = -0.3, 0.3, -2.0
spawn('coaster', 0, 731, 'candy', (XA, YC, TOP), CO, 0)
cob = spawn('coaster', 0, 731, 'candy', (XB, YC, TOP), CO, 0)
T.pop_in(cob, 168, CO, 8)

blue = MA((0.08, 0.32, 0.95), 0.92, rough=0.04, emit=0.18)
FILL = 0.75


def cup_at(x, seed):
    cp = spawn('clear_cup', 1, seed, 'candy', (x, YC, TOP + LIFT), CS, 0)
    piv = next(o for o in cp.children if o.name.startswith('water_pivot'))
    piv.scale = (1, 1, FILL)
    for o in piv.children:
        o.data.materials.clear()
        o.data.materials.append(blue)
    return cp


cupA = cup_at(XA, 3907)
cupB = cup_at(XB, 3907)
T.pop_in(cupB, 172, CS, 8)

WTOP = 0.032 + 0.22 * FILL
icem = MA((0.92, 0.98, 1.0), 0.4, rough=0.03, emit=0.1)
for k, (dx, dy, rz) in enumerate(((-0.024, -0.018, 12), (0.026, -0.008, -20), (0.0, 0.026, 35))):
    o = C.rounded_box('ice', (dx, dy, WTOP - 0.008), (0.04, 0.04, 0.036), 0.3, icem, cupA)
    o.rotation_euler = (math.radians(6 * (k - 1)), math.radians(8), math.radians(rz))

dropm = MA((0.95, 0.98, 1.0), 0.45, rough=0.02, emit=0.08)


def rad(z):
    return 0.078 + 0.017 * z / 0.27 + 0.003


def drop_at(a, z, r):
    a = math.radians(a)
    rr = rad(z)
    return C.sphere('drop', (math.cos(a) * rr, math.sin(a) * rr, z), (r, r * 0.6, r * 1.25), dropm, cupA, 12)


def sk(o, f, m):
    b = o.get('b0') or tuple(o.scale)
    o['b0'] = b
    K(o, 'scale', f, tuple(v * w for v, w in zip(b, m)))


rng = random.Random(42)
first, later = [], []
for k in range(30):
    a = rng.uniform(-160, -20)
    z = rng.uniform(0.03, WTOP - 0.01)
    o = drop_at(a, z, rng.uniform(0.0055, 0.01))
    (first if k < 13 else later).append(o)
for o in first:
    sk(o, 0, (1, 1, 1))
for k, o in enumerate(later):
    f = 334 + k * 3
    sk(o, 0, (0, 0, 0))
    sk(o, f, (0, 0, 0))
    sk(o, f + 8, (1, 1, 1))

run = drop_at(-95, 0.17, 0.011)
for f, z in ((0, 0.17), (10, 0.165), (44, 0.012), (50, 0.004)):
    rr = rad(z)
    K(run, 'location', f, (math.cos(math.radians(-95)) * rr, math.sin(math.radians(-95)) * rr, z))
sk(run, 48, (1, 1, 1))
sk(run, 52, (0, 0, 0))
pud = C.sphere('puddle', (0, 0, 0), (0.07, 0.05, 0.004), dropm, None, 20)
pud.location = (XA, YC - 0.17, TOP + LIFT + 0.003)
sk(pud, 0, (0.3, 0.3, 1))
sk(pud, 46, (0.3, 0.3, 1))
sk(pud, 58, (1, 1, 1))

clock = spawn('time_clock', 1, 77, 'candy', (0.0, YC + 0.12, TOP + 0.62), 1.3, 0)
hm = next(o for o in clock.children if o.name.startswith('hand_m'))
hh = next(o for o in clock.children if o.name.startswith('hand_h'))
T.pop_in(clock, 326, 1.3, 8)
K(hm, 'rotation_euler', 330, (0, 0, 0))
K(hm, 'rotation_euler', 390, (0, math.radians(360), 0))
K(hh, 'rotation_euler', 330, (0, 0, 0))
K(hh, 'rotation_euler', 390, (0, math.radians(30), 0))
T.pop_out(clock, 394, 1.3, 6)


def label(txt, rgb, loc, w, f_in, f_out, h=0.18, sz=0.13):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


label('¿DENTRO?', (0.1, 0.35, 0.9), (-0.42, YC - 0.3, TOP + 1.0), 0.72, 244, 324)
label('¿AIRE?', (0.15, 0.6, 0.55), (0.42, YC - 0.3, TOP + 1.0), 0.56, 250, 324)
label('UN RATITO DESPUÉS', (0.45, 0.3, 0.75), (0.0, YC - 0.35, TOP + 1.12), 1.3, 330, 394, 0.16, 0.1)
label('SECO', (0.85, 0.45, 0.1), (XB, YC - 0.3, TOP + 0.72), 0.44, 482, 544, 0.15, 0.11)

PNL = Vector((0.0, -1.05, 0.45))
PS = 1.7
panel = spawn('explain_panel', 0, 93, 'candy', tuple(PNL), PS, 0)
scr = next(o for o in panel.children if o.name.startswith('screen'))
ink = M((0.25, 0.35, 0.6), rough=0.4, emit=0.2)
C.tube('cupl', [(0.05, -0.014, 0.06), (0.065, -0.014, -0.15), (0.155, -0.014, -0.15), (0.17, -0.014, 0.06)], 0.007, ink, scr)
C.rounded_box('pw', (0.11, -0.01, -0.07), (0.09, 0.004, 0.14), 0.05, M((0.4, 0.68, 1.0), rough=0.5, emit=0.25), scr)
dm = M((0.55, 0.8, 1.0), rough=0.4, emit=0.35)
vap = C.empty('vap', scr, (0, 0, 0))
for k in range(9):
    C.sphere('v', (-0.16 + 0.05 * (k % 3) + 0.012 * (k // 3), -0.016, -0.08 + 0.07 * (k // 3)), (0.011, 0.004, 0.011), dm, vap, 10)
arr = C.empty('arr', scr, (0, 0, 0))
am = M((1.0, 0.8, 0.15), rough=0.3, coat=0.4, emit=1.2)
C.tube('a1', [(-0.03, -0.018, 0.0), (0.03, -0.018, -0.03)], 0.009, am, arr)
C.tube('a2', [(0.03, -0.018, -0.03), (0.005, -0.018, -0.03)], 0.008, am, arr)
C.tube('a3', [(0.03, -0.018, -0.03), (0.018, -0.018, -0.008)], 0.008, am, arr)
drp = C.empty('drp', scr, (0, 0, 0))
for z in (-0.02, -0.07, -0.12):
    for x in (0.045, 0.177):
        C.sphere('pd', (x, -0.018, z), (0.009, 0.004, 0.012), M((1, 1, 1), rough=0.3, emit=0.5), drp, 10)
glyph('DIBUJO', 0.04, 0.006, ink, scr, (0.0, -0.02, 0.16))
for o, f in ((vap, 566), (arr, 590), (drp, 640)):
    sk(o, 0, (0, 0, 0))
    sk(o, f, (0, 0, 0))
    sk(o, f + 12, (1, 1, 1))
T.pop_in(panel, 546, PS, 10)
T.pop_out(panel, 702, PS, 6)

W0 = ((0.0, -6.3, 1.9), (0.0, -1.6, 0.9), 29)
OP0 = ((XA - 0.12, YC - 0.95, TOP + 0.36), (XA, YC, TOP + 0.3), 46)
OP1 = ((XA - 0.08, YC - 1.1, TOP + 0.4), (XA, YC, TOP + 0.3), 44)
WS = ((0.0, -3.4, 1.15), (0.0, -2.0, 0.98), 36)
CA = ((XA - 0.05, YC - 1.05, TOP + 0.36), (XA, YC, TOP + 0.3), 42)
CB = ((XB + 0.05, YC - 1.15, TOP + 0.42), (XB, YC, TOP + 0.38), 38)
WQ = ((0.0, -5.6, 1.7), (0.0, -1.8, 1.05), 26)
WP = ((0.0, -6.0, 1.75), (0.0, -1.3, 1.5), 29)
WE = ((0.0, -5.3, 1.6), (0.0, -1.7, 1.0), 24)
camkey(0, OP0)
camkey(56, OP1)
for a, b, pose in ((58, 156, W0), (158, 232, WQ), (234, 326, WQ), (328, 398, WQ), (400, 468, CA), (470, 544, CB), (546, 708, WP), (710, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

luma = make('luma', 1.45)
moki = make('moki', 1.2)
L0 = Vector((-0.76, -1.42, Z0))
M0 = Vector((0.74, -1.38, Z0))
T.place(luma, 0, L0)
T.turn(luma, 0, 25)
S(luma, 6, (1, 1, 1))
S(luma, 10, (1.1, 1.1, 0.86))
S(luma, 16, (0.95, 0.95, 1.08))
S(luma, 22, (1, 1, 1))
for side in ('L', 'R'):
    T.arm(luma, side, 6, fwd=-40, out=60)
    T.arm(luma, side, 70, fwd=-40, out=60)
    T.rest_arm(luma, side, 80)
gesture(luma, 'hops', 60)
T.turn(luma, 236, 15)
T.turn(luma, 400, 35)
T.arm(luma, 'R', 402, 0, None)
T.arm(luma, 'R', 410, fwd=-70, out=25)
T.arm(luma, 'R', 456, fwd=-70, out=25)
T.rest_arm(luma, 'R', 466)
gesture(luma, 'bounce', 474)
T.turn(luma, 472, 10)
T.turn(luma, 550, 20)
gesture(luma, 'sway', 640)
T.turn(luma, 716, -10)
S(luma, 722, (1, 1, 1))
S(luma, 728, (0.96, 0.96, 1.06))
S(luma, 760, (1, 1, 1))
gesture(luma, 'bounce', 812)
T.turn(luma, 812, 20)

T.place(moki, 0, M0)
T.turn(moki, 0, -25)
gesture(moki, 'breathe', 84)
T.arm(moki, 'L', 160, 0, None)
T.arm(moki, 'L', 168, fwd=-75, out=30)
T.arm(moki, 'L', 196, fwd=-75, out=30)
T.rest_arm(moki, 'L', 206)
T.turn(moki, 236, -10)
for side in ('L', 'R'):
    T.arm(moki, side, 238, 0, None)
    T.arm(moki, side, 246, fwd=-55, out=45)
    T.arm(moki, side, 310, fwd=-55, out=45)
    T.rest_arm(moki, side, 320)
T.turn(moki, 550, -30)
T.arm(moki, 'L', 552, 0, None)
T.arm(moki, 'L', 560, fwd=-85, out=35)
T.arm(moki, 'L', 690, fwd=-85, out=35)
T.rest_arm(moki, 'L', 702)
T.turn(moki, 722, -20)
for k, f in enumerate(range(774, 806, 8)):
    T.turn(moki, f, -40 if k % 2 == 0 else 0)
S(moki, 774, (1, 1, 1))
S(moki, 779, (1.08, 1.08, 0.9))
S(moki, 786, (1, 1, 1))
T.turn(moki, 812, -20)
C.wave(moki, 'R', 820, cycles=2, period=8)
confetti(818, (0.0, YC, TOP + 0.9), n=24, spread=1.2)

T.lines(EID, LINES)
T.blinks(luma, (40, 150, 290, 380, 520, 660, 830))
T.blinks(moki, (55, 200, 330, 470, 610, 760))
