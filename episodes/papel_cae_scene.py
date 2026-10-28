from stage import *
from episodes.papel_cae_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M
EID = 'papel_cae'
Z0 = 0.08
auto_dress(EID, ENV)
for l in bpy.data.lights:
    if l.type == 'SUN':
        l.color = (1.0, 0.95, 0.86)
    else:
        l.color = (0.86, 0.94, 1.0)

OP = ((0.25, -3.8, 3.2), (0.25, -1.8, 0.75), 24)
WM = ((0.9, -3.65, 1.75), (0.9, -1.75, 0.88), 30)
W0 = ((0.0, -7.2, 1.65), (0.0, -1.75, 0.8), 28)
WT = ((0.0, -3.55, 0.95), (0.0, -1.86, 0.72), 34)
WR = ((0.15, -3.3, 0.75), (0.15, -1.86, 0.7), 34)
WL = ((-0.15, -3.3, 0.75), (-0.15, -1.86, 0.7), 34)
WE = ((1.2, -4.4, 0.95), (1.18, -1.9, 0.6), 30)
for a, b, pose in ((0, 88, OP), (90, 148, WM), (150, 326, W0), (328, 414, WT), (416, 468, W0), (470, 564, WR), (566, 642, WL), (644, 722, W0), (724, 800, WE), (802, TOTAL - 1, W0)):
    camkey(a, pose)
    camkey(b, pose)

H = 1.3
TX, TY = 0.0, -1.72
tower = spawn('drop_tower', 1, 5121, 'fresh', (TX, TY, Z0), 1.0, 0)
trL = next(o for o in tower.children if o.name.startswith('trayL'))
trR = next(o for o in tower.children if o.name.startswith('trayR'))
TOPZ = Z0 + H + 0.04
PL = Vector((TX - 0.25, TY - 0.14, TOPZ))
PR = Vector((TX + 0.25, TY - 0.14, TOPZ + 0.01))
pad = C.empty('pad', None, (TX, TY - 0.16, Z0))
C.rounded_box('padm', (0, 0, 0.012), (1.0, 0.42, 0.024), 0.5, M((0.78, 0.66, 0.98), rough=0.5, coat=0.3), pad)
FLOOR = Z0 + 0.024

paper = M((1.0, 0.62, 0.12), rough=0.55, coat=0.15)
ink = M((0.2, 0.45, 0.95), rough=0.5, coat=0.1)
pink = M((1.0, 0.45, 0.6), rough=0.4, coat=0.3)
crease = M((0.8, 0.42, 0.05), rough=0.7, coat=0.0)
air = M((0.55, 0.85, 1.0), rough=0.3, emit=1.4)


def sheet(name, P, heart=False, arrows=False):
    o = C.empty(name, None, tuple(P))
    C.rounded_box('pg', (0, 0, 0), (0.32, 0.23, 0.008), 0.3, paper, o)
    for k in range(3):
        y = -0.06 + k * 0.05
        C.tube('ln', [(-0.12, y, 0.006), (0.12, y, 0.006)], 0.003, ink, o)
    if heart:
        for sx in (-1, 1):
            C.sphere('hl', (sx * 0.022, 0.0, 0.009), (0.028, 0.028, 0.004), pink, o, 16)
        C.rounded_box('hb', (0, -0.022, 0.009), (0.04, 0.04, 0.006), 0.2, pink, o).rotation_euler = (0, 0, math.radians(45))
    ar = None
    if arrows:
        ar = C.empty('air', o, (0, 0, -0.06))
        for x in (-0.1, 0.0, 0.1):
            C.tube('as', [(x, 0, -0.16), (x, 0, -0.03)], 0.008, air, ar)
            C.tube('a1', [(x, 0, -0.02), (x - 0.03, 0, -0.06)], 0.008, air, ar)
            C.tube('a2', [(x, 0, -0.02), (x + 0.03, 0, -0.06)], 0.008, air, ar)
        ar.scale = (0, 0, 0)
    return o, ar


def paper_ball(name, P, s, rnd):
    o = C.empty(name, None, tuple(P))
    R = 0.07
    C.sphere('core', (0, 0, R), (R, R, R * 0.95), paper, o, 20)
    for k in range(8):
        a = k * 2.4
        z = 1 - 2 * (k + 0.5) / 8
        rr = math.sqrt(1 - z * z)
        n = Vector((math.cos(a) * rr, math.sin(a) * rr, z))
        C.sphere('lump', tuple(Vector((0, 0, R)) + n * R * 0.55), (R * 0.62, R * 0.5, R * 0.55), paper, o, 14, rot=(rnd(), rnd(), rnd()))
    for k in range(4):
        a = k * 1.6
        C.tube('cr', [(math.cos(a) * R * 0.9, -R * 0.7, R + math.sin(a) * 0.03), (math.cos(a + 0.8) * R * 0.7, -R * 0.85, R + 0.02)], 0.0035, crease, o)
    o.scale = (s, s, s)
    return o


_r = [0]


