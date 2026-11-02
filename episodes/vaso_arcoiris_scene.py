from stage import *
from episodes.vaso_arcoiris_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
from props.costumes import flat
EID = 'vaso_arcoiris'
Z0 = 0.08
auto_dress(EID, ENV)

GOLD = (1.0, 0.72, 0.4)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    e = l.energy
    for f, c in ((0, GOLD), (50, GOLD), (66, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
    for f, v in ((0, 1.0), (226, 1.0), (240, 0.7), (370, 0.7), (384, 1.0)):
        l.energy = e * v
        l.keyframe_insert('energy', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (1.0, 0.66, 0.38, 1)), (50, (1.0, 0.66, 0.38, 1)), (66, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)


def vis(o, keys):
    for f, on in keys:
        o.scale = (1, 1, 1) if on else (0, 0, 0)
        o.keyframe_insert('scale', frame=f)


YC = -2.0
spawn('low_table', 0, 7311, 'fresh', (0.0, YC, Z0), 1.0, 0)
TOP = Z0 + 0.62
CS = 1.6
GY = -1.86
SY = -2.18
GZ = TOP + 0.2
WY = -0.6

cream = M((0.98, 0.95, 0.88), rough=0.8, coat=0.1)
wallm = M((0.96, 0.66, 0.56), rough=0.85, coat=0.05)
frame_m = M((0.45, 0.82, 0.72), rough=0.4, coat=0.6)
pink = M((1.0, 0.56, 0.68), rough=0.4, coat=0.6)
sky = M((0.3, 0.62, 1.0), rough=0.5, coat=0.1, emit=0.35)
sun_m = M((1.0, 0.86, 0.3), rough=0.4, coat=0.2, emit=2.5)
cloud_m = M((1.0, 1.0, 1.0), rough=0.7, coat=0.1, emit=0.6)
beam_m = MA((1.0, 0.88, 0.45), 0.7, rough=0.2, emit=2.2)
spot_m = M((1.0, 0.82, 0.35), rough=0.6, coat=0.0, emit=0.5)
RB = [(0.95, 0.08, 0.1), (1.0, 0.42, 0.02), (1.0, 0.85, 0.02), (0.08, 0.7, 0.15), (0.05, 0.3, 0.95), (0.42, 0.12, 0.85)]
rb_m = [M(c, rough=0.6, coat=0.0, emit=0.6) for c in RB]

WZ = GZ + (GZ - TOP - 0.006) / (GY - SY) * (WY - GY)
wall = C.empty('pared', None, (0, -0.42, 0))
C.rounded_box('wall', (0, 0, 1.2), (2.1, 0.1, 2.4), 0.04, wallm, wall)
C.rounded_box('skirt', (0, -0.06, Z0 + 0.06), (2.1, 0.04, 0.12), 0.02, pink, wall)
win = C.empty('ventana', None, (0, WY + 0.12, WZ))
WW, WH = 1.12, 0.78
C.rounded_box('pane', (0, 0.02, 0), (WW, 0.02, WH), 0.01, sky, win)
for z in (-WH / 2, WH / 2):
    C.rounded_box('fh', (0, -0.02, z), (WW + 0.1, 0.07, 0.07), 0.03, frame_m, win)
for x in (-WW / 2, 0.0, WW / 2):
    C.rounded_box('fv', (x, -0.02, 0), (0.07, 0.07, WH + 0.1), 0.03, frame_m, win)
C.rounded_box('sill', (0, -0.08, -WH / 2 - 0.06), (WW + 0.24, 0.16, 0.05), 0.02, pink, win)
C.sphere('sun', (0.0, 0.0, 0.2), (0.11, 0.01, 0.11), sun_m, win, 32)
for k in range(8):
    a = k * math.pi / 4
    C.tube('sr', [(math.cos(a) * 0.14, 0.0, 0.2 + math.sin(a) * 0.14), (math.cos(a) * 0.19, 0.0, 0.2 + math.sin(a) * 0.19)], 0.012, sun_m, win)
cloud = C.empty('nube', win, (-0.75, -0.03, 0.2))
for dx, dz, r in ((0, 0, 0.11), (-0.1, -0.02, 0.08), (0.1, -0.02, 0.085), (0.04, 0.06, 0.08)):
    C.sphere('c', (dx, 0, dz), (r, 0.015, r * 0.8), cloud_m, cloud, 24)
for f, x in ((0, -0.75), (226, -0.75), (240, 0.0), (370, 0.0), (384, 0.75)):
    K(cloud, 'location', f, (x, -0.03, 0.2))
K(cloud, 'scale', 0, (0, 0, 0))
K(cloud, 'scale', 224, (0, 0, 0))
K(cloud, 'scale', 226, (1, 1, 1))
K(cloud, 'scale', 384, (1, 1, 1))
K(cloud, 'scale', 386, (0, 0, 0))

cups = {}
for side, x in (('L', -0.3), ('R', 0.3)):
    spawn('coaster', 0, 515 + (side == 'R'), 'candy', (x, GY, TOP), 0.95, 0)
    cup = spawn('clear_cup', 1, 3901, 'candy', (x, GY, TOP + 0.024), CS, 0)
    piv = next(o for o in cup.children if o.name.startswith('water_pivot'))
    for o in piv.children:
        o.data.materials.clear()
        o.data.materials.append(MA((0.4, 0.72, 1.0), 0.3, rough=0.04, emit=0.06))
    cups[side] = (cup, piv, x)
    C.rounded_box('sheet', (x, SY, TOP + 0.003), (0.44, 0.28, 0.006), 0.2, cream, None)
FILL = 0.75
cR, pR, _ = cups['R']
pR.scale = (1, 1, FILL)
cL, pL, _ = cups['L']
T.pop_in(cL, 212, 1.0, 8)
for f, v in ((0, 0.001), (738, 0.001), (762, FILL)):
    pL.scale = (1, 1, v)
    pL.keyframe_insert('scale', frame=f)


def beam(x):
    wp = Vector((x, WY, WZ))
    gp = Vector((x, GY, GZ))
    sp = Vector((x, SY, TOP + 0.008))
    a = C.empty('beam_in', None, (0, 0, 0))
    C.tube('b', [tuple(wp), tuple(gp)], 0.03, beam_m, a)
    w = C.empty('beam_out', None, (0, 0, 0))
    C.tube('b', [tuple(gp), tuple(sp)], 0.024, beam_m, w)
    spot = C.empty('spot', None, (x, SY, TOP + 0.008))
    C.sphere('s', (0, 0, 0), (0.1, 0.075, 0.002), spot_m, spot, 32)
    rb = C.empty('rainbow', None, (x, SY, TOP + 0.008))
    n = len(RB)
    for k, m in enumerate(rb_m):
        u = k - (n - 1) / 2
        o = C.rounded_box('band', (u * 0.056, -0.012 * abs(u), 0), (0.054, 0.22, 0.003), 0.3, m, rb)
        o.rotation_euler = (0, 0, math.radians(-u * 5))
    fan = C.empty('fan', None, (0, 0, 0))
    for k, m in enumerate(rb_m):
        u = k - (n - 1) / 2
        C.tube('fr', [tuple(gp), (x + u * 0.056, SY - 0.02, TOP + 0.012)], 0.009, m, fan)
    return a, w, spot, rb, fan


aR, wR, sR, rR, fR = beam(0.3)
aL, wL, sL, rL, fL = beam(-0.3)
vis(aR, ((0, 1), (226, 1), (228, 0), (384, 0), (386, 1)))
vis(wR, ((0, 0),))
vis(sR, ((0, 0),))
vis(rR, ((0, 1), (226, 1), (228, 0), (384, 0), (386, 1)))
vis(fR, ((0, 0), (504, 0), (510, 1), (712, 1), (716, 0)))
vis(aL, ((0, 0), (384, 0), (386, 1)))
vis(wL, ((0, 0), (384, 0), (386, 1), (760, 1), (762, 0)))
vis(sL, ((0, 0), (384, 0), (386, 1), (760, 1), (762, 0)))
vis(rL, ((0, 0), (760, 0), (764, 1)))
vis(fL, ((0, 0),))

PJ0 = Vector((-0.6, -1.8, TOP))
jug = spawn('pitcher', 1, 9071, 'candy', tuple(PJ0), 1.15, 0)
PJ1 = Vector((-0.5, GY, TOP + 0.5))
K(jug, 'location', 0, tuple(PJ0))
K(jug, 'location', 716, tuple(PJ0))
K(jug, 'location', 732, tuple(PJ1))
K(jug, 'location', 768, tuple(PJ1))
K(jug, 'location', 786, tuple(PJ0))
K(jug, 'rotation_euler', 0, (0, 0, 0))
K(jug, 'rotation_euler', 732, (0, 0, 0))
K(jug, 'rotation_euler', 742, (0, math.radians(72), 0))
K(jug, 'rotation_euler', 760, (0, math.radians(72), 0))
K(jug, 'rotation_euler', 770, (0, 0, 0))
stream = C.empty('chorro', None, (0, 0, 0))
C.tube('st', [(-0.33, GY, TOP + 0.47), (-0.31, GY, TOP + 0.36), (-0.3, GY, TOP + 0.2)], 0.014, MA((0.45, 0.75, 1.0), 0.55, rough=0.05, emit=0.2), stream)
vis(stream, ((0, 0), (740, 0), (742, 1), (760, 1), (762, 0)))


def label(txt, rgb, loc, w, f_in, f_out, h=0.16, sz=0.11):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


label('¿VACÍO?', (0.85, 0.3, 0.45), (-0.36, -2.05, TOP + 0.66), 0.6, 300, 384)
label('¿CON AGUA?', (0.15, 0.45, 0.85), (0.38, -2.05, TOP + 0.66), 0.74, 306, 384)

OP = ((0.3, -2.85, 1.38), (0.3, -2.1, 0.74), 30)
W0 = ((0.0, -6.4, 1.9), (0.0, -1.3, 1.12), 27)
MS = ((0.0, -5.3, 1.75), (0.0, -1.5, 1.05), 26)
CS_ = ((0.0, -3.55, 2.15), (0.0, -1.98, 0.74), 30)
SD = ((0.0, -4.5, 1.5), (0.05, -1.9, 0.95), 28)
WE = ((0.0, -4.9, 1.65), (-0.1, -1.55, 1.0), 26)
camkey(0, OP)
camkey(54, OP)
for a, b, pose in ((56, 176, W0), (178, 380, MS), (382, 498, CS_), (500, 604, SD), (606, 712, CS_), (714, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

bol = make('bolita', 1.2)
pimo = make('pimo', 1.3)
B0 = Vector((-0.95, -1.45, Z0))
P0 = Vector((0.95, -1.45, Z0))
T.place(bol, 0, B0)
T.turn(bol, 0, 25)
T.place(pimo, 0, P0)
T.turn(pimo, 0, -25)

S(bol, 6, (1, 1, 1))
S(bol, 10, (1.08, 1.08, 0.88))
S(bol, 16, (0.95, 0.95, 1.08))
S(bol, 22, (1, 1, 1))
for side in ('L', 'R'):
    T.arm(bol, side, 8, 0, None)
    T.arm(bol, side, 16, fwd=-150, out=30)
    T.arm(bol, side, 56, fwd=-150, out=30)
    T.rest_arm(bol, side, 66)
gesture(pimo, 'breathe', 30)
T.turn(pimo, 84, -5)
T.arm(pimo, 'R', 88, 0, None)
T.arm(pimo, 'R', 96, fwd=-150, out=10)
T.arm(pimo, 'R', 150, fwd=-150, out=10)
T.rest_arm(pimo, 'R', 160)
T.turn(pimo, 164, -30)
gesture(bol, 'sway', 168)
T.arm(bol, 'R', 172, 0, None)
T.arm(bol, 'R', 180, fwd=-80, out=20)
T.arm(bol, 'R', 226, fwd=-80, out=20)
T.rest_arm(bol, 'R', 236)
T.arm(pimo, 'L', 196, 0, None)
T.arm(pimo, 'L', 204, fwd=-95, out=20)
T.arm(pimo, 'L', 222, fwd=-95, out=20)
T.rest_arm(pimo, 'L', 232)
for side in ('L', 'R'):
    T.arm(pimo, side, 252, 0, None)
    T.arm(pimo, side, 260, fwd=-40, out=65)
    T.arm(pimo, side, 330, fwd=-40, out=65)
    T.rest_arm(pimo, side, 340)
T.turn(bol, 250, 35)
T.turn(bol, 386, 30)
gesture(bol, 'hops', 404)
for side in ('L', 'R'):
    T.arm(bol, side, 402, 0, None)
    T.arm(bol, side, 410, fwd=-140, out=25)
    T.arm(bol, side, 448, fwd=-140, out=25)
    T.rest_arm(bol, side, 458)
T.turn(pimo, 496, -20)
T.arm(pimo, 'R', 500, 0, None)
T.arm(pimo, 'R', 508, fwd=-90, out=25)
T.arm(pimo, 'R', 580, fwd=-90, out=25)
T.rest_arm(pimo, 'R', 590)
for side in ('L', 'R'):
    T.arm(pimo, side, 600, 0, None)
    T.arm(pimo, side, 608, fwd=-60, out=55)
    T.arm(pimo, side, 676, fwd=-60, out=55)
    T.rest_arm(pimo, side, 686)
gesture(bol, 'breathe', 520)
T.turn(bol, 708, 15)
T.arm(bol, 'R', 712, 0, None)
T.arm(bol, 'R', 722, fwd=-90, out=10)
T.arm(bol, 'R', 766, fwd=-90, out=10)
T.rest_arm(bol, 'R', 778)
gesture(bol, 'bounce', 780)
for side in ('L', 'R'):
    T.arm(bol, side, 784, 0, None)
    T.arm(bol, side, 792, fwd=-150, out=25)
    T.arm(bol, side, 826, fwd=-150, out=25)
    T.rest_arm(bol, side, 836)
T.turn(pimo, 770, -30)
gesture(pimo, 'hops', 796)
C.wave(pimo, 'R', 830, cycles=2, period=8)
confetti(812, (0.0, -2.0, TOP + 0.9), n=22, spread=1.1)

T.lines(EID, LINES)
T.blinks(bol, (60, 200, 360, 480, 620, 740, 840))
T.blinks(pimo, (70, 180, 320, 470, 590, 700, 820))
