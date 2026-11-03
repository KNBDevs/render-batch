from stage import *
from episodes.burbuja_seca_plan import *
import ep_tools as T
import bmesh
from props.lib import spawn, auto_dress, M, MA, glyph
EID = 'burbuja_seca'
Z0 = 0.08
auto_dress(EID, ENV)
LI = (1.0, 0.55, 0.9)
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, LI), (50, LI), (64, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)
bgc = sc.world.node_tree.nodes['Background'].inputs[0]
b0 = tuple(bgc.default_value)
for f, c in ((0, (0.98, 0.72, 0.95, 1)), (50, (0.98, 0.72, 0.95, 1)), (64, b0)):
    bgc.default_value = c
    bgc.keyframe_insert('default_value', frame=f)

YT = -1.8
XD = -0.3
XW = 0.42
TW, TD, TH = 0.56, 0.42, 0.05
PH = 0.26
TZ = Z0 + PH + TH


def tray(name, x, rgb, prgb):
    C.rounded_box(name + '_ped', (x, YT, Z0 + PH / 2), (TW + 0.06, TD + 0.06, PH), 0.2, M(prgb, rough=0.5, coat=0.4), None)
    e = C.empty(name, None, (x, YT, Z0 + PH))
    C.rounded_box('base', (0, 0, TH / 2), (TW, TD, TH), 0.25, M(rgb, rough=0.45, coat=0.6), e)
    C.rounded_box('rim', (0, 0, TH + 0.004), (TW - 0.06, TD - 0.06, 0.008), 0.3, M(tuple(v * 0.9 for v in rgb), rough=0.6, coat=0.2), e)
    return e


tray('dry', XD, (1.0, 0.82, 0.42), (0.8, 0.62, 1.0))
tray('wet', XW, (1.0, 0.82, 0.42), (0.5, 0.85, 0.75))
film = C.empty('film', None, (XW, YT, TZ + 0.012))
C.rounded_box('f', (0, 0, 0), (TW - 0.07, TD - 0.07, 0.006), 0.4, MA((0.55, 0.8, 1.0), 0.55, rough=0.02, emit=0.12), film)
for k in range(5):
    C.sphere('drop', (-0.18 + 0.09 * k, -0.08 + 0.04 * (k % 3), 0.006), (0.02, 0.02, 0.008), MA((0.7, 0.9, 1.0), 0.6, rough=0.02, emit=0.2), film, 12)
film.scale = (0, 0, 0)
K(film, 'scale', 0, (0, 0, 0))
K(film, 'scale', 136, (0, 0, 0))
K(film, 'scale', 150, (0.35, 0.35, 1))
K(film, 'scale', 170, (0.7, 0.7, 1))
K(film, 'scale', 190, (1, 1, 1))

ST = Vector((-0.52, -1.36, Z0))
RH = 0.86
spawn('bubble_stand', 1, 820, 'candy', tuple(ST), 1.0, 0, h=RH)
RING = Vector((ST.x + 0.04, ST.y, Z0 + RH))
sp = spawn('sponge', 1, 830, 'pastel', (XW + 0.5, YT - 0.1, Z0), 1.0, 0)


def bmat():
    m = bpy.data.materials.new('bubble')
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    lw = nt.nodes.new('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.35
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    cr = ramp.color_ramp
    cr.elements[0].position = 0.0
    cr.elements[0].color = (0.75, 0.95, 1.0, 1)
    cr.elements[1].position = 1.0
    cr.elements[1].color = (1.0, 0.55, 0.95, 1)
    e = cr.elements.new(0.5)
    e.color = (1.0, 0.95, 0.45, 1)
    e = cr.elements.new(0.75)
    e.color = (0.55, 1.0, 0.7, 1)
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Strength'].default_value = 0.9
    gl = nt.nodes.new('ShaderNodeBsdfGlossy')
    gl.inputs['Roughness'].default_value = 0.02
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    add = nt.nodes.new('ShaderNodeAddShader')
    mix = nt.nodes.new('ShaderNodeMixShader')
    mt = nt.nodes.new('ShaderNodeMath')
    mt.operation = 'MULTIPLY_ADD'
    mt.inputs[1].default_value = 0.75
    mt.inputs[2].default_value = 0.22
    nt.links.new(lw.outputs['Facing'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], em.inputs['Color'])
    nt.links.new(ramp.outputs['Color'], gl.inputs['Color'])
    nt.links.new(em.outputs[0], add.inputs[0])
    nt.links.new(gl.outputs[0], add.inputs[1])
    nt.links.new(lw.outputs['Facing'], mt.inputs[0])
    nt.links.new(mt.outputs[0], mix.inputs['Fac'])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(add.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    try:
        m.surface_render_method = 'BLENDED'
    except Exception:
        pass
    return m


BM = bmat()
DM = MA((0.75, 0.92, 1.0), 0.7, rough=0.02, emit=0.4)


def ghost(o):
    for c in [o] + list(o.children_recursive):
        if hasattr(c, 'visible_shadow'):
            c.visible_shadow = False


def bubble(r):
    e = C.empty('bub', None, (0, 0, -5))
    C.sphere('s', (0, 0, 0), (r, r, r), BM, e, 32)
    ghost(e)
    e.scale = (0, 0, 0)
    return e


def dome(r, loc):
    e = C.empty('dome', None, loc)
    o = C.sphere('d', (0, 0, 0), (r, r, r), BM, e, 32)
    me = o.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.0001], context='VERTS')
    bm.to_mesh(me)
    bm.free()
    ghost(e)
    e.scale = (0, 0, 0)
    return e


