from stage import *
from episodes.torre_ancha_plan import *
import ep_tools as T
from mathutils import Euler
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'torre_ancha'
Z0 = 0.08
auto_dress(EID, ENV)
CY = (0.35, 0.95, 1.0)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, CY), (52, CY), (66, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (0.62, 0.95, 1.0, 1)), (52, (0.62, 0.95, 1.0, 1)), (66, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

YT = -1.85
SZ = 0.18
H = SZ / 2
SP = SZ + 0.006
XC = -0.2
XP = 0.42
mat_ = M((0.62, 0.86, 0.98), rough=0.7, coat=0.15)
C.rounded_box('mat', (0.1, YT - 0.42, Z0 + 0.006), (1.5, 1.5, 0.012), 0.2, mat_, None)
Z1 = Z0 + 0.012


def bkey(o, f, center, rot):
    e = Euler(tuple(math.radians(a) for a in rot))
    loc = Vector(center) - e.to_matrix() @ Vector((0, 0, H))
    K(o, 'location', f, tuple(loc))
    K(o, 'rotation_euler', f, tuple(e))


col = [spawn('soft_block', k % 3, 700 + k, 'candy', (XC, YT, Z1 + k * SZ), 1.0, 0) for k in range(6)]
PYR = [(XP - SP, 0), (XP, 0), (XP + SP, 0), (XP - SP / 2, 1), (XP + SP / 2, 1), (XP, 2)]
pyr = [spawn('soft_block', (k + 1) % 3, 760 + k, 'candy', (x, YT, Z1 + r * SZ), 1.0, 0) for k, (x, r) in enumerate(PYR)]


def col_pose(f, phi):
    py = YT - H if phi > 0 else YT + H
    piv = Vector((XC, py, Z1))
    m = Euler((math.radians(phi), 0, 0)).to_matrix()
    for k, o in enumerate(col):
        rel = Vector((0, YT - py, k * SZ + H))
        bkey(o, f, piv + m @ rel, (phi, 0, 0))


def pyr_pose(f, phi):
    px = XP - SP - H if phi < 0 else XP + SP + H
    piv = Vector((px, YT, Z1))
    m = Euler((0, math.radians(phi), 0)).to_matrix()
    for o, (x, r) in zip(pyr, PYR):
        rel = Vector((x - px, 0, r * SZ + H))
        bkey(o, f, piv + m @ rel, (0, phi, 0))


LAND = [(0.02, -0.27, 90, 8), (-0.05, -0.47, 180, -12), (0.06, -0.66, 90, 20), (-0.04, -0.85, 180, -6),
        (0.05, -1.04, 270, 14), (-0.03, -1.22, 180, -18)]


def col_fall(f0, fall=12, fly=14, wob=()):
    f = f0
    for a in wob:
        col_pose(f, a)
        f += 6
    col_pose(f, 0)
    for t in range(0, fall + 1, 2):
        col_pose(f + t, 25 * (t / fall) ** 2)
    fs = f + fall
    m = Euler((math.radians(25), 0, 0)).to_matrix()
    piv = Vector((XC, YT - H, Z1))
    for k, o in enumerate(col):
        c0 = piv + m @ Vector((0, H, k * SZ + H))
        lx, dy, ry, rz = LAND[k]
        c1 = Vector((XC + lx, YT + dy, Z1 + H))
        d = fly - 4 + k
        for t in range(2, d + 1, 2):
            u = t / d
            p = c0.lerp(c1, u)
            p.z = c0.z + (c1.z - c0.z) * u * u + 0.12 * u * (1 - u)
            bkey(o, fs + t, p, (25 + (ry - 25) * u, 0, rz * u))
        bkey(o, fs + d, c1, (ry, 0, rz))
        bkey(o, fs + d + 3, c1 + Vector((0, 0, 0.03)), (ry, 0, rz))
        bkey(o, fs + d + 6, c1, (ry, 0, rz))
    return fs + fly + 6


def col_rebuild(f0, step=10, d=12):
    for k, o in enumerate(col):
        lx, dy, ry, rz = LAND[k]
        c0 = Vector((XC + lx, YT + dy, Z1 + H))
        c1 = Vector((XC, YT, Z1 + k * SZ + H))
        fa = f0 + k * step
        bkey(o, fa, c0, (ry, 0, rz))
        for t in range(2, d + 1, 2):
            u = t / d
            p = c0.lerp(c1, u)
            p.z += 0.25 * 4 * u * (1 - u)
            bkey(o, fa + t, p, (ry * (1 - u), 0, rz * (1 - u)))
        bkey(o, fa + d, c1, (0, 0, 0))


col_pose(0, 0)
col_pose(10, 0)
col_fall(12, wob=(-3, 5))
col_rebuild(124)
col_pose(196, 0)
col_pose(352, 0)
col_fall(354, wob=(-4, 5, -7, 9, -6))

for o in pyr:
    o.scale = (0, 0, 0)
for k, o in enumerate(pyr):
    T.pop_in(o, 130 + k * 11, 1.0, 8)
pyr_pose(0, 0)
for f0 in (354, 708):
    for k, a in enumerate((0, 1.6, -1.8, 1.2, -0.8, 0.4, 0)):
        pyr_pose(f0 + k * 5, a)

ring_m = MA((1.0, 0.9, 0.35), 0.75, emit=0.8)
TK0 = Vector((1.05, -1.3, Z0))
MK0 = Vector((-1.08, -1.3, Z0))


def shock(f):
    e = C.empty('shock', None, (TK0.x, TK0.y, Z0 + 0.02))
    C.tube('r', [(math.cos(a / 20 * 6.2832) * 0.3, math.sin(a / 20 * 6.2832) * 0.3, 0) for a in range(21)], 0.012, ring_m, e)
    K(e, 'scale', 0, (0, 0, 0))
    K(e, 'scale', f - 1, (0, 0, 0))
    K(e, 'scale', f, (0.6, 0.6, 1))
    K(e, 'scale', f + 10, (1.8, 1.8, 1))
    K(e, 'scale', f + 12, (0, 0, 0))


for f in (12, 354, 708):
    shock(f)

yel = M((1.0, 0.58, 0.08), rough=0.3, coat=0.4, emit=1.0)
base = C.empty('base', None, (XP, YT - 0.17, Z1 + 0.004))
C.rounded_box('bar', (0, 0, 0.012), (3 * SP, 0.06, 0.028), 0.4, yel, base)
for sg in (-1, 1):
    x0 = sg * (1.5 * SP + 0.02)
    C.tube('ar', [(x0, 0, 0.02), (x0 + sg * 0.1, 0, 0.02)], 0.018, yel, base)
    C.tube('ah1', [(x0 + sg * 0.1, 0, 0.02), (x0 + sg * 0.06, 0, 0.06)], 0.016, yel, base)
    C.tube('ah2', [(x0 + sg * 0.1, 0, 0.02), (x0 + sg * 0.06, 0, -0.02)], 0.016, yel, base)
base.scale = (0, 0, 0)
T.pop_in(base, 540, 1.0, 8)
T.pop_out(base, 632, 1.0, 6)


def label(txt, rgb, loc, w, f_in, f_out, h=0.18, sz=0.13):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


label('¿ESTRECHA?', (0.85, 0.25, 0.3), (-0.44, YT - 0.3, Z0 + 1.42), 0.94, 236, 330)
label('¿ANCHA?', (0.15, 0.55, 0.3), (0.62, YT - 0.3, Z0 + 1.42), 0.7, 242, 330)

OP = ((0.3, -5.0, 0.32), (0.05, -1.6, 0.72), 26)
W = ((0.0, -6.3, 1.9), (0.0, -1.6, 0.9), 29)
WQ = ((0.0, -5.6, 1.75), (0.0, -1.7, 0.95), 27)
CJ = ((XP + 0.98, YT - 1.5, Z0 + 0.66), (XP + 0.02, YT, Z0 + 0.26), 42)
WE = ((0.0, -5.3, 1.6), (0.0, -1.65, 0.95), 25)
for a, b, pose in ((0, 58, OP), (60, 200, W), (202, 330, WQ), (332, 462, W), (464, 520, WQ), (522, 636, CJ),
                   (638, 736, W), (738, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

tuki = make('tuki', 1.4)
moki = make('moki', 1.3)
T.place(tuki, 0, TK0)
T.turn(tuki, 0, -30)
hop_to(tuki, 0, TK0, TK0, 12, 0.5)
for side in ('L', 'R'):
    T.arm(tuki, side, 22, 0, None)
    T.arm(tuki, side, 30, fwd=-40, out=70)
    T.arm(tuki, side, 80, fwd=-40, out=70)
    T.rest_arm(tuki, side, 90)
T.turn(tuki, 100, -45)
for k in range(6):
    f = 124 + k * 10
    T.arm(tuki, 'R', f, fwd=-70, out=30)
    T.arm(tuki, 'R', f + 5, fwd=-100, out=20)
T.rest_arm(tuki, 'R', 190)
T.turn(tuki, 200, -30)
for side in ('L', 'R'):
    T.arm(tuki, side, 206, 0, None)
    T.arm(tuki, side, 214, fwd=-55, out=45)
    T.arm(tuki, side, 300, fwd=-55, out=45)
    T.rest_arm(tuki, side, 310)
hop_to(tuki, 338, TK0, TK0, 16, 0.6)
T.turn(tuki, 400, -50)
for side in ('L', 'R'):
    T.arm(tuki, side, 404, 0, None)
    T.arm(tuki, side, 410, fwd=-150, out=20)
    T.arm(tuki, side, 440, fwd=-150, out=20)
    T.rest_arm(tuki, side, 450)
T.turn(tuki, 470, -25)
T.arm(tuki, 'R', 640, 0, None)
T.arm(tuki, 'R', 648, fwd=-160, out=10)
T.arm(tuki, 'R', 676, fwd=-160, out=10)
T.rest_arm(tuki, 'R', 684)
hop_to(tuki, 690, TK0, TK0, 18, 0.8)
gesture(tuki, 'hops', 744)
for side in ('L', 'R'):
    T.arm(tuki, side, 742, 0, None)
    T.arm(tuki, side, 750, fwd=-150, out=25)
    T.arm(tuki, side, 800, fwd=-150, out=25)
    T.rest_arm(tuki, side, 810)
C.wave(tuki, 'L', 820, cycles=2, period=8)

T.place(moki, 0, MK0)
T.turn(moki, 0, 30)
S(moki, 30, (1, 1, 1))
S(moki, 34, (1.06, 1.06, 0.9))
S(moki, 40, (1, 1, 1))
T.arm(moki, 'R', 96, 0, None)
T.arm(moki, 'R', 104, fwd=-150, out=10)
T.arm(moki, 'R', 124, fwd=-150, out=10)
T.turn(moki, 126, 50)
for side in ('L', 'R'):
    T.arm(moki, side, 128, 0, None)
    T.arm(moki, side, 136, fwd=-85, out=25)
    T.arm(moki, side, 190, fwd=-85, out=25)
    T.rest_arm(moki, side, 200)
for f in (134, 156, 178):
    S(moki, f, (1.03, 1.03, 0.95))
    S(moki, f + 6, (1, 1, 1))
T.turn(moki, 204, 30)
gesture(moki, 'breathe', 240)
T.turn(moki, 440, 40)
gesture(moki, 'hops', 468)
T.arm(moki, 'L', 528, 0, None)
T.arm(moki, 'L', 536, fwd=-80, out=35)
T.arm(moki, 'L', 600, fwd=-80, out=35)
T.rest_arm(moki, 'L', 610)
T.turn(moki, 640, 25)
for side in ('L', 'R'):
    T.arm(moki, side, 744, 0, None)
    T.arm(moki, side, 752, fwd=-120, out=30)
    T.arm(moki, side, 796, fwd=-120, out=30)
    T.rest_arm(moki, side, 806)
C.wave(moki, 'R', 814, cycles=2, period=8)
confetti(744, (XP, YT, Z0 + 0.9), n=24, spread=1.2)

T.lines(EID, LINES)
T.blinks(tuki, (44, 160, 300, 470, 580, 690, 830))
T.blinks(moki, (70, 190, 340, 480, 630, 780))
