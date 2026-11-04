from stage import *
from episodes.barquito_papel_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'barquito_papel'
Z0 = 0.08
auto_dress(EID, ENV)
LI = (0.35, 0.95, 0.88)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, LI), (52, LI), (64, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (0.25, 0.62, 0.66, 1)), (52, (0.25, 0.62, 0.66, 1)), (64, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

TX, TY = 0.1, -1.85
SB = 3.2
spawn('water_tray', 0, 931, 'fresh', (TX, TY, Z0), SB, 0)
WZ = Z0 + 0.058 * SB
FZ = Z0 + 0.016 * SB
XP, YP = TX - 0.2, TY - 0.3
XF, YF = TX + 0.24, TY + 0.32
BS = 2.2
DR = 0.035 * BS


def boat(style, seed):
    e = C.empty('carrier', None, (0, 0, -5))
    b = spawn('paper_boat', style, seed, 'candy', (0, 0, 0), BS, 0, parent=e)
    return e, b


def wet(b, f0, f1, rgb, w):
    m = C.mat('wet_' + b.name, rgb, rough=0.6, coat=0.25)
    for o in b.children_recursive:
        if o.type == 'MESH':
            o.data.materials.clear()
            o.data.materials.append(m)
    bc = m.node_tree.nodes['Principled BSDF'].inputs['Base Color']
    for f, c in ((0, rgb), (f0, rgb), (f1, w)):
        bc.default_value = (*c, 1)
        bc.keyframe_insert('default_value', frame=f)


Y = {}


def bob(e, f0, f1, x, z, ph=0.0):
    for f in range(f0, f1 + 1, 12):
        K(e, 'location', f, (x, Y[e.name], z + 0.012 * math.sin(f * 0.26 + ph)))
        K(e, 'rotation_euler', f, (math.radians(3 * math.sin(f * 0.21 + ph)), 0, 0))


def sink(e, b, f0, f1, x):
    y = Y[e.name]
    K(b, 'scale', f0, (BS, BS, BS))
    K(e, 'location', f0, (x, y, WZ - DR))
    K(e, 'rotation_euler', f0, (0, 0, 0))
    K(b, 'scale', f0 + (f1 - f0) // 2, (BS * 0.97, BS * 1.05, BS * 0.6))
    K(e, 'location', f0 + (f1 - f0) // 3, (x, y, WZ - DR - 0.06))
    K(e, 'rotation_euler', f0 + (f1 - f0) // 3, (0, math.radians(10), 0))
    K(b, 'scale', f1, (BS * 0.95, BS * 1.1, BS * 0.42))
    K(e, 'location', f1, (x + 0.04, y, FZ))
    K(e, 'rotation_euler', f1, (0, math.radians(14), 0))


BW = MA((0.8, 0.95, 1.0), 0.55, rough=0.05, emit=0.4)


def bubbles(x, y, fs):
    for i, f in enumerate(fs):
        d = C.empty('bub', None, (x + 0.05 * math.sin(i * 2.1), y - 0.1, FZ + 0.05))
        C.sphere('b', (0, 0, 0), (0.022, 0.022, 0.022), BW, d, 12)
        K(d, 'scale', 0, (0, 0, 0))
        K(d, 'scale', f - 1, (0, 0, 0))
        K(d, 'scale', f, (1, 1, 1))
        K(d, 'location', f, (x + 0.05 * math.sin(i * 2.1), y - 0.1, FZ + 0.05))
        K(d, 'location', f + 12, (x + 0.05 * math.sin(i * 2.1) + 0.03, y - 0.1, WZ + 0.01))
        K(d, 'scale', f + 13, (0, 0, 0))


RM = MA((0.85, 0.97, 1.0), 0.6, rough=0.05, emit=0.3)


def ripple(x, y, f0, r=0.3):
    o = C.empty('rip', None, (x, y, WZ + 0.004))
    C.tube('r', [(math.cos(k * 6.2832 / 32) * r, math.sin(k * 6.2832 / 32) * r * 0.7, 0) for k in range(33)], 0.008, RM, o)
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f0 - 1, (0, 0, 0))
    K(o, 'scale', f0, (0.3, 0.3, 1))
    K(o, 'scale', f0 + 14, (1.3, 1.3, 1))
    K(o, 'scale', f0 + 15, (0, 0, 0))


A, ab = boat(0, 941)
Y[A.name] = YP
wet(ab, 4, 30, (1.0, 0.86, 0.6), (0.82, 0.55, 0.32))
bob(A, 0, 20, XP, WZ - DR)
sink(A, ab, 22, 56, XP)
bubbles(XP, YP, (36, 40, 45, 50, 56))
T.pop_out(A, 160, 1.0, 6)

P, pb = boat(0, 942)
F, fb = boat(2, 943)
Y[P.name] = YP
Y[F.name] = YF
wet(pb, 350, 440, (1.0, 0.86, 0.6), (0.82, 0.55, 0.32))
for e, x, y in ((P, XP, YP), (F, XF, YF)):
    K(e, 'location', 0, (x, y, -5))
    K(e, 'location', 165, (x, y, -5))
    K(e, 'location', 166, (x, y, WZ + 0.55))
    T.pop_in(e, 166, 1.0, 8)
    K(e, 'location', 190, (x, y, WZ + 0.55))
    K(e, 'location', 204 if e is P else 210, (x, y, WZ - DR))
ripple(XP, YP, 205)
ripple(XF, YF, 211)
bob(P, 216, 420, XP, WZ - DR)
sink(P, pb, 426, 472, XP)
bubbles(XP, YP, (440, 446, 452, 458, 466, 472))
bob(F, 222, 756, XF, WZ - DR, 1.7)
XG = TX - 0.4
n = 8
for i in range(1, n + 1):
    u = i / n
    f = 768 + round(u * 64)
    K(F, 'location', f, (XF + (XG - XF) * u, YF, WZ - DR + 0.01 * math.sin(f * 0.26)))
for f in range(840, TOTAL, 12):
    K(F, 'location', f, (XG, YF, WZ - DR + 0.012 * math.sin(f * 0.26)))
for f in (776, 800, 824):
    ripple(XF + (XG - XF) * (f - 768) / 64, YF, f, 0.25)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


PC = (0.75, 0.35, 0.05)
FC = (0.15, 0.3, 0.6)
LP = (XP - 0.3, YP - 0.35, WZ + 0.66)
LF = (XF + 0.2, YF + 0.1, WZ + 0.98)
label('¿PAPEL?', PC, LP, 0.94, 240, 338)
label('¿ALUMINIO?', FC, LF, 1.28, 246, 338)
label('PAPEL', PC, LP, 0.8, 626, 716)
label('ALUMINIO', FC, LF, 1.12, 630, 716)

OP = ((XP - 0.15, YP - 1.35, WZ + 0.28), (XP, YP, WZ + 0.08), 30)
OP2 = ((XP - 0.1, YP - 1.25, WZ + 0.35), (XP, YP, WZ), 30)
W = ((0.1, -4.75, 2.35), (0.1, -1.45, 0.8), 24)
WQ = ((0.1, -4.6, 2.25), (0.1, -1.45, 0.82), 24)
CSN = ((XP - 0.3, YP - 1.5, WZ + 0.45), (XP, YP, WZ + 0.02), 30)
CH = ((XF + 0.45, YF - 1.7, WZ + 0.75), (XF, YF, WZ + 0.12), 30)
WE = ((0.0, -4.6, 2.2), (0.0, -1.45, 0.82), 24)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 200, W), (202, 340, WQ), (342, 400, W), (402, 476, CSN), (478, 542, W),
                   (544, 620, CH), (622, 720, WQ), (722, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

moki = make('moki', 1.3)
pimo = make('pimo', 1.45)
MK0 = Vector((-0.82, -0.72, Z0))
PM0 = Vector((1.02, -0.7, Z0))
T.place(moki, 0, MK0)
T.turn(moki, 0, 35)
T.turn(moki, 60, 25)
T.arm(moki, 'L', 10, 0, None)
T.arm(moki, 'L', 16, fwd=-90, out=30)
T.arm(moki, 'L', 70, fwd=-90, out=30)
T.rest_arm(moki, 'L', 80)
T.turn(moki, 226, 15)
gesture(moki, 'breathe', 250)
T.turn(moki, 340, 40)
T.turn(moki, 520, 30)
for side in ('L', 'R'):
    T.arm(moki, side, 548, 0, None)
    T.arm(moki, side, 554, fwd=-150, out=25)
    T.arm(moki, side, 600, fwd=-150, out=25)
    T.rest_arm(moki, side, 610)
gesture(moki, 'hops', 560)
MK1 = Vector((-0.75, -0.95, Z0))
hop_to(moki, 724, MK0, MK1, 12, 0.3)
T.turn(moki, 738, 60)
T.arm(moki, 'R', 752, 0, None)
T.arm(moki, 'R', 758, fwd=-150, out=30)
T.arm(moki, 'R', 800, fwd=-150, out=30)
T.rest_arm(moki, 'R', 810)
gesture(moki, 'hops', 800)
C.wave(moki, 'L', 826, cycles=2, period=8)

T.place(pimo, 0, PM0)
T.turn(pimo, 0, -35)
T.arm(pimo, 'R', 100, 0, None)
T.arm(pimo, 'R', 106, fwd=-150, out=30)
T.arm(pimo, 'R', 156, fwd=-150, out=30)
T.rest_arm(pimo, 'R', 166)
T.turn(pimo, 226, -20)
T.turn(pimo, 340, -45)
T.arm(pimo, 'L', 480, 0, None)
T.arm(pimo, 'L', 486, fwd=-80, out=40)
T.arm(pimo, 'L', 530, fwd=-80, out=40)
T.rest_arm(pimo, 'L', 540)
T.turn(pimo, 616, -25)
for side in ('L', 'R'):
    T.arm(pimo, side, 624, 0, None)
    T.arm(pimo, side, 630, fwd=-140, out=35)
    T.arm(pimo, side, 690, fwd=-140, out=35)
    T.rest_arm(pimo, side, 700)
T.turn(pimo, 720, -40)
C.wave(pimo, 'R', 820, cycles=2, period=8)
confetti(790, (XG, YF, WZ + 0.9), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(moki, (44, 150, 300, 460, 590, 700, 840))
T.blinks(pimo, (70, 190, 330, 500, 650, 790))
