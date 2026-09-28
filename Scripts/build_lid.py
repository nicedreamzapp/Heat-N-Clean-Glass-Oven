"""
build_lid.py — analytic STEP solids for the Heat-N-Clean Glass Oven LID parts.

Builds two TRUE analytic solids (real cylinders / planes / circular holes — NOT
meshes) for the sheet-metal fab quote:

    04_Lid_Assembly      twin-wall perforated lid, M6 bolt rings, ceramic holder,
                         top disk + handle.  304SS, 1.2 mm.
    05b_Lid_Hinge_Strap  bolt-on strap with one curled Ø8 barrel (Ø5.2 bore).
                         304SS, 1.2 mm.

All dimensions and world positions come from Scripts/hnc_params.py (the single
source of truth copied verbatim from the trimesh generator export_all_parts.py),
so these solids drop straight into the closed-lid world position on the chamber.

Run:  ./.venv-cad/bin/python Scripts/build_lid.py
"""
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hnc_params import *  # noqa: F401,F403

from build123d import (
    Cylinder, Box, Pos, Rot, Location, Align, Axis,
    Compound, Solid,
    export_step, import_step,
)


def as_compound(result):
    """Boolean chains can return a single Solid, a Part, or a ShapeList of
    several disjoint solids (this lid is an assembly of separate sheet-metal
    pieces). Always hand export_step a single exportable shape."""
    try:
        solids = result.solids()
    except AttributeError:
        solids = [result]
    if len(solids) == 1:
        return solids[0]
    return Compound(children=list(solids))

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPTS_DIR)
STEP_DIR = os.path.join(PROJECT_DIR, "CAD Exports", "STEP")
os.makedirs(STEP_DIR, exist_ok=True)

LID_PATH = os.path.join(STEP_DIR, "04_Lid_Assembly.step")
STRAP_PATH = os.path.join(STEP_DIR, "05b_Lid_Hinge_Strap.step")

CENTER = (Align.CENTER, Align.CENTER, Align.CENTER)


# ---------------------------------------------------------------------------
# Helpers — true analytic primitives
# ---------------------------------------------------------------------------
def hollow_tube(inner_r, outer_r, height, z_bottom):
    """Analytic hollow cylinder, axis = Z, sitting from z_bottom upward."""
    zc = z_bottom + height / 2.0
    outer = Pos(0, 0, zc) * Cylinder(radius=outer_r, height=height, align=CENTER)
    inner = Pos(0, 0, zc) * Cylinder(radius=inner_r, height=height, align=CENTER)
    return outer - inner


def flat_ring(inner_r, outer_r, z_bottom, thickness):
    """Analytic flat washer/disk band, axis = Z."""
    zc = z_bottom + thickness / 2.0
    outer = Pos(0, 0, zc) * Cylinder(radius=outer_r, height=thickness, align=CENTER)
    if inner_r <= 0:
        return outer
    inner = Pos(0, 0, zc) * Cylinder(radius=inner_r, height=thickness, align=CENTER)
    return outer - inner


def radial_cutter(r_mid, ang_deg, z, radius, length):
    """A cylinder lying horizontally, pointed radially outward at ang_deg,
    centered on the wall at (r_mid, z) — used to bore a round radial hole."""
    a = math.radians(ang_deg)
    # cylinder default axis = Z; rotate so axis -> radial direction (in XY plane).
    # radial direction is (cos a, sin a, 0); that's Z rotated -90 about Y then +ang about Z
    cut = Cylinder(radius=radius, height=length, align=CENTER)
    cut = Rot(0, 90, 0) * cut                 # axis now +X
    cut = Rot(0, 0, ang_deg) * cut            # axis now radial at ang_deg
    cut = Pos(r_mid * math.cos(a), r_mid * math.sin(a), z) * cut
    return cut


