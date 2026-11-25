from stage import *
from episodes.nav26_02_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, MA, glyph
from props.costumes import dress
from episodes.nav_look import winter, snow
EID = 'nav26_02'
Z0 = 0.08
auto_dress(EID, ENV)
winter()
snow(TOTAL, n=80, speed=0.01)
F = {l[0]: l[3] for l in LINES}
D = {l[0]: int(T.dur(f'ep_{EID}_{l[0]}', l[2]) * FPS) for l in LINES}

TX, TY = 0.0, -1.45
spawn('low_table', 0, 6201, 'pastel', (TX, TY, Z0), 1.0, 0)
TOP = Z0 + 0.62
NAVY = M((0.08, 0.12, 0.3), rough=0.9)
cush = C.empty('cushion', None, (TX, TY, TOP))
C.rounded_box('c', (0, 0, 0.05), (0.42, 0.42, 0.1), 0.5, NAVY, cush)
ICEM = MA((0.35, 0.68, 1.0), 0.92, rough=0.1, emit=0.35)
HI = M((1.0, 0.85, 0.3), rough=0.3, emit=0.6)
DROP = MA((0.45, 0.7, 1.0), 0.8, rough=0.05, emit=0.2)


def flake(name, parent, loc, r, rot=(0, 0, 0)):
    o = C.empty(name, parent, loc, rot)
    C.sphere('hub', (0, 0, 0), (r * 0.16, r * 0.16, r * 0.05), ICEM, o, 16)
    arms = []
    for k in range(6):
        a = C.empty(f'arm{k}', o, (0, 0, 0), (0, 0, math.radians(90 + 60 * k)))
        C.tube('s', [(0, 0, 0), (r, 0, 0)], r * 0.06, ICEM, a)
        for t, L in ((0.45, 0.3), (0.72, 0.2)):
            for sg in (-1, 1):
                C.tube('b', [(r * t, 0, 0), (r * (t + L * 0.6), sg * r * L, 0)], r * 0.045, ICEM, a)
        C.sphere('tip', (r, 0, 0), (r * 0.07, r * 0.07, r * 0.05), ICEM, a, 10)
        arms.append(a)
    return o, arms


small, _ = flake('small', None, (TX, TY, 2.4), 0.05)
LAND = F['l1'] - 6
K(small, 'location', 0, (TX + 0.3, TY - 0.1, 2.6))
K(small, 'scale', 0, (3, 3, 3))
K(small, 'scale', LAND - 20, (1, 1, 1))
K(small, 'location', LAND, (TX, TY, TOP + 0.11))
for f in range(0, LAND, 12):
    K(small, 'rotation_euler', f, (0, 0, math.radians(f * 2)))
K(small, 'rotation_euler', LAND, (0, 0, math.radians(LAND * 2)))

LS = 1.35
lupa = spawn('magnifier', 0, 6202, 'candy', (0, 0, 0), LS, 0)
lupa.rotation_euler = (0, math.radians(-90), 0)
for o in lupa.children_recursive:
    if o.type == 'MESH' and o.data.materials and o.data.materials[0].name.startswith('pa'):
        o.visible_shadow = False
lens_c = Vector((-0.42 * LS, 0, 0))
SPOT = Vector((TX, TY, TOP + 0.12))
L_ON = SPOT + Vector((0, -0.2, 0.2)) - lens_c
L_OFF = Vector((0.42, TY - 0.32, TOP + 0.5)) - lens_c
view = C.empty('view', lupa, (0, 0.03, 0.42), (0, math.radians(90), 0))
C.sphere('vbg', (0, 0.012, 0), (0.165, 0.004, 0.165), NAVY, view, 40)
big, arms = flake('big', view, (0, -0.01, 0), 0.14, (math.radians(90), 0, 0))
drop = C.empty('drop', view, (0, -0.03, -0.02))
C.sphere('d', (0, 0, 0), (0.05, 0.04, 0.06), DROP, drop, 24)

