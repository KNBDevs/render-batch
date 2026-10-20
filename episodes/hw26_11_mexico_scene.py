from stage import *
from episodes.hw26_11_mexico_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props import halloween as HW
EID = 'hw26_11_mexico'
Z0 = 0.08
auto_dress(EID, ENV)

W0 = ((0, -6.3, 1.75), (0, -1.0, 0.95), 27)
WC = ((0, -5.0, 1.5), (0, -0.9, 0.9), 24)
WT = ((0, -5.0, 1.45), (0, -0.8, 0.88), 24)
camkey(0, W0)
camkey(160, W0)
camkey(176, WC)
camkey(780, WC)
camkey(796, WT)
camkey(TOTAL - 1, WT)

TS = 1.3
tb = HW.remembrance_table('mesa', (0, -0.62, Z0), w=0.95, cloth=(0.95, 0.9, 0.8))
tb['root'].scale = (TS,) * 3
TZ = Z0 + tb['top'] * TS
TY = -0.62

alb = HW.album('album', (-0.38, TY - 0.12, TZ), w=0.34, h=0.24, rot=(0, 0, math.radians(8)))
mg0 = HW.marigold('cempa0', (-0.12, TY - 0.2, TZ + 0.02), r=0.1)
for f, z in ((0, 0.0), (24, 0.0), (32, 0.06), (40, 0.0), (48, 0.03), (54, 0.0)):
    K(mg0, 'location', f, (-0.12, TY - 0.2, TZ + 0.02 + z))

fr = HW.photo_frame('foto', (0.1, TY + 0.1, TZ), h=0.3)
bb = spawn('bread_basket', 0, 1101, 'autumn', (0.38, TY - 0.02, TZ), 1.0, 0)
pan = HW.pan_de_muerto('pan', (0.38, TY - 0.02, TZ + 0.07), r=0.07)
gl = HW.water_glass('vaso', (-0.2, TY + 0.12, TZ), h=0.1)
mgs = []
for k, (x, y) in enumerate(((-0.05, 0.15), (0.24, 0.16), (-0.42, 0.14))):
    m_ = HW.marigold(f'cempa{k + 1}', (x, TY + y, TZ + 0.02), r=0.075)
    mgs.append(m_)
for k, o in enumerate([fr, pan, gl] + mgs):
    T.pop_in(o, 196 + 12 * k, 1.0, 12)
bb.scale = (0, 0, 0)
T.pop_in(bb, 196, 1.0, 12)

pp = HW.papel_picado('papel', (-0.75, TY + 0.35, 1.45), (0.75, TY + 0.35, 1.45), n=5, sag=0.08)
T.pop_in(pp, 230, 1.0, 14)

sg = HW.card('lab_mx', 'México', _font(), (0.0, TY - 0.45, 1.75), w=0.6, h=0.18, bg=(0.4, 0.27, 0.45), ink=(1.0, 0.9, 0.7), rot=(math.radians(-6), 0, 0))
T.pop_in(sg, 180, 1.0, 12)
T.pop_out(sg, 780, 1.0, 10)

pimo = make('pimo', 1.2)
ruki = make('ruki', 1.2)
PP = Vector((-0.98, -0.75, Z0))
RP = Vector((0.98, -0.78, Z0))
T.place(pimo, 0, PP)
T.place(ruki, 0, RP)
T.turn(pimo, 0, 35)
T.turn(ruki, 0, -30)
for f, z in ((12, 0.0), (18, 0.06), (24, 0.0)):
    K(pimo['hold'], 'location', f, tuple(PP + Vector((0, 0, z))))
T.arm(pimo, 'R', 20, 0, None)
T.arm(pimo, 'R', 30, fwd=-55, out=40)
T.arm(pimo, 'R', 90, fwd=-55, out=40)
T.rest_arm(pimo, 'R', 102)
gesture(pimo, 'breathe', 300)
gesture(ruki, 'breathe', 240)

rf = HW.marigold('cempa_r', (0, 0, 0), r=0.09)
RP2 = Vector((0.75, -0.8, Z0))
SLOT = Vector((0.3, TY + 0.14, TZ + 0.02))
K(rf, 'scale', 0, (0, 0, 0))
K(rf, 'scale', 500, (0, 0, 0))
K(rf, 'scale', 510, (1, 1, 1))
HAND = Vector((-0.28, -0.22, 0.55))
K(rf, 'location', 500, tuple(RP + HAND))
K(rf, 'location', 516, tuple(RP + HAND))
hop_to(ruki, 516, RP, RP2, 12, apex=0.1)
K(rf, 'location', 528, tuple(RP2 + HAND))
K(rf, 'location', 552, tuple(SLOT + Vector((0, 0, 0.12))))
K(rf, 'location', 566, tuple(SLOT))
for side in ('L', 'R'):
    T.arm(ruki, side, 500, 0, None)
    T.arm(ruki, side, 510, fwd=-65, out=25)
    T.arm(ruki, side, 562, fwd=-65, out=25)
    T.rest_arm(ruki, side, 576)
T.turn(ruki, 516, -30)
T.turn(ruki, 530, -45)
T.turn(ruki, 600, -45)
T.turn(ruki, 612, -25)
hop_to(ruki, 640, RP2, RP, 12, apex=0.1)

lab = HW.card('lab_dm', 'Día de Muertos', _font(), (0.0, TY - 0.45, 1.75), w=0.86, h=0.18, bg=(0.98, 0.62, 0.2), ink=(0.15, 0.2, 0.26), rot=(math.radians(-6), 0, 0))
T.pop_in(lab, 796, 1.0, 12)

T.lines(EID, LINES)
T.blinks(pimo, (40, 170, 300, 430, 560, 690, 820, 960))
T.blinks(ruki, (80, 220, 350, 480, 610, 740, 870, 990))
