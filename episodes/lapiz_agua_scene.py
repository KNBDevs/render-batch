from stage import *
from episodes.lapiz_agua_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'lapiz_agua'
Z0 = 0.08
auto_dress(EID, ENV)
BLUE = (0.55, 0.82, 1.0)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, BLUE), (64, BLUE), (78, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
for f, c in ((0, (0.3, 0.62, 1.0, 1)), (64, (0.3, 0.62, 1.0, 1)), (78, (0.6, 0.75, 1.0, 1))):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

TC = Vector((0.0, -2.0, Z0))
spawn('low_table', 2, 4407, 'candy', tuple(TC), 1.0, 0)
TOP = Z0 + 0.62
CUP = Vector((0.0, -2.0, TOP))
CS = 2.0
cup = spawn('clear_cup', 1, 3901, 'candy', tuple(CUP), CS, 0)
piv = next(o for o in cup.children if o.name.startswith('water_pivot'))
FILL = 0.75
piv.scale = (1, 1, FILL)
for o in piv.children:
    o.data.materials.clear()
    o.data.materials.append(MA((0.4, 0.72, 1.0), 0.2, rough=0.04, emit=0.04))
WZ = TOP + CS * (0.032 + 0.22 * FILL)
C.tube('surf', [(math.cos(k * 6.2832 / 48) * 0.168, math.sin(k * 6.2832 / 48) * 0.168, 0) for k in range(49)], 0.004, MA((0.85, 0.95, 1.0), 0.6, emit=0.3), None).location = (CUP.x, CUP.y, WZ)

LEAN = math.radians(16)
PSC = 1.3
CUT = 0.24
SHIFT = 0.075
P_IN = Vector((0.03, CUP.y, WZ))
P_UP = Vector((-0.2, -2.12, TOP + 0.8))
pen = C.empty('pen', None, tuple(P_IN), (0, LEAN, 0))
pr = spawn('big_pencil', 0, 2290, 'candy', (0, 0, -CUT * PSC), PSC, 0, pen, L=0.8, cut=CUT)
under = next(o for o in pr.children if o.name.startswith('under'))


def broken(o, f, on, sh=SHIFT):
    K(o, 'location', f, (sh if on else 0.0, 0, 0))
    K(o, 'scale', f, (1.2, 1.2, 1.0) if on else (1, 1, 1))
    K(o, 'rotation_euler', f, (0, math.radians(-7 if sh > 0 else 7) if on else 0, 0))


broken(under, 0, True)
broken(under, 127, True)
broken(under, 129, False)
K(pen, 'location', 0, tuple(P_IN))
K(pen, 'rotation_euler', 0, (0, LEAN, 0))
K(pen, 'location', 126, tuple(P_IN))
K(pen, 'rotation_euler', 126, (0, LEAN, 0))
K(pen, 'location', 134, tuple(P_IN + Vector((0, 0, 0.42))))
K(pen, 'rotation_euler', 134, (0, LEAN * 0.5, 0))
K(pen, 'location', 146, tuple(P_UP))
K(pen, 'rotation_euler', 146, (0, math.radians(90), 0))
for k, f in enumerate(range(158, 320, 20)):
    K(pen, 'rotation_euler', f, (math.radians(4 if k % 2 else -4), math.radians(90), 0))
K(pen, 'location', 326, tuple(P_UP))
K(pen, 'rotation_euler', 326, (0, math.radians(90), 0))
K(pen, 'location', 336, tuple(P_IN + Vector((0, 0, 0.42))))
K(pen, 'rotation_euler', 336, (0, LEAN * 0.5, 0))
K(pen, 'location', 344, tuple(P_IN))
K(pen, 'rotation_euler', 344, (0, LEAN, 0))
broken(under, 341, False)
broken(under, 343, True)
broken(under, 465, True)
broken(under, 466, False)
broken(under, 555, False)
broken(under, 556, True)

W0 = ((0.0, -6.3, 1.9), (0.0, -1.6, 0.86), 31)
OP = ((-0.12, CUP.y - 1.15, 0.98), (-0.1, CUP.y, 0.98), 30)
WM = ((0.0, -3.95, 1.55), (0.0, -2.12, 1.36), 30)
WS = ((0.0, -3.25, 1.12), (0.02, -2.0, 1.02), 36)
WT = ((0.03, -2.32, TOP + 1.95), (0.03, -2.0, TOP + 0.3), 34)
WP = ((0.0, -5.6, 1.75), (0.0, -1.3, 1.62), 31)
WQ = ((0.05, -4.7, 1.6), (0.05, -1.8, 1.08), 28)
WE = ((-0.35, -4.1, 1.45), (-0.35, -1.9, 1.08), 30)
for a, b, pose in ((0, 64, OP), (66, 124, W0), (126, 232, WM), (234, 350, WQ), (352, 464, WS), (466, 554, WT), (556, 690, WP), (692, 790, WE), (792, TOTAL - 1, W0)):
    camkey(a, pose)
    camkey(b, pose)

def label(txt, rgb, loc, w, f_in, f_out):
    h = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, 0.18), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), h)
    glyph(txt, 0.13, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), h, (0, -0.022, -0.004))
    T.pop_in(h, f_in, 1.0, 8)
    T.pop_out(h, f_out, 1.0, 6)


