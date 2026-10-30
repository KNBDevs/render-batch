from stage import *
from episodes.rampa_alta_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, glyph
EID = 'rampa_alta'
Z0 = 0.08
auto_dress(EID, ENV, offset=(0, 0.7, 0))
WARM = (1.0, 0.72, 0.42)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, WARM), (70, WARM), (84, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
bg0 = tuple(bgc.default_value)
for f, c in ((0, (1.0, 0.62, 0.38, 1)), (70, (1.0, 0.62, 0.38, 1)), (84, bg0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

L = 1.4
YB = -0.1
XL, XH = -0.55, 0.55
HL, HH, HM = 0.2, 0.66, 0.46
BR = 0.176
GY = -2.95
rl = spawn('toy_ramp', 0, 5101, 'candy', (XL, YB, Z0), 1.0, 0, L=L, W=0.5, H=HL)
rh = spawn('toy_ramp', 0, 5101, 'candy', (XH, YB, Z0), 1.0, 0, L=L, W=0.5, H=HH)


def parts(root):
    tl = next(o for o in root.children if o.name.startswith('tilt'))
    po = next(o for o in root.children if o.name.startswith('post'))
    ft = next(o for o in root.children if o.name.startswith('foot'))
    return tl, po, ft


tl_l, po_l, ft_l = parts(rl)
tl_h, po_h, ft_h = parts(rh)


def set_h(tl, po, ft, f, h):
    a = math.asin(h / L)
    K(tl, 'rotation_euler', f, (a, 0, 0))
    K(po, 'location', f, (0, L * math.cos(a) - 0.07, 0))
    K(po, 'scale', f, (1, 1, h - 0.012))
    K(ft, 'location', f, (0, L * math.cos(a) - 0.07, 0.015))


set_h(tl_l, po_l, ft_l, 0, HL)
set_h(tl_h, po_h, ft_h, 0, HH)
T.pop_in(rh, 128, 1.0, 10)
set_h(tl_l, po_l, ft_l, 694, HL)
set_h(tl_l, po_l, ft_l, 712, HM)

goal = spawn('toy_goal', 0, 7302, 'candy', (XL, GY, Z0), 1.0, 180, W=1.0, H=0.62)
net = next(o for o in goal.children if o.name.startswith('net'))


def ramp_pt(x, h, s):
    a = math.asin(h / L)
    return Vector((x, YB + s * math.cos(a) - BR * math.sin(a), Z0 + 0.04 + s * math.sin(a) + BR * math.cos(a) - BR))


def roll(ball, x, h, f0, t_ramp, d_floor, t_floor, hold_end=None):
    s0 = L - 0.12
    K(ball, 'location', f0, tuple(ramp_pt(x, h, s0)))
    K(ball, 'rotation_euler', f0, (0, 0, 0))
    ang = 0.0
    prev = ramp_pt(x, h, s0)
    for t in range(1, t_ramp + 1):
        u = t / t_ramp
        p = ramp_pt(x, h, s0 * (1 - u * u))
        ang += (prev - p).length / BR
        prev = p
        K(ball, 'location', f0 + t, tuple(p))
        K(ball, 'rotation_euler', f0 + t, (ang, 0, 0))
    y0 = YB - 0.02
    for t in range(1, t_floor + 1):
        u = t / t_floor
        p = Vector((x, y0 - d_floor * (1 - (1 - u) ** 2), Z0))
        ang += (prev - p).length / BR
        prev = p
        K(ball, 'location', f0 + t_ramp + t, tuple(p))
        K(ball, 'rotation_euler', f0 + t_ramp + t, (ang, 0, 0))
    return prev


def mk_ball():
    b = C.empty('ballp', None, (0, 0, 0))
    pb = spawn('play_ball', 2, 909, 'candy', (0, 0, 0), 1.6, 0, b)
    for o in pb.children:
        o.data.materials.clear()
        o.data.materials.append(BALLM if o.name.startswith('ball') else BANDM)
    return b


BALLM = M((1.0, 0.42, 0.18), rough=0.35, coat=0.8)
BANDM = M((0.98, 0.97, 0.94), rough=0.35, coat=0.7)


b1 = mk_ball()
K(b1, 'location', 0, tuple(ramp_pt(XL, HL, L - 0.12)))
END_L = roll(b1, XL, HL, 30, 16, 1.3, 34)
K(b1, 'location', 134, tuple(END_L))
T.pop_out(b1, 136, 1.0, 6)
b2 = mk_ball()
b3 = mk_ball()
for b, x, h in ((b2, XL, HL), (b3, XH, HH)):
    K(b, 'scale', 0, (0, 0, 0))
    K(b, 'location', 0, tuple(ramp_pt(x, h, L - 0.12)))
    T.pop_in(b, 150 if b is b2 else 162, 1.0, 8)
roll(b2, XL, HL, 340, 16, 1.3, 34)
END_H = roll(b3, XH, HH, 340, 11, 3.4, 48)
T.pop_out(b2, 664, 1.0, 6)
T.pop_out(b3, 664, 1.0, 6)
b4 = mk_ball()
K(b4, 'scale', 0, (0, 0, 0))
T.pop_in(b4, 682, 1.0, 8)
K(b4, 'location', 0, tuple(ramp_pt(XL, HL, L - 0.12)))
K(b4, 'location', 694, tuple(ramp_pt(XL, HL, L - 0.12)))
K(b4, 'location', 712, tuple(ramp_pt(XL, HM, L - 0.12)))
roll(b4, XL, HM, 716, 13, 2.95, 26)
for f, sc3 in ((752, (1, 1, 1)), (756, (1.06, 1.25, 1.04)), (764, (0.98, 0.94, 1)), (772, (1, 1, 1))):
    K(net, 'scale', f, sc3)

ink = M((0.99, 0.98, 0.95), rough=0.3, coat=0.6, emit=0.1)


def qcard(txt, rgb, loc, f_in, f_out):
    h = C.empty('q', None, loc)
    C.rounded_box('card', (0, 0, 0), (0.5, 0.05, 0.5), 0.3, M(rgb, rough=0.4, coat=0.6, emit=0.15), h)
    glyph(txt, 0.4, 0.02, ink, h, (0, -0.04, -0.015))
    T.pop_in(h, f_in, 1.0, 8)
    T.pop_out(h, f_out, 1.0, 6)
    for k in range(6):
        K(h, 'location', f_in + 10 + 12 * k, (loc[0], loc[1], loc[2] + 0.04 * (1 if k % 2 else -1)))


qcard('?', (0.95, 0.35, 0.3), (XL, YB + 0.9, Z0 + 1.0), 212, 336)
qcard('?', (0.3, 0.5, 0.95), (XH, YB + 0.9, Z0 + 1.45), 220, 336)


def marker(x, y, rgb, f_in, f_out):
    h = C.empty('mk', None, (x, y, Z0))
    C.rounded_box('strip', (0, 0, 0.006), (0.6, 0.08, 0.012), 0.3, M(rgb, rough=0.4, coat=0.6, emit=0.2), h)
    C.tube('pole', [(0.34, 0, 0), (0.34, 0, 0.5)], 0.018, M((0.98, 0.97, 0.94), coat=0.6), h)
    C.rounded_box('flag', (0.45, 0, 0.42), (0.2, 0.025, 0.14), 0.3, M(rgb, rough=0.4, coat=0.6, emit=0.2), h)
    T.pop_in(h, f_in, 1.0, 8)
    T.pop_out(h, f_out, 1.0, 6)


marker(XL, END_L.y, (0.95, 0.35, 0.3), 558, 662)
marker(XH, END_H.y, (0.3, 0.5, 0.95), 564, 662)
am = M((1.0, 0.82, 0.15), rough=0.3, coat=0.5, emit=0.9)


def chevrons(x, h, n, f_in, f_out):
    a = math.asin(h / L)
    root = C.empty('chv', None, (x, YB, Z0), (a, 0, 0))
    for k in range(n):
        y = L * 0.75 - k * 0.3
        c = C.empty('cv', root, (0, y, 0.3))
        C.tube('c', [(-0.16, 0.12, 0), (0, 0, 0), (0.16, 0.12, 0)], 0.032, am, c)
        K(c, 'scale', 0, (0, 0, 0))
        K(c, 'scale', f_in + 6 * k, (0, 0, 0))
        K(c, 'scale', f_in + 6 * k + 8, (1, 1, 1))
        K(c, 'scale', f_out, (1, 1, 1))
        K(c, 'scale', f_out + 6, (0, 0, 0))


chevrons(XL, HL, 1, 478, 556)
chevrons(XH, HH, 3, 486, 556)


def floor_arrow(x, y0, y1, f_in, f_out):
    root = C.empty('fa', None, (x, 0, Z0 + 0.02))
    seg = C.empty('fas', root, (0, y0, 0))
    C.tube('s', [(0, 0, 0), (0, -1, 0)], 0.04, am, seg)
    hd = C.empty('fah', root, (0, y1, 0))
    C.tube('h1', [(0, 0, 0), (-0.14, 0.17, 0)], 0.04, am, hd)
    C.tube('h2', [(0, 0, 0), (0.14, 0.17, 0)], 0.04, am, hd)
    d = y0 - y1
    K(seg, 'scale', 0, (0, 0, 0))
    K(seg, 'scale', f_in, (1, 0.001, 1))
    K(seg, 'scale', f_in + 18, (1, d, 1))
    K(hd, 'scale', 0, (0, 0, 0))
    K(hd, 'scale', f_in + 16, (0, 0, 0))
    K(hd, 'scale', f_in + 22, (1, 1, 1))
    for o in (seg, hd):
        K(o, 'scale', f_out, (1, d, 1) if o is seg else (1, 1, 1))
        K(o, 'scale', f_out + 6, (0, 0, 0))


floor_arrow(XL - 0.38, YB - 0.15, END_L.y, 568, 662)
floor_arrow(XH + 0.38, YB - 0.15, END_H.y, 574, 662)

tuki = make('tuki', 1.4)
ruki = make('ruki', 1.45)
TK = Vector((-1.55, 0.6, Z0))
RK = Vector((1.55, 0.65, Z0))
T.place(tuki, 0, TK)
T.turn(tuki, 0, 25)
T.arm(tuki, 'R', 18, 0, None)
T.arm(tuki, 'R', 26, fwd=-70, out=20)
T.rest_arm(tuki, 'R', 40)
gesture(tuki, 'bounce', 4)
T.turn(tuki, 60, 10)
S(tuki, 84, (1, 1, 1))
S(tuki, 90, (1.1, 1.1, 0.86))
S(tuki, 104, (1, 1, 1))
for side in ('L', 'R'):
    T.arm(tuki, side, 84, 0, None)
    T.arm(tuki, side, 92, fwd=-20, out=70)
    T.arm(tuki, side, 120, fwd=-20, out=70)
    T.rest_arm(tuki, side, 132)
T.turn(tuki, 146, 40)
T.turn(tuki, 236, 20)
T.turn(tuki, 336, 5)
gesture(tuki, 'hops', 398)
for side in ('L', 'R'):
    T.arm(tuki, side, 400, 0, None)
    T.arm(tuki, side, 406, fwd=-60, out=60)
    T.arm(tuki, side, 444, fwd=-60, out=60)
    T.rest_arm(tuki, side, 456)
T.turn(tuki, 470, 35)
T.turn(tuki, 680, 20)
T.arm(tuki, 'R', 688, 0, None)
T.arm(tuki, 'R', 696, fwd=-80, out=30)
T.arm(tuki, 'R', 714, fwd=-80, out=30)
T.rest_arm(tuki, 'R', 726)
T.turn(tuki, 730, 0)
gesture(tuki, 'hops', 760)
for side in ('L', 'R'):
    T.arm(tuki, side, 758, 0, None)
    T.arm(tuki, side, 764, fwd=-10, out=150)
    T.arm(tuki, side, 800, fwd=-10, out=150)
    T.rest_arm(tuki, side, 812)
gesture(tuki, 'sway', 820)

T.place(ruki, 0, RK)
T.turn(ruki, 0, -25)
T.turn(ruki, 120, -45)
T.arm(ruki, 'L', 120, 0, None)
T.arm(ruki, 'L', 130, fwd=-60, out=40)
T.arm(ruki, 'L', 196, fwd=-60, out=40)
T.rest_arm(ruki, 'L', 208)
T.turn(ruki, 216, -20)
T.arm(ruki, 'L', 224, 0, None)
T.arm(ruki, 'L', 232, fwd=-70, out=50)
T.arm(ruki, 'L', 262, fwd=-70, out=50)
T.rest_arm(ruki, 'L', 272)
T.arm(ruki, 'R', 268, 0, None)
T.arm(ruki, 'R', 276, fwd=-70, out=50)
T.arm(ruki, 'R', 306, fwd=-70, out=50)
T.rest_arm(ruki, 'R', 318)
T.turn(ruki, 336, -10)
gesture(ruki, 'bounce', 404)
T.turn(ruki, 470, -30)
T.arm(ruki, 'L', 474, 0, None)
T.arm(ruki, 'L', 484, fwd=-80, out=30)
T.arm(ruki, 'L', 548, fwd=-80, out=30)
T.rest_arm(ruki, 'L', 560)
gesture(ruki, 'breathe', 566)
T.turn(ruki, 566, -15)
T.turn(ruki, 700, -35)
C.wave(ruki, 'R', 792, cycles=2, period=8)
gesture(ruki, 'bounce', 770)
confetti(760, (XL, GY + 0.2, 0.6), n=30, spread=1.6)

OP = ((0.0, -4.6, 6.8), (0.0, -1.05, 0.1), 30)
W0 = ((0.0, -7.2, 2.8), (0.0, -0.6, 0.85), 30)
WT = ((-1.0, -3.0, 1.4), (-1.2, 0.6, 0.95), 32)
WR = ((1.0, -3.0, 1.45), (1.2, 0.65, 1.0), 32)
WQ = ((0.0, -6.2, 2.6), (0.0, 0.1, 0.95), 29)
WD = ((0.0, -6.9, 5.8), (0.0, -1.9, 0.1), 30)
WS = ((0.0, -5.5, 2.5), (0.0, 0.3, 0.62), 30)
WG = ((0.0, -7.0, 3.6), (-0.15, -0.9, 0.5), 30)
for a, b, pose in ((0, 82, OP), (84, 138, WT), (140, 210, WR), (212, 332, WQ), (334, 396, WD), (398, 466, WT), (468, 556, WS), (558, 680, WD), (682, 790, WG), (792, TOTAL - 1, W0)):
    camkey(a, pose)
    camkey(b, pose)

T.lines(EID, LINES)
T.blinks(tuki, (50, 170, 300, 430, 600, 740, 840))
T.blinks(ruki, (70, 190, 320, 460, 620, 780))