ON = F['m2'] + D['m2'] - 4
K(lupa, 'location', 0, tuple(L_OFF))
K(lupa, 'scale', 0, (0, 0, 0))
K(lupa, 'scale', F['m2'] + 4, (0, 0, 0))
K(lupa, 'scale', F['m2'] + 12, (LS, LS, LS))
K(lupa, 'location', ON - 12, tuple(L_OFF))
K(lupa, 'location', ON, tuple(L_ON))
K(view, 'scale', 0, (0, 0, 0))
K(view, 'scale', ON, (0, 0, 0))
K(view, 'scale', ON + 1, (1, 1, 1))
set_interp(view, 'CONSTANT')
K(lupa, 'location', F['m4'] - 6, tuple(L_ON))
K(lupa, 'location', F['m4'] + 6, tuple(L_OFF))
K(lupa, 'scale', F['m4'] + 2, (LS, LS, LS))
K(lupa, 'scale', F['m4'] + 10, (0, 0, 0))
intro, _ = flake('intro', None, (0.2, -2.35, 2.05), 0.22, (math.radians(90), 0, 0))
for f in range(0, 50, 2):
    K(intro, 'rotation_euler', f, (math.radians(90), math.radians(f * 3), 0))
K(intro, 'scale', 0, (1, 1, 1))
K(intro, 'location', 0, (0.2, -2.35, 2.05))
K(intro, 'scale', 34, (1, 1, 1))
K(intro, 'location', 48, (0.3, -1.6, 2.4))
K(intro, 'scale', 48, (0, 0, 0))

