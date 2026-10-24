from stage import *
from episodes.patron_ab_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress
EID = 'patron_ab'
Z0 = 0.08
auto_dress(EID, ENV)
TX = -1.2
TY = -1.75
GAP = 0.4
TS = 1.25
train = spawn('toy_train', 0, 3301, (0.95, 0.45, 0.4), (TX, TY, Z0), 1.0, 0, n=5, gap=GAP)
SLOT = [Vector((TX + GAP * (i + 1), TY - 0.02, Z0 + 0.18)) for i in range(5)]
ICONS = ['hoja', 'flor', 'hoja', 'flor']
FAM = {'hoja': (0.45, 0.8, 0.5), 'flor': (1.0, 0.62, 0.75), 'zapato': (0.45, 0.65, 1.0)}
tiles = [spawn('symbol_tile', 2, 3310 + i, FAM[ic], tuple(SLOT[i]), TS, 0, icon=ic) for i, ic in enumerate(ICONS)]
TB = Vector((0.0, -0.75, Z0))
spawn('low_table', 0, 3320, (0.98, 0.85, 0.55), tuple(TB), 1.0, 0)
CH = Vector((0.02, -0.82, Z0 + 0.62))
CF = Vector((0.42, -0.82, Z0 + 0.62))
cand_h = spawn('symbol_tile', 2, 3331, FAM['hoja'], tuple(CH), TS, 0, icon='hoja')
cand_f = spawn('symbol_tile', 2, 3332, FAM['flor'], tuple(CF), TS, 0, icon='flor')
T.pop_in(cand_h, 448, TS)
T.pop_in(cand_f, 454, TS)
TP = Vector((-1.05, -0.7, Z0))
BP = Vector((1.05, -0.7, Z0))
HAND = Vector((-0.75, -1.15, 1.45))
FEET = Vector((-0.4, -0.82, Z0 + 0.62))
TF = Vector((-0.95, -2.3, Z0))
SF = TF + Vector((0.45, -0.05, 0))
shoe = spawn('symbol_tile', 2, 3340, FAM['zapato'], tuple(HAND), TS * 1.9, 0, icon='zapato')

C0 = ((-0.4, -4.6, 0.7), (-0.45, -1.3, 0.95), 28)
W1 = ((-0.15, -7.5, 2.5), (-0.15, -1.3, 0.95), 30)
W2 = ((0.0, -6.2, 1.6), (0.0, -1.6, 0.75), 30)
WE = ((-0.15, -7.3, 2.4), (-0.15, -1.3, 0.95), 30)
camkey(0, C0)
camkey(92, ((-0.35, -4.8, 0.8), (-0.42, -1.3, 0.95), 28))
camkey(108, W1)
camkey(170, W1)
camkey(186, W2)
camkey(340, W2)
camkey(356, W1)
camkey(530, W1)
camkey(548, W2)
camkey(630, W2)
camkey(648, WE)
camkey(TOTAL - 1, ((-0.15, -7.0, 2.3), (-0.15, -1.3, 0.95), 30))

tuki = make('tuki', 1.6)
bopi = make('bopi', 1.6)
T.place(tuki, 0, TP)
T.turn(tuki, 0, 10)
T.place(bopi, 0, BP)
T.turn(bopi, 0, -25)


def fly(o, f0, a, b, dur=14, apex=0.5, s=1.0):
    K(o, 'location', f0 - 1, tuple(a))
    for t in range(0, dur + 1, 2):
        u = t / dur
        p = a.lerp(b, u)
        p.z += apex * 4 * u * (1 - u)
        K(o, 'location', f0 + t, tuple(p))
    K(o, 'location', f0 + dur, tuple(b))
    K(o, 'scale', f0 + dur, (s,) * 3)
    K(o, 'scale', f0 + dur + 2, (s * 1.15, s * 1.15, s * 0.8))
    K(o, 'scale', f0 + dur + 6, (s * 0.96, s * 0.96, s * 1.05))
    K(o, 'scale', f0 + dur + 9, (s,) * 3)


def pulse(o, f, s=TS, up=0.1):
    K(o, 'scale', f - 1, (s,) * 3)
    K(o, 'scale', f + 3, (s * 1.28,) * 3)
    K(o, 'scale', f + 8, (s,) * 3)


S1 = TS * 1.9
for k, f in enumerate(range(0, 96, 12)):
    K(shoe, 'location', f, tuple(HAND + Vector((0, 0, 0.06 if k % 2 else 0))))
    K(shoe, 'rotation_euler', f, (0, math.radians(8 if k % 2 else -8), 0))
T.arm(tuki, 'R', 0, fwd=-20, out=150)
T.arm(tuki, 'L', 0, fwd=-20, out=150)
for f in (20, 44, 68):
    S(tuki, f, (1, 1, 1))
    S(tuki, f + 6, (1.05, 1.05, 0.95))
    S(tuki, f + 12, (1, 1, 1))
