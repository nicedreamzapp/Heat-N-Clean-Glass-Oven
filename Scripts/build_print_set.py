"""PRINT_SET_2026-11-08: plastic fit/display print set (Matt 2026-11-08).
12 metal parts copied from FAB_PACKAGE_2026-11-08 (no 14 tray this round) + 6 ceramic solids drawn here
at the measured sizes (hnc_params + the viewer meshes). Fit check places each ceramic where the viewers put it."""
import os, sys, math, shutil, json
from build123d import *
sys.path.insert(0, os.path.dirname(__file__)); import hnc_params as P
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "FAB_PACKAGE_2026-11-08"); OUT = os.path.join(ROOT, "PRINT_SET_2026-11-08")
for d in ("STL", "STEP"): os.makedirs(os.path.join(OUT, d), exist_ok=True)
METAL = ["01_Inner_Wall_Tube", "02_Outer_Perforated_Tube", "03_Support_Ring", "04_Bottom_Cap", "05_One_Piece_Top_Cap",
         "06_Lid_Inner_Tube", "07_Lid_Outer_Perforated_Tube", "08_Lid_Top_Disk", "09_Lid_Ceramic_Holder",
         "10_Lid_Handle", "11_Lid_Hinge_Strap", "13_Hinge_Pin"]
for n in METAL: shutil.copy(os.path.join(PKG, "STL", n + ".stl"), os.path.join(OUT, "STL", n + ".stl"))

def solid(x): return x if not isinstance(x, ShapeList) else Compound(children=list(x))
def cyl(r, h, z0=0): return Pos(0, 0, z0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))
def ring(ri, ro, z0, z1): return cyl(ro, z1 - z0, z0) - cyl(ri, z1 - z0, z0)
def radial(ang, r_mid, z, rad, length): return Rot(0, 0, ang) * Pos(r_mid, 0, z) * Rot(0, 90, 0) * Cylinder(rad, length)
RO, RI, H = P.ceramic_outer_r, P.ceramic_inner_r, P.cylinder_height        # 46.25 / 40.75 / 91
BOLT = P.ring_screw_angles                                                    # 52.4 + n*60

# C1 heater core: tube, 4 glass slots (10.5 wide, 23.5 deep, R5.25 round bottom) at the hnc_params angles,
# thermocouple hole Ø6.4 at 314.6 deg z 8.2, helical heater-wire groove (30 wraps z 15.5-66.5, 1.0 wide, 0.6 deep, as the viewer mesh)
core = ring(RI, RO, 0, H)
sb = H - P.slot_depth                                       # 67.5 slot bottom
for a in P.slot_positions:
    sl = Pos(0, 0, sb + P.slot_width / 2) * Box(RO + 3, P.slot_width, H, align=(Align.MIN, Align.CENTER, Align.MIN))
    sl += Pos(0, 0, sb + P.slot_width / 2) * Rot(0, 90, 0) * Cylinder(P.slot_width / 2, RO + 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    core -= Rot(0, 0, a) * sl
core -= radial(P.hole_position_angle, (RI + RO) / 2, P.hole_center_height, P.hole_diameter / 2, 12)
GROOVE = os.environ.get("HNC_GROOVE", "1") == "1"
if GROOVE:
    pitch = (P.groove_start_height - P.groove_end_height) / P.num_wraps     # 1.7
    hx = Helix(pitch, P.groove_start_height - P.groove_end_height, RO + 0.2, center=(0, 0, P.groove_end_height))
    p0 = hx @ 0; t0 = hx % 0
    pl = Plane(origin=p0, z_dir=t0, x_dir=(p0.X, p0.Y, 0))
    with BuildSketch(pl) as sk: Rectangle(1.6, 1.0)        # radial 45.65 .. 47.25 (0.6 into the wall, helix at r 46.45)
    sw = sweep(sk.sketch, path=hx, is_frenet=True)
    core = core - sw
core = solid(core)

def disk():   # base / lid disk as modelled: Ø92.5 x 4.5 body + raised centre Ø77 x 1.0 with a 0.5 taper (6.0 overall)
    pts = [(0, 0), (38.5, 0), (38.5, 1.0), (46.25, 1.5), (46.25, 6.0), (0, 6.0)]
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ): Polygon(*pts, align=None)
        revolve(axis=Axis.Z)
    return bp.part
