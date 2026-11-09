from stage import *
from episodes.lupa_mariquita_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'lupa_mariquita'
Z0 = 0.08
auto_dress(EID, ENV)
GRN = (0.62, 1.0, 0.5)
for l in list(bpy.data.lights):
    e = l.energy * 0.4
    for f, c, k in ((0, GRN, 0.6), (58, GRN, 0.6), (74, (1.0, 0.96, 0.88), 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
for f, c, s in ((0, (0.16, 0.36, 0.14, 1), 0.14), (58, (0.16, 0.36, 0.14, 1), 0.14), (74, tuple(bg[0].default_value), 0.2)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)
    bg[1].default_value = s
    bg[1].keyframe_insert('default_value', frame=f)
bpy.data.materials['Sky'].node_tree.nodes['Emission'].inputs[1].default_value = 0.3

TX, TY = 0.0, -1.45
spawn('low_table', 0, 6201, 'pastel', (TX, TY, Z0), 1.0, 0)
TOP = Z0 + 0.62
LX = 0.02

POT = M((0.96, 0.62, 0.45), rough=0.4, coat=0.6)
LEAF = M((0.36, 0.72, 0.3), rough=0.45, coat=0.5)
RIB = M((0.62, 0.88, 0.45), rough=0.45, coat=0.5)
pot = C.empty('leaf_pot', None, (LX, TY + 0.05, TOP))
C.lathe('pot', [(0.0, 0.0), (0.09, 0.0), (0.11, 0.02), (0.13, 0.15), (0.145, 0.16), (0.145, 0.185), (0.12, 0.19), (0.0, 0.19)], POT, pot, segs=48)
C.sphere('soil', (0, 0, 0.18), (0.12, 0.12, 0.02), M((0.45, 0.3, 0.22), rough=0.8), pot, 24)
for k, y in enumerate((-0.03, 0.03)):
    C.sphere('band', (0, 0, 0.09 + k * 0.03), (0.125 + k * 0.004, 0.125 + k * 0.004, 0.006), M((1.0, 0.9, 0.55), rough=0.4, coat=0.6), pot, 32)
C.tube('stem', [(0, 0, 0.18), (0.0, -0.01, 0.3), (0.0, -0.03, 0.38)], 0.014, LEAF, pot)
leaf = C.empty('leaf', pot, (0, -0.04, 0.42), (math.radians(62), 0, 0))
C.sphere('blade', (0, 0, 0), (0.17, 0.24, 0.016), LEAF, leaf, 40)
C.tube('rib', [(0, -0.22, 0.014), (0, 0.22, 0.014)], 0.007, RIB, leaf)
for sy in (-0.1, 0.0, 0.1):
    for sx in (-1, 1):
        C.tube('vein', [(0, sy, 0.013), (sx * 0.1, sy + 0.08, 0.012)], 0.004, RIB, leaf)

RED = M((0.92, 0.12, 0.1), rough=0.25, coat=0.9)
BLK = M((0.08, 0.07, 0.08), rough=0.35, coat=0.6)
WHT = M((1.0, 1.0, 1.0), rough=0.3, emit=0.2)
SPOTS = [(0.0, 0.62), (-0.42, 0.25), (0.42, 0.25), (-0.5, -0.25), (0.5, -0.25), (-0.26, -0.6), (0.26, -0.6)]


def ladybug(name, parent, loc, R, rot=(0, 0, 0)):
    o = C.empty(name, parent, loc, rot)
    C.sphere('shell', (0, 0, 0), (R, R * 1.15, R * 0.62), RED, o, 32)
    C.tube('seam', [(0, -R * 1.1, R * 0.5), (0, R * 0.45, R * 0.66)], R * 0.035, BLK, o)
    for sx, sy in SPOTS:
        z = R * 0.62 * math.sqrt(max(0.05, 1 - sx * sx - sy * sy * 0.75))
        C.sphere('spot', (sx * R, sy * R * 1.15, z), (R * 0.17, R * 0.17, R * 0.06), BLK, o, 14)
    C.sphere('head', (0, R * 1.08, R * 0.12), (R * 0.52, R * 0.4, R * 0.4), BLK, o, 24)
    for sx in (-1, 1):
        C.sphere('eye', (sx * R * 0.22, R * 1.38, R * 0.22), (R * 0.12, R * 0.08, R * 0.12), WHT, o, 12)
        C.tube('ant', [(sx * R * 0.15, R * 1.3, R * 0.4), (sx * R * 0.4, R * 1.7, R * 0.8)], R * 0.035, BLK, o)
        C.sphere('tip', (sx * R * 0.4, R * 1.7, R * 0.8), (R * 0.07, R * 0.07, R * 0.07), BLK, o, 10)
    return o


bug = ladybug('ladybug', leaf, (0.0, 0.02, 0.02), 0.045)
BUGW = Vector((LX, TY + 0.002, TOP + 0.447))
for f, yaw in ((0, 0), (300, 0), (330, 20), (360, -10), (390, 0)):
    K(bug, 'rotation_euler', f, (0, 0, math.radians(yaw)))

LS = 1.35
LR = 0.17 * LS
lupa = spawn('magnifier', 0, 6202, 'candy', (0, 0, 0), LS, 0)
lupa.rotation_euler = (0, math.radians(-90), 0)
for o in lupa.children_recursive:
    if o.type == 'MESH' and o.data.materials and o.data.materials[0].name.startswith('pa'):
        o.visible_shadow = False
lens_c = Vector((-0.42 * LS, 0, 0))
L_ON = BUGW + Vector((0, -0.2, 0.0)) - lens_c
L_OFF = Vector((0.42, TY - 0.32, TOP + 0.5)) - lens_c
L_HID = L_OFF

view = C.empty('view', lupa, (0, 0.03, 0.42), (0, math.radians(90), 0))
C.sphere('vleaf', (0, 0.012, 0), (0.16, 0.004, 0.16), LEAF, view, 40)
C.tube('vrib', [(0.0, 0.006, -0.16), (0.0, 0.006, 0.16)], 0.006, RIB, view)
big = ladybug('bigbug', view, (0, 0, 0), 0.09, (math.radians(90), 0, 0))
big.location = (0, -0.02, -0.02)

K(lupa, 'location', 0, tuple(L_OFF))
K(lupa, 'scale', 0, (0, 0, 0))
K(lupa, 'scale', 108, (0, 0, 0))
K(lupa, 'scale', 116, (LS, LS, LS))


def move(f0, f1, a, b):
    K(lupa, 'location', f0, tuple(a))
    K(lupa, 'location', f1, tuple(b))


def magn(f, on):
    v = 1.0 if on else 0.0
    K(view, 'scale', f, (v, v, v))
    set_interp(view, 'CONSTANT')


magn(0, False)
move(386, 398, L_OFF, L_ON)
magn(399, True)
magn(619, False)
move(620, 632, L_ON, L_OFF)
move(744, 754, L_OFF, L_ON)
magn(755, True)
for f, rz in ((420, 0), (440, 5), (460, -5), (480, 0), (800, 0), (812, 6), (824, -6), (836, 0)):
    K(big, 'rotation_euler', f, (math.radians(90), 0, math.radians(rz)))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, RC, BC = (0.05, 0.42, 0.15), (0.75, 0.08, 0.15), (0.1, 0.3, 0.75)
label('¿GRANDE?', GC, (-0.44, TY - 0.55, Z0 + 1.6), 0.94, 276, 396)
label('¿PEQUEÑA?', RC, (0.46, TY - 0.55, Z0 + 1.6), 1.0, 282, 396)
label('¡GRANDE!', GC, (-0.22, TY - 0.5, TOP + 0.85), 0.86, 566, 618, 0.24, 0.17)
label('SIN LUPA', RC, (-0.2, TY - 0.5, TOP + 0.85), 0.9, 640, 744, 0.24, 0.17)
label('¡CON LUPA!', BC, (-0.22, TY - 0.5, TOP + 0.85), 0.98, 760, 840, 0.24, 0.17)

OP = ((-0.26, -2.95, 1.42), (-0.24, TY, 1.16), 22)
OP2 = ((-0.26, -3.05, 1.45), (-0.24, TY, 1.16), 21.5)
W = ((0.04, -4.0, 1.55), (0.04, -1.25, 1.0), 21)
WQ = ((0.02, -4.2, 1.75), (0.02, -1.25, 1.05), 21)
CB = ((LX + 0.02, -3.0, 1.22), (LX + 0.02, TY, 1.06), 21)
CL = ((0.04, -3.7, 1.38), (0.04, TY, 1.02), 21)
WE = ((0.04, -4.05, 1.6), (0.04, -1.25, 1.02), 21)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 240, W), (242, 396, WQ), (398, 552, CB), (554, 692, CL), (694, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

moki = make('moki', 1.4)
luma = make('luma', 1.3)
spawn('play_step', 0, 6203, 'fresh', (-0.66, -0.78, Z0), 1.1, 0)
MK = Vector((-0.66, -0.82, Z0 + 0.235 * 1.1))
LM = Vector((0.95, -1.1, Z0))
T.place(moki, 0, MK)
T.turn(moki, 0, 20)
T.place(luma, 0, LM)
T.turn(luma, 0, -35)
T.place(moki, 0, MK + Vector((0.12, -0.05, 0)))
T.place(moki, 56, MK + Vector((0.12, -0.05, 0)))
T.place(moki, 70, MK)
for f0 in (100, 380, 612, 738):
    T.arm(luma, 'R', f0, 0, None)
    T.arm(luma, 'R', f0 + 6, fwd=-95, out=35)
    T.arm(luma, 'R', f0 + 18, fwd=-95, out=35)
    T.rest_arm(luma, 'R', f0 + 26)
for f0 in (14, 486, 704, 760):
    T.arm(moki, 'L', f0, 0, None)
    T.arm(moki, 'L', f0 + 6, fwd=-70, out=45)
    T.arm(moki, 'L', f0 + 22, fwd=-70, out=45)
    T.rest_arm(moki, 'L', f0 + 30)
gesture(moki, 'hops', 414)
gesture(luma, 'breathe', 560)
gesture(moki, 'hops', 794)
gesture(luma, 'hops', 796)
C.wave(moki, 'R', 826, cycles=2, period=8)
C.wave(luma, 'L', 826, cycles=2, period=8)
confetti(806, (0.1, TY, Z0 + 2.0), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(moki, (44, 150, 300, 460, 590, 700, 840))
T.blinks(luma, (70, 190, 330, 500, 650, 790))
