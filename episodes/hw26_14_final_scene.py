from stage import *
from episodes.hw26_14_final_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props.costumes import dress
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_14_final'
Z0 = 0.08
autumn(dusk=True)
auto_dress(EID, ENV)

BD = Vector((0, -0.45, Z0))
spawn('label_board', 1, 1401, 'autumn', tuple(BD), 0.9, 0)
FY = BD.y - 0.05
ROWS = [1.24, 0.95, 0.66]
INK = (0.15, 0.2, 0.26)
CREAM = (0.98, 0.86, 0.6)
font = _font()


def mk(name, text, z, w, h, bg, ink, small=1.0):
    c = HW.card(name, text, font, (BD.x, FY, Z0 + z), w=w, h=h, bg=bg, ink=ink)
    if small != 1.0:
        tx = next(o for o in c.children if o.name.endswith('.text'))
        tx.scale = tuple(v * small for v in tx.scale)
    return c


old = [mk(f'hw{k}', 'Halloween', ROWS[k], 0.62, 0.18, CREAM, INK) for k in range(3)]
for k, c in enumerate(old):
    T.pop_in(c, 8 + 10 * k, 1.0, 10)
new = [old[0],
       mk('ts', 'Todos los Santos\ny Fieles Difuntos', ROWS[1], 0.74, 0.24, (0.62, 0.55, 0.78), (1.0, 0.97, 0.9), 0.62),
       mk('dm', 'Día de Muertos', ROWS[2], 0.68, 0.18, (0.98, 0.62, 0.2), INK)]
for k, f in ((1, 240), (2, 300)):
    o, n = old[k], new[k]
    K(o, 'scale', f, (1, 1, 1))
    K(o, 'scale', f + 6, (0, 1, 1))
    K(n, 'scale', 0, (0, 1, 1))
    K(n, 'scale', f + 6, (0, 1, 1))
    K(n, 'scale', f + 12, (1, 1, 1))

gruno = make('gruno', 1.3)
bopi = make('bopi', 1.25)
pimo = make('pimo', 1.2)
dress(gruno, 'gruno', COSTUME, 0)
dress(bopi, 'bopi', COSTUME, 1)
dress(pimo, 'pimo', COSTUME, 0)
GP = Vector((-0.95, -0.85, Z0))
BP = Vector((0.95, -0.88, Z0))
P0 = Vector((-2.8, -0.5, Z0))
P1 = Vector((0.4, -1.2, Z0))
T.place(gruno, 0, GP)
T.place(bopi, 0, BP)
T.place(pimo, 0, P0)
T.turn(gruno, 0, 30)
T.turn(bopi, 0, -30)
T.turn(pimo, 0, 60)
for side in ('L', 'R'):
    T.arm(gruno, side, 0, 0, None)
    T.arm(gruno, side, 14, fwd=-120, out=40)
    T.arm(gruno, side, 60, fwd=-120, out=40)
    T.rest_arm(gruno, side, 72)
for f, z in ((20, 0.0), (26, 0.06), (32, 0.0)):
    K(gruno['hold'], 'location', f, tuple(GP + Vector((0, 0, z))))
T.arm(bopi, 'L', 230, 0, None)
T.arm(bopi, 'L', 240, fwd=-60, out=60)
T.arm(bopi, 'L', 250, fwd=-60, out=40)
T.arm(bopi, 'L', 300, fwd=-60, out=60)
T.arm(bopi, 'L', 310, fwd=-60, out=40)
T.rest_arm(bopi, 'L', 322)
for f, a in ((236, 0), (244, 10), (296, 10), (304, -6), (316, 0)):
    K(bopi['sq'], 'rotation_euler', f, (0, math.radians(a), 0))
gesture(bopi, 'breathe', 400)
gesture(gruno, 'breathe', 380)

PM = Vector((-1.2, -1.35, Z0))
hop_to(pimo, 520, P0, PM, 12, apex=0.2)
hop_to(pimo, 534, PM, Vector((-0.4, -1.45, Z0)), 12, apex=0.2)
hop_to(pimo, 548, Vector((-0.4, -1.45, Z0)), P1, 12, apex=0.2)
T.turn(pimo, 560, -15)
C.wave(pimo, 'R', 566, cycles=2, period=8)
T.turn(gruno, 560, 30)
T.turn(gruno, 570, -10)

