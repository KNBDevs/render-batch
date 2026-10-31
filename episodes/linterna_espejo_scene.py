from stage import *
from episodes.linterna_espejo_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'linterna_espejo'
Z0 = 0.08
auto_dress(EID, ENV)
for l in list(bpy.data.lights):
    l.energy *= 0.42
    l.color = (0.82, 0.86, 1.0)
sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.2
bpy.data.materials['Sky'].node_tree.nodes['Emission'].inputs[1].default_value = 0.45

TP = Vector((-0.56, -2.0, 0.34))
BX = Vector((0.0, -1.95, Z0))
SH = Vector((0.78, -1.98, Z0))
SHC = SH + Vector((0, 0, 0.2))
MR = Vector((-0.38, -1.12, Z0))
MS = 1.4
F = MR + Vector((0, 0, 0.36 * MS))
HIT = Vector((-0.23, -1.97, 0.3))

box = C.empty('box', None, tuple(BX))
C.rounded_box('bx', (0, 0, 0.28), (0.44, 0.4, 0.56), 0.06, M((0.55, 0.62, 0.98), rough=0.45, coat=0.5), box)
C.rounded_box('lid', (0, 0, 0.57), (0.48, 0.44, 0.06), 0.4, M((0.98, 0.66, 0.4), rough=0.4, coat=0.6), box)
for z in (0.15, 0.42):
    C.rounded_box('band', (0, -0.205, z), (0.46, 0.02, 0.04), 0.4, M((0.98, 0.9, 0.55), rough=0.4, coat=0.6), box)

shell = spawn('sea_shell', 0, 640, 'candy', tuple(SH), 1.4, -20)

torch = spawn('toy_torch', 1, 7311, 'fresh', tuple(TP), 1.2, 0)
bpy.ops.object.light_add(type='SPOT', location=(0.09, 0, 0))
tl = bpy.context.object
tl.parent = torch
tl.rotation_euler = (0, -math.pi / 2, 0)
tl.data.color = (1.0, 0.92, 0.68)
tl.data.energy = 40
tl.data.spot_size = math.radians(22)
tl.data.spot_blend = 0.6
tl.data.shadow_soft_size = 0.02

beam_m = MA((1.0, 0.94, 0.62), 0.2, emit=1.0)
spot_m = M((1.0, 0.95, 0.7), rough=0.3, emit=3.0)
dim_m = M((1.0, 0.9, 0.7), rough=0.4, emit=0.5)


def beam(name, r0, r1, m=beam_m):
    o = C.empty(name, None, (0, 0, 0))
    C.lathe('cone', [(0.0, 0.0), (0.0, r0), (1.0, r1), (1.0, 0.0)], m, o, segs=32)
    o.scale = (0, 0, 0)
    return o


def aim(o, f, A, B, on=True):
    d = B - A
    K(o, 'location', f, tuple(A))
    K(o, 'rotation_euler', f, tuple(d.to_track_quat('Z', 'Y').to_euler()))
    K(o, 'scale', f, (1, 1, d.length) if on else (0, 0, 0))


def point(f, tgt):
    d = tgt - TP
    yaw = math.atan2(d.y, d.x)
    pitch = -math.atan2(d.z, math.hypot(d.x, d.y))
    K(torch, 'rotation_euler', f, (0, pitch, yaw))


def disc(name, loc, n, r, m):
    q = Vector((0, 0, 1)).rotation_difference(n.normalized())
    o = C.empty(name, None, tuple(loc), tuple(q.to_euler()))
    C.sphere('d', (0, 0, 0), (r, r, 0.004), m, o, 24)
    return o


def ball(name, loc, r, m):
    o = C.empty(name, None, tuple(loc))
    C.sphere('b', (0, 0, 0), (r, r, r), m, o, 20)
    return o


def show(o, f_in, f_out=None, s=1.0):
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f_in - 1, (0, 0, 0))
    K(o, 'scale', f_in + 3, (s, s, s))
    if f_out:
        K(o, 'scale', f_out, (s, s, s))
        K(o, 'scale', f_out + 3, (0, 0, 0))


TA = TP + (HIT - TP).normalized() * 0.1
b1 = beam('b1', 0.03, 0.09)
point(0, HIT)
aim(b1, 0, TA, HIT)
point(320, HIT)
aim(b1, 320, TA, HIT)
spot_box = disc('spbox', HIT + Vector((-0.004, 0, 0)), Vector((-1, 0, 0)), 0.085, spot_m)
show(spot_box, 1, 324)

mirror = spawn('hand_mirror', 0, 5512, 'candy', tuple(MR), MS, 0)
face = next(o for o in mirror.children if o.name.startswith('face'))
nrm = ((TP - F).normalized() + (SHC - F).normalized()).normalized()
face.rotation_euler = Vector((0, -1, 0)).rotation_difference(nrm).to_euler()
card = C.empty('card', None, tuple(F))
card.rotation_euler = face.rotation_euler
C.rounded_box('cb', (0, 0, 0), (0.44, 0.03, 0.44), 0.08, M((0.78, 0.58, 0.36), rough=0.85, coat=0.0), card)
for k in range(9):
    x = -0.18 + k * 0.045
    C.tube('flute', [(x, -0.017, -0.2), (x, -0.017, 0.2)], 0.004, M((0.66, 0.47, 0.28), rough=0.9, coat=0.0), card)
