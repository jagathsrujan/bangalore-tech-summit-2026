# QDD planetary actuator v1.0 - parametric build script for FreeCAD (run inside the GUI session)
# Axis = Z. Motor base sits on z = 0, output face is at the +Z end. Units: mm.
#
#   import runpy; ns = runpy.run_path(r".../build_actuator.py"); doc = ns['build']()
#
# Values marked MEASURE are not in the motor datasheet. Measure the real motor, edit P, re-run.
import math
import FreeCAD as App
import Part

V = App.Vector

# ----------------------------------------------------------------- parameters
P = dict(
    # gears (spur, 20 deg, profile shifted so the 12T sun is not undercut)
    m=1.0, alpha=20.0, Zs=12, Zp=24, Zr=60, n_planets=3,
    x_sun=0.4, x_planet=-0.4, x_ring=-0.4,
    sun_tip_r=7.2,            # truncated (full would be 7.4 and too pointed to print)
    ring_tip_r=28.9,          # shortened to avoid involute interference at the planet root
    backlash=0.08,            # removed from every tooth (mm of tooth thickness at pitch circle)
    face=12.0,
    # motor: 5010 outrunner, from the robu.in datasheet
    motor_d=50.0, motor_h=26.0, shaft_d=4.0,
    motor_holes=((9.5, 0), (-9.5, 0), (0, 8), (0, -8)),   # 19 mm and 16 mm base patterns
    bell_slot_r=(8.0, 12.5),  # MEASURE: sun flange is slotted for rotor bolt circles of 16-25 mm
    shaft_out=3.0,            # MEASURE: length of shaft sticking out of the motor base
    # bearings and pins
    b686=(6.0, 13.0, 5.0), b6807=(35.0, 47.0, 7.0),
    pin_d=6.0, pin_len=22.0,
    # housing
    od=78.0, tube_id=56.0, base_t=4.0, bolt_r=35.0,
    fit=0.05,                 # radial allowance added to bearing seats
    # encoder (AS5600 breakout 23 x 23 x 1.6, holes 16 x 16, magnet 6 x 2.5)
    enc_gap=1.5, enc_pcb=(23.0, 1.6), enc_chip_h=1.75, enc_hole=8.0, magnet=(6.0, 2.5),
)

m = P['m']; al = math.radians(P['alpha'])
a_c = m * (P['Zs'] + P['Zp']) / 2.0          # carrier radius = 18

# axial stack
Z_BELL = P['motor_h']                # 26.0  top of rotor bell
Z_FLG = Z_BELL + 5.0                 # 31.0  top of sun flange
Z_RP0 = Z_FLG + 1.0                  # 32.0  rear carrier plate bottom
Z_RP1 = Z_RP0 + 4.0                  # 36.0  rear carrier plate top
Z_G0 = Z_RP1 + 0.5                   # 36.5  planets bottom
Z_G1 = Z_G0 + P['face']              # 48.5  planets top
Z_FP0 = Z_G1 + 0.5                   # 49.0  front carrier plate bottom = housing front face
Z_FP1 = Z_FP0 + 7.0                  # 56.0
Z_BRG0 = Z_FP1 + 0.5                 # 56.5  6807 rear face
Z_BRG1 = Z_BRG0 + P['b6807'][2]      # 63.5
Z_COVER1 = Z_BRG1 + 1.5              # 65.0  front cover outer face
Z_OUT = Z_BRG1 + 6.0                 # 69.5  output flange face
Z_BASE = -P['base_t']                # -4.0  housing rear face

# encoder stack behind the motor (all negative z)
Z_CUP_TOP = -0.5
Z_MAG = Z_CUP_TOP - (P['shaft_out'] - 0.5) - 1.0 - P['magnet'][1]   # magnet outer face
Z_CHIP = Z_MAG - P['enc_gap']
Z_PCB_FRONT = Z_CHIP - P['enc_chip_h']
Z_PCB_BACK = Z_PCB_FRONT - P['enc_pcb'][1]
Z_CAP = Z_PCB_BACK - 4.5             # outer face of the rear cap


# ----------------------------------------------------------------- helpers
def inv(a):
    return math.tan(a) - a


