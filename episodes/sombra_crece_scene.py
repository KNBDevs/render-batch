from stage import *
from episodes.sombra_crece_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, glyph
from props.costumes import flat, star_pts
EID = 'sombra_crece'
Z0 = 0.08
auto_dress(EID, ENV)

NIGHT = (0.1, 0.13, 0.3, 1)
for l in list(bpy.data.lights):
    e = l.energy
    for f, v in ((0, 0.08), (50, 0.08), (68, 0.8), (TOTAL, 0.8)):
        l.energy = e * v
        l.keyframe_insert('energy', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, NIGHT), (50, NIGHT), (68, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

HL = Z0 + 0.62
SC = Vector((0.35, 0.0, HL))
LP = Vector((-0.35, -1.35, HL))
DIR = SC - LP
YAW = math.atan2(-DIR.x, DIR.y)
RS = 0.12

mint = M((0.45, 0.85, 0.72), rough=0.4, coat=0.6)
pink = M((1.0, 0.55, 0.68), rough=0.4, coat=0.6)
cream = M((0.97, 0.94, 0.86), rough=0.85, coat=0.1)
pool_m = M((1.0, 0.86, 0.55), rough=0.8, coat=0.0, emit=1.0)
shade = M((0.2, 0.17, 0.32), rough=0.95, coat=0.0)
glow = M((1.0, 0.9, 0.6), rough=0.3, coat=0.0, emit=3.0)
star_m = M((1.0, 0.8, 0.12), rough=0.35, coat=0.6)
ink = M((0.15, 0.08, 0.05), rough=0.5)
ray_m = M((1.0, 0.85, 0.3), rough=0.3, coat=0.3, emit=1.6)

SW, SH = 1.6, 1.32
scr = C.empty('pantalla', None, (SC.x, SC.y, 0), (0, 0, YAW))
C.rounded_box('pane', (0, 0, HL), (SW, 0.012, SH), 0.004, cream, scr)
for x in (-SW / 2 - 0.03, SW / 2 + 0.03):
    C.rounded_box('post', (x, 0, (HL + SH / 2 + 0.06) / 2), (0.07, 0.07, HL + SH / 2 + 0.06), 0.03, mint, scr)
    C.rounded_box('foot', (x, 0, Z0 + 0.03), (0.14, 0.36, 0.06), 0.03, mint, scr)
    C.sphere('knob', (x, 0, HL + SH / 2 + 0.11), (0.06, 0.06, 0.06), pink, scr, 24)
C.rounded_box('top', (0, 0, HL + SH / 2 + 0.04), (SW + 0.1, 0.06, 0.06), 0.025, pink, scr)
C.rounded_box('bot', (0, 0, HL - SH / 2 - 0.03), (SW + 0.1, 0.06, 0.05), 0.02, pink, scr)
C.sphere('pool', (0, -0.009, HL), (0.7, 0.002, 0.64), pool_m, scr, 48)
shd = C.empty('sombra', scr, (0, -0.016, HL))
flat('sombra_m', star_pts(RS), 0.003, shade, shd, bevel=0)

lamp = C.empty('linterna', None, (LP.x, LP.y, 0), (0, 0, YAW))
C.rounded_box('ped', (0, 0, (Z0 + HL - 0.1) / 2), (0.16, 0.16, HL - 0.1 - Z0), 0.06, pink, lamp)
C.rounded_box('pbase', (0, 0, Z0 + 0.03), (0.32, 0.32, 0.06), 0.03, pink, lamp)
C.rounded_box('head', (0, -0.02, HL), (0.24, 0.2, 0.2), 0.07, mint, lamp)
C.sphere('lens', (0, 0.085, HL), (0.075, 0.018, 0.075), glow, lamp, 32)
C.tube('handle', [(-0.07, -0.02, HL + 0.1), (0, -0.02, HL + 0.16), (0.07, -0.02, HL + 0.1)], 0.014, pink, lamp)

rail = C.empty('rail', None, (0, 0, 0))
U = DIR.normalized()
N_ = Vector((-U.y, U.x, 0))
for s in (-1, 1):
    a = LP + U * 0.2 + N_ * 0.05 * s
    b = LP + U * 1.3 + N_ * 0.05 * s
    C.tube('r', [(a.x, a.y, Z0 + 0.012), (b.x, b.y, Z0 + 0.012)], 0.012, mint, rail)
for k in range(6):
    p = LP + U * (0.25 + 0.2 * k)
    C.rounded_box('sl', (p.x, p.y, Z0 + 0.006), (0.16, 0.035, 0.012), 0.005, pink, rail).rotation_euler = (0, 0, YAW)

cart = C.empty('cart', None, (0, 0, 0), (0, 0, YAW))
C.rounded_box('cbase', (0, 0, Z0 + 0.04), (0.16, 0.12, 0.05), 0.02, pink, cart)
C.tube('stick', [(0, 0, Z0 + 0.06), (0, 0, HL - RS * 0.8)], 0.01, M((0.62, 0.44, 0.28), rough=0.5), cart)
star = C.empty('star', cart, (0, 0, HL))
flat('star_m', star_pts(RS), 0.03, star_m, star, bevel=0.008)
for sx in (-1, 1):
    C.sphere('eye', (sx * 0.02, -0.018, 0.008), (0.008, 0.004, 0.011), ink, star, 12)
C.tube('smile', [(-0.014, -0.017, -0.012), (0, -0.017, -0.019), (0.014, -0.017, -0.012)], 0.003, ink, star)

rays = C.empty('rayos', None, tuple(LP), (0, 0, 0))
ray_objs = []
for k in range(2):
    e = C.empty('ray', rays, (0, 0, 0))
    C.tube('rt', [(0.0, 0, 0), (1.0, 0, 0)], 0.01, ray_m, e)
    ray_objs.append(e)

TK = [(0, 0.22), (360, 0.22), (420, 0.8), (520, 0.8), (560, 0.24), (620, 0.24), (662, 0.8), (700, 0.8), (740, 0.22), (TOTAL, 0.22)]


def t_at(f):
    for (f0, a), (f1, b) in zip(TK, TK[1:]):
        if f0 <= f <= f1:
            u = (f - f0) / max(1, f1 - f0)
            u = u * u * (3 - 2 * u)
            return a + (b - a) * u
    return TK[-1][1]


RAY_ON = (480, 712)
for f in range(0, TOTAL + 1, 2):
    t = t_at(f)
    p = LP + DIR * t
    K(cart, 'location', f, (p.x, p.y, 0))
    sc_ = 1.0 / t
    K(shd, 'scale', f, (sc_, 1, sc_))
    for k, s in enumerate((1, -1)):
        tip = SC + Vector((0, 0, s * RS * sc_))
        d = tip - LP
        q = d.normalized().to_track_quat('X', 'Z')
        on = RAY_ON[0] <= f <= RAY_ON[1]
        K(ray_objs[k], 'rotation_euler', f, tuple(q.to_euler()))
        K(ray_objs[k], 'scale', f, (d.length, 1, 1) if on else (0, 0, 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.18, sz=0.13):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


label('¿GRANDE?', (0.15, 0.45, 0.85), (-0.55, -1.0, 1.85), 0.8, 300, 334)
label('¿PEQUEÑA?', (0.85, 0.3, 0.45), (0.6, -1.0, 1.85), 0.86, 306, 336)

OP = ((-0.05, -2.55, 1.02), (0.5, 0.0, 0.8), 22)
W0 = ((0.08, -4.3, 1.5), (0.08, -0.5, 1.02), 22)
MS = ((0.06, -4.2, 1.45), (0.06, -0.5, 1.0), 22)
CS = ((0.06, -3.9, 2.2), (0.06, -0.45, 0.86), 23)
WE = ((0.08, -4.2, 1.45), (0.08, -0.5, 1.0), 22)
camkey(0, OP)
camkey(54, OP)
for a, b, pose in ((56, 176, W0), (178, 340, MS), (342, 498, CS), (500, 604, W0), (606, 698, CS), (700, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

luma = make('luma', 1.25)
tuki = make('tuki', 1.2)
L0 = Vector((-1.0, -0.6, Z0))
U0 = Vector((1.15, -0.62, Z0))
T.place(luma, 0, L0)
T.turn(luma, 0, 25)
T.place(tuki, 0, U0)
T.turn(tuki, 0, -15)

S(tuki, 6, (1, 1, 1))
S(tuki, 10, (1.08, 1.08, 0.88))
S(tuki, 16, (0.95, 0.95, 1.08))
S(tuki, 22, (1, 1, 1))
for side in ('L', 'R'):
    T.arm(tuki, side, 8, 0, None)
    T.arm(tuki, side, 16, fwd=-150, out=30)
    T.arm(tuki, side, 52, fwd=-150, out=30)
    T.rest_arm(tuki, side, 64)
gesture(luma, 'breathe', 40)
T.arm(luma, 'R', 90, 0, None)
T.arm(luma, 'R', 98, fwd=-70, out=40)
T.arm(luma, 'R', 160, fwd=-70, out=40)
T.rest_arm(luma, 'R', 170)
T.turn(tuki, 176, -35)
T.arm(tuki, 'R', 180, 0, None)
T.arm(tuki, 'R', 188, fwd=-80, out=20)
T.arm(tuki, 'R', 236, fwd=-80, out=20)
T.rest_arm(tuki, 'R', 246)
gesture(tuki, 'sway', 250)
T.turn(luma, 256, 10)
for side in ('L', 'R'):
    T.arm(luma, side, 262, 0, None)
    T.arm(luma, side, 270, fwd=-40, out=65)
    T.arm(luma, side, 330, fwd=-40, out=65)
    T.rest_arm(luma, side, 340)
T.turn(luma, 346, 45)
for a, b in ((350, 424), (548, 566), (612, 666), (700, 744)):
    T.arm(luma, 'R', a, 0, None)
    T.arm(luma, 'R', a + 8, fwd=-85, out=10)
    T.arm(luma, 'R', b, fwd=-85, out=10)
    T.rest_arm(luma, 'R', b + 10)
T.turn(luma, 440, 20)
gesture(tuki, 'hops', 432)
for side in ('L', 'R'):
    T.arm(tuki, side, 430, 0, None)
    T.arm(tuki, side, 438, fwd=-140, out=25)
    T.arm(tuki, side, 470, fwd=-140, out=25)
    T.rest_arm(tuki, side, 480)
T.arm(luma, 'L', 512, 0, None)
T.arm(luma, 'L', 520, fwd=-120, out=30)
T.arm(luma, 'L', 540, fwd=-120, out=30)
T.rest_arm(luma, 'L', 548)
T.turn(tuki, 600, -50)
T.turn(tuki, 726, -40)
gesture(tuki, 'bounce', 742)
C.wave(tuki, 'R', 776, cycles=3, period=8)
T.turn(luma, 760, 20)
C.wave(luma, 'L', 800, cycles=2, period=8)
confetti(790, (0.35, -0.3, HL + 0.75), n=22, spread=1.1)

T.lines(EID, LINES)
T.blinks(luma, (60, 200, 360, 480, 600, 700, 830))
T.blinks(tuki, (70, 150, 300, 420, 560, 690, 820))
