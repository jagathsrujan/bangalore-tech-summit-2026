# Bench setups for the two existing gearboxes: stand + test arm + AS5600 encoder.
# ENCODER = "rear"   : magnet on the shaft end visible through the hole in the back of the NEMA 17,
#                      sensor in the existing press-fit holder (this is how the gearboxes are built).
# ENCODER = "output" : magnet in the centre of the test arm, sensor on a post in front of the output.
# Run inside the FreeCAD GUI session:
#   import runpy; ns = runpy.run_path(r".../build_bench.py"); ns['build_all']()
# Parts are modelled in a canonical frame (gearbox axis = +Z towards the output, table = -Y)
# and then placed onto each imported STEP assembly.
import math, os
import FreeCAD as App
import Part
import Import

V = App.Vector
ROOT = r"E:\bangalore tech summit"

ENCODER = "rear"
ENC_STEP = os.path.join(ROOT, "3d-printable-planetary-gearbox", "cad", "encoder_mount_assembly.step")

SETUPS = {
    "Planetary": dict(
        step=os.path.join(ROOT, "Planetary Gearbox - Two-stage 16to1 ratio.step"),
        # canonical X, Y, Z expressed in the STEP's coordinates, and the canonical origin
        frame=(V(1, 0, 0), V(0, 0, 1), V(0, -1, 0)), origin=V(0, 0, 0),
        od=85.0, clamp=(16.0, 40.0),            # housing diameter, clamped length along the axis
        out_z=60.0,                             # output face
        out_holes=[(-6.81, 1.63), (-1.63, -6.81), (1.63, 6.81), (6.81, -1.63)],  # 4 x M3, BCD 14
        hub_d=30.0, centre_hole=0.0,
        housing_labels=("Ring gear",),
        # rear encoder: X, Y, Z of the encoder-mount model in STEP coordinates, and the motor rear-face centre
        enc_frame=(V(-1, 0, 0), V(0, 0, -1), V(0, -1, 0)), enc_origin=V(0, 63.99, 0),
    ),
    "Cycloidal": dict(
        step=os.path.join(ROOT, "cycloidal-drive-print-ready", "Cycloidal Drive - 3D Printable DIY.STEP"),
        frame=(V(0, 1, 0), V(0, 0, 1), V(1, 0, 0)), origin=V(0, 0, 20.5),
        od=115.0, clamp=(88.0, 112.0),
        out_z=129.03,
        out_holes=[(-1.67, 12.89), (-12.0, 5.0), (-10.33, -7.89), (1.67, -12.89), (12.0, -5.0), (10.33, 7.89)],  # 6 x M3, BCD 26
        hub_d=38.0, centre_hole=0.0,
        housing_labels=("Roller pins housing",),
        enc_frame=(V(0, -1, 0), V(0, 0, -1), V(1, 0, 0)), enc_origin=V(20.03, 0, 20.5),
    ),
}

GAP = 0.2            # radial clearance between clamp and housing
UNDER = 11.0         # material under the housing / ear width
DEPTH = 24.0
ARM_T = 5.0
MAGNET = (6.0, 2.5)      # diametric magnet, pressed into the centre of the arm hub
ENC_GAP = 1.5           # magnet face to AS5600 chip face
CHIP_H = 1.75; PCB = (23.0, 1.6); PCB_HOLE = 8.0
POST_T = 8.0


def cyl(d, h, z0, x=0.0, y=0.0):
    return Part.makeCylinder(d / 2.0, h, V(x, y, z0), V(0, 0, 1))


def placement(frame, origin):
    x, y, z = frame
    m = App.Matrix(x.x, y.x, z.x, origin.x,
                   x.y, y.y, z.y, origin.y,
                   x.z, y.z, z.z, origin.z,
                   0, 0, 0, 1)
    return App.Placement(m)


