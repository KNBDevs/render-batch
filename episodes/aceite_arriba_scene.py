from stage import *
from episodes.aceite_arriba_plan import *
import random
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'aceite_arriba'
Z0 = 0.08
auto_dress(EID, ENV)
GOLD = (1.0, 0.62, 0.22)
for l in list(bpy.data.lights):
    e, base = l.energy, tuple(l.color)
    for f, c, k in ((0, GOLD, 1.25), (58, GOLD, 1.25), (74, base, 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.95, 0.5, 0.18, 1)), (58, (0.95, 0.5, 0.18, 1)), (74, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)

BX, BY = 0.0, -1.55
BS = 1.3
R, TH = 0.24, 0.012
stand = C.empty('bottle_stand', None, (BX, BY, Z0))
C.lathe('coaster', [(0, 0.0), (0, 0.34), (0.02, 0.36), (0.05, 0.33), (0.055, 0.0)], M((0.98, 0.62, 0.72), rough=0.4, coat=0.6), stand, segs=56)
C.tube('coaster_ring', [(math.cos(k * 6.2832 / 56) * 0.3, math.sin(k * 6.2832 / 56) * 0.3, 0.056) for k in range(57)], 0.01, M((0.55, 0.78, 1.0), rough=0.4, coat=0.6), stand)
bt = C.empty('oil_bottle', None, (BX, BY, Z0 + 0.055))
bt.scale = (BS, BS, BS)
GL = MA((0.92, 0.97, 1.0), 0.12)
out = [(0, 0.0), (0, R - 0.02), (0.02, R), (0.74, R), (0.86, 0.15), (0.92, 0.095), (1.0, 0.095)]
inn = [(1.0, 0.095 - TH), (0.92, 0.095 - TH), (0.86, 0.15 - TH), (0.74, R - TH), (0.03, R - TH), (0.03, 0.0)]
C.lathe('glass', out + [(1.004, 0.09)] + inn, GL, bt, segs=56)
CAP = M((0.98, 0.5, 0.62), rough=0.35, coat=0.7)
C.lathe('cap', [(0.98, 0.0), (0.98, 0.112), (0.99, 0.12), (1.09, 0.12), (1.1, 0.11), (1.105, 0.0)], CAP, bt, segs=48)
for z in (1.01, 1.035, 1.06):
    C.tube('cap_rib', [(math.cos(k * 6.2832 / 48) * 0.122, math.sin(k * 6.2832 / 48) * 0.122, z) for k in range(49)], 0.005, M((1.0, 0.82, 0.86), rough=0.35, coat=0.7), bt)
C.tube('base_band', [(math.cos(k * 6.2832 / 56) * (R + 0.004), math.sin(k * 6.2832 / 56) * (R + 0.004), 0.06) for k in range(57)], 0.012, M((0.55, 0.78, 1.0), rough=0.4, coat=0.6), bt)

RI = R - TH - 0.006
WAT = C.mat('oil_water', (0.1, 0.4, 1.0), rough=0.05, coat=0.5, emit=0.12)
WA = WAT.node_tree.nodes['Principled BSDF'].inputs['Alpha']
OIL = MA((1.0, 0.7, 0.0), 0.92, rough=0.05, emit=0.4)
wp = C.empty('water_lvl', bt, (0, 0, 0.032))
C.lathe('water', [(0, 0.0), (0, RI), (1.0, RI), (1.0, 0.0)], WAT, wp, segs=48)
op = C.empty('oil_lvl', bt, (0, 0, 0.45))
C.lathe('oil', [(0, 0.0), (0, RI), (1.0, RI), (1.0, 0.0)], OIL, op, segs=48)
WH, OH, WM = 0.42, 0.2, 0.6


def levels(f, mixed):
    WA.default_value = 0.22 if mixed else 0.86
    WA.keyframe_insert('default_value', frame=f)
    if mixed:
        K(wp, 'scale', f, (1, 1, WM))
        K(op, 'location', f, (0, 0, 0.032 + WM))
        K(op, 'scale', f, (1, 1, 0.002))
    else:
        K(wp, 'scale', f, (1, 1, WH))
        K(op, 'location', f, (0, 0, 0.032 + WH))
        K(op, 'scale', f, (1, 1, OH))


rnd = random.Random(54)
DRM = M((1.0, 0.62, 0.0), rough=0.3, coat=0.6, emit=0.25)
DROPS = []
for i in range(40):
    a = math.radians(rnd.uniform(-160, -20))
    rr = rnd.uniform(0.04, RI - 0.05)
    z = rnd.uniform(0.08, 0.032 + WM - 0.05)
    s = rnd.uniform(0.035, 0.06)
    d = C.empty('drop', bt, (math.cos(a) * rr, math.sin(a) * rr, z))
    C.sphere('d', (0, 0, 0), (s, s, s * 0.9), DRM, d, 16)
    K(d, 'scale', 0, (0, 0, 0))
    DROPS.append((d, (math.cos(a) * rr, math.sin(a) * rr, z)))


