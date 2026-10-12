from stage import *
from episodes.hw26_03_faroles_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props.costumes import dress
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_03_faroles'
Z0 = 0.08
autumn(dusk=True)
auto_dress(EID, ENV)

W0 = ((0, -6.4, 1.75), (0, -1.15, 0.95), 32)
WT = ((-0.15, -5.0, 1.55), (-0.15, -1.35, 1.0), 34)
WP = ((0.35, -5.2, 1.6), (0.35, -1.3, 1.0), 34)
camkey(0, W0)
camkey(140, W0)
camkey(152, WT)
camkey(398, WT)
camkey(410, WP)
camkey(600, WP)
camkey(612, W0)
camkey(TOTAL - 1, W0)

TY = -1.55
spawn('low_table', 2, 2603, 'autumn', (-0.3, TY, Z0), 0.9, 0)
TOP = Z0 + 0.62 * 0.9
font = _font()

gruno = make('gruno', 1.45)
ruki = make('ruki', 1.35)
dress(gruno, 'gruno', COSTUME, 0)
dress(ruki, 'ruki', COSTUME, 0)
GP = Vector((-0.95, -0.95, Z0))
RP = Vector((0.95, -0.9, Z0))
T.place(gruno, 0, GP)
T.place(ruki, 0, RP)
T.turn(gruno, 0, 30)
T.turn(ruki, 0, -40)

tur = HW.turnip_lantern('turnip', (-0.4, TY - 0.02, TOP), h=0.36)
HW.led_light('tled', (0, 0.0, 0.1), h=0.06, parent=tur)
glow_m = bpy.data.materials.get('glow')

PK = Vector((0.5, -1.15, Z0))
pump = HW.pumpkin('bigpump', tuple(PK), h=0.7, face=True)
T.pop_in(pump, 4, 1.0, 10)
K(pump, 'scale', 440, (1, 1, 1))
K(pump, 'scale', 446, (1.15, 1.15, 1.15))
K(pump, 'scale', 452, (1, 1, 1))

for f, a in ((20, 30), (28, 10), (40, 10), (48, 55), (60, 55), (70, 30)):
    T.turn(gruno, f, a)
T.arm(gruno, 'R', 24, fwd=-30, out=70)
T.arm(gruno, 'R', 60, fwd=-30, out=70)
T.rest_arm(gruno, 'R', 72)
S(gruno, 52, (1, 1, 1))
S(gruno, 56, (1.06, 1.06, 0.94))
S(gruno, 62, (1, 1, 1))

ir = spawn('region_sign', 0, 2621, 'autumn', (-0.05, TY + 0.3, Z0), 1.45, 0, label='Irlanda')
T.pop_in(ir, 168, 1.45, 10)
for k, f in enumerate((210, 234, 258)):
    K(tur, 'scale', f, (1, 1, 1))
    K(tur, 'scale', f + 4, (1.08, 1.08, 1.08))
    K(tur, 'scale', f + 10, (1, 1, 1))
T.turn(gruno, 196, 45)
gesture(gruno, 'breathe', 250)
T.pop_out(ir, 400, 1.45, 8)

na = spawn('region_sign', 2, 2622, 'autumn', (0.22, -0.45, Z0), 1.55, 0, label='Norteamérica')
T.pop_in(na, 426, 1.55, 10)
T.turn(ruki, 430, -20)
gesture(ruki, 'breathe', 470)
T.pop_out(na, 598, 1.55, 8)

G2 = Vector((0.0, -1.2, Z0))
hop_to(gruno, 612, GP, G2, 14, apex=0.25)
T.turn(gruno, 626, 70)
for k in range(3):
    f = 640 + k * 16
    T.arm(gruno, 'L', f, fwd=-80, out=30)
    T.arm(gruno, 'R', f, fwd=-80, out=30)
    T.arm(gruno, 'L', f + 8, fwd=-80, out=55)
    T.arm(gruno, 'R', f + 8, fwd=-80, out=55)
    S(gruno, f, (1, 1, 1))
    S(gruno, f + 6, (1.04, 0.97, 1.0))
    S(gruno, f + 12, (1, 1, 1))
T.rest_arm(gruno, 'L', 694)
T.rest_arm(gruno, 'R', 694)
T.turn(gruno, 700, 20)
T.turn(ruki, 616, -35)
C.wave(ruki, 'L', 622, cycles=2, period=8)

hop_to(gruno, 720, G2, GP, 14, apex=0.25)
T.turn(gruno, 734, 40)
T.arm(gruno, 'R', 738, fwd=-50, out=50)
T.arm(gruno, 'R', 790, fwd=-50, out=50)
T.rest_arm(gruno, 'R', 800)
for f in (756, 774):
    K(tur, 'scale', f, (1, 1, 1))
    K(tur, 'scale', f + 5, (1.1, 1.1, 1.1))
    K(tur, 'scale', f + 10, (1, 1, 1))
    K(pump, 'scale', f + 3, (1, 1, 1))
    K(pump, 'scale', f + 8, (1.05, 1.05, 1.05))
    K(pump, 'scale', f + 13, (1, 1, 1))
gesture(ruki, 'sway', 790)
gesture(gruno, 'sway', 800)

T.lines(EID, LINES)
T.blinks(gruno, (40, 150, 270, 380, 500, 630, 760))
T.blinks(ruki, (70, 190, 310, 430, 560, 690, 810))