def tangent_cutter_or_solid(radius, length, t_off, ha, pivot_r, pivot_z):
    """Cylinder whose axis is the hinge-pin tangent line (matches generator
    _tangent_cyl). Returns an analytic cylinder positioned in world space."""
    htx, hty = -math.sin(ha), math.cos(ha)
    cyl = Cylinder(radius=radius, height=length, align=CENTER)
    # align Z -> tangent (htx, hty, 0): that is Z rotated -90 about Y (-> +X),
    # then rotated to the tangent heading in XY.
    heading = math.degrees(math.atan2(hty, htx))
    cyl = Rot(0, 90, 0) * cyl                 # axis -> +X
    cyl = Rot(0, 0, heading) * cyl            # axis -> tangent direction
    cx = pivot_r * math.cos(ha) + htx * t_off
    cy = pivot_r * math.sin(ha) + hty * t_off
    cyl = Pos(cx, cy, pivot_z) * cyl
    return cyl


# ===========================================================================
# 04_Lid_Assembly
# ===========================================================================
def build_lid():
    lid_height = 35
    lid_bottom_z = housing_top_z          # 91
    lid_top_z = lid_bottom_z + lid_height  # 126

    # --- 1. Solid shells, fused FIRST (booleans on holes come after) --------
    # Inner tube  (ID 141.7 / OD 144.1)
    inner_tube = hollow_tube(housing_inner_r, housing_outer_r, lid_height, lid_bottom_z)
    # Outer tube  (ID 152.1 / OD 154.5)
    outer_tube = hollow_tube(mesh_inner_r, mesh_outer_r, lid_height, lid_bottom_z)

    # Bottom ring (perforated band ceramic_outer_r -> mesh_outer_r at lid bottom)
    bottom_ring = flat_ring(ceramic_outer_r, mesh_outer_r, lid_bottom_z, sheet_metal_thickness)

    # Ceramic-holder wall + retaining shelf (holds the ceramic lid disk)
    lid_ring_inner_r = ceramic_outer_r - 10
    lid_wall_bottom = lid_bottom_z + sheet_metal_thickness
    lid_wall_height = 6.0 - sheet_metal_thickness         # 4.8
    holder_wall = hollow_tube(ceramic_outer_r, ceramic_outer_r + sheet_metal_thickness,
                              lid_wall_height, lid_wall_bottom)
    shelf_z = lid_wall_bottom + lid_wall_height
    holder_shelf = flat_ring(lid_ring_inner_r, ceramic_outer_r, shelf_z, sheet_metal_thickness)

    # Top disk (full Ø, closes the lid)
    top_disk = flat_ring(0, mesh_outer_r, lid_top_z, sheet_metal_thickness)

    # Handle — twin posts + cross bar (matches generator placement)
    lid_top_surface_z = lid_top_z + sheet_metal_thickness
    handle_height = 25
    handle_width = 50
    handle_bar_r = 4
    handle_offset_dist = 40
    slot_4_end_angle = slot_positions[3] + (slot_width * scale_factor / 2 / circumference * 360)
    large_gap_arc_deg = gaps[3] * scale_factor / circumference * 360
    _hinge_angle = slot_4_end_angle + large_gap_arc_deg / 2
    if _hinge_angle >= 360:
        _hinge_angle -= 360
    opp = math.radians(_hinge_angle) + math.pi
    hx = handle_offset_dist * math.cos(opp)
    hy = handle_offset_dist * math.sin(opp)
    tx = -math.sin(math.radians(_hinge_angle))
    ty = math.cos(math.radians(_hinge_angle))
    bar_heading = math.degrees(math.atan2(ty, tx))

    post1 = Pos(hx + tx * handle_width / 2, hy + ty * handle_width / 2,
                lid_top_surface_z + handle_height / 2) * \
        Cylinder(radius=handle_bar_r, height=handle_height, align=CENTER)
    post2 = Pos(hx - tx * handle_width / 2, hy - ty * handle_width / 2,
                lid_top_surface_z + handle_height / 2) * \
        Cylinder(radius=handle_bar_r, height=handle_height, align=CENTER)
    bar = Cylinder(radius=handle_bar_r, height=handle_width, align=CENTER)
    bar = Rot(0, 90, 0) * bar
    bar = Rot(0, 0, bar_heading) * bar
    bar = Pos(hx, hy, lid_top_surface_z + handle_height) * bar

    # --- 2. M6 radial bolt-ring holes (Ø6.6) through BOTH walls FIRST -------
    # Cut M6 before the perfs (clean single-solid booleans). The identical
    # radial cutter is bored into the inner tube AND the outer tube separately
    # so the holes line up across both walls.
    lid_ring_zs = [lid_bottom_z + 28, lid_bottom_z + 8]   # 119 (top), 99 (bottom)
    m6_len = (mesh_outer_r - housing_inner_r) + 8.0        # spans inner + outer wall
    r_mid = (housing_inner_r + mesh_outer_r) / 2.0
    m6_centers = []   # (ang_deg, z) of every M6 hole, for perf-exclusion below
    m6_count = 0
    for hz in lid_ring_zs:
        for ha_deg in ring_screw_angles:
            cut = radial_cutter(r_mid, ha_deg, hz, ring_screw_hole_r, m6_len)
            inner_tube = inner_tube - cut
            outer_tube = outer_tube - radial_cutter(r_mid, ha_deg, hz, ring_screw_hole_r, m6_len)
            m6_centers.append((ha_deg, hz))
            m6_count += 1

    # --- 3. Perforations on the OUTER tube (Ø4) -----------------------------
    # Cut into the OUTER TUBE ALONE (single solid -> robust booleans). SKIP any
    # perf that lands inside an M6 bolt-hole footprint (just as the fab drawing
    # clears the perf field around each bolt) — otherwise the Ø6.6 / Ø4 overlap
    # fragments the tube into degenerate slivers that mangle on STEP export.
    # This mirrors the generator (in_lid_ring_hole wins over in_perf).
    lid_perf_n_z = int((lid_height - 10) / perf_spacing)
    perf_len = (mesh_outer_r - mesh_inner_r) + 6.0  # overshoot both faces
    perf_clear = ring_screw_hole_r + perf_hole_r + 0.5   # exclusion radius (arc)
    perf_count = 0
    perf_skipped = 0
    for zi in range(lid_perf_n_z):
        z = lid_bottom_z + 5 + zi * perf_spacing
        offset = (perf_spacing / 2) if (zi % 2) else 0.0
        for ai in range(perf_n_ang):
            ang = (ai / perf_n_ang) * 360 + math.degrees(offset / perf_mid_r)
            # skip if too close to any M6 hole (arc distance on the perf cylinder)
            skip = False
            for (ma, mz) in m6_centers:
                dz = z - mz
                if abs(dz) > perf_clear + 4:
                    continue
                dang = abs(ang - ma)
                if dang > 180:
                    dang = 360 - dang
                arc = math.radians(dang) * perf_mid_r
                if math.hypot(arc, dz) < perf_clear:
                    skip = True
                    break
            if skip:
                perf_skipped += 1
                continue
            outer_tube = outer_tube - radial_cutter(perf_mid_r, ang, z, perf_hole_r, perf_len)
            perf_count += 1

    # --- 4. Collect every finished piece as its own solid -------------------
    # The lid is an assembly of separate sheet-metal pieces (it is not one
    # contiguous lump), so we gather all solids into a flat list and build the
    # Compound from them directly. We deliberately do NOT boolean-union the
    # hole-riddled tubes with the rest (a fuse against a many-faced perforated
    # tube silently drops solids in OCP); each piece stays a clean analytic
    # solid the shop can measure.
    def _flatten(obj):
        try:
            return list(obj.solids())
        except AttributeError:
            return [obj]

    pieces = []
    for part in (inner_tube, outer_tube, bottom_ring, holder_wall,
                 holder_shelf, top_disk, post1, post2, bar):
        pieces.extend(_flatten(part))
    lid = Compound(children=pieces)

    return lid, {
        "lid_height": lid_height,
        "lid_bottom_z": lid_bottom_z,
        "perf_skipped_for_M6": perf_skipped,
        "perf_count": perf_count,
        "m6_count": m6_count,
        "m6_z_levels": lid_ring_zs,
    }