def spacer(h):   # ID 136.1 / OD 144.1, 6 radial Ø6.6 holes at mid height on the bolt angles
    ri, ro = 68.05, 72.05
    s = ring(ri, ro, 0, h)
    for a in BOLT: s -= radial(a, (ri + ro) / 2, h / 2, 3.3, 8)
    return solid(s)
def foot():      # Ø20 x 20 post on a Ø28 x 5 base, Ø6.6 leg-screw hole through
    f = cyl(14, 5) + cyl(10, 20, 5)
    return solid(f - cyl(3.3, 30, -1))
CER = {"C1_Ceramic_Heater_Core": core, "C2_Ceramic_Base_Disk": disk(), "C3_Ceramic_Lid_Disk": disk(),
       "C4_Spacer_Ring_14mm": spacer(14), "C5_Spacer_Ring_10mm": spacer(10), "C6_Ceramic_Foot": foot()}
info = {}
for n, s in CER.items():
    export_step(s, os.path.join(OUT, "STEP", n + ".step")); export_stl(s, os.path.join(OUT, "STL", n + ".stl"))
    bb = s.bounding_box(); info[n] = [round(bb.size.X, 1), round(bb.size.Y, 1), round(bb.size.Z, 1), len(s.solids()), round(s.volume, 1)]
    print("wrote", n, info[n])
json.dump(info, open("/tmp/print_info.json", "w"))

# ── fit check in the assembly frame (viewer positions) ─────────────────────────────────────────────────────────
if os.environ.get("HNC_FIT", "1") != "1": sys.exit(0)
metal = {n: solid(import_step(os.path.join(PKG, "STEP", n + ".step"))) for n in METAL + ["14_Steel_Tray"]}
CORE_Z = float(os.environ.get("HNC_CORE_Z", 5.06))
placed = {"core": Pos(0, 0, CORE_Z) * core, "basedisk": Pos(0, 0, -0.44) * CER["C2_Ceramic_Base_Disk"],
          "liddisk": Pos(0, 0, 91.2) * CER["C3_Ceramic_Lid_Disk"]}
for k, z0 in (("sp_bot", -31.0), ("sp_seat", -5.0), ("sp_top", 52.0)): placed[k] = Pos(0, 0, z0) * CER["C4_Spacer_Ring_14mm"]
for k, z0 in (("sp_low", 95.2), ("sp_high", 115.2)): placed[k] = Pos(0, 0, z0) * CER["C5_Spacer_Ring_10mm"]
for i, a in enumerate((40, 160, 280)):
    placed["foot%d" % i] = Pos(60 * math.cos(math.radians(a)), 60 * math.sin(math.radians(a)), -56.7) * CER["C6_Ceramic_Foot"]
for k, s in placed.items():
    bb = s.bounding_box()
    for n, m in metal.items():
        mb = m.bounding_box()
        if bb.max.Z < mb.min.Z or bb.min.Z > mb.max.Z: continue
        x = s & m; v = x.volume if x is not None else 0
        if v > 0.01: print("CLASH", k, n, round(v, 2), "mm3")
for i, a in enumerate(list(placed)):
    for b in list(placed)[i + 1:]:
        x = placed[a] & placed[b]; v = x.volume if x is not None else 0
        if v > 0.01: print("CLASH", a, b, round(v, 2), "mm3")
# bolt lines (M6 Ø6) through every spacer ring + both tubes: must hit no ceramic
zs = {"sp_bot": -24.0, "sp_seat": 2.15, "sp_top": 59.0, "sp_low": 100.2, "sp_high": 120.2}
for k, zb in zs.items():
    for a in BOLT:
        rod = radial(a, 70.0, zb, 3.0, 14)
        x = rod & placed[k]; v = x.volume if x is not None else 0
        if v > 0.01: print("BOLT BLOCKED", k, a, round(v, 2))
for i, a in enumerate((40, 160, 280)):
    rod = Pos(60 * math.cos(math.radians(a)), 60 * math.sin(math.radians(a)), -70) * cyl(3.0, 44)
    x = rod & placed["foot%d" % i]; v = x.volume if x is not None else 0
    if v > 0.01: print("LEG SCREW BLOCKED", i, round(v, 2))
print("fit check done")
