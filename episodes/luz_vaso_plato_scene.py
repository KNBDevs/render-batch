from stage import *
from episodes.luz_vaso_plato_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'luz_vaso_plato'
Z0 = 0.08
auto_dress(EID, ENV)
VIO = (0.62, 0.42, 1.0)
for l in list(bpy.data.lights):
    e = l.energy * 0.36
    for f, c, k in ((0, VIO, 0.55), (58, VIO, 0.55), (74, (0.82, 0.86, 1.0), 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
for f, c, s in ((0, (0.22, 0.12, 0.42, 1), 0.12), (58, (0.22, 0.12, 0.42, 1), 0.12), (74, tuple(bg[0].default_value), 0.2)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)
    bg[1].default_value = s
    bg[1].keyframe_insert('default_value', frame=f)
bpy.data.materials['Sky'].node_tree.nodes['Emission'].inputs[1].default_value = 0.3

TX, TY = 0.0, -1.45
spawn('low_table', 0, 6101, 'pastel', (TX, TY, Z0), 1.0, 0)
TOP = Z0 + 0.62
BZ = TOP + 0.225
HX = 0.0
TP = Vector((-0.6, TY, BZ))

blk = C.empty('torch_block', None, (TP.x - 0.02, TY, TOP))
C.rounded_box('tb', (0, 0, 0.085), (0.22, 0.16, 0.17), 0.3, M((0.98, 0.72, 0.42), rough=0.4, coat=0.6), blk)
torch = spawn('toy_torch', 0, 6102, 'fresh', tuple(TP), 1.1, 0)
bpy.ops.object.light_add(type='SPOT', location=(0.09, 0, 0))
tl = bpy.context.object
tl.parent = torch
tl.rotation_euler = (0, -math.pi / 2, 0)
tl.data.color = (1.0, 0.92, 0.68)
tl.data.spot_size = math.radians(20)
tl.data.spot_blend = 0.6
tl.data.shadow_soft_size = 0.02

beam_m = MA((1.0, 0.94, 0.62), 0.2, emit=1.0)
spot_m = M((1.0, 0.95, 0.7), rough=0.3, emit=3.0)
CONST = []


def disc(name, loc, n, r, m, parent=None):
    q = Vector((0, 0, 1)).rotation_difference(n.normalized())
    o = C.empty(name, parent, tuple(loc), tuple(q.to_euler()))
    C.sphere('d', (0, 0, 0), (r, r, 0.004), m, o, 24)
    CONST.append(o)
    return o


SN = Vector((-1.0, -0.75, 0.0)).normalized()
SCC = Vector((0.55, TY + 0.06, TOP + 0.27))
scr = C.empty('light_screen', None, (SCC.x, SCC.y, TOP), tuple(Vector((0, -1, 0)).rotation_difference(SN).to_euler()))
FR = M((0.55, 0.78, 1.0), rough=0.4, coat=0.7)
C.rounded_box('board', (0, 0.012, 0.27), (0.44, 0.024, 0.46), 0.1, M((0.99, 0.97, 0.92), rough=0.7, coat=0.1), scr)
for z in (0.04, 0.5):
    C.tube('fr', [(-0.23, -0.004, z), (0.23, -0.004, z)], 0.02, FR, scr)
for x in (-0.23, 0.23):
    C.tube('fr', [(x, -0.004, 0.04), (x, -0.004, 0.5)], 0.02, FR, scr)
    C.sphere('ft', (x, 0.0, 0.015), (0.06, 0.09, 0.02), FR, scr, 16)
for k, x in enumerate((-0.15, -0.05, 0.05, 0.15)):
    C.sphere('stud', (x, -0.022, 0.5), (0.022, 0.012, 0.022), M([(1.0, 0.55, 0.6), (1.0, 0.85, 0.35)][k % 2], rough=0.35, coat=0.7), scr, 12)
HIT = Vector((SCC.x, SCC.y, BZ)) + SN * 0.03
spot_scr = disc('spot_scr', HIT, SN, 0.11, spot_m)
halo = C.empty('halo', None, tuple(HIT + SN * 0.03))
C.sphere('h', (0, 0, 0), (0.17, 0.17, 0.17), MA((1.0, 0.92, 0.6), 0.1, emit=0.8), halo, 20)
CONST.append(halo)

cup = spawn('clear_cup', 1, 6103, 'candy', (HX, TY, TOP), 1.6, 0)
CUP_OFF = (HX + 0.3, TY - 0.22, TOP)
cglow = C.empty('cglow', None, (HX, TY, BZ))
C.sphere('g', (0, 0, 0), (0.12, 0.12, 0.16), MA((1.0, 0.95, 0.7), 0.12, emit=0.6), cglow, 20)
CONST.append(cglow)

plate = C.empty('dot_plate', None, (HX, TY, TOP))
plate.scale = (1.25, 1.25, 1.25)
PM = M((0.99, 0.96, 0.9), rough=0.3, coat=0.8)
pax = C.empty('pax', plate, (0, 0, 0.18), (0, math.radians(90), 0))
C.lathe('plate', [(0.0, 0.0), (0.0, 0.1), (0.012, 0.15), (0.032, 0.172), (0.04, 0.17), (0.024, 0.145), (0.01, 0.1), (0.01, 0.0)], PM, pax, segs=64)
DOTS = [(1.0, 0.42, 0.5), (0.4, 0.75, 1.0), (1.0, 0.82, 0.3), (0.5, 0.85, 0.5)]
for k in range(12):
    a = k * 6.2832 / 12
    C.sphere('dot', (-0.006, math.cos(a) * 0.158, 0.18 + math.sin(a) * 0.158), (0.008, 0.014, 0.014), M(DOTS[k % 4], rough=0.3, coat=0.8), plate, 12)
CRM = M((0.98, 0.6, 0.45), rough=0.4, coat=0.6)
C.rounded_box('cradle', (0, 0, 0.02), (0.12, 0.2, 0.04), 0.4, CRM, plate)
for y in (-0.07, 0.07):
    C.sphere('peg', (0.035, y, 0.05), (0.02, 0.02, 0.03), CRM, plate, 12)
spot_pl = disc('spot_pl', (-0.016, 0, 0.18), Vector((-1, 0, 0)), 0.07, spot_m, plate)

P_HOLD = Vector((HX, TY, TOP))
P_BACK = Vector((HX + 0.22, TY + 0.2, TOP))
P_BLOCK = Vector((HX - 0.3, TY, TOP))
TA = TP + Vector((0.1, 0, 0))
beam = C.empty('beam', None, tuple(TA), (0, math.radians(90), 0))
C.lathe('cone', [(0.0, 0.0), (0.0, 0.03), (1.0, 0.09), (1.0, 0.0)], beam_m, beam, segs=32)
CONST.append(beam)


def state(f, s):
    if s == 'off':
        K(beam, 'scale', f, (0, 0, 0))
        tl.data.energy = 0
    else:
        end = {'hold': P_HOLD.x - 0.02, 'block': P_BLOCK.x - 0.02, 'glass': HIT.x}[s]
        sx = 1.25 if s == 'glass' else 1.0
        K(beam, 'scale', f, (sx, 1, end - TA.x))
        tl.data.energy = 38
    tl.data.keyframe_insert('energy', frame=f)
    on_scr = 1.0 if s == 'glass' else 0.0
    on_pl = 1.0 if s in ('hold', 'block') else 0.0
    for o, v in ((spot_scr, on_scr), (halo, on_scr), (cglow, on_scr), (spot_pl, on_pl)):
        K(o, 'scale', f, (v, v, v))


def slide(f0, f1, a, b):
    K(plate, 'location', f0, tuple(a))
    K(plate, 'location', f1, tuple(b))


K(cup, 'location', 0, CUP_OFF)
K(cup, 'scale', 0, (0, 0, 0))
K(cup, 'scale', 110, (0, 0, 0))
K(cup, 'scale', 118, (1.6, 1.6, 1.6))
K(cup, 'location', 170, CUP_OFF)
K(cup, 'location', 190, tuple(P_HOLD))
state(0, 'hold')
state(170, 'off')
slide(0, 170, P_HOLD, P_HOLD)
slide(172, 186, P_HOLD, P_BACK)
state(400, 'glass')
slide(462, 474, P_BACK, P_BLOCK)
state(474, 'block')
slide(552, 562, P_BLOCK, P_BACK)
state(562, 'glass')
slide(620, 632, P_BACK, P_BLOCK)
state(632, 'block')
slide(690, 702, P_BLOCK, P_BACK)
state(702, 'glass')
slide(744, 756, P_BACK, P_BLOCK)
state(756, 'block')
slide(790, 800, P_BLOCK, P_BACK)
state(800, 'glass')
for o in CONST + [tl.data]:
    set_interp(o, 'CONSTANT')
for f, yaw in ((800, 0), (808, 4), (816, -4), (824, 4), (832, -4), (840, 0)):
    K(torch, 'rotation_euler', f, (0, 0, math.radians(yaw)))
    K(spot_scr, 'location', f, tuple(HIT + SN.cross(Vector((0, 0, 1))) * (yaw * 0.012)))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, RC = (0.05, 0.42, 0.15), (0.75, 0.08, 0.15)
label('¿VASO?', GC, (-0.42, TY - 0.55, Z0 + 1.55), 0.78, 276, 396)
label('¿PLATO?', RC, (0.42, TY - 0.55, Z0 + 1.55), 0.86, 282, 396)
label('¡PASA!', GC, (0.3, TY - 0.45, TOP + 0.62), 0.74, 566, 618, 0.24, 0.17)
label('NO PASA', RC, (-0.28, TY - 0.45, TOP + 0.62), 0.9, 634, 690, 0.24, 0.17)

OP = ((-0.45, -2.75, 1.48), (-0.4, TY, 1.06), 24)
OP2 = ((-0.4, -2.85, 1.5), (-0.35, TY, 1.08), 24)
W = ((0.18, -4.0, 1.55), (0.18, -1.25, 1.0), 21)
WQ = ((0.18, -4.2, 1.75), (0.18, -1.25, 1.05), 21)
CB = ((0.18, -3.3, 1.2), (0.18, TY, 0.98), 19.5)
CL = ((0.18, -3.8, 1.38), (0.18, TY, 1.0), 21)
WE = ((0.18, -4.05, 1.6), (0.18, -1.25, 1.02), 21)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 240, W), (242, 396, WQ), (398, 552, CB), (554, 692, CL), (694, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

ruki = make('ruki', 1.35)
luma = make('luma', 1.3)
RK = Vector((-0.64, -0.8, Z0))
LM = Vector((0.95, -1.12, Z0))
T.place(ruki, 0, RK)
T.turn(ruki, 0, 18)
T.place(luma, 0, LM)
T.turn(luma, 0, -35)
for f0, f1 in ((396, 404), (778, 786)):
    T.arm(ruki, 'R', f0 - 6, 0, None)
    T.arm(ruki, 'R', f0, fwd=-80, out=35)
    T.arm(ruki, 'R', f1 + 6, fwd=-80, out=35)
    T.rest_arm(ruki, 'R', f1 + 14)
T.arm(ruki, 'L', 14, fwd=-60, out=55)
T.arm(ruki, 'L', 60, fwd=-60, out=55)
T.rest_arm(ruki, 'L', 70)
for f0 in (100, 176, 456, 540, 608, 684, 738, 782):
    T.arm(luma, 'R', f0, 0, None)
    T.arm(luma, 'R', f0 + 6, fwd=-95, out=35)
    T.arm(luma, 'R', f0 + 18, fwd=-95, out=35)
    T.rest_arm(luma, 'R', f0 + 26)
gesture(luma, 'hops', 412)
gesture(ruki, 'breathe', 476)
gesture(luma, 'breathe', 560)
gesture(ruki, 'hops', 794)
gesture(luma, 'hops', 796)
C.wave(ruki, 'L', 826, cycles=2, period=8)
C.wave(luma, 'L', 826, cycles=2, period=8)
confetti(806, (0.1, TY, Z0 + 2.0), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(ruki, (44, 150, 300, 460, 590, 700, 840))
T.blinks(luma, (70, 190, 330, 500, 650, 790))
