from stage import *
from episodes.luz_colores_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'luz_colores'
Z0 = 0.08
auto_dress(EID, ENV)
DARK = (0.35, 0.4, 1.0)
LV = ((0, 0.2), (300, 0.2), (330, 0.14), (690, 0.14), (730, 0.4))
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    l.color = DARK
    for f, k in LV:
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0, s0 = tuple(bg[0].default_value), bg[1].default_value
for f, c, v in ((0, (0.05, 0.06, 0.2, 1), 0.25), (690, (0.05, 0.06, 0.2, 1), 0.2), (730, (0.12, 0.12, 0.35, 1), 0.4)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)
    bg[1].default_value = v
    bg[1].keyframe_insert('default_value', frame=f)
sky = bpy.data.materials.get('Sky')
if sky:
    se = sky.node_tree.nodes['Emission'].inputs[1]
    s1 = se.default_value
    for f, k in LV:
        se.default_value = s1 * k
        se.keyframe_insert('default_value', frame=f)

SX, SY, SZ = 0.0, -0.85, 1.0
SW, SH = 1.7, 1.1
scr = C.empty('light_screen', None, (SX, SY, Z0))
FR = M((0.62, 0.5, 0.95), rough=0.4, coat=0.6)
FR2 = M((0.98, 0.62, 0.72), rough=0.4, coat=0.6)
C.rounded_box('panel', (0, 0, SZ), (SW, 0.04, SH), 0.04, M((0.96, 0.96, 0.95), rough=0.75, coat=0.0), scr)
q = (SW / 2 + 0.03, SH / 2 + 0.03)
C.tube('frame', [(-q[0], -0.03, SZ - q[1]), (q[0], -0.03, SZ - q[1]), (q[0], -0.03, SZ + q[1]), (-q[0], -0.03, SZ + q[1]), (-q[0], -0.03, SZ - q[1])], 0.045, FR, scr)
for sx in (-1, 1):
    C.tube('leg', [(sx * (SW / 2 - 0.15), 0.02, SZ - q[1]), (sx * (SW / 2 - 0.05), 0.02, 0.06)], 0.035, FR, scr)
    C.sphere('foot', (sx * (SW / 2 - 0.05), 0.02, 0.04), (0.09, 0.12, 0.05), FR2, scr, 20)
for k in range(7):
    C.sphere('bead', (-SW / 2 + 0.2 + k * (SW - 0.4) / 6, -0.05, SZ + q[1] + 0.035), (0.035, 0.03, 0.035), FR2 if k % 2 else FR, scr, 14)

PY = SY - 0.03
RED = (1.0, 0.04, 0.04)
BLU = (0.08, 0.2, 1.0)


def rig_torch(style, seed, pos, rgb):
    t = spawn('toy_torch', style, seed, 'candy', pos, 1.5, 0)
    fl = C.empty('filter', t, (0.0, 0, 0))
    ax = C.empty('fax', fl, (0, 0, 0), (0, math.radians(90), 0))
    fr = [0.132, 0.071, 0.112][style] + 0.01
    lr = [0.062, 0.056, 0.03][style] + 0.012
    C.lathe('fring', [(fr - 0.005, lr - 0.012), (fr - 0.005, lr), (fr + 0.02, lr + 0.004), (fr + 0.03, lr - 0.004), (fr + 0.03, lr - 0.012)], M((0.98, 0.95, 0.9), rough=0.35, coat=0.7), ax, segs=40)
    C.lathe('fdisc', [(fr + 0.012, 0.0), (fr + 0.012, lr - 0.01), (fr + 0.02, lr - 0.01), (fr + 0.02, 0.0)], M(rgb, rough=0.1, coat=1.0, emit=3.0), ax, segs=40)
    bpy.ops.object.light_add(type='SPOT', location=pos)
    sp = bpy.context.object
    sp.data.color = rgb
    sp.data.spot_size = math.radians(34)
    sp.data.spot_blend = 0.12
    sp.data.shadow_soft_size = 0.02
    return t, sp


TR0 = Vector((-0.74, -2.1, Z0 + 0.62))
TB0 = Vector((0.7, -2.1, Z0 + 0.62))
tr, spr = rig_torch(0, 5501, TR0, RED)
tb, spb = rig_torch(2, 5502, TB0, BLU)


