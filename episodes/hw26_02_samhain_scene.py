from stage import *
from episodes.hw26_02_samhain_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props.costumes import dress
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_02_samhain'
Z0 = 0.08
autumn()
auto_dress(EID, ENV)

W0 = ((0, -6.3, 1.75), (0, -1.15, 0.98), 32)
WC = ((0.0, -4.6, 1.55), (0.0, -1.3, 1.08), 40)
camkey(0, W0)
camkey(150, W0)
camkey(164, WC)
camkey(400, WC)
camkey(408, WC)
WT = ((0.0, -5.4, 1.85), (0.0, -1.3, 1.22), 33)
camkey(418, WT)
camkey(632, WT)
camkey(644, W0)
camkey(TOTAL - 1, W0)

TY = -1.55
table = spawn('low_table', 0, 2602, 'autumn', (0, TY, Z0), 0.9, 0)
TOP = Z0 + 0.62 * 0.9
font = _font()

pimo = make('pimo', 1.3)
ruki = make('ruki', 1.35)
dress(pimo, 'pimo', COSTUME, 0)
dress(ruki, 'ruki', COSTUME, 0)
PP = Vector((-0.82, -0.95, Z0))
RP = Vector((0.82, -0.95, Z0))
T.place(pimo, 0, PP)
T.place(ruki, 0, RP)
T.turn(pimo, 0, 35)
T.turn(ruki, 0, -40)


def top_z(ch):
    bpy.context.view_layer.update()
    z = 0.0
    for o in ch['root'].children_recursive:
        if o.type == 'MESH':
            for c in o.bound_box:
                z = max(z, (o.matrix_world @ Vector(c)).z)
    return z


alb = HW.album('alb', (0.0, TY - 0.08, TOP), w=0.46, h=0.32, rot=(0, 0, 0))
lid = alb['lid']
K(lid, 'rotation_euler', 0, (0, 0, 0))
K(lid, 'rotation_euler', 14, (0, 0, 0))
K(lid, 'rotation_euler', 30, (0, math.radians(180), 0))
T.arm(ruki, 'L', 6, fwd=-55, out=25)
T.rest_arm(ruki, 'L', 32)

HZ = top_z(ruki)
leaf = HW.autumn_leaf('bigleaf', (0, 0, 0), 0.2, rgb=(0.86, 0.42, 0.12))
L0 = Vector((RP.x - 0.5, RP.y + 0.1, 2.6))
LH = Vector((RP.x + 0.03, RP.y - 0.06, HZ - 0.07))
for k, t in enumerate(range(0, 41, 4)):
    u = t / 40
    p = L0.lerp(LH, u)
    p.x += 0.18 * math.sin(u * 3 * math.pi) * (1 - u)
    K(leaf, 'location', t, tuple(p))
    K(leaf, 'rotation_euler', t, (math.radians(55 * u + 25 * math.sin(u * 9) * (1 - u)), math.radians(-25 * u + 30 * math.sin(u * 7) * (1 - u)), 0))
K(leaf, 'location', 44, tuple(LH))
K(leaf, 'rotation_euler', 44, (math.radians(55), math.radians(-25), 0))
S(ruki, 40, (1, 1, 1))
S(ruki, 44, (1.05, 1.05, 0.94))
S(ruki, 52, (1, 1, 1))
T.turn(pimo, 30, 45)
gesture(pimo, 'hops', 18)
T.turn(ruki, 46, -20)

IR = HW.card('c_ir', 'Irlanda', font, (-0.3, TY + 0.02, TOP + 0.72), w=0.5, h=0.16, bg=(0.51, 0.58, 0.52), ink=(1.0, 0.95, 0.85))
T.pop_in(IR, 170, 1.0, 10)
SAM = HW.card('c_sam', 'Samhain', font, (-0.3, TY + 0.02, TOP + 0.5), w=0.5, h=0.16, bg=(0.91, 0.87, 0.81), ink=(0.2, 0.12, 0.24))
T.pop_in(SAM, 236, 1.0, 10)
bask = HW.harvest_basket('bask', (-0.3, TY - 0.03, TOP), h=0.24)
T.pop_in(bask, 196, 1.0, 10)

dial = spawn('season_dial', 0, 2611, 'autumn', (0.2, TY + 0.02, TOP), 1.15, 0)
needle = next(o for o in dial.children if o.name.startswith('dial_needle'))
T.pop_in(dial, 206, 1.15, 10)
K(needle, 'rotation_euler', 0, (0, math.radians(-30), 0))
K(needle, 'rotation_euler', 262, (0, math.radians(-30), 0))
K(needle, 'rotation_euler', 300, (0, math.radians(70), 0))
K(needle, 'rotation_euler', 306, (0, math.radians(62), 0))
K(needle, 'rotation_euler', 312, (0, math.radians(66), 0))
T.turn(ruki, 250, -40)
T.arm(ruki, 'L', 256, fwd=-60, out=35)
T.rest_arm(ruki, 'L', 320)
for o in (IR, SAM):
    T.pop_out(o, 404, 1.0, 8)
T.pop_out(bask, 408, 1.0, 8)
T.pop_out(dial, 408, 1.15, 8)
K(bask, 'scale', 640, (0, 0, 0))
K(bask, 'scale', 646, (1.15, 1.15, 1.15))
K(bask, 'scale', 650, (1, 1, 1))
K(dial, 'scale', 640, (0, 0, 0))
K(dial, 'scale', 646, (1.3, 1.3, 1.3))
K(dial, 'scale', 650, (1.15, 1.15, 1.15))

