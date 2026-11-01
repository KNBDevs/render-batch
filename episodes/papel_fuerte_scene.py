from stage import *
from episodes.papel_fuerte_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'papel_fuerte'
Z0 = 0.08
auto_dress(EID, ENV)
LIL = (1.0, 0.42, 0.82)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, LIL), (52, LIL), (66, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (1.0, 0.78, 0.95, 1)), (52, (1.0, 0.78, 0.95, 1)), (66, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

YC = -2.0
spawn('low_table', 2, 6113, 'fresh', (0.0, YC, Z0), 1.0, 0)
TOP = Z0 + 0.62
BX = 0.30
for k, x in enumerate((-BX, BX)):
    spawn('book_stack', k, 4410 + 7 * k, 'candy', (x, YC, TOP), 1.0, 0)
BT = TOP + 0.2
GAP = 0.17
L2, W2 = 0.36, 0.15
NX, NY = 37, 21
A = 0.026
D = 0.17

verts = []
for i in range(NX):
    for j in range(NY):
        verts.append((-L2 + 2 * L2 * i / (NX - 1), -W2 + 2 * W2 * j / (NY - 1), 0.0))
faces = [(i * NY + j, (i + 1) * NY + j, (i + 1) * NY + j + 1, i * NY + j + 1) for i in range(NX - 1) for j in range(NY - 1)]
me = bpy.data.meshes.new('paper')
me.from_pydata(verts, [], faces)
paper = C.link(bpy.data.objects.new('paper', me), None)
paper.location = (0, YC, BT + 0.002)
pm = M((1.0, 0.92, 0.66), rough=0.6, coat=0.2)
pm2 = M((0.38, 0.62, 1.0), rough=0.6, coat=0.2)
me.materials.append(pm)
me.materials.append(pm2)
for p in me.polygons:
    p.use_smooth = False
    p.material_index = (p.index % (NY - 1)) % 2
sol = paper.modifiers.new('sol', 'SOLIDIFY')
sol.thickness = 0.005
paper.shape_key_add(name='base')
sag = paper.shape_key_add(name='sag', from_mix=False)
fold = paper.shape_key_add(name='fold', from_mix=False)
SL = GAP + 0.09
for n, (x, y, z) in enumerate(verts):
    s = abs(x)
    sg = 1 if x >= 0 else -1
    if s <= SL:
        xn = sg * s * GAP / SL
        zn = -D * math.cos(math.pi * xn / (2 * GAP)) ** 2
    else:
        xn = sg * (s - 0.09)
        zn = 0.0
    sag.data[n].co = (xn, y, zn)
    j = n % NY
    fold.data[n].co = (x, y * 0.55, A if j % 2 else 0.0)
lines_ = M((0.35, 0.6, 0.98), rough=0.4, coat=0.5)
ink = C.empty('ink', paper, (0, 0, 0))
for j in (3, 9, 15):
    yb = -W2 + 2 * W2 * j / (NY - 1)
    C.tube('stripe', [(-L2 + 0.02, yb, 0.004), (L2 - 0.02, yb, 0.004)], 0.004, lines_, ink)
K(ink, 'scale', 0, (1, 1, 1))
K(ink, 'scale', 104, (1, 1, 1))
K(ink, 'scale', 114, (0, 0, 0))


def kv(key, f, v):
    key.value = v
    key.keyframe_insert('value', frame=f)


kv(sag, 0, 0)
kv(sag, 11, 0)
kv(sag, 18, 0.85)
kv(sag, 22, 1.0)
kv(sag, 120, 1.0)
kv(sag, 134, 0.0)
kv(fold, 0, 0)
kv(fold, 148, 0)
kv(fold, 190, 1.0)
kv(sag, 368, 0.0)
kv(sag, 373, 0.07)
kv(sag, 380, 0.035)
kv(sag, 646, 0.035)
kv(sag, 652, 0.09)
kv(sag, 660, 0.06)
PL = Vector((0, YC, BT + 0.002))
K(paper, 'location', 0, tuple(PL))
K(paper, 'location', 118, tuple(PL))
K(paper, 'location', 138, (0.12, YC - 0.12, BT + 0.32))
K(paper, 'location', 300, (0.12, YC - 0.12, BT + 0.32))
K(paper, 'location', 316, tuple(PL))
K(paper, 'rotation_euler', 118, (0, 0, 0))
K(paper, 'rotation_euler', 138, (math.radians(-55), 0, 0))
K(paper, 'rotation_euler', 160, (math.radians(-55), math.radians(6), 0))
K(paper, 'rotation_euler', 180, (math.radians(-55), math.radians(-5), 0))
K(paper, 'rotation_euler', 200, (math.radians(-55), 0, 0))
K(paper, 'rotation_euler', 300, (math.radians(-55), 0, 0))
K(paper, 'rotation_euler', 316, (0, 0, 0))
for mm in (pm, pm2):
    glow = mm.node_tree.nodes.get('Principled BSDF')
    if glow is None:
        continue
    es = glow.inputs.get('Emission Strength')
    ec = glow.inputs.get('Emission Color') or glow.inputs.get('Emission')
    if es is None or ec is None:
        continue
    ec.default_value = (1.0, 0.85, 0.3, 1)
    for f, v in ((0, 0.0), (452, 0.0), (464, 0.25), (530, 0.25), (542, 0.0)):
        es.default_value = v
        es.keyframe_insert('default_value', frame=f)

AS = 0.72
AH = 0.185 * AS
a1 = spawn('fruit', 0, 31, 'pastel', (0, YC, BT + 0.9), AS, 0)
TOPF = BT + 0.002 + A + 0.004
K(a1, 'location', 0, (0, YC, BT + 0.9))
K(a1, 'location', 6, (0, YC, BT + 0.5))
K(a1, 'location', 11, (0, YC, BT + 0.006))
K(a1, 'location', 22, (0, YC, BT - D + 0.006))
K(a1, 'location', 34, (0, YC - 0.3, TOP + 0.002))
K(a1, 'location', 40, (0, YC - 0.34, TOP + 0.002))
K(a1, 'rotation_euler', 22, (0, 0, 0))
K(a1, 'rotation_euler', 40, (math.radians(-80), 0, 0))
K(a1, 'rotation_euler', 330, (math.radians(-80), 0, 0))
K(a1, 'location', 330, (0, YC - 0.34, TOP + 0.002))
K(a1, 'location', 346, (-0.2, YC - 0.3, BT + 0.3))
K(a1, 'rotation_euler', 352, (0, 0, 0))
K(a1, 'location', 360, (-0.09, YC, BT + 0.14))
K(a1, 'location', 368, (-0.09, YC, TOPF))
K(a1, 'location', 373, (-0.09, YC, TOPF - 0.07 * D))
K(a1, 'location', 380, (-0.09, YC, TOPF - 0.035 * D))
K(a1, 'location', 646, (-0.09, YC, TOPF - 0.035 * D))
K(a1, 'location', 652, (-0.09, YC, TOPF - 0.08 * D))
K(a1, 'location', 660, (-0.09, YC, TOPF - 0.055 * D))
a2 = spawn('fruit', 0, 32, 'pastel', (0.62, YC + 0.1, TOP), AS, 30)
K(a2, 'location', 0, (0.62, YC + 0.1, TOP + 0.002))
K(a2, 'location', 612, (0.62, YC + 0.1, TOP + 0.002))
K(a2, 'location', 628, (0.34, YC - 0.22, BT + 0.3))
K(a2, 'location', 640, (0.1, YC, BT + 0.12))
K(a2, 'location', 646, (0.1, YC, TOPF))
K(a2, 'location', 652, (0.1, YC, TOPF - 0.08 * D))
K(a2, 'location', 660, (0.1, YC, TOPF - 0.055 * D))

arm_ = M((1.0, 0.78, 0.15), rough=0.3, coat=0.4, emit=1.0)
ups = C.empty('ups', None, (0, YC - 0.12, 0))
for x in (-0.09, 0.0, 0.09):
    C.tube('au', [(x, 0, TOP + 0.03), (x, 0, BT - 0.04)], 0.008, arm_, ups)
    C.tube('al', [(x - 0.018, 0, BT - 0.065), (x, 0, BT - 0.035)], 0.007, arm_, ups)
    C.tube('ar', [(x + 0.018, 0, BT - 0.065), (x, 0, BT - 0.035)], 0.007, arm_, ups)
K(ups, 'scale', 0, (1, 1, 0))
K(ups, 'scale', 470, (1, 1, 0))
K(ups, 'scale', 480, (1, 1, 1))
K(ups, 'scale', 536, (1, 1, 1))
K(ups, 'scale', 544, (1, 1, 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.18, sz=0.13):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


label('¿AGUANTA?', (0.15, 0.55, 0.3), (-0.48, YC - 0.3, TOP + 1.12), 0.84, 236, 320)
label('¿SE CAE?', (0.85, 0.25, 0.3), (0.46, YC - 0.3, TOP + 1.12), 0.7, 242, 320)

OP0 = ((0.0, YC - 0.95, TOP + 0.08), (0.0, YC, BT + 0.12), 24)
OP1 = ((0.0, YC - 1.0, TOP + 0.1), (0.0, YC, BT + 0.02), 24)
W0 = ((0.0, -6.3, 1.95), (0.0, -1.6, 0.95), 29)
WF = ((0.0, -4.9, 1.7), (0.0, -1.8, 1.05), 28)
WQ = ((0.0, -5.7, 1.8), (0.0, -1.8, 1.1), 26)
CJ = ((0.0, YC - 1.5, BT + 0.45), (0.0, YC, BT - 0.01), 50)
CS_ = ((0.95, YC - 0.55, BT + 0.1), (0.12, YC, BT - 0.02), 40)
WE = ((0.0, -5.3, 1.65), (0.0, -1.7, 1.05), 24)
camkey(0, OP0)
camkey(56, OP1)
for a, b, pose in ((58, 140, W0), (142, 318, WF), (320, 428, CJ), (430, 548, CS_), (550, 608, WQ), (610, 700, CJ), (702, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

ruki = make('ruki', 1.35)
moki = make('moki', 1.3)
R0 = Vector((-0.84, -1.4, Z0))
M0 = Vector((0.84, -1.38, Z0))
T.place(ruki, 0, R0)
T.turn(ruki, 0, 30)
S(ruki, 20, (1, 1, 1))
S(ruki, 24, (1.08, 1.08, 0.88))
S(ruki, 30, (0.96, 0.96, 1.06))
S(ruki, 36, (1, 1, 1))
for side in ('L', 'R'):
    T.arm(ruki, side, 24, 0, None)
    T.arm(ruki, side, 32, fwd=-40, out=70)
    T.arm(ruki, side, 80, fwd=-40, out=70)
    T.rest_arm(ruki, side, 92)
gesture(ruki, 'sway', 100)
for side in ('L', 'R'):
    T.arm(ruki, side, 200, 0, None)
    T.arm(ruki, side, 208, fwd=-55, out=45)
    T.arm(ruki, side, 286, fwd=-55, out=45)
    T.rest_arm(ruki, side, 296)
T.turn(ruki, 320, 20)
T.arm(ruki, 'R', 326, 0, None)
T.arm(ruki, 'R', 336, fwd=-100, out=15)
T.arm(ruki, 'R', 358, fwd=-110, out=10)
T.rest_arm(ruki, 'R', 372)
gesture(ruki, 'hops', 382)
for side in ('L', 'R'):
    T.arm(ruki, side, 380, 0, None)
    T.arm(ruki, side, 388, fwd=-140, out=30)
    T.arm(ruki, side, 424, fwd=-140, out=30)
    T.rest_arm(ruki, side, 434)
T.turn(ruki, 556, 40)
T.arm(ruki, 'L', 560, 0, None)
T.arm(ruki, 'L', 568, fwd=-80, out=35)
T.arm(ruki, 'L', 612, fwd=-80, out=35)
T.rest_arm(ruki, 'L', 620)
T.turn(ruki, 700, 25)
gesture(ruki, 'bounce', 784)
for side in ('L', 'R'):
    T.arm(ruki, side, 784, 0, None)
    T.arm(ruki, side, 792, fwd=-150, out=20)
    T.arm(ruki, side, 820, fwd=-150, out=20)
    T.rest_arm(ruki, side, 830)
C.wave(ruki, 'L', 832, cycles=2, period=8)

T.place(moki, 0, M0)
T.turn(moki, 0, -25)
S(moki, 24, (1, 1, 1))
S(moki, 28, (1.06, 1.06, 0.9))
S(moki, 34, (1, 1, 1))
gesture(moki, 'breathe', 50)
T.arm(moki, 'R', 104, 0, None)
T.arm(moki, 'R', 112, fwd=-150, out=10)
T.arm(moki, 'R', 132, fwd=-150, out=10)
for side in ('L', 'R'):
    T.arm(moki, side, 134, 0, None)
    T.arm(moki, side, 142, fwd=-85, out=30)
    T.arm(moki, side, 296, fwd=-85, out=30)
    T.arm(moki, side, 312, fwd=-100, out=20)
    T.rest_arm(moki, side, 322)
T.turn(moki, 140, -45)
for f in (152, 166, 180):
    S(moki, f, (1.03, 1.03, 0.95))
    S(moki, f + 6, (1, 1, 1))
T.turn(moki, 330, -25)
T.arm(moki, 'R', 452, 0, None)
T.arm(moki, 'R', 460, fwd=-75, out=30)
T.arm(moki, 'R', 530, fwd=-75, out=30)
T.rest_arm(moki, 'R', 540)
T.turn(moki, 604, -40)
T.arm(moki, 'L', 606, 0, None)
T.arm(moki, 'L', 616, fwd=-95, out=20)
T.arm(moki, 'L', 642, fwd=-110, out=10)
T.rest_arm(moki, 'L', 656)
T.turn(moki, 672, -20)
gesture(moki, 'hops', 676)
for side in ('L', 'R'):
    T.arm(moki, side, 700, 0, None)
    T.arm(moki, side, 710, fwd=-120, out=30)
    T.arm(moki, side, 752, fwd=-120, out=30)
    T.rest_arm(moki, side, 762)
C.wave(moki, 'R', 812, cycles=2, period=8)
confetti(800, (0.0, YC, BT + 0.9), n=24, spread=1.2)

T.lines(EID, LINES)
T.blinks(ruki, (44, 160, 300, 470, 580, 690, 830))
T.blinks(moki, (70, 190, 340, 480, 630, 780))