# ===========================================================================
# 05b_Lid_Hinge_Strap
# ===========================================================================
def build_strap():
    ha = math.radians(HINGE_ANGLE_DEG)      # 292.4 deg
    htx, hty = -math.sin(ha), math.cos(ha)

    # Plate: 1.2 (radial thick) x 28 (along tangent) x 14 (tall), like the box
    # in the generator, rotated to the hinge clocking, sat at z=98, pushed out
    # along the tangent by 5 (matches _htx*5/_hty*5 offset).
    plate = Box(sheet_metal_thickness, 28, 14, align=CENTER)
    plate = Rot(0, 0, HINGE_ANGLE_DEG) * plate
    px = 78.15 * math.cos(ha) + htx * 5
    py = 78.15 * math.sin(ha) + hty * 5
    plate = Pos(px, py, 98) * plate

    # M6 clearance hole (Ø6.6) bored radially at r=78.15, z=99
    bolt_cut = radial_cutter(78.15, HINGE_ANGLE_DEG, 99, ring_screw_hole_r, 6.0)
    plate = plate - bolt_cut

    # Curled barrel: outer Ø8 (R4), bored Ø5.2 (R2.6) for the Ø5 pin.
    barrel_outer = tangent_cutter_or_solid(HINGE_BARREL_OUTER_R, HINGE_KN_LEN, HINGE_T_OFF,
                                           ha, HINGE_PIVOT_R, HINGE_PIVOT_Z)
    barrel_bore = tangent_cutter_or_solid(HINGE_BARREL_BORE_R, HINGE_KN_LEN + 2.0, HINGE_T_OFF,
                                          ha, HINGE_PIVOT_R, HINGE_PIVOT_Z)
    barrel = barrel_outer - barrel_bore

    strap = plate + barrel

    return strap, {
        "barrel_outer_dia": 2 * HINGE_BARREL_OUTER_R,
        "barrel_bore_dia": 2 * HINGE_BARREL_BORE_R,
        "bolt_hole_dia": 2 * ring_screw_hole_r,
        "hinge_angle": HINGE_ANGLE_DEG,
    }


