from stage import *
from episodes.sombra_larga_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'sombra_larga'
Z0 = 0.08
auto_dress(EID, ENV)
DAWN = (1.0, 0.55, 0.5)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, DAWN, 0.7), (64, DAWN, 0.7), (80, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.95, 0.42, 0.5, 1)), (64, (0.95, 0.42, 0.5, 1)), (80, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

TY = -1.5
CREAM = M((1.0, 0.96, 0.9), rough=0.35, coat=0.7)
CORAL = M((1.0, 0.5, 0.45), rough=0.35, coat=0.7)
MINT = M((0.45, 0.85, 0.7), rough=0.4, coat=0.6)
GOLD = M((1.0, 0.8, 0.3), rough=0.3, coat=0.8)
SKYB = M((0.5, 0.75, 1.0), rough=0.35, coat=0.7)
LEAF = M((0.35, 0.78, 0.4), rough=0.4, coat=0.6)
BARK = M((0.62, 0.4, 0.26), rough=0.5, coat=0.4)
DARK = M((0.03, 0.02, 0.06), rough=1.0, coat=0.0)

mat = C.empty('ground_mat', None, (0, TY, Z0))
C.lathe('disc', [(0.0, 0.0), (0.0, 1.55), (0.015, 1.58), (0.03, 1.55), (0.03, 0.0)], CREAM, mat, segs=72, sx=1.3, sy=0.8)
C.tube('rim', [(math.cos(k * 6.2832 / 72) * 1.56 * 1.3, math.sin(k * 6.2832 / 72) * 1.56 * 0.8, 0.03) for k in range(73)], 0.022, CORAL, mat)
GZ = Z0 + 0.035

tree = C.empty('toy_tree', None, (0, TY, GZ))
C.lathe('pot', [(0.0, 0.0), (0.0, 0.13), (0.02, 0.14), (0.16, 0.12), (0.18, 0.13), (0.18, 0.0)], SKYB, tree, segs=48)
C.tube('trunk', [(0, 0, 0.15), (0, 0, 0.42)], 0.045, BARK, tree)
for x, z, r in ((0, 0.6, 0.22), (-0.14, 0.52, 0.15), (0.14, 0.52, 0.15), (0, 0.76, 0.13)):
    C.sphere('crown', (x, 0, z), (r, r * 0.95, r), LEAF, tree, 32)
for x, z in ((-0.12, 0.66), (0.1, 0.7), (0.17, 0.5), (-0.05, 0.48), (0.02, 0.84)):
    C.sphere('fruit', (x, -0.17, z), (0.032, 0.032, 0.032), CORAL, tree, 16)
G = 1.45
tree.scale = (G, G, G)
TH = 0.86 * G

AY = TY + 0.5
AR = 1.55
arc = C.empty('sun_arc', None, (0, AY, GZ))
for k, (m, dr) in enumerate(((CORAL, 0.0), (GOLD, -0.05), (MINT, -0.1))):
    C.tube('band', [(math.cos(math.pi * i / 64) * (AR + dr), 0.0, math.sin(math.pi * i / 64) * (AR + dr)) for i in range(65)], 0.024, m, arc)
for sx in (-1, 1):
    C.rounded_box('foot', (sx * (AR - 0.05), 0, 0.04), (0.26, 0.2, 0.08), 0.4, SKYB, arc)

sun = C.empty('toy_sun', None, (0, AY - 0.06, GZ))
SUNM = M((1.0, 0.82, 0.2), rough=0.3, coat=0.5, emit=1.6)
RAYM = M((1.0, 0.62, 0.22), rough=0.3, coat=0.5, emit=1.0)
C.sphere('core', (0, 0, 0), (0.15, 0.08, 0.15), SUNM, sun, 32)
for k in range(10):
    a = k * 6.2832 / 10
    C.rounded_box('ray', (math.cos(a) * 0.21, 0.0, math.sin(a) * 0.21), (0.06, 0.03, 0.06), 0.5, RAYM, sun)
for sx in (-1, 1):
    C.sphere('eye', (sx * 0.05, -0.08, 0.03), (0.016, 0.01, 0.022), DARK, sun, 12)
C.tube('smile', [(math.cos(math.pi * (1.15 + 0.7 * i / 12)) * 0.06, -0.08, -0.01 + math.sin(math.pi * (1.15 + 0.7 * i / 12)) * 0.05) for i in range(13)], 0.008, DARK, sun)
sun.scale = (1.3, 1.3, 1.3)

sh = C.empty('shadow', None, (0, TY, GZ + 0.004))
trunk_s = C.empty('trunk_s', sh, (0, 0, 0))
C.rounded_box('ts', (0.5, 0, 0), (1.0, 0.09 * G, 0.004), 0.3, DARK, trunk_s)
crown_s = C.empty('crown_s', sh, (0, 0, 0.001))
C.sphere('cs', (0, 0, 0), (1.0, 1.0, 0.004), DARK, crown_s, 40)
C.sphere('base', (0, 0, -0.001), (0.2 * G, 0.13 * G, 0.004), DARK, sh, 32)


def theta(f):
    pts = ((0, 145), (236, 145), (376, 88), (500, 88), (546, 35), (770, 35), (772, 145), (826, 145), (850, 88), (TOTAL, 88))
    for (a, ta), (b, tb) in zip(pts, pts[1:]):
        if a <= f <= b:
            u = 0 if b == a else (f - a) / (b - a)
            u = u * u * (3 - 2 * u)
            return ta + (tb - ta) * u
    return pts[-1][1]


for f in list(range(0, TOTAL + 1, 4)) + [771, 772]:
    t = math.radians(theta(f))
    K(sun, 'location', f, (math.cos(t) * (AR - 0.05), AY - 0.06, GZ + math.sin(t) * (AR - 0.05)))
    K(sun, 'rotation_euler', f, (0, 0, math.radians(f * 0.6)))
    L = max(-1.6, min(1.6, -TH * math.cos(t) / max(math.sin(t), 0.05)))
    sgn = 1 if L >= 0 else -1
    a = abs(L)
    K(trunk_s, 'scale', f, (sgn * max(a * 0.62, 0.001), 1, 1))
    K(crown_s, 'location', f, (L * 0.74, 0, 0.001))
    K(crown_s, 'scale', f, ((0.24 + a * 0.2) * G, 0.2 * G, 1))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


KC, OC, GC = (0.08, 0.06, 0.16), (0.85, 0.35, 0.05), (0.05, 0.42, 0.15)
LZ = GZ + AR + 0.55
LY = AY - 0.3
label('¿LARGA?', KC, (-0.5, LY, LZ), 0.92, 190, 372, 0.3, 0.2)
label('¿CORTA?', OC, (0.5, LY, LZ), 0.92, 198, 372, 0.3, 0.2)
label('¡CORTA!', GC, (0.0, LY, LZ), 0.92, 396, 482, 0.3, 0.22)
label('¡LARGA!', OC, (0.0, LY, LZ), 0.92, 552, 584, 0.3, 0.22)

EYP = -2.95
exp = C.empty('diagram', None, (0.0, EYP, 1.1))
C.rounded_box('panel', (0, 0.04, 0.4), (1.3, 0.03, 0.9), 0.4, M((0.5, 0.56, 0.92), rough=0.8, coat=0.0), exp)
YEL = M((1.0, 0.78, 0.1), rough=0.3, coat=0.6, emit=0.8)
GRD = M((0.3, 0.6, 0.35), rough=0.6, coat=0.2)
for sx, sl, hi in ((-1, 0.44, False), (1, 0.09, True)):
    cx = sx * 0.31
    tx = cx if hi else cx - 0.14
    C.rounded_box('gl', (cx, -0.02, 0.1), (0.56, 0.02, 0.03), 0.4, GRD, exp)
    C.tube('tr', [(tx, -0.04, 0.11), (tx, -0.04, 0.32)], 0.02, BARK, exp)
    C.sphere('cr', (tx, -0.04, 0.38), (0.09, 0.02, 0.09), LEAF, exp, 20)
    C.rounded_box('sh', (tx + sl / 2, -0.045, 0.115), (sl, 0.02, 0.035), 0.4, DARK, exp)
    sp = (tx, -0.04, 0.7) if hi else (cx - 0.24, -0.04, 0.24)
    C.sphere('sn', sp, (0.075, 0.02, 0.075), YEL, exp, 20)
C.rounded_box('sep', (0, -0.03, 0.4), (0.014, 0.01, 0.7), 0.3, M((0.3, 0.35, 0.6), rough=0.5), exp)
T.pop_in(exp, 590, 1.2, 10)
T.pop_out(exp, 768, 1.2, 6)
label('LARGA', OC, (-0.37, EYP - 0.1, 1.06), 0.5, 600, 768, 0.17, 0.11)
label('CORTA', GC, (0.37, EYP - 0.1, 1.06), 0.5, 640, 768, 0.17, 0.11)
label('LARGA', OC, (0.0, LY, LZ), 0.9, 792, 824, 0.3, 0.2)
label('CORTA', GC, (0.0, LY, LZ), 0.9, 830, TOTAL + 10, 0.3, 0.2)
confetti(856, (0.0, TY, Z0 + 2.0), n=24, spread=1.2)

OP = ((1.7, -3.7, 1.25), (0.5, TY + 0.1, 0.35), 20)
W = ((0.0, -5.6, 2.2), (0.0, -1.4, 0.95), 18)
CU = ((0.0, -5.9, 2.3), (0.0, -1.4, 1.05), 18)
EXP = ((0.0, -5.25, 1.55), (0.0, EYP, 1.5), 30)
camkey(0, OP)
camkey(56, OP)
for a, b, pose in ((70, 186, W), (188, 376, CU), (378, 584, W), (588, 770, EXP), (772, TOTAL - 1, W)):
    camkey(a, pose)
    camkey(b, pose)

pimo = make('pimo', 1.1)
ruki = make('ruki', 1.1)
PP, RP = Vector((-1.5, TY - 0.55, Z0)), Vector((1.5, TY - 0.55, Z0))
T.turn(pimo, 0, 25)
T.turn(ruki, 0, -25)
for ch, p0, dx in ((pimo, PP, -0.7), (ruki, RP, 0.7)):
    T.place(ch, 0, p0 + Vector((dx, 0, 0)))
    T.place(ch, 66, p0 + Vector((dx, 0, 0)))
    T.place(ch, 68, p0)
    T.place(ch, 586, p0)
    T.place(ch, 588, p0 + Vector((dx * 1.4, 0, 0)))
    T.place(ch, 770, p0 + Vector((dx * 1.4, 0, 0)))
    T.place(ch, 772, p0)

for ch, side, f0 in ((ruki, 'R', 104), (pimo, 'L', 182), (ruki, 'R', 236), (ruki, 'R', 300), (pimo, 'L', 492), (pimo, 'L', 782), (pimo, 'L', 822)):
    T.arm(ch, side, f0, 0, None)
    T.arm(ch, side, f0 + 6, fwd=-85, out=30)
    T.arm(ch, side, f0 + 20, fwd=-85, out=30)
    T.rest_arm(ch, side, f0 + 28)
gesture(pimo, 'hops', 72)
gesture(ruki, 'hops', 410)
C.wave(pimo, 'R', 862, cycles=2, period=10)
C.wave(ruki, 'L', 858, cycles=2, period=10)
gesture(ruki, 'hops', 846)

T.lines(EID, LINES)
T.blinks(pimo, (70, 200, 340, 470, 620, 740, 880))
T.blinks(ruki, (80, 230, 360, 520, 660, 800))
