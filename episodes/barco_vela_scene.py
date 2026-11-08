from stage import *
from episodes.barco_vela_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph, boat_rig
EID = 'barco_vela'
Z0 = 0.08
auto_dress(EID, ENV)
PINK = (1.0, 0.55, 0.78)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, PINK, 0.9), (58, PINK, 0.9), (74, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.85, 0.4, 0.62, 1)), (58, (0.85, 0.4, 0.62, 1)), (74, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

CX, TY = 0.05, -1.45
L, Wd, H = 1.5, 0.8, 0.5
WZ = Z0 + H - 0.05
can = C.empty('water_canal', None, (CX, TY, Z0))
WALL = M((0.98, 0.7, 0.45), rough=0.4, coat=0.7)
TRIM = M((0.55, 0.8, 1.0), rough=0.35, coat=0.8)
for y in (-Wd / 2, Wd / 2):
    C.rounded_box('wall', (0, y, H / 2 + 0.06), (L, 0.06, H - 0.12), 0.3, WALL, can)
    C.tube('rim', [(-L / 2, y, H), (L / 2, y, H)], 0.035, TRIM, can)
for x in (-L / 2, L / 2):
    C.rounded_box('end', (x, 0, H / 2 + 0.06), (0.06, Wd + 0.06, H - 0.12), 0.3, WALL, can)
    C.tube('rim', [(x, -Wd / 2, H), (x, Wd / 2, H)], 0.035, TRIM, can)
C.rounded_box('floor', (0, 0, 0.1), (L, Wd, 0.06), 0.2, WALL, can)
for x in (-L / 2 + 0.12, L / 2 - 0.12):
    for y in (-Wd / 2 + 0.06, Wd / 2 - 0.06):
        C.sphere('foot', (x, y, 0.04), (0.07, 0.07, 0.05), TRIM, can, 16)
C.rounded_box('water', (0, 0, (0.13 + H - 0.05) / 2), (L - 0.04, Wd - 0.04, H - 0.05 - 0.13), 0.05, MA((0.3, 0.62, 1.0), 0.75, rough=0.06, emit=0.15), can)
FL = [M((1.0, 0.45, 0.5), rough=0.35, coat=0.7), M((1.0, 0.95, 0.9), rough=0.35, coat=0.7)]
for k in range(13):
    x = -L / 2 + 0.1 + k * (L - 0.2) / 12
    C.sphere('float', (x, 0, H - 0.04), (0.035, 0.035, 0.03), FL[k % 2], can, 14)
C.tube('rope', [(-L / 2 + 0.05, 0, H - 0.04), (L / 2 - 0.05, 0, H - 0.04)], 0.008, FL[1], can)
GOAL = []
for y in (-Wd / 2, Wd / 2):
    C.tube('post', [(L / 2 - 0.12, y, H), (L / 2 - 0.12, y, H + 0.36)], 0.02, TRIM, can)
    fl = C.empty('flag', can, (L / 2 - 0.12, y, H + 0.32))
    for i in range(3):
        for j in range(2):
            C.rounded_box('chk', (0.025 + i * 0.05, 0, -j * 0.05), (0.05, 0.012, 0.05), 0.1, M((0.15, 0.2, 0.4) if (i + j) % 2 else (1, 1, 1), rough=0.4, coat=0.5), fl)
    GOAL.append(fl)

BS = 1.0
X0, X1 = CX - L / 2 + 0.32, CX + L / 2 - 0.34
YS, YN = TY + 0.2, TY - 0.2
sail = spawn('toy_sailboat', 0, 6201, (0.4, 0.75, 1.0), (X0, YS, WZ - 0.03), BS, 0)
bare = spawn('toy_sailboat', 1, 6202, (1.0, 0.75, 0.3), (X0, YN, WZ - 0.03), BS, 0)
brig = next(o for o in bare.children if o.name.startswith('rig'))
SAILM = M((1.0, 0.42, 0.35), rough=0.55, coat=0.2)
for bt in (sail, bare):
    rg = next(o for o in bt.children if o.name.startswith('rig'))
    for o in rg.children_recursive:
        if o.type == 'MESH' and not o.name.startswith(('mast', 'cap')):
            o.data.materials.clear()
            o.data.materials.append(SAILM)
K(brig, 'scale', 0, (0, 0, 0))
K(brig, 'scale', 728, (0, 0, 0))
K(brig, 'scale', 736, (1.15, 1.15, 1.15))
K(brig, 'scale', 742, (1, 1, 1))
K(sail, 'scale', 0, (0, 0, 0))
K(sail, 'scale', 126, (0, 0, 0))
K(sail, 'scale', 134, (BS * 1.1,) * 3)
K(sail, 'scale', 140, (BS,) * 3)


def glide(o, y, f0, f1, xa, xb, bob=True):
    n = max(2, (f1 - f0) // 4)
    for i in range(n + 1):
        u = i / n
        e = u * u * (3 - 2 * u)
        f = f0 + round((f1 - f0) * u)
        K(o, 'location', f, (xa + (xb - xa) * e, y, WZ - 0.03 + (0.008 * math.sin(f * 0.5) if bob else 0)))
        K(o, 'rotation_euler', f, (math.radians(3 * math.sin(f * 0.4)), 0, 0))


glide(bare, YN, 0, 60, X0, X0)
glide(bare, YN, 330, 560, X0, X0 + 0.08)
glide(bare, YN, 560, 744, X0 + 0.08, X0 + 0.08)
glide(bare, YN, 748, 800, X0 + 0.08, X1)
glide(bare, YN, 800, TOTAL - 1, X1, X1)
glide(sail, YS, 140, 344, X0, X0)
glide(sail, YS, 348, 470, X0, X1)
glide(sail, YS, 470, TOTAL - 1, X1, X1)
for fl in GOAL:
    for f0 in (470, 800):
        for d, a in ((0, 0), (4, 14), (8, -14), (12, 10), (16, 0)):
            K(fl, 'rotation_euler', f0 + d, (0, 0, math.radians(a)))

FP = Vector((CX - L / 2 - 0.12, TY - 0.05, WZ + 0.1))
fan = spawn('hand_fan', 0, 6203, 'candy', tuple(FP), 1.0, 0)
FB = (math.radians(0), math.radians(-70), math.radians(90))
T.pop_in(fan, 180, 1.0, 8)
K(fan, 'rotation_euler', 0, FB)


def fanning(f0, f1):
    for f in range(f0, f1, 6):
        s = 1 if (f - f0) // 6 % 2 else -1
        K(fan, 'rotation_euler', f, (math.radians(s * 22), FB[1], FB[2]))
    K(fan, 'rotation_euler', f1, FB)


fanning(336, 470)
fanning(560, 640)
fanning(744, 800)
WM = MA((1.0, 1.0, 1.0), 0.55, emit=0.6)
rnd = random.Random(6204)


def gusts(f0, f1, xb, y0, y1):
    for k in range(4):
        g = C.empty('gust', None, (0, 0, 0))
        r = 0.05
        pts = [(math.cos(a) * r * 2.4, 0, math.sin(a) * r) for a in [i * 0.4 for i in range(12)]]
        C.tube('g', pts, 0.008, WM, g)
        K(g, 'scale', 0, (0, 0, 0))
        y = y0 + (y1 - y0) * k / 3
        for c, fs in enumerate(range(f0 + k * 6, f1 - 20, 24)):
            K(g, 'scale', fs - 1, (0, 0, 0))
            K(g, 'location', fs, (FP.x + 0.15, y, WZ + 0.12 + 0.06 * (k % 2)))
            K(g, 'scale', fs, (1, 1, 1))
            K(g, 'location', fs + 20, (xb, y, WZ + 0.14 + 0.06 * (k % 2)))
            K(g, 'scale', fs + 20, (1, 1, 1))
            K(g, 'scale', fs + 21, (0, 0, 0))


gusts(340, 476, X1 - 0.1, YN, YS)
gusts(560, 646, X1 - 0.2, YS - 0.05, YS + 0.05)
gusts(746, 806, X1 - 0.2, YN - 0.05, YN + 0.05)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, RC = (0.05, 0.42, 0.15), (0.75, 0.08, 0.15)
label('¿CON VELA?', GC, (-0.5, TY - 0.5, Z0 + 1.6), 0.72, 276, 396, 0.22, 0.12)
label('¿SIN VELA?', RC, (0.28, TY - 0.5, Z0 + 1.6), 0.72, 282, 396, 0.22, 0.12)
label('VIENTO', (0.05, 0.2, 0.7), (-0.3, TY - 0.6, WZ - 0.2), 0.8, 566, 684, 0.24, 0.17)
label('¡EMPUJA!', RC, (0.42, TY - 0.6, WZ - 0.2), 0.95, 580, 684, 0.24, 0.17)

OP = ((X0 + 0.35, -2.7, 1.85), (X0 + 0.4, TY + 0.15, 0.85), 24)
OP2 = ((X0 + 0.35, -2.8, 1.88), (X0 + 0.4, TY + 0.15, 0.87), 24)
W = ((-0.12, -3.45, 2.15), (-0.12, -1.2, 0.98), 20)
WQ = ((-0.12, -3.6, 2.3), (-0.12, -1.2, 1.03), 20)
CB = ((-0.05, -3.2, 1.95), (-0.05, TY + 0.1, 0.85), 20)
CL = ((-0.12, -3.4, 2.1), (-0.12, TY + 0.15, 0.95), 20)
WE = ((-0.12, -3.5, 2.2), (-0.12, -1.2, 1.0), 20)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 240, W), (242, 396, WQ), (398, 552, CB), (554, 692, CL), (694, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

moki = make('moki', 1.25)
bopi = make('bopi', 1.2)
MK = Vector((0.42, -0.6, Z0))
BP = Vector((-0.72, -0.85, Z0))
T.place(moki, 0, MK)
T.turn(moki, 0, -10)
T.place(bopi, 0, BP)
T.turn(bopi, 0, 25)
T.arm(moki, 'R', 12, fwd=-70, out=50)
T.arm(moki, 'R', 56, fwd=-70, out=50)
T.rest_arm(moki, 'R', 66)
T.place(moki, 700, MK)
T.place(moki, 716, MK + Vector((-0.05, -0.05, 0)))
T.arm(moki, 'R', 718, 0, None)
T.arm(moki, 'R', 726, fwd=-95, out=40)
T.arm(moki, 'R', 740, fwd=-95, out=40)
T.rest_arm(moki, 'R', 750)
T.arm(bopi, 'R', 120, 0, None)
T.arm(bopi, 'R', 128, fwd=-90, out=40)
T.arm(bopi, 'R', 144, fwd=-90, out=40)
T.rest_arm(bopi, 'R', 152)
for f0, f1 in ((176, 470), (556, 640), (742, 800)):
    T.arm(bopi, 'R', f0, 0, None)
    T.arm(bopi, 'R', f0 + 6, fwd=-80, out=55)
    T.arm(bopi, 'R', f1, fwd=-80, out=55)
    T.rest_arm(bopi, 'R', f1 + 8)
gesture(moki, 'hops', 476)
gesture(bopi, 'breathe', 600)
gesture(moki, 'hops', 796)
gesture(bopi, 'hops', 812)
C.wave(moki, 'L', 826, cycles=2, period=8)
C.wave(bopi, 'L', 826, cycles=2, period=8)
confetti(806, (X1, TY, Z0 + 1.8), n=20, spread=1.0)

T.lines(EID, LINES)
T.blinks(moki, (44, 150, 300, 460, 590, 700, 840))
T.blinks(bopi, (70, 190, 330, 500, 650, 790))
