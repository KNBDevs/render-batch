from stage import *
from episodes.globo_papelitos_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, glyph
EID = 'globo_papelitos'
Z0 = 0.08
auto_dress(EID, ENV)
TEAL = (0.3, 0.95, 0.9)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, TEAL, 1.2), (58, TEAL, 1.2), (74, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.15, 0.7, 0.72, 1)), (58, (0.15, 0.7, 0.72, 1)), (74, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

TX, TY = 0.15, -1.45
spawn('low_table', 0, 5601, 'pastel', (TX, TY, Z0), 1.0, 0)
TOP = Z0 + 0.62
SX, PX, RY = -0.22, 0.48, -1.42

sca = C.empty('wool_scarf', None, (SX, RY, TOP))
S1, S2 = M((0.92, 0.3, 0.38), rough=0.75, coat=0.1), M((1.0, 0.86, 0.5), rough=0.75, coat=0.1)
for lay, (z, dx) in enumerate(((0.022, 0.0), (0.062, 0.05))):
    for i in range(6):
        x = -0.3 + dx + i * 0.11
        C.rounded_box('seg', (x, 0, z), (0.118, 0.3, 0.04), 0.12, S1 if i % 2 == 0 else S2, sca)
        for j in range(4):
            C.tube('rib', [(x - 0.045, -0.105 + j * 0.07, z + 0.021), (x + 0.045, -0.105 + j * 0.07, z + 0.021)], 0.006, S2 if i % 2 == 0 else S1, sca)
for j in range(6):
    y = -0.11 + j * 0.044
    C.tube('fringe', [(0.33 + 0.05, y, 0.06), (0.43, y + 0.01, 0.025), (0.47, y, 0.012)], 0.009, S1, sca)
    C.sphere('tip', (0.47, y, 0.012), (0.014, 0.014, 0.014), S2, sca, 12)

tray = C.empty('paper_tray', None, (PX, RY, TOP))
TM = M((0.55, 0.82, 1.0), rough=0.4, coat=0.7)
C.lathe('tray', [(0.0, 0.0), (0.0, 0.27), (0.01, 0.285), (0.045, 0.29), (0.05, 0.275), (0.02, 0.255), (0.012, 0.0)], TM, tray, segs=56)
for k in range(10):
    a = k * 6.2832 / 10
    C.sphere('bead', (math.cos(a) * 0.282, math.sin(a) * 0.282, 0.05), (0.018, 0.018, 0.018), M((1.0, 0.95, 0.6), rough=0.35, coat=0.7), tray, 12)

GS = 1.0
bal = spawn('big_balloon', 0, 5602, 'candy', (0, 0, 0), GS, 0)
for o in bal.children:
    if o.name.startswith(('body', 'knot')):
        o.data.materials[0] = M((1.0, 0.42, 0.22), rough=0.18, coat=1.0)
BOY = -0.56
TOX = -0.5
tuki = make('tuki', 1.4)
bolita = make('bolita', 1.2)
TKY = RY - BOY
ARM = {}


def hold(f, x, lift, tilt=0.0, fwd=None):
    T.place(tuki, f, Vector((x + TOX, TKY, Z0)))
    K(bal, 'location', f, (x, RY, Z0 + lift))
    K(bal, 'rotation_euler', f, (0, math.radians(tilt), 0))
    fw = fwd if fwd is not None else -70 - (lift - 0.6) * 90
    T.arm(tuki, 'R', f, fwd=fw, out=40)
    ARM[f] = (x, lift)


T.turn(tuki, 0, 0)
HI, LO, RUB = 1.0, 0.9, 0.69
for f in range(0, 60, 6):
    hold(f, PX, HI + (0.03 if (f // 6) % 2 else 0.0), 3 if (f // 6) % 2 else -3)
hold(64, PX, HI)
hold(140, PX, HI)
for k, f in enumerate(range(143, 161, 3)):
    u = (k + 1) / 6
    hold(f, PX + (SX - PX) * u, HI + (RUB - HI) * u + 0.06 * math.sin(u * 3.1416))
n = 0
for f in range(164, 236, 6):
    n += 1
    hold(f, SX + (0.13 if n % 2 else -0.13), RUB + 0.01, 8 if n % 2 else -8)
hold(238, SX, RUB)
for k, f in enumerate(range(241, 262, 3)):
    u = (k + 1) / 7
    hold(f, SX + (PX - SX) * u, RUB + (HI - RUB) * u + 0.06 * math.sin(u * 3.1416))
hold(330, PX, HI)
hold(398, PX, LO)
hold(760, PX, LO)

rnd = random.Random(5603)
PCOL = [(1.0, 0.45, 0.55), (1.0, 0.85, 0.3), (0.45, 0.85, 0.5), (0.45, 0.65, 1.0), (0.8, 0.55, 1.0), (1.0, 0.65, 0.3)]
PM = [M(c, rough=0.6, coat=0.2, emit=0.08) for c in PCOL]
BITS = []
BH = Vector((PX, RY, Z0 + LO))
for i in range(32):
    a = rnd.uniform(0, 6.2832)
    rr = 0.23 * math.sqrt(rnd.uniform(0.02, 1))
    p0 = Vector((PX + math.cos(a) * rr, RY + math.sin(a) * rr, TOP + 0.016 + rnd.uniform(0, 0.006)))
    b = C.empty('bit', None, tuple(p0), (0, 0, rnd.uniform(0, 3.1)))
    w = rnd.uniform(0.07, 0.1)
    C.rounded_box('pp', (0, 0, 0), (w, w * rnd.uniform(0.7, 1.0), 0.006), 0.2, PM[i % len(PM)], b)
    BITS.append((b, p0))
JUMP = [x for x in range(len(BITS)) if x % 6 != 5]
STUCK = {}
for n2, i in enumerate(JUMP):
    b, p0 = BITS[i]
    a = -1.5708 + rnd.uniform(-1.4, 1.4)
    z = rnd.uniform(0.03, 0.17)
    r = 0.06 + (0.25 - 0.06) * (z - 0.03) / 0.14 + 0.012
    ps = BH + Vector((math.cos(a) * r, math.sin(a) * r, z))
    f0 = 404 + (n2 * 29) % 22
    K(b, 'location', 0, tuple(p0))
    K(b, 'location', f0, tuple(p0))
    K(b, 'location', f0 + 3, tuple(p0 + Vector((0, 0, 0.03))))
    K(b, 'location', f0 + 9, tuple(ps))
    K(b, 'rotation_euler', f0, tuple(b.rotation_euler))
    K(b, 'rotation_euler', f0 + 9, (math.radians(rnd.uniform(-60, 60)), math.radians(rnd.uniform(-60, 60)), rnd.uniform(0, 3.1)))
    STUCK[i] = ps
for i in range(len(BITS)):
    if i not in STUCK:
        b, p0 = BITS[i]
        f0 = 410 + i % 10
        for d, h in ((0, 0), (3, 0.06), (6, 0)):
            K(b, 'location', f0 + d, tuple(p0 + Vector((0, 0, h))))

HEAD = Vector((PX + TOX, TKY - 0.02, Z0 + 1.33))
REM = [(760, BH, 0, -54), (774, BH + Vector((TOX * 0.5, 0.2, 0.62)), 0, -165), (788, HEAD, 0, -175), (800, HEAD, 0, -175)]
for f, p, tl, fw in REM:
    K(bal, 'location', f, tuple(p))
    K(bal, 'rotation_euler', f, (0, 0, 0))
    for i, ps in STUCK.items():
        K(BITS[i][0], 'location', f, tuple(ps + (p - BH)))
    T.arm(tuki, 'R', f, fwd=fw, out=30)
    T.arm(tuki, 'L', f, fwd=fw, out=30)
for side in ('L', 'R'):
    T.rest_arm(tuki, side, 810)
for f, dz in ((812, 0.0), (818, 0.05), (824, 0.0)):
    K(bal, 'location', f, tuple(HEAD + Vector((0, 0, dz))))
    for i, ps in STUCK.items():
        K(BITS[i][0], 'location', f, tuple(ps + (HEAD - BH) + Vector((0, 0, dz))))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, RC = (0.05, 0.42, 0.15), (0.75, 0.08, 0.15)
label('¿SÍ?', GC, (PX - 0.62, RY - 0.55, Z0 + 1.55), 0.72, 276, 396)
label('¿NO?', RC, (PX + 0.62, RY - 0.55, Z0 + 1.55), 0.72, 282, 396)
label('LANA', RC, (SX + 0.2, RY - 0.4, TOP + 0.3), 0.55, 566, 684, 0.2, 0.13)
label('¡ATRAE!', (0.05, 0.2, 0.7), (PX + 0.1, RY - 0.62, Z0 + LO + 0.78), 0.95, 576, 684, 0.24, 0.17)

OP = ((PX - 0.25, -3.05, 1.0), (PX - 0.25, RY, 0.98), 22)
OP2 = ((PX - 0.25, -2.95, 1.02), (PX - 0.25, RY, 1.0), 23)
W = ((0.48, -4.7, 1.65), (0.48, -1.5, 0.9), 19.5)
WQ = ((0.48, -4.9, 1.9), (0.48, -1.5, 1.0), 19.5)
CB = ((PX - 0.25, -3.45, 1.1), (PX - 0.25, RY, Z0 + 0.95), 28)
CL = ((0.62, -4.3, 1.3), (0.62, RY, 1.0), 20)
WE = ((0.48, -4.75, 1.75), (0.48, -1.5, 0.95), 19.5)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 240, W), (242, 350, WQ), (352, 552, CB), (554, 690, CL), (692, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

BL0 = Vector((1.25, -1.45, Z0))
T.place(bolita, 0, BL0)
T.turn(bolita, 0, -30)
T.arm(bolita, 'L', 94, 0, None)
T.arm(bolita, 'L', 100, fwd=-100, out=45)
T.arm(bolita, 'L', 160, fwd=-100, out=45)
T.rest_arm(bolita, 'L', 170)
T.arm(bolita, 'L', 410, 0, None)
T.arm(bolita, 'L', 416, fwd=-130, out=40)
T.arm(bolita, 'L', 460, fwd=-130, out=40)
T.rest_arm(bolita, 'L', 468)
gesture(bolita, 'breathe', 560)
T.arm(bolita, 'R', 560, 0, None)
T.arm(bolita, 'R', 566, fwd=-90, out=50)
T.arm(bolita, 'R', 640, fwd=-90, out=50)
T.rest_arm(bolita, 'R', 650)
gesture(bolita, 'hops', 796)
C.wave(bolita, 'L', 826, cycles=2, period=8)
C.wave(tuki, 'R', 826, cycles=2, period=8)
confetti(806, (PX, RY, Z0 + 2.0), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(tuki, (44, 150, 300, 460, 590, 700, 840))
T.blinks(bolita, (70, 190, 330, 500, 650, 790))
