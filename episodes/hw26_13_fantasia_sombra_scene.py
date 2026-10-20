from stage import *
from episodes.hw26_13_fantasia_sombra_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props.costumes import dress, flat
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_13_fantasia_sombra'
Z0 = 0.08
autumn(dusk=True)
auto_dress(EID, ENV)

SX, SY = -0.15, -0.4
SW, SH = 1.35, 1.15
scr = HW.shadow_screen('pantalla', (SX, SY, Z0), w=SW, h=SH)
PZ = Z0 + 0.25 + SH / 2
FRONT = SY - 0.012
lamp = spawn('shadow_lamp', 2, 1301, 'autumn', (SX + 0.1, 1.2, Z0), 1.6, 0)

cream = M((0.95, 0.93, 0.89), rough=0.55, coat=0.3)
shade = M((0.36, 0.33, 0.44), rough=0.9, coat=0.0)
ink = M((0.15, 0.12, 0.18), rough=0.5)


def ghost_pts(w, h, n=24):
    pts = []
    for k in range(n + 1):
        a = math.pi * k / n
        pts.append((w * math.cos(a), h * 0.35 + w * math.sin(a)))
    pts.append((-w * 1.25, h * 0.05))
    pts.append((-w * 1.0, -h * 0.05))
    for k in range(13):
        x = -w + 2 * w * k / 12
        pts.append((x, -h * 0.5 + 0.1 * h * abs(math.sin(math.pi * 3 * k / 12))))
    pts.append((w * 1.0, -h * 0.05))
    pts.append((w * 1.25, h * 0.05))
    return pts


cut = C.empty('cutout', None, (SX, -0.1, 0.8))
flat('cut_body', ghost_pts(0.16, 0.36), 0.01, cream, cut)
for sx in (-1, 1):
    C.sphere(f'cut_eye{sx}', (sx * 0.05, -0.008, 0.16), (0.022, 0.004, 0.03), ink, cut, 12)
C.tube('cut_stick', [(0, 0.0, -0.2), (0, 0.0, -0.55)], 0.012, M((0.6, 0.42, 0.26), rough=0.5), cut)
sh = C.empty('sombra', None, (SX, FRONT, PZ + 0.05))
flat('sombra_m', ghost_pts(0.3, 0.62), 0.004, shade, sh)
flat('sombra_back', ghost_pts(0.3, 0.62), 0.004, shade, sh, loc=(0, 0.024, 0))
for sx in (-1, 1):
    C.sphere(f'sombra_eye{sx}', (sx * 0.095, -0.004, 0.29), (0.04, 0.003, 0.055), M((0.93, 0.9, 0.84), rough=0.9), sh, 16)
K(sh, 'scale', 0, (1, 1, 1))
for k, f in enumerate(range(0, 400, 24)):
    d = 0.03 if k % 2 else -0.03
    K(cut, 'location', f, (SX + d, -0.1, 0.8 + 0.02 * (k % 2)))
    K(sh, 'location', f, (SX + d * 1.8, FRONT, PZ + 0.05 + 0.035 * (k % 2)))
K(cut, 'location', 420, (SX, -0.1, 0.8))
K(sh, 'location', 420, (SX, FRONT, PZ + 0.05))
K(sh, 'scale', 420, (1, 1, 1))
K(cut, 'location', 452, (SX - 0.45, 0.3, 0.55))
K(sh, 'location', 446, (SX + 0.5, FRONT, PZ + 0.02))
K(sh, 'scale', 446, (0.3, 1, 0.3))
K(sh, 'scale', 450, (0, 0, 0))
K(cut, 'location', 820, (SX - 0.45, 0.3, 0.55))

hand = C.empty('mano', None, (SX + 0.05, FRONT, PZ + 0.1))
C.sphere('palm', (0, 0, 0), (0.16, 0.004, 0.14), shade, hand, 32)
for k, (x, z, rz) in enumerate(((-0.12, 0.25, 14), (-0.045, 0.3, 5), (0.045, 0.3, -5), (0.12, 0.25, -14))):
    C.sphere(f'finger{k}', (x, 0, z), (0.035, 0.004, 0.14), shade, hand, 20, rot=(0, math.radians(rz), 0))
C.sphere('thumb', (-0.17, 0, 0.01), (0.04, 0.004, 0.09), shade, hand, 20, rot=(0, math.radians(50), 0))
for f, v in ((0, 0), (790, 0), (804, 1.0)):
    K(hand, 'scale', f, (v, v, v))
for f, x in ((804, 0.0), (816, 0.04), (828, -0.04), (840, 0.0)):
    K(hand, 'location', f, (SX + 0.05 + x, FRONT, PZ + 0.1))

gruno = make('gruno', 1.15)
GP = Vector((SX + 0.05, 0.45, Z0))
T.place(gruno, 0, GP)
T.turn(gruno, 0, 0)
dress(gruno, 'gruno', COSTUME, 0)
for side in ('L', 'R'):
    T.arm(gruno, side, 0, fwd=-70, out=30)
