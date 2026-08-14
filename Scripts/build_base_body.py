"""
Build 01_Base_Body as a TRUE ANALYTIC SOLID (real cylinders / planes / circular
holes) for sheet-metal fabrication quoting — NOT a tessellated mesh.

Reproduces export_all_parts.py PART 1A (inner housing) + 1B (outer perforated
mesh) + 1C (support ring) + standoff fins, with analytic features:
  - inner tube : ID 141.7 / OD 144.1, z = housing_bottom_z .. housing_top_z
                 (top edge dipped where the 4 glass slots cut in)
  - outer tube : ID 152.1 / OD 154.5, z = housing_bottom_z .. housing_top_z (h=122.7)
  - 4 glass slots : 10.5 wide x 23.5 deep from the TOP edge, rounded bottom,
                    through BOTH walls, at slot_positions
  - perforations  : Ø4 radial holes on the OUTER wall only, on the perf grid
  - M6 clamp holes: Ø6.6 radial holes through BOTH walls, 3 z-levels x 6 angles
  - wire holes    : Ø8 radial through inner wall, z = 66.5 & 15.5
  - tc hole       : Ø10 radial through inner wall
  - 3 leg holes   : Ø6.6 vertical through the support-ring horizontal lip

All numbers come from Scripts/hnc_params.py — nothing hardcoded.
World CS is preserved (Z = chamber axis), so it assembles with the other parts.
"""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hnc_params import *  # noqa: F401,F403  (single source of truth)

from build123d import (
    BuildPart, Cylinder, Box, Align, Locations, Rotation, Pos,
    Mode, Axis, fillet, export_step, import_step,
)
from build123d import Solid, Compound
from build123d import ShapeList


def as_compound(shape):
    """Normalize any boolean result (Solid / Compound / ShapeList) into a single
    Compound so subsequent .cut()/.fuse() calls always have a valid method."""
    if isinstance(shape, (list, ShapeList)):
        return Compound(list(shape))
    if isinstance(shape, Compound):
        return shape
    return Compound([shape])

# ---------------------------------------------------------------------------
# z extents from the source
# ---------------------------------------------------------------------------
ring_wall_top_z = hole_bottom_height - 2            # 3.0  (support-ring wall top)
Z_BOT = housing_bottom_z                            # -31.7
Z_TOP = housing_top_z                               # 91.0
WALL_H = Z_TOP - Z_BOT                              # 122.7
Z_MID = (Z_BOT + Z_TOP) / 2.0

# Radial-hole cylinder length: long enough to punch clean through any wall pair
RADIAL_LEN = 2 * mesh_outer_r + 20


def annulus(inner_r, outer_r, height, z_bottom):
    """Analytic hollow cylinder (outer cylinder minus inner cylinder)."""
    outer = Solid.make_cylinder(outer_r, height).locate(Pos(0, 0, z_bottom))
    inner = Solid.make_cylinder(inner_r, height).locate(Pos(0, 0, z_bottom))
    return outer.cut(inner)


def radial_hole(angle_deg, z, hole_r, length=RADIAL_LEN):
    """A cylinder lying along the radial direction at `angle_deg`, centered on
    the axis, at height `z` — used to bore a circular radial hole."""
    # cylinder along +Z by default; rotate to lie along X, move to z, rotate about Z
    cyl = Solid.make_cylinder(hole_r, length)          # axis +Z, base at origin
    cyl = cyl.rotate(Axis.Y, 90)                       # now axis along +X, spanning 0..length in X
    cyl = cyl.locate(Pos(-length / 2, 0, z))           # center it on the chamber axis
    cyl = cyl.rotate(Axis.Z, angle_deg)                # clock to the hole angle
    return cyl


def vertical_hole(angle_deg, radius_pos, hole_r, z_center, height):
    """Vertical (Z-axis) circular hole at polar position (radius_pos, angle)."""
    x = radius_pos * np.cos(np.radians(angle_deg))
    y = radius_pos * np.sin(np.radians(angle_deg))
    return Solid.make_cylinder(hole_r, height).locate(Pos(x, y, z_center - height / 2))


# ===========================================================================
# 1. Build the two walls + support ring + standoff fins, fuse into one solid
# ===========================================================================
print("Building walls...")
inner_wall = annulus(housing_inner_r, housing_outer_r, WALL_H, Z_BOT)
outer_wall = annulus(mesh_inner_r, mesh_outer_r, WALL_H, Z_BOT)