def rnd():
    _r[0] = (_r[0] * 1103515245 + 12345) % 2147483648
    return (_r[0] / 2147483648.0 - 0.5) * 1.2


def flutter(o, f0, P0, P1, n, amp, cyc, tilt=28):
    K(o, 'location', f0, tuple(P0))
    K(o, 'rotation_euler', f0, (0, 0, 0))
    for k in range(2, n + 1, 2):
        u = k / n
        p = P0.lerp(P1, u)
        e = math.sin(2 * math.pi * cyc * u)
        p.x += amp * e * (1 - u * 0.4)
        K(o, 'location', f0 + k, tuple(p))
        K(o, 'rotation_euler', f0 + k, (0, math.radians(tilt * math.cos(2 * math.pi * cyc * u)) * (1 - u * 0.6), math.radians(10 * e)))
    K(o, 'rotation_euler', f0 + n, (0, 0, 0))


def fall(o, f0, z0, z1, g, s):
    p = o.location.copy()
    K(o, 'location', f0, tuple(p))
    tf = math.sqrt(2 * (z0 - z1) / g) * FPS
    for k in range(1, int(tf) + 1):
        u = k / FPS
        K(o, 'location', f0 + k, (p.x, p.y, z0 - 0.5 * g * u * u))
    fi = round(f0 + tf)
    K(o, 'location', fi, (p.x, p.y, z1))
    K(o, 'scale', fi - 1, (s, s, s))
    K(o, 'scale', fi, (s * 1.15, s * 1.15, s * 0.82))
    K(o, 'location', fi + 4, (p.x, p.y, z1 + 0.04))
    K(o, 'location', fi + 8, (p.x, p.y, z1))
    K(o, 'scale', fi + 4, (s, s, s))
    return fi


def tilt(tr, sgn, f, hold=40):
    K(tr, 'rotation_euler', f - 2, (0, 0, 0))
    K(tr, 'rotation_euler', f + 3, (0, sgn * math.radians(70), 0))
    K(tr, 'rotation_euler', f + hold, (0, sgn * math.radians(70), 0))
    K(tr, 'rotation_euler', f + hold + 12, (0, 0, 0))


tuki = make('tuki', 1.15)
moki = make('moki', 1.0)
TK0 = Vector((-0.5, -1.66, Z0))
MK0 = Vector((1.0, -1.72, Z0))
B1 = Vector((-1.25, -1.7, Z0))
P1 = Vector((1.25, -1.72, Z0))
T.place(tuki, 0, TK0)
T.turn(tuki, 0, 25)
T.place(moki, 0, MK0)
T.turn(moki, 0, -20)

s1, _ = sheet('sheet1', PR)
tilt(trR, 1, 6, 30)
HEAD = Vector((MK0.x, MK0.y - 0.02, Z0 + 1.12))
flutter(s1, 8, PR, HEAD, 62, 0.22, 2.5)
K(s1, 'location', 70, tuple(HEAD))
K(s1, 'location', 124, tuple(HEAD))
K(s1, 'rotation_euler', 124, (0, 0, 0))
K(s1, 'location', 132, tuple(HEAD + Vector((0.3, -0.1, 0.1))))
K(s1, 'rotation_euler', 132, (0, math.radians(40), 0))
T.pop_out(s1, 132, 1.0, 6)
T.arm(tuki, 'R', 0, 0, None)
T.arm(tuki, 'R', 2, fwd=-40, out=50)
T.rest_arm(tuki, 'R', 12)
S(moki, 66, (1, 1, 1))
S(moki, 70, (1.08, 1.08, 0.9))
S(moki, 76, (1, 1, 1))
for k, f in enumerate(range(112, 130, 6)):
    T.turn(moki, f, -40 if k % 2 else 0)
T.turn(moki, 132, -20)
gesture(moki, 'sway', 96)

hop_to(tuki, 140, TK0, B1, 14, 0.35)
T.turn(tuki, 156, 30)
hop_to(moki, 140, MK0, P1, 14, 0.35)
T.turn(moki, 156, -30)

HAND = Vector((-1.0, -1.95, 0.5))
s2, _ = sheet('sheet2', HAND)
s2.rotation_euler = (math.radians(70), 0, 0)
T.pop_in(s2, 160, 1.0, 6)
K(s2, 'scale', 172, (1, 1, 1))
K(s2, 'scale', 180, (0.7, 0.8, 1))
K(s2, 'scale', 188, (0.4, 0.45, 1))
K(s2, 'scale', 196, (0, 0, 0))
_r[0] = 77
pb = paper_ball('pball', HAND + Vector((0, 0, -0.08)), 1.35, rnd)
K(pb, 'scale', 0, (0, 0, 0))
K(pb, 'scale', 186, (0, 0, 0))
K(pb, 'scale', 192, (1.6, 1.6, 1.6))
K(pb, 'scale', 196, (1.35, 1.35, 1.35))
for f in (176, 182, 188):
    S(tuki, f - 3, (1, 1, 1))
    S(tuki, f, (1.1, 1.1, 0.9))
