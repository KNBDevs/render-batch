from stage import *
from episodes.rima_gato_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'rima_gato'
Z0 = 0.08
auto_dress(EID, ENV)
TB = Vector((0.0, -1.35, Z0))
tbl = spawn('low_table', 2, 3501, (0.55, 0.75, 0.95), tuple(TB), 1.0, 0)
tbl.scale = (1.3, 1.2, 1.0)
TOP = Z0 + 0.62
CS = 2.0

D0, D1 = 60, 96
for l in list(bpy.data.lights):
    e = l.energy
    for f, k in ((0, 0.12), (D0, 0.12), (D1, 1.0)):
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bgs = sc.world.node_tree.nodes['Background'].inputs[1]
for f, v in ((0, 0.12), (D0, 0.12), (D1, 0.5)):
    bgs.default_value = v
    bgs.keyframe_insert('default_value', frame=f)
skys = bpy.data.materials['Sky'].node_tree.nodes['Emission'].inputs[1]
for f, v in ((0, 0.3), (D0, 0.3), (D1, 1.0)):
    skys.default_value = v
    skys.keyframe_insert('default_value', frame=f)
bpy.ops.object.light_add(type='SPOT', location=(0.0, -2.6, 3.4))
sp = bpy.context.object
sp.data.color = (1.0, 0.55, 0.85)
sp.data.spot_size = math.radians(38)
sp.data.spot_blend = 0.6
sp.data.shadow_soft_size = 0.3
tt = C.empty('sptgt', None, (0, -1.4, TOP))
cs = sp.constraints.new('TRACK_TO')
cs.target = tt
for f, v in ((0, 1600), (D0, 1600), (D1, 0)):
    sp.data.energy = v
    sp.data.keyframe_insert('energy', frame=f)

stand = spawn('pair_stand', 0, 3510, (1.0, 0.5, 0.65), (0.0, TB.y + 0.02, TOP), 1.5, 0)
sA = next(o for o in stand.children_recursive if o.name.startswith('slotA'))
sB = next(o for o in stand.children_recursive if o.name.startswith('slotB'))
link = next(o for o in stand.children_recursive if o.name.startswith('link'))
cat = spawn('symbol_tile', 2, 3520, (1.0, 0.55, 0.3), (0, 0, 0), CS, 0, sA, icon='gato')
mesa = spawn('symbol_tile', 0, 3530, (0.7, 0.55, 0.4), (0, 0, 0), CS, 0, sB, icon='mesa')
zap = spawn('symbol_tile', 2, 3540, (0.3, 0.5, 1.0), (0, 0, 0), CS, 0, sB, icon='zapato')
pato = spawn('symbol_tile', 2, 3550, (0.35, 0.75, 0.95), (0, 0, 0), CS, 0, sB, icon='pato')

for t in range(0, 17, 2):
    u = t / 16
    e = 1 - (1 - u) ** 3
    K(mesa, 'location', 18 + t, (0.9 * (1 - e), -0.3 * (1 - e), 0.5 * (1 - e) + 0.15 * math.sin(math.pi * u)))
K(mesa, 'scale', 0, (0, 0, 0))
K(mesa, 'scale', 17, (0, 0, 0))
K(mesa, 'scale', 20, (CS,) * 3)
for f, a in ((34, 0), (37, -8), (40, 6), (43, 0)):
    K(mesa, 'rotation_euler', f, (0, math.radians(a), 0))
T.pop_out(mesa, 250, CS)
T.pop_in(zap, 286, CS)
T.pop_out(zap, 356, CS)
T.pop_in(pato, 368, CS)


def glow(f0, f1):
    K(link, 'scale', f0 - 1, (0, 0, 0))
    K(link, 'scale', f0 + 5, (1.25, 1.25, 1.25))
    K(link, 'scale', f0 + 10, (1, 1, 1))
    if f1:
        K(link, 'scale', f1, (1, 1, 1))
        K(link, 'scale', f1 + 6, (0, 0, 0))


K(link, 'scale', 0, (0, 0, 0))
glow(312, 352)
glow(392, None)
for k, f in enumerate(range(470, 530, 12)):
    K(link, 'scale', f, (1.15,) * 3 if k % 2 == 0 else (1,) * 3)

MP = Vector((-1.03, -1.22, Z0))
LP = Vector((1.1, -1.3, Z0))
moki = make('moki', 1.6)
luma = make('luma', 1.6)
T.place(moki, 0, MP)
T.turn(moki, 0, 25)
T.place(luma, 0, LP)
T.turn(luma, 0, -25)

C0 = ((-0.39, -3.2, 1.2), (-0.39, -1.4, 1.1), 42)
W1 = ((-0.12, -7.6, 2.1), (-0.1, -1.1, 1.2), 30)
WT = ((0.12, -5.5, 1.65), (0.12, -1.3, 1.2), 30)
WE = ((-0.12, -7.1, 2.05), (-0.1, -1.1, 1.2), 30)
camkey(0, C0)
camkey(14, C0)
camkey(40, ((0.0, -4.0, 1.25), (0.0, -1.4, 1.1), 30))
camkey(84, ((0.0, -4.2, 1.3), (0.0, -1.4, 1.1), 29))
camkey(104, W1)
camkey(440, W1)
camkey(456, WT)
camkey(536, WT)
camkey(552, W1)
camkey(640, W1)
camkey(656, WE)
camkey(TOTAL - 1, ((-0.12, -6.9, 2.0), (-0.1, -1.15, 1.2), 30))

