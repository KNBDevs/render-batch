from stage import *
from episodes.coche_globo_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'coche_globo'
Z0 = 0.08
ZT = 0.1
auto_dress(EID, ENV)
VIO = (0.85, 0.45, 1.0)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, VIO, 1.15), (80, VIO, 1.15), (92, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.55, 0.3, 0.8, 1)), (80, (0.55, 0.3, 0.8, 1)), (92, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

YS, YM, YF, YE = -2.2, -1.1, 0.7, 0.5
TW = 1.0
CS = 1.8
track = C.empty('race_track', None, (0, 0, 0))
TRK = M((0.42, 0.75, 1.0), rough=0.3, coat=0.7)
RAIL = M((1.0, 0.62, 0.3), rough=0.35, coat=0.8)
WH = M((0.99, 0.98, 0.95), rough=0.4, coat=0.5)
YEL = M((1.0, 0.85, 0.3), rough=0.4, coat=0.6)
C.rounded_box('bed', (0, -0.85, ZT / 2), (TW, 4.0, ZT), 0.08, TRK, track)
for sx in (-1, 1):
    C.rounded_box('rail', (sx * (TW / 2 + 0.02), -0.85, ZT + 0.015), (0.05, 4.02, 0.06), 0.4, RAIL, track)
C.rounded_box('start', (0, YS + 0.54, ZT + 0.002), (TW - 0.04, 0.05, 0.006), 0.3, WH, track)
for k in range(7):
    y = YS + 0.75 + k * 0.32
    if abs(y + 0.5) > 0.12 and y < YF - 0.15:
        C.rounded_box('dash', (0, y, ZT + 0.002), (0.04, 0.14, 0.006), 0.3, WH, track)
C.rounded_box('half', (0, -0.5, ZT + 0.002), (TW - 0.04, 0.06, 0.006), 0.3, YEL, track)
spawn('finish_line', 0, 5701, 'candy', (0, YF, ZT), 0.54, 0)

car = spawn('balloon_racer', 0, 5702, 'candy', (0, YS, ZT), CS, 0)
MZ = car['mount'][2] * CS
AX = [o for o in car.children if o.name.startswith('axle')]
BALM = M((1.0, 0.3, 0.22), rough=0.18, coat=1.0)
bal = C.empty('racer_balloon', car, (0, 0.02, car['mount'][2]))
C.sphere('bb', (0, 0, 0.92), (1.0, 1.1, 1.0), BALM, bal, 48)
C.sphere('shine', (-0.38, -0.55, 1.35), (0.16, 0.06, 0.24), M((1, 1, 1), rough=0.1, coat=1.0, emit=0.6), bal, 16)
C.sphere('neck', (0, 0.02, car['mount'][2]), (0.03, 0.03, 0.035), BALM, car, 16)
RB = {}


def balloon(f, r):
    r = max(r, 0.001)
    K(bal, 'scale', f, (r, r, r))
    RB[f] = r


def carpos(f, y, rz=0.0, z=0.0):
    K(car, 'location', f, (0, y, ZT + z))
    K(car, 'rotation_euler', f, (0, math.radians(rz), 0))
    for a in AX:
        K(a, 'rotation_euler', f, (-(y - YS) / (0.075 * CS), 0, 0))


PUFF = MA((1.0, 1.0, 1.0), 0.55, rough=0.6, emit=0.4)
rnd = random.Random(5703)


def puff(fs, p, d, s=0.05, life=14):
    o = C.sphere('puff', tuple(p), (1, 1, 1), PUFF, None, 16)
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', fs - 1, (0, 0, 0))
    K(o, 'scale', fs + 3, (s, s, s))
    K(o, 'scale', fs + life, (0, 0, 0))
    K(o, 'location', fs, tuple(p))
    K(o, 'location', fs + life, tuple(Vector(p) + Vector(d)))


def run(f0, y0, y1, n, r0, rest=0.03):
    for k in range(0, n + 1, 2):
        u = k / n
        y = y0 + (y1 - y0) * (1 - (1 - u) ** 2)
        carpos(f0 + k, y)
        balloon(f0 + k, rest + (r0 - rest) * (1 - u) ** 0.8)
        if k % 4 == 0 and u < 0.85:
            j = rnd.uniform(-0.03, 0.03)
            puff(f0 + k, (j, y - 0.56, ZT + MZ - 0.03), (j * 3, -0.7, 0.08), 0.05 + 0.06 * (1 - u))


tuki = make('tuki', 1.25)
ruki = make('ruki', 1.15)
TK, RK = Vector((-0.9, -1.45, Z0)), Vector((0.95, -1.45, Z0))

carpos(0, YS)
balloon(0, 0.0)
for f in range(0, 80, 8):
    carpos(f + 4, YS, 2 if (f // 8) % 2 else -2)
    carpos(f + 8, YS, 0)
T.place(tuki, 0, (0, -3.1, 0.0))
T.turn(tuki, 0, 180)
S(tuki, 0, (1.08, 1.08, 0.86))
for f in range(6, 76, 12):
    for i in range(3):
        puff(f + i * 3, (rnd.uniform(-0.04, 0.04), -2.86, 0.7), (0, 0.24, -0.4), 0.075, 12)
S(tuki, 84, (1.08, 1.08, 0.86))
S(tuki, 86, (1, 1, 1))
T.place(tuki, 85, (0, -3.1, 0.0))
T.place(tuki, 86, TK)
T.turn(tuki, 85, 180)
T.turn(tuki, 86, 25)
T.place(ruki, 0, (2.6, -1.0, Z0))
T.place(ruki, 86, (2.6, -1.0, Z0))
T.place(ruki, 88, RK)
T.turn(ruki, 0, -25)

pump = C.empty('hand_pump', None, (RK.x - 0.3, RK.y - 0.36, Z0))
K(pump, 'location', 0, (3.5, -1.0, Z0))
K(pump, 'location', 87, (3.5, -1.0, Z0))
K(pump, 'location', 88, (RK.x - 0.3, RK.y - 0.36, Z0))
PB = M((0.3, 0.75, 0.55), rough=0.35, coat=0.8)
PH = M((1.0, 0.85, 0.3), rough=0.35, coat=0.8)
C.rounded_box('foot', (0, 0, 0.02), (0.26, 0.12, 0.04), 0.4, PH, pump)
C.lathe('barrel', [(0.03, 0.0), (0.03, 0.055), (0.2, 0.06), (0.42, 0.06), (0.47, 0.045), (0.5, 0.0)], PB, pump, segs=40)
for z in (0.12, 0.3):
    C.tube('band', [(math.cos(k * 6.2832 / 32) * 0.062, math.sin(k * 6.2832 / 32) * 0.062, z) for k in range(33)], 0.008, PH, pump)
hdl = C.empty('pump_handle', pump, (0, 0, 0.0))
C.tube('rod', [(0, 0, 0.45), (0, 0, 0.66)], 0.014, WH, hdl)
C.tube('grip', [(-0.13, 0, 0.66), (0.13, 0, 0.66)], 0.03, PH, hdl)
for sx in (-1, 1):
    C.sphere('cap', (sx * 0.135, 0, 0.66), (0.034, 0.034, 0.034), PB, hdl, 16)
HZ = ZT + MZ - Z0 - 0.04
HY = YS - 0.54 - pump.location.y
hose = C.tube('hose', [(0.0, -0.05, 0.05), (-0.1, -0.2, 0.03), (-0.4, HY + 0.1, 0.04), (-0.7, HY + 0.02, HZ - 0.03), (-pump.location.x, HY, HZ)], 0.018, M((0.35, 0.35, 0.45), rough=0.5, coat=0.3), pump)


def hose_vis(f, on):
    hose.hide_render = not on
    hose.keyframe_insert('hide_render', frame=f)


hose_vis(0, False)
hose_vis(130, True)


def pumping(f0, n, r0, r1, per=16):
    for i in range(n):
        f = f0 + i * per
        K(hdl, 'location', f, (0, 0, 0.0))
        K(hdl, 'location', f + per // 2, (0, 0, -0.16))
        K(hdl, 'location', f + per, (0, 0, 0.0))
        for side in ('L', 'R'):
            T.arm(ruki, side, f, fwd=-62, out=28)
            T.arm(ruki, side, f + per // 2, fwd=-38, out=28)
            T.arm(ruki, side, f + per, fwd=-62, out=28)
        balloon(f + per // 2 + 2, r0 + (r1 - r0) * (i + 1) / n)
    for side in ('L', 'R'):
        T.rest_arm(ruki, side, f0 + n * per + 6)


balloon(138, 0.0)
balloon(146, 0.045)
pumping(300, 2, 0.045, 0.085, 20)
carpos(340, YS)
balloon(344, 0.085)
hose_vis(345, False)
run(346, YS, YM, 52, 0.085)
carpos(468, YM)
carpos(470, YS)
balloon(468, 0.03)
balloon(470, 0.045)
hose_vis(470, True)
pumping(476, 5, 0.045, 0.17, 16)
carpos(554, YS)
balloon(554, 0.17)
hose_vis(555, False)
run(556, YS, YE, 72, 0.17)
carpos(662, YE)
balloon(662, 0.03)
carpos(664, YS)
balloon(664, 0.17)
YX = YS + 1.0
run(722, YS, YX, 64, 0.17, 0.08)
carpos(786, YX)
balloon(786, 0.08)
carpos(788, YE)
balloon(788, 0.03)
carpos(TOTAL - 1, YE)
balloon(TOTAL - 1, 0.03)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2, rz=0.0):
    e = C.empty('lab', None, loc, (0, 0, math.radians(rz)))
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


def arrow(rgb, loc, sign, f_in, f_out, rz=0.0, ln=0.42):
    e = C.empty('arrow', None, loc, (math.radians(-90 * sign), 0, math.radians(rz)))
    m = M(rgb, rough=0.3, coat=0.8, emit=0.35)
    C.tube('shaft', [(0, 0, 0), (0, 0, ln)], 0.03, m, e)
    C.lathe('head', [(ln - 0.01, 0.0), (ln - 0.01, 0.075), (ln + 0.14, 0.0)], m, e, segs=32)
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


def follow(objs, f0, n, y0, y1):
    for o in objs:
        p0 = Vector(o.location)
        K(o, 'location', f0, tuple(p0))
        for k in range(0, n + 1, 2):
            u = k / n
            K(o, 'location', f0 + k, tuple(p0 + Vector((0, (y1 - y0) * (1 - (1 - u) ** 2), 0))))


BL, OR = (0.1, 0.35, 0.85), (0.9, 0.35, 0.05)
label('¿POCO AIRE?', BL, (-0.6, -0.9, 1.7), 1.4, 214, 296, 0.36, 0.24)
label('¿MUCHO AIRE?', OR, (0.6, -0.6, 2.05), 1.5, 222, 296, 0.36, 0.24)
label('POCO AIRE', BL, (0.0, YM + 0.2, ZT + 1.0), 1.25, 398, 466, 0.32, 0.22)
label('MUCHO AIRE', OR, (-0.6, YF + 0.3, ZT + 1.2), 1.3, 590, 658, 0.32, 0.21)
label('¡META!', (0.05, 0.5, 0.2), (0.6, YF + 0.3, ZT + 1.2), 0.9, 596, 658, 0.32, 0.23)
EX = [arrow((0.2, 0.55, 1.0), (0, YS - 0.55, ZT + MZ + 0.55), -1, 690, 776, 0, 0.4),
      label('AIRE', BL, (0.02, YS - 0.5, ZT + MZ + 0.92), 0.7, 692, 776, 0.28, 0.2, -90),
      arrow((1.0, 0.55, 0.15), (0, YS + 0.55, ZT + MZ + 0.55), 1, 708, 776, 0, 0.4),
      label('¡EMPUJA!', OR, (0.02, YS + 0.55, ZT + MZ + 0.92), 1.05, 710, 776, 0.28, 0.2, -90)]
follow(EX, 722, 64, YS, YS + 1.0)

OP = ((0.45, -0.95, 0.5), (0.0, -2.9, 0.58), 24)
W = ((0.35, -5.0, 2.35), (0.0, -1.0, 0.55), 25)
WQ = ((0.35, -4.9, 2.3), (0.0, -1.05, 0.52), 25)
SIDE = ((-2.75, -2.05, 0.85), (0.0, -2.05, 0.72), 24)
SIDE2 = ((-2.75, -1.2, 0.85), (0.0, -1.2, 0.72), 24)
FIN = ((0.9, -1.7, 1.35), (0.0, 0.75, 0.5), 26)
for a, b, pose in ((0, 88, OP), (90, 296, W), (298, 468, W), (470, 662, WQ), (664, 722, SIDE), (786, 786, SIDE2), (788, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

T.arm(ruki, 'R', 96, 0, None)
T.arm(ruki, 'R', 102, fwd=-110, out=35)
T.arm(ruki, 'R', 150, fwd=-110, out=35)
T.rest_arm(ruki, 'R', 158)
T.arm(tuki, 'L', 206, 0, None)
T.arm(tuki, 'L', 212, fwd=-100, out=40)
T.arm(tuki, 'L', 280, fwd=-100, out=40)
T.rest_arm(tuki, 'L', 288)
gesture(tuki, 'hops', 404)
T.arm(ruki, 'L', 412, 0, None)
T.arm(ruki, 'L', 418, fwd=-95, out=45)
T.arm(ruki, 'L', 462, fwd=-95, out=45)
T.rest_arm(ruki, 'L', 470)
gesture(tuki, 'hops', 600)
T.place(tuki, 662, TK)
T.place(tuki, 664, (-0.8, 1.35, 0.0))
T.turn(tuki, 664, 0)
T.place(ruki, 662, RK)
T.place(ruki, 664, (1.3, -1.15, Z0))
T.turn(ruki, 662, -25)
T.turn(ruki, 664, -90)
T.arm(ruki, 'R', 688, 0, None)
T.arm(ruki, 'R', 694, fwd=-90, out=50)
T.arm(ruki, 'R', 760, fwd=-90, out=50)
T.rest_arm(ruki, 'R', 768)
T.place(ruki, 786, (1.3, -1.15, Z0))
T.place(ruki, 788, (0.82, 1.4, 0.0))
T.turn(ruki, 786, -90)
T.turn(ruki, 788, -15)
T.turn(tuki, 788, 15)
gesture(tuki, 'hops', 830)
gesture(ruki, 'hops', 834)
confetti(842, (0, YF + 0.3, 1.6), n=20, spread=1.0)
C.wave(tuki, 'R', 856, cycles=2, period=8)
C.wave(ruki, 'L', 856, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(tuki, (48, 160, 300, 450, 560, 700, 820))
T.blinks(ruki, (70, 190, 340, 500, 640, 760, 870))