stand = spawn('card_easel', 1, 2208, 'candy', tuple(MR + Vector((0, 0.02, 0))), 1.2, 0)
T.pop_in(stand, 330, 1.2, 8)
T.pop_out(stand, 438, 1.2, 6)
T.pop_in(card, 334, 1.0, 8)
T.pop_out(card, 436, 1.0, 6)
T.pop_in(mirror, 444, MS, 10)

FC = F + nrm * 0.03
point(336, FC)
TB = TP + (FC - TP).normalized() * 0.1
for f in (336, 900):
    aim(b1, f, TB, FC)
spot_card = disc('spcard', F + nrm * 0.02, nrm, 0.06, dim_m)
show(spot_card, 340, 436)
glow_card = ball('gc', SHC + Vector((0, -0.02, 0)), 0.05, MA((1.0, 0.9, 0.6), 0.12, emit=0.4))
show(glow_card, 360, 436)
spot_m2 = disc('spmir', F + nrm * 0.02, nrm, 0.07, spot_m)
show(spot_m2, 452)

b2 = beam('b2', 0.05, 0.09)
aim(b2, 0, FC, FC + (SHC - FC) * 0.05, False)
aim(b2, 454, FC, FC + (SHC - FC) * 0.05, False)
aim(b2, 455, FC, FC + (SHC - FC) * 0.05)
aim(b2, 464, FC, SHC)
aim(b2, 700, FC, SHC)
halo = ball('halo', SHC + Vector((0, -0.05, 0)), 0.13, MA((1.0, 0.92, 0.6), 0.1, emit=0.8))
show(halo, 464, 700)
bpy.ops.object.light_add(type='POINT', location=tuple(SHC + Vector((0, -0.25, 0.1))))
sl = bpy.context.object
sl.data.color = (1.0, 0.9, 0.65)
for f, v in ((0, 0), (462, 0), (468, 10), (700, 10), (712, 0)):
    sl.data.energy = v
    sl.data.keyframe_insert('energy', frame=f)

arr_m = M((1.0, 0.45, 0.75), rough=0.3, coat=0.4, emit=1.4)
UP = Vector((0, -0.06, 0.16))


def arrow(name, A, B, f):
    o = C.empty(name, None, tuple(A + UP))
    d = B - A
    C.tube('sh', [(0, 0, 0), tuple(d * 0.92)], 0.026, arr_m, o)
    u = d.normalized()
    side = u.cross(Vector((0, -1, 0))).normalized()
    tip = d
    for sg in (1, -1):
        C.tube('hd', [tuple(tip), tuple(tip - u * 0.13 + side * sg * 0.09)], 0.026, arr_m, o)
    show(o, f, 640)
    return o


arrow('ar1', TP + (FC - TP) * 0.12, FC, 566)
arrow('ar2', FC, SHC + (FC - SHC) * 0.1, 590)


def label(txt, rgb, loc, w, f_in, f_out):
    h = C.empty('lab', None, loc)
    C.rounded_box('lc', (0, 0, 0), (w, 0.03, 0.18), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.25), h)
    glyph(txt, 0.13, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), h, (0, -0.022, -0.004))
    T.pop_in(h, f_in, 1.0, 8)
    T.pop_out(h, f_out, 1.0, 6)


label('¿ESPEJO?', (0.1, 0.35, 0.85), (-0.4, -2.4, 1.76), 0.74, 244, 326)
label('¿CARTÓN?', (0.62, 0.32, 0.08), (0.42, -2.4, 1.76), 0.74, 250, 326)

DANCE = [(744, Vector((0.55, -1.45, 0))), (756, Vector((0.32, -1.3, 0))), (768, Vector((0.7, -1.22, 0))), (780, Vector((1.0, -1.4, 0))),
         (792, Vector((0.62, -1.45, 0))), (804, Vector((0.38, -1.25, 0))), (816, Vector((0.85, -1.2, 0))), (830, Vector((0.55, -1.38, 0)))]
FLOOR = Z0 + 0.006
fspot = C.empty('fspot', None, (0, 0, 0))
C.sphere('fs', (0, 0, 0), (0.15, 0.15, 0.006), spot_m, fspot, 24)
fspot.scale = (0, 0, 0)
K(fspot, 'scale', 0, (0, 0, 0))
K(fspot, 'scale', 712, (0, 0, 0))
K(fspot, 'scale', 718, (1, 1, 1))
P0 = Vector((SHC.x - 0.05, SHC.y + 0.02, FLOOR))
K(fspot, 'location', 712, tuple(P0))
aim(b2, 712, FC, P0)
for f, p in DANCE:
    q = Vector((p.x, p.y, FLOOR))
    K(fspot, 'location', f, tuple(q))
    aim(b2, f, FC, q)
    n = ((TP - F).normalized() + (q - F).normalized()).normalized()
    K(face, 'rotation_euler', f, tuple(Vector((0, -1, 0)).rotation_difference(n).to_euler()))