def cycle(fs0, fs1, f0, f1):
    levels(fs0, False)
    levels(fs0 + 10, True)
    for i, (d, p) in enumerate(DROPS):
        K(d, 'location', fs0, (p[0] * 0.3, p[1] * 0.3, 0.032 + WH + 0.05))
        K(d, 'scale', fs0, (0, 0, 0))
        K(d, 'location', fs0 + 10, p)
        K(d, 'scale', fs0 + 10, (1, 1, 1))
        K(d, 'location', fs1, p)
        K(d, 'location', f0, p)
        u = (p[2] - 0.08) / (WM - 0.1)
        fe = round(f0 + (f1 - f0) * (0.35 + 0.65 * (1 - u)))
        K(d, 'scale', fe - 8, (1, 1, 1))
        K(d, 'location', fe, (p[0] * 0.8, p[1] * 0.8, 0.032 + WH + 0.04))
        K(d, 'scale', fe, (0.4, 0.4, 0.4))
        K(d, 'scale', fe + 2, (0, 0, 0))
    levels(f0, True)
    levels(f1, False)
    WA.default_value = 0.22
    WA.keyframe_insert('default_value', frame=f1 - 14)


levels(0, False)
cycle(112, 186, 330, 470)
cycle(722, 752, 762, 830)
for f, ang, dz in ((0, 0, 0), (6, 4, 0), (12, -4, 0), (18, 4, 0), (24, 0, 0)):
    K(bt, 'rotation_euler', f, (0, math.radians(ang), 0))
for fa, fb in ((112, 186), (722, 752)):
    K(bt, 'rotation_euler', fa, (0, 0, 0))
    K(bt, 'location', fa, (BX, BY, Z0 + 0.055))
    n = 0
    for f in range(fa + 4, fb - 3, 6):
        n += 1
        K(bt, 'rotation_euler', f, (0, math.radians(22 if n % 2 else -22), 0))
        K(bt, 'location', f, (BX, BY, Z0 + 0.055 + (0.16 if n % 2 else 0.06)))
    K(bt, 'rotation_euler', fb, (0, 0, 0))
    K(bt, 'location', fb, (BX, BY, Z0 + 0.055))

clock = spawn('time_clock', 0, 5401, 'pastel', (BX - 0.62, BY + 0.4, Z0), 1.15, 12)
hm = next(o for o in clock.children if o.name.startswith('hand_m'))
hh = next(o for o in clock.children if o.name.startswith('hand_h'))
K(hm, 'rotation_euler', 0, (0, 0, 0))
K(hh, 'rotation_euler', 0, (0, math.radians(90), 0))
K(hm, 'rotation_euler', 320, (0, 0, 0))
K(hh, 'rotation_euler', 320, (0, math.radians(90), 0))
K(hm, 'rotation_euler', 470, (0, 2 * 6.2832, 0))
K(hh, 'rotation_euler', 470, (0, math.radians(90) + 2 * 6.2832 / 12, 0))
T.pop_in(clock, 310, 1.15, 8)
T.pop_out(clock, 548, 1.15, 6)


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


