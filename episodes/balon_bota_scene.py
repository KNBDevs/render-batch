from stage import *
from episodes.balon_bota_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
from mathutils import Euler
EID = 'balon_bota'
Z0 = 0.08
auto_dress(EID, ENV)
NIGHT = (0.5, 0.68, 1.0)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, NIGHT, 0.5), (64, NIGHT, 0.5), (80, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.12, 0.2, 0.55, 1)), (64, (0.12, 0.2, 0.55, 1)), (80, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

TY = -1.45
CREAM = M((1.0, 0.96, 0.9), rough=0.35, coat=0.7)
CORAL = M((1.0, 0.45, 0.4), rough=0.35, coat=0.7)
MINT = M((0.45, 0.85, 0.7), rough=0.4, coat=0.6)
GOLD = M((1.0, 0.8, 0.3), rough=0.3, coat=0.8)
DARK = M((0.05, 0.03, 0.06), rough=0.6, coat=0.2)

spot = C.empty('court', None, (0, TY, Z0))
C.lathe('disc', [(0.0, 0.0), (0.0, 0.62), (0.012, 0.64), (0.024, 0.62), (0.024, 0.0)], M((0.98, 0.62, 0.3), rough=0.5, coat=0.4), spot, segs=64)
C.tube('ring', [(math.cos(k * 6.2832 / 64) * 0.5, math.sin(k * 6.2832 / 64) * 0.5, 0.026) for k in range(65)], 0.014, CREAM, spot)
GZ = Z0 + 0.024

R = 0.34
ball = C.empty('ball', None, (0, TY, GZ))
sq = C.empty('squash', ball, (0, 0, 0))
C.sphere('skin', (0, 0, R), (R, R, R), M((1.0, 0.5, 0.15), rough=0.45, coat=0.5), sq, 48)
for rot in ((0, 0, 0), (0, 0, 1.5708)):
    rv = Euler(rot)
    pts = []
    for k in range(65):
        a = k * 6.2832 / 64
        v = Vector((math.cos(a) * R * 1.01, 0, math.sin(a) * R * 1.01))
        v.rotate(rv)
        pts.append((v.x, v.y, v.z + R))
    C.tube('seam', pts, 0.008, DARK, sq)
C.tube('belt', [(math.cos(k * 6.2832 / 64) * R * 1.01, math.sin(k * 6.2832 / 64) * R * 1.01, R) for k in range(65)], 0.008, DARK, sq)
C.sphere('valve', (0.0, -R * 0.98, R * 1.25), (0.022, 0.012, 0.022), GOLD, sq, 12)

D = (1.3, 1.3, 0.46)
ROUND = (1.0, 1.0, 1.0)


def lerp(a, b, u):
    return tuple(x + (y - x) * u for x, y in zip(a, b))


def at(f, z, s):
    K(ball, 'location', f, (0, TY, GZ + z))
    K(sq, 'scale', f, s)


at(0, 1.25, (0.95, 0.95, 0.8))
at(14, 0.0, (1.0, 1.0, 0.7))
at(17, 0.0, (1.45, 1.45, 0.36))
at(24, 0.0, D)
at(236, 0.0, D)
for k, f in enumerate((240, 266, 292, 318, 344)):
    at(f + 14, 0.0, lerp(D, ROUND, (k + 1) / 5))
at(366, 0.0, ROUND)
at(378, 1.15, ROUND)
at(381, 1.15, ROUND)
for f_hit, f_top, h in ((392, 404, 0.85), (416, 426, 0.5), (436, 444, 0.25), (452, 458, 0.08)):
    at(f_hit - 1, 0.0, ROUND)
    at(f_hit, 0.0, (1.18, 1.18, 0.74))
    at(f_hit + 2, 0.02, ROUND)
    at(f_top, h, ROUND)
at(462, 0.0, ROUND)
at(500, 0.0, ROUND)
at(528, 0.0, D)
at(532, 0.0, D)
at(540, 0.9, (1.1, 1.1, 0.68))
at(547, 0.0, (1.05, 1.05, 0.62))
at(549, 0.0, (1.45, 1.45, 0.34))
at(556, 0.0, D)
at(830, 0.0, D)
at(840, 0.0, ROUND)
at(848, 0.75, ROUND)
for f_hit, f_top, h in ((856, 866, 0.45), (874, 882, 0.15)):
    at(f_hit - 1, 0.0, ROUND)
    at(f_hit, 0.0, (1.18, 1.18, 0.74))
    at(f_hit + 2, 0.02, ROUND)
    at(f_top, h, ROUND)
at(890, 0.0, ROUND)

PX = 0.68
pump = C.empty('air_pump', None, (PX, TY - 0.12, GZ))
C.rounded_box('foot', (0, 0, 0.025), (0.36, 0.2, 0.05), 0.4, MINT, pump)
C.lathe('barrel', [(0.04, 0.0), (0.04, 0.075), (0.06, 0.085), (0.5, 0.08), (0.53, 0.06), (0.55, 0.03), (0.55, 0.0)], CORAL, pump, segs=40)
for z in (0.16, 0.3, 0.44):
    C.tube('stripe', [(math.cos(k * 6.2832 / 40) * 0.083, math.sin(k * 6.2832 / 40) * 0.083, z) for k in range(41)], 0.008, CREAM, pump)
hd = C.empty('handle', pump, (0, 0, 0))
C.tube('rod', [(0, 0, 0.5), (0, 0, 0.8)], 0.016, CREAM, hd)
C.tube('bar', [(-0.17, 0, 0.8), (0.17, 0, 0.8)], 0.03, GOLD, hd)
for sx in (-1, 1):
    C.sphere('knob', (sx * 0.18, 0, 0.8), (0.04, 0.04, 0.04), MINT, hd, 16)
hose = C.empty('hose', None, (0, 0, 0))
C.tube('h', [(PX - 0.06, TY - 0.19, GZ + 0.06), (PX - 0.2, TY - 0.26, GZ + 0.03), (0.2, TY - 0.2, GZ + 0.06), (0.06, TY - R * 1.15, GZ + 0.15)], 0.016, M((0.35, 0.6, 1.0), rough=0.4, coat=0.6), hose)
K(hd, 'location', 0, (0, 0, 0))
for f in (240, 266, 292, 318, 344):
    K(hd, 'location', f - 2, (0, 0, 0))
    K(hd, 'location', f + 6, (0, 0, -0.26))
    K(hd, 'location', f + 14, (0, 0, -0.26))
    K(hd, 'location', f + 22, (0, 0, 0))
T.pop_in(pump, 118, 1.25, 8)
T.pop_out(pump, 362, 1.25, 6)
T.pop_in(hose, 226, 1.0, 6)
T.pop_out(hose, 360, 1.0, 4)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


KC, OC, GC = (0.08, 0.06, 0.16), (0.85, 0.35, 0.05), (0.05, 0.42, 0.15)
LY, LZ = -1.0, 2.1
label('¿BOTA?', GC, (-0.48, LY, LZ), 0.86, 190, 372, 0.3, 0.2)
label('¿NO BOTA?', OC, (0.5, LY, LZ), 1.08, 198, 372, 0.3, 0.2)
label('¡BOTA!', GC, (0.0, LY, LZ), 0.86, 396, 482, 0.3, 0.22)
label('¡PLOF!', OC, (0.0, LY, LZ), 0.86, 552, 584, 0.3, 0.22)

exp = C.empty('diagram', None, (0.0, -2.1, 1.12))
C.rounded_box('panel', (0, 0.04, 0.4), (1.3, 0.03, 0.88), 0.4, M((0.5, 0.56, 0.92), rough=0.8, coat=0.0), exp)
ORG = M((1.0, 0.5, 0.15), rough=0.45, coat=0.5)
YEL = M((1.0, 0.85, 0.2), rough=0.3, coat=0.5, emit=0.6)
GRD = M((0.3, 0.6, 0.35), rough=0.6, coat=0.2)
for cx in (-0.31, 0.31):
    C.rounded_box('gl', (cx, -0.02, 0.1), (0.5, 0.02, 0.03), 0.4, GRD, exp)
C.sphere('flat', (-0.31, -0.04, 0.16), (0.17, 0.03, 0.06), ORG, exp, 24)
C.sphere('round', (0.31, -0.04, 0.27), (0.14, 0.03, 0.14), ORG, exp, 24)
for k in range(8):
    a = k * 6.2832 / 8
    C.tube('push', [(0.31 + math.cos(a) * 0.04, -0.07, 0.27 + math.sin(a) * 0.04), (0.31 + math.cos(a) * 0.11, -0.07, 0.27 + math.sin(a) * 0.11)], 0.009, YEL, exp)
C.tube('up', [(0.31, -0.05, 0.46), (0.31, -0.05, 0.7)], 0.025, M(GC, rough=0.4, coat=0.5), exp)
for sx in (-1, 1):
    C.tube('uph', [(0.31 + sx * 0.07, -0.05, 0.64), (0.31, -0.05, 0.73)], 0.025, M(GC, rough=0.4, coat=0.5), exp)
C.rounded_box('sep', (0, -0.03, 0.4), (0.014, 0.01, 0.7), 0.3, M((0.3, 0.35, 0.6), rough=0.5), exp)
T.pop_in(exp, 590, 1.2, 10)
T.pop_out(exp, 768, 1.2, 6)
label('¡EMPUJA!', GC, (0.0, -2.2, 2.0), 0.8, 620, 768, 0.2, 0.12)
label('SIN AIRE', OC, (-0.37, -2.2, 1.06), 0.62, 600, 768, 0.19, 0.105)
label('CON AIRE', GC, (0.37, -2.2, 1.06), 0.62, 640, 768, 0.19, 0.105)
label('SIN AIRE', OC, (0.0, LY, LZ), 1.0, 792, 824, 0.3, 0.2)
label('CON AIRE', GC, (0.0, LY, LZ), 1.0, 830, TOTAL + 10, 0.3, 0.2)
confetti(858, (0.0, TY, Z0 + 2.0), n=24, spread=1.2)

OP = ((0.6, -3.0, 0.55), (0.0, TY, 0.4), 24)
W = ((0.0, -5.4, 1.75), (0.0, -1.25, 1.08), 18)
WQ = ((0.0, -5.5, 1.9), (0.0, -1.25, 1.2), 18)
EXP = ((0.0, -4.75, 1.55), (0.0, -2.1, 1.5), 30)
camkey(0, OP)
camkey(56, OP)
for a, b, pose in ((70, 186, W), (188, 376, WQ), (378, 584, W), (588, 770, EXP), (772, TOTAL - 1, W)):
    camkey(a, pose)
    camkey(b, pose)

tuki = make('tuki', 1.15)
moki = make('moki', 1.15)
TP, MP = Vector((-1.2, -1.5, Z0)), Vector((1.18, -1.5, Z0))
T.turn(tuki, 0, 25)
T.turn(moki, 0, -25)
for ch, p0, dx in ((tuki, TP, -0.6), (moki, MP, 0.6)):
    T.place(ch, 0, p0 + Vector((dx, 0, 0)))
    T.place(ch, 66, p0 + Vector((dx, 0, 0)))
    T.place(ch, 68, p0)
    T.place(ch, 586, p0)
    T.place(ch, 588, p0 + Vector((dx * 1.8, 0, 0)))
    T.place(ch, 770, p0 + Vector((dx * 1.8, 0, 0)))
    T.place(ch, 772, p0)

T.arm(moki, 'R', 104, 0, None)
T.arm(moki, 'R', 112, fwd=-80, out=25)
T.arm(moki, 'R', 132, fwd=-80, out=25)
T.rest_arm(moki, 'R', 142)
for f in (240, 266, 292, 318, 344):
    T.arm(moki, 'R', f - 2, fwd=-100, out=20)
    T.arm(moki, 'R', f + 8, fwd=-55, out=20)
    T.arm(moki, 'R', f + 20, fwd=-100, out=20)
T.rest_arm(moki, 'R', 368)
for ch, side, f0 in ((tuki, 'L', 182), (moki, 'R', 372), (tuki, 'L', 492), (tuki, 'L', 782), (tuki, 'L', 820)):
    T.arm(ch, side, f0, 0, None)
    T.arm(ch, side, f0 + 6, fwd=-85, out=30)
    T.arm(ch, side, f0 + 20, fwd=-85, out=30)
    T.rest_arm(ch, side, f0 + 28)
gesture(tuki, 'hops', 72)
gesture(moki, 'hops', 410)
gesture(tuki, 'hops', 860)
C.wave(tuki, 'R', 866, cycles=2, period=10)
C.wave(moki, 'L', 862, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(tuki, (70, 200, 340, 470, 620, 740, 880))
T.blinks(moki, (80, 230, 360, 520, 660, 800))
