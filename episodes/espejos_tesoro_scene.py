from stage import *
from episodes.espejos_tesoro_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'espejos_tesoro'
Z0 = 0.08
auto_dress(EID, ENV)
NIGHT = (0.45, 0.55, 1.0)
for l in list(bpy.data.lights):
    e = l.energy * 0.42
    for f, c, k in ((0, NIGHT, 0.45), (64, NIGHT, 0.45), (80, (0.78, 0.84, 1.0), 1.0)):
        l.color = c
        l.keyframe_insert('color', frame=f)
        l.energy = e * k
        l.keyframe_insert('energy', frame=f)
bg = sc.world.node_tree.nodes['Background'].inputs
b0 = tuple(bg[0].default_value)
for f, c in ((0, (0.12, 0.16, 0.42, 1)), (64, (0.12, 0.16, 0.42, 1)), (80, b0)):
    bg[0].default_value = c
    bg[0].keyframe_insert('default_value', frame=f)
sc.world.node_tree.nodes['Background'].inputs[1].default_value = 0.2
bpy.data.materials['Sky'].node_tree.nodes['Emission'].inputs[1].default_value = 0.45

CREAM = M((1.0, 0.96, 0.9), rough=0.35, coat=0.7)
CORAL = M((1.0, 0.5, 0.45), rough=0.35, coat=0.7)
MINT = M((0.45, 0.85, 0.7), rough=0.4, coat=0.6)
GOLD = M((1.0, 0.8, 0.3), rough=0.3, coat=0.8)
SKYB = M((0.5, 0.75, 1.0), rough=0.35, coat=0.7)
LILA = M((0.72, 0.6, 1.0), rough=0.35, coat=0.7)

TY = -1.95
TP = Vector((-1.0, TY, 0.5))
CH = Vector((0.8, TY, Z0))
GEM = CH + Vector((0, -0.02, 0.5))
M1 = Vector((-0.62, -1.2, Z0))
M2 = Vector((0.62, -1.2, Z0))
MS = 1.4
F1 = M1 + Vector((0, 0, 0.36 * MS))
F2 = M2 + Vector((0, 0, 0.36 * MS))

tower = C.empty('tower', None, (0, TY, Z0))
for k, m in enumerate((CORAL, SKYB, GOLD, MINT, LILA)):
    C.rounded_box('blk', (0.02 * (-1) ** k, 0, 0.12 + k * 0.23), (0.56, 0.42, 0.22), 0.12, m, tower)
C.sphere('top', (0, 0, 1.3), (0.13, 0.13, 0.13), CORAL, tower, 24)

chest = C.empty('chest', None, tuple(CH))
C.rounded_box('body', (0, 0, 0.16), (0.46, 0.32, 0.3), 0.15, CORAL, chest)
C.rounded_box('lid', (0, 0, 0.34), (0.5, 0.36, 0.08), 0.4, GOLD, chest)
C.rounded_box('lock', (0, -0.17, 0.25), (0.08, 0.03, 0.1), 0.4, GOLD, chest)
gem_m = M((0.4, 0.95, 0.85), rough=0.15, coat=0.9, emit=0.3)
C.sphere('gem', (0, -0.02, 0.5), (0.11, 0.11, 0.13), gem_m, chest, 24)
chest.scale = (1.15, 1.15, 1.15)
GEM = CH + Vector((0, -0.02, 0.5 * 1.15))

torch = spawn('toy_torch', 1, 9142, 'fresh', tuple(TP), 1.25, 0)
bpy.ops.object.light_add(type='SPOT', location=(0.09, 0, 0))
tl = bpy.context.object
tl.parent = torch
tl.rotation_euler = (0, -math.pi / 2, 0)
tl.data.color = (1.0, 0.92, 0.68)
tl.data.energy = 40
tl.data.spot_size = math.radians(22)
tl.data.spot_blend = 0.6
stand = C.empty('tstand', None, (TP.x, TY, Z0))
C.lathe('st', [(0.0, 0.0), (0.0, 0.16), (0.05, 0.14), (0.36, 0.05), (0.38, 0.0)], SKYB, stand, segs=32)

beam_m = MA((1.0, 0.94, 0.62), 0.2, emit=1.0)
spot_m = M((1.0, 0.95, 0.7), rough=0.3, emit=3.0)


def beam(name, r0, r1):
    o = C.empty(name, None, (0, 0, 0))
    C.lathe('cone', [(0.0, 0.0), (0.0, r0), (1.0, r1), (1.0, 0.0)], beam_m, o, segs=32)
    o.scale = (0, 0, 0)
    return o


def aim(o, f, A, B, on=True):
    d = B - A
    K(o, 'location', f, tuple(A))
    K(o, 'rotation_euler', f, tuple(d.to_track_quat('Z', 'Y').to_euler()))
    K(o, 'scale', f, (1, 1, d.length) if on else (0, 0, 0))


def point(f, tgt):
    d = tgt - TP
    K(torch, 'rotation_euler', f, (0, -math.atan2(d.z, math.hypot(d.x, d.y)), math.atan2(d.y, d.x)))


