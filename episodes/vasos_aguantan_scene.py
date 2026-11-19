from stage import *
from episodes.vasos_aguantan_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'vasos_aguantan'
Z0 = 0.08
auto_dress(EID, ENV)
WARM = (1.0, 0.66, 0.35)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, WARM, 0.75), (64, WARM, 0.75), (80, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (1.0, 0.6, 0.3, 1)), (64, (1.0, 0.6, 0.3, 1)), (80, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

TY = -1.5
CREAM = M((1.0, 0.96, 0.9), rough=0.35, coat=0.7)
CORAL = M((1.0, 0.5, 0.45), rough=0.35, coat=0.7)
MINT = M((0.45, 0.85, 0.7), rough=0.4, coat=0.6)
GOLD = M((1.0, 0.8, 0.3), rough=0.3, coat=0.8)
SKYB = M((0.5, 0.75, 1.0), rough=0.35, coat=0.7)
WOOD = M((0.95, 0.72, 0.45), rough=0.45, coat=0.5)
CUPW = M((1.0, 0.98, 0.95), rough=0.5, coat=0.3)

mat = C.empty('rug', None, (0, TY, Z0))
C.lathe('disc', [(0.0, 0.0), (0.0, 1.3), (0.015, 1.33), (0.03, 1.3), (0.03, 0.0)], MINT, mat, segs=72, sx=1.25, sy=0.8)
C.tube('rim', [(math.cos(k * 6.2832 / 72) * 1.31 * 1.25, math.sin(k * 6.2832 / 72) * 1.31 * 0.8, 0.03) for k in range(73)], 0.022, CREAM, mat)
GZ = Z0 + 0.035
CS = 1.5
H = 0.25 * CS


def cup(loc, band):
    o = C.empty('cup', None, loc)
    C.lathe('c', [(0.0, 0.0), (0.0, 0.105), (0.24, 0.075), (0.25, 0.07), (0.25, 0.0)], CUPW, o, segs=32)
    for z, r in ((0.05, 0.1), (0.17, 0.085)):
        C.tube('b', [(math.cos(k * 6.2832 / 40) * r, math.sin(k * 6.2832 / 40) * r, z) for k in range(41)], 0.012, band, o)
    o.scale = (CS, CS, CS)
    return o


def squash(o, f, d=6, s=CS):
    K(o, 'scale', f, (s, s, s))
    K(o, 'scale', f + d * 0.5, (s * 1.25, s * 1.25, s * 0.5))
    K(o, 'scale', f + d, (s * 1.45, s * 1.45, s * 0.14))


c0 = cup((0, TY, GZ), CORAL)
squash(c0, 18)
T.pop_out(c0, 84, (CS * 1.45, CS * 1.45, CS * 0.14), 6)

cups = []
bands = (CORAL, SKYB, GOLD)
k = 0
for j, y in enumerate((-0.4, -0.13, 0.13, 0.4)):
    for i, x in enumerate((-0.36, 0.0, 0.36)):
        c = cup((x, TY + y, GZ), bands[(i + j) % 3])
        T.pop_in(c, 236 + k * 4, CS, 6)
        cups.append(c)
        k += 1
board = C.empty('board', None, (0, TY, GZ + H))
C.rounded_box('bd', (0, 0, 0.025), (1.2, 1.2, 0.05), 0.2, WOOD, board)
C.rounded_box('edge', (0, -0.6, 0.025), (1.2, 0.02, 0.055), 0.4, CORAL, board)
T.pop_in(board, 296, 1.0, 8)
for f, dz, s in ((372, 0.0, 1.0), (375, -0.02, 0.94), (380, 0.0, 1.0), (384, -0.008, 0.98), (388, 0.0, 1.0)):
    K(board, 'location', f, (0, TY, GZ + H + dz))
    for c in cups:
        K(c, 'scale', f, (CS, CS, CS * s))

C1 = Vector((-0.9, TY - 0.35, GZ))
c1 = cup(tuple(C1), MINT)
T.pop_in(c1, 492, CS, 8)
squash(c1, 530)
T.pop_out(c1, 586, (CS * 1.45, CS * 1.45, CS * 0.14), 6)
blk = C.empty('block', None, tuple(C1 + Vector((0, 0, 1.6))))
C.rounded_box('bk', (0, 0, 0.16), (0.32, 0.32, 0.32), 0.2, CORAL, blk)
C.sphere('dot', (0, -0.165, 0.16), (0.06, 0.01, 0.06), GOLD, blk, 16)
T.pop_in(blk, 504, 1.0, 8)
for f, z in ((514, 1.6), (530, H + 0.0), (536, 0.05 * CS)):
    K(blk, 'location', f, tuple(C1 + Vector((0, 0, z))))
T.pop_out(blk, 586, 1.0, 6)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


KC, OC, GC = (0.08, 0.06, 0.16), (0.85, 0.35, 0.05), (0.05, 0.42, 0.15)
LZ, LY = 2.05, TY - 0.55
label('¿AGUANTAN?', GC, (-0.6, LY, LZ), 1.1, 212, 372, 0.3, 0.16)
label('¿SE APLASTAN?', OC, (0.6, LY, LZ), 1.2, 220, 372, 0.3, 0.14)
label('¡AGUANTAN!', GC, (0.0, LY, LZ), 1.1, 396, 482, 0.3, 0.2)
label('¡PLAF!', OC, (0.0, LY, LZ), 0.9, 552, 584, 0.3, 0.22)

EYP = -2.95
exp = C.empty('diagram', None, (0.0, EYP, 1.1))
C.rounded_box('panel', (0, 0.04, 0.4), (1.3, 0.03, 0.9), 0.4, M((0.5, 0.56, 0.92), rough=0.8, coat=0.0), exp)
RED = M((1.0, 0.4, 0.3), rough=0.3, coat=0.5, emit=0.6)
ARR = M((1.0, 0.85, 0.3), rough=0.3, coat=0.5, emit=0.6)


def arrow(x, z0, z1, r, m):
    C.tube('sh', [(x, -0.05, z0), (x, -0.05, z1 + r * 2)], r, m, exp)
    hd = C.empty('hd', exp, (x, -0.05, z1), (math.pi, 0, 0))
    C.lathe('h', [(0.0, 0.0), (0.0, r * 2.6), (r * 3.2, 0.0)], m, hd, segs=16)


C.rounded_box('fl', (-0.31, -0.03, 0.1), (0.5, 0.02, 0.025), 0.4, WOOD, exp)
C.rounded_box('flat', (-0.31, -0.04, 0.13), (0.16, 0.02, 0.03), 0.4, CUPW, exp)
arrow(-0.31, 0.66, 0.18, 0.03, RED)
C.rounded_box('fr', (0.31, -0.03, 0.1), (0.5, 0.02, 0.025), 0.4, WOOD, exp)
for k in range(4):
    x = 0.31 + (k - 1.5) * 0.11
    C.rounded_box('cp', (x, -0.04, 0.18), (0.07, 0.02, 0.13), 0.3, CUPW, exp)
    arrow(x, 0.5, 0.29, 0.012, ARR)
C.rounded_box('top', (0.31, -0.04, 0.26), (0.48, 0.02, 0.02), 0.3, WOOD, exp)
C.rounded_box('sep', (0, -0.03, 0.4), (0.014, 0.01, 0.7), 0.3, M((0.3, 0.35, 0.6), rough=0.5), exp)
T.pop_in(exp, 590, 1.2, 10)
T.pop_out(exp, 768, 1.2, 6)
label('UN VASO', OC, (-0.37, EYP - 0.1, 1.06), 0.52, 600, 768, 0.17, 0.1)
label('MUCHOS', GC, (0.37, EYP - 0.1, 1.06), 0.52, 640, 768, 0.17, 0.1)
label('PLAF', OC, (0.0, LY, LZ), 0.9, 792, 824, 0.3, 0.2)
label('AGUANTAN', GC, (0.0, LY, LZ), 1.0, 830, TOTAL + 10, 0.3, 0.19)
confetti(856, (0.0, TY, Z0 + 2.0), n=24, spread=1.2)

OP = ((0.9, -3.7, 0.75), (0.0, TY, 0.6), 22)
W = ((0.0, -5.5, 2.1), (0.0, -1.4, 0.9), 18)
CU = ((0.2, -4.2, 1.5), (0.0, TY, 0.75), 24)
CU2 = ((-1.3, -4.0, 1.2), (-0.6, TY - 0.3, 0.5), 22)
EXP = ((0.0, -5.25, 1.55), (0.0, EYP, 1.5), 30)
camkey(0, OP)
camkey(56, OP)
for a, b, pose in ((70, 330, W), (332, 400, CU), (402, 500, W), (502, 584, CU2), (588, 770, EXP), (772, TOTAL - 1, W)):
    camkey(a, pose)
    camkey(b, pose)

tuki = make('tuki', 1.0)
ruki = make('ruki', 1.0)
TP, RP = Vector((-1.5, TY - 0.55, Z0)), Vector((1.45, TY - 0.6, Z0))
TOP = Vector((0, TY, GZ + H + 0.05))
T.turn(tuki, 0, 0)
T.turn(tuki, 68, 25)
T.turn(ruki, 0, -25)
T.place(tuki, 0, Vector((0, TY, GZ + H)))
T.place(tuki, 18, Vector((0, TY, GZ + H)))
T.place(tuki, 24, Vector((0, TY, Z0)))
T.place(tuki, 66, Vector((0, TY, Z0)))
T.place(tuki, 68, TP)
T.place(tuki, 340, TP)
T.place(tuki, 354, Vector((-0.8, TY - 0.3, GZ + H + 0.6)))
T.place(tuki, 368, TOP + Vector((0, 0, 0.12)))
T.place(tuki, 372, TOP)
T.turn(tuki, 372, 0)
for f, dz in ((375, -0.02), (380, 0.0), (384, -0.008), (388, 0.0)):
    T.place(tuki, f, TOP + Vector((0, 0, dz)))
for f in range(410, 470, 12):
    T.place(tuki, f, TOP)
    T.place(tuki, f + 6, TOP + Vector((0, 0, 0.12)))
    T.place(tuki, f + 12, TOP)
T.place(ruki, 0, RP + Vector((0.7, 0, 0)))
T.place(ruki, 66, RP + Vector((0.7, 0, 0)))
T.place(ruki, 68, RP)
T.place(ruki, 586, RP)
T.place(ruki, 588, RP + Vector((0.98, 0, 0)))
T.place(ruki, 770, RP + Vector((0.98, 0, 0)))
T.place(ruki, 772, RP)

for ch, side, f0 in ((ruki, 'L', 90), (tuki, 'R', 212), (ruki, 'L', 236), (ruki, 'L', 290), (tuki, 'R', 492), (ruki, 'L', 506), (tuki, 'R', 782), (tuki, 'R', 822)):
    T.arm(ch, side, f0, 0, None)
    T.arm(ch, side, f0 + 6, fwd=-85, out=30)
    T.arm(ch, side, f0 + 20, fwd=-85, out=30)
    T.rest_arm(ch, side, f0 + 28)
gesture(ruki, 'hops', 410)
gesture(ruki, 'hops', 846)
C.wave(tuki, 'R', 862, cycles=2, period=10)
C.wave(ruki, 'L', 858, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(tuki, (70, 200, 340, 470, 620, 740, 880))
T.blinks(ruki, (80, 230, 360, 520, 660, 800))
