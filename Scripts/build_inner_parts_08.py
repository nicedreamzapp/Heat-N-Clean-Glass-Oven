"""
build_inner_parts_08.py — make the 0.8 mm inner parts REAL (2026-09-09).

The five inside parts were specified at 0.8 mm on 2026-08-07; our own
files stayed at 1.2 and the request was later conceded by email. This rebuilds
those five parts from hnc_params (inner_sheet_thickness = 0.8) and assembles a
complete 14-part package next to the old one, copying the nine unchanged parts.

  01 Inner Wall Tube      <- build_base_body.py (PARTS_DIR mode, outer tube skipped)
  03 Support Ring         <- build_base_body.py  (Ø141.7 ring — seats inside the inner wall)
  06 Lid Inner Tube       <- built here with build_lid helpers
  09 Lid Ceramic Holder   <- build_fab_4_parts.build_lid_ceramic_holder
  12 Hold-Down Ring       <- build_cap_shell_ring.build_hold_down_ring

Run: ./.venv-cad/bin/python Scripts/build_inner_parts_08.py
Out: CAD Exports/FAB_PACKAGE_2026-09-09/STEP/  (all 14 parts)
"""
import os, sys, shutil, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hnc_params import *  # noqa
from build123d import export_step, import_step

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(SCRIPTS)
OLD = os.path.join(PROJ, "CAD Exports", "FAB_PACKAGE", "STEP")
TOSEND = os.path.join(PROJ, "Factory Files", "2026-08-24 Tianrun", "TO SEND")   # gitignored working dir
OUT = os.path.join(PROJ, "CAD Exports", "FAB_PACKAGE_2026-09-09", "STEP")
os.makedirs(OUT, exist_ok=True)
PY = sys.executable

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

# ── 1. copy the nine unchanged 1.2 mm / rod / tray parts ─────────────────────
unchanged = {
    "02_Outer_Perforated_Tube.step": os.path.join(TOSEND, "02_Outer_Perforated_Tube_slots_2026-08-24.step"),
    "04_Bottom_Cap.step": None, "05_Cap_Shell.step": None, "07_Lid_Outer_Perforated_Tube.step": None,
    "08_Lid_Top_Disk.step": None, "10_Lid_Handle.step": None, "11_Lid_Hinge_Strap.step": None,
    "13_Hinge_Pin.step": None, "14_Steel_Tray.step": None,
}
for name, src in unchanged.items():
    src = src or os.path.join(OLD, name)
    shutil.copy2(src, os.path.join(OUT, name))
    log("copied", name)

# ── 2. 01 inner wall + 03 support ring via build_base_body.py ────────────────
log("building 01 + 03 (base body, outer skipped) ...")
env = dict(os.environ, SKIP_OUTER="1", PARTS_DIR=OUT)
r = subprocess.run([PY, os.path.join(SCRIPTS, "build_base_body.py")], env=env, capture_output=True, text=True)
print(r.stdout[-1500:]); print(r.stderr[-1500:])
assert r.returncode == 0, "build_base_body failed"

# ── 3. 06 lid inner tube (ID 141.7 / OD 143.3 / H 35, two M6 rings) ──────────
log("building 06 lid inner tube ...")
import build_lid as BL
lid_height, lid_bottom_z = 35, housing_top_z
tube = BL.hollow_tube(housing_inner_r, housing_outer_r, lid_height, lid_bottom_z)
m6_len = (mesh_outer_r - housing_inner_r) + 8.0
r_mid = (housing_inner_r + mesh_outer_r) / 2.0
for hz in (lid_bottom_z + 28, lid_bottom_z + 8):
    for ang in ring_screw_angles:
        tube = tube - BL.radial_cutter(r_mid, ang, hz, ring_screw_hole_r, m6_len)
export_step(BL.as_compound(tube), os.path.join(OUT, "06_Lid_Inner_Tube.step"))

# ── 4. 09 lid ceramic holder ─────────────────────────────────────────────────
log("building 09 lid ceramic holder ...")
import build_fab_4_parts as F4
holder, info, _ = F4.build_lid_ceramic_holder()
export_step(F4.as_compound(holder), os.path.join(OUT, "09_Lid_Ceramic_Holder.step"))
print("  ", info)

# ── 5. 12 hold-down ring ─────────────────────────────────────────────────────
log("building 12 hold-down ring ...")
import build_cap_shell_ring as CR
ring = CR.build_hold_down_ring()
export_step(ring, os.path.join(OUT, "12_Hold_Down_Ring.step"))

# ── 6. verify every file re-imports as a solid ───────────────────────────────
log("verifying ...")
for name in sorted(os.listdir(OUT)):
    if not name.endswith(".step"): continue
    p = import_step(os.path.join(OUT, name))
    bb = p.bounding_box()
    print(f"  {name:36s} solids={len(p.solids()):3d} vol={p.volume:12.1f}  size {bb.size.X:7.1f} x {bb.size.Y:7.1f} x {bb.size.Z:7.1f}")
log("DONE ->", OUT)
