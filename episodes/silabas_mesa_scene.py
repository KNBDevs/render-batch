from stage import *
from episodes.silabas_mesa_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress
EID = 'silabas_mesa'
Z0 = 0.08
auto_dress(EID, ENV)
TB = Vector((0.0, -1.35, Z0))
spawn('low_table', 1, 3401, (0.95, 0.68, 0.4), tuple(TB), 1.0, 0)
TOP = Z0 + 0.62
CS = 1.5


def easel(style, seed, x, icon, col):
    e = spawn('card_easel', style, seed, (0.55, 0.62, 0.95), (x, TB.y - 0.05, TOP), 1.0, 0)
    slot = next(o for o in e.children_recursive if o.name.startswith('card'))
    card = spawn('symbol_tile', 0, seed + 1, col, (0, 0, 0), CS, 0, slot, icon=icon)
    return e, card


em, cm = easel(0, 3410, -0.3, 'mesa', (0.95, 0.65, 0.35))
ep, cp = easel(0, 3420, 0.3, 'pelota', (1.0, 0.45, 0.45))
T.pop_in(ep, 212, 1.0)
ball = spawn('play_ball', 1, 3430, (1.0, 0.35, 0.3), (2.2, -1.8, Z0), 2.2, 0)
BALL = Vector((0.42, -1.78, Z0))
for t in range(0, 25, 3):
    u = t / 24
    K(ball, 'location', 196 + t, tuple(Vector((2.2, -1.8, Z0)).lerp(BALL, 1 - (1 - u) ** 2)))
    K(ball, 'rotation_euler', 196 + t, (0, math.radians(-420 * (1 - (1 - u) ** 2)), 0))

TP = Vector((-0.95, -0.85, Z0))
PP = Vector((0.95, -0.85, Z0))
tuki = make('tuki', 1.6)
pimo = make('pimo', 1.6)
T.place(tuki, 0, TP)
T.turn(tuki, 0, 20)
T.place(pimo, 0, PP)
T.turn(pimo, 0, -25)

C0 = ((-0.55, -4.5, 1.05), (-0.55, -1.2, 1.1), 30)
W1 = ((0.0, -6.8, 2.1), (0.0, -1.1, 1.25), 30)
WT = ((0.0, -6.0, 1.95), (0.0, -1.1, 1.3), 30)
WE = ((0.0, -6.6, 2.05), (0.0, -1.1, 1.25), 30)
camkey(0, C0)
camkey(96, ((-0.5, -4.7, 1.1), (-0.5, -1.2, 1.1), 30))
camkey(112, W1)
camkey(520, W1)
camkey(536, WT)
camkey(640, WT)
camkey(656, WE)
camkey(TOTAL - 1, ((0.0, -6.4, 2.0), (0.0, -1.1, 1.25), 30))


def clap_at(ch, f):
    for sd in ('L', 'R'):
        T.arm(ch, sd, f - 5, fwd=-65, out=40)
        T.arm(ch, sd, f, fwd=-65, out=4)
        T.arm(ch, sd, f + 5, fwd=-65, out=40)
    S(ch, f, (1.04, 1.04, 0.96))
    S(ch, f + 5, (1, 1, 1))


def hands_closed(ch, f0, f1):
    for sd in ('L', 'R'):
        T.arm(ch, sd, f0, fwd=-60, out=8)
        T.arm(ch, sd, f1, fwd=-60, out=8)


def rest(ch, f):
    T.rest_arm(ch, 'L', f)
    T.rest_arm(ch, 'R', f)


