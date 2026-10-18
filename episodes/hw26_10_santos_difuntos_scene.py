from stage import *
from episodes.hw26_10_santos_difuntos_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props import halloween as HW
EID = 'hw26_10_santos_difuntos'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -6.3, 1.75), (0, -1.0, 0.95), 32)
WC = ((0, -5.0, 1.5), (0, -0.9, 0.9), 28)
camkey(0, W0)
camkey(160, W0)
camkey(176, WC)
camkey(880, WC)
camkey(896, W0)
camkey(TOTAL - 1, W0)

TB = Vector((0, -0.9, Z0))
TS = 0.8
spawn('low_table', 0, 1010, 'pastel', tuple(TB), TS, 0)
TZ = TB.z + 0.62 * TS
RY = TB.y - 0.1
spawn('calendar_rail', 0, 1011, 'pastel', (0, RY, TZ), 1.0, 0)
CZ = TZ + 0.06
CS = 0.9
ca = spawn('date_card', 0, 1012, (0.95, 0.75, 0.4), (0, RY - 0.04, CZ), CS, 0, label=('1', 'NOV'))
cb = spawn('date_card', 0, 1013, (0.62, 0.55, 0.78), (0, RY + 0.03, CZ + 0.05), CS, 0, label=('2', 'NOV'))
AX, BX = -0.27, 0.27
T.pop_in(cb, 6, CS, 10)
K(ca, 'location', 0, (0, RY - 0.04, CZ + 0.6))
K(ca, 'scale', 0, (0, 0, 0))
K(ca, 'scale', 22, (0, 0, 0))
K(ca, 'scale', 26, (CS,) * 3)
K(ca, 'location', 24, (0, RY - 0.04, CZ + 0.6))
K(ca, 'location', 38, (0, RY - 0.04, CZ))
K(ca, 'location', 186, (0, RY - 0.04, CZ))
K(ca, 'location', 210, (AX, RY - 0.01, CZ))
K(cb, 'location', 186, (0, RY + 0.03, CZ + 0.05))
K(cb, 'location', 214, (BX, RY - 0.01, CZ))


def glow(name, x, rgb, f0, f1):
    g = C.empty(name, None, (x, RY + 0.08, CZ + 0.2 * CS))
    C.sphere(name + '.disc', (0, 0, 0), (0.3, 0.01, 0.3), M(rgb, rough=0.6, coat=0.0, emit=0.9), g, 40)
    for f, v in ((0, 0), (f0, 0), (f0 + 16, 1), (f1, 1), (f1 + 16, 0.55)):
        K(g, 'scale', f, (v, v, v))
    return g


glow('glowA', AX, (1.0, 0.88, 0.6), 220, 470)
glow('glowB', BX, (0.86, 0.8, 0.98), 500, 740)

la = HW.card('lab_a', 'Todos los Santos', _font(), (AX - 0.08, RY - 0.3, 1.42), w=0.86, h=0.17, bg=(0.98, 0.82, 0.5), ink=(0.15, 0.2, 0.26), rot=(math.radians(-6), 0, 0))
lb = HW.card('lab_b', 'Fieles Difuntos', _font(), (BX + 0.08, RY - 0.3, 1.19), w=0.82, h=0.17, bg=(0.4, 0.27, 0.45), ink=(1.0, 0.9, 0.7), rot=(math.radians(-6), 0, 0))
T.pop_in(la, 236, 1.0, 12)
T.pop_in(lb, 516, 1.0, 12)
T.pop_out(la, 884, 1.0, 10)
T.pop_out(lb, 884, 1.0, 10)

b1 = HW.bouquet('ramo1', (BX + 0.3, RY + 0.22, TZ), h=0.24, cols=((0.95, 0.92, 0.88), (0.86, 0.78, 0.95), (0.95, 0.75, 0.8)))
T.pop_in(b1, 560, 0.8, 14)

pimo = make('pimo', 1.2)
ruki = make('ruki', 1.2)
PP = Vector((-1.0, -0.6, Z0))
RP = Vector((1.0, -0.62, Z0))
T.place(pimo, 0, PP)
T.place(ruki, 0, RP)
T.turn(pimo, 0, 30)
T.turn(ruki, 0, -30)
for side in ('L', 'R'):
    T.arm(pimo, side, 0, 0, None)
T.arm(pimo, 'R', 10, fwd=-60, out=30)
T.arm(pimo, 'R', 40, fwd=-60, out=30)
T.rest_arm(pimo, 'R', 52)
for f, a in ((60, 30), (68, 18), (76, 30), (84, 18), (92, 30)):
    K(pimo['sq'], 'rotation_euler', f, (0, math.radians(a - 30), 0))
T.arm(ruki, 'L', 176, 0, None)
T.arm(ruki, 'L', 186, fwd=-55, out=40)
T.arm(ruki, 'L', 214, fwd=-55, out=40)
T.rest_arm(ruki, 'L', 226)
gesture(ruki, 'breathe', 300)
gesture(pimo, 'breathe', 420)
T.arm(ruki, 'L', 230, 0, None)
T.arm(ruki, 'L', 240, fwd=-40, out=55)
T.arm(ruki, 'L', 300, fwd=-40, out=55)
T.rest_arm(ruki, 'L', 312)
T.arm(ruki, 'L', 520, 0, None)
T.arm(ruki, 'L', 530, fwd=-40, out=40)
T.arm(ruki, 'L', 590, fwd=-40, out=40)
T.rest_arm(ruki, 'L', 602)

b2 = HW.bouquet('ramo2', (0, 0, 0), h=0.24, cols=((0.98, 0.85, 0.4), (0.95, 0.92, 0.88), (0.95, 0.75, 0.8)))
P2 = Vector((-0.78, -0.55, Z0))
SLOT = Vector((AX - 0.3, RY + 0.22, TZ))
K(b2, 'scale', 0, (0, 0, 0))
K(b2, 'scale', 880, (0, 0, 0))
K(b2, 'scale', 890, (0.8,) * 3)
K(b2, 'location', 880, tuple(PP + Vector((0.3, -0.28, 0.5))))
hop_to(pimo, 896, PP, P2, 12, apex=0.12)
K(b2, 'location', 896, tuple(PP + Vector((0.3, -0.28, 0.5))))
K(b2, 'location', 908, tuple(P2 + Vector((0.3, -0.28, 0.5))))
K(b2, 'location', 930, tuple(SLOT + Vector((0, 0, 0.12))))
K(b2, 'location', 944, tuple(SLOT))
for side in ('L', 'R'):
    T.arm(pimo, side, 880, 0, None)
    T.arm(pimo, side, 890, fwd=-70, out=25)
    T.arm(pimo, side, 940, fwd=-70, out=25)
    T.rest_arm(pimo, side, 954)
T.turn(pimo, 896, 30)
T.turn(pimo, 912, 45)
T.turn(pimo, 950, 45)
T.turn(pimo, 964, 15)
T.turn(ruki, 940, -30)
T.turn(ruki, 952, -10)

T.lines(EID, LINES)
T.blinks(pimo, (40, 170, 300, 430, 560, 690, 820, 960))
T.blinks(ruki, (80, 220, 350, 480, 610, 740, 870, 990))
