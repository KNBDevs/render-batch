from stage import *
from episodes.plastilina_bota_plan import *
import ep_tools as T
import bmesh
from props.lib import spawn, auto_dress, M
EID = 'plastilina_bota'
Z0 = 0.08
auto_dress(EID, ENV)
for l in bpy.data.lights:
    if l.type == 'SUN':
        l.color = (0.88, 0.8, 1.0)
        l.energy *= 1.1
    else:
        l.color = (1.0, 0.86, 0.96)
sc.world.node_tree.nodes['Background'].inputs[0].default_value = (0.62, 0.56, 1.0, 1)

OP = ((-0.68, -3.35, 0.48), (-0.66, -1.9, 0.5), 24)
WB = ((-0.62, -3.5, 1.0), (-0.62, -1.8, 0.62), 30)
W0 = ((0.0, -6.65, 1.55), (0.0, -1.75, 0.8), 28)
WT = ((0.0, -3.55, 0.95), (0.0, -1.86, 0.72), 34)
WS = ((-0.15, -3.3, 0.6), (-0.15, -1.86, 0.55), 34)
WE = ((0.52, -3.5, 0.75), (0.52, -1.8, 0.42), 28)
WF = ((0.35, -6.3, 1.45), (0.35, -1.75, 0.8), 28)
for a, b, pose in ((0, 58, OP), (60, 126, WB), (128, 330, W0), (334, 430, WT), (432, 494, W0), (496, 576, WS), (578, 708, W0), (712, 802, WE), (804, TOTAL - 1, WF)):
    camkey(a, pose)
    camkey(b, pose)

H = 1.3
TX, TY = 0.0, -1.72
tower = spawn('drop_tower', 0, 3707, 'candy', (TX, TY, Z0), 1.0, 0)
trays = [o for o in tower.children if o.name.startswith('tray')]
trL = next(o for o in trays if o.name.startswith('trayL'))
trR = next(o for o in trays if o.name.startswith('trayR'))
T.pop_in(tower, 132, 1.0, 10)
TOPZ = Z0 + H + 0.04
PL = Vector((TX - 0.25, TY - 0.14, TOPZ))
PR = Vector((TX + 0.25, TY - 0.14, TOPZ))
pad = C.empty('pad', None, (TX, TY - 0.16, Z0))
C.rounded_box('padm', (0, 0, 0.012), (1.0, 0.42, 0.024), 0.5, M((0.98, 0.95, 0.9), rough=0.5, coat=0.3), pad)
T.pop_in(pad, 134, 1.0, 10)
FLOOR = Z0 + 0.024

clay_m = M((0.7, 0.42, 0.95), rough=0.88, coat=0.0)
dent_m = M((0.56, 0.32, 0.8), rough=0.9, coat=0.0)


def clay_ball(name, P, s):
    o = C.empty(name, None, tuple(P))
    R = 0.1
    C.sphere('clay', (0, 0, R), (R, R * 0.96, R * 0.94), clay_m, o, 28)
    for a, b in ((-0.5, 0.4), (0.3, 0.9), (0.6, 0.2)):
        n = Vector((math.sin(a) * math.cos(b), -math.cos(a) * math.cos(b), math.sin(b) * 0.6)).normalized()
        q = Vector((0, 0, 1)).rotation_difference(n)
        C.sphere('dent', tuple(Vector((0, 0, R)) + n * R * 0.97), (0.028, 0.028, 0.008), dent_m, o, 12, rot=tuple(q.to_euler()))
    o.scale = (s, s, s)
    return o


def drop(o, f0, z0, z1, g, e, s, flat=False, hold=2, nmax=6):
    h = z0 - z1
    p = o.location.copy()
    K(o, 'location', f0, tuple(p))
    K(o, 'scale', f0, (s, s, s))
    f = f0
    hits = []
    tf = math.sqrt(2 * h / g) * FPS
    for k in range(1, int(tf) + 1):
        u = k / FPS
        K(o, 'location', f0 + k, (p.x, p.y, z0 - 0.5 * g * u * u))
    f = f0 + tf
    fi = round(f)
    K(o, 'location', fi, (p.x, p.y, z1))
    K(o, 'scale', fi - 2, (s * 0.92, s * 0.92, s * 1.12))
    hits.append(fi)
    if flat:
        K(o, 'scale', fi, (s * 1.45, s * 1.45, s * 0.45))
        K(o, 'scale', fi + 3, (s * 1.75, s * 1.75, s * 0.28))
        return hits
    K(o, 'scale', fi, (s * 1.28, s * 1.28, s * 0.68))
    K(o, 'scale', fi + hold, (s * 1.28, s * 1.28, s * 0.68))
    K(o, 'location', fi + hold, (p.x, p.y, z1))
    K(o, 'scale', fi + hold + 3, (s * 0.9, s * 0.9, s * 1.12))
    K(o, 'scale', fi + hold + 7, (s, s, s))
    start = fi + hold
    hb = h
    for n in range(nmax):
        hb *= e
        if hb < 0.02:
            break
        tu = math.sqrt(2 * hb / g) * FPS
        tot = 2 * tu
        for k in range(1, int(tot)):
            u = k / FPS
            v = math.sqrt(2 * g * hb)
            K(o, 'location', start + k, (p.x, p.y, z1 + v * u - 0.5 * g * u * u))
        end = round(start + tot)
        K(o, 'location', end, (p.x, p.y, z1))
        K(o, 'scale', end - 1, (s, s, s))
        K(o, 'scale', end, (s * (1 + 0.2 * hb / h), s * (1 + 0.2 * hb / h), s * (1 - 0.25 * hb / h)))
        K(o, 'scale', end + 3, (s, s, s))
        hits.append(end)
        start = end
    return hits


