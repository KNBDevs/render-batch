from stage import *
from episodes.sombra_color_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'sombra_color'
Z0 = 0.08
auto_dress(EID, ENV)
NAVY = (0.35, 0.45, 1.0)
for l in list(bpy.data.lights):
    e = l.energy * 0.45
    for f, c, k in ((0, NAVY, 0.5), (64, NAVY, 0.5), (80, (0.86, 0.88, 1.0), 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
for f, c, s in ((0, (0.06, 0.1, 0.32, 1), 0.12), (64, (0.06, 0.1, 0.32, 1), 0.12), (80, tuple(bg[0].default_value), 0.2)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)
    bg[1].default_value = s
    bg[1].keyframe_insert('default_value', frame=f)
bpy.data.materials['Sky'].node_tree.nodes['Emission'].inputs[1].default_value = 0.3

TX, TY = 0.0, -1.45
spawn('low_table', 1, 6801, 'pastel', (TX, TY, Z0), 1.0, 0)
TOP = Z0 + 0.62
BZ = TOP + 0.21
TP = Vector((-0.62, TY, BZ))
blk = C.empty('torch_block', None, (TP.x - 0.02, TY, TOP))
C.rounded_box('tb', (0, 0, 0.08), (0.22, 0.16, 0.16), 0.3, M((0.55, 0.8, 0.98), rough=0.4, coat=0.6), blk)
torch = spawn('toy_torch', 1, 6802, 'candy', tuple(TP), 1.1, 0)

CONST = []
SN = Vector((-1.0, -0.75, 0.0)).normalized()
SCC = Vector((0.52, TY + 0.06, TOP))
scr = C.empty('shadow_screen', None, tuple(SCC), tuple(Vector((0, -1, 0)).rotation_difference(SN).to_euler()))
FR = M((1.0, 0.62, 0.45), rough=0.4, coat=0.7)
BW, BH = 0.66, 0.6
C.rounded_box('board', (0, 0.014, 0.03 + BH / 2), (BW, 0.026, BH), 0.08, M((0.99, 0.97, 0.93), rough=0.7, coat=0.1), scr)
for z in (0.03, 0.03 + BH):
    C.tube('fr', [(-BW / 2, -0.004, z), (BW / 2, -0.004, z)], 0.022, FR, scr)
for x in (-BW / 2, BW / 2):
    C.tube('fr', [(x, -0.004, 0.03), (x, -0.004, 0.03 + BH)], 0.022, FR, scr)
    C.sphere('ft', (x, 0.0, 0.015), (0.06, 0.1, 0.02), FR, scr, 16)
for k, x in enumerate((-0.22, -0.11, 0.0, 0.11, 0.22)):
    C.sphere('stud', (x, -0.024, 0.03 + BH), (0.022, 0.012, 0.022), M([(0.55, 0.8, 0.98), (1.0, 0.85, 0.35)][k % 2], rough=0.35, coat=0.7), scr, 12)

SZ = 0.33
patch = C.empty('patch', scr, (0, -0.006, SZ))
C.sphere('p', (0, 0, 0), (0.27, 0.004, 0.25), M((1.0, 0.95, 0.72), rough=0.3, emit=2.2), patch, 32)
CONST.append(patch)
DARK = M((0.005, 0.005, 0.01), rough=1.0, coat=0.0)
REDS = M((1.0, 0.1, 0.14), rough=0.4, emit=1.6)
sh_mug = C.empty('sh_mug', scr, (0, -0.014, SZ - 0.02))
C.rounded_box('b', (-0.02, 0, 0), (0.2, 0.006, 0.26), 0.3, DARK, sh_mug)
C.tube('h', [(0.08 + 0.055 * math.sin(a * math.pi / 8), 0, 0.065 * math.cos(a * math.pi / 8)) for a in range(9)], 0.016, DARK, sh_mug)
CONST.append(sh_mug)
sh_red = C.empty('sh_red', scr, (0, -0.014, SZ - 0.01))
C.rounded_box('b', (0, 0, 0), (0.2, 0.006, 0.3), 0.3, REDS, sh_red)
CONST.append(sh_red)

beam_m = MA((1.0, 0.94, 0.62), 0.16, emit=1.0)
red_m = MA((1.0, 0.15, 0.2), 0.3, emit=1.2)
TA = TP + Vector((0.1, 0, 0))
HITX = (SCC + SN * 0.0).x - 0.08
beam = C.empty('beam', None, tuple(TA), (0, math.radians(90), 0))
C.lathe('cone', [(0.0, 0.0), (0.0, 0.03), (1.0, 0.09), (1.0, 0.0)], beam_m, beam, segs=32)
CONST.append(beam)
rbeam = C.empty('rbeam', None, (0.06, TY, BZ), (0, math.radians(90), 0))
C.lathe('cone', [(0.0, 0.0), (0.0, 0.075), (1.0, 0.11), (1.0, 0.0)], red_m, rbeam, segs=32)
CONST.append(rbeam)

P_HOLD = Vector((0.0, TY, TOP))
MUG_OFF = Vector((-0.3, TY + 0.3, TOP))
CUP_OFF = Vector((0.04, TY + 0.34, TOP))
mug = spawn('mug', 0, 6803, 'candy', tuple(P_HOLD), 1.5, -90)
GLASS = MA((1.0, 0.12, 0.18), 0.5, rough=0.05, emit=0.35)
cup = C.empty('red_cup', None, tuple(CUP_OFF))
R, H = 0.1, 0.28
C.lathe('glass', [(0, 0.0), (0, R * 0.85), (0.02, R * 0.92), (H, R), (H + 0.004, R - 0.004), (H, R - 0.01), (0.03, R * 0.85), (0.03, 0.0)], GLASS, cup, segs=48)
C.tube('rim', [(math.cos(a * math.pi / 24) * (R + 0.003), math.sin(a * math.pi / 24) * (R + 0.003), H - 0.012) for a in range(49)], 0.008, M((1.0, 0.85, 0.35), coat=0.7), cup)
C.tube('foot', [(math.cos(a * math.pi / 24) * R * 0.86, math.sin(a * math.pi / 24) * R * 0.86, 0.01) for a in range(49)], 0.01, M((1.0, 0.85, 0.35), coat=0.7), cup)


def state(f, s):
    on = 0.0 if s == 'off' else 1.0
    K(beam, 'scale', f, (2.7 * on, 2.7 * on, (HITX - TA.x) * on + 0.001))
    K(patch, 'scale', f, (on,) * 3)
    v = 1.0 if s == 'mug' else 0.0
    K(sh_mug, 'scale', f, (v,) * 3)
    v = 1.0 if s == 'red' else 0.0
    K(sh_red, 'scale', f, (v,) * 3)
    K(rbeam, 'scale', f, (v, v, (HITX - 0.06) * v + 0.001))


def move(o, f0, f1, a, b, hop=0.12):
    K(o, 'location', f0, tuple(a))
    m = (a + b) / 2
    K(o, 'location', (f0 + f1) // 2, (m.x, m.y, m.z + hop))
    K(o, 'location', f1, tuple(b))


K(cup, 'scale', 0, (0, 0, 0))
K(cup, 'scale', 110, (0, 0, 0))
K(cup, 'scale', 118, (1.15, 1.15, 1.15))
K(cup, 'scale', 122, (1, 1, 1))
state(0, 'mug')
state(180, 'off')
move(mug, 182, 196, P_HOLD, MUG_OFF)
move(cup, 200, 216, CUP_OFF, P_HOLD)
state(400, 'red')
state(484, 'off')
move(cup, 484, 496, P_HOLD, CUP_OFF)
move(mug, 498, 510, MUG_OFF, P_HOLD)
state(510, 'mug')
state(548, 'off')
move(mug, 548, 560, P_HOLD, MUG_OFF)
move(cup, 562, 574, CUP_OFF, P_HOLD)
state(574, 'red')
state(600, 'off')
move(cup, 600, 612, P_HOLD, CUP_OFF)
move(mug, 736, 746, MUG_OFF, P_HOLD)
state(746, 'mug')
state(820, 'off')
move(mug, 820, 832, P_HOLD, MUG_OFF)
move(cup, 834, 846, CUP_OFF, P_HOLD)
state(846, 'red')
for o, s in ((cup, 1.0), (mug, 1.5)):
    K(o, 'scale', 598, (s, s, s))
    K(o, 'scale', 604, (0, 0, 0))
    K(o, 'scale', 730, (0, 0, 0))
    K(o, 'scale', 736, (s, s, s))
for o in CONST:
    set_interp(o, 'CONSTANT')


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


KC, RC, YC = (0.06, 0.06, 0.1), (0.85, 0.06, 0.12), (0.8, 0.5, 0.0)
label('¿NEGRA?', KC, (-0.42, TY - 0.6, Z0 + 1.6), 0.86, 262, 396)
label('¿ROJA?', RC, (0.42, TY - 0.6, Z0 + 1.6), 0.78, 270, 396)
label('¡ROJA!', RC, (0.3, TY - 0.5, TOP + 0.7), 0.74, 420, 480, 0.24, 0.17)
label('NEGRA', KC, (0.3, TY - 0.5, TOP + 0.7), 0.74, 516, 546, 0.24, 0.17)
label('TAZA', YC, (-0.42, TY - 0.6, Z0 + 1.6), 0.66, 742, TOTAL + 10, 0.24, 0.16)
label('NEGRA', KC, (0.3, TY - 0.5, TOP + 0.7), 0.74, 752, 814, 0.24, 0.17)
label('VASO', RC, (0.42, TY - 0.6, Z0 + 1.6), 0.66, 840, TOTAL + 10, 0.24, 0.16)
label('ROJA', RC, (0.3, TY - 0.5, TOP + 0.7), 0.66, 850, TOTAL + 10, 0.24, 0.17)

exp = C.empty('diagram', None, (0.0, -2.1, 1.12))
C.rounded_box('panel', (0, 0.04, 0.4), (1.2, 0.03, 0.86), 0.4, M((0.9, 0.94, 1.0), rough=0.5, coat=0.3), exp)
C.rounded_box('divider', (0, 0.0, 0.4), (1.08, 0.03, 0.022), 0.4, M((1.0, 1.0, 1.0), rough=0.5, coat=0.3), exp)
YEL = M((1.0, 0.82, 0.2), rough=0.3, coat=0.6, emit=0.6)
RED = M((1.0, 0.12, 0.16), rough=0.3, coat=0.6, emit=0.5)


def arrow(x0, x1, z, m):
    C.tube('shaft', [(x0, -0.03, z), (x1 - 0.05, -0.03, z)], 0.022, m, exp)
    C.lathe('tip', [(0.0, 0.0), (0.0, 0.05), (0.08, 0.0)], m, C.empty('t', exp, (x1 - 0.06, -0.03, z), (0, math.radians(90), 0)), segs=20)


for z, kind in ((0.6, 'red'), (0.18, 'mug')):
    arrow(-0.5, -0.16, z, YEL)
    if kind == 'red':
        ic = C.empty('icup', exp, (-0.06, -0.06, z - 0.1))
        C.lathe('g', [(0, 0.0), (0, 0.06), (0.17, 0.07), (0.17, 0.0)], M((1.0, 0.15, 0.2), rough=0.2, coat=0.8, emit=0.3), ic, segs=32)
        arrow(0.04, 0.36, z, RED)
        C.sphere('dot', (0.46, -0.03, z), (0.08, 0.01, 0.08), RED, exp, 24)
    else:
        spawn('mug', 0, 6803, 'candy', (-0.06, -0.06, z - 0.1), 0.85, -90, parent=exp)
        C.sphere('dot', (0.46, -0.03, z), (0.08, 0.01, 0.08), DARK, exp, 24)
T.pop_in(exp, 590, 1.2, 10)
T.pop_out(exp, 738, 1.2, 6)
label('LUZ', YC, (-0.33, -2.2, 1.96), 0.42, 600, 738, 0.17, 0.1)
label('ROJA', RC, (0.2, -2.2, 1.96), 0.5, 612, 738, 0.17, 0.1)
label('NEGRA', KC, (0.2, -2.2, 1.3), 0.4, 640, 738, 0.15, 0.085)
confetti(880, (0.1, TY, Z0 + 2.0), n=22, spread=1.1)

OP = ((-0.18, -3.35, 1.5), (-0.1, TY, 1.04), 18.5)
W = ((0.05, -4.1, 1.55), (0.05, -1.25, 1.0), 21)
WQ = ((0.05, -4.3, 1.75), (0.05, -1.25, 1.06), 21)
CB = ((0.14, -3.9, 1.35), (0.14, -1.3, 1.0), 18)
EXP = ((0.0, -4.75, 1.75), (0.0, -1.85, 1.48), 28)
WE = ((0.1, -4.2, 1.6), (0.1, -1.25, 1.02), 20.5)
camkey(0, OP)
camkey(40, OP)
for a, b, pose in ((64, 240, W), (242, 396, WQ), (398, 586, CB), (588, 740, EXP), (742, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

pimo = make('pimo', 1.3)
tuki = make('tuki', 1.3)
PP = Vector((-0.98, -0.95, Z0))
TK = Vector((1.12, -0.92, Z0))
T.place(pimo, 0, PP)
T.turn(pimo, 0, 22)
T.place(tuki, 0, TK)
T.turn(tuki, 0, -32)
gesture(pimo, 'hops', 50)
for f0 in (104, 262, 404, 504):
    T.arm(tuki, 'L', f0, 0, None)
    T.arm(tuki, 'L', f0 + 6, fwd=-90, out=35)
    T.arm(tuki, 'L', f0 + 22, fwd=-90, out=35)
    T.rest_arm(tuki, 'L', f0 + 30)
for f0 in (14, 256, 496, 744, 842):
    T.arm(pimo, 'R', f0, 0, None)
    T.arm(pimo, 'R', f0 + 6, fwd=-85, out=30)
    T.arm(pimo, 'R', f0 + 24, fwd=-85, out=30)
    T.rest_arm(pimo, 'R', f0 + 32)
gesture(tuki, 'hops', 412)
gesture(pimo, 'breathe', 520)
gesture(pimo, 'hops', 878)
gesture(tuki, 'hops', 880)
C.wave(pimo, 'L', 900, cycles=2, period=8)
C.wave(tuki, 'R', 900, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(pimo, (44, 150, 300, 460, 590, 700, 860, 920))
T.blinks(tuki, (70, 190, 330, 500, 650, 790, 900))