def gear_outline(z, x, r_tip, r_root, ds, n=9, rot=0.0):
    """Closed polygon face of an external involute gear. ds = change in tooth thickness at pitch."""
    r = m * z / 2.0
    rb = r * math.cos(al)
    s = m * (math.pi / 2 + 2 * x * math.tan(al)) + ds

    def psi(R):
        return s / (2 * r) + inv(al) - inv(math.acos(min(1.0, rb / R)))

    r0 = max(rb, r_root)
    assert psi(r_tip) > 0, "tooth is pointed below the tip radius"
    assert psi(r0) < math.pi / z, "teeth overlap at the root"
    radii = [r0 + (r_tip - r0) * i / (n - 1) for i in range(n)]
    pts = []
    for k in range(z):
        th = rot + 2 * math.pi * k / z
        flank = [(R, psi(R)) for R in radii]
        if r_root < rb:
            flank = [(r_root, psi(rb))] + flank
        for R, p in flank:
            pts.append(V(R * math.cos(th - p), R * math.sin(th - p), 0))
        for R, p in reversed(flank):
            pts.append(V(R * math.cos(th + p), R * math.sin(th + p), 0))
        mid = th + math.pi / z
        pts.append(V(r_root * math.cos(mid), r_root * math.sin(mid), 0))
    pts.append(pts[0])
    return Part.Face(Part.Wire(Part.makePolygon(pts)))


def cyl(d, h, z0, x=0.0, y=0.0):
    return Part.makeCylinder(d / 2.0, h, V(x, y, z0), V(0, 0, 1))


def polar(r, n, a0=0.0):
    return [(r * math.cos(math.radians(a0) + 2 * math.pi * i / n),
             r * math.sin(math.radians(a0) + 2 * math.pi * i / n)) for i in range(n)]


def radial_slot(w, r1, r2, h, z0, ang_deg):
    """Stadium slot of width w whose centre runs from radius r1 to r2 along ang_deg."""
    s = cyl(w, h, z0, r1, 0).fuse(cyl(w, h, z0, r2, 0))
    s = s.fuse(Part.makeBox(r2 - r1, w, h, V(r1, -w / 2.0, z0)))
    s.rotate(V(0, 0, 0), V(0, 0, 1), ang_deg)
    return s


r_s = m * P['Zs'] / 2; r_p = m * P['Zp'] / 2; r_r = m * P['Zr'] / 2
SUN_ROOT = r_s - m * (1.25 - P['x_sun'])
PL_TIP = r_p + m * (1 + P['x_planet']); PL_ROOT = r_p - m * (1.25 - P['x_planet'])
RING_ROOT = r_r + m * (1.25 + P['x_ring'])
PLANET_POS = polar(a_c, P['n_planets'])
POST_POS = polar(20.0, P['n_planets'], 60.0)
FRONT_BOLTS = polar(P['bolt_r'], 6, 30.0)
REAR_BOLTS = polar(34.0, 4, 45.0)
HUB_BOLTS = polar(12.0, 4, 45.0)
OUT_BOLTS = polar(16.0, 6, 0.0)


# ----------------------------------------------------------------- printed parts
def make_sun():
    teeth = gear_outline(P['Zs'], P['x_sun'], P['sun_tip_r'], SUN_ROOT, -P['backlash'])
    z_t0 = Z_G0 - 0.5
    body = teeth.extrude(V(0, 0, Z_G1 - z_t0)); body.translate(V(0, 0, z_t0))
    s = cyl(34.0, Z_FLG - Z_BELL, Z_BELL).fuse(cyl(10.0, z_t0 - Z_FLG, Z_FLG)).fuse(body)
    r1, r2 = P['bell_slot_r']
    for k in range(4):
        a = 45.0 + 90.0 * k
        s = s.cut(radial_slot(3.4, r1, r2, 10, Z_BELL - 1, a))
        s = s.cut(radial_slot(6.2, r1, r2, 3.2, Z_FLG - 3.2, a))     # screw-head recess
    s = s.cut(cyl(7.0, 4.0, Z_BELL - 0.01))                          # clears a shaft stub / circlip
    return s.removeSplitter()


def make_planet(i):
    px, py = PLANET_POS[i]
    phi = math.atan2(py, px)
    f = gear_outline(P['Zp'], P['x_planet'], PL_TIP, PL_ROOT, -P['backlash'],
                     rot=phi + math.pi / P['Zp'])
    g = f.extrude(V(0, 0, P['face'])); g.translate(V(px, py, Z_G0))
    od = P['b686'][1] + 2 * P['fit']; w = P['b686'][2]
    g = g.cut(cyl(od, w, Z_G0, px, py)).cut(cyl(od, w, Z_G1 - w, px, py))
    g = g.cut(cyl(10.0, P['face'], Z_G0, px, py))            # leaves a 2 mm rib between outer races
    return g