bol = make('bolita', 1.2)
pimo = make('pimo', 1.45)
B0 = Vector((-0.78, -1.74, Z0))
B1 = Vector((-1.25, -1.7, Z0))
B2 = Vector((0.62, -1.5, Z0))
T.place(bol, 0, B0)
T.turn(bol, 0, 28)

HAND = Vector((-0.27, -1.9, 0.36))
c1 = clay_ball('clay1', HAND, 1.35)
T.pop_in(c1, 8, 1.35, 6)
T.arm(bol, 'R', 0, fwd=-70, out=25)
T.arm(bol, 'R', 36, fwd=-70, out=25)
T.arm(bol, 'R', 42, fwd=-30, out=10)
T.rest_arm(bol, 'R', 52)
K(c1, 'location', 38, tuple(HAND))
c1.location = (HAND.x, HAND.y, HAND.z)
drop(c1, 40, HAND.z, Z0, 7.0, 0, 1.35, flat=True)
K(c1, 'scale', 188, (2.36, 2.36, 0.38))
K(c1, 'scale', 196, (0, 0, 0))
S(bol, 52, (1, 1, 1))
S(bol, 56, (1.1, 1.1, 0.88))
S(bol, 62, (1, 1, 1))
T.turn(bol, 66, 0)
T.turn(bol, 110, 28)
gesture(bol, 'sway', 96)

PM_OFF = Vector((2.5, -1.3, Z0))
P1 = Vector((1.25, -1.72, Z0))
T.place(pimo, 0, PM_OFF)
T.place(pimo, 126, PM_OFF)
hop_to(pimo, 128, PM_OFF, P1, 16, 0.45)
T.turn(pimo, 0, -40)
T.turn(pimo, 146, -28)
T.place(bol, 160, B0)
hop_to(bol, 162, B0, B1, 12, 0.25)
T.turn(bol, 176, 30)

ball = spawn('play_ball', 1, 815, ((0.95, 0.22, 0.25)), PL, 1.35, 0)
c2 = clay_ball('clay2', PR, 1.35)
T.pop_in(ball, 200, 1.35, 8)
T.pop_in(c2, 212, 1.35, 8)
T.arm(pimo, 'L', 186, 0, None)
T.arm(pimo, 'L', 194, fwd=-85, out=10)
T.arm(pimo, 'L', 216, fwd=-85, out=10)
T.rest_arm(pimo, 'L', 226)
for x, f in ((PL.x, 240), (PR.x, 246)):
    word3d('?', (1.0, 0.78, 0.2), (x, TY - 0.2, TOPZ + 0.42), f, 334, size=0.32)
T.arm(pimo, 'L', 252, fwd=-60, out=30)
T.arm(pimo, 'L', 300, fwd=-60, out=30)
T.rest_arm(pimo, 'L', 312)

FD = 340
for tr, sgn in ((trL, -1), (trR, 1)):
    K(tr, 'rotation_euler', FD - 2, (0, 0, 0))
    K(tr, 'rotation_euler', FD + 3, (0, sgn * math.radians(70), 0))
    K(tr, 'rotation_euler', FD + 40, (0, sgn * math.radians(70), 0))
    K(tr, 'rotation_euler', FD + 52, (0, 0, 0))
drop(ball, FD, PL.z, FLOOR, 9.8, 0.62, 1.35)
drop(c2, FD, PR.z, FLOOR, 9.8, 0, 1.35, flat=True)
S(bol, 436, (1, 1, 1))
gesture(bol, 'hops', 440)
T.turn(bol, 436, 15)
T.turn(bol, 480, 30)

T.pop_out(ball, 470, 1.35, 6)
K(ball, 'location', 476, (PL.x, PL.y, FLOOR))
K(ball, 'location', 477, tuple(PL))
T.pop_in(ball, 480, 1.35, 8)
SD = 500
for tr, sgn in ((trL, -1),):
    K(tr, 'rotation_euler', SD - 2, (0, 0, 0))
    K(tr, 'rotation_euler', SD + 3, (0, sgn * math.radians(70), 0))
    K(tr, 'rotation_euler', SD + 60, (0, sgn * math.radians(70), 0))
    K(tr, 'rotation_euler', SD + 72, (0, 0, 0))