K(shoe, 'rotation_euler', 104, (0, 0, 0))
T.rest_arm(tuki, 'R', 106)
T.rest_arm(tuki, 'L', 106)
T.turn(tuki, 100, 30)
T.turn(bopi, 100, -35)
BH = Vector((0.72, -1.15, 1.0))
fly(shoe, 108, HAND + Vector((0, 0, 0.06)), BH, dur=14, apex=0.35, s=S1)
T.arm(bopi, 'L', 116, 0, None)
T.arm(bopi, 'L', 122, fwd=-50, out=45)
T.turn(bopi, 128, -60)
fly(shoe, 134, BH, SLOT[4], dur=16, apex=0.4, s=TS)
T.rest_arm(bopi, 'L', 150)
T.turn(bopi, 156, -25)
T.turn(tuki, 150, 15)

for i, f in enumerate((182, 202, 228, 249)):
    pulse(tiles[i], f)
T.arm(bopi, 'L', 178, 0, None)
T.arm(bopi, 'L', 184, fwd=-45, out=55)
T.rest_arm(bopi, 'L', 244)
gesture(tuki, 'sway', 200)

ring_m = C.mat('pair', (1.0, 0.78, 0.2), rough=0.3, coat=0.7, emit=0.6)


def pair_ring(cx, f_in, f_out):
    g = C.empty('pair', None, (cx, TY - 0.24, Z0 + 0.38))
    w, h = 0.36, 0.22
    pts = []
    for k in range(41):
        a = k * 6.2832 / 40
        pts.append((math.cos(a) * w, 0, math.sin(a) * h))
    C.tube('ring', pts, 0.022, ring_m, g)
    T.pop_in(g, f_in, 1.0)
    T.pop_out(g, f_out, 1.0)
    return g


cx01 = (SLOT[0].x + SLOT[1].x) / 2
cx23 = (SLOT[2].x + SLOT[3].x) / 2
pair_ring(cx01, 274, 440)
pair_ring(cx23, 292, 440)
for f in (300, 316):
    pulse(tiles[0], f)
    pulse(tiles[1], f)
    pulse(tiles[2], f + 8)
    pulse(tiles[3], f + 8)
T.turn(tuki, 270, 0)
gesture(bopi, 'breathe', 276)

K(shoe, 'rotation_euler', 362, (0, 0, 0))
for k, f in enumerate(range(366, 392, 5)):
    K(shoe, 'rotation_euler', f, (0, math.radians(12 if k % 2 else -12), 0))
K(shoe, 'rotation_euler', 394, (0, 0, 0))
T.turn(tuki, 360, 20)
T.arm(tuki, 'R', 362, 0, None)
T.arm(tuki, 'R', 368, fwd=-40, out=60)
T.rest_arm(tuki, 'R', 400)
fly(shoe, 404, SLOT[4], FEET, dur=20, apex=0.6, s=TS)
T.turn(tuki, 410, 35)
T.turn(tuki, 432, 10)

q = word3d('?', (0.55, 0.3, 0.95), (SLOT[4].x, TY - 0.1, 1.08), 456, 552, size=0.5, max_w=0.8)
for f in range(470, 540, 16):
    K(q, 'location', f, (SLOT[4].x, TY - 0.1, 1.08))
    K(q, 'location', f + 8, (SLOT[4].x, TY - 0.1, 1.16))
T.turn(bopi, 450, -15)
T.turn(tuki, 452, 25)
for f in (486, 516):
    pulse(cand_h, f)
for f in (500, 528):
    pulse(cand_f, f)
T.turn(tuki, 486, 40)
T.turn(tuki, 500, 15)
T.turn(tuki, 516, 40)
T.turn(tuki, 528, 15)

T.turn(tuki, 538, 30)
T.arm(tuki, 'R', 540, 0, None)
T.arm(tuki, 'R', 546, fwd=-60, out=70)
T.rest_arm(tuki, 'R', 584)
fly(cand_h, 556, CH, SLOT[4], dur=18, apex=0.55, s=TS)
for i, f in enumerate(range(592, 632, 8)):
    pulse(tiles[i] if i < 4 else cand_h, f)
confetti(612, (-0.3, -1.6, 2.2), n=24, spread=2.0)
gesture(tuki, 'hops', 600)
gesture(bopi, 'sway', 604)

T.turn(tuki, 646, 40)
T.turn(tuki, 652, 0)
hop_to(tuki, 654, TP, TF, 20, apex=1.15)
fly(shoe, 682, FEET, SF, dur=16, apex=0.5, s=TS * 1.2)
T.turn(tuki, 684, 25)
pulse(shoe, 704, TS * 1.2)
gesture(tuki, 'bounce', 712)
C.wave(bopi, 'R', 720, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(tuki, (60, 150, 250, 340, 470, 560, 640, 740))
T.blinks(bopi, (40, 130, 260, 390, 500, 610, 720))