OC = (0.9, 0.55, 0.05)
WC = (0.15, 0.4, 0.85)
TOPZ = Z0 + 0.055 + 1.1 * BS
label('¿ARRIBA?', OC, (BX - 0.62, BY - 0.6, TOPZ + 0.12), 1.0, 226, 344)
label('¿ABAJO?', WC, (BX + 0.62, BY - 0.6, Z0 + 0.42), 0.95, 232, 344)
label('UN RATO DESPUÉS', (0.5, 0.3, 0.7), (BX, BY - 0.6, TOPZ + 0.35), 1.55, 306, 400, 0.26, 0.17)
OZ = Z0 + 0.055 + (0.032 + WH + OH / 2) * BS
WZ = Z0 + 0.055 + (0.032 + WH / 2) * BS
label('ACEITE', OC, (BX + 0.62, BY - 0.42, OZ), 0.82, 566, 684, 0.22, 0.16)
label('AGUA', WC, (BX + 0.56, BY - 0.42, WZ), 0.68, 572, 684, 0.22, 0.16)
ARM = M((1.0, 0.7, 0.15), rough=0.3, coat=0.6, emit=0.6)
arr = C.empty('arrow_up', None, (BX - 0.42, BY - 0.42, OZ - 0.18))
C.tube('shaft', [(0, 0, -0.14), (0, 0, 0.1)], 0.022, ARM, arr)
C.tube('hl', [(-0.07, 0, 0.04), (0, 0, 0.12), (0.07, 0, 0.04)], 0.022, ARM, arr)
T.pop_in(arr, 580, 1.0, 8)
for f in range(590, 680, 12):
    K(arr, 'location', f, (BX - 0.42, BY - 0.42, OZ - (0.18 if (f // 12) % 2 else 0.1)))
T.pop_out(arr, 684, 1.0, 6)

OP = ((0.1, -3.3, 0.35), (-0.3, BY, 0.75), 21)
OP2 = ((0.06, -3.2, 0.37), (-0.3, BY, 0.77), 22)
W = ((0.05, -4.6, 1.7), (0.05, -1.6, 0.85), 19.5)
WQ = ((0.05, -4.85, 1.95), (0.05, -1.6, 0.95), 19.5)
CB = ((BX, -3.9, 1.0), (BX, BY, Z0 + 0.78), 25)
CL = ((BX + 0.2, -3.9, OZ + 0.1), (BX + 0.18, BY, OZ - 0.12), 26)
WE = ((0.05, -4.7, 1.8), (0.05, -1.6, 0.8), 19.5)
camkey(0, OP)
camkey(30, OP)
camkey(58, OP2)
for a, b, pose in ((60, 190, W), (192, 350, WQ), (352, 552, CB), (554, 690, CL), (692, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

luma = make('luma', 1.3)
moki = make('moki', 1.2)
LM0 = Vector((-1.15, -1.7, Z0))
MK0 = Vector((1.25, -1.5, Z0))
T.place(luma, 0, Vector((-0.78, -1.9, Z0)))
T.turn(luma, 0, 35)
for side in ('L', 'R'):
    T.arm(luma, side, 6, fwd=-90, out=30)
    for f in range(12, 54, 6):
        T.arm(luma, side, f, fwd=-80 if (f // 6) % 2 else -100, out=30)
    T.rest_arm(luma, side, 60)
hop_to(luma, 62, Vector((-0.78, -1.9, Z0)), LM0, 12, 0.25)
T.turn(luma, 80, 28)
for side in ('L', 'R'):
    T.arm(luma, side, 110, fwd=-100, out=35)
    for f in range(116, 186, 6):
        T.arm(luma, side, f, fwd=-80 if (f // 6) % 2 else -120, out=35)
    T.rest_arm(luma, side, 192)
T.arm(luma, 'R', 198, 0, None)
T.arm(luma, 'R', 204, fwd=-160, out=20)
T.arm(luma, 'R', 228, fwd=-160, out=20)
T.arm(luma, 'R', 234, fwd=-60, out=40)
T.arm(luma, 'R', 250, fwd=-60, out=40)
T.rest_arm(luma, 'R', 258)
gesture(luma, 'hops', 476)
T.arm(luma, 'L', 474, 0, None)
T.arm(luma, 'L', 480, fwd=-160, out=20)
T.arm(luma, 'L', 520, fwd=-160, out=20)
T.rest_arm(luma, 'L', 530)
T.turn(luma, 556, 40)
for side in ('L', 'R'):
    T.arm(luma, side, 720, fwd=-100, out=35)
    for f in range(726, 752, 6):
        T.arm(luma, side, f, fwd=-80 if (f // 6) % 2 else -120, out=35)
    T.rest_arm(luma, side, 758)
gesture(luma, 'hops', 790)
C.wave(luma, 'L', 826, cycles=2, period=8)

T.place(moki, 0, MK0)
T.turn(moki, 0, -35)
T.arm(moki, 'L', 94, 0, None)
for f in range(100, 140, 6):
    T.arm(moki, 'L', f, fwd=-120 if (f // 6) % 2 else -150, out=30)
T.rest_arm(moki, 'L', 146)
T.turn(moki, 300, -42)
T.arm(moki, 'L', 406, 0, None)
T.arm(moki, 'L', 412, fwd=-120, out=35)
T.arm(moki, 'L', 452, fwd=-120, out=35)
T.rest_arm(moki, 'L', 462)
gesture(moki, 'breathe', 560)
T.arm(moki, 'R', 560, 0, None)
T.arm(moki, 'R', 566, fwd=-90, out=50)
T.arm(moki, 'R', 640, fwd=-90, out=50)
T.rest_arm(moki, 'R', 650)
gesture(moki, 'hops', 796)
C.wave(moki, 'R', 820, cycles=2, period=8)
confetti(784, (BX, BY, TOPZ + 0.6), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(luma, (44, 150, 300, 460, 590, 700, 840))
T.blinks(moki, (70, 190, 330, 500, 650, 790))