def ring_cutter(z0, h):
    cutter = gear_outline(P['Zr'], P['x_ring'], RING_ROOT, P['ring_tip_r'], +P['backlash'],
                          rot=math.pi / P['Zr'])
    c = cutter.extrude(V(0, 0, h)); c.translate(V(0, 0, z0))
    return c


def make_housing():
    od = P['od']; bt = P['base_t']
    h = cyl(od, Z_FP0 + bt, Z_BASE)
    h = h.cut(cyl(P['tube_id'], Z_RP1, 0))                    # motor cavity
    h = h.cut(ring_cutter(Z_RP1, Z_FP0 - Z_RP1 + 0.01))
    h = h.cut(cyl(12.0, bt + 1, Z_BASE - 0.5))                # shaft / magnet cup
    for (x, y) in P['motor_holes']:
        h = h.cut(cyl(3.4, bt + 1, Z_BASE - 0.5, x, y))
        h = h.cut(cyl(6.2, 1.6, Z_BASE - 0.01, x, y))         # head recess
    h = h.cut(Part.makeBox(12, 6, bt + 1, V(-6, 20, Z_BASE - 0.5)))   # motor wire exit
    for (x, y) in FRONT_BOLTS:
        h = h.cut(cyl(4.2, 7.0, Z_FP0 - 7.0, x, y))           # M3 heat-set inserts, front
    for (x, y) in REAR_BOLTS:
        h = h.cut(cyl(4.2, 7.0, Z_BASE - 0.01, x, y))         # M3 heat-set inserts, rear
    return h.removeSplitter()


def make_carrier_rear():
    c = cyl(54.0, Z_RP1 - Z_RP0, Z_RP0)
    for (x, y) in PLANET_POS:
        c = c.fuse(cyl(8.5, Z_G0 - Z_RP1, Z_RP1, x, y))       # inner-race boss
    c = c.cut(cyl(17.0, 10, Z_RP0 - 1))                       # sun passes through
    for (x, y) in PLANET_POS:
        c = c.cut(cyl(P['pin_d'], 3.5, Z_G0 - 3.5, x, y))     # pin pocket, 1 mm floor
    for (x, y) in POST_POS:
        c = c.cut(cyl(3.4, 10, Z_RP0 - 1, x, y))
        c = c.cut(Part.makeCone(3.3, 1.7, 1.7, V(x, y, Z_RP0 - 0.01), V(0, 0, 1)))  # countersink
    return c.removeSplitter()


def make_carrier_front():
    c = cyl(54.0, Z_FP1 - Z_FP0, Z_FP0)
    c = c.fuse(cyl(39.0, Z_BRG0 - Z_FP1, Z_FP1))              # shoulder for the 6807 inner race
    hub_top = Z_BRG1 - 0.2
    c = c.fuse(cyl(P['b6807'][0], hub_top - Z_BRG0, Z_BRG0))
    for (x, y) in PLANET_POS:
        c = c.fuse(cyl(8.5, Z_FP0 - Z_G1, Z_G1, x, y))
    for (x, y) in POST_POS:
        c = c.fuse(cyl(10.0, Z_FP0 - Z_RP1, Z_RP1, x, y))     # spacer posts between planets
        c = c.cut(cyl(4.2, 6.0, Z_RP1 - 0.01, x, y))          # insert in post end
    pin_top = Z_G0 - 3.5 + P['pin_len']
    for (x, y) in PLANET_POS:
        c = c.cut(cyl(P['pin_d'], pin_top - Z_G1 + 0.3, Z_G1 - 0.01, x, y))
    for (x, y) in HUB_BOLTS:
        c = c.cut(cyl(4.2, 6.5, hub_top - 6.5, x, y))         # inserts for the output flange
    return c.removeSplitter()


def make_front_cover():
    c = cyl(P['od'], Z_COVER1 - Z_FP0, Z_FP0)
    c = c.cut(cyl(58.0, Z_FP1 + 0.3 - Z_FP0, Z_FP0 - 0.01))   # carrier plate cavity
    c = c.cut(cyl(P['b6807'][1] + 2 * P['fit'], Z_BRG1 - Z_FP1, Z_FP1))
    c = c.cut(cyl(43.0, 5, Z_BRG1 - 1))                       # retaining lip bore
    for (x, y) in FRONT_BOLTS:
        c = c.cut(cyl(3.4, 30, Z_FP0 - 1, x, y))
        c = c.cut(cyl(6.5, 6.0, Z_COVER1 - 6.0, x, y))        # M3 x 16 socket head
    return c.removeSplitter()