label('¿ROTO?', (0.85, 0.25, 0.08), (-0.36, CUP.y - 0.3, TOP + 1.2), 0.56, 244, 322)
label('¿ENTERO?', (0.08, 0.3, 0.85), (0.36, CUP.y - 0.3, TOP + 1.2), 0.72, 250, 322)

PNL = Vector((0.0, -1.05, 0.45))
PS = 1.7
panel = spawn('explain_panel', 0, 91, 'candy', tuple(PNL), PS, 0)
scr = next(o for o in panel.children if o.name.startswith('screen'))
R = 0.34 * 0.82
C.rounded_box('water', (0, -0.008, -0.105), (0.34, 0.004, 0.205), 0.01, M((0.45, 0.72, 1.0), rough=0.5, coat=0.2, emit=0.25), scr)
C.tube('wline', [(-0.17 + 0.34 * k / 16, -0.012, 0.006 * math.sin(k * 1.6)) for k in range(17)], 0.006, M((0.2, 0.45, 0.9), rough=0.4, emit=0.2), scr)
lm = M((1.0, 0.8, 0.15), rough=0.3, coat=0.4, emit=1.2)
A = Vector((-0.13, -0.018, -0.17))
S0 = Vector((0.0, -0.018, 0.0))
E = Vector((0.16, -0.018, 0.12))
seg1 = C.empty('seg1', scr, tuple(A))
C.tube('s1', [(0, 0, 0), tuple(S0 - A)], 0.012, lm, seg1)
seg2 = C.empty('seg2', scr, tuple(S0))
C.tube('s2', [(0, 0, 0), tuple(E - S0)], 0.012, lm, seg2)
d = (E - S0).normalized()
nrm = Vector((-d.z, 0, d.x))
head = C.empty('head', scr, tuple(E))
C.tube('h1', [(0, 0, 0), tuple(-d * 0.05 + nrm * 0.035)], 0.011, lm, head)
C.tube('h2', [(0, 0, 0), tuple(-d * 0.05 - nrm * 0.035)], 0.011, lm, head)
eye = C.empty('eye', scr, (0.205, -0.02, 0.165))
C.sphere('ew', (0, 0, 0), (0.04, 0.008, 0.026), M((1, 1, 1), rough=0.4, emit=0.3), eye, 20)
C.sphere('ep', (-0.01, -0.006, -0.004), (0.015, 0.006, 0.015), M((0.15, 0.2, 0.35), rough=0.4), eye, 14)
for o, f in ((seg1, 578), (seg2, 598), (head, 612), (eye, 566)):
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f, (0, 0, 0))
    K(o, 'scale', f + 12, (1, 1, 1))
T.pop_in(panel, 552, PS, 10)
T.pop_out(panel, 686, PS, 6)