K(face, 'rotation_euler', 700, tuple(Vector((0, -1, 0)).rotation_difference(nrm).to_euler()))
K(face, 'rotation_euler', 0, tuple(Vector((0, -1, 0)).rotation_difference(nrm).to_euler()))
K(fspot, 'location', TOTAL - 1, tuple(Vector((0.55, -1.38, FLOOR))))
aim(b2, TOTAL - 1, FC, Vector((0.55, -1.38, FLOOR)))

OP0 = ((-0.25, -4.7, 0.36), (-0.2, -1.9, 0.52), 17)
OP1 = ((-0.25, -4.9, 0.44), (-0.2, -1.9, 0.52), 17)
W0 = ((-0.15, -6.3, 1.75), (-0.15, -1.5, 0.95), 26)
WC = ((-0.18, -5.3, 1.35), (-0.15, -1.55, 0.8), 21)
WI = ((-0.15, -5.5, 1.55), (-0.15, -1.6, 0.85), 21.5)
WD = ((-0.15, -5.85, 1.8), (-0.15, -1.6, 0.92), 23)
camkey(0, OP0)
camkey(84, OP1)
for a, b, pose in ((88, 330, W0), (332, 556, WC), (558, 700, WI), (702, TOTAL - 1, WD)):
    camkey(a, pose)
    camkey(b, pose)

pimo = make('pimo', 1.3)
bopi = make('bopi', 1.4)
P0p = Vector((-1.0, -1.8, Z0))
B0 = Vector((0.75, -0.8, Z0))
T.place(pimo, 0, P0p)
T.turn(pimo, 0, 45)
T.arm(pimo, 'R', 0, fwd=-50, out=10)
T.arm(pimo, 'R', 900, fwd=-50, out=10)
S(pimo, 8, (1, 1, 1))
S(pimo, 12, (1.06, 1.06, 0.92))
S(pimo, 18, (1, 1, 1))
T.turn(pimo, 30, 20)
T.turn(pimo, 60, 45)
gesture(pimo, 'hops', 178)
T.turn(pimo, 236, 30)
T.turn(pimo, 400, 40)
S(pimo, 400, (1, 1, 1))
S(pimo, 405, (0.95, 0.95, 1.06))
S(pimo, 412, (1, 1, 1))
gesture(pimo, 'bounce', 470)
T.turn(pimo, 560, 30)
for f in (676, 690):
    S(pimo, f, (1, 1, 1))
    S(pimo, f + 5, (1.04, 1.04, 0.9))
    S(pimo, f + 10, (1, 1, 1))
T.turn(pimo, 742, 35)
gesture(pimo, 'bounce', 800)

T.place(bopi, 0, B0)
T.turn(bopi, 0, -25)
T.arm(bopi, 'L', 92, 0, None)
T.arm(bopi, 'L', 100, fwd=-80, out=50)
T.arm(bopi, 'L', 118, fwd=-80, out=10)
T.arm(bopi, 'L', 150, fwd=-80, out=10)
T.rest_arm(bopi, 'L', 162)
T.turn(bopi, 236, -10)
for side in ('L', 'R'):
    T.arm(bopi, side, 320, 0, None)
    T.arm(bopi, side, 330, fwd=-70, out=15)
    T.arm(bopi, side, 346, fwd=-70, out=15)
    T.rest_arm(bopi, side, 358)
    T.arm(bopi, side, 436, 0, None)
    T.arm(bopi, side, 444, fwd=-70, out=15)
    T.arm(bopi, side, 458, fwd=-70, out=15)
    T.rest_arm(bopi, side, 470)
T.turn(bopi, 560, -20)
T.arm(bopi, 'R', 562, 0, None)
T.arm(bopi, 'R', 570, fwd=-60, out=40)
T.arm(bopi, 'R', 630, fwd=-60, out=40)
T.rest_arm(bopi, 'R', 640)
T.turn(bopi, 650, 0)
T.arm(bopi, 'R', 650, 0, None)
T.arm(bopi, 'R', 656, fwd=-150, out=10)
for k, f in enumerate(range(660, 696, 6)):
    K(bopi['spin'], 'rotation_euler', f, (0, 0, math.radians(8 if k % 2 else -8)))
T.arm(bopi, 'R', 696, fwd=-150, out=10)
T.rest_arm(bopi, 'R', 706)
B1 = Vector((0.85, -1.15, Z0))
B2 = Vector((0.45, -1.1, Z0))
B3 = Vector((0.95, -1.05, Z0))
hop_to(bopi, 760, B0, B1, 12, 0.3)
T.turn(bopi, 772, -60)
hop_to(bopi, 784, B1, B2, 12, 0.3)
T.turn(bopi, 796, 30)
hop_to(bopi, 808, B2, B3, 12, 0.3)
T.turn(bopi, 822, -20)
gesture(bopi, 'spin', 830)

T.lines(EID, LINES)
T.blinks(pimo, (40, 150, 300, 430, 600, 720, 840))
T.blinks(bopi, (70, 210, 360, 520, 680, 820))