# Support ring (PART 1C): horizontal lip @ lip_z + vertical retaining wall
print("Building support ring...")
l_ring_inner_r = ceramic_outer_r - 10               # 36.25
horizontal_lip = annulus(l_ring_inner_r, housing_inner_r, sheet_metal_thickness, lip_z)
wall_bottom = lip_z + sheet_metal_thickness
ring_wall_h = ring_wall_top_z - wall_bottom
vertical_wall = annulus(ceramic_outer_r, ceramic_outer_r + sheet_metal_thickness,
                        ring_wall_h, wall_bottom)
support_ring = horizontal_lip.fuse(vertical_wall)

# Standoff fins (vent-chamber spacers) between the two walls — same set the
# generator builds (slot edges + non-hole midpoints)
print("Building standoff fins...")
fin_thickness = sheet_metal_thickness
fin_depth = air_gap
fin_r = (housing_outer_r + mesh_inner_r) / 2        # 74.05
fin_bottom_z = housing_bottom_z + 5
fin_top_z = housing_top_z - slot_depth - 2
fin_full_height = fin_top_z - fin_bottom_z
fin_center_z = (fin_bottom_z + fin_top_z) / 2

fin_angles = []
for slot_center in slot_positions:
    fin_angles.append(slot_center - slot_arc_half_deg)
    fin_angles.append(slot_center + slot_arc_half_deg)
for i in range(4):
    next_i = (i + 1) % 4
    a, b = slot_positions[i], slot_positions[next_i]
    mid = (a + b) / 2
    if b < a:
        mid = (a + b + 360) / 2
        if mid >= 360:
            mid -= 360
    skip = False
    for h_ang in [wire_hole_angle, wire_hole_angle + 5, tc_cable_hole_angle]:
        diff = abs(mid - h_ang)
        if diff > 180:
            diff = 360 - diff
        if diff < 6:
            skip = True
            break
    if not skip:
        fin_angles.append(mid)

fins = []
for ang in fin_angles:
    fin = Box(fin_depth, fin_thickness, fin_full_height,
              align=(Align.CENTER, Align.CENTER, Align.CENTER))
    fin = fin.locate(Pos(fin_r, 0, fin_center_z))
    fin = fin.rotate(Axis.Z, ang)
    fins.append(fin)

# ---------------------------------------------------------------------------
# CUTTER BUILDERS (shared between inner & outer wall)
# ---------------------------------------------------------------------------
def single_solid(shape):
    """Return the single Solid from a boolean result, asserting it stayed one
    connected manifold body. Used to keep each tube a clean solid."""
    if isinstance(shape, Solid):
        return shape
    if isinstance(shape, (list, ShapeList)):
        sols = [s for s in shape if isinstance(s, Solid)]
        if len(sols) == 1:
            return sols[0]
        return Compound(sols)
    # Compound -> grab its solids
    sols = shape.solids()
    if len(sols) == 1:
        return sols[0]
    return shape


print("Cutting glass slots...")
half_w = slot_width / 2.0                       # 5.25
slot_bottom_z = Z_TOP - slot_depth              # 67.5
r_in = housing_inner_r - 5
r_out = mesh_outer_r + 5
slot_radial_depth = r_out - r_in
straight_top = Z_TOP
straight_bot = slot_bottom_z + half_w           # bottom of straight section
box_h = straight_top - straight_bot

slot_cutters = []
for slot_center in slot_positions:
    slot_box = Box(slot_radial_depth, slot_width, box_h + 0.01,
                   align=(Align.CENTER, Align.CENTER, Align.CENTER))
    slot_box = slot_box.locate(Pos((r_in + r_out) / 2, 0,
                                   (straight_top + straight_bot) / 2))
    # rounded bottom = horizontal cylinder, axis radial (along X)
    round_cyl = Solid.make_cylinder(half_w, slot_radial_depth)
    round_cyl = round_cyl.rotate(Axis.Y, 90)
    round_cyl = round_cyl.locate(Pos((r_in + r_out) / 2 - slot_radial_depth / 2,
                                     0, straight_bot))
    cutter = slot_box.fuse(round_cyl)
    cutter = single_solid(cutter).rotate(Axis.Z, slot_center)
    slot_cutters.append(cutter)


# ---- perforation cutters (outer wall only) -------------------------------
perf_len = 2 * (mesh_outer_r + 2)


def in_a_slot(ang, z):
    z_from_top = Z_TOP - z
    if z_from_top < 0 or z_from_top > slot_depth + 0.5:
        return False
    for sc in slot_positions:
        d = abs(ang - sc)
        if d > 180:
            d = 360 - d
        if d <= slot_arc_half_deg + 1.5:
            return True
    return False


def near_ring(z):
    for _, h_z in ring_screw_sets:
        if abs(z - h_z) < (ring_screw_hole_r + perf_hole_r + 0.5):
            return True
    return False