HANDS = TP + Vector((0.12, -0.42, 0.75))
word = word3d('mesa', (0.85, 0.3, 0.02), (-0.35, -1.75, 1.45), 6, None, size=0.55, max_w=3.6)
for f in range(18, 52, 8):
    K(word, 'location', f, (-0.35, -1.75, 1.45 + (0.05 if (f // 8) % 2 else 0)))
for sd in ('L', 'R'):
    T.arm(tuki, sd, 0, 0, None)
    T.arm(tuki, sd, 30, fwd=-70, out=55)
for t in range(0, 15, 3):
    u = t / 14
    K(word, 'location', 52 + t, tuple(Vector((-0.35, -1.75, 1.45)).lerp(HANDS, u)))
    K(word, 'scale', 52 + t, ((1 - u) * 0.9 + 0.05,) * 3)
K(word, 'scale', 67, (0, 0, 0))
hands_closed(tuki, 66, 112)
for k, f in enumerate(range(72, 110, 6)):
    T.turn(tuki, f, 20 + (8 if k % 2 else -8))
rest(tuki, 120)
T.turn(tuki, 116, 35)

COLS = [(0.08, 0.28, 0.85), (0.8, 0.12, 0.4), (0.08, 0.5, 0.2)]
T.turn(pimo, 118, -10)
for f in (147, 165):
    clap_at(pimo, f)
rest(pimo, 178)
word3d('me', COLS[0], (-0.36, -1.45, 2.05), 147, 214, size=0.6)
word3d('sa', COLS[1], (0.36, -1.45, 2.05), 165, 214, size=0.6)

T.turn(tuki, 200, 15)
T.turn(pimo, 200, -40)
for f in (231, 243, 262):
    clap_at(tuki, f)
rest(tuki, 276)
for x, txt, f, c in ((-0.62, 'pe', 231, COLS[0]), (0.0, 'lo', 243, COLS[1]), (0.62, 'ta', 262, COLS[2])):
    word3d(txt, c, (x, -1.45, 2.05), f, 318, size=0.6)
gesture(tuki, 'bounce', 280)

mesa_ch = [word3d(t, COLS[i], (-0.3 + 0.6 * i, -1.45, 2.12), 336 + i * 6, 640, size=0.5) for i, t in enumerate(('me', 'sa'))]
pel_ch = [word3d(t, COLS[i], (-0.56 + 0.56 * i, -1.45, 1.68), 352 + i * 6, 640, size=0.5) for i, t in enumerate(('pe', 'lo', 'ta'))]
T.turn(pimo, 330, -20)
T.arm(pimo, 'L', 332, 0, None)
T.arm(pimo, 'L', 338, fwd=-50, out=70)
T.rest_arm(pimo, 'L', 380)
gesture(pimo, 'breathe', 430)
for i, o in enumerate(mesa_ch + pel_ch):
    f = 456 + i * 9
    K(o, 'location', f - 1, tuple(o.location))
    K(o, 'location', f + 4, tuple(o.location + Vector((0, 0, 0.12))))
    K(o, 'location', f + 9, tuple(o.location))

T.turn(tuki, 526, 25)
for o, f in zip(mesa_ch + pel_ch, (531, 548, 570, 582, 600)):
    clap_at(tuki, f)
    K(o, 'location', f - 1, tuple(o.location))
    K(o, 'location', f + 3, tuple(o.location + Vector((0, 0, 0.16))))
    K(o, 'location', f + 9, tuple(o.location))
rest(tuki, 612)
gesture(pimo, 'sway', 560)

T.turn(tuki, 650, 10)
for sd in ('L', 'R'):
    T.arm(tuki, sd, 656, fwd=-60, out=8)
    T.arm(tuki, sd, 670, fwd=-60, out=8)
    T.arm(tuki, sd, 680, fwd=-55, out=70)
    T.arm(tuki, sd, 724, fwd=-55, out=70)
for k, f in enumerate(range(684, 720, 9)):
    T.turn(tuki, f, 10 + (12 if k % 2 else -12))
T.turn(tuki, 726, 15)
rest(tuki, 732)
for f in (752, 764):
    clap_at(tuki, f)
rest(tuki, 776)
confetti(758, (0.0, -1.5, 2.4), n=22, spread=2.0)
gesture(pimo, 'hops', 756)
C.blink(tuki, 700)

T.lines(EID, LINES)
T.blinks(tuki, (50, 150, 300, 400, 480, 620, 740))
T.blinks(pimo, (40, 130, 250, 360, 470, 580, 690))
