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
parts["06_Lid_Inner_Tube"] = src("06_Lid_Inner_Tube")
parts["07_Lid_Outer_Perforated_Tube"] = src("07_Lid_Outer_Perforated_Tube")
# 08 lid top disk: 6 holes in the skirt for the upper lid bolts
td = src("08_Lid_Top_Disk")
for a in BOLT: td -= rhole(a, 78.1, 119.0)
parts["08_Lid_Top_Disk"] = solid(td)
# 09 lid ceramic holder: wraps the ceramic lid disk edge, holds it from above (disk glued in); bolt-on upright wall
wall_ri = 46.25 + 0.2
h = (ring(38.8, wall_ri + T, 96.05, 96.05 + T) + ring(wall_ri, wall_ri + T, 91.0, 96.05 + T)
     + ring(wall_ri, 77.2, 91.0, 91.0 + T) + ring(70.7, 70.7 + T, 91.0 + T, 105.0) + ring(77.2 - T, 77.2, 91.0 + T, 94.0))
for a in BOLT: h -= rhole(a, 70.7 + T / 2, 99.0, length=6)
parts["09_Lid_Ceramic_Holder"] = solid(h)
parts["10_Lid_Handle"] = src("10_Lid_Handle")
parts["11_Lid_Hinge_Strap"] = src("11_Lid_Hinge_Strap")
parts["13_Hinge_Pin"] = src("13_Hinge_Pin")
parts["14_Steel_Tray"] = src("14_Steel_Tray")

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "STEP")); os.makedirs(os.path.join(OUT, "STL"))
for name, shape in parts.items():
    export_step(shape, os.path.join(OUT, "STEP", name + ".step"))
    export_stl(shape, os.path.join(OUT, "STL", name + ".stl"))
    print("wrote", name)
# 05 top cap exists only as a mesh today (pre-June one-piece cap + the 6 bolt tabs): ship the STL and say so
trimesh.load(os.path.join(ROOT, "viewer-full", "cap.glb"), force="mesh").export(os.path.join(OUT, "STL", "05_One_Piece_Top_Cap.stl"))
print("wrote 05_One_Piece_Top_Cap (STL only)")
