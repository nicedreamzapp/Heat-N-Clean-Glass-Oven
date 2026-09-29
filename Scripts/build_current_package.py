"""Build FAB_PACKAGE_2026-09-28 from the approved design (see CURRENT.md).

Sources: cad-source/*.step are the Sept 9 solids for parts that were approved as-is or only get holes/patches here.
Every change made on 2026-09-28 is applied below, in code, so the package can be rebuilt exactly.
Run:  .venv-cad/bin/python Scripts/build_current_package.py
"""
import math, os, shutil
from build123d import *
import trimesh

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "cad-source")
OUT = os.path.join(ROOT, "FAB_PACKAGE_2026-09-28")
T = 0.8                                   # inside parts
BOLT = [52.4 + 60 * k for k in range(6)]  # one bolt clocking for every ring
WIRE = [(183.0, 4.0), (188.0, 4.0), (315.0, 3.2)]   # heater leads Ø8, thermocouple Ø6.4, at r 58
R_WIRE = 58.0

def solid(x): return x if not isinstance(x, ShapeList) else Compound(children=list(x))
def ring(ri, ro, z0, z1):
    return Pos(0, 0, z0) * (Cylinder(ro, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))
                            - Cylinder(ri, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
def vhole(ang, r, rad, z0, z1):
    a = math.radians(ang)
    return Pos(r * math.cos(a), r * math.sin(a), z0) * Cylinder(rad, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))
def rhole(ang, r_mid, z, rad=3.3, length=8):
    return Rot(0, 0, ang) * Pos(r_mid, 0, z) * Rot(0, 90, 0) * Cylinder(rad, length)
def sector(a0, a1, z0, z1, ri=70.85, ro=71.65):
    w = 2 * (ro + 1) * math.sin(math.radians((a1 - a0) / 2))
    return solid(ring(ri, ro, z0, z1) & (Rot(0, 0, (a0 + a1) / 2) * Pos((ri + ro) / 2, 0, (z0 + z1) / 2) * Box(ro - ri + 2, w, z1 - z0)))
def src(name): return solid(import_step(os.path.join(SRC, name + ".step")))

CAP_T = 1.2                  # top cap sheet; the lid now sits on it, so every lid part is raised by this much
SLOTS = [6.5, 77.1, 147.7, 218.3]   # glass slots (hnc_params)
LIFT = Pos(0, 0, CAP_T)

parts = {}
# 01 inner wall: wires no longer pass the wall -> close the wire slot, the TC hole, and their mirror copies
parts["01_Inner_Wall_Tube"] = solid(src("01_Inner_Wall_Tube") + sector(179, 187, 11.5, 70.5) + sector(310, 319, 3.0, 13.5)
                                     + sector(-1, 7, 11.5, 66.0) + sector(130, 139, 3.0, 13.5))
parts["02_Outer_Perforated_Tube"] = src("02_Outer_Perforated_Tube")
# 03 support ring: plate + disk-centering wall + NEW bolt-on outer wall (6 seat-bolt holes) + leg holes + wire holes
sr = ring(36.25, 70.85, -6.3, -5.5) + ring(46.25, 47.05, -5.5, 3.0) + ring(70.05, 70.85, -5.5, 8.5)
for a in BOLT: sr -= rhole(a, 70.45, 2.15, length=6)
for a in (40, 160, 280): sr -= vhole(a, 65.85, 3.3, -8, -4)
for a, r in WIRE: sr -= vhole(a, R_WIRE, r, -8, -4)
parts["03_Support_Ring"] = solid(sr)
# 04 bottom cap: wire/TC holes under the support ring; old tube-gap holes plugged
bc = src("04_Bottom_Cap")
for a, r in WIRE: bc -= vhole(a, R_WIRE, r, -40, -10)
for a, r in [(183.0, 4.0), (188.0, 4.0), (315.0, 3.0)]: bc += vhole(a, 74.05, r + 0.6, -32.9, -31.7)
parts["04_Bottom_Cap"] = solid(bc)
# 05 one-piece top cap, redrawn clean 2026-09-28 from the pre-June cap's layout:
#   flat top (1.2) sitting ON the tube tops, open in the middle so the ceramic core top stays bare for the lid disk;
#   sleeves hugging the ceramic, the inner tube and the outer tube (0.2 mm clearance each);
#   6 tabs down the outside to the top bolt line (Ø6.6 at z 59); 4 glass slots straight through, lined up with the walls;
#   vent holes over the gap between the tubes. The 5 old screw ears are gone (nothing screws into them anymore).
# (OCC fails cutting the slots through the fused cap, so each ring gets its slots first, then everything fuses)
def slot_box(a): return Rot(0, 0, a) * Pos(63.37, 0, 86.13) * Box(39.9, 11.0, 16.3)
rings = []
for ri, ro, z0, z1 in [(46.45, 78.65, 91.0, 91.0 + CAP_T),   # top plate
                       (46.45, 47.65, 81.0, 91.2),            # sleeve around the ceramic core
                       (69.85, 70.65, 86.0, 91.2),            # sleeve just inside the inner tube
                       (77.45, 78.65, 81.0, 91.2)]:           # skirt outside the outer tube
    r = ring(ri, ro, z0, z1)
    for a in SLOTS: r = r - slot_box(a)
    rings.append(r)