C0 = F['m3'] + 4
NUMS = []
step = max(10, (D['m3'] - 20) // 6)
for k, a in enumerate(arms):
    f = C0 + k * step
    K(a, 'scale', f - 1, (1, 1, 1))
    K(a, 'scale', f + 3, (1.18, 1.6, 1.6))
    K(a, 'scale', f + 9, (1, 1, 1))
    ang = math.radians(90 + 60 * k)
    NUMS.append((k, f))

M0 = F['l3'] + 10
M1 = M0 + 50
K(big, 'scale', 0, (1, 1, 1))
K(big, 'scale', M0, (1, 1, 1))
K(big, 'scale', M1, (0, 0, 0))
K(drop, 'scale', 0, (0, 0, 0))
K(drop, 'scale', M0 + 20, (0, 0, 0))
K(drop, 'scale', M1 + 6, (1, 1, 1))
K(small, 'scale', M0, (1, 1, 1))
K(small, 'scale', M1, (0, 0, 0))
sdrop = C.empty('sdrop', None, (TX, TY, TOP + 0.115))
C.sphere('d', (0, 0, 0), (0.025, 0.025, 0.018), DROP, sdrop, 16)
K(sdrop, 'scale', 0, (0, 0, 0))
K(sdrop, 'scale', M0 + 20, (0, 0, 0))
K(sdrop, 'scale', M1 + 6, (1, 1, 1))
for l in list(bpy.data.lights):
    base = tuple(l.color)
    for f, c in ((0, base), (M0 - 10, base), (M0, (1.0, 0.75, 0.5)), (M1 + 10, (1.0, 0.75, 0.5)), (M1 + 30, base)):
        l.color = c
        l.keyframe_insert('color', frame=f)

hero, harms = flake('hero', None, (0, TY - 0.6, 2.1), 0.34, (math.radians(90), 0, 0))
K(hero, 'scale', 0, (0, 0, 0))
T.pop_in(hero, F['m4'] + 4, 1.0, 10)
for f in range(F['m4'] + 14, TOTAL, 2):
    K(hero, 'rotation_euler', f, (math.radians(90), math.radians((f - F['m4']) * 0.8), 0))


def label(txt, rgb, loc, w, f_in, f_out, h=0.27, sz=0.2):
    e = C.empty('lab', None, loc)
    C.rounded_box('card', (0, 0, 0), (w, 0.03, h), 0.5, M((1.0, 0.98, 0.94), rough=0.5, coat=0.3, emit=0.15), e)
    glyph(txt, sz, 0.012, M(rgb, rough=0.35, coat=0.5, emit=0.15), e, (0, -0.022, -0.004))
    T.pop_in(e, f_in, 1.0, 8)
    T.pop_out(e, f_out, 1.0, 6)
    return e


BC, OC, GC = (0.04, 0.14, 0.55), (0.7, 0.2, 0.02), (0.05, 0.42, 0.15)
label('¿CÓMO ES DE CERCA?', BC, (0.0, TY - 0.55, Z0 + 1.65), 1.4, F['l1'] + 10, F['m2'] - 2, 0.27, 0.15)
for k, f in NUMS[:5]:
    label(str(k + 1), GC, (0.0, TY - 0.5, TOP + 0.95), 0.3, f, f + step - 2, 0.24, 0.17)
label('¡6 PUNTAS!', GC, (-0.05, TY - 0.5, TOP + 0.95), 0.9, NUMS[5][1], F['l3'] - 2, 0.24, 0.16)
label('¡UNA GOTITA!', OC, (-0.05, TY - 0.5, TOP + 0.95), 1.0, M1 - 4, F['m4'] - 2, 0.24, 0.16)
label('HIELO CON 6 PUNTAS', BC, (0.05, TY - 0.95, 0.88), 1.35, F['m4'] + 24, TOTAL + 10, 0.24, 0.14)

moki = make('moki', 1.4)
luma = make('luma', 1.3)
dress(moki, 'moki', COSTUME, 0)
dress(luma, 'luma', COSTUME, 1)
spawn('play_step', 0, 6203, 'fresh', (-0.66, -0.78, Z0), 1.1, 0)
MK = Vector((-0.66, -0.82, Z0 + 0.235 * 1.1))
LM = Vector((0.95, -1.1, Z0))
T.place(moki, 0, MK)
T.turn(moki, 0, 20)
T.place(luma, 0, LM)
T.turn(luma, 0, -35)
for f, z in ((0, 0), (14, 8), (40, 8), (52, 0)):
    K(moki['spin'], 'rotation_euler', f, (math.radians(-z), 0, 0))
gesture(moki, 'hops', 18)
for f0 in (F['m2'] + 2,):
    T.arm(luma, 'R', f0, 0, None)
    T.arm(luma, 'R', f0 + 6, fwd=-95, out=35)
    T.arm(luma, 'R', f0 + 18, fwd=-95, out=35)
    T.rest_arm(luma, 'R', f0 + 26)
for k in range(6):
    f0 = C0 + k * step
    T.arm(moki, 'L', f0 - 2, fwd=-40 if k % 2 else -70, out=45)
T.rest_arm(moki, 'L', C0 + 6 * step + 6)
gesture(luma, 'hops', F['l2'] + 4)
gesture(luma, 'breathe', F['l3'] + 4)
gesture(moki, 'hops', F['m4'] + 30)
C.wave(moki, 'R', TOTAL - 44, cycles=2, period=8)
C.wave(luma, 'L', TOTAL - 44, cycles=2, period=8)

OP = ((0.15, -3.1, 2.1), (0.2, -1.45, 2.1), 22)
W = ((0.04, -4.0, 1.55), (0.04, -1.25, 1.0), 21)
CB = ((0.02, -3.0, 1.32), (0.02, TY, 1.16), 21)
CL = ((0.04, -3.7, 1.38), (0.04, TY, 1.02), 21)
HE = ((0.0, -4.0, 1.8), (0.0, -1.5, 1.5), 22)
for a, b, pose in ((0, 30, OP), (34, ON - 2, W), (ON, M1 + 20, CB), (M1 + 22, F['m4'] - 2, CL), (F['m4'], TOTAL - 1, HE)):
    camkey(a, pose)
    camkey(b, pose)

T.lines(EID, LINES)
T.blinks(moki, (44, 150, 300, 460, 590, 700, 840))
T.blinks(luma, (70, 190, 330, 500, 650, 790))