def disc(name, loc, n, r, m):
    q = Vector((0, 0, 1)).rotation_difference(n.normalized())
    o = C.empty(name, None, tuple(loc), tuple(q.to_euler()))
    C.sphere('d', (0, 0, 0), (r, r, 0.004), m, o, 24)
    return o


def show(o, f_in, f_out=None, s=1.0):
    K(o, 'scale', 0, (0, 0, 0))
    K(o, 'scale', f_in - 1, (0, 0, 0))
    K(o, 'scale', f_in + 3, (s, s, s))
    if f_out:
        K(o, 'scale', f_out, (s, s, s))
        K(o, 'scale', f_out + 3, (0, 0, 0))


def mirror(loc, a, b, seed):
    mr = spawn('hand_mirror', 0, seed, 'candy', tuple(loc), MS, 0)
    F = loc + Vector((0, 0, 0.36 * MS))
    face = next(o for o in mr.children if o.name.startswith('face'))
    nrm = ((a - F).normalized() + (b - F).normalized()).normalized()
    face.rotation_euler = Vector((0, -1, 0)).rotation_difference(nrm).to_euler()
    return mr, F, nrm


HITW = Vector((-0.3, TY, TP.z + (GEM.z - TP.z) * (0.7 / 1.8)))
b1 = beam('b1', 0.03, 0.09)
TA = TP + (GEM - TP).normalized() * 0.1
point(0, GEM)
aim(b1, 0, TA, HITW)
point(262, GEM)
aim(b1, 262, TA, HITW)
sw = disc('spw', HITW + Vector((-0.01, 0, 0)), Vector((-1, 0, 0)), 0.09, spot_m)
show(sw, 1, 266)

mr1, F1, n1 = mirror(M1, TP, F2, 5512)
mr2, F2b, n2 = mirror(M2, F1, GEM, 5513)
T.pop_in(mr1, 256, MS, 10)
T.pop_in(mr2, 330, MS, 10)
T.pop_out(mr2, 518, MS, 6)
T.pop_in(mr2, 580, MS, 8)
TB = TP + (F1 - TP).normalized() * 0.1
point(268, F1)
aim(b1, 268, TB, F1)
aim(b1, 900, TB, F1)
show(disc('sp1', F1 + n1 * 0.02, n1, 0.07, spot_m), 270)

FAR = F1 + (F2 - F1) * 1.6
b2 = beam('b2', 0.05, 0.09)
aim(b2, 0, F1, F1 + (F2 - F1) * 0.05, False)
aim(b2, 273, F1, F1 + (F2 - F1) * 0.05, False)
aim(b2, 274, F1, F1 + (F2 - F1) * 0.05)
aim(b2, 300, F1, FAR)
aim(b2, 334, F1, FAR)
aim(b2, 336, F1, F2)
aim(b2, 520, F1, F2)
aim(b2, 523, F1, FAR)
aim(b2, 582, F1, FAR)
aim(b2, 586, F1, F2)
aim(b2, 900, F1, F2)
sp2 = disc('sp2', F2 + n2 * 0.02, n2, 0.07, spot_m)
show(sp2, 338, 518)
show(sp2, 588)

b3 = beam('b3', 0.05, 0.09)
for f, on, e in ((0, False, 0.05), (339, False, 0.05), (340, True, 0.05), (360, True, 1.0), (518, True, 1.0), (520, False, 1.0),
                 (588, False, 0.05), (589, True, 0.05), (600, True, 1.0), (900, True, 1.0)):
    aim(b3, f, F2, F2 + (GEM - F2) * e, on)
halo = C.empty('halo', None, tuple(GEM + Vector((0, -0.04, 0))))
C.sphere('h', (0, 0, 0), (0.2, 0.2, 0.2), MA((0.6, 1.0, 0.9), 0.14, emit=1.0), halo, 24)
show(halo, 362, 518)
show(halo, 600)
bpy.ops.object.light_add(type='POINT', location=tuple(GEM + Vector((0, -0.3, 0.15))))
gl = bpy.context.object
gl.data.color = (0.6, 1.0, 0.9)
for f, v in ((0, 0), (360, 0), (366, 14), (516, 14), (522, 0), (598, 0), (604, 14), (TOTAL, 14)):
    gl.data.energy = v
    gl.data.keyframe_insert('energy', frame=f)
for f in range(364, 500, 12):
    K(chest, 'scale', f, (1.15, 1.15, 1.15))
    K(chest, 'scale', f + 6, (1.21, 1.21, 1.21))
K(chest, 'scale', 506, (1.15, 1.15, 1.15))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.25), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


KC, OC, GC = (0.08, 0.06, 0.16), (0.85, 0.35, 0.05), (0.05, 0.42, 0.15)
LZ, LY = 1.95, -2.0
label('¿LLEGA?', GC, (-0.55, LY, LZ), 0.98, 190, 372, 0.3, 0.19)
label('¿NO LLEGA?', OC, (0.55, LY, LZ), 1.12, 198, 372, 0.3, 0.17)
label('¡LLEGA!', GC, (0.0, LY, LZ), 0.92, 396, 482, 0.3, 0.22)
label('¡NO LLEGA!', OC, (0.0, LY, LZ), 1.12, 552, 584, 0.3, 0.2)

