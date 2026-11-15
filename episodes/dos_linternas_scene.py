from stage import *
from episodes.dos_linternas_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'dos_linternas'
Z0 = 0.08
auto_dress(EID, ENV)
DUSK = (1.0, 0.5, 0.32)
for l in list(bpy.data.lights):
    e = l.energy * 0.5
    for f, c, k in ((0, DUSK, 0.45), (64, DUSK, 0.45), (80, (0.9, 0.9, 1.0), 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
for f, c, s in ((0, (0.2, 0.06, 0.22, 1), 0.12), (64, (0.2, 0.06, 0.22, 1), 0.12), (80, tuple(bg[0].default_value), 0.2)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)
    bg[1].default_value = s
    bg[1].keyframe_insert('default_value', frame=f)
bpy.data.materials['Sky'].node_tree.nodes['Emission'].inputs[1].default_value = 0.3

TY = -1.45
spawn('low_table', 0, 7101, 'pastel', (0, TY, Z0), 1.0, 0)
TOP = Z0 + 0.62
CREAM = M((1.0, 0.96, 0.9), rough=0.35, coat=0.7)
CORAL = M((1.0, 0.5, 0.45), rough=0.35, coat=0.7)
MINT = M((0.45, 0.85, 0.7), rough=0.4, coat=0.6)
GOLD = M((1.0, 0.8, 0.3), rough=0.3, coat=0.8)
WIN = M((0.35, 0.65, 1.0), rough=0.1, coat=1.0, emit=0.6)

RP = Vector((0.0, TY + 0.1, TOP))
rk = C.empty('toy_rocket', None, tuple(RP))
C.lathe('body', [(0, 0.0), (0, 0.06), (0.02, 0.075), (0.3, 0.08), (0.34, 0.076), (0.34, 0.0)], CREAM, rk, segs=56)
C.lathe('nose', [(0.34, 0.0), (0.34, 0.077), (0.42, 0.06), (0.5, 0.028), (0.53, 0.0)], CORAL, rk, segs=56)
C.tube('band', [(math.cos(k * 6.2832 / 48) * 0.08, math.sin(k * 6.2832 / 48) * 0.08, 0.1) for k in range(49)], 0.01, GOLD, rk)
for k in range(3):
    fe = C.empty('fin', rk, (0, 0, 0), (0, 0, math.radians(90 + k * 120)))
    C.rounded_box('f', (0.1, 0, 0.08), (0.08, 0.024, 0.16), 0.4, MINT, fe)
C.sphere('win', (0, -0.074, 0.22), (0.036, 0.014, 0.036), WIN, rk, 24)
C.tube('wring', [(math.cos(k * 6.2832 / 40) * 0.04, -0.077, 0.22 + math.sin(k * 6.2832 / 40) * 0.04) for k in range(41)], 0.008, GOLD, rk)
rk.scale = (1.15, 1.15, 1.15)

SY = TY + 0.62
SB = Z0 + 0.42
scr = C.empty('wall_screen', None, (0, SY, SB))
FR = M((1.0, 0.62, 0.45), rough=0.4, coat=0.7)
BW, BH = 1.9, 1.4
C.rounded_box('board', (0, 0.014, BH / 2), (BW, 0.026, BH), 0.04, M((0.99, 0.97, 0.93), rough=0.7, coat=0.1), scr)
for z in (0.0, BH):
    C.tube('fr', [(-BW / 2, -0.004, z), (BW / 2, -0.004, z)], 0.026, FR, scr)
for x in (-BW / 2, BW / 2):
    C.tube('fr', [(x, -0.004, 0.0), (x, -0.004, BH)], 0.026, FR, scr)
    C.tube('post', [(x * 0.92, 0.02, -SB + Z0), (x * 0.92, 0.02, 0.0)], 0.03, MINT, scr)
    C.sphere('ft', (x * 0.92, 0.02, -SB + Z0 + 0.02), (0.08, 0.12, 0.025), MINT, scr, 16)
for k in range(9):
    x = -0.8 + k * 0.2
    C.sphere('stud', (x, -0.026, BH), (0.024, 0.012, 0.024), M([(0.55, 0.8, 0.98), (1.0, 0.85, 0.35)][k % 2], rough=0.35, coat=0.7), scr, 12)

CONST = []
DARK = M((0.01, 0.008, 0.02), rough=1.0, coat=0.0)
LIT = M((1.0, 0.93, 0.66), rough=0.3, emit=2.0)
SX = 0.43


def silhouette(x, parent=scr, z=0.22, y=-0.018, k=1.45):
    s = C.empty('shadow', parent, (x, y, z))
    C.rounded_box('b', (0, 0, 0.21), (0.18, 0.006, 0.38), 0.3, DARK, s)
    C.sphere('n', (0, 0, 0.44), (0.09, 0.004, 0.14), DARK, s, 24)
    for sx in (-1, 1):
        C.rounded_box('f', (sx * 0.12, 0, 0.09), (0.08, 0.006, 0.17), 0.35, DARK, s)
    s.scale = (k, 1.0, k)
    return s


def patch(x):
    p = C.empty('lit', scr, (x, -0.008, 0.66))
    C.sphere('p', (0, 0, 0), (0.42, 0.004, 0.5), LIT, p, 40)
    return p


sh_r, sh_l = silhouette(SX), silhouette(-SX)
pa_r, pa_l = patch(SX), patch(-SX)
CONST += [sh_r, sh_l, pa_r, pa_l]

beam_m = MA((1.0, 0.92, 0.6), 0.14, emit=1.0)
TL = Vector((-0.46, TY - 0.17, TOP + 0.11))
TR = Vector((0.46, TY - 0.17, TOP + 0.11))
for p in (TL, TR):
    b = C.empty('torch_block', None, (p.x, p.y, TOP))
    C.rounded_box('tb', (0, 0, 0.035), (0.2, 0.16, 0.07), 0.3, M((0.55, 0.8, 0.98), rough=0.4, coat=0.6), b)


def aim(src, dst):
    d = dst - src
    return math.degrees(math.atan2(d.y, d.x)), d


HIT_R = Vector((SX, SY - 0.02, SB + 0.62))
HIT_L = Vector((-SX, SY - 0.02, SB + 0.62))
a_l, d_l = aim(TL, HIT_R)
a_r, d_r = aim(TR, HIT_L)
torch_l = spawn('toy_torch', 0, 7102, 'candy', tuple(TL), 1.5, a_l)
torch_r = spawn('toy_torch', 0, 7103, 'pastel', tuple(TR), 1.5, a_r)


def beam(src, d):
    e = C.empty('beam', None, tuple(src + d.normalized() * 0.15), Vector((0, 0, 1)).rotation_difference(d.normalized()).to_euler())
    C.lathe('cone', [(0.0, 0.0), (0.0, 0.03), (1.0, 0.1), (1.0, 0.0)], beam_m, e, segs=32)
    return e, (RP + Vector((0, 0, 0.3)) - src).length - 0.15


bm_l, len_l = beam(TL, d_l)
bm_r, len_r = beam(TR, d_r)
CONST += [bm_l, bm_r]


def light(f, left, right):
    for on, bm_, ln, sh, pa in ((left, bm_l, len_l, sh_r, pa_r), (right, bm_r, len_r, sh_l, pa_l)):
        v = 1.0 if on else 0.0
        K(bm_, 'scale', f, (2.6 * v, 2.6 * v, ln * v + 0.001))
        K(pa, 'scale', f, (v,) * 3)
        K(sh, 'scale', f, (1.45 * v, 1.0 * v, 1.45 * v))


light(0, True, False)
light(380, True, True)
light(500, False, True)
light(548, True, True)
light(586, False, False)
light(772, True, True)
light(788, True, False)
light(826, True, True)
for o in CONST:
    set_interp(o, 'CONSTANT')
K(torch_r, 'scale', 0, (0, 0, 0))
T.pop_in(torch_r, 118, 1.5, 8)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


KC, OC, GC = (0.08, 0.06, 0.16), (0.85, 0.35, 0.05), (0.05, 0.42, 0.15)
LZ = SB + BH + 0.2
label('¿UNA?', KC, (-0.45, SY - 0.2, LZ), 0.8, 190, 372, 0.3, 0.22)
label('¿DOS?', OC, (0.45, SY - 0.2, LZ), 0.8, 198, 372, 0.3, 0.22)
label('¡DOS!', GC, (0.0, SY - 0.2, LZ), 0.8, 396, 482, 0.3, 0.22)
label('UNA', KC, (0.0, SY - 0.2, LZ), 0.7, 506, 544, 0.3, 0.22)
label('¡DOS!', GC, (0.0, SY - 0.2, LZ), 0.8, 552, 584, 0.3, 0.22)

exp = C.empty('diagram', None, (0.0, -2.1, 1.12))
C.rounded_box('panel', (0, 0.04, 0.4), (1.24, 0.03, 0.86), 0.4, M((0.92, 0.9, 1.0), rough=0.5, coat=0.3), exp)
YEL = M((1.0, 0.8, 0.15), rough=0.3, coat=0.6, emit=0.6)
PANW = M((0.99, 0.97, 0.93), rough=0.6, coat=0.2)
C.rounded_box('wall', (0, 0.0, 0.62), (1.0, 0.02, 0.34), 0.2, PANW, exp)
for sx in (-1, 1):
    C.rounded_box('lamp', (sx * 0.44, -0.03, 0.14), (0.14, 0.03, 0.08), 0.4, YEL, exp)
    a, b = Vector((sx * 0.4, -0.04, 0.18)), Vector((-sx * 0.3, -0.04, 0.5))
    C.tube('ray', [tuple(a), tuple(b)], 0.014, YEL, exp)
    silhouette(-sx * 0.3, exp, 0.47, -0.02, 0.36)
C.rounded_box('icon', (0, -0.05, 0.36), (0.06, 0.02, 0.14), 0.4, M((1.0, 0.5, 0.45), rough=0.3, coat=0.6), exp)
C.sphere('icon_n', (0, -0.05, 0.45), (0.03, 0.02, 0.045), M((1.0, 0.5, 0.45), rough=0.3, coat=0.6), exp, 16)
T.pop_in(exp, 590, 1.2, 10)
T.pop_out(exp, 768, 1.2, 6)
label('CADA LUZ', OC, (0.0, -2.2, 1.98), 0.76, 600, 768, 0.17, 0.1)
label('¡SU SOMBRA!', KC, (0.0, -2.25, 0.93), 0.9, 640, 768, 0.2, 0.12)
label('1 LUZ', OC, (-0.45, SY - 0.2, LZ), 0.7, 792, 824, 0.27, 0.18)
label('2 LUCES', GC, (0.0, SY - 0.2, LZ), 0.98, 830, TOTAL + 10, 0.3, 0.2)
confetti(856, (0.0, TY, Z0 + 2.0), n=24, spread=1.2)

OP = ((0.28, -3.0, 1.32), (0.26, SY, 1.05), 22)
W = ((0.0, -4.8, 1.62), (0.0, -1.2, 1.08), 18)
WQ = ((0.0, -4.95, 1.8), (0.0, -1.2, 1.2), 18)
CU = ((0.0, -4.75, 1.62), (0.0, SY, 1.12), 18)
EXP = ((0.0, -4.75, 1.75), (0.0, -1.85, 1.48), 28)
camkey(0, OP)
camkey(56, OP)
for a, b, pose in ((70, 186, W), (188, 376, WQ), (378, 584, CU), (588, 770, EXP), (772, TOTAL - 1, W)):
    camkey(a, pose)
    camkey(b, pose)

bolita = make('bolita', 1.15)
moki = make('moki', 1.15)
BP, MP = Vector((-1.04, -1.4, Z0)), Vector((1.04, -1.4, Z0))
T.turn(bolita, 0, 25)
T.turn(moki, 0, -25)
for ch, p0, dx in ((bolita, BP, -0.6), (moki, MP, 0.6)):
    T.place(ch, 0, p0 + Vector((dx, 0, 0)))
    T.place(ch, 66, p0 + Vector((dx, 0, 0)))
    T.place(ch, 68, p0)
    T.place(ch, 586, p0)
    T.place(ch, 588, p0 + Vector((dx * 1.8, 0, 0)))
    T.place(ch, 770, p0 + Vector((dx * 1.8, 0, 0)))
    T.place(ch, 772, p0)

T.arm(bolita, 'L', 4, 0, None)
T.arm(bolita, 'L', 12, fwd=-75, out=20)
T.arm(bolita, 'L', 34, fwd=-75, out=20)
T.rest_arm(bolita, 'L', 44)
T.arm(moki, 'R', 104, 0, None)
T.arm(moki, 'R', 112, fwd=-80, out=25)
T.arm(moki, 'R', 132, fwd=-80, out=25)
T.rest_arm(moki, 'R', 142)
for ch, side, f0 in ((bolita, 'L', 182), (moki, 'R', 372), (bolita, 'L', 492), (bolita, 'L', 540), (bolita, 'L', 782), (bolita, 'L', 820)):
    T.arm(ch, side, f0, 0, None)
    T.arm(ch, side, f0 + 6, fwd=-85, out=30)
    T.arm(ch, side, f0 + 20, fwd=-85, out=30)
    T.rest_arm(ch, side, f0 + 28)
gesture(bolita, 'hops', 72)
gesture(moki, 'hops', 410)
C.wave(bolita, 'R', 862, cycles=2, period=10)
C.wave(moki, 'L', 858, cycles=2, period=10)
gesture(moki, 'hops', 846)

T.lines(EID, LINES)
T.blinks(bolita, (70, 200, 340, 470, 620, 740, 880))
T.blinks(moki, (80, 230, 360, 520, 660, 800))
