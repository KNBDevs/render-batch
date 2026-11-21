from stage import *
from episodes.manguera_arcoiris_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'manguera_arcoiris'
Z0 = 0.08
auto_dress(EID, ENV)
PINK = (1.0, 0.55, 0.78)
for l in list(bpy.data.lights):
    e = l.energy
    for f, c, k in ((0, PINK, 0.7), (64, PINK, 0.7), (80, (1.0, 0.95, 0.88), 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.55, 0.22, 0.42, 1)), (64, (0.55, 0.22, 0.42, 1)), (80, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

CORAL = M((1.0, 0.5, 0.45), rough=0.35, coat=0.7)
GOLD = M((1.0, 0.8, 0.3), rough=0.3, coat=0.8)
GREEN = M((0.3, 0.75, 0.4), rough=0.4, coat=0.6)
CREAM = M((1.0, 0.96, 0.9), rough=0.35, coat=0.7)

TY = -1.95
SUNP = Vector((-1.45, 0.4, 3.05))
sun_o = C.empty('sun', None, tuple(SUNP))
C.sphere('disc', (0, 0, 0), (0.42, 0.12, 0.42), M((1.0, 0.78, 0.2), rough=0.3, emit=0.8), sun_o, 32)
for i in range(10):
    a = i * math.tau / 10
    C.sphere('ray', (0.6 * math.cos(a), 0, 0.6 * math.sin(a)), (0.08, 0.05, 0.08), M((1.0, 0.62, 0.2), emit=0.7), sun_o, 16)
for f in range(0, TOTAL, 48):
    K(sun_o, 'rotation_euler', f, (0, f * 0.004, 0))

post = C.empty('post', None, (0, TY, Z0))
C.lathe('pole', [(0.0, 0.0), (0.0, 0.22), (0.05, 0.22), (0.09, 0.07), (0.78, 0.06), (0.82, 0.1), (0.84, 0.0)], CORAL, post, segs=32)
C.sphere('cap', (0, 0, 0.86), (0.1, 0.1, 0.08), GOLD, post, 24)
coil = []
for i in range(60):
    t = i / 59
    a = t * math.tau * 2.2
    r = 0.36 - 0.18 * t
    coil.append((0.55 + r * math.cos(a), -1.55 + r * math.sin(a) * 0.7, 0.05))
coil += [(0.2, -1.75, 0.05), (0.08, -1.9, 0.12), (0.06, -1.93, 0.35)]
C.tube('hose', coil, 0.045, GREEN, None)

NZ = Vector((0, TY, Z0 + 0.92))
noz = C.empty('noz', None, tuple(NZ))
nb = C.empty('nb', noz, (0, 0, 0), (0, math.pi / 2, 0))
C.lathe('n1', [(-0.05, 0.0), (-0.05, 0.09), (0.08, 0.09), (0.24, 0.06), (0.27, 0.075), (0.27, 0.0)], GOLD, nb, segs=32)
C.tube('grip', [(-0.05, 0, 0), (-0.06, 0, -0.18)], 0.04, GREEN, noz)


def point(f, tgt):
    d = tgt - NZ
    K(noz, 'rotation_euler', f, (0, -math.atan2(d.z, math.hypot(d.x, d.y)), math.atan2(d.y, d.x)))


WATER = MA((0.65, 0.88, 1.0), 0.4, emit=0.25)
MIST = MA((0.9, 0.96, 1.0), 0.22, emit=0.3)
ML = Vector((-0.95, TY - 0.05, 1.3))
MR = Vector((0.8, TY - 0.05, 0.65))


def jet(name, a, b, lift):
    pts = [tuple(a + (b - a) * t + Vector((0, 0, lift * 4 * t * (1 - t)))) for t in (0, 0.2, 0.4, 0.6, 0.8, 1.0)]
    o = C.empty(name, None, (0, 0, 0))
    C.tube('w', pts, 0.03, WATER, o)
    for i in range(14):
        t = i / 13
        p = a + (b - a) * t + Vector((0, 0, lift * 4 * t * (1 - t)))
        C.sphere('dr', tuple(p + Vector((0, -0.03, 0.05 * math.sin(i * 2.1)))), (0.035, 0.035, 0.05), WATER, o, 12)
    return o


def mist(name, c, seed):
    rnd = random.Random(seed)
    o = C.empty(name, None, tuple(c))
    for i in range(44):
        p = (rnd.uniform(-0.55, 0.55), rnd.uniform(-0.12, 0.12), rnd.uniform(-0.45, 0.45))
        r = rnd.uniform(0.025, 0.06)
        C.sphere('m', p, (r, r, r), MIST if i % 3 else WATER, o, 10)
    return o


def show(o, f_in, f_out=None, s=1.0):
    if f_in > 0:
        K(o, 'scale', 0, (0, 0, 0))
        K(o, 'scale', f_in - 1, (0, 0, 0))
    K(o, 'scale', f_in + 4, (s, s, s))
    if f_out:
        K(o, 'scale', f_out, (s, s, s))
        K(o, 'scale', f_out + 4, (0, 0, 0))


TL = NZ + (ML - NZ).normalized() * 0.28
TR = NZ + (MR - NZ).normalized() * 0.28
jl = jet('jl', TL, ML + Vector((0.3, 0, -0.1)), 0.25)
jr = jet('jr', TR, MR - Vector((0.3, 0, 0)), 0.3)
ml = mist('ml', ML, 77)
mr = mist('mr', MR, 78)
for o, spans in ((jl, ((0, 252), (518, 826))), (ml, ((4, 256), (522, 830))), (jr, ((262, 506), (836, None))), (mr, ((266, 510), (840, None)))):
    for a, b in spans:
        show(o, a, b)
point(0, ML)
point(246, ML)
point(258, MR)
point(500, MR)
point(512, ML)
point(822, ML)
point(834, MR)

RB = [(1.0, 0.25, 0.25), (1.0, 0.6, 0.15), (1.0, 0.92, 0.25), (0.3, 0.85, 0.35), (0.3, 0.6, 1.0), (0.65, 0.4, 1.0)]
RC = Vector((0.8, TY - 0.14, 0.3))
bow = C.empty('bow', None, tuple(RC))
for k, rgb in enumerate(RB):
    r = 0.64 - k * 0.06
    pts = [(r * math.cos(t), 0, r * math.sin(t)) for t in [math.pi * i / 24 for i in range(25)]]
    C.tube('arc', pts, 0.034, MA(rgb, 0.88, emit=0.55), bow)
show(bow, 322, 506)
show(bow, 842)
for f in range(352, 500, 14):
    K(bow, 'scale', f, (1, 1, 1))
    K(bow, 'scale', f + 7, (1.04, 1.04, 1.04))
K(bow, 'scale', 502, (1, 1, 1))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.25), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


