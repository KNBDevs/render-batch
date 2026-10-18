from stage import *
from episodes.hw26_09_telarana_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props.costumes import dress, flat
from props import halloween as HW
from episodes.hw_look import autumn
EID = 'hw26_09_telarana'
Z0 = 0.08
autumn(dusk=True)
auto_dress(EID, ENV)

W0 = ((0.05, -6.0, 1.5), (0.05, -1.0, 0.85), 30)
WC = ((0.45, -3.3, 0.95), (0.45, -1.0, 0.8), 32)
camkey(0, W0)
camkey(168, W0)
camkey(188, WC)
camkey(470, WC)
camkey(490, W0)
camkey(TOTAL - 1, W0)

FP = Vector((0.45, -1.0, Z0))
FS = 0.85
spawn('web_frame', 0, 909, 'autumn', tuple(FP), FS, 0)
BAR = FP + Vector((0, 0, FS * 1.3))
HUB = FP + Vector((0, 0, FS * 0.72))
web, parts = HW.web('web', tuple(HUB), r=0.43, spokes=8, rings=5)
web.location.y -= 0.005
HW.reveal(parts, 262, 460)

SP = 0.46
s = SP / 0.8
seda = HW.spider('Seda', span=SP)
sr = seda['root']
legs = seda['legs']
TOPP = BAR + Vector((0, 0, 0.03))
K(sr, 'location', 0, tuple(TOPP))
K(sr, 'location', 176, tuple(TOPP))
K(sr, 'rotation_euler', 0, (0, 0, 0))
for f, a in ((120, 0), (126, 16), (134, -16), (142, 16), (150, 0)):
    K(sr, 'rotation_euler', f, (0, 0, math.radians(a)))
K(sr, 'rotation_euler', 176, (0, 0, 0))
OFF = Vector((0, 0.16 * s - 0.04, 0))
HANG = BAR + OFF + Vector((0, 0, -0.3 * s))
K(sr, 'location', 186, tuple(BAR + OFF + Vector((0, 0, 0.02))))
K(sr, 'rotation_euler', 186, (math.radians(90), 0, 0))
K(sr, 'location', 198, tuple(HANG))
K(sr, 'location', 252, tuple(HUB + OFF))
K(sr, 'rotation_euler', 252, (math.radians(90), 0, 0))
for k, f in enumerate(range(270, 460, 38)):
    K(sr, 'rotation_euler', f, (math.radians(90), math.radians(12 if k % 2 else -12), 0))
K(sr, 'rotation_euler', 470, (math.radians(90), 0, 0))
K(sr, 'location', 470, tuple(HUB + OFF))
for k, f in enumerate(range(262, 460, 10)):
    lg = legs[f"leg_{'L' if k % 2 else 'R'}_{1 + (k // 2) % 4}"]
    r0 = tuple(lg.rotation_euler)
    K(lg, 'rotation_euler', f, r0)
    K(lg, 'rotation_euler', f + 5, (r0[0], r0[1] + math.radians(14), r0[2]))
    K(lg, 'rotation_euler', f + 10, r0)

bpy.context.scene.frame_set(300)
bpy.context.view_layer.update()
spw = seda['spinneret'].matrix_world.translation.copy()
silk = HW._m('silk', (0.78, 0.8, 0.83), rough=0.5, emit=0.15, coat=0.0)
drag = C.tube('dragline', [tuple(BAR + Vector((0, -0.005, 0))), tuple(Vector((BAR.x, BAR.y - 0.005, spw.z)))], 0.004, silk, None)
drag.data.bevel_factor_mapping_end = 'SPLINE'
for f, v in ((0, 0.0), (192, 0.0), (252, 1.0)):
    drag.data.bevel_factor_end = v
    drag.data.keyframe_insert('bevel_factor_end', frame=f)