T.arm(tuki, 'R', 168, fwd=-70, out=15)
T.arm(tuki, 'L', 168, fwd=-70, out=15)
T.arm(tuki, 'R', 196, fwd=-70, out=15)
T.arm(tuki, 'L', 196, fwd=-70, out=15)
T.rest_arm(tuki, 'R', 206)
T.rest_arm(tuki, 'L', 206)
T.pop_out(pb, 200, 1.35, 6)
K(pb, 'location', 206, tuple(HAND + Vector((0, 0, -0.08))))
K(pb, 'location', 207, tuple(PL))
T.pop_in(pb, 212, 1.35, 8)
s3, ar3 = sheet('sheet3', PR, arrows=True)
T.pop_in(s3, 212, 1.0, 8)
for x, f in ((PL.x, 244), (PR.x, 250)):
    word3d('?', (1.0, 0.78, 0.2), (x, TY - 0.2, TOPZ + 0.42), f, 328, size=0.32)
T.arm(moki, 'R', 238, fwd=-55, out=30)
T.arm(moki, 'R', 300, fwd=-55, out=30)
T.rest_arm(moki, 'R', 312)

FD = 328
tilt(trL, -1, FD)
tilt(trR, 1, FD, 80)
fall(pb, FD, PL.z, FLOOR, 9.8, 1.35)
SL = Vector((PR.x + 0.02, PR.y - 0.04, FLOOR + 0.006))
flutter(s3, FD + 2, PR, SL, 78, 0.18, 3)
K(s3, 'location', 408, tuple(SL))
gesture(tuki, 'hops', 420)
T.turn(tuki, 418, 10)
T.turn(tuki, 470, 30)

T.pop_out(s3, 462, 1.0, 6)
K(s3, 'location', 468, tuple(SL))
K(s3, 'location', 469, tuple(PR))
T.pop_in(s3, 470, 1.0, 8)
tilt(trR, 1, 482, 76)
flutter(s3, 484, PR, SL, 76, 0.16, 2.5, 22)
K(ar3, 'scale', 486, (0, 0, 0))
K(ar3, 'scale', 492, (1.2, 1.2, 1.2))
K(ar3, 'scale', 496, (1, 1, 1))
K(ar3, 'scale', 554, (1, 1, 1))
K(ar3, 'scale', 560, (0, 0, 0))

T.pop_out(pb, 560, 1.35, 6)
K(pb, 'location', 566, tuple(PL))
T.pop_in(pb, 568, 1.35, 8)
stk = C.empty('streak', pb, (0, 0, 0))
for x in (-0.11, 0.11):
    C.tube('sk', [(x, -0.02, 0.2), (x, -0.02, 0.45)], 0.007, air, stk)
stk.scale = (0, 0, 0)
K(stk, 'scale', 0, (0, 0, 0))
tilt(trL, -1, 590)
K(stk, 'scale', 589, (0, 0, 0))
K(stk, 'scale', 592, (1, 1, 1))
fi = fall(pb, 590, PL.z, FLOOR, 9.8, 1.35)
K(stk, 'scale', fi - 1, (1, 1, 1))
K(stk, 'scale', fi + 1, (0, 0, 0))
T.arm(moki, 'R', 474, fwd=-50, out=35)
T.arm(moki, 'R', 540, fwd=-50, out=35)
T.rest_arm(moki, 'R', 552)
gesture(moki, 'breathe', 576)

TH = Vector((-1.02, -1.95, 0.52))
pb2 = paper_ball('pball2', TH, 1.35, rnd)
T.pop_in(pb2, 646, 1.35, 8)
T.arm(tuki, 'R', 650, fwd=-60, out=20)
T.arm(tuki, 'R', 684, fwd=-100, out=20)
T.arm(tuki, 'R', 692, fwd=-20, out=20)
T.rest_arm(tuki, 'R', 704)
MH = Vector((0.7, -2.25, 0.36))
K(pb2, 'location', 688, tuple(TH))
for k in range(0, 25, 2):
    u = k / 24
    p = TH.lerp(MH, u)
    p.z += 0.75 * 4 * u * (1 - u)
    K(pb2, 'location', 688 + k, tuple(p))
T.arm(moki, 'L', 700, fwd=-75, out=15)
T.arm(moki, 'L', 770, fwd=-75, out=15)
T.rest_arm(moki, 'L', 782)
K(pb2, 'scale', 720, (1.35, 1.35, 1.35))
K(pb2, 'scale', 728, (0, 0, 0))
s4, _ = sheet('letter', MH + Vector((0, -0.02, 0.06)), heart=True)
s4.rotation_euler = (math.radians(80), 0, 0)
T.pop_in(s4, 726, 1.4, 10)
for k, f in enumerate(range(740, TOTAL, 18)):
    K(s4, 'rotation_euler', f, (math.radians(80), math.radians(5 if k % 2 else -5), 0))
gesture(moki, 'bounce', 800)
C.wave(tuki, 'R', 812, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(tuki, (40, 150, 280, 400, 540, 680, 820))
T.blinks(moki, (60, 200, 330, 460, 620, 760))