def aim(t, sp, f, pos, tgt):
    d = Vector(tgt) - Vector(pos)
    K(t, 'location', f, tuple(pos))
    K(t, 'rotation_euler', f, tuple(d.to_track_quat('X', 'Z').to_euler()))
    K(sp, 'location', f, tuple(Vector(pos) + d.normalized() * 0.32))
    K(sp, 'rotation_euler', f, tuple(d.to_track_quat('-Z', 'Y').to_euler()))


def power(sp, f, v):
    sp.data.energy = v
    sp.data.keyframe_insert('energy', frame=f)


P = 110
for sp, fo in ((spr, 4), (spb, 40)):
    power(sp, 0, 0)
    power(sp, fo, 0)
    power(sp, fo + 3, P)
L0 = (SX - 0.45, PY, SZ)
R0 = (SX + 0.45, PY, SZ)
LC = (SX - 0.17, PY, SZ)
RC = (SX + 0.17, PY, SZ)
plan = [(0, L0, R0), (350, L0, R0), (396, LC, RC), (720, LC, RC), (740, (SX - 0.38, PY, SZ + 0.1), (SX + 0.38, PY, SZ - 0.1)),
        (770, LC, RC)]
for (fa, la, ra), (fb, lb, rb) in zip(plan, plan[1:]):
    n = max(1, (fb - fa) // 6) if fb - fa < 100 else 1
    for i in range(n + 1):
        u = i / n
        e = u * u * (3 - 2 * u)
        f = round(fa + (fb - fa) * u)
        aim(tr, spr, f, TR0, Vector(la).lerp(Vector(lb), e))
        aim(tb, spb, f, TB0, Vector(ra).lerp(Vector(rb), e))
for o in (tr, tb, spr, spb):
    if o.animation_data:
        for fc in o.animation_data.action.fcurves if hasattr(o.animation_data.action, 'fcurves') else []:
            for kp in fc.keyframe_points:
                kp.interpolation = 'LINEAR'

spark = C.empty('spark', None, (SX, PY - 0.05, SZ))
C.sphere('s', (0, 0, 0), (0.08, 0.02, 0.08), M((1.0, 0.5, 0.9), rough=0.2, emit=3.0), spark, 16)
K(spark, 'scale', 0, (0, 0, 0))
K(spark, 'scale', 392, (0, 0, 0))
K(spark, 'scale', 398, (1.6, 1.6, 1.6))
K(spark, 'scale', 410, (0, 0, 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.35), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.5), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


MOR = (0.45, 0.15, 0.7)
FUC = (1.0, 0.1, 0.65)
TOPZ = Z0 + SZ + SH / 2 + 0.3
label('¿MORADO?', MOR, (SX - 0.5, SY - 0.6, TOPZ), 1.05, 230, 344)
label('¿ROSA?', FUC, (SX + 0.52, SY - 0.6, TOPZ + 0.3), 0.85, 236, 344)
label('LUZ', FUC, (SX + 0.4, SY - 0.45, Z0 + SZ + 0.36), 0.55, 560, 684, 0.22, 0.16)

pc = C.empty('paint_card', None, (SX - 0.3, SY - 0.55, Z0 + SZ + 0.4))
C.rounded_box('card', (0, 0, 0), (0.88, 0.03, 0.42), 0.4, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.35), pc)
glyph('PINTURA', 0.1, 0.01, M(MOR, rough=0.35, coat=0.5, emit=0.4), pc, (0, -0.022, 0.12))
for x, rgb in ((-0.29, (0.9, 0.08, 0.06)), (0.0, (0.1, 0.25, 0.95)), (0.29, (0.42, 0.12, 0.62))):
    C.metablob('dab', [((x, -0.02, -0.06), 0.075, (1, 0.4, 1)), ((x + 0.04, -0.02, -0.04), 0.06, (1, 0.4, 1)), ((x - 0.03, -0.02, -0.09), 0.05, (1, 0.4, 1))], M(rgb, rough=0.25, coat=0.8, emit=0.3), pc)