perf_cutters = []
for ang, z in perf_holes:
    if in_a_slot(ang, z):
        continue
    if near_ring(z):
        continue
    c = Solid.make_cylinder(perf_hole_r, perf_len)
    c = c.rotate(Axis.Y, 90)
    c = c.locate(Pos(-perf_len / 2, 0, z))
    c = c.rotate(Axis.Z, ang)
    perf_cutters.append(c)
perf_count = len(perf_cutters)


# ---- M6 radial cutters (both walls) --------------------------------------
m6_cutters = []
for angs, z in ring_screw_sets:
    for ang in angs:
        m6_cutters.append(radial_hole(ang, z, ring_screw_hole_r))
m6_count = len(m6_cutters)


# ---- functional radial cutters (inner wall) ------------------------------
func_specs = [
    (wire_hole_angle, wire_top_z, wire_hole_diameter / 2),
    (wire_hole_angle, wire_bot_z, wire_hole_diameter / 2),
    (tc_cable_hole_angle, tc_cable_hole_z, 5.0),
]
func_cutters = [radial_hole(a, z, r) for a, z, r in func_specs]
func_count = len(func_cutters)


def cut_many(solid, cutters, chunk=30, label=""):
    """Cut a list of tool cutters out of one Solid, in chunks, keeping the result
    a single clean Solid. Tools in a chunk are grouped as a Compound (NOT fused —
    the cutters are disjoint, so a boolean union would yield a null shape); OCC's
    cut handles a Compound tool removing all of them at once."""
    out = solid
    for i in range(0, len(cutters), chunk):
        grp = cutters[i:i + chunk]
        tool = grp[0] if len(grp) == 1 else Compound(list(grp))
        out = single_solid(out.cut(tool))
        if label:
            print(f"  {label} chunk {i//chunk + 1}/"
                  f"{(len(cutters)+chunk-1)//chunk} done")
    return out


# ===========================================================================
# 2. INNER TUBE solid: slots + M6 + wire/tc holes
# ===========================================================================
print("Machining INNER tube...")
inner_solid = inner_wall
inner_solid = cut_many(inner_solid, slot_cutters, label="inner-slot")
inner_solid = cut_many(inner_solid, m6_cutters, label="inner-M6")
inner_solid = cut_many(inner_solid, func_cutters, label="inner-func")
inner_solid = single_solid(inner_solid)
print(f"  inner tube volume {inner_solid.volume:.1f} mm^3")

# ===========================================================================
# 3. OUTER TUBE solid: slots + perforations + M6
# ===========================================================================
print("Machining OUTER tube...")
outer_solid = outer_wall
outer_solid = cut_many(outer_solid, slot_cutters, label="outer-slot")
outer_solid = cut_many(outer_solid, perf_cutters, chunk=30, label="outer-perf")
outer_solid = cut_many(outer_solid, m6_cutters, label="outer-M6")
outer_solid = single_solid(outer_solid)
print(f"  outer tube volume {outer_solid.volume:.1f} mm^3")

# ===========================================================================
# 4. SUPPORT RING solid: 3 vertical leg bolt holes through the lip
# ===========================================================================
print("Machining SUPPORT RING...")
leg_cutters = []
for ang in leg_angles:
    leg_cutters.append(vertical_hole(ang, leg_hole_r, bolt_hole_size / 2,
                                     lip_z + sheet_metal_thickness / 2,
                                     sheet_metal_thickness + 10))
leg_count = len(leg_cutters)
ring_solid = cut_many(support_ring, leg_cutters, label="ring-leg")
ring_solid = single_solid(ring_solid)
print(f"  support ring volume {ring_solid.volume:.1f} mm^3")

# ===========================================================================
# 5. Assemble final part = inner tube + outer tube + ring + fins
#    (kept as separate clean solids in one Compound — a valid multi-body STEP
#    for the twin-wall fabrication; each is its own manifold sheet-metal part)
# ===========================================================================
print("Assembling final part...")
all_solids = [inner_solid, outer_solid, ring_solid] + fins
body = Compound(all_solids)


# ===========================================================================
# Export
# ===========================================================================
out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "CAD Exports", "STEP")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "01_Base_Body.step")

print(f"Exporting -> {out_path}")
export_step(body, out_path)
print("Export done.")

print("\nBUILD SUMMARY")
print(f"  slots cut      : {len(slot_positions)}")
print(f"  perf holes cut : {perf_count}")
print(f"  M6 holes cut   : {m6_count}")
print(f"  func holes cut : {func_count}")
print(f"  leg holes cut  : {leg_count}")
print(f"  fins           : {len(fins)}")
print(f"  total volume   : {body.volume:.1f} mm^3")