cap = rings[0]
for r in rings[1:]: cap = cap + r
for a in BOLT:
    cap = cap + Rot(0, 0, a) * Pos(78.05, 0, 66.1) * Box(CAP_T, 14.0, 30.2) - rhole(a, 78.05, 59.0, length=6)
for k in range(60):
    if min(abs((k * 6.0 - s + 180) % 360 - 180) for s in SLOTS) > 9:
        cap = cap - vhole(k * 6.0, 73.85, 1.75, 90.0, 93.0)
# 2026-09-28 (Matt): metal slot grooves. Each glass slot gets a U-channel (two side walls + floor) down to the wall
# slots' bottom (z 67.5), so the insulation is never open and the cap stays ONE piece (the channels bridge each slot).
# Two runs per slot: ceramic -> inner tube, and inner tube -> outer tube (the tube walls themselves carry the slot).
SLOT_HW = 5.5                                   # channel inside half-width = the cap slot (11.0); wall slots are 10.5
FLOOR = 67.5                                    # bottom of the wall slots (23.5 deep from z 91)
def groove(a, r0, r1):
    L, rm = r1 - r0, (r0 + r1) / 2
    g = Pos(rm, 0, FLOOR - CAP_T / 2) * Box(L, 2 * (SLOT_HW + CAP_T), CAP_T)
    for s in (-1, 1):
        g = g + Pos(rm, s * (SLOT_HW + CAP_T / 2), (FLOOR - CAP_T + 91.0 + CAP_T) / 2) * Box(L, CAP_T, 91.0 + CAP_T - (FLOOR - CAP_T))
    return Rot(0, 0, a) * g
for a in SLOTS:
    cap = cap + groove(a, 46.45, 70.3) + groove(a, 71.85, 75.5)   # ends pulled in so the square corners clear the tubes
parts["05_One_Piece_Top_Cap"] = solid(cap)
parts["06_Lid_Inner_Tube"] = solid(LIFT * src("06_Lid_Inner_Tube"))
parts["07_Lid_Outer_Perforated_Tube"] = solid(LIFT * src("07_Lid_Outer_Perforated_Tube"))
# 08 lid top disk: 6 holes in the skirt for the upper lid bolts
td = src("08_Lid_Top_Disk")   # holes cut at the original height, then the whole part is raised with the lid
for a in BOLT: td -= rhole(a, 78.1, 119.0)
parts["08_Lid_Top_Disk"] = solid(LIFT * td)
# 09 lid ceramic holder: sits on the top cap (z 92.2). The ceramic lid disk still rests on the core top (z 91,
# raised center down in the bore), so the pocket wraps its edge from the lid bottom up and the shelf stays at the
# disk's top (z 96.05); the disk's lower 1.2 mm passes through the cap's center opening. Disk glued in.
Z0 = 91.0 + CAP_T
wall_ri = 46.25 + 0.2
h = (ring(38.8, wall_ri + T, 96.05, 96.05 + T) + ring(wall_ri, wall_ri + T, Z0, 96.05 + T)
     + ring(wall_ri, 77.2, Z0, Z0 + T) + ring(70.7, 70.7 + T, Z0 + T, 105.0 + CAP_T) + ring(77.2 - T, 77.2, Z0 + T, 94.0 + CAP_T))
for a in BOLT: h -= rhole(a, 70.7 + T / 2, 99.0 + CAP_T, length=6)
parts["09_Lid_Ceramic_Holder"] = solid(h)
parts["10_Lid_Handle"] = solid(LIFT * src("10_Lid_Handle"))
parts["11_Lid_Hinge_Strap"] = solid(LIFT * src("11_Lid_Hinge_Strap"))
parts["13_Hinge_Pin"] = solid(LIFT * src("13_Hinge_Pin"))
parts["14_Steel_Tray"] = src("14_Steel_Tray")

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "STEP")); os.makedirs(os.path.join(OUT, "STL"))
shutil.copy(os.path.join(ROOT, "Scripts", "package_README.txt"), os.path.join(OUT, "README.txt"))
for name, shape in parts.items():
    export_step(shape, os.path.join(OUT, "STEP", name + ".step"))
    export_stl(shape, os.path.join(OUT, "STL", name + ".stl"))
    print("wrote", name)
# the viewers show exactly these parts
VIEW = {"01_Inner_Wall_Tube": "viewer-full/01", "03_Support_Ring": "viewer-full/03", "04_Bottom_Cap": "viewer-full/04",
        "05_One_Piece_Top_Cap": "viewer-full/cap", "06_Lid_Inner_Tube": "viewer-lid-full/06", "07_Lid_Outer_Perforated_Tube": "viewer-lid-full/07",
        "08_Lid_Top_Disk": "viewer-lid-full/08", "09_Lid_Ceramic_Holder": "viewer-lid-full/09", "10_Lid_Handle": "viewer-lid-full/10",
        "11_Lid_Hinge_Strap": "viewer-lid-full/11", "13_Hinge_Pin": "viewer-lid-full/13"}
for name, dst in VIEW.items():
    trimesh.load(os.path.join(OUT, "STL", name + ".stl")).export(os.path.join(ROOT, dst + ".glb"))
print("viewer meshes refreshed from the package")