glyph('+', 0.1, 0.01, M((0.3, 0.3, 0.4), emit=0.3), pc, (-0.16, -0.03, -0.1))
glyph('=', 0.1, 0.01, M((0.3, 0.3, 0.4), emit=0.3), pc, (0.16, -0.03, -0.1))
T.pop_in(pc, 474, 1.0, 8)
T.pop_out(pc, 684, 1.0, 6)

OP = ((0.0, -3.1, 1.05), (0.0, SY, Z0 + SZ + 0.02), 22)
OP2 = ((0.0, -3.0, 1.05), (0.0, SY, Z0 + SZ + 0.02), 23)
W = ((0.0, -5.3, 1.8), (0.0, -1.3, 0.95), 19.5)
WQ = ((0.0, -5.2, 1.9), (0.0, -1.3, 1.08), 19.5)
CS = ((0.0, -3.7, 1.15), (0.0, SY, Z0 + SZ), 24)
CS2 = ((0.0, -3.5, 1.2), (0.0, SY, Z0 + SZ + 0.1), 24)
WE = ((0.0, -5.1, 1.8), (0.0, -1.3, 0.95), 19.5)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 190, W), (192, 350, WQ), (352, 466, CS), (468, 552, WQ), (554, 688, CS2), (690, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

bopi = make('bopi', 1.2)
ruki = make('ruki', 1.3)
BP0 = Vector((-1.15, -1.68, Z0))
RK0 = Vector((1.32, -1.62, Z0))
T.place(bopi, 0, BP0)
T.turn(bopi, 0, 30)
T.arm(bopi, 'R', 8, 0, None)
T.arm(bopi, 'R', 14, fwd=-90, out=30)
T.arm(bopi, 'R', 36, fwd=-90, out=30)
T.arm(bopi, 'L', 38, 0, None)
T.arm(bopi, 'L', 44, fwd=-90, out=30)
T.rest_arm(bopi, 'R', 50)
T.rest_arm(bopi, 'L', 70)
T.turn(bopi, 196, 15)
T.arm(bopi, 'R', 200, 0, None)
T.arm(bopi, 'R', 206, fwd=-150, out=25)
T.arm(bopi, 'R', 246, fwd=-150, out=25)
T.rest_arm(bopi, 'R', 256)
T.turn(bopi, 300, 30)
gesture(bopi, 'hops', 470)
T.turn(bopi, 556, 35)
T.arm(bopi, 'R', 700, 0, None)
T.arm(bopi, 'R', 706, fwd=-150, out=25)
T.arm(bopi, 'R', 736, fwd=-150, out=25)
T.rest_arm(bopi, 'R', 746)
gesture(bopi, 'hops', 776)
C.wave(bopi, 'L', 826, cycles=2, period=8)

T.place(ruki, 0, RK0)
T.turn(ruki, 0, -30)
T.arm(ruki, 'L', 108, 0, None)
T.arm(ruki, 'L', 114, fwd=-110, out=45)
T.arm(ruki, 'L', 130, fwd=-110, out=15)
T.arm(ruki, 'L', 146, fwd=-110, out=45)
T.arm(ruki, 'L', 162, fwd=-110, out=15)
T.rest_arm(ruki, 'L', 172)
T.turn(ruki, 300, -20)
for side in ('L', 'R'):
    T.arm(ruki, side, 412, 0, None)
    T.arm(ruki, side, 418, fwd=-150, out=25)
    T.arm(ruki, side, 452, fwd=-150, out=25)
    T.rest_arm(ruki, side, 462)
gesture(ruki, 'hops', 420)
gesture(ruki, 'breathe', 556)
T.arm(ruki, 'L', 556, 0, None)
T.arm(ruki, 'L', 562, fwd=-90, out=50)
T.arm(ruki, 'L', 640, fwd=-90, out=50)
T.rest_arm(ruki, 'L', 650)
T.turn(ruki, 700, -35)
C.wave(ruki, 'R', 820, cycles=2, period=8)
confetti(778, (SX, SY - 0.3, TOPZ + 0.3), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(bopi, (44, 150, 300, 460, 590, 700, 840))
T.blinks(ruki, (70, 190, 330, 500, 650, 790))
