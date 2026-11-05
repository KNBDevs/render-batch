from stage import *
from episodes.agua_camina_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'agua_camina'
Z0 = 0.08
auto_dress(EID, ENV)
LI = (1.0, 0.55, 0.85)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, LI), (52, LI), (64, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (0.62, 0.3, 0.55, 1)), (52, (0.62, 0.3, 0.55, 1)), (64, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

PH = 0.14
CY = -1.85
XA, XB = -0.52, 0.52
C.rounded_box('ped', (0, CY, Z0 + PH / 2), (1.95, 0.8, PH), 0.3, M((0.98, 0.78, 0.52), rough=0.5, coat=0.4), None)
ZB = Z0 + PH
CSC = 3.0
KC = CSC / 2.4
ca = spawn('clear_cup', 1, 2201, 'fresh', (XA, CY, ZB), CSC, 0)
cb = spawn('clear_cup', 1, 2202, 'candy', (XB, CY, ZB), CSC, 0)
WM = MA((0.01, 0.2, 0.9), 1.0, rough=0.05, emit=0.25)


def water(cup):
    p = next(o for o in cup.children_recursive if o.name.startswith('water_pivot'))
    for o in p.children:
        o.data.materials.clear()
        o.data.materials.append(WM)
    return p


wa, wb = water(ca), water(cb)
for cup in (ca, cb):
    for o in cup.children_recursive:
        for m in (getattr(o.data, 'materials', None) or []):
            if m and m.name.startswith('pa') and m is not WM:
                b = m.node_tree.nodes['Principled BSDF']
                if b.inputs['Alpha'].default_value < 0.3:
                    b.inputs['Alpha'].default_value = 0.1
                    b.inputs['Coat Weight'].default_value = 0.25
LA, LB, LE = 0.86, 0.001, 0.44
K(wa, 'scale', 0, (1, 1, LA))
for f in range(4, 52, 6):
    K(wa, 'scale', f, (1.0 + 0.03 * ((f // 6) % 2), 1.0 + 0.03 * ((f // 6) % 2), LA + 0.03 * ((f // 6) % 2)))
K(wa, 'scale', 56, (1, 1, LA))
K(wb, 'scale', 0, (1, 1, LB))
for o in wb.children:
    for f, h in ((0, True), (523, True), (524, False)):
        o.hide_render = h
        o.keyframe_insert('hide_render', frame=f)
K(wa, 'scale', 520, (1, 1, LA))
K(wb, 'scale', 520, (1, 1, LB))
K(wa, 'scale', 740, (1, 1, LE + 0.02))
K(wb, 'scale', 740, (1, 1, LE))

ctrl = [(XA + 0.04 * KC, 0.05), (XA + 0.1 * KC, 0.25), (XA + 0.17 * KC, 0.45), (XA + 0.27 * KC, 0.57), (-0.09, 0.64), (0.09, 0.64),
        (XB - 0.27 * KC, 0.57), (XB - 0.17 * KC, 0.45), (XB - 0.1 * KC, 0.25), (XB - 0.04 * KC, 0.05)]
for _ in range(3):
    nx = [ctrl[0]]
    for a, b in zip(ctrl, ctrl[1:]):
        nx += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
    ctrl = nx + [ctrl[-1]]
PTS = [Vector((x, CY, ZB + z * KC)) for x, z in ctrl]
L = [0.0]
for a, b in zip(PTS, PTS[1:]):
    L.append(L[-1] + (b - a).length)
S = [v / L[-1] for v in L]

strip = C.empty('paper_strip', None, (0, 0, 0))
DRY = (0.97, 0.96, 0.92)
WET = (0.12, 0.38, 1.0)
EM = M((0.92, 0.9, 0.86), rough=0.6, coat=0.2)
NSEG = 24


def wet_f(s):
    return 290 + s * 2 * 140 if s < 0.5 else 430 + (s - 0.5) * 2 * 90


step = len(PTS) / NSEG
for i in range(NSEG):
    a, b = int(i * step), min(len(PTS) - 1, int((i + 1) * step) + 1)
    s = S[(a + b) // 2]
    m = C.mat(f'strip{i}', DRY, rough=0.7, coat=0.25)
    C.tube('seg', [tuple(p) for p in PTS[a:b + 1]], 0.032 * KC, m, strip)
    for k in range(a, b, 3):
        C.sphere('dot', tuple(PTS[k] + Vector((0, -0.03, 0))), (0.009, 0.004, 0.009), EM, strip, 8)
    bc = m.node_tree.nodes['Principled BSDF'].inputs['Base Color']
    f1 = round(wet_f(s))
    for f, c in ((0, DRY), (f1 - 10, DRY), (f1, WET)):
        bc.default_value = (*c, 1)
        bc.keyframe_insert('default_value', frame=f)
K(strip, 'scale', 0, (0, 0, 0))
K(strip, 'location', 0, (0, 0, 0.4))
K(strip, 'scale', 167, (0, 0, 0))
K(strip, 'scale', 175, (1, 1, 1))
K(strip, 'location', 175, (0, 0, 0.4))
K(strip, 'location', 186, (0, 0, 0))

DM = MA((0.01, 0.2, 0.9), 1.0, rough=0.05, emit=0.25)
half = [k for k in range(len(PTS)) if S[k] >= 0.52]
for j, f0 in enumerate((524, 540, 556, 572, 590, 610, 632)):
    d = C.empty('drop', None, tuple(PTS[half[0]]))
    C.sphere('d', (0, -0.035, 0), (0.026, 0.026, 0.03), DM, d, 12)
    K(d, 'scale', 0, (0, 0, 0))
    K(d, 'scale', f0 - 1, (0, 0, 0))
    K(d, 'scale', f0, (1, 1, 1))
    n = len(half) - 1
    for q in range(0, n + 1, 4):
        K(d, 'location', f0 + round(36 * q / n), tuple(PTS[half[q]]))
    K(d, 'location', f0 + 36, tuple(PTS[half[-1]]))
    K(d, 'scale', f0 + 36, (1, 1, 1))
    K(d, 'scale', f0 + 38, (0, 0, 0))

clock = spawn('time_clock', 0, 2203, 'pastel', (0.0, CY + 0.32, ZB), 1.0, 0)
hm = next(o for o in clock.children if o.name.startswith('hand_m'))
hh = next(o for o in clock.children if o.name.startswith('hand_h'))
K(hm, 'rotation_euler', 0, (0, 0, 0))
K(hh, 'rotation_euler', 0, (0, math.radians(90), 0))
K(hm, 'rotation_euler', 290, (0, 0, 0))
K(hh, 'rotation_euler', 290, (0, math.radians(90), 0))
K(hm, 'rotation_euler', 740, (0, 8 * 6.2832, 0))
K(hh, 'rotation_euler', 740, (0, math.radians(90) + 8 * 6.2832 / 12, 0))
K(clock, 'scale', 0, (0, 0, 0))
K(clock, 'scale', 279, (0, 0, 0))
T.pop_in(clock, 280, 1.0, 8)
T.pop_out(clock, 760, 1.0, 6)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


BLU = (0.15, 0.3, 0.7)
label('¿LLEGARÁ?', BLU, (0.0, CY + 0.1, ZB + 1.42), 1.2, 236, 330)
label('UN RATO DESPUÉS', (0.5, 0.25, 0.6), (0.0, CY + 0.1, ZB + 1.42), 1.75, 334, 420, sz=0.17)
label('¡HA LLEGADO!', BLU, (0.0, CY + 0.1, ZB + 1.42), 1.35, 748, TOTAL + 10)

OP = ((-0.95, -3.3, 0.9), (-0.78, -1.6, 0.6), 30)
OP2 = ((-0.88, -3.15, 0.86), (-0.74, -1.6, 0.58), 31)
W = ((0.05, -4.7, 1.7), (0.05, -1.6, 0.55), 22)
WQ = ((0.05, -4.55, 1.65), (0.05, -1.6, 0.65), 22)
CSN = ((0.0, -3.5, 1.2), (0.0, CY, ZB + 0.5), 30)
CH = ((0.62, -3.3, 1.0), (XB, CY, ZB + 0.35), 30)
WE = ((0.0, -4.6, 1.7), (0.0, -1.6, 0.62), 22)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 196, W), (198, 330, WQ), (332, 424, W), (426, 516, CSN), (518, 604, CH),
                   (606, 736, W), (738, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

tuki = make('tuki', 1.4)
ruki = make('ruki', 1.45)
TK0 = Vector((-1.0, -1.3, Z0))
RK0 = Vector((0.98, -0.62, Z0))
T.place(tuki, 0, TK0)
T.turn(tuki, 0, 55)
gesture(tuki, 'breathe', 10)
for side in ('L', 'R'):
    T.arm(tuki, side, 8, 0, None)
    T.arm(tuki, side, 14, fwd=-120, out=35)
    T.arm(tuki, side, 52, fwd=-120, out=35)
    T.rest_arm(tuki, side, 62)
T.turn(tuki, 70, 30)
T.turn(tuki, 210, 20)
T.arm(tuki, 'R', 210, 0, None)
T.arm(tuki, 'R', 216, fwd=-150, out=25)
T.arm(tuki, 'R', 250, fwd=-150, out=25)
T.rest_arm(tuki, 'R', 260)
T.turn(tuki, 300, 40)
T.arm(tuki, 'R', 432, 0, None)
T.arm(tuki, 'R', 438, fwd=-80, out=40)
T.arm(tuki, 'R', 476, fwd=-80, out=40)
T.rest_arm(tuki, 'R', 486)
T.turn(tuki, 600, 25)
TK1 = Vector((-0.95, -1.5, Z0))
hop_to(tuki, 742, TK0, TK1, 12, 0.3)
gesture(tuki, 'hops', 756)
for side in ('L', 'R'):
    T.arm(tuki, side, 744, 0, None)
    T.arm(tuki, side, 750, fwd=-150, out=30)
    T.arm(tuki, side, 800, fwd=-150, out=30)
    T.rest_arm(tuki, side, 810)
C.wave(tuki, 'L', 828, cycles=2, period=8)

T.place(ruki, 0, RK0)
T.turn(ruki, 0, -30)
T.turn(ruki, 92, -40)
T.arm(ruki, 'L', 140, 0, None)
T.arm(ruki, 'L', 148, fwd=-90, out=30)
T.arm(ruki, 'L', 180, fwd=-90, out=30)
T.rest_arm(ruki, 'L', 190)
T.turn(ruki, 300, -45)
T.arm(ruki, 'L', 526, 0, None)
T.arm(ruki, 'L', 532, fwd=-80, out=40)
T.arm(ruki, 'L', 570, fwd=-80, out=40)
T.rest_arm(ruki, 'L', 580)
gesture(ruki, 'breathe', 612)
T.turn(ruki, 612, -25)
T.turn(ruki, 740, -35)
C.wave(ruki, 'R', 820, cycles=2, period=8)
confetti(762, (0.0, CY, ZB + 1.1), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(tuki, (44, 150, 300, 460, 590, 700, 840))
T.blinks(ruki, (70, 190, 330, 500, 650, 790))