OC, GC = (0.85, 0.35, 0.05), (0.05, 0.42, 0.15)
LZ, LY = 2.0, -2.0
label('¿SALE?', GC, (-0.55, LY, LZ), 0.92, 190, 372, 0.3, 0.19)
label('¿NO SALE?', OC, (0.55, LY, LZ), 1.08, 198, 372, 0.3, 0.17)
label('¡SALE!', GC, (0.0, LY, LZ), 0.9, 396, 482, 0.3, 0.22)
label('¡NO SALE!', OC, (0.0, LY, LZ), 1.08, 552, 584, 0.3, 0.2)

EYP = -2.95
exp = C.empty('diagram', None, (0.0, EYP, 1.1))
C.rounded_box('panel', (0, 0.04, 0.4), (1.3, 0.03, 0.9), 0.4, M((0.25, 0.4, 0.8), rough=0.8, coat=0.0), exp)
C.sphere('esun', (-0.48, -0.04, 0.55), (0.12, 0.02, 0.12), M((1.0, 0.78, 0.2), emit=0.7), exp, 24)
C.tube('in', [(-0.36, -0.045, 0.52), (-0.08, -0.045, 0.42)], 0.016, M((1.0, 0.9, 0.5), emit=0.6), exp)
C.sphere('drop', (0.0, -0.05, 0.4), (0.1, 0.02, 0.12), MA((0.55, 0.85, 1.0), 0.85, emit=0.4), exp, 24)
for k, rgb in enumerate(RB):
    zz = 0.62 - k * 0.075
    C.tube('fan', [(0.08, -0.045, 0.4), (0.5, -0.045, zz)], 0.013, M(rgb, emit=0.5), exp)