def make_stand(od, z0, upper):
    r = od / 2.0; w = r + UNDER; ex = r + UNDER / 2.0
    bore = cyl(od + 2 * GAP, DEPTH + 2, z0 - 1)
    zc = z0 + DEPTH / 2.0
    if not upper:
        s = Part.makeBox(2 * w, w - 0.2, DEPTH, V(-w, -w, z0))
        s = s.fuse(Part.makeBox(2 * w + 40, 6, DEPTH, V(-w - 20, -w, z0)))      # feet
        s = s.cut(bore)
        for x in (-ex, ex):
            s = s.cut(Part.makeCylinder(2.1, 7.0, V(x, -7.2, zc), V(0, 1, 0)))     # M3 insert
        for x in (-w - 12, w + 12):
            s = s.cut(Part.makeCylinder(2.75, 10, V(x, -w - 2, zc), V(0, 1, 0)))   # table bolt
        if ENCODER == "output":
            for x in (-18.0, 18.0):
                s = s.cut(cyl(4.2, 7.0, z0 + DEPTH - 7.0, x, -w + 9.0))           # M3 insert for the encoder post
    else:
        s = cyl(od + 12.0, DEPTH, z0).fuse(Part.makeBox(2 * w, 16, DEPTH, V(-w, 0.2, z0)))
        s = s.common(Part.makeBox(4 * w, 2 * w, DEPTH, V(-2 * w, 0.2, z0)))
        s = s.cut(bore)
        for x in (-ex, ex):
            s = s.cut(Part.makeCylinder(1.7, 30, V(x, -1, zc), V(0, 1, 0)))
    return s.removeSplitter()


def make_arm(cfg):
    t = ARM_T; z = cfg['out_z']
    a = cyl(cfg['hub_d'], t, z).fuse(Part.makeBox(100.0, 14.0, t, V(0, -7.0, z))).fuse(cyl(14.0, t, z, 100.0, 0))
    for (x, y) in cfg['out_holes']:
        a = a.cut(cyl(3.4, t + 2, z - 1, x, y))
        a = a.cut(cyl(6.2, 2.0, z + t - 2.0, x, y))        # head recess
    a = a.cut(cyl(4.2, t + 2, z - 1, 100.0, 0))            # load hole, 100 mm from the axis
    a = a.cut(cyl(4.2, t + 2, z - 1, 50.0, 0))             # load hole, 50 mm
    if ENCODER == "output":
        a = a.cut(cyl(MAGNET[0] + 0.1, MAGNET[1] + 0.1, z + t - MAGNET[1] - 0.1))   # magnet pocket on the axis
    return a.removeSplitter()


def enc_z(cfg):
    """Axial positions of the encoder stack in front of the arm."""
    z_mag = cfg['out_z'] + ARM_T
    z_chip = z_mag + ENC_GAP
    z_pcb0 = z_chip + CHIP_H
    z_pcb1 = z_pcb0 + PCB[1]
    return z_mag, z_chip, z_pcb0, z_pcb1


def make_encoder_post(cfg):
    """Bolts to the front of Stand_Lower and holds the AS5600 board on the output axis."""
    w = cfg['od'] / 2.0 + UNDER
    zc1 = cfg['clamp'][0] + DEPTH                     # front face of the stand
    z_mag, z_chip, z_pcb0, z_pcb1 = enc_z(cfg)
    zp0 = z_pcb1 - 1.0; zp1 = zp0 + POST_T            # board sits in a 1 mm deep pocket
    p = Part.makeBox(52, 16, 5, V(-26, -w, zc1))      # tab against the stand
    p = p.fuse(Part.makeBox(30, 6, zp1 + 25 - zc1, V(-15, -w, zc1)))          # bar along the table
    p = p.fuse(Part.makeBox(30, w + 18, POST_T, V(-15, -w, zp0)))             # post up to the axis
    rib = Part.makePolygon([V(0, -w + 6, zp1), V(0, -w + 6, zp1 + 25), V(0, -w + 46, zp1), V(0, -w + 6, zp1)])
    rib = Part.Face(Part.Wire(rib)).extrude(V(5, 0, 0)); rib.translate(V(-2.5, 0, 0))
    p = p.fuse(rib)
    p = p.cut(cyl(cfg['od'] + 2.0, cfg['out_z'] - 0.5 - (zc1 - 1), zc1 - 1))   # clear the housing in front of the stand
    for x in (-18.0, 18.0):
        p = p.cut(cyl(3.4, 7, zc1 - 1, x, -w + 9.0))
    half = PCB[0] / 2 + 0.15
    p = p.cut(Part.makeBox(2 * half, 2 * half, 1.01, V(-half, -half, zp0 - 0.01)))    # board pocket
    for sx in (-1, 1):
        for sy in (-1, 1):
            p = p.cut(cyl(2.6, 6.0, zp0, sx * PCB_HOLE, sy * PCB_HOLE))            # M3 self-tap
    p = p.cut(Part.makeBox(12, 12, POST_T + 2, V(-6, -6, zp0 - 1)))                # header pins / wiring window
    return p.removeSplitter()


