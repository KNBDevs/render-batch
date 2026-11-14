from stage import *
from episodes.botella_chorros_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'botella_chorros'
Z0 = 0.08
auto_dress(EID, ENV)
TQ = (0.45, 1.0, 0.9)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, TQ, 1.05), (80, TQ, 1.05), (94, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.2, 0.62, 0.66, 1)), (80, (0.2, 0.62, 0.66, 1)), (94, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

rnd = random.Random(7031)
JY = -1.55
BX = 0.72
SH = 0.8
ZB = Z0 + SH
R = 0.17
WL = 0.66
HT, HB = 0.52, 0.08
HX = BX - R

MINT = M((0.5, 0.86, 0.72), rough=0.4, coat=0.6)
SUN = M((1.0, 0.82, 0.38), rough=0.4, coat=0.6)
CORAL = M((1.0, 0.55, 0.5), rough=0.35, coat=0.7)
stool = C.empty('stool', None, (BX, JY, Z0))
C.rounded_box('seat', (0, 0, SH - 0.045), (0.56, 0.46, 0.09), 0.4, MINT, stool)
C.tube('seat_edge', [(0.28 * math.cos(k * 6.2832 / 48) * 1.0, 0.23 * math.sin(k * 6.2832 / 48), SH - 0.09) for k in range(49)], 0.012, CORAL, stool)
for sx in (-1, 1):
    for sy in (-1, 1):
        C.tube('leg', [(sx * 0.2, sy * 0.15, 0.03), (sx * 0.21, sy * 0.16, SH - 0.09)], 0.036, SUN, stool)
        C.sphere('foot', (sx * 0.2, sy * 0.15, 0.03), (0.05, 0.05, 0.035), CORAL, stool, 16)
C.tube('rung', [(-0.2, -0.155, 0.3), (0.2, -0.155, 0.3)], 0.022, CORAL, stool)
C.tube('rung', [(-0.2, 0.155, 0.3), (0.2, 0.155, 0.3)], 0.022, CORAL, stool)

bottle = C.empty('bottle', None, (BX, JY, ZB))
prof = [(0, 0.0), (0, R - 0.03), (0.02, R), (0.74, R), (0.84, 0.09), (0.9, 0.065), (0.92, 0.065)]
inn = [(0.92, 0.055), (0.9, 0.055), (0.84, 0.08), (0.74, R - 0.012), (0.03, R - 0.012), (0.03, 0.0)]
C.lathe('glass', prof + inn, MA((0.9, 0.97, 1.0), 0.05), bottle, segs=64)
C.lathe('cap', [(0.9, 0.0), (0.9, 0.075), (0.93, 0.082), (0.99, 0.078), (1.0, 0.06), (1.0, 0.0)], CORAL, bottle, segs=40)
C.tube('band', [(math.cos(a) * (R + 0.004), math.sin(a) * (R + 0.004), 0.3) for a in [math.pi * 0.25 + k * math.pi * 1.5 / 40 for k in range(41)]], 0.03, SUN, bottle)
wpiv = C.empty('water_piv', bottle, (0, 0, 0.03))
C.lathe('water', [(0, 0.0), (0, R - 0.018), (WL - 0.03, R - 0.018), (WL - 0.03, 0.0)], MA((0.2, 0.55, 1.0), 0.45, rough=0.05, emit=0.1), wpiv, segs=56)
K(wpiv, 'scale', 0, (1, 1, 1))
K(wpiv, 'scale', 380, (1, 1, 0.97))
K(wpiv, 'scale', TOTAL - 1, (1, 1, 0.9))
HOLE = M((0.18, 0.3, 0.5), rough=0.5)
for hz in (HT, HB):
    C.sphere('hole', (-R - 0.002, 0, hz), (0.008, 0.03, 0.03), HOLE, bottle, 16)


def tirita(name, hz, rgb):
    e = C.empty(name, None, (HX - 0.012, JY, ZB + hz))
    C.rounded_box('strip', (0, 0, 0), (0.018, 0.09, 0.16), 0.4, M(rgb, rough=0.5, coat=0.3), e)
    C.rounded_box('pad', (-0.008, 0, 0), (0.012, 0.06, 0.06), 0.4, M((1.0, 0.95, 0.88), rough=0.6, coat=0.2), e)
    for dy in (-0.028, 0.028):
        for dz in (-0.058, 0.058):
            C.sphere('dot', (-0.009, dy, dz), (0.004, 0.008, 0.008), M((1.0, 1.0, 1.0), rough=0.4), e, 8)
    return e


tt = tirita('tirita_top', HT, (1.0, 0.62, 0.72))
tb = tirita('tirita_bot', HB, (0.6, 0.78, 1.0))
K(tt, 'scale', 0, (0, 0, 0))
K(tb, 'location', 380, tuple(tb.location))
K(tb, 'location', 390, (HX - 0.2, JY + 0.15, ZB + HB + 0.15))
K(tb, 'rotation_euler', 380, (0, 0, 0))
K(tb, 'rotation_euler', 390, (0.9, -0.4, 0.6))
T.pop_out(tb, 392, 1.0, 5)

JET = MA((0.12, 0.42, 1.0), 0.9, rough=0.05, emit=0.25)
DROP = MA((0.3, 0.6, 1.0), 0.9, rough=0.05, emit=0.35)
TRAY_Z = Z0 + 0.06


def jet(name, hz, f_on, rad):
    d = WL - hz
    zh = ZB + hz
    xl = 2 * math.sqrt(d * (zh - TRAY_Z))
    piv = C.empty(name, None, (HX - 0.005, JY, zh))
    n = 28
    pts = [(-xl * k / n, 0, -(xl * k / n) ** 2 / (4 * d)) for k in range(n + 1)]
    C.tube('stream', pts, rad, JET, piv, radii=[1.0 - 0.25 * k / n for k in range(n + 1)], res=8)
    if f_on > 0:
        K(piv, 'scale', 0, (0, 0, 0))
    K(piv, 'scale', f_on, (0, 0, 0))
    K(piv, 'scale', f_on + 4, (0.45, 1, 0.45))
    K(piv, 'scale', f_on + 9, (1, 1, 1))
    per = 14
    for j in range(6):
        b = C.empty('drop', piv, (0, 0, 0))
        C.sphere('d', (0, 0, 0), (rad * 1.3, rad * 1.3, rad * 1.3), DROP, b, 10)
        f = f_on + 9 + j * per / 6.0
        while f < TOTAL:
            for u in (0.0, 0.34, 0.67, 1.0):
                x = -xl * u
                K(b, 'location', int(round(f + u * per)), (x, rnd.uniform(-0.006, 0.006), -x * x / (4 * d)))
            f += per
        if f_on > 0:
            K(b, 'scale', 0, (0, 0, 0))
            K(b, 'scale', int(f_on + 9 + j * per / 6.0), (0, 0, 0))
            K(b, 'scale', int(f_on + 10 + j * per / 6.0), (1, 1, 1))
        act = b.animation_data.action
        cv = list(act.fcurves) if hasattr(act, 'fcurves') and len(getattr(act, 'fcurves', [])) else [fc for ly in act.layers for st in ly.strips for bg_ in st.channelbags for fc in bg_.fcurves]
        for fc in cv:
            if fc.data_path == 'location':
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'
    return HX - 0.005 - xl


xt = jet('jet_top', HT, -10, 0.028)
xb = jet('jet_bot', HB, 384, 0.038)

spawn('water_tray', 0, 7032, 'pastel', (xb, JY, Z0), 1.15, 0)
for k, (x, f_on, top) in enumerate(((xt, 0, Z0 + 0.004), (xb, 392, TRAY_Z + 0.005))):
    for j in range(3):
        rg = C.empty('ripple', None, (x, JY, top))
        C.tube('r', [(math.cos(a * 6.2832 / 32) * 0.06, math.sin(a * 6.2832 / 32) * 0.05, 0) for a in range(33)], 0.007, DROP, rg)
        f = f_on + j * 6
        K(rg, 'scale', 0, (0, 0, 0))
        while f < TOTAL - 2:
            K(rg, 'scale', f, (0.3, 0.3, 1))
            K(rg, 'scale', f + 17, (1.8, 1.8, 1))
            K(rg, 'scale', f + 18, (0, 0, 0))
            f += 18
puddle = C.empty('puddle', None, (xt, JY, Z0 + 0.002))
C.sphere('pd', (0, 0, 0), (0.2, 0.16, 0.006), MA((0.35, 0.65, 1.0), 0.6, rough=0.05, emit=0.15), puddle, 32)
K(puddle, 'scale', 0, (0.3, 0.3, 1))
K(puddle, 'scale', 260, (1.0, 1.0, 1))
K(puddle, 'scale', TOTAL - 1, (1.35, 1.35, 1))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


GC, BC, RC = (0.05, 0.42, 0.15), (0.1, 0.3, 0.8), (0.8, 0.3, 0.1)
label('¿ARRIBA?', RC, (-0.3, -1.3, 1.86), 1.25, 186, 300, 0.38, 0.27)
label('¿ABAJO?', BC, (-0.3, -1.3, 1.4), 1.2, 196, 300, 0.38, 0.27)
label('¡LLEGA!', GC, (xb + 0.12, -1.95, 0.5), 0.62, 398, 490, 0.24, 0.15)

exp = C.empty('diagram', None, (0.0, -2.45, 1.12))
C.rounded_box('panel', (0, 0.04, 0.42), (1.42, 0.03, 0.96), 0.4, M((0.22, 0.55, 0.5), rough=0.7, coat=0.1), exp)
GLS = M((0.95, 0.97, 1.0), rough=0.4, coat=0.4)
WAT = M((0.15, 0.45, 0.95), rough=0.5, coat=0.3)
ARW = M((1.0, 0.82, 0.2), rough=0.4, coat=0.5, emit=0.2)
DWN = M((0.1, 0.3, 0.8), rough=0.4, coat=0.5)
C.rounded_box('ibottle', (0.36, 0.0, 0.42), (0.34, 0.02, 0.74), 0.3, GLS, exp)
C.rounded_box('iwater', (0.36, -0.012, 0.38), (0.28, 0.02, 0.6), 0.3, WAT, exp)
for k, zz in enumerate((0.6, 0.45, 0.3)):
    C.tube('down', [(0.36, -0.03, zz + 0.06), (0.36, -0.03, zz - 0.02)], 0.008 + 0.005 * k, DWN, exp)
    C.lathe('dtip', [(0.0, 0.0), (0.0, 0.022 + 0.01 * k), (-0.04, 0.0)], DWN, C.empty('t', exp, (0.36, -0.03, zz - 0.015)), segs=16)
for zz, L, rad in ((0.6, 0.18, 0.012), (0.16, 0.58, 0.03)):
    p = C.empty('arw', exp, (0.2, -0.04, zz))
    C.tube('shaft', [(0, 0, 0), (-L + 0.05, 0, 0)], rad, ARW, p)
    C.lathe('tip', [(0.0, 0.0), (0.0, rad * 2.4), (0.07, 0.0)], ARW, C.empty('t', p, (-L + 0.06, 0, 0), (0, -math.pi / 2, 0)), segs=20)
T.pop_in(exp, 574, 1.2, 10)
T.pop_out(exp, 790, 1.2, 6)
label('ARRIBA', RC, (-0.3, -2.55, 1.98), 0.6, 584, 790, 0.19, 0.12)
label('ABAJO', BC, (-0.32, -2.55, 1.06), 0.56, 600, 790, 0.19, 0.12)
label('¡EMPUJA MÁS!', GC, (0.0, -2.55, 0.86), 0.96, 650, 790, 0.19, 0.11)

label('CORTITO', RC, (xt + 0.05, -1.95, 1.0), 0.86, 806, TOTAL + 10, 0.26, 0.16)
label('LEJOS', GC, (xb + 0.05, -1.95, 0.44), 0.68, 832, TOTAL + 10, 0.26, 0.17)
confetti(866, (0, -1.6, 1.3), n=26, spread=1.5)

OP = ((-0.05, -3.9, 0.62), (-0.05, -1.5, 0.92), 18)
OM = ((-0.55, -3.7, 1.3), (-0.55, -1.45, 0.72), 26)
W = ((0.0, -4.6, 1.75), (0.0, -1.45, 0.88), 22)
RK = ((0.45, -3.8, 1.4), (0.45, -1.45, 0.85), 25)
CU = ((-0.15, -3.95, 1.25), (-0.15, -1.55, 0.78), 25)
EXP = ((0.0, -4.7, 1.62), (0.0, -2.45, 1.52), 30)
FIN = ((0.0, -4.7, 1.6), (0.0, -1.45, 0.82), 22)
for a, b, pose in ((0, 46, OP), (48, 92, OM), (94, 298, W), (300, 376, RK), (378, 490, W), (492, 570, CU), (572, 792, EXP), (794, TOTAL - 1, FIN)):
    camkey(a, pose)
    camkey(b, pose)

pimo = make('pimo', 1.1)
ruki = make('ruki', 1.1)
PM, RK0, RKB = Vector((-1.08, -1.22, Z0)), Vector((1.12, -1.2, Z0)), Vector((0.3, -1.16, Z0))
T.place(pimo, 0, PM)
T.turn(pimo, 0, 25)
T.place(ruki, 0, RK0)
T.turn(ruki, 0, -25)
T.place(ruki, 300, RK0)
T.turn(ruki, 300, -25)
T.place(ruki, 334, RKB)
T.turn(ruki, 334, 55)
T.place(ruki, 392, RKB)
T.turn(ruki, 392, 55)
T.place(ruki, 420, RK0)
T.turn(ruki, 420, -25)
for ch, p0, dx in ((pimo, PM, -0.6), (ruki, RK0, 0.6)):
    T.place(ch, 490, p0)
    T.place(ch, 492, p0 + Vector((dx, 0, 0)))
    T.place(ch, 792, p0 + Vector((dx, 0, 0)))
    T.place(ch, 794, p0)

T.arm(pimo, 'L', 4, 0, None)
T.arm(pimo, 'L', 12, fwd=-75, out=20)
T.arm(pimo, 'L', 60, fwd=-75, out=20)
T.rest_arm(pimo, 'L', 70)
T.arm(ruki, 'R', 98, 0, None)
T.arm(ruki, 'R', 106, fwd=-80, out=25)
T.arm(ruki, 'R', 150, fwd=-80, out=25)
T.rest_arm(ruki, 'R', 160)
T.arm(pimo, 'L', 180, 0, None)
T.arm(pimo, 'L', 188, fwd=-85, out=30)
T.arm(pimo, 'L', 230, fwd=-85, out=30)
T.rest_arm(pimo, 'L', 240)
T.arm(ruki, 'L', 350, 0, None)
T.arm(ruki, 'L', 366, fwd=-80, out=15)
T.arm(ruki, 'L', 382, fwd=-80, out=15)
T.rest_arm(ruki, 'L', 394)
gesture(ruki, 'hops', 424)
gesture(pimo, 'hops', 404)
T.arm(pimo, 'L', 800, 0, None)
T.arm(pimo, 'L', 808, fwd=-60, out=50)
T.arm(pimo, 'L', 850, fwd=-60, out=50)
T.rest_arm(pimo, 'L', 860)
C.wave(pimo, 'R', 872, cycles=2, period=10)
C.wave(ruki, 'L', 868, cycles=2, period=10)
gesture(ruki, 'hops', 862)

T.lines(EID, LINES)
T.blinks(pimo, (60, 170, 330, 470, 620, 740, 900))
T.blinks(ruki, (70, 200, 360, 500, 650, 790, 910))