EYP = -2.95
exp = C.empty('diagram', None, (0.0, EYP, 1.1))
C.rounded_box('panel', (0, 0.04, 0.4), (1.3, 0.03, 0.9), 0.4, M((0.5, 0.56, 0.92), rough=0.8, coat=0.0), exp)
YEL = M((1.0, 0.85, 0.3), rough=0.3, coat=0.6, emit=1.2)
GRY = M((0.85, 0.9, 1.0), rough=0.2, coat=0.9, emit=0.3)
for sx in (-1, 1):
    cx = sx * 0.31
    C.rounded_box('tw', (cx, -0.03, 0.32), (0.1, 0.02, 0.42), 0.3, CORAL, exp)
    C.sphere('tl', (cx - 0.24, -0.04, 0.32), (0.04, 0.02, 0.04), GOLD, exp, 16)
    C.sphere('tg', (cx + 0.2, -0.04, 0.2), (0.045, 0.02, 0.05), MINT, exp, 16)
    if sx < 0:
        C.tube('ray', [(cx - 0.22, -0.045, 0.32), (cx - 0.06, -0.045, 0.32)], 0.014, YEL, exp)
        C.sphere('bang', (cx - 0.055, -0.05, 0.32), (0.03, 0.01, 0.03), M((1.0, 0.4, 0.3), emit=1.0), exp, 12)
    else:
        for mx, mz in ((cx - 0.2, 0.62), (cx + 0.2, 0.62)):
            C.rounded_box('mi', (mx, -0.04, mz), (0.08, 0.015, 0.08), 0.4, GRY, exp)
        C.tube('ray', [(cx - 0.22, -0.045, 0.33), (cx - 0.2, -0.045, 0.6), (cx + 0.2, -0.045, 0.6), (cx + 0.2, -0.045, 0.25)], 0.014, YEL, exp)
C.rounded_box('sep', (0, -0.03, 0.4), (0.014, 0.01, 0.7), 0.3, M((0.3, 0.35, 0.6), rough=0.5), exp)
T.pop_in(exp, 590, 1.2, 10)
T.pop_out(exp, 768, 1.2, 6)
label('CHOCA', OC, (-0.37, EYP - 0.1, 1.06), 0.5, 600, 768, 0.17, 0.11)
label('LLEGA', GC, (0.37, EYP - 0.1, 1.06), 0.5, 640, 768, 0.17, 0.11)
label('CHOCA', OC, (0.0, LY, LZ), 0.9, 792, 824, 0.3, 0.2)
label('LLEGA', GC, (0.0, LY, LZ), 0.9, 830, TOTAL + 10, 0.3, 0.2)
confetti(856, (0.0, TY, Z0 + 2.0), n=24, spread=1.2)

OP = ((-1.2, -4.0, 0.75), (-0.35, TY, 0.6), 22)
W = ((0.0, -5.6, 2.1), (0.0, -1.45, 0.95), 18)
CU = ((0.6, -4.6, 1.6), (0.3, -1.6, 0.6), 22)
EXP = ((0.0, -5.25, 1.55), (0.0, EYP, 1.5), 30)
camkey(0, OP)
camkey(56, OP)
for a, b, pose in ((70, 186, W), (188, 330, W), (332, 400, CU), (402, 584, W), (588, 770, EXP), (772, TOTAL - 1, W)):
    camkey(a, pose)
    camkey(b, pose)

bol = make('bolita', 1.0)
mok = make('moki', 1.0)
BP, MP = Vector((-1.6, -1.75, Z0)), Vector((1.68, -1.75, Z0))
T.turn(bol, 0, 25)
T.turn(mok, 0, -25)
for ch, p0, dx in ((bol, BP, -0.7), (mok, MP, 0.7)):
    T.place(ch, 0, p0 + Vector((dx, 0, 0)))
    T.place(ch, 66, p0 + Vector((dx, 0, 0)))
    T.place(ch, 68, p0)
    T.place(ch, 586, p0)
    T.place(ch, 588, p0 + Vector((dx * 1.4, 0, 0)))
    T.place(ch, 770, p0 + Vector((dx * 1.4, 0, 0)))
    T.place(ch, 772, p0)

for ch, side, f0 in ((mok, 'L', 104), (bol, 'R', 182), (bol, 'R', 250), (mok, 'L', 324), (bol, 'R', 500), (bol, 'R', 782), (bol, 'R', 822)):
    T.arm(ch, side, f0, 0, None)
    T.arm(ch, side, f0 + 6, fwd=-85, out=30)
    T.arm(ch, side, f0 + 20, fwd=-85, out=30)
    T.rest_arm(ch, side, f0 + 28)
gesture(bol, 'hops', 72)
gesture(mok, 'hops', 410)
gesture(bol, 'hops', 846)
C.wave(bol, 'R', 862, cycles=2, period=10)
C.wave(mok, 'L', 858, cycles=2, period=10)

T.lines(EID, LINES)
T.blinks(bol, (70, 200, 340, 470, 620, 740, 880))
T.blinks(mok, (80, 230, 360, 520, 660, 800))