def make_encoder_refs(cfg):
    z_mag, z_chip, z_pcb0, z_pcb1 = enc_z(cfg)
    h = PCB[0] / 2
    board = Part.makeBox(2 * h, 2 * h, PCB[1], V(-h, -h, z_pcb0)).fuse(Part.makeBox(4.9, 3.9, CHIP_H, V(-2.45, -1.95, z_chip)))
    magnet = cyl(MAGNET[0], MAGNET[1], z_mag - MAGNET[1])
    return board, magnet


def encoder_solids():
    """Holder, sensor board and magnet from the existing encoder-mount design (motor solids dropped)."""
    shape = Part.read(ENC_STEP)
    keep = [s for s in shape.Solids if s.BoundBox.ZMax < 10.0]     # motor body/boss/shaft reach z > 10
    keep.sort(key=lambda s: -s.Volume)
    holder = keep[0]
    magnet = [s for s in keep[1:] if abs(s.BoundBox.XLength - 6.0) < 0.3 and abs(s.BoundBox.ZLength - 2.5) < 0.3]
    rest = [s for s in keep[1:] if not any(s.isSame(mg) for mg in magnet)]
    return holder, rest, (Part.makeCompound(magnet) if magnet else None)


def build(name):
    cfg = SETUPS[name]
    doc_name = name + "_Bench"
    if doc_name in App.listDocuments():
        App.closeDocument(doc_name)
    doc = App.newDocument(doc_name)
    Import.insert(cfg['step'], doc.Name)
    doc.recompute()
    grp = doc.addObject("App::DocumentObjectGroup", "BENCH_SETUP")
    pl = placement(cfg['frame'], cfg['origin'])

    def add(label, shape, color, p):
        o = doc.addObject("Part::Feature", label)
        s = shape.copy(); s.Placement = p
        o.Shape = s
        grp.addObject(o)
        try:
            o.ViewObject.ShapeColor = color
        except Exception:
            pass
        return o

    z0 = cfg['clamp'][0]
    add("Stand_Lower", make_stand(cfg['od'], z0, False), (0.45, 0.47, 0.50), pl)
    add("Stand_Upper", make_stand(cfg['od'], z0, True), (0.45, 0.47, 0.50), pl)
    add("Test_Arm", make_arm(cfg), (0.90, 0.25, 0.20), pl)
    if ENCODER == "output":
        add("Encoder_Post", make_encoder_post(cfg), (0.95, 0.60, 0.10), pl)
        board, magnet = make_encoder_refs(cfg)
        add("AS5600_Board", board, (0.10, 0.50, 0.20), pl)
        add("Magnet_6x2p5", magnet, (0.90, 0.10, 0.10), pl)
    else:
        epl = placement(cfg['enc_frame'], cfg['enc_origin'])
        holder, rest, magnet = encoder_solids()
        add("Encoder_Holder", holder, (0.95, 0.60, 0.10), epl)
        # the reference motor's rear boss / shaft stub are not part of the sensor: keep board-side solids only
        board = [s for s in rest if s.BoundBox.ZMax < 0.0]      # chip face is at z = -0.5 since holder r3
        if board: add("AS5600_Board", Part.makeCompound(board), (0.10, 0.50, 0.20), epl)
        if magnet: add("Magnet_6x2p5", magnet, (0.90, 0.10, 0.10), epl)
    doc.recompute()
    return doc


def build_all():
    return {n: build(n) for n in SETUPS}