wl = legs['leg_L_1']
r0 = tuple(wl.rotation_euler)
for f, d in ((756, 0), (762, 40), (770, 25), (778, 40), (786, 25), (794, 0)):
    K(wl, 'rotation_euler', f, (r0[0], r0[1] + math.radians(d), r0[2]))

moki = make('moki', 1.25)
dress(moki, 'moki', COSTUME, 1)
MP = Vector((-0.75, -0.8, Z0))
MP2 = Vector((-0.5, -0.85, Z0))
T.place(moki, 0, MP)
T.turn(moki, 0, 30)
hop_to(moki, 482, MP, MP2, 12, apex=0.2)

sheet_m = M((0.95, 0.92, 0.85), rough=0.55, coat=0.3)
band_m = M((0.5, 0.3, 0.52), rough=0.45, coat=0.5)
sheet = C.empty('sheet', None, (0, 0, 0))
sw, sh = 0.26, 0.2
flat('sheet_body', [(-sw, -sh), (sw, -sh), (sw, sh), (-sw, sh)], 0.03, sheet_m, sheet, bevel=0.012)
for k, z in enumerate((-sh * 0.55, sh * 0.55)):
    flat(f'sheet_band{k}', [(-sw * 0.98, z - 0.022), (sw * 0.98, z - 0.022), (sw * 0.98, z + 0.022), (-sw * 0.98, z + 0.022)], 0.036, band_m, sheet, bevel=0.006)


def hold(p, f, dx=0.0, dz=0.0, rz=30):
    K(sheet, 'location', f, tuple(p + Vector((0.32 + dx, -0.3, 0.5 + dz))))
    K(sheet, 'rotation_euler', f, (0, 0, math.radians(rz)))


hold(MP, 0)
hold(MP, 36)
hold(MP, 50, 0.18, 0.06)
hold(MP, 110, 0.18, 0.06)
hold(MP, 124)
hold(MP, 482)
hold(MP2, 494)
hold(MP2, 512, 0.25, 0.3, 10)
hold(MP2, 650, 0.25, 0.3, 10)
hold(MP2, 666)
for side in ('L', 'R'):
    T.arm(moki, side, 0, fwd=-70, out=25)
    T.arm(moki, side, 666, fwd=-70, out=25)
    T.arm(moki, side, 680, fwd=-40, out=60)
    T.rest_arm(moki, side, 700)

TBL = Vector((-1.25, -0.2, Z0))
spawn('low_table', 1, 911, 'autumn', tuple(TBL), 0.62, 0)
TOPZ = TBL.z + 0.62 * 0.62 + 0.03
T.turn(moki, 672, 30)
T.turn(moki, 680, -45)
K(sheet, 'location', 680, tuple(MP2 + Vector((0.32, -0.3, 0.5))))
K(sheet, 'rotation_euler', 680, (0, 0, math.radians(30)))
K(sheet, 'location', 690, tuple(Vector((TBL.x + 0.25, TBL.y - 0.25, TOPZ + 0.3))))
K(sheet, 'location', 700, tuple(Vector((TBL.x, TBL.y, TOPZ))))
K(sheet, 'rotation_euler', 700, (math.radians(90), 0, 0))
T.turn(moki, 740, -45)
T.turn(moki, 750, 25)
for f, z in ((704, 0.0), (708, 0.04), (712, 0.0)):
    K(sheet, 'location', f, tuple(Vector((TBL.x, TBL.y, TOPZ + z))))
gesture(moki, 'breathe', 300)
C.wave(moki, 'R', 790, cycles=2, period=8)

lab = HW.card('lab_hl', 'hilos de seda', _font(), (FP.x, -1.4, 1.62), w=0.82, h=0.18, bg=(0.4, 0.27, 0.45), ink=(1.0, 0.9, 0.7), rot=(math.radians(-6), 0, 0))
T.pop_in(lab, 520, 1.0, 10)
T.pop_out(lab, 660, 1.0, 8)

T.lines(EID, LINES)
T.blinks(moki, (20, 160, 300, 430, 560, 690, 810))