HWC = HW.card('c_hw', 'Halloween', font, (-0.09, TY + 0.04, TOP + 1.06), w=0.5, h=0.15, bg=(0.75, 0.46, 0.27), ink=(1.0, 0.95, 0.85))
tiles = []
for k, (kind, x, z) in enumerate((('leaf', -0.36, 0.62), ('apple', -0.09, 0.7), ('lantern', 0.18, 0.62))):
    g = C.empty(f'tile{k}', None, (x, TY + 0.04, TOP + z))
    C.rounded_box(f'tileb{k}', (0, 0.012, 0), (0.17, 0.02, 0.17), 0.02, M((0.96, 0.93, 0.86), rough=0.6, coat=0.2), g)
    if kind == 'lantern':
        HW.turnip_lantern(f'tl{k}', (0, -0.01, -0.06), h=0.11, parent=g)
    else:
        HW.pictogram(f'pic{k}', kind, (0, -0.005, 0), s=0.05, parent=g)
    tiles.append(g)
    T.pop_in(g, 428 + k * 14, 1.5, 8)
dots = []
for k, g in enumerate(tiles):
    a = Vector(g.location)
    b = Vector((-0.09, TY + 0.03, TOP + 1.06))
    for j in range(3):
        u = (j + 1) / 4
        d = C.empty(f'dot{k}{j}', None, tuple(a.lerp(b, u) + Vector((0, 0, 0.06 if k != 1 else 0.0))))
        C.sphere(f'dots{k}{j}', (0, 0, 0), (0.016,) * 3, M((0.4, 0.32, 0.44), rough=0.4, coat=0.5), d, 12)
        T.pop_in(d, 480 + k * 6 + j * 3, 1.0, 6)
        dots.append(d)
T.pop_in(HWC, 512, 1.0, 10)
for o in dots + [HWC]:
    T.pop_out(o, 640, 1.0, 8)
for o in tiles:
    T.pop_out(o, 640, 1.5, 8)
for f, a in ((430, 20), (444, 0), (458, -20), (520, 0)):
    T.turn(pimo, f, 35 + a * 0.5)
gesture(ruki, 'breathe', 470)
gesture(pimo, 'breathe', 540)

T.turn(ruki, 650, -70)
T.arm(ruki, 'L', 650, fwd=-150, out=10)
LB = Vector((bask.location.x, bask.location.y, TOP + 0.2))
mid = Vector(((LH.x + LB.x) / 2, LH.y - 0.15, HZ + 0.25))
for t in range(0, 25, 3):
    u = t / 24
    p = (LH * (1 - u) * (1 - u)) + (mid * 2 * u * (1 - u)) + (LB * u * u)
    K(leaf, 'location', 654 + t, tuple(p))
    K(leaf, 'rotation_euler', 654 + t, (math.radians(55 - 10 * u), math.radians(-25 + 200 * u), 0))
K(leaf, 'location', 682, tuple(LB))
T.rest_arm(ruki, 'L', 684)
T.turn(ruki, 690, -40)
leaf2 = HW.autumn_leaf('leaf2', (0, 0, 0), 0.15, rgb=(0.8, 0.55, 0.15))
K(leaf2, 'scale', 0, (0, 0, 0))
K(leaf2, 'scale', 663, (0, 0, 0))
K(leaf2, 'scale', 664, (1, 1, 1))
M0 = Vector((0.1, TY - 0.1, 2.3))
M1 = Vector((0.1, TY - 0.12, TOP + 0.01))
K(leaf2, 'location', 0, tuple(M0))
for t in range(0, 37, 4):
    u = t / 36
    p = M0.lerp(M1, u)
    p.x += 0.15 * math.sin(u * 3 * math.pi) * (1 - u)
    K(leaf2, 'location', 664 + t, tuple(p))
    K(leaf2, 'rotation_euler', 664 + t, (math.radians(90 * u + 30 * math.sin(u * 8) * (1 - u)), 0, math.radians(40 * u)))
K(leaf2, 'location', 702, tuple(M1))
T.turn(ruki, 700, -25)
T.arm(ruki, 'L', 700, fwd=-50, out=40)
T.rest_arm(ruki, 'L', 730)
T.arm(ruki, 'L', 740, fwd=-60, out=20)
LB2 = LB + Vector((0.05, 0.02, 0.01))
for t in range(0, 19, 3):
    u = t / 18
    p = M1.lerp(LB2, u)
    p.z += 0.3 * 4 * u * (1 - u)
    K(leaf2, 'location', 744 + t, tuple(p))
K(leaf2, 'location', 764, tuple(LB2))
T.rest_arm(ruki, 'L', 768)
T.turn(ruki, 770, -40)

scarf = C.empty('scarf', None, (0.2, TY - 0.06, TOP + 0.9))
sm = M((0.4, 0.32, 0.44), rough=0.55, coat=0.2)
stripe = M((0.91, 0.74, 0.47), rough=0.55, coat=0.2)
pts = [(-0.11 + 0.22 * k / 10, 0, 0.02 * math.sin(k * 0.6)) for k in range(11)]
C.tube('scarf_band', pts, 0.028, sm, scarf)
for sx in (-0.07, 0.06):
    C.tube(f'scarf_tail{sx}', [(sx, 0, 0), (sx + 0.01, 0, -0.08), (sx + 0.02, 0, -0.14)], 0.026, sm, scarf)
    C.tube(f'scarf_str{sx}', [(sx + 0.005, -0.02, -0.09), (sx + 0.018, -0.02, -0.1)], 0.02, stripe, scarf)
T.pop_in(scarf, 790, 1.4, 10)
T.turn(pimo, 796, 20)
gesture(pimo, 'sway', 830)
gesture(ruki, 'sway', 836)
C.wave(pimo, 'R', 870, cycles=2, period=8)
C.wave(ruki, 'L', 874, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(pimo, (40, 150, 260, 380, 500, 610, 720, 860))
T.blinks(ruki, (70, 190, 310, 430, 560, 690, 800))
