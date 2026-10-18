from stage import *
from episodes.hw26_08_murcielago_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props.costumes import dress, flat
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_08_murcielago'
Z0 = 0.08
autumn(dusk=True)
auto_dress(EID, ENV)

W0 = ((0, -5.6, 1.6), (0, -1.0, 0.9), 32)
WC = ((0.5, -3.6, 1.5), (0.5, -0.95, 1.35), 30)
WF = ((0, -5.8, 1.9), (0, -1.0, 1.15), 31)
camkey(0, W0)
camkey(160, W0)
camkey(182, WC)
camkey(448, WC)
camkey(468, WF)
camkey(640, WF)
camkey(660, W0)
camkey(TOTAL - 1, W0)

PP = Vector((0.55, -0.95, Z0))
PS = 1.0
spawn('perch_stand', 1, 808, 'autumn', tuple(PP), PS, 0)
TOP = PP + Vector((0, 0, PS * (0.8 + 0.026)))
VS = 0.85
velo = HW.bat('Velo', h=VS)
vr = velo['root']
SEAT = TOP - Vector((0, 0, 0.05 * VS / 0.5))
vr.location = SEAT
K(vr, 'location', 0, tuple(SEAT))
HW.fold_wings(velo, 0, 1.0)
for f, z in ((0, 0.12), (10, 0.0), (16, 0.015), (22, 0.0)):
    K(vr, 'location', f, tuple(SEAT + Vector((0, 0, z))))
HW.fold_wings(velo, 176, 1.0)
HW.fold_wings(velo, 194, 0.0)
for f, a in ((60, 0), (70, -18), (150, -18), (162, 0)):
    K(vr, 'rotation_euler', f, (0, 0, math.radians(a)))
for f, a in ((210, 0), (222, 8), (240, -8), (252, 0)):
    K(velo['rig'], 'rotation_euler', f, (math.radians(a), 0, 0))
HW.fold_wings(velo, 462, 0.0)
PATH = [(470, (0.0, 0.0, 0.3)), (512, (-0.45, -0.1, 0.7)), (556, (-1.05, 0.15, 0.75)), (598, (-0.55, 0.25, 0.5)), (632, (0.0, 0.0, 0.0))]
K(vr, 'location', 462, tuple(SEAT))
K(vr, 'rotation_euler', 462, (0, 0, 0))
HW.flap(velo, 468, 630, period=12, amp=34)
for f, d in PATH:
    K(vr, 'location', f, tuple(SEAT + Vector(d)))
for f, a in ((470, 0), (512, 25), (556, -10), (598, -35), (632, 0)):
    K(vr, 'rotation_euler', f, (0, 0, math.radians(a)))
HW.fold_wings(velo, 632, 0.0)
HW.fold_wings(velo, 648, 1.0)
for f, z in ((632, 0.0), (636, -0.02), (642, 0.0)):
    K(vr, 'location', f, tuple(SEAT + Vector((0, 0, z))))
HW.fold_wings(velo, 770, 1.0)
HW.fold_wings(velo, 782, 0.35)
HW.fold_wings(velo, 794, 1.0)

luma = make('luma', 1.25)
dress(luma, 'luma', COSTUME, 0)
LP = Vector((-0.75, -0.8, Z0))
T.place(luma, 0, LP)
for f, a in ((0, 30), (466, 30), (512, 20), (556, -5), (598, 10), (632, 30), (700, 15), (712, -10), (790, -10), (800, 20)):
    T.turn(luma, f, a)
gesture(luma, 'breathe', 200)
T.arm(luma, 'R', 40, 0, None)
T.arm(luma, 'R', 50, fwd=-60, out=35)
T.arm(luma, 'R', 120, fwd=-60, out=35)
T.rest_arm(luma, 'R', 130)
for f, z in ((196, 0.0), (202, 0.06), (208, 0.0)):
    K(luma['hold'], 'location', f, tuple(LP + Vector((0, 0, z))))
LP2 = LP + Vector((-0.25, -0.05, 0))
hop_to(luma, 640, LP, LP2, 10, apex=0.15)

gruno = make('gruno', 1.35)
G0 = Vector((-2.7, -0.3, Z0))
G1 = Vector((-1.5, -0.3, Z0))
G2 = Vector((-0.3, -0.45, Z0))
T.place(gruno, 0, G0)
T.turn(gruno, 0, 25)
hop_to(gruno, 646, G0, G1, 12, apex=0.25)
hop_to(gruno, 660, G1, G2, 12, apex=0.25)
ga = T._arm(gruno, 'R')
am_ = next(o for o in ga.children if '.armmesh.' in o.name)
L = am_.scale.z / 0.6
cape_m = M((0.86, 0.42, 0.14), rough=0.45, coat=0.6)
trim_m = M((0.98, 0.8, 0.45), rough=0.4, coat=0.6)
cp = C.empty('cape_piv', ga, (am_.location.x, 0.0, am_.location.z - am_.scale.z * 0.95))
cw = 1.7 * L
cl = 2.3 * L
flat('cape', [(-0.15 * L, 0.0), (cw, 0.0), (cw * 1.1, -cl), (cw * 0.45, -cl * 1.08), (-0.1 * L, -cl * 0.95)], 0.05 * L, cape_m, cp)
C.tube('cape_trim', [(-0.2 * L, 0.0, 0.0), (cw * 1.02, 0.0, 0.0)], 0.07 * L, trim_m, cp)
T.pop_in(cp, 668, 1.0, 8)
for f, a in ((672, 10), (680, 15)):
    T.turn(gruno, f, a)
T.arm(gruno, 'R', 676, 0, None)
T.arm(gruno, 'L', 676, 0, None)
T.arm(gruno, 'R', 684, fwd=0, out=95)
K(cp, 'rotation_euler', 676, (0, 0, 0))
K(cp, 'rotation_euler', 684, (0, math.radians(95), 0))
for k, f in enumerate(range(690, 758, 8)):
    up = k % 2 == 0
    T.arm(gruno, 'R', f, fwd=0, out=115 if up else 75)
    T.arm(gruno, 'L', f, fwd=0, out=150 if up else 100)
    K(cp, 'rotation_euler', f, (math.radians(18 if up else -14), math.radians(95 + (-20 if up else 20)), 0))
T.rest_arm(gruno, 'R', 768)
T.rest_arm(gruno, 'L', 768)
K(cp, 'rotation_euler', 760, (0, math.radians(95), 0))
K(cp, 'rotation_euler', 768, (0, 0, 0))
hop_to(gruno, 700, G2, G2, 10, apex=0.12)
hop_to(gruno, 724, G2, G2, 10, apex=0.12)
S(gruno, 764, (1, 1, 1))
S(gruno, 770, (1.06, 1.06, 0.92))
S(gruno, 778, (1, 1, 1))

lab = HW.card('lab_np', 'sin plumas', _font(), (0.5, -1.3, 2.4), w=0.7, h=0.17, bg=(0.4, 0.27, 0.45), ink=(1.0, 0.9, 0.7), rot=(math.radians(-6), 0, 0))
T.pop_in(lab, 330, 1.0, 10)
T.pop_out(lab, 448, 1.0, 8)

T.lines(EID, LINES)
T.blinks(luma, (30, 150, 260, 380, 520, 660, 780))
T.blinks(gruno, (690, 740, 790))


