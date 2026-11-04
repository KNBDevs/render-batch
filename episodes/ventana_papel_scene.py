from stage import *
from episodes.ventana_papel_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'ventana_papel'
Z0 = 0.08
auto_dress(EID, ENV)
NIGHT = (0.3, 0.42, 1.0)
LV = ((0, 0.22), (60, 0.22), (76, 0.75), (300, 0.75), (330, 0.38), (690, 0.38), (720, 0.85))
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, k in LV:
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
    for f, c in ((0, NIGHT), (60, NIGHT), (76, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0, s0 = tuple(bg[0].default_value), bg[1].default_value
for f, c, v in ((0, (0.08, 0.1, 0.32, 1), 0.3), (60, (0.08, 0.1, 0.32, 1), 0.3), (76, b0, s0 * 0.8), (300, b0, s0 * 0.8),
                (330, b0, s0 * 0.45), (690, b0, s0 * 0.45), (720, b0, s0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)
    bg[1].default_value = v
    bg[1].keyframe_insert('default_value', frame=f)
sky = bpy.data.materials.get('Sky')
if sky:
    se = sky.node_tree.nodes['Emission'].inputs[1]
    s1 = se.default_value
    for f, k in LV:
        se.default_value = s1 * k
        se.keyframe_insert('default_value', frame=f)

HX, HY = 0.05, -1.62
HW, HD, HH = 1.15, 0.75, 0.72
HS = 1.25
house = C.empty('cardboard_house', None, (HX, HY, Z0))
house.scale = (HS, HS, HS)
CB = M((0.78, 0.56, 0.34), rough=0.7, coat=0.15)
CB2 = M((0.66, 0.45, 0.26), rough=0.7, coat=0.15)
TRIM = M((0.98, 0.62, 0.72), rough=0.4, coat=0.6)
TRIM2 = M((0.55, 0.78, 1.0), rough=0.4, coat=0.6)
C.rounded_box('body', (0, 0, HH / 2), (HW, HD, HH), 0.06, CB, house)
for sx in (-1, 1):
    r = C.empty('roof', house, (sx * HW * 0.25, 0, HH + 0.15), (0, math.radians(sx * 32), 0))
    C.rounded_box('slab', (0, 0, 0), (HW * 0.6, HD + 0.14, 0.06), 0.3, CB2, r)
C.tube('ridge', [(-0.02, -(HD + 0.14) / 2, HH + 0.33), (-0.02, (HD + 0.14) / 2, HH + 0.33)], 0.03, TRIM, house)
C.rounded_box('chimney', (HW * 0.28, 0.05, HH + 0.32), (0.16, 0.16, 0.24), 0.3, CB2, house)
C.tube('chim_rim', [(HW * 0.28 + 0.09 * math.cos(k * 6.2832 / 24), 0.05 + 0.09 * math.sin(k * 6.2832 / 24), HH + 0.44) for k in range(25)], 0.016, TRIM2, house)
C.rounded_box('door', (0, -HD / 2 - 0.005, 0.17), (0.2, 0.02, 0.3), 0.4, CB2, house)
C.sphere('knob', (0.06, -HD / 2 - 0.02, 0.17), (0.02, 0.012, 0.02), TRIM2, house, 12)
FY = -HD / 2 - 0.012
WZ = 0.47
WS = 0.26
WXP, WXC = -0.32, 0.32


def frame(x, m):
    q = WS / 2 + 0.02
    C.tube('wframe', [(x - q, FY - 0.006, WZ - q), (x + q, FY - 0.006, WZ - q), (x + q, FY - 0.006, WZ + q), (x - q, FY - 0.006, WZ + q), (x - q, FY - 0.006, WZ - q)], 0.022, m, house)
    C.tube('wbar', [(x, FY - 0.008, WZ - q), (x, FY - 0.008, WZ + q)], 0.012, m, house)
    C.tube('wbar', [(x - q, FY - 0.008, WZ), (x + q, FY - 0.008, WZ)], 0.012, m, house)


def pane(name, x, rgb, f_on, emit_hi):
    m = C.mat(name, rgb, rough=0.6, coat=0.2, emit=0.0001)
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Emission Color'].default_value = (1.0, 0.85, 0.5, 1)
    es = p.inputs['Emission Strength']
    for f, v in ((0, 0.0), (f_on, 0.0), (f_on + 8, emit_hi)):
        es.default_value = v
        es.keyframe_insert('default_value', frame=f)
    o = C.empty('pane_' + name, house, (x, FY + 0.004, WZ))
    C.rounded_box('pn', (0, 0, 0), (WS, 0.012, WS), 0.2, m, o)
    return o


ON = 360
paper = pane('paper', WXP, (0.97, 0.95, 0.88), ON, 1.1)
card = pane('card', WXC, (0.6, 0.4, 0.22), ON, 0.0)
paper2 = pane('paper2', WXC, (0.97, 0.95, 0.88), ON, 1.1)
frame(WXP, TRIM)
frame(WXC, TRIM2)
K(paper2, 'scale', 0, (0, 0, 0))
K(paper2, 'scale', 727, (0, 0, 0))
T.pop_in(paper2, 728, 1.0, 8)
T.pop_out(card, 722, 1.0, 6)

HALO = MA((1.0, 0.8, 0.4), 0.1, rough=0.2, emit=0.25)


def glow(x, f_on):
    g = C.empty('halo', None, (HX + x * HS, HY + FY * HS - 0.12, Z0 + WZ * HS))
    C.sphere('h', (0, 0, 0), (WS * 0.75 * HS, 0.004, WS * 0.75 * HS), HALO, g, 32)
    K(g, 'scale', 0, (0, 0, 0))
    K(g, 'scale', f_on, (0, 0, 0))
    K(g, 'scale', f_on + 10, (1, 1, 1))
    for f in range(f_on + 24, TOTAL, 24):
        K(g, 'scale', f, (1.06, 1, 1.06) if (f // 24) % 2 else (1, 1, 1))
    bpy.ops.object.light_add(type='AREA', location=(HX + x * HS, HY + FY * HS - 0.05, Z0 + WZ * HS))
    al = bpy.context.object
    al.rotation_euler = (math.radians(-90), 0, 0)
    al.data.size = WS * HS
    al.data.color = (1.0, 0.82, 0.5)
    for f, v in ((0, 0), (f_on, 0), (f_on + 8, 20)):
        al.data.energy = v
        al.data.keyframe_insert('energy', frame=f)


glow(WXP, ON)
glow(WXC, 730)

torch = spawn('toy_torch', 1, 3311, 'candy', (0, 0, 0), 1.3, 0)
beam = next(o for o in torch.children_recursive if o.name.startswith('beam'))
TP0 = Vector((1.05, -2.3, Z0 + 0.05))
CHM = Vector((HX + HW * 0.28 * HS, HY + 0.05 * HS, Z0 + HH * HS + 1.0))
K(torch, 'location', 0, tuple(TP0))
K(torch, 'rotation_euler', 0, (0, 0, math.radians(160)))
K(beam, 'scale', 0, (0.001, 0.001, 0.001))
for i in range(0, 9):
    u = i / 8
    p = TP0 + (CHM - TP0) * u + Vector((0, 0, 0.5 * math.sin(math.pi * u)))
    K(torch, 'location', 118 + round(u * 22), tuple(p))
K(torch, 'rotation_euler', 140, (0, math.radians(90), math.radians(90)))
K(torch, 'location', 156, tuple(CHM - Vector((0, 0, 0.55))))
K(torch, 'scale', 150, (1.3, 1.3, 1.3))
K(torch, 'scale', 158, (0.001, 0.001, 0.001))
spark = C.empty('spark', None, tuple(CHM - Vector((0, 0, 0.42))))
C.sphere('s', (0, 0, 0), (0.07, 0.07, 0.07), M((1.0, 0.9, 0.5), rough=0.2, emit=3.0), spark, 16)
K(spark, 'scale', 0, (0, 0, 0))
K(spark, 'scale', ON - 1, (0, 0, 0))
K(spark, 'scale', ON + 4, (1.4, 1.4, 1.4))
K(spark, 'scale', ON + 14, (0, 0, 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


PC = (0.85, 0.45, 0.1)
CC = (0.45, 0.28, 0.12)
LZ = Z0 + HH * HS + 0.75
label('¿PAPEL?', PC, (HX + WXP * HS - 0.15, HY - 0.75, LZ), 0.9, 226, 344)
label('¿CARTÓN?', CC, (HX + WXC * HS + 0.15, HY - 0.75, LZ + 0.32), 1.05, 232, 344)
label('PAPEL', PC, (HX + WXP - 0.1, HY - 0.6, LZ), 0.78, 566, 680)
label('CARTÓN', CC, (HX + WXC + 0.12, HY - 0.6, LZ + 0.32), 0.95, 570, 680)

OP = ((-0.62, -3.75, 1.0), (-0.45, -1.9, 0.68), 28)
OP2 = ((-0.58, -3.65, 0.98), (-0.4, -1.9, 0.66), 29)
W = ((0.05, -5.0, 1.9), (0.05, -1.6, 0.8), 21)
WQ = ((0.05, -4.85, 1.9), (0.05, -1.6, 0.92), 21)
CSN = ((HX, -4.0, 1.0), (HX, HY, Z0 + WZ * HS + 0.05), 26)
CH = ((HX + WXP * HS - 0.1, HY - 1.75, Z0 + WZ * HS + 0.15), (HX + WXP * HS - 0.1, HY, Z0 + WZ * HS), 30)
CH2 = ((HX + WXC * HS + 0.12, HY - 1.75, Z0 + WZ * HS + 0.15), (HX + WXC * HS + 0.12, HY, Z0 + WZ * HS), 30)
WE = ((0.05, -4.7, 1.8), (0.05, -1.6, 0.8), 21)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 190, W), (192, 350, WQ), (352, 414, CSN), (416, 472, CH), (474, 552, CH2),
                   (554, 686, WQ), (688, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

luma = make('luma', 1.3)
bol = make('bolita', 1.15)
LM0 = Vector((-1.12, -1.7, Z0))
BL0 = Vector((1.18, -1.55, Z0))
T.place(luma, 0, Vector((-0.95, -2.3, Z0)))
T.turn(luma, 0, 30)
for side in ('L', 'R'):
    T.arm(luma, side, 8, 0, None)
    T.arm(luma, side, 14, fwd=-100, out=40)
    T.arm(luma, side, 50, fwd=-100, out=40)
    T.rest_arm(luma, side, 60)
hop_to(luma, 62, Vector((-0.95, -2.3, Z0)), LM0, 12, 0.25)
T.turn(luma, 80, 25)
T.arm(luma, 'R', 198, 0, None)
T.arm(luma, 'R', 204, fwd=-150, out=25)
T.arm(luma, 'R', 244, fwd=-150, out=25)
T.rest_arm(luma, 'R', 254)
T.turn(luma, 300, 45)
T.turn(luma, 478, 35)
T.arm(luma, 'R', 480, 0, None)
T.arm(luma, 'R', 486, fwd=-80, out=40)
T.arm(luma, 'R', 530, fwd=-80, out=40)
T.rest_arm(luma, 'R', 540)
LM1 = Vector((-1.05, -1.78, Z0))
hop_to(luma, 694, LM0, LM1, 12, 0.3)
T.arm(luma, 'R', 708, 0, None)
T.arm(luma, 'R', 714, fwd=-110, out=10)
T.arm(luma, 'R', 736, fwd=-110, out=10)
T.rest_arm(luma, 'R', 746)
gesture(luma, 'hops', 760)
C.wave(luma, 'L', 826, cycles=2, period=8)

T.place(bol, 0, BL0)
T.turn(bol, 0, -35)
T.arm(bol, 'L', 98, 0, None)
T.arm(bol, 'L', 104, fwd=-150, out=30)
T.arm(bol, 'L', 136, fwd=-150, out=30)
T.rest_arm(bol, 'L', 146)
gesture(bol, 'hops', 120)
T.turn(bol, 300, -45)
for side in ('L', 'R'):
    T.arm(bol, side, 422, 0, None)
    T.arm(bol, side, 428, fwd=-150, out=25)
    T.arm(bol, side, 470, fwd=-150, out=25)
    T.rest_arm(bol, side, 480)
gesture(bol, 'hops', 430)
T.turn(bol, 560, -25)
gesture(bol, 'breathe', 566)
T.turn(bol, 720, -40)
C.wave(bol, 'R', 820, cycles=2, period=8)
confetti(762, (HX, HY, Z0 + HH + 0.9), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(luma, (44, 150, 300, 460, 590, 700, 840))
T.blinks(bol, (70, 190, 330, 500, 650, 790))
