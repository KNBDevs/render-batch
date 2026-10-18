from stage import *
from episodes.hw26_05_escocia_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
from props.costumes import dress
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_05_escocia'
Z0 = 0.08
autumn(dusk=True)
auto_dress(EID, ENV)

W0 = ((0, -6.3, 1.75), (0, -0.9, 1.0), 31)
WT = ((0.15, -5.1, 1.55), (0.15, -1.1, 0.95), 26)
WB = ((0.3, -5.1, 1.55), (0.3, -1.1, 0.95), 26)
camkey(0, WT)
camkey(140, WT)
camkey(152, W0)
camkey(486, W0)
camkey(496, WB)
camkey(640, WB)
camkey(652, W0)
camkey(TOTAL - 1, W0)

dr = HW.door('door', (0, -0.15, Z0), h=1.5)
hinge = dr['hinge']
mat = spawn('perform_mat', 0, 2651, 'autumn', (-0.05, -1.25, Z0), 1.6, 0)
notes = [o for o in mat.children if o.name.startswith('note')]
for o in notes:
    o.location.z += 0.35
    T.pop_in(o, 230, 1.0, 10)
    T.pop_out(o, 470, 1.0, 8)
for k, o in enumerate(notes):
    z0 = o.location.z
    for f in range(240, 470, 24):
        K(o, 'location', f + k * 6, (o.location.x, o.location.y, z0))
        K(o, 'location', f + 12 + k * 6, (o.location.x, o.location.y, z0 + 0.06))

tuki = make('tuki', 1.4)
bopi = make('bopi', 1.35)
ruki = make('ruki', 1.35)
dress(tuki, 'tuki', COSTUME, 0)
dress(bopi, 'bopi', COSTUME, 0)
dress(ruki, 'ruki', COSTUME, 0)
TP = Vector((-0.45, -1.25, Z0))
BP = Vector((0.85, -1.15, Z0))
RD = Vector((0.0, -0.05, Z0))
RO = Vector((0.12, -0.7, Z0))
T.place(tuki, 0, TP)
T.place(bopi, 0, BP)
T.place(ruki, 0, RD)
K(ruki['hold'], 'scale', 0, (0, 0, 0))
K(ruki['hold'], 'scale', 650, (0, 0, 0))
K(ruki['hold'], 'scale', 651, (1, 1, 1))
T.turn(tuki, 0, 160)
T.turn(bopi, 0, -30)

for f in (34, 44):
    T.arm(tuki, 'R', f, fwd=-100, out=10)
    T.arm(tuki, 'R', f + 5, fwd=-80, out=10)
T.rest_arm(tuki, 'R', 56)
T.turn(tuki, 70, 160)
T.turn(tuki, 84, 10)
gesture(tuki, 'sway', 92)

sc = spawn('region_sign', 0, 2652, 'autumn', (0.22, -0.6, Z0), 1.5, 0, label='Escocia')
T.pop_in(sc, 170, 1.5, 10)
T.pop_out(sc, 480, 1.5, 8)
T.turn(tuki, 200, 0)
for k in range(4):
    f = 250 + k * 50
    gesture(tuki, 'sway' if k % 2 == 0 else 'hops', f)
    T.arm(tuki, 'L', f, fwd=-100, out=60)
    T.arm(tuki, 'R', f + 12, fwd=-100, out=60)
    T.rest_arm(tuki, 'L', f + 24)
    T.rest_arm(tuki, 'R', f + 36)
T.turn(bopi, 260, -20)
gesture(bopi, 'breathe', 320)

T.turn(bopi, 496, -10)
S(bopi, 540, (1, 1, 1))
for k, f in enumerate((550, 560, 570, 585)):
    S(bopi, f, (1.06, 1.06, 0.95))
    S(bopi, f + 5, (1, 1, 1))
T.arm(bopi, 'R', 548, fwd=-120, out=40)
T.arm(bopi, 'L', 548, fwd=-120, out=40)
T.rest_arm(bopi, 'R', 600)
T.rest_arm(bopi, 'L', 600)
bm = M((0.55, 0.85, 1.0), rough=0.3, coat=0.5, emit=0.6)
for k, f in enumerate((550, 560, 570, 585)):
    d = C.empty(f'bipnote{k}', None, tuple(BP + Vector((0.1 * k - 0.15, -0.25, 1.55))))
    C.sphere(f'bipn{k}', (0, 0, 0), (0.05, 0.03, 0.05), bm, d, 14)
    T.pop_in(d, f, 1.0, 6)
    K(d, 'location', f + 24, tuple(BP + Vector((0.1 * k - 0.15, -0.25, 1.8))))
    T.pop_out(d, f + 24, 1.0, 6)
T.turn(tuki, 590, 30)

K(hinge, 'rotation_euler', 652, (0, 0, 0))
K(hinge, 'rotation_euler', 676, (0, 0, math.radians(-100)))
hop_to(ruki, 666, RD, RO, 14, apex=0.2)
hop_to(tuki, 650, TP, TP + Vector((-0.35, -0.05, 0)), 12, apex=0.2)
hop_to(bopi, 652, BP, BP + Vector((0.22, -0.1, 0)), 12, apex=0.2)
T.turn(ruki, 682, -10)
C.wave(ruki, 'L', 690, cycles=2, period=8)
T.turn(tuki, 676, 5)
T.turn(bopi, 676, -25)
for ch, f0 in ((tuki, 760), (bopi, 766), (ruki, 772)):
    gesture(ch, 'sway', f0)
T.arm(tuki, 'R', 760, fwd=-120, out=40)
T.rest_arm(tuki, 'R', 820)
gesture(tuki, 'hops', 830)
gesture(bopi, 'hops', 836)

T.lines(EID, LINES)
T.blinks(tuki, (40, 150, 260, 380, 500, 610, 720, 840))
T.blinks(bopi, (70, 190, 310, 430, 620, 750))
T.blinks(ruki, (700, 800))
