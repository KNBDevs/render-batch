from stage import *
from episodes.balanza_globo_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, glyph
EID = 'balanza_globo'
Z0 = 0.08
auto_dress(EID, ENV)
WARM = (1.0, 0.8, 0.58)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, WARM), (64, WARM), (78, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
for f, c in ((0, (1.0, 0.62, 0.42, 1)), (64, (1.0, 0.62, 0.42, 1)), (78, tuple(bgc.default_value))):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

BC = Vector((0.0, -1.95, Z0))
BSC = 1.25
H, HL, PZ = 0.62 * BSC, 0.42 * BSC, 0.12 * BSC
bal = spawn('toy_balance', 2, 5120, 'candy', tuple(BC), BSC, 0)
piv = next(o for o in bal.children_recursive if o.name.startswith('beam_pivot'))
hang = {s: next(o for o in piv.children if o.name.startswith(f'hang_{s}')) for s in 'LR'}
pan = {s: next(o for o in hang[s].children if o.name.startswith(f'pan_{s}')) for s in 'LR'}
TIP = math.radians(15)


def tilt(f, a):
    K(piv, 'rotation_euler', f, (0, a, 0))
    for s in 'LR':
        K(hang[s], 'rotation_euler', f, (0, -a, 0))


def pan_top(side, a):
    sx = -1 if side == 'L' else 1
    return Vector((BC.x + sx * HL * math.cos(a), BC.y, BC.z + H - sx * HL * math.sin(a) + PZ + 0.055 * BSC))


for f, a in ((0, 0), (150, 0), (164, -TIP), (358, -TIP), (374, TIP * 1.1), (380, TIP * 0.95), (386, TIP)):
    tilt(f, a)

GS = 1.2
free = spawn('big_balloon', 0, 8061, 'candy', (0, 0, 0), GS, 0)
onpan = spawn('big_balloon', 0, 8061, 'candy', (0, 0, 0.0), GS / BSC, 0, pan['L'])
B0 = Vector((-1.85, -1.95, Z0 + 0.04 * GS))
B1 = Vector((-0.92, -1.95, Z0 + 0.04 * GS))
for k, f in enumerate(range(0, 66, 6)):
    u = f / 64
    K(free, 'location', f, tuple(B0.lerp(B1, min(1, u))))
    K(free, 'rotation_euler', f, (0, math.radians(6 * math.sin(k * 1.4)), 0))
PL = pan_top('L', 0)
K(free, 'location', 118, tuple(B1))
K(free, 'rotation_euler', 118, (0, 0, 0))
for t in range(0, 31, 3):
    u = t / 30
    p = B1.lerp(PL, u)
    p.z += 0.5 * 4 * u * (1 - u)
    K(free, 'location', 120 + t, tuple(p))
SW1 = 150
K(free, 'scale', SW1, (GS,) * 3)
K(free, 'scale', SW1 + 1, (0, 0, 0))
K(onpan, 'scale', 0, (0, 0, 0))
K(onpan, 'scale', SW1, (0, 0, 0))
K(onpan, 'scale', SW1 + 1, (GS / BSC,) * 3)
SW2 = 712
HEAD = Vector((-1.5, -1.8, Z0 + 1.24))
PL2 = pan_top('L', TIP)
K(onpan, 'scale', SW2, (GS / BSC,) * 3)
K(onpan, 'scale', SW2 + 1, (0, 0, 0))
K(free, 'location', SW2, tuple(PL2))
K(free, 'scale', SW2, (0, 0, 0))
K(free, 'scale', SW2 + 1, (GS,) * 3)
for t in range(0, 25, 3):
    u = t / 24
    p = PL2.lerp(HEAD, u)
    p.z += 0.45 * 4 * u * (1 - u)
    K(free, 'location', SW2 + 1 + t, tuple(p))
K(free, 'location', 740, tuple(HEAD))
for f, dz in ((768, 0.0), (774, 0.35), (780, 0.0), (786, 0.3), (792, 0.0)):
    K(free, 'location', f, tuple(HEAD + Vector((0, 0, dz))))
K(free, 'location', TOTAL - 1, tuple(HEAD))

AS = 1.1
af = spawn('fruit', 0, 3, 'pastel', (0, 0, 0), AS, 0)
ap = spawn('fruit', 0, 3, 'pastel', (0, 0, 0.004), AS / BSC, 0, pan['R'])
AH = Vector((1.02, -2.08, Z0 + 1.02))
PR = pan_top('R', -TIP)
AV = PR + Vector((0, 0, 0.36))
K(af, 'location', 0, tuple(AH))
T.pop_in(af, 172, AS, 8)
K(af, 'location', 226, tuple(AH))
K(af, 'location', 240, tuple(AV))
for k, f in enumerate(range(246, 346, 12)):
    K(af, 'location', f, tuple(AV + Vector((0, 0, 0.03 if k % 2 else -0.01))))
K(af, 'location', 350, tuple(AV))
K(af, 'location', 358, tuple(PR))
SW3 = 358
K(af, 'scale', SW3, (AS,) * 3)
K(af, 'scale', SW3 + 1, (0, 0, 0))
K(ap, 'scale', 0, (0, 0, 0))
K(ap, 'scale', SW3, (0, 0, 0))
K(ap, 'scale', SW3 + 1, (AS / BSC,) * 3)


def card(txt, rgb, loc, w, f_in, f_out, size=0.15):
    h = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, 0.22), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), h)
    glyph(txt, size, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), h, (0, -0.022, -0.004))
    T.pop_in(h, f_in, 1.0, 8)
    T.pop_out(h, f_out, 1.0, 6)
    return h