ST_IN = Vector((-0.07, CUP.y - 0.02, WZ))
straw = C.empty('strawp', None, (0, 0, 0))
sw = spawn('striped_straw', 1, 812, 'fresh', (0, 0, -0.22), 1.0, 0, straw, L=0.7, cut=0.22)
sund = next(o for o in sw.children if o.name.startswith('under'))
HANDL = Vector((-0.62, -1.95, 0.95))
K(straw, 'location', 0, tuple(HANDL))
K(straw, 'rotation_euler', 0, (0, math.radians(-30), 0))
T.pop_in(straw, 690, 1.0, 8)
K(straw, 'location', 712, tuple(HANDL))
K(straw, 'location', 722, tuple(ST_IN + Vector((0, 0, 0.36))))
K(straw, 'rotation_euler', 722, (0, math.radians(-14), 0))
K(straw, 'location', 732, tuple(ST_IN))
K(straw, 'rotation_euler', 732, (0, math.radians(-20), 0))
broken(sund, 0, False)
broken(sund, 729, False)
broken(sund, 731, True, -SHIFT)

luma = make('luma', 1.45)
ruki = make('ruki', 1.45)
LS = Vector((-0.45, -1.55, Z0))
L0 = Vector((-0.92, -1.66, Z0))
R0 = Vector((1.0, -1.72, Z0))
T.place(luma, 0, LS)
T.turn(luma, 0, 0)
S(luma, 4, (1, 1, 1))
S(luma, 8, (1.12, 1.12, 0.84))
S(luma, 14, (0.94, 0.94, 1.1))
S(luma, 20, (1, 1, 1))
gesture(luma, 'hops', 22)
T.arm(luma, 'R', 6, fwd=-40, out=60)
T.arm(luma, 'L', 6, fwd=-40, out=60)
T.arm(luma, 'R', 50, fwd=-40, out=60)
T.arm(luma, 'L', 50, fwd=-40, out=60)
T.rest_arm(luma, 'R', 60)
T.rest_arm(luma, 'L', 60)
T.place(luma, 62, LS)
hop_to(luma, 64, LS, L0, 12, 0.35)
T.turn(luma, 78, 30)
gesture(luma, 'bounce', 174)
T.turn(luma, 236, 20)
T.turn(luma, 352, 30)
for side in ('L', 'R'):
    T.arm(luma, side, 398, 0, None)
    T.arm(luma, side, 404, fwd=-60, out=45)
    T.arm(luma, side, 440, fwd=-60, out=45)
    T.rest_arm(luma, side, 450)
S(luma, 400, (1, 1, 1))
S(luma, 405, (1.08, 1.08, 0.9))
S(luma, 412, (1, 1, 1))
T.turn(luma, 560, 15)
T.arm(luma, 'R', 684, 0, None)
T.arm(luma, 'R', 692, fwd=-70, out=25)
T.arm(luma, 'R', 734, fwd=-70, out=25)
T.rest_arm(luma, 'R', 746)
T.turn(luma, 700, 35)
gesture(luma, 'bounce', 758)
gesture(luma, 'sway', 800)
T.turn(luma, 800, 15)

T.place(ruki, 0, R0)
T.turn(ruki, 0, -30)
T.arm(ruki, 'R', 108, 0, None)
T.arm(ruki, 'R', 120, fwd=-75, out=25)
T.arm(ruki, 'R', 326, fwd=-75, out=25)
T.arm(ruki, 'R', 338, fwd=-55, out=25)
T.rest_arm(ruki, 'R', 352)
T.turn(ruki, 236, -10)
T.arm(ruki, 'L', 238, 0, None)
T.arm(ruki, 'L', 246, fwd=-50, out=40)
T.arm(ruki, 'L', 300, fwd=-50, out=40)
T.rest_arm(ruki, 'L', 312)
T.turn(ruki, 360, -30)
gesture(ruki, 'breathe', 478)
T.turn(ruki, 556, -45)
T.arm(ruki, 'L', 562, 0, None)
T.arm(ruki, 'L', 570, fwd=-85, out=35)
T.arm(ruki, 'L', 640, fwd=-85, out=35)
T.rest_arm(ruki, 'L', 652)
T.turn(ruki, 700, -35)
T.turn(ruki, 792, -15)
C.wave(ruki, 'R', 812, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(luma, (40, 150, 290, 380, 520, 660, 820))
T.blinks(ruki, (60, 200, 330, 450, 600, 760))