for sd in ('L', 'R'):
    T.arm(moki, sd, 0, 0, None)
    T.arm(moki, sd, 36, fwd=-40, out=70)
    T.arm(moki, sd, 84, fwd=-40, out=70)
    T.rest_arm(moki, sd, 96)
gesture(moki, 'bounce', 44)

WA = (-0.42, -1.55, 1.68)
WB = (0.42, -1.55, 1.68)
T.turn(luma, 108, -35)
T.arm(luma, 'R', 112, 0, None)
T.arm(luma, 'R', 120, fwd=-20, out=95)
T.rest_arm(luma, 'R', 200)
word3d('gato', (0.95, 0.45, 0.1), WA, 150, None, size=0.32)
word3d('mesa', (0.55, 0.35, 0.8), WB, 172, 250, size=0.32)

T.turn(moki, 206, 10)
for k, f in enumerate(range(214, 250, 6)):
    K(moki['spin'], 'rotation_euler', f, (0, math.radians(7 if k % 2 else -7), math.radians(10)))
K(moki['spin'], 'rotation_euler', 252, (0, 0, math.radians(15)))
T.arm(moki, 'R', 210, 0, None)
T.arm(moki, 'R', 218, fwd=-80, out=30)
T.rest_arm(moki, 'R', 256)

T.turn(luma, 280, -20)
gesture(luma, 'breathe', 282)
word3d('zapato', (0.95, 0.45, 0.1), WB, 298, 356, size=0.32)
word3d('pato', (0.95, 0.45, 0.1), WB, 384, 640, size=0.32)
gesture(luma, 'sway', 386)

T.arm(luma, 'L', 452, 0, None)
T.arm(luma, 'L', 460, fwd=-50, out=70)
T.arm(luma, 'R', 452, 0, None)
T.arm(luma, 'R', 460, fwd=-50, out=70)
T.rest_arm(luma, 'L', 524)
T.rest_arm(luma, 'R', 524)
gesture(moki, 'breathe', 470)

T.turn(moki, 556, 20)
gesture(moki, 'hops', 566)
confetti(604, (0.0, -1.5, 2.3), n=22, spread=2.0)
gesture(luma, 'bounce', 600)

shoe = C.empty('moki_shoe', None, (0, 0, 0))
um = M((0.18, 0.45, 0.95), rough=0.4, coat=0.6)
dm = M((0.98, 0.96, 0.9), rough=0.5, coat=0.3)
C.rounded_box('sole', (0, 0, 0.02), (0.3, 0.13, 0.04), 0.5, dm, shoe)
C.sphere('toe', (-0.08, 0, 0.06), (0.08, 0.065, 0.05), um, shoe, 32)
C.rounded_box('body', (0.02, 0, 0.07), (0.22, 0.12, 0.08), 0.5, um, shoe)
C.rounded_box('heel', (0.09, 0, 0.11), (0.1, 0.12, 0.13), 0.5, um, shoe)
C.tube('collar', [(0.05, -0.06, 0.17), (0.09, 0.0, 0.18), (0.05, 0.06, 0.17)], 0.012, dm, shoe)
for k in range(3):
    x = -0.06 + k * 0.04
    C.tube('lace', [(x, -0.045, 0.1 + k * 0.02), (x + 0.012, 0.045, 0.1 + k * 0.02)], 0.009, dm, shoe)
shoe.rotation_euler = (0, 0, math.radians(-20))
SH0 = MP + Vector((0.15, -0.5, 0.0))
SH1 = Vector((-0.4, TB.y - 0.3, TOP))
K(shoe, 'scale', 0, (0, 0, 0))
K(shoe, 'scale', 641, (0, 0, 0))
K(shoe, 'scale', 648, (1.6,) * 3)
K(shoe, 'scale', 652, (1.4,) * 3)
K(shoe, 'location', 641, tuple(SH0))
for t in range(0, 17, 2):
    u = t / 16
    p = SH0.lerp(SH1, u)
    p.z += 0.45 * 4 * u * (1 - u)
    K(shoe, 'location', 652 + t, tuple(p))
T.turn(moki, 640, 35)
T.arm(moki, 'R', 640, 0, None)
T.arm(moki, 'R', 650, fwd=-60, out=40)
T.arm(moki, 'R', 668, fwd=-55, out=60)
T.rest_arm(moki, 'R', 690)

K(pato, 'location', 676, (0, 0, 0))
K(pato, 'rotation_euler', 676, (0, 0, 0))
K(pato, 'location', 688, (-0.06, -0.08, 0.1))
K(pato, 'rotation_euler', 688, (0, math.radians(-10), math.radians(-22)))
K(pato, 'location', 724, (-0.06, -0.08, 0.1))
K(pato, 'rotation_euler', 724, (0, math.radians(-10), math.radians(-22)))
K(pato, 'location', 736, (0, 0, 0))
K(pato, 'rotation_euler', 736, (0, 0, 0))
T.arm(moki, 'L', 676, 0, None)
T.arm(moki, 'L', 684, fwd=-55, out=50)
T.rest_arm(moki, 'L', 730)
gesture(luma, 'breathe', 700)
T.turn(moki, 744, 25)
gesture(moki, 'breathe', 750)

T.lines(EID, LINES)
T.blinks(moki, (60, 150, 280, 400, 500, 620, 740))
T.blinks(luma, (40, 130, 250, 360, 470, 590, 700, 770))