# ===========================================================================
# Validation
# ===========================================================================
def validate(path, label, extra=None):
    p = import_step(path)
    vol = p.volume
    bb = p.bounding_box()
    print(f"\n=== VALIDATE {label} ===")
    print(f"  file: {path}")
    print(f"  solids: {len(p.solids())}   volume: {vol:,.1f} mm^3  (valid solid: {vol > 0})")
    print(f"  bbox min: ({bb.min.X:.2f}, {bb.min.Y:.2f}, {bb.min.Z:.2f})")
    print(f"  bbox max: ({bb.max.X:.2f}, {bb.max.Y:.2f}, {bb.max.Z:.2f})")
    print(f"  bbox size: ({bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f})")
    if extra:
        for k, v in extra.items():
            print(f"  {k}: {v}")
    return vol > 0


# ===========================================================================
if __name__ == "__main__":
    print("Building 04_Lid_Assembly ...")
    lid, lid_info = build_lid()
    lid = as_compound(lid)
    export_step(lid, LID_PATH)
    print("  exported", LID_PATH)

    print("Building 05b_Lid_Hinge_Strap ...")
    strap, strap_info = build_strap()
    strap = as_compound(strap)
    export_step(strap, STRAP_PATH)
    print("  exported", STRAP_PATH)

    # Reload + report measured dims
    lid_extra = {
        "tube ID inner/outer (mm)": f"{2*housing_inner_r:.1f} / {2*mesh_inner_r:.1f}",
        "tube OD inner/outer (mm)": f"{2*housing_outer_r:.1f} / {2*mesh_outer_r:.1f}",
        "lid_height (mm)": lid_info["lid_height"],
        "lid_bottom_z (mm)": lid_info["lid_bottom_z"],
        "perf Ø (mm)": 2 * perf_hole_r,
        "perf count": lid_info["perf_count"],
        "perf skipped (M6 clearance)": lid_info["perf_skipped_for_M6"],
        "M6 Ø (mm)": 2 * ring_screw_hole_r,
        "M6 count": lid_info["m6_count"],
        "M6 z-levels (mm)": lid_info["m6_z_levels"],
        "M6 angles (deg)": [round(a, 1) for a in ring_screw_angles],
    }
    validate(LID_PATH, "04_Lid_Assembly", lid_extra)

    strap_extra = {
        "barrel outer Ø (mm)": strap_info["barrel_outer_dia"],
        "barrel bore Ø (mm)": strap_info["barrel_bore_dia"],
        "bolt hole Ø (mm)": strap_info["bolt_hole_dia"],
        "bolts under lid @ (deg)": strap_info["hinge_angle"],
    }
    validate(STRAP_PATH, "05b_Lid_Hinge_Strap", strap_extra)

    print("\nDONE.")