PLq = pan_top('L', -TIP)
card('?', (0.85, 0.25, 0.08), (PLq.x, BC.y - 0.35, PLq.z + 0.98), 0.24, 244, 352, 0.17)
card('?', (0.08, 0.3, 0.85), (AV.x, BC.y - 0.35, AV.z + 0.42), 0.24, 250, 352, 0.17)
PLd = pan_top('L', TIP)
card('AIRE', (0.15, 0.45, 0.9), (PLd.x - 0.05, BC.y - 0.5, PLd.z + 1.0), 0.5, 520, 604, 0.13)
air = C.empty('air', None, (PLd.x, BC.y - 0.42, PLd.z + 0.42))
am = M((0.75, 0.9, 1.0), rough=0.2, coat=0.6, emit=0.5)
for k in range(5):
    a = k * 6.2832 / 5
    C.sphere('puff', (math.cos(a) * 0.15, 0, math.sin(a) * 0.15), (0.045, 0.02, 0.045), am, air, 16)
T.pop_in(air, 526, 1.0, 8)
T.pop_out(air, 604, 1.0, 6)

PRd = pan_top('R', TIP)
arrow = C.empty('arrow', None, (PRd.x + 0.42, BC.y - 0.2, PRd.z + 0.2))
lm = M((1.0, 0.78, 0.12), rough=0.3, coat=0.5, emit=1.0)
C.tube('shaft', [(0, 0, 0.28), (0, 0, -0.18)], 0.03, lm, arrow)
C.tube('h1', [(0, 0, -0.2), (-0.1, 0, -0.08)], 0.028, lm, arrow)
C.tube('h2', [(0, 0, -0.2), (0.1, 0, -0.08)], 0.028, lm, arrow)
T.pop_in(arrow, 382, 1.0, 8)
for k, f in enumerate(range(392, 500, 10)):
    K(arrow, 'location', f, tuple(Vector((PRd.x + 0.42, BC.y - 0.2, PRd.z + 0.2 - (0.06 if k % 2 else 0.0)))))
T.pop_out(arrow, 502, 1.0, 6)

bol = make('bolita', 1.3)
mok = make('moki', 1.4)
BL0 = Vector((-2.55, -1.95, Z0))
BL1 = Vector((-1.62, -1.95, Z0))
BLs = Vector((-1.5, -1.8, Z0))
for k, f in enumerate(range(0, 66, 6)):
    T.place(bol, f, BL0.lerp(BL1, min(1, f / 64)))
    S(bol, f, (1.06, 1.06, 0.92) if k % 2 else (0.98, 0.98, 1.03))
S(bol, 70, (1, 1, 1))
T.turn(bol, 0, 80)
for side in ('L', 'R'):
    T.arm(bol, side, 0, fwd=-80, out=20)
    T.arm(bol, side, 64, fwd=-80, out=20)
    T.rest_arm(bol, side, 74)
T.turn(bol, 70, 30)
T.place(bol, 108, BL1)
T.place(bol, 120, Vector((-1.45, -1.95, Z0)))
for side in ('L', 'R'):
    T.arm(bol, side, 112, 0, None)
    T.arm(bol, side, 122, fwd=-150, out=25)
    T.arm(bol, side, 146, fwd=-160, out=25)
    T.rest_arm(bol, side, 158)