ball.location = PL
hits = drop(ball, SD, PL.z, FLOOR, 1.9, 0.6, 1.35, hold=10, nmax=4)
fi = hits[0]
glow = M((0.4, 1.0, 0.6), rough=0.3, emit=1.6)
press = C.empty('press', None, (PL.x, PL.y - 0.02, FLOOR + 0.1))
for a in (0, 180):
    d = Vector((math.cos(math.radians(a)), 0, 0))
    C.tube('pl', [tuple(d * 0.24), tuple(d * 0.36)], 0.012, glow, press)
    C.tube('ph1', [tuple(d * 0.24), tuple(d * 0.29 + Vector((0, 0, 0.05)))], 0.012, glow, press)
    C.tube('ph2', [tuple(d * 0.24), tuple(d * 0.29 + Vector((0, 0, -0.05)))], 0.012, glow, press)
K(press, 'scale', 0, (0, 0, 0))
K(press, 'scale', fi - 1, (0, 0, 0))
K(press, 'scale', fi + 2, (1, 1, 1))
K(press, 'scale', fi + 9, (1, 1, 1))
K(press, 'scale', fi + 12, (0, 0, 0))
up = C.empty('uparrow', None, (PL.x + 0.21, PL.y - 0.08, FLOOR + 0.25))
C.tube('ua', [(0, 0, 0), (0, 0, 0.3)], 0.022, glow, up)
C.tube('ub1', [(0, 0, 0.32), (-0.07, 0, 0.22)], 0.022, glow, up)
C.tube('ub2', [(0, 0, 0.32), (0.07, 0, 0.22)], 0.022, glow, up)
K(up, 'scale', 0, (0, 0, 0))
K(up, 'scale', fi + 9, (0, 0, 0))
K(up, 'scale', fi + 14, (1.15, 1.15, 1.15))
K(up, 'scale', fi + 18, (1, 1, 1))
K(up, 'location', fi + 14, (PL.x + 0.21, PL.y - 0.08, FLOOR + 0.25))
K(up, 'location', fi + 40, (PL.x + 0.21, PL.y - 0.08, FLOOR + 0.55))
K(up, 'scale', fi + 40, (1, 1, 1))
K(up, 'scale', fi + 46, (0, 0, 0))
T.arm(pimo, 'L', 584, 0, None)
T.arm(pimo, 'L', 592, fwd=-50, out=35)
T.arm(pimo, 'L', 630, fwd=-50, out=35)
T.rest_arm(pimo, 'L', 640)
gesture(pimo, 'breathe', 616)
T.turn(bol, 660, 50)

PM2 = Vector((1.45, -1.6, Z0))
T.place(pimo, 698, P1)
T.place(pimo, 708, PM2)
T.turn(pimo, 708, -45)
T.place(bol, 708, B1)
hop_to(bol, 710, B1, B2, 14, 0.5)
T.turn(bol, 724, -20)
for f in (726, 738):
    S(bol, f - 4, (1, 1, 1))
    S(bol, f, (1.12, 1.12, 0.84))
    S(bol, f + 5, (1, 1, 1))
K(c2, 'scale', 724, (2.36, 2.36, 0.38))
K(c2, 'scale', 728, (2.5, 2.5, 0.27))
K(c2, 'scale', 740, (2.5, 2.5, 0.27))
K(c2, 'scale', 750, (0, 0, 0))


def star_obj(name, P, m):
    bm = bmesh.new()
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        r = 0.13 if k % 2 == 0 else 0.058
        pts.append(bm.verts.new((math.cos(a) * r, 0, math.sin(a) * r)))
    face = bm.faces.new(pts)
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    vs = [v for v in ext['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0.05, 0), verts=vs)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = C.empty(name, None, tuple(P))
    ob = C.mesh_obj('star', bm, m, o, smooth=False)
    ob.location = (0, -0.025, 0.14)
    b = ob.modifiers.new('bev', 'BEVEL')
    b.width = 0.018
    b.segments = 4
    return o


SP0 = Vector((PR.x - 0.1, PR.y - 0.2, FLOOR))
star = star_obj('clay_star', SP0, clay_m)
T.pop_in(star, 750, 1.15, 10)
K(star, 'location', 750, tuple(SP0))
K(star, 'location', 772, tuple(SP0 + Vector((0, 0, 0.05))))
for k, f in enumerate(range(772, TOTAL, 16)):
    K(star, 'rotation_euler', f, (0, math.radians(8 if k % 2 else -8), 0))
gesture(bol, 'bounce', 800)
C.wave(pimo, 'R', 826, cycles=2, period=8)

T.lines(EID, LINES)
T.blinks(bol, (30, 120, 260, 390, 520, 690, 840))
T.blinks(pimo, (180, 300, 420, 560, 700, 820))