def make_output_flange():
    f = cyl(41.0, Z_OUT - Z_BRG1, Z_BRG1)
    for (x, y) in HUB_BOLTS:
        f = f.cut(cyl(3.4, 10, Z_BRG1 - 1, x, y))
        f = f.cut(cyl(6.2, 3.2, Z_OUT - 3.2, x, y))
    for (x, y) in OUT_BOLTS:
        f = f.cut(cyl(4.2, 5.5, Z_OUT - 5.5, x, y))           # M3 inserts, bolt circle 32 mm
    return f


def make_magnet_cup():
    top = Z_CUP_TOP
    c = cyl(9.0, top - Z_MAG, Z_MAG)
    c = c.cut(cyl(P['shaft_d'], P['shaft_out'] - 0.5 + 0.01, top - (P['shaft_out'] - 0.5)))
    c = c.cut(cyl(P['magnet'][0] + 0.1, P['magnet'][1] + 0.01, Z_MAG - 0.01))
    return c


def make_rear_cap():
    od = P['od']
    c = cyl(od, Z_BASE - Z_CAP, Z_CAP)
    c = c.cut(cyl(62.0, Z_BASE - Z_PCB_BACK, Z_PCB_BACK + 2.0))   # wiring cavity
    half = P['enc_pcb'][0] / 2 + 0.15
    c = c.cut(Part.makeBox(2 * half, 2 * half, 2.01, V(-half, -half, Z_PCB_BACK)))   # board pocket
    e = P['enc_hole']
    for (x, y) in ((e, e), (-e, e), (-e, -e), (e, -e)):
        c = c.cut(cyl(2.6, 4.0, Z_CAP + 0.8, x, y))           # M3 self-tap for the board screws
    c = c.cut(cyl(8.0, 5, Z_CAP - 1))                         # header pins / solder joints
    c = c.cut(Part.makeBox(14, 20, Z_BASE - Z_PCB_BACK - 2.0 + 0.01, V(-7, 22, Z_PCB_BACK + 2.0)))  # cable exit
    for (x, y) in REAR_BOLTS:
        c = c.cut(cyl(3.4, 40, Z_CAP - 1, x, y))
        c = c.cut(cyl(6.5, 3.2, Z_CAP - 0.01, x, y))          # M3 socket head
    return c.removeSplitter()


def make_test_arm():
    t = 5.0
    a = cyl(41.0, t, Z_OUT).fuse(Part.makeBox(100.0, 14.0, t, V(0, -7.0, Z_OUT)))
    a = a.fuse(cyl(14.0, t, Z_OUT, 100.0, 0))
    for (x, y) in OUT_BOLTS:
        a = a.cut(cyl(3.4, t + 2, Z_OUT - 1, x, y))
    a = a.cut(cyl(4.2, t + 2, Z_OUT - 1, 100.0, 0))            # load hole, 100 mm from the axis
    a = a.cut(cyl(4.2, t + 2, Z_OUT - 1, 50.0, 0))             # load hole, 50 mm
    a = a.cut(cyl(14.0, t + 2, Z_OUT - 1))                     # access to the flange centre
    return a.removeSplitter()


STAND_Z = (6.0, 30.0)        # clamps the plain part of the housing


def make_stand(upper):
    z0, z1 = STAND_Z; d = z1 - z0
    bore = cyl(P['od'] + 0.4, d + 2, z0 - 1)
    if not upper:
        s = Part.makeBox(100, 49.8, d, V(-50, -50, z0))
        s = s.fuse(Part.makeBox(140, 6, d, V(-70, -50, z0)))   # feet
        s = s.cut(bore)
        for x in (-44.5, 44.5):
            s = s.cut(Part.makeCylinder(2.1, 7.0, V(x, -7.2, (z0 + z1) / 2), V(0, 1, 0)))   # insert
        for x in (-62.0, 62.0):
            s = s.cut(Part.makeCylinder(2.75, 10, V(x, -52, (z0 + z1) / 2), V(0, 1, 0)))    # table bolt
    else:
        s = cyl(90.0, d, z0).fuse(Part.makeBox(100, 16, d, V(-50, 0.2, z0)))
        s = s.common(Part.makeBox(200, 100, d, V(-100, 0.2, z0)))
        s = s.cut(bore)
        for x in (-44.5, 44.5):
            s = s.cut(Part.makeCylinder(1.7, 30, V(x, -1, (z0 + z1) / 2), V(0, 1, 0)))
    return s.removeSplitter()