ST = Vector((-0.25, -1.4, Z0))
stool = spawn('mushroom_stool', 1, 1402, 'autumn', tuple(ST), 0.55, 0)
SZ = ST.z + 0.24
lan = HW.turnip_lantern('farol', (0, 0, 0), h=0.42)
G2 = Vector((-0.75, -1.15, Z0))
hop_to(gruno, 600, GP, G2, 12, apex=0.15)
HAND = Vector((0.3, -0.25, 0.45))
K(lan, 'scale', 0, (0, 0, 0))
K(lan, 'scale', 596, (0, 0, 0))
K(lan, 'scale', 604, (1, 1, 1))
K(lan, 'location', 596, tuple(GP + HAND))
K(lan, 'location', 612, tuple(G2 + HAND))
K(lan, 'location', 630, tuple(ST + Vector((0, 0, SZ + 0.12))))
K(lan, 'location', 640, tuple(ST + Vector((0, 0, SZ))))
K(lan, 'rotation_euler', 0, (0, 0, 0))
K(lan, 'location', 862, tuple(ST + Vector((0, 0, SZ))))
K(lan, 'location', 872, tuple(ST + Vector((0, 0, SZ + 0.38))))
K(lan, 'rotation_euler', 862, (0, 0, 0))
K(lan, 'rotation_euler', 876, (0, math.radians(180), 0))
K(lan, 'rotation_euler', 908, (0, math.radians(180), 0))
K(lan, 'rotation_euler', 924, (0, math.radians(360), 0))
K(lan, 'location', 926, tuple(ST + Vector((0, 0, SZ + 0.38))))
K(lan, 'location', 938, tuple(ST + Vector((0, 0, SZ))))
for side in ('L', 'R'):
    T.arm(gruno, side, 596, 0, None)
    T.arm(gruno, side, 606, fwd=-70, out=25)
    T.arm(gruno, side, 636, fwd=-70, out=25)
    T.rest_arm(gruno, side, 648)
    T.arm(gruno, side, 856, 0, None)
    T.arm(gruno, side, 866, fwd=-90, out=25)
    T.arm(gruno, side, 932, fwd=-90, out=25)
    T.rest_arm(gruno, side, 944)
T.turn(gruno, 600, 10)
T.turn(gruno, 610, 20)
for f, a in ((880, 0), (888, -8), (896, 8), (904, 0)):
    K(gruno['sq'], 'rotation_euler', f, (0, math.radians(a), 0))

crew = []
for k, (cid, x, y, st) in enumerate((('luma', -1.2, 1.5, 0), ('ruki', -0.6, 1.7, 0), ('tuki', 0.0, 1.8, 1), ('moki', 0.6, 1.7, 1), ('bolita', 1.2, 1.5, 0))):
    ch = make(cid, 0.95)
    dress(ch, cid, COSTUME, st)
    p = Vector((x, y, Z0))
    T.place(ch, 0, p)
    T.turn(ch, 0, -x * 12)
    crew.append((ch, p))
    gesture(ch, 'breathe', 100 + 37 * k)
for k, (ch, p) in enumerate(crew):
    C.wave(ch, 'R' if k % 2 else 'L', 950 + 4 * k, cycles=2, period=8)
    C.blink(ch, 120 + 90 * k)
    C.blink(ch, 700 + 50 * k)

seda = HW.spider('Seda', span=0.45)
seda['root'].location = (-1.05, 0.75, Z0)
seda['root'].rotation_euler = (0, 0, math.radians(-25))
spawn('perch_stand', 0, 1403, 'autumn', (1.2, 0.95, Z0), 1.0, 0)
velo = HW.bat('Velo', h=0.5)
velo['root'].location = (1.2, 0.95, Z0 + 0.826 - 0.05)
HW.fold_wings(velo, 0, 1.0)
HW.fold_wings(velo, 960, 1.0)
HW.fold_wings(velo, 972, 0.3)
HW.fold_wings(velo, 984, 1.0)

C.wave(bopi, 'R', 950, cycles=2, period=8)
C.wave(pimo, 'L', 954, cycles=2, period=8)

W0 = ((-0.4, -3.9, 1.45), (-0.35, -0.6, 1.0), 24)
WB = ((0, -4.5, 1.45), (0, -0.5, 0.98), 23)
WT = ((0, -0.9, 3.0), (0, 1.4, 0.85), 20)
WE = ((0, -4.8, 1.45), (0, -0.9, 0.85), 22)
camkey(0, W0)
camkey(184, W0)
camkey(200, WB)
camkey(520, WB)
camkey(752, WB)
camkey(753, WT)
camkey(856, WT)
camkey(857, WE)
camkey(864, WE)
camkey(TOTAL - 1, WE)

T.lines(EID, LINES)
T.blinks(gruno, (90, 240, 380, 520, 700, 840, 980))
T.blinks(bopi, (60, 200, 350, 480, 620, 780, 940))
T.blinks(pimo, (580, 720, 860, 990))
