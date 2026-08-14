"""
build_fab_4_parts.py — 4 analytic B-rep STEP solids for the fab quote package.

Each part is reconstructed from its approved reference GLB mesh: the GLB is
measured for OD / ID / height / hole patterns, then a clean analytic build123d
solid (real cylinders / planes / circular holes — NOT a tessellated mesh) is
built to match those dims within ~0.3 mm and exported as STEP.

Parts:
  03_Support_Ring      <- CAD Exports/Core Split/3_Support_Ring_Full.glb
  08_Lid_Top_Disk      <- CAD Exports/Lid Split/3_Lid_Top_Disk.glb
  09_Lid_Ceramic_Holder<- CAD Exports/Lid Split/4_Lid_Ceramic_Holder.glb
  10_Lid_Handle        <- CAD Exports/Lid Split/5_Lid_Handle.glb

Run: ./.venv-cad/bin/python Scripts/build_fab_4_parts.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import trimesh
from hnc_params import *  # noqa: F401,F403
from build123d import (
    Cylinder, Box, Pos, Rot, Align, Compound,
    export_step, import_step,
)

CENTER = (Align.CENTER, Align.CENTER, Align.CENTER)
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPTS_DIR)
GLB_DIR = os.path.join(PROJECT_DIR, "CAD Exports")
OUT_DIR = os.path.join(PROJECT_DIR, "CAD Exports", "FAB_PACKAGE", "STEP")
os.makedirs(OUT_DIR, exist_ok=True)


# ── helpers ────────────────────────────────────────────────────────────────
def flat_ring(inner_r, outer_r, z_bottom, thickness):
    zc = z_bottom + thickness / 2.0
    outer = Pos(0, 0, zc) * Cylinder(radius=outer_r, height=thickness, align=CENTER)
    if inner_r <= 0:
        return outer
    inner = Pos(0, 0, zc) * Cylinder(radius=inner_r, height=thickness, align=CENTER)
    return outer - inner


def hollow_tube(inner_r, outer_r, height, z_bottom):
    zc = z_bottom + height / 2.0
    outer = Pos(0, 0, zc) * Cylinder(radius=outer_r, height=height, align=CENTER)
    inner = Pos(0, 0, zc) * Cylinder(radius=inner_r, height=height, align=CENTER)
    return outer - inner


def vbore(ang_deg, r_pos, hole_r, z_center, depth):
    """Vertical (Z-axis) circular through-hole cutter centred at (r_pos,ang)."""
    a = math.radians(ang_deg)
    x, y = r_pos * math.cos(a), r_pos * math.sin(a)
    return Pos(x, y, z_center) * Cylinder(radius=hole_r, height=depth, align=CENTER)


def as_compound(result):
    try:
        solids = result.solids()
    except AttributeError:
        solids = [result]
    if len(solids) == 1:
        return solids[0]
    return Compound(children=list(solids))


def glb_bbox(rel):
    m = trimesh.load(os.path.join(GLB_DIR, rel), force='mesh')
    return m.bounds, (m.bounds[1] - m.bounds[0])


# ═══════════════════════════════════════════════════════════════════════════
# 1. SUPPORT RING  (3_Support_Ring_Full.glb : Ø143 x 18, z -6.85..11.15)
#    Profile read from mesh:
#      inner bore r=36.25, present only at the bottom plate (z -6.7..-5.5)
#      flat annulus wall r 46.25/47.25 from z -5.5 .. +3.0
#      outer rim r 70.3/71.5 (OD 143) spanning the full height z -6.85 .. 11.15
#    Interpretation: a formed 304SS seating ring — an outer rim band (full
#    height) + a flat inner seat/plate near the bottom with a Ø72.5 bore step
#    and a central Ø72.5 -> Ø92.5 ledge. We reproduce it as concentric
#    sheet-metal bands matching the measured radii & z-spans, then drill the
#    3 leg holes (Ø6.6 @ leg_angles on r=leg_hole_r) the assembly uses.
# ═══════════════════════════════════════════════════════════════════════════
def build_support_ring():
    bb, ext = glb_bbox("Core Split/3_Support_Ring_Full.glb")
    z_lo, z_hi = float(bb[0][2]), float(bb[1][2])          # -6.85 .. 11.15
    T = sheet_metal_thickness                               # 1.2

    # measured radii from the mesh
    r_bore   = 36.25      # central bore (bottom plate)
    r_in_a   = 46.25      # inner annulus wall ID
    r_in_b   = 47.25      # inner annulus wall OD  (~1.0 wall)
    r_rim_in = 70.30      # outer rim ID
    r_rim_out = 71.50     # outer rim OD  -> OD 143.0

    # Bottom plate: flat annulus, bore Ø72.5 .. inner wall, sits at the bottom
    plate_z0 = z_lo                       # -6.85
    plate_t  = 1.35                       # (-6.85 .. -5.5)
    bottom_plate = flat_ring(r_bore, r_rim_out, plate_z0, plate_t)

    # Inner annular wall (Ø92.5 / Ø94.5 band) rising from the plate to z~+3.0
    inner_wall = hollow_tube(r_in_a, r_in_b, (3.0 - (plate_z0 + plate_t)), plate_z0 + plate_t)

    # Outer rim band — full height of the part (the seating flange wall)
    outer_rim = hollow_tube(r_rim_in, r_rim_out, (z_hi - z_lo), z_lo)

    ring = as_compound(bottom_plate + inner_wall + outer_rim)

    # 3 leg bolt holes Ø6.6 at leg_angles on r=leg_hole_r (drilled through plate)
    holes = 0
    for ang in leg_angles:
        if leg_hole_r < r_rim_in:   # only drill where there's plate material
            ring = ring - vbore(ang, leg_hole_r, bolt_hole_size / 2,
                                plate_z0 + plate_t / 2, plate_t + 4)
            holes += 1
    info = {
        "OD (mm)": round(2 * r_rim_out, 2),
        "bore Ø (mm)": round(2 * r_bore, 2),
        "inner annulus Ø (mm)": f"{2*r_in_a:.1f}/{2*r_in_b:.1f}",
        "height (mm)": round(z_hi - z_lo, 2),
        "leg holes Ø6.6 @": f"{leg_angles} on r={leg_hole_r}",
        "leg holes drilled": holes,
    }
    return as_compound(ring), info, (bb, ext)


# ═══════════════════════════════════════════════════════════════════════════
# 2. LID TOP DISK  (3_Lid_Top_Disk.glb : Ø157.5 x 14.2, z 113.0..127.2)
#    Mesh read: full disk (min r=0 -> NO central bore, NO vent perforations —
#    radial histogram is uniform), a solid top face at z~126-127, and a thin
#    rim wall at the outer edge dropping to z=113 (r 77.55..78.75 at z~113).
#    -> a dished top: a flat top plate at OD 157.5 + a short outer rim skirt.
# ═══════════════════════════════════════════════════════════════════════════
def build_lid_top_disk():
    bb, ext = glb_bbox("Lid Split/3_Lid_Top_Disk.glb")
    z_lo, z_hi = float(bb[0][2]), float(bb[1][2])    # 113.0 .. 127.2
    r_out = float(ext[0]) / 2.0                       # 78.75 -> OD 157.5
    T = sheet_metal_thickness

    # Top plate (full Ø, solid) — the closing face, at the top
    top_plate = flat_ring(0, r_out, z_hi - T, T)

    # Outer rim skirt: vertical wall hanging from the plate down to z_lo
    skirt_h = (z_hi - T) - z_lo
    skirt = hollow_tube(r_out - T, r_out, skirt_h, z_lo)

    disk = as_compound(top_plate + skirt)
    info = {
        "OD (mm)": round(2 * r_out, 2),
        "height (mm)": round(z_hi - z_lo, 2),
        "top plate thk (mm)": T,
        "rim skirt height (mm)": round(skirt_h, 2),
        "central bore": "none (solid disk per mesh)",
        "vent holes": "none (uniform radial mesh — no perforation ring)",
    }
    return disk, info, (bb, ext)


# ═══════════════════════════════════════════════════════════════════════════
# 3. LID CERAMIC HOLDER  (4_Lid_Ceramic_Holder.glb : Ø154.5 x 14, z 91..105)
#    Mesh read: a big flat web at z 91.35..92.05 spanning r 46.25..77.25,
#    bore inner edge r=36.25, hanging walls up to z~102, a small top band at
#    z 104.65 r 70.3..71.5. This is the lid's ceramic retainer (analog of the
#    body Hold-Down Ring): a flat web + concentric retaining walls/lip.
#    Reproduce: flat web ring + bore grab lip + ceramic-OD flap wall + outer
#    chamber-edge rim, at the measured radii, web at the bottom (z~91.7).
# ═══════════════════════════════════════════════════════════════════════════
def build_lid_ceramic_holder():
    bb, ext = glb_bbox("Lid Split/4_Lid_Ceramic_Holder.glb")
    z_lo, z_hi = float(bb[0][2]), float(bb[1][2])     # 91.0 .. 105.0
    r_out = float(ext[0]) / 2.0                        # 77.25 -> OD 154.5
    T = sheet_metal_thickness

    r_bore   = 36.25       # grab-lip ID (mesh inner edge)
    r_cer_in = ceramic_outer_r        # 46.25  (web ID)
    r_flap   = 71.50       # ceramic-OD / inner flap wall radius
    r_rim    = r_out       # 77.25 outer rim

    web_z = z_lo                       # web at bottom 91.0
    # flat web band (Ø92.5 .. Ø154.5) — the main flange
    web = flat_ring(r_cer_in, r_rim, web_z, T)

    # bore grab lip: short ring rising from the bore edge
    grab = hollow_tube(r_bore, r_bore + T, 1.0, web_z)
    # bore web (closes Ø72.5..Ø92.5 inner ledge that the mesh shows near bore)
    inner_web = flat_ring(r_bore, r_cer_in, web_z, T)

    # retaining wall rising to the top band at z 104.65 (r ~70.3..71.5)
    wall_h = (z_hi - 0.35) - (web_z + T)
    ret_wall = hollow_tube(r_flap - T, r_flap, wall_h, web_z + T)
    # top return band at r 70.3..71.5
    top_band = flat_ring(r_flap - T, r_flap, z_hi - T, T)

    # outer chamber rim wall (short)
    rim_wall = hollow_tube(r_rim - T, r_rim, 3.0, web_z)

    holder = as_compound(web + grab + inner_web + ret_wall + top_band + rim_wall)
    info = {
        "OD (mm)": round(2 * r_rim, 2),
        "bore Ø (mm)": round(2 * r_bore, 2),
        "web Ø band (mm)": f"{2*r_cer_in:.1f}..{2*r_rim:.1f}",
        "height (mm)": round(z_hi - z_lo, 2),
        "retaining wall r (mm)": r_flap,
        "approximated": "wall/web layout reproduced from mesh radii bands",
    }
    return holder, info, (bb, ext)


# ═══════════════════════════════════════════════════════════════════════════
# 4. LID HANDLE  (5_Lid_Handle.glb : 54.2 x 27.1 x 29, z 127..156)
#    Mesh read: a U/staple of round Ø8 (R4) bar. Two feet (R4 round) at z=127
#    centred A(-38.36,27.46) B(7.87,46.51), span 50 mm @ heading 22.4°. Legs
#    rise vertically to ~z152, crossbar (round Ø8) joins the tops at z~152..156.
# ═══════════════════════════════════════════════════════════════════════════
def build_lid_handle():
    bb, ext = glb_bbox("Lid Split/5_Lid_Handle.glb")
    R = 4.0                              # Ø8 round bar (measured R4)
    foot_z = float(bb[0][2])             # 127.0
    bar_z = float(bb[1][2]) - R          # crossbar centre ~152.0
    # measured foot centres
    ax, ay = -38.36, 27.46
    bx, by = 7.87, 46.51
    span = math.hypot(bx - ax, by - ay)          # 50.0
    heading = math.degrees(math.atan2(by - ay, bx - ax))  # 22.4

    # two vertical legs
    leg_h = bar_z - foot_z
    legA = Pos(ax, ay, foot_z + leg_h / 2) * Cylinder(radius=R, height=leg_h, align=CENTER)
    legB = Pos(bx, by, foot_z + leg_h / 2) * Cylinder(radius=R, height=leg_h, align=CENTER)

    # crossbar — round bar from A-top to B-top, oriented along the heading
    cx, cy = (ax + bx) / 2, (ay + by) / 2
    bar = Cylinder(radius=R, height=span, align=CENTER)
    bar = Rot(0, 90, 0) * bar            # axis -> +X
    bar = Rot(0, 0, heading) * bar       # axis -> heading
    bar = Pos(cx, cy, bar_z) * bar

    handle = as_compound(legA + legB + bar)
    info = {
        "bar Ø (mm)": 2 * R,
        "foot span (mm)": round(span, 2),
        "heading (deg)": round(heading, 2),
        "leg height (mm)": round(leg_h, 2),
        "overall H (mm)": round(float(ext[2]), 2),
        "feet @ z (mm)": round(foot_z, 2),
        "section": "round Ø8 (U/staple)",
    }
    return handle, info, (bb, ext)


# ── build / export / validate ──────────────────────────────────────────────
def export_validate(part, out_name, info, glb_bb_ext, label):
    path = os.path.join(OUT_DIR, out_name)
    part = as_compound(part)
    export_step(part, path)
    re = import_step(path)
    bb = re.bounding_box()
    vol = re.volume
    gbb, gext = glb_bb_ext
    print(f"\n========== {label} ==========")
    print(f"  OUT: {path}")
    print(f"  valid solid: {vol > 0}   volume: {vol:,.1f} mm^3   solids: {len(re.solids())}")
    print(f"  STEP bbox min ({bb.min.X:.2f},{bb.min.Y:.2f},{bb.min.Z:.2f})  "
          f"max ({bb.max.X:.2f},{bb.max.Y:.2f},{bb.max.Z:.2f})")
    print(f"  STEP size  X{bb.size.X:7.2f}  Y{bb.size.Y:7.2f}  Z{bb.size.Z:7.2f}")
    print(f"  GLB  size  X{gext[0]:7.2f}  Y{gext[1]:7.2f}  Z{gext[2]:7.2f}")
    dx, dy, dz = bb.size.X - gext[0], bb.size.Y - gext[1], bb.size.Z - gext[2]
    print(f"  Δ size     X{dx:+7.2f}  Y{dy:+7.2f}  Z{dz:+7.2f}  (mm)")
    for k, v in info.items():
        print(f"    {k}: {v}")
    return vol > 0, (dx, dy, dz)


if __name__ == "__main__":
    results = []
    sr, sr_i, sr_g = build_support_ring()
    results.append(export_validate(sr, "03_Support_Ring.step", sr_i, sr_g, "03 Support Ring"))

    ltd, ltd_i, ltd_g = build_lid_top_disk()
    results.append(export_validate(ltd, "08_Lid_Top_Disk.step", ltd_i, ltd_g, "08 Lid Top Disk"))

    lch, lch_i, lch_g = build_lid_ceramic_holder()
    results.append(export_validate(lch, "09_Lid_Ceramic_Holder.step", lch_i, lch_g, "09 Lid Ceramic Holder"))

    lh, lh_i, lh_g = build_lid_handle()
    results.append(export_validate(lh, "10_Lid_Handle.step", lh_i, lh_g, "10 Lid Handle"))

    print("\n================ SUMMARY ================")
    ok = all(r[0] for r in results)
    print("all valid solids:", ok)
    for (v, d), name in zip(results, ["03_Support_Ring", "08_Lid_Top_Disk",
                                      "09_Lid_Ceramic_Holder", "10_Lid_Handle"]):
        maxd = max(abs(x) for x in d)
        print(f"  {name:24s} valid={v}  max|Δsize|={maxd:.2f}mm  "
              f"{'OK<=0.3' if maxd <= 0.31 else 'CHECK'}")