T.turn(gruno, 196, 0)
T.turn(gruno, 206, 40)
T.turn(gruno, 380, 40)
T.turn(gruno, 390, 0)
for f, z in ((200, 0.0), (206, 0.05), (212, 0.0)):
    K(gruno['hold'], 'location', f, tuple(GP + Vector((0, 0, z))))

pimo = make('pimo', 1.15)
PP = Vector((-1.05, -0.95, Z0))
T.place(pimo, 0, PP)
T.turn(pimo, 0, 35)
for f, a in ((14, 0), (22, 8), (60, 8), (68, 0)):
    K(pimo['sq'], 'rotation_euler', f, (0, math.radians(-a), 0))
gesture(pimo, 'breathe', 300)
T.turn(pimo, 600, 35)
T.turn(pimo, 612, 60)
T.turn(pimo, 760, 60)
T.turn(pimo, 772, 35)
for f, z in ((800, 0.0), (806, 0.07), (812, 0.0)):
    K(pimo['hold'], 'location', f, tuple(PP + Vector((0, 0, z))))

BK = Vector((0.95, -0.5, Z0))
spawn('low_table', 2, 1302, 'autumn', tuple(BK), 0.7, 0)
BZ = BK.z + 0.62 * 0.7
bs = spawn('book_stand', 1, 1303, 'autumn', (BK.x, BK.y - 0.05, BZ), 1.1, 0, tilt=60)
t = math.radians(60)
apos = Vector((BK.x, BK.y - 0.05 + 1.1 * (0.05 + 0.12 * math.cos(t) - 0.02), BZ + 1.1 * (0.06 + 0.12 * math.sin(t) + 0.015)))
alb = HW.album('cuento', tuple(apos), w=0.5, h=0.36, rot=(t, 0, 0), cover=(0.3, 0.45, 0.62))
K(alb['lid'], 'rotation_euler', 0, (0, math.radians(180), 0))
stars = M((0.98, 0.8, 0.35), rough=0.4, emit=0.3)
for k, (x, y) in enumerate(((-0.17, 0.12), (-0.08, -0.1), (0.15, 0.13), (0.2, -0.08))):
    C.sphere(f'estrella{k}', (x, y, 0.06), (0.018, 0.018, 0.004), stars, alb['root'], 5)
nubi = HW.ghost('Nubi', h=0.42)
nr = nubi['root']
NP = apos + Vector((0, -0.08, 0.12))
K(nr, 'location', 0, tuple(NP - Vector((0, 0, 0.3))))
K(nr, 'scale', 0, (0, 0, 0))
K(nr, 'scale', 622, (0, 0, 0))
K(nr, 'location', 622, tuple(NP - Vector((0, 0, 0.3))))
K(nr, 'scale', 638, (1, 1, 1))
K(nr, 'location', 640, tuple(NP))
for k, f in enumerate(range(650, TOTAL, 20)):
    K(nr, 'location', f, tuple(NP + Vector((0, 0, 0.025 if k % 2 else 0.0))))
na = nubi['arms'][1]
r0 = tuple(na.rotation_euler)
for f, d in ((650, 0), (658, -70), (666, -50), (674, -70), (682, -50), (690, -70), (700, 0)):
    K(na, 'rotation_euler', f, (r0[0], r0[1] + math.radians(d), r0[2]))
mo = nubi['mouth']
n = max(2, round(T.dur('ep_%s_u1' % EID, LINES[3][2]) * FPS / 4))
for k in range(n + 1):
    f = LINES[3][3] + 4 * k
    v = 1.0 if (k % 2 == 0 or k == n) else 1.6
    K(mo, 'scale', f, (1.0, 1.0, v))
cl = HW.card('lab_cuento', 'cuento', _font(), (BK.x, BK.y - 0.35, 1.6), w=0.5, h=0.16, bg=(0.3, 0.45, 0.62), ink=(1.0, 0.95, 0.8), rot=(math.radians(-6), 0, 0))
T.pop_in(cl, 630, 1.0, 12)
ls = HW.card('lab_sombra', 'sombra', _font(), (SX, SY - 0.3, PZ + SH / 2 + 0.2), w=0.55, h=0.16, bg=(0.4, 0.27, 0.45), ink=(1.0, 0.9, 0.7), rot=(math.radians(-6), 0, 0))
T.pop_in(ls, 412, 1.0, 12)
T.pop_out(ls, 600, 1.0, 8)

W0 = ((0, -6.3, 1.6), (0, -0.6, 0.9), 26)
WR = ((2.4, 1.7, 1.7), (SX, 0.2, 0.75), 30)
WB = ((0.95, -3.3, 1.3), (0.95, -0.5, 0.95), 30)
camkey(0, W0)
camkey(176, W0)
camkey(212, WR)
camkey(392, WR)
camkey(426, W0)
camkey(608, W0)
camkey(626, WB)
camkey(756, WB)
camkey(774, W0)
camkey(TOTAL - 1, W0)

T.lines(EID, LINES)
T.blinks(pimo, (40, 170, 300, 430, 560, 690, 820))
T.blinks(gruno, (90, 240, 380, 520, 700))