T.pop_in(exp, 590, 1.2, 10)
T.pop_out(exp, 768, 1.2, 6)
label('GOTITA', (0.1, 0.3, 0.7), (-0.32, EYP - 0.1, 1.08), 0.56, 620, 768, 0.17, 0.11)
label('COLORES', GC, (0.38, EYP - 0.1, 1.08), 0.62, 660, 768, 0.17, 0.11)
label('NADA', OC, (0.0, LY, LZ), 0.8, 792, 826, 0.3, 0.2)
label('¡ARCOÍRIS!', GC, (0.0, LY, LZ), 1.15, 836, TOTAL + 10, 0.3, 0.18)
confetti(856, (0.0, TY, Z0 + 2.0), n=24, spread=1.2)

OP = ((-0.55, -4.7, 1.45), (-0.8, -1.8, 1.2), 22)
W = ((0.0, -5.7, 2.1), (0.0, -1.45, 1.05), 18)
CU = ((0.7, -4.5, 1.2), (0.75, -1.9, 0.85), 24)
EXP = ((0.0, -5.25, 1.55), (0.0, EYP, 1.5), 30)
camkey(0, OP)
camkey(56, OP)
for a, b, pose in ((70, 186, W), (188, 318, W), (320, 400, CU), (402, 584, W), (588, 770, EXP), (772, TOTAL - 1, W)):
    camkey(a, pose)
    camkey(b, pose)

pim = make('pimo', 1.0)
ruk = make('ruki', 1.0)
PP, RP = Vector((-1.7, -1.6, Z0)), Vector((1.75, -1.6, Z0))
T.turn(pim, 0, 25)
T.turn(ruk, 0, -25)
T.place(pim, 0, Vector((-1.15, -1.6, Z0)))
T.place(pim, 60, Vector((-1.15, -1.6, Z0)))
T.place(pim, 70, PP)
T.place(ruk, 0, RP + Vector((0.7, 0, 0)))
T.place(ruk, 66, RP + Vector((0.7, 0, 0)))
T.place(ruk, 68, RP)
for ch, p0, dx in ((pim, PP, -0.7), (ruk, RP, 0.7)):
    T.place(ch, 586, p0)
    T.place(ch, 588, p0 + Vector((dx * 1.4, 0, 0)))
    T.place(ch, 770, p0 + Vector((dx * 1.4, 0, 0)))
    T.place(ch, 772, p0)
T.arm(pim, 'R', 0, fwd=-80, out=20)
T.arm(pim, 'L', 0, fwd=-80, out=20)
T.arm(pim, 'R', 56, fwd=-80, out=20)
T.arm(pim, 'L', 56, fwd=-80, out=20)
T.rest_arm(pim, 'R', 66)
T.rest_arm(pim, 'L', 66)
for ch, side, f0 in ((ruk, 'L', 104), (pim, 'R', 236), (ruk, 'L', 410), (pim, 'R', 494), (pim, 'R', 818)):
    T.arm(ch, side, f0, 0, None)
    T.arm(ch, side, f0 + 6, fwd=-85, out=30)
    T.arm(ch, side, f0 + 20, fwd=-85, out=30)
    T.rest_arm(ch, side, f0 + 28)
gesture(pim, 'hops', 24)
gesture(ruk, 'hops', 404)
gesture(pim, 'hops', 846)
C.wave(pim, 'R', 862, cycles=2, period=10)
C.wave(ruk, 'L', 858, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(pim, (70, 200, 340, 470, 620, 740, 880))
T.blinks(ruk, (80, 230, 360, 520, 660, 800))