def fly(e, f0, f1, p0, p1, wig=0.06, grow=8):
    K(e, 'scale', 0, (0, 0, 0))
    K(e, 'scale', f0 - 1, (0, 0, 0))
    K(e, 'scale', f0 + grow, (1, 1, 1))
    n = max(2, (f1 - f0) // 4)
    for i in range(n + 1):
        u = i / n
        p = p0.lerp(p1, u)
        p.z = p0.z + (p1.z - p0.z) * (u ** 1.3) + 0.12 * math.sin(math.pi * u)
        p.x += wig * math.sin(u * 7.0)
        K(e, 'location', f0 + round(u * (f1 - f0)), tuple(p))


def pop(e, f, at):
    K(e, 'scale', f, (1, 1, 1))
    K(e, 'scale', f + 2, (1.18, 1.18, 0.9))
    K(e, 'scale', f + 3, (0, 0, 0))
    for k in range(8):
        a = k * math.pi / 4
        d = C.empty('drop', None, (0, 0, -5))
        C.sphere('dr', (0, 0, 0), (0.014, 0.014, 0.014), DM, d, 10)
        ghost(d)
        p0 = at + Vector((0, 0, 0.05))
        p1 = at + Vector((0.16 * math.cos(a), 0.1 * math.sin(a), 0.1 + 0.03 * (k % 2)))
        K(d, 'scale', 0, (0, 0, 0))
        K(d, 'scale', f + 2, (0, 0, 0))
        K(d, 'scale', f + 3, (1, 1, 1))
        K(d, 'scale', f + 11, (0, 0, 0))
        K(d, 'location', f + 2, tuple(p0))
        K(d, 'location', f + 11, tuple(p1))
    ring = C.empty('splash', None, (at.x, at.y, at.z + 0.006))
    C.tube('r', [(math.cos(a / 20 * 6.2832) * 0.1, math.sin(a / 20 * 6.2832) * 0.1, 0) for a in range(21)], 0.006, DM, ring)
    ghost(ring)
    K(ring, 'scale', 0, (0, 0, 0))
    K(ring, 'scale', f + 2, (0, 0, 0))
    K(ring, 'scale', f + 3, (0.6, 0.6, 1))
    K(ring, 'scale', f + 10, (1.6, 1.6, 1))
    K(ring, 'scale', f + 12, (0, 0, 0))


def settle(e, f, at, r, ro=1.26):
    K(e, 'scale', f, (1, 1, 1))
    K(e, 'scale', f + 3, (0, 0, 0))
    d = dome(r * ro, (at.x, at.y, TZ + 0.014))
    K(d, 'scale', 0, (0, 0, 0))
    K(d, 'scale', f + 1, (0, 0, 0))
    K(d, 'scale', f + 4, (1.12, 1.12, 0.85))
    K(d, 'scale', f + 8, (0.96, 0.96, 1.06))
    K(d, 'scale', f + 12, (1, 1, 1))
    return d


R0 = 0.16
b0 = bubble(0.18)
fly(b0, 0, 32, Vector((XD - 0.05, YT, TZ + 1.0)), Vector((XD, YT, TZ + 0.13)), wig=0.04, grow=3)
pop(b0, 33, Vector((XD, YT, TZ)))

b1 = bubble(R0)
b2 = bubble(R0)
fly(b1, 340, 390, RING + Vector((0.12, 0, 0)), Vector((XD + 0.02, YT, TZ + R0)))
pop(b1, 391, Vector((XD + 0.02, YT, TZ)))
fly(b2, 350, 400, RING + Vector((0.12, 0, 0)), Vector((XW, YT + 0.02, TZ + R0)), wig=0.08)
settle(b2, 401, Vector((XW, YT + 0.02, 0)), R0)

SPOTS = [(-0.14, -0.06, 0.1), (0.15, -0.07, 0.09), (-0.04, 0.09, 0.1), (0.16, 0.1, 0.08), (0.02, -0.1, 0.075)]
for k, (dx, dy, r) in enumerate(SPOTS):
    b = bubble(r)
    f0 = 694 + k * 5
    fly(b, f0, f0 + 36 + k * 3, RING + Vector((0.12, 0, 0.02 * k)), Vector((XW + dx, YT + dy, TZ + r)), wig=0.05 + 0.01 * k)
    settle(b, f0 + 37 + k * 3, Vector((XW + dx, YT + dy, 0)), r)

air_m = MA((1.0, 1.0, 1.0), 0.6, emit=0.6)


def puff(f):
    e = C.empty('puff', None, (RING.x - 0.2, RING.y, RING.z))
    for dz in (-0.05, 0.0, 0.05):
        C.tube('l', [(0, 0, dz), (0.1, 0, dz)], 0.008, air_m, e)
    ghost(e)
    K(e, 'scale', 0, (0, 0, 0))
    K(e, 'scale', f - 1, (0, 0, 0))
    K(e, 'scale', f + 2, (1, 1, 1))
    K(e, 'location', f, (RING.x - 0.2, RING.y, RING.z))
    K(e, 'location', f + 10, (RING.x - 0.08, RING.y, RING.z))
    K(e, 'scale', f + 12, (0, 0, 0))


for f in (338, 348, 692, 700, 708):
    puff(f)

SP0 = Vector((XW + 0.5, YT - 0.1, Z0))
K(sp, 'location', 0, tuple(SP0))
K(sp, 'location', 128, tuple(SP0))
K(sp, 'location', 136, (XW + 0.16, YT, TZ + 0.012))
for k, x in enumerate((-0.14, 0.14, -0.12, 0.14, -0.1, 0.1)):
    K(sp, 'location', 142 + k * 8, (XW + x, YT + (0.05 if k % 2 else -0.05), TZ + 0.012))
K(sp, 'location', 196, (XW + 0.12, YT, TZ + 0.012))
K(sp, 'location', 204, tuple(SP0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.18, sz=0.13):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)


OR = (0.8, 0.2, 0.0)
BL = (0.0, 0.2, 0.7)
label('¿SECA?', OR, (XD - 0.05, YT - 0.1, Z0 + 1.22), 0.62, 236, 330)
label('¿MOJADA?', BL, (XW + 0.08, YT - 0.1, Z0 + 1.22), 0.84, 242, 330)
label('SECA', OR, (XD - 0.05, YT - 0.1, Z0 + 1.22), 0.54, 536, 630)
label('MOJADA', BL, (XW + 0.08, YT - 0.1, Z0 + 1.22), 0.78, 540, 630)

OP = ((XD + 0.18, YT - 1.05, TZ + 0.1), (XD, YT, TZ + 0.3), 30)
W = ((0.0, -5.5, 1.6), (0.04, -1.6, 0.64), 26)
WQ = ((0.0, -5.1, 1.5), (0.04, -1.65, 0.68), 25)
CW = ((XW + 0.02, YT - 1.75, TZ + 0.5), (XW + 0.24, YT + 0.2, TZ + 0.28), 30)
CB = ((0.06, YT - 1.9, TZ + 0.6), (0.06, YT, TZ + 0.12), 30)
WE = ((0.5, YT - 2.3, TZ + 0.75), (0.52, YT + 0.3, TZ + 0.3), 26)
for a, b, pose in ((0, 58, OP), (60, 200, W), (202, 330, WQ), (332, 462, W), (464, 520, CW), (522, 636, WQ),
                   (638, 736, W), (738, TOTAL - 1, WE)):
    camkey(a, pose)
    camkey(b, pose)

bolita = make('bolita', 1.2)
pimo = make('pimo', 1.4)
BK0 = Vector((-0.9, -1.3, Z0))
PK0 = Vector((0.98, -1.28, Z0))
T.place(bolita, 0, BK0)
T.turn(bolita, 0, 25)
for side in ('L', 'R'):
    T.arm(bolita, side, 34, 0, None)
    T.arm(bolita, side, 40, fwd=-60, out=60)
    T.arm(bolita, side, 80, fwd=-60, out=60)
    T.rest_arm(bolita, side, 90)
T.turn(bolita, 200, 15)
T.arm(bolita, 'R', 206, 0, None)
T.arm(bolita, 'R', 214, fwd=-70, out=35)
T.arm(bolita, 'R', 300, fwd=-70, out=35)
T.rest_arm(bolita, 'R', 310)
T.turn(bolita, 322, 70)
for f in (336, 346, 690, 698, 706):
    S(bolita, f, (1.06, 1.06, 0.94))
    S(bolita, f + 4, (0.96, 0.96, 1.05))
    S(bolita, f + 8, (1, 1, 1))
T.turn(bolita, 396, 30)
for side in ('L', 'R'):
    T.arm(bolita, side, 404, 0, None)
    T.arm(bolita, side, 410, fwd=-150, out=20)
    T.arm(bolita, side, 440, fwd=-150, out=20)
    T.rest_arm(bolita, side, 450)
T.turn(bolita, 630, 20)
T.arm(bolita, 'R', 640, 0, None)
T.arm(bolita, 'R', 646, fwd=-150, out=10)
T.arm(bolita, 'R', 670, fwd=-150, out=10)
T.rest_arm(bolita, 'R', 678)
T.turn(bolita, 682, 70)
BK1 = Vector((-0.8, -0.9, Z0))
BK2 = Vector((0.12, -1.12, Z0))
T.turn(bolita, 734, 40)
hop_to(bolita, 736, BK0, BK1, 11, 0.35)
hop_to(bolita, 748, BK1, BK2, 12, 0.35)
T.turn(bolita, 760, 10)
gesture(bolita, 'hops', 772)
for side in ('L', 'R'):
    T.arm(bolita, side, 762, 0, None)
    T.arm(bolita, side, 768, fwd=-150, out=25)
    T.arm(bolita, side, 800, fwd=-150, out=25)
    T.rest_arm(bolita, side, 810)
C.wave(bolita, 'L', 820, cycles=2, period=8)

T.place(pimo, 0, PK0)
T.turn(pimo, 0, -30)
T.arm(pimo, 'R', 96, 0, None)
T.arm(pimo, 'R', 104, fwd=-150, out=10)
T.arm(pimo, 'R', 124, fwd=-150, out=10)
T.rest_arm(pimo, 'R', 130)
PK1 = Vector((0.9, -1.45, Z0))
hop_to(pimo, 122, PK0, PK1, 12, 0.3)
T.turn(pimo, 126, -70)
T.arm(pimo, 'L', 130, 0, None)
for k in range(7):
    f = 136 + k * 8
    T.arm(pimo, 'L', f, fwd=-75, out=20 + (15 if k % 2 else 0))
T.rest_arm(pimo, 'L', 204)
hop_to(pimo, 200, PK1, PK0, 12, 0.3)
T.turn(pimo, 206, -30)
gesture(pimo, 'breathe', 240)
T.turn(pimo, 440, -40)
gesture(pimo, 'hops', 468)
T.arm(pimo, 'L', 528, 0, None)
T.arm(pimo, 'L', 536, fwd=-80, out=35)
T.arm(pimo, 'L', 600, fwd=-80, out=35)
T.rest_arm(pimo, 'L', 610)
T.turn(pimo, 640, -25)
for side in ('L', 'R'):
    T.arm(pimo, side, 744, 0, None)
    T.arm(pimo, side, 752, fwd=-120, out=30)
    T.arm(pimo, side, 796, fwd=-120, out=30)
    T.rest_arm(pimo, side, 806)
C.wave(pimo, 'R', 814, cycles=2, period=8)
confetti(744, (XW, YT, Z0 + 0.9), n=20, spread=1.1)

T.lines(EID, LINES)
T.blinks(bolita, (44, 160, 300, 470, 580, 690, 830))
T.blinks(pimo, (70, 190, 340, 480, 630, 780))