S(bol, 122, (1.1, 1.1, 0.88))
S(bol, 134, (0.95, 0.95, 1.06))
S(bol, 150, (1, 1, 1))
T.place(bol, 156, Vector((-1.45, -1.95, Z0)))
T.place(bol, 168, BLs)
T.turn(bol, 168, 25)
T.turn(bol, 236, 35)
T.turn(bol, 380, 30)
for side in ('L', 'R'):
    T.arm(bol, side, 382, 0, None)
    T.arm(bol, side, 388, fwd=-60, out=50)
    T.arm(bol, side, 420, fwd=-60, out=50)
    T.rest_arm(bol, side, 432)
S(bol, 384, (1, 1, 1))
S(bol, 389, (1.1, 1.1, 0.88))
S(bol, 396, (1, 1, 1))
T.turn(bol, 520, 20)
T.place(bol, 636, BLs)
gesture(bol, 'hops', 642)
T.turn(bol, 690, 40)
T.arm(bol, 'R', 696, 0, None)
T.arm(bol, 'R', 704, fwd=-120, out=30)
T.arm(bol, 'L', 700, 0, None)
T.arm(bol, 'L', 708, fwd=-120, out=30)
T.turn(bol, 728, 5)
for side in ('L', 'R'):
    T.arm(bol, side, 736, fwd=-150, out=40)
    T.arm(bol, side, 760, fwd=-150, out=40)
    T.rest_arm(bol, side, 772)
T.place(bol, 766, BLs)
for f, dz in ((768, 0.0), (774, 0.35), (780, 0.0), (786, 0.3), (792, 0.0)):
    T.place(bol, f, BLs + Vector((0, 0, dz)))
land(bol, 792)
gesture(bol, 'sway', 812)

MK = Vector((1.22, -1.8, Z0))
T.place(mok, 0, MK)
T.turn(mok, 0, -35)
gesture(mok, 'breathe', 20)
T.arm(mok, 'L', 84, 0, None)
T.arm(mok, 'L', 94, fwd=-60, out=35)
T.arm(mok, 'L', 140, fwd=-60, out=35)
T.rest_arm(mok, 'L', 152)
T.arm(mok, 'L', 164, 0, None)
T.arm(mok, 'L', 172, fwd=-75, out=30)
T.arm(mok, 'L', 228, fwd=-75, out=30)
T.arm(mok, 'L', 240, fwd=-85, out=45)
T.arm(mok, 'L', 350, fwd=-85, out=45)
T.arm(mok, 'L', 358, fwd=-70, out=40)
T.rest_arm(mok, 'L', 372)
T.turn(mok, 236, -25)
T.arm(mok, 'R', 244, 0, None)
T.arm(mok, 'R', 252, fwd=-40, out=55)
T.arm(mok, 'R', 330, fwd=-40, out=55)
T.rest_arm(mok, 'R', 342)
T.turn(mok, 440, -30)
T.arm(mok, 'L', 448, 0, None)
T.arm(mok, 'L', 456, fwd=-80, out=35)
T.arm(mok, 'L', 500, fwd=-80, out=35)
T.rest_arm(mok, 'L', 510)
T.turn(mok, 512, -45)
T.arm(mok, 'L', 516, 0, None)
T.arm(mok, 'L', 524, fwd=-90, out=50)
T.arm(mok, 'L', 596, fwd=-90, out=50)
T.rest_arm(mok, 'L', 608)
T.turn(mok, 640, -30)
T.turn(mok, 740, -40)
gesture(mok, 'bounce', 790)
C.wave(mok, 'R', 820, cycles=2, period=8)

OP0 = ((-2.05, -3.7, 0.32), (-1.95, -1.95, 0.95), 24)
OP1 = ((-1.25, -3.7, 0.32), (-1.15, -1.95, 0.95), 24)
W0 = ((0.0, -6.4, 1.85), (0.0, -1.7, 0.92), 31)
WM = ((0.62, -4.3, 1.5), (0.62, -1.95, 1.12), 30)
WQ = ((0.0, -5.3, 1.6), (0.0, -1.95, 1.08), 30)
WS = ((0.15, -4.5, 1.25), (0.15, -1.95, 0.98), 30)
WB = ((-0.75, -4.2, 1.35), (-0.75, -1.9, 1.0), 30)
WE = ((-0.4, -4.9, 1.55), (-0.4, -1.9, 1.15), 30)
camkey(0, OP0)
camkey(64, OP1)
for a, b, pose in ((66, 162, W0), (164, 234, WM), (236, 350, WQ), (352, 440, WS), (442, 612, W0), (614, 700, WB), (702, 760, WE), (762, TOTAL - 1, W0)):
    camkey(a, pose)
    camkey(b, pose)

T.lines(EID, LINES)
T.blinks(bol, (40, 160, 300, 420, 560, 690, 830))
T.blinks(mok, (55, 190, 320, 470, 620, 760))