def bearing(dims, z0, x=0.0, y=0.0):
    i, o, w = dims
    return cyl(o, w, z0, x, y).cut(cyl(i, w, z0, x, y))


def make_test_ring():
    """13 mm slice of the ring gear for a fit test before printing the full housing."""
    r = cyl(P['od'] - 8.0, Z_FP0 - Z_RP1, Z_RP1)
    return r.cut(ring_cutter(Z_RP1 - 0.5, Z_FP0 - Z_RP1 + 1.0))


# ----------------------------------------------------------------- build
PRINTED = [  # name, qty
    ("Housing_RingGear", 1), ("Sun_Gear", 1), ("Planet", 3), ("Carrier_Rear", 1),
    ("Carrier_Front_Output", 1), ("Front_Cover", 1), ("Output_Flange", 1),
    ("Rear_Cap_Encoder", 1), ("Magnet_Cup", 1), ("Test_Arm", 1),
    ("Stand_Lower", 1), ("Stand_Upper", 1),
]


def build(doc_name="QDD_Actuator"):
    if doc_name in App.listDocuments():
        App.closeDocument(doc_name)
    doc = App.newDocument(doc_name)

    def add(name, shape, color, group, transp=0):
        o = doc.addObject("Part::Feature", name)
        o.Shape = shape
        group.addObject(o)
        try:
            o.ViewObject.ShapeColor = color
            o.ViewObject.Transparency = transp
        except Exception:
            pass
        return o

    gp = doc.addObject("App::DocumentObjectGroup", "PRINTED")
    gh = doc.addObject("App::DocumentObjectGroup", "BOUGHT")
    ga = doc.addObject("App::DocumentObjectGroup", "BENCH_ACCESSORIES")

    dark = (0.20, 0.22, 0.26); light = (0.80, 0.80, 0.82)
    add("Housing_RingGear", make_housing(), dark, gp, 60)
    add("Sun_Gear", make_sun(), (0.95, 0.60, 0.10), gp)
    for i in range(P['n_planets']):
        add("Planet_%d" % (i + 1), make_planet(i), (0.15, 0.55, 0.90), gp)
    add("Carrier_Rear", make_carrier_rear(), light, gp)
    add("Carrier_Front_Output", make_carrier_front(), light, gp)
    add("Front_Cover", make_front_cover(), dark, gp, 60)
    add("Output_Flange", make_output_flange(), (0.90, 0.25, 0.20), gp)
    add("Rear_Cap_Encoder", make_rear_cap(), dark, gp, 60)
    add("Magnet_Cup", make_magnet_cup(), (0.95, 0.60, 0.10), gp)

    add("Test_Arm", make_test_arm(), (0.90, 0.25, 0.20), ga)
    add("Stand_Lower", make_stand(False), (0.45, 0.47, 0.50), ga)
    add("Stand_Upper", make_stand(True), (0.45, 0.47, 0.50), ga)

    motor = cyl(P['motor_d'], P['motor_h'], 0).fuse(cyl(P['shaft_d'], P['shaft_out'], -P['shaft_out']))
    add("Motor_5010_REF", motor, (0.55, 0.55, 0.58), gh)
    for i, (x, y) in enumerate(PLANET_POS):
        add("Pin_6x22_%d" % (i + 1), cyl(P['pin_d'], P['pin_len'], Z_G0 - 3.5, x, y), (0.7, 0.7, 0.7), gh)
        add("Brg_686_%da" % (i + 1), bearing(P['b686'], Z_G0, x, y), (0.85, 0.85, 0.3), gh)
        add("Brg_686_%db" % (i + 1), bearing(P['b686'], Z_G1 - P['b686'][2], x, y), (0.85, 0.85, 0.3), gh)
    add("Brg_6807", bearing(P['b6807'], Z_BRG0), (0.85, 0.85, 0.3), gh)
    add("Magnet_6x2p5", cyl(P['magnet'][0], P['magnet'][1], Z_MAG), (0.9, 0.1, 0.1), gh)
    half = P['enc_pcb'][0] / 2
    pcb = Part.makeBox(2 * half, 2 * half, P['enc_pcb'][1], V(-half, -half, Z_PCB_BACK))
    pcb = pcb.fuse(Part.makeBox(4.9, 3.9, P['enc_chip_h'], V(-2.45, -1.95, Z_PCB_FRONT)))
    add("AS5600_Board_REF", pcb, (0.1, 0.5, 0.2), gh)
    doc.recompute()
    return doc
