from stage import *
from episodes.piedras_sube_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'piedras_sube'
Z0 = 0.08
auto_dress(EID, ENV)
TEAL = (0.45, 1.0, 0.82)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, TEAL), (52, TEAL), (66, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (0.7, 1.0, 0.9, 1)), (52, (0.7, 1.0, 0.9, 1)), (66, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

YC = -2.0
spawn('low_table', 2, 6113, 'candy', (0.0, YC, Z0), 1.0, 0)
TOP = Z0 + 0.62
JS = 2.0
JX = -0.05
jar = C.empty('jar', None, (JX, YC, TOP))
jar.scale = (JS, JS, JS)
R, RI, H, BOT = 0.075, 0.067, 0.40, 0.02
glass = MA((0.9, 0.97, 1.0), 0.12)
C.lathe('jar_glass', [(0, 0.0), (0, R * 0.92), (0.012, R), (H, R), (H + 0.004, R - 0.004), (H, RI), (BOT, RI), (BOT, 0.0)], glass, jar, segs=56)
C.tube('jar_rim', [(math.cos(a) * (R + 0.003), math.sin(a) * (R + 0.003), H - 0.008) for a in [i * math.tau / 48 for i in range(49)]], 0.007, M((0.98, 0.55, 0.62), coat=0.7), jar)
C.tube('jar_foot', [(math.cos(a) * (R * 0.94), math.sin(a) * (R * 0.94), 0.008) for a in [i * math.tau / 48 for i in range(49)]], 0.008, M((0.55, 0.78, 0.98), coat=0.7), jar)
redm = M((0.95, 0.25, 0.3), rough=0.35, coat=0.5, emit=0.25)
L0W = 0.20
C.tube('mark', [(math.cos(a) * (R + 0.002), math.sin(a) * (R + 0.002), L0W) for a in [math.radians(d) for d in range(-150, -29, 6)]], 0.0035, redm, jar)
for z in (0.10, 0.15, 0.25, 0.30, 0.35):
    C.tube('tick', [(math.cos(a) * (R + 0.002), math.sin(a) * (R + 0.002), z) for a in [math.radians(d) for d in range(-104, -75, 7)]], 0.0022, M((0.4, 0.55, 0.8), rough=0.4), jar)

water = MA((0.25, 0.62, 1.0), 0.32, rough=0.03, emit=0.04)
piv = C.empty('wpiv', jar, (0, 0, BOT + 0.001))
C.lathe('water', [(0, 0.0), (0, RI - 0.003), (1.0, RI - 0.003), (1.0, 0.0)], water, piv, segs=48)
LV = [L0W, 0.238, 0.275, 0.313, 0.35]
DROPS = (322, 348, 374, 400)


def wl(f, z):
    K(piv, 'scale', f, (1, 1, z - BOT))


wl(0, LV[0])
for k, f in enumerate(DROPS):
    wl(f, LV[k])
    wl(f + 4, LV[k + 1] + 0.008)
    wl(f + 9, LV[k + 1])

BR = 0.034
ball = C.empty('ball', jar, (0, 0, LV[0]))
C.sphere('ball_b', (0, 0, 0), (BR, BR, BR), M((1.0, 0.55, 0.12), rough=0.3, coat=0.8), ball, 24)
C.tube('ball_band', [(math.cos(a) * (BR + 0.001), math.sin(a) * (BR + 0.001), 0) for a in [i * math.tau / 32 for i in range(33)]], 0.005, M((1, 1, 1), rough=0.3, coat=0.6), ball)
ball.rotation_euler = (math.radians(70), 0, math.radians(20))


def bz(f, z, x=0.0, y=0.0):
    K(ball, 'location', f, (x, y, z + BR * 0.15))


bz(0, LV[0])
bz(16, LV[0] + 0.004)
bz(32, LV[0])
for k, f in enumerate(DROPS):
    bz(f + 1, LV[k], 0.012 * (-1) ** k)
    bz(f + 5, LV[k + 1] + 0.01, -0.01 * (-1) ** k)
    bz(f + 11, LV[k + 1], 0.008 * (-1) ** k)

stm = [M(c, rough=0.55, coat=0.35) for c in ((0.2, 0.19, 0.26), (0.32, 0.22, 0.16), (0.16, 0.25, 0.24), (0.28, 0.22, 0.32))]
BW = Vector((0.36, YC + 0.06, TOP))
spawn('mixing_bowl', 1, 2207, 'candy', tuple(BW), 1.1, 0)
SS = ((0.058, 0.05, 0.036), (0.055, 0.05, 0.038), (0.06, 0.048, 0.035), (0.054, 0.05, 0.036))
REST = ((0.008, 0.004, BOT + 0.037), (-0.01, 0.006, BOT + 0.11), (0.01, -0.006, BOT + 0.183), (-0.006, 0.004, BOT + 0.256))
bowl_l = (Vector(BW) - Vector((JX, YC, TOP))) / JS
stones = []
for k, f in enumerate(DROPS):
    s = C.sphere('stone', (0, 0, 0), SS[k], stm[k], jar, 20)
    s.rotation_euler = (math.radians(8 * k), math.radians(-6 + 5 * k), math.radians(40 * k))
    sb = (bowl_l.x + 0.02 * (k - 1.5), bowl_l.y, bowl_l.z + 0.05)
    K(s, 'location', 0, sb)
    K(s, 'location', f - 22, sb)
    K(s, 'location', f - 16, (sb[0], sb[1], H + 0.12))
    K(s, 'location', f - 10, (0.02, -0.005, H + 0.09))
    K(s, 'location', f - 6, (0.012, 0.0, H + 0.07))
    K(s, 'location', f, (REST[k][0], REST[k][1], LV[k] + 0.01))
    K(s, 'location', f + 8, REST[k])
    stones.append(s)

sp = MA((0.8, 0.93, 1.0), 0.5, rough=0.05, emit=0.3)
for k, f in enumerate(DROPS):
    for j in range(5):
        a = j * math.tau / 5 + k
        d = C.sphere('spl', (0, 0, LV[k + 1]), (0.007, 0.007, 0.009), sp, jar, 10)
        K(d, 'scale', 0, (0, 0, 0))
        K(d, 'scale', f, (0, 0, 0))
        K(d, 'scale', f + 2, (0.007, 0.007, 0.009))
        K(d, 'scale', f + 12, (0, 0, 0))
        K(d, 'location', f, (0, 0, LV[k + 1]))
        K(d, 'location', f + 12, (math.cos(a) * 0.05, math.sin(a) * 0.05, LV[k + 1] + 0.05))

for k, s in enumerate(stones):
    m = s.data.materials[0]
    bs = m.node_tree.nodes.get('Principled BSDF')
    if bs is None:
        continue
    es = bs.inputs.get('Emission Strength')
    ec = bs.inputs.get('Emission Color') or bs.inputs.get('Emission')
    if es is None or ec is None:
        continue
    ec.default_value = (1.0, 0.82, 0.35, 1)
    for f, v in ((0, 0.0), (520, 0.0), (532, 0.3), (600, 0.3), (612, 0.0)):
        es.default_value = v
        es.keyframe_insert('default_value', frame=f)

arm_ = M((1.0, 0.78, 0.15), rough=0.3, coat=0.4, emit=1.0)
ups = C.empty('ups', jar, (0, 0, 0))
for x in (-0.115, 0.115):
    C.tube('au', [(x, -0.02, 0.2), (x, -0.02, 0.33)], 0.008, arm_, ups)
    C.tube('al', [(x - 0.022, -0.02, 0.305), (x, -0.02, 0.335)], 0.007, arm_, ups)
    C.tube('ar', [(x + 0.022, -0.02, 0.305), (x, -0.02, 0.335)], 0.007, arm_, ups)
K(ups, 'scale', 0, (0, 0, 0))
K(ups, 'scale', 622, (0, 0, 0))
K(ups, 'scale', 632, (1, 1, 1))
K(ups, 'scale', 700, (1, 1, 1))
K(ups, 'scale', 708, (0, 0, 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.18, sz=0.13):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


label('¿SUBE?', (0.15, 0.55, 0.3), (-0.5, YC - 0.3, TOP + 1.12), 0.6, 250, 320)
label('¿IGUAL?', (0.25, 0.3, 0.85), (0.42, YC - 0.3, TOP + 1.12), 0.66, 256, 320)

W0 = ((0.0, -6.3, 1.95), (0.0, -1.6, 0.95), 29)
OP0 = ((JX + 0.02, YC - 0.32, TOP + 2.05), (JX, YC, TOP + 0.3), 30)
OP1 = ((JX + 0.02, YC - 0.36, TOP + 2.25), (JX, YC, TOP + 0.3), 30)
WQ = ((0.0, -5.7, 1.8), (0.0, -1.8, 1.1), 26)
CJ = ((JX, YC - 1.6, TOP + 0.52), (JX, YC, TOP + 0.43), 58)
CS_ = ((JX, YC - 1.5, TOP + 0.64), (JX, YC, TOP + 0.4), 58)
WP = ((0.0, -5.4, 1.75), (0.0, -1.7, 1.1), 27)
WE = ((0.0, -5.3, 1.65), (0.0, -1.7, 1.05), 24)
camkey(0, OP0)
camkey(56, OP1)
for a, b, pose in ((58, 200, W0), (202, 318, WQ), (320, 424, CJ), (426, 508, CJ), (510, 612, CS_), (614, 704, CJ), (706, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

tuki = make('tuki', 1.4)
pimo = make('pimo', 1.3)
T0 = Vector((-0.74, -1.42, Z0))
P0 = Vector((0.76, -1.36, Z0))
T.place(tuki, 0, T0)
T.turn(tuki, 0, 30)
for f in (0, 20, 40):
    T.arm(tuki, 'R', f, fwd=-150, out=10)
    T.arm(tuki, 'R', f + 10, fwd=-135, out=20)
T.arm(tuki, 'R', 84, fwd=-150, out=10)
T.rest_arm(tuki, 'R', 96)
gesture(tuki, 'hops', 50)
S(tuki, 8, (1, 1, 1))
S(tuki, 12, (1.08, 1.08, 0.88))
S(tuki, 18, (0.96, 0.96, 1.06))
S(tuki, 24, (1, 1, 1))
T.turn(tuki, 112, 15)
T.turn(tuki, 300, 35)
for side in ('L', 'R'):
    T.arm(tuki, side, 356, 0, None)
    T.arm(tuki, side, 364, fwd=-60, out=55)
    T.arm(tuki, side, 420, fwd=-60, out=55)
    T.rest_arm(tuki, side, 430)
gesture(tuki, 'bounce', 436)
T.arm(tuki, 'R', 432, 0, None)
T.arm(tuki, 'R', 440, fwd=-80, out=20)
T.arm(tuki, 'R', 496, fwd=-80, out=20)
T.rest_arm(tuki, 'R', 506)
T.turn(tuki, 512, 20)
gesture(tuki, 'sway', 640)
T.turn(tuki, 712, 40)
T.arm(tuki, 'R', 712, 0, None)
T.arm(tuki, 'R', 724, fwd=-140, out=15)
T.arm(tuki, 'R', 736, fwd=-70, out=25)
T.arm(tuki, 'R', 800, fwd=-70, out=25)
T.rest_arm(tuki, 'R', 812)
gesture(tuki, 'hops', 752)
T.turn(tuki, 790, 15)
C.wave(tuki, 'L', 812, cycles=2, period=8)

GRAB = Vector((T0.x + 0.36, T0.y - 0.34, Z0 + 0.72))
gl = (GRAB - Vector((JX, YC, TOP))) / JS
bz(712, LV[4])
K(ball, 'location', 724, (gl.x * 0.5, gl.y * 0.5, H + 0.12))
K(ball, 'location', 736, tuple(gl))
K(ball, 'location', 800, tuple(gl))
K(ball, 'location', 812, (gl.x, gl.y, gl.z - 0.05))

T.place(pimo, 0, P0)
T.turn(pimo, 0, -25)
gesture(pimo, 'breathe', 60)
S(pimo, 112, (1, 1, 1))
S(pimo, 116, (1.06, 1.06, 0.9))
S(pimo, 124, (1, 1, 1))
T.arm(pimo, 'R', 112, 0, None)
T.arm(pimo, 'R', 120, fwd=-150, out=10)
T.arm(pimo, 'R', 170, fwd=-150, out=10)
T.rest_arm(pimo, 'R', 180)
for side in ('L', 'R'):
    T.arm(pimo, side, 206, 0, None)
    T.arm(pimo, side, 214, fwd=-55, out=45)
    T.arm(pimo, side, 290, fwd=-55, out=45)
    T.rest_arm(pimo, side, 300)
T.turn(pimo, 300, -40)
for f in DROPS:
    T.arm(pimo, 'L', f - 24, 0, None)
    T.arm(pimo, 'L', f - 14, fwd=-90, out=30)
    T.arm(pimo, 'L', f - 6, fwd=-100, out=15)
    T.rest_arm(pimo, 'L', f + 2)
T.turn(pimo, 512, -25)
T.arm(pimo, 'L', 512, 0, None)
T.arm(pimo, 'L', 520, fwd=-75, out=30)
T.arm(pimo, 'L', 604, fwd=-75, out=30)
T.rest_arm(pimo, 'L', 612)
for side in ('L', 'R'):
    T.arm(pimo, side, 616, 0, None)
    T.arm(pimo, side, 626, fwd=-120, out=30)
    T.arm(pimo, side, 690, fwd=-120, out=30)
    T.rest_arm(pimo, side, 700)
gesture(pimo, 'bounce', 760)
T.turn(pimo, 760, -15)
C.wave(pimo, 'R', 816, cycles=2, period=8)
confetti(816, (0.0, YC, TOP + 0.95), n=24, spread=1.2)

T.lines(EID, LINES)
T.blinks(tuki, (44, 160, 300, 470, 580, 690, 830))
T.blinks(pimo, (70, 190, 340, 480, 630, 780))
