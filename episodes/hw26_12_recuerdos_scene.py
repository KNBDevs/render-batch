from stage import *
from episodes.hw26_12_recuerdos_plan import *
import ep_tools as T
from props.lib import spawn, auto_dress, M, _font
from props import halloween as HW
EID = 'hw26_12_recuerdos'
Z0 = 0.08
auto_dress(EID, ENV)

TB = Vector((0, -0.85, Z0))
TS = 0.9
spawn('low_table', 1, 1201, 'pastel', tuple(TB), TS, 0)
TZ = TB.z + 0.62 * TS
TILT = 55
SS = 1.35
st = spawn('book_stand', 0, 1202, 'pastel', (0, TB.y - 0.08, TZ), SS, 0, tilt=TILT)
t = math.radians(TILT)
AW, AH = 0.74, 0.5
apos = Vector((0, TB.y - 0.08 + SS * (0.05 + 0.12 * math.cos(t) - 0.02), TZ + SS * (0.06 + 0.12 * math.sin(t) + 0.015)))
alb = HW.album('album', tuple(apos - Vector((0, 0.0, 0.0))), w=AW, h=AH, rot=(t, 0, 0), cover=(0.45, 0.3, 0.5))
K(alb['lid'], 'rotation_euler', 0, (0, math.radians(180), 0))
ar = alb['root']
fr = HW.photo_frame('foto', (AW * 0.2, -0.02, 0.058), h=0.22, parent=ar, rot=(math.radians(-90), 0, 0))
paper = M((0.99, 0.97, 0.92), rough=0.6, coat=0.1)
dr = C.empty('dibujo', ar, (-AW * 0.22, 0.0, 0.058))
C.rounded_box('dib_paper', (0, 0, 0), (0.22, 0.28, 0.004), 0.002, paper, dr)
C.sphere('dib_sun', (0.05, 0.08, 0.004), (0.03, 0.03, 0.003), M((1.0, 0.75, 0.2), rough=0.5), dr, 20)
kite = C.empty('dib_kite', dr, (-0.03, 0.0, 0.004), (0, 0, math.radians(20)))
C.sphere('dib_kite_m', (0, 0, 0), (0.035, 0.05, 0.003), M((0.9, 0.35, 0.45), rough=0.5), kite, 4)
C.tube('dib_tail', [(-0.03, -0.05, 0.004), (-0.01, -0.08, 0.004), (-0.04, -0.11, 0.004)], 0.003, M((0.3, 0.45, 0.75), rough=0.5), dr)
C.rounded_box('dib_grass', (0, -0.115, 0.004), (0.2, 0.03, 0.003), 0.002, M((0.45, 0.72, 0.4), rough=0.6), dr)

card = HW.card('tarjeta', 'con cariño', _font(), (0.24, TB.y - 0.32, TZ + 0.1), w=0.36, h=0.14, bg=(0.97, 0.88, 0.9), ink=(0.4, 0.25, 0.42), rot=(math.radians(-70), 0, math.radians(-12)))
T.pop_in(card, 200, 1.0, 12)

bq = HW.bouquet('ramo', (-0.33, TB.y + 0.08, TZ), h=0.26, cols=((0.95, 0.92, 0.88), (0.95, 0.75, 0.8), (0.98, 0.85, 0.4)))
T.pop_in(bq, 520, 1.0, 14)
mb = spawn('memory_box', 0, 1203, 'pastel', (0.3, TB.y + 0.1, TZ), 0.9, -10)
T.pop_in(mb, 540, 0.9, 12)
hinge = next(o for o in mb.children_recursive if o.name.startswith('mlid_hinge'))
K(hinge, 'rotation_euler', 0, (0, 0, 0))
K(hinge, 'rotation_euler', 560, (0, 0, 0))
K(hinge, 'rotation_euler', 578, (math.radians(-100), 0, 0))
note = C.empty('nota', mb, (0, 0, 0.14))
C.rounded_box('nota_m', (0, 0, 0.0), (0.16, 0.004, 0.12), 0.002, paper, note)
C.sphere('nota_h', (0, -0.004, 0.0), (0.025, 0.003, 0.022), M((0.9, 0.35, 0.45), rough=0.5), note, 16)
K(note, 'location', 0, (0, 0, 0.0))
K(note, 'location', 566, (0, 0, 0.0))
K(note, 'location', 584, (0, 0, 0.14))

luma = make('luma', 1.15)
ruki = make('ruki', 1.2)
LP = Vector((-1.05, -0.72, Z0))
RP = Vector((1.05, -0.75, Z0))
T.place(luma, 0, LP)
T.place(ruki, 0, RP)
T.turn(luma, 0, 35)
T.turn(ruki, 0, -30)
for f, a in ((10, 35), (18, 25), (26, 35)):
    K(luma['sq'], 'rotation_euler', f, (0, math.radians(a - 35), 0))
T.arm(ruki, 'L', 210, 0, None)
T.arm(ruki, 'L', 222, fwd=-50, out=50)
T.arm(ruki, 'L', 300, fwd=-50, out=50)
T.arm(ruki, 'L', 320, fwd=-35, out=35)
T.arm(ruki, 'L', 400, fwd=-35, out=35)
T.rest_arm(ruki, 'L', 414)
gesture(ruki, 'breathe', 440)
gesture(luma, 'breathe', 300)

lamp = HW.led_light('luz', (0, 0, 0), h=0.12)
LH = LP + Vector((0.32, -0.25, 0.5))
LT = Vector((-0.15, TB.y - 0.32, TZ + 0.42))
K(lamp, 'scale', 0, (0, 0, 0))
K(lamp, 'scale', 680, (0, 0, 0))
K(lamp, 'scale', 690, (1, 1, 1))
K(lamp, 'location', 680, tuple(LH))
K(lamp, 'location', 706, tuple(LT))
K(lamp, 'location', 830, tuple(LT))
for side in ('L', 'R'):
    T.arm(luma, side, 680, 0, None)
    T.arm(luma, side, 692, fwd=-75, out=30)
T.turn(luma, 690, 45)
hop_to(luma, 690, LP, LP + Vector((0.18, 0, 0)), 10, apex=0.06)
ld = bpy.data.lights.new('page_glow', 'POINT')
ld.color = (1.0, 0.82, 0.55)
ld.shadow_soft_size = 0.3
lo = bpy.data.objects.new('page_glow', ld)
bpy.context.scene.collection.objects.link(lo)
lo.location = tuple(apos + Vector((0, -0.35, 0.25)))
for f, e in ((0, 0.0), (696, 0.0), (726, 25.0), (TOTAL - 1, 25.0)):
    ld.energy = e
    ld.keyframe_insert('energy', frame=f)
T.turn(ruki, 700, -30)
T.turn(ruki, 712, -42)
for f, a in ((712, 0), (724, 8), (800, 8), (812, 0)):
    K(ruki['sq'], 'rotation_euler', f, (0, math.radians(-a), 0))

W0 = ((0, -6.3, 1.75), (0, -1.0, 0.95), 32)
WC = ((0, -4.7, 1.45), (0, -0.85, 0.85), 26)
camkey(0, W0)
camkey(150, W0)
WA = ((0, -2.25, 1.05), tuple(apos), 28)
camkey(170, WA)
camkey(480, WA)
camkey(500, WC)
camkey(TOTAL - 1, WC)

T.lines(EID, LINES)
T.blinks(luma, (60, 190, 320, 450, 580, 720, 800))
T.blinks(ruki, (90, 230, 360, 490, 620, 760))
