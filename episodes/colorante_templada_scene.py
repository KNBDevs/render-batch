from stage import *
from episodes.colorante_templada_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'colorante_templada'
Z0 = 0.08
auto_dress(EID, ENV)
TINT = (0.45, 0.85, 1.0)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, TINT, 1.1), (80, TINT, 1.1), (94, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.25, 0.6, 0.85, 1)), (80, (0.25, 0.6, 0.85, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

rnd = random.Random(6601)
TS = 0.8
spawn('low_table', 1, 6603, 'pastel', (0.0, -1.6, Z0), TS, 0)
ZT = Z0 + 0.62 * TS
GL = MA((0.92, 0.97, 1.0), 0.035)
R, TH, H, WL = 0.23, 0.012, 0.5, 0.41
RI = R - TH - 0.006
WT = ZT + WL
BLUE = (0.05, 0.25, 1.0)


def ring(rr, z, n=64):
    return [(math.cos(k * 6.2832 / n) * rr, math.sin(k * 6.2832 / n) * rr, z) for k in range(n + 1)]


def glass(name, x, y, water_rgb, band_rgb):
    g = C.empty(name, None, (x, y, ZT))
    out = [(0, 0.0), (0, R - 0.02), (0.02, R), (H - 0.04, R + 0.01), (H, R + 0.03), (H + 0.012, R + 0.03)]
    inn = [(H + 0.012, R - TH + 0.03), (H - 0.03, R - TH + 0.01), (0.03, R - TH), (0.03, 0.0)]
    C.lathe('glass', out + inn, GL, g, segs=64)
    C.tube('band', ring(R + 0.008, 0.07), 0.014, M(band_rgb, rough=0.35, coat=0.7), g)
    C.tube('band2', ring(R + 0.01, 0.1), 0.008, M((1.0, 1.0, 1.0), rough=0.35, coat=0.7), g)
    C.lathe('water', [(0.03, 0.0), (0.03, RI), (WL, RI + 0.008), (WL, 0.0)], MA(water_rgb, 0.16, rough=0.05), g, segs=56)
    C.tube('surface', ring(RI + 0.004, WL), 0.007, MA(water_rgb, 0.75, rough=0.05, emit=0.3), g)
    return g


GA, GB = Vector((-0.29, -1.64, 0)), Vector((0.29, -1.64, 0))
ga = glass('cold', GA.x, GA.y, (0.7, 0.9, 1.0), (0.3, 0.6, 1.0))
gb = glass('warm', GB.x, GB.y, (1.0, 0.92, 0.8), (1.0, 0.55, 0.2))
ICE = MA((0.85, 0.95, 1.0), 0.45, rough=0.1, emit=0.15)
for k, (dx, dy, rz) in enumerate(((-0.08, 0.05, 0.3), (0.09, -0.02, -0.5))):
    ie = C.empty('ice_e', ga, (dx, dy, WL - 0.01), (0, 0, rz))
    C.rounded_box('ice', (0, 0, 0), (0.1, 0.1, 0.09), 0.45, ICE, ie)
SUN = M((1.0, 0.6, 0.15), rough=0.35, coat=0.7, emit=0.2)
for k in range(3):
    xx = -0.09 + k * 0.09
    C.tube('wave', [(xx + 0.018 * math.sin(t * 3.0), -0.05, H + 0.06 + t * 0.045) for t in range(5)], 0.009, SUN, gb)

CB_ = MA(BLUE, 0.7, rough=0.08, emit=0.45)
CB2 = MA(BLUE, 0.28, rough=0.08, emit=0.15)
ca = C.empty('cold_thread', ga, (0.0, 0.0, WL - 0.005))
C.sphere('blob', (0, 0, 0), (0.05, 0.05, 0.025), CB_, ca, 20)
th = C.empty('th', ca, (0, 0, 0))
C.tube('t', [(0.0, 0, 0), (0.012, 0, -0.33), (-0.01, 0, -0.66), (0.006, 0, -1.0)], 0.018, CB_, th)
K(ca, 'scale', 0, (0, 0, 0))
K(ca, 'scale', 18, (0, 0, 0))
K(ca, 'scale', 22, (1, 1, 1))
K(th, 'scale', 18, (1, 1, 0.02))
K(th, 'scale', 90, (1, 1, 0.08))
K(th, 'scale', 600, (1.3, 1.3, 0.22))
K(th, 'scale', 900, (1.4, 1.4, 0.25))

cw = C.empty('warm_tint', gb, (0.0, 0.0, WL - 0.006))
C.lathe('tint', [(-WL + 0.035, 0.0), (-WL + 0.035, RI - 0.01), (0.0, RI - 0.008), (0.0, 0.0)], MA(BLUE, 0.68, rough=0.06, emit=0.5), cw, segs=48)
K(cw, 'scale', 0, (0, 0, 0))
K(cw, 'scale', 312, (0, 0, 0))
K(cw, 'scale', 314, (0.12, 0.12, 0.05))
K(cw, 'scale', 336, (0.55, 0.55, 0.45))
K(cw, 'scale', 366, (1, 1, 1))
for k in range(7):
    a = k * 6.2832 / 7 + 0.3
    sw = C.empty('swirl', gb, (0, 0, WL - 0.02))
    C.sphere('s', (0, 0, 0), (0.07, 0.07, 0.055), CB2, sw, 16)
    K(sw, 'scale', 0, (0, 0, 0))
    K(sw, 'scale', 313, (0, 0, 0))
    K(sw, 'scale', 318, (0.4, 0.4, 0.4))
    K(sw, 'location', 314, (0, 0, WL - 0.02))
    K(sw, 'location', 344, (math.cos(a) * 0.1, math.sin(a) * 0.1, WL - 0.08 - 0.04 * (k % 3)))
    K(sw, 'location', 366, (math.cos(a + 0.8) * 0.13, math.sin(a + 0.8) * 0.13, 0.12 + 0.04 * (k % 4)))
    K(sw, 'scale', 344, (1.2, 1.2, 1.2))
    K(sw, 'scale', 366, (1.4, 1.4, 1.4))
    K(sw, 'scale', 372, (0, 0, 0))

RUB = M((1.0, 0.4, 0.45), rough=0.45, coat=0.6)
dr = C.empty('dropper', None, (GA.x, GA.y, ZT + 0.82))
C.lathe('tube', [(-0.3, 0.0), (-0.3, 0.008), (-0.27, 0.022), (0.0, 0.026), (0.0, 0.0)], MA((0.9, 0.97, 1.0), 0.25, rough=0.05), dr, segs=32)
C.lathe('ink', [(-0.27, 0.0), (-0.27, 0.012), (-0.12, 0.016), (-0.12, 0.0)], MA(BLUE, 0.8, rough=0.1, emit=0.2), dr, segs=24)
C.tube('collar', ring(0.03, 0.0, 32), 0.012, RUB, dr)
bulb = C.empty('bulb', dr, (0, 0, 0.0))
C.lathe('b', [(0.0, 0.0), (0.0, 0.034), (0.03, 0.05), (0.12, 0.052), (0.17, 0.035), (0.19, 0.0)], RUB, bulb, segs=36)
C.tube('rib', ring(0.052, 0.07, 36), 0.006, M((1.0, 0.75, 0.8), rough=0.45, coat=0.6), bulb)
T.pop_in(dr, 2, 1.0, 6)
for f0 in (10, 300):
    K(bulb, 'scale', f0, (1, 1, 1))
    K(bulb, 'scale', f0 + 4, (0.72, 0.72, 0.92))
    K(bulb, 'scale', f0 + 10, (1, 1, 1))
K(dr, 'location', 60, (GA.x, GA.y, ZT + 0.82))
K(dr, 'location', 70, (-0.05, -1.45, ZT + 0.62))
K(dr, 'location', 286, (-0.05, -1.45, ZT + 0.62))
K(dr, 'location', 296, (GB.x, GB.y, ZT + 0.82))
K(dr, 'location', 330, (GB.x, GB.y, ZT + 0.82))
K(dr, 'location', 340, (0.02, -1.42, ZT + 0.62))
DROP = MA(BLUE, 0.85, rough=0.05, emit=0.3)
for x0, f0 in ((GA.x, 14), (GB.x, 304)):
    d = C.empty('drop', None, (x0, GA.y, ZT + 0.5))
    C.sphere('d', (0, 0, 0), (0.02, 0.02, 0.03), DROP, d, 12)
    K(d, 'scale', 0, (0, 0, 0))
    K(d, 'scale', f0, (0, 0, 0))
    K(d, 'scale', f0 + 1, (1, 1, 1))
    K(d, 'location', f0, (x0, GA.y, ZT + 0.5))
    K(d, 'location', f0 + 8, (x0, GA.y, WT))
    K(d, 'scale', f0 + 8, (1, 1, 1))
    K(d, 'scale', f0 + 9, (0, 0, 0))

bt = C.empty('ink_bottle', None, (0.0, -1.38, ZT))
C.lathe('body', [(0, 0.0), (0, 0.075), (0.02, 0.085), (0.15, 0.085), (0.19, 0.05), (0.22, 0.03), (0.22, 0.0)], MA((0.4, 0.6, 1.0), 0.45, rough=0.08), bt, segs=40)
C.lathe('liq', [(0.012, 0.0), (0.012, 0.07), (0.12, 0.07), (0.12, 0.0)], MA(BLUE, 0.85, rough=0.1, emit=0.15), bt, segs=32)
C.lathe('cap', [(0.22, 0.0), (0.22, 0.036), (0.27, 0.036), (0.28, 0.0)], RUB, bt, segs=24)
C.sphere('drop_icon', (0, -0.087, 0.1), (0.025, 0.01, 0.034), M((1.0, 1.0, 1.0), rough=0.4, coat=0.4, emit=0.2), bt, 12)
T.pop_in(bt, 104, 1.0, 8)

moki = make('moki', 1.1)
tuki = make('tuki', 1.1)
MP, TP = Vector((-1.03, -1.6, Z0)), Vector((1.03, -1.6, Z0))
T.place(moki, 0, MP)
T.turn(moki, 0, 25)
T.place(tuki, 0, TP)
T.turn(tuki, 0, -25)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


BC, OC, GC = (0.1, 0.3, 0.85), (0.85, 0.35, 0.05), (0.05, 0.42, 0.15)
label('FRÍA', BC, (GA.x, -1.95, ZT + 0.62), 0.5, 120, 766, 0.2, 0.13)
label('TEMPLADA', OC, (GB.x, -1.95, ZT + 0.62), 0.66, 128, 766, 0.2, 0.12)
label('¿FRÍA?', BC, (-0.45, -1.1, 2.0), 0.72, 216, 296, 0.32, 0.2)
label('¿TEMPLADA?', OC, (0.5, -0.9, 2.15), 1.02, 224, 296, 0.32, 0.18)
label('1 MINUTO DESPUÉS', GC, (0.3, -1.95, ZT + 1.3), 1.0, 330, 476, 0.18, 0.1)
label('1 MINUTO DESPUÉS', GC, (-0.35, -1.95, ZT + 1.3), 1.0, 480, 594, 0.18, 0.1)
label('¡RÁPIDO!', OC, (GB.x, -2.0, ZT + 1.02), 0.7, 384, 470, 0.24, 0.15)
label('¡DESPACITO!', BC, (GA.x, -2.0, ZT + 1.02), 0.86, 486, 594, 0.24, 0.14)

exp = C.empty('diagram', None, (0.0, -2.1, 1.12))
C.rounded_box('panel', (0, 0.04, 0.4), (1.16, 0.03, 0.86), 0.4, M((0.85, 0.93, 1.0), rough=0.5, coat=0.3), exp)
C.rounded_box('divider', (0, 0.0, 0.38), (0.025, 0.03, 0.72), 0.4, M((1.0, 1.0, 1.0), rough=0.5, coat=0.3), exp)
WD = M((0.55, 0.8, 1.0), rough=0.4, coat=0.4, emit=0.15)
WW = M((1.0, 0.75, 0.5), rough=0.4, coat=0.4, emit=0.15)
CD = M(BLUE, rough=0.3, coat=0.6, emit=0.3)
for side, mat, step, amp in ((-1, WD, 18, 0.012), (1, WW, 5, 0.04)):
    cx = side * 0.28
    for k in range(12):
        bx, bz = cx + ((k % 4) - 1.5) * 0.11, 0.12 + (k // 4) * 0.13
        d = C.empty('mol', exp, (bx, -0.03, bz))
        C.sphere('m', (0, 0, 0), (0.035,) * 3, mat, d, 12)
        f = 604
        while f < 770:
            K(d, 'location', f, (bx + rnd.uniform(-amp, amp), -0.03, bz + rnd.uniform(-amp, amp)))
            f += step
    for k in range(3):
        d = C.empty('ink', exp, (cx, -0.035, 0.52))
        C.sphere('c', (0, 0, 0), (0.04,) * 3, CD, d, 12)
        a = k * 2.094 + 0.5
        reach = 0.04 if side < 0 else 0.2
        K(d, 'location', 620, (cx + math.cos(a) * 0.02, -0.035, 0.52 + math.sin(a) * 0.02))
        K(d, 'location', 740, (cx + math.cos(a) * reach, -0.035, 0.4 + math.sin(a) * reach))
T.pop_in(exp, 604, 1.2, 10)
T.pop_out(exp, 764, 1.2, 6)
label('FRÍA', BC, (-0.28, -2.18, 1.92), 0.5, 618, 764, 0.2, 0.13)
label('TEMPLADA', OC, (0.28, -2.18, 1.92), 0.66, 632, 764, 0.2, 0.12)
label('¡DESPACITO!', BC, (-0.48, -1.9, 1.62), 0.92, 790, TOTAL + 10, 0.3, 0.17)
label('¡RAPIDÍSIMO!', OC, (0.5, -1.9, 1.62), 1.02, 806, TOTAL + 10, 0.3, 0.16)
confetti(846, (0, -1.6, 1.6), n=30, spread=1.6)

OP = ((-0.15, -3.55, 2.35), (-0.5, -1.62, 0.82), 30)
W = ((0.0, -5.5, 1.8), (0.0, -1.6, 0.95), 28)
CB = ((0.45, -4.3, 1.25), (0.38, -1.6, 0.9), 30)
CA = ((-0.45, -4.3, 1.25), (-0.38, -1.6, 0.9), 30)
EXP = ((0.0, -4.75, 1.75), (0.0, -1.85, 1.48), 28)
FIN = ((0.0, -5.6, 1.72), (0.0, -1.6, 1.0), 28)
for a, b, pose in ((0, 88, OP), (90, 290, W), (292, 476, CB), (478, 594, CA), (596, 766, EXP), (768, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

T.arm(moki, 'R', 4, 0, None)
T.arm(moki, 'R', 12, fwd=-75, out=25)
T.arm(moki, 'R', 56, fwd=-75, out=25)
T.rest_arm(moki, 'R', 68)
gesture(moki, 'breathe', 30)
T.arm(tuki, 'L', 96, 0, None)
T.arm(tuki, 'L', 108, fwd=-70, out=30)
T.arm(tuki, 'L', 140, fwd=-70, out=30)
T.rest_arm(tuki, 'L', 152)
T.arm(tuki, 'L', 288, 0, None)
T.arm(tuki, 'L', 298, fwd=-80, out=20)
T.arm(tuki, 'L', 330, fwd=-80, out=20)
T.rest_arm(tuki, 'L', 342)
gesture(tuki, 'hops', 382)
gesture(moki, 'hops', 488)
gesture(tuki, 'breathe', 600)
T.arm(moki, 'R', 770, 0, None)
T.arm(moki, 'R', 780, fwd=-60, out=60)
T.arm(moki, 'R', 830, fwd=-60, out=60)
T.rest_arm(moki, 'R', 840)
C.wave(moki, 'L', 850, cycles=2, period=10)
C.wave(tuki, 'R', 846, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(moki, (50, 170, 320, 450, 580, 720, 860))
T.blinks(tuki, (60, 180, 340, 480, 640, 760))
