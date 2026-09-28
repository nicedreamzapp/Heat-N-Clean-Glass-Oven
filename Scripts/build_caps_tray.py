"""
Analytic STEP builder for fab-shop quote — TRUE solids (cylinders/planes/circular
holes), NOT meshes. Parts: 02_Bottom_Cap, 05_Hinge_Pin, 12_Steel_Tray (all 304SS).

Coordinate system is the WORLD frame from hnc_params.py so parts assemble with the
rest of the generator. Run with the project venv:
  .venv-cad/bin/python Scripts/build_caps_tray.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from hnc_params import *  # noqa: F401,F403

from build123d import (
    Pos, Rot, Axis, Plane, Location,
    Cylinder, Box, Compound,
    export_step, import_step,
)
from build123d import Vector

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PROJ, "CAD Exports", "STEP")
os.makedirs(OUT, exist_ok=True)

# extra length added to cutting cylinders so they fully pierce the wall
PIERCE = 4.0


# =============================================================================
# 02_Bottom_Cap  — flat disk + upward lip + drilled holes + radial M6 lip holes
# =============================================================================
def build_bottom_cap():
    leg_height_local = 25  # not needed for the cap, kept for clarity

    # --- flat disk -----------------------------------------------------------
    # disk spans z = [bottom_cap_z, bottom_cap_z + sheet_metal_thickness]
    # top face at bottom_cap_z + sheet_metal_thickness
    disk_z_lo = bottom_cap_z
    disk_z_top = bottom_cap_z + sheet_metal_thickness
    disk_zc = (disk_z_lo + disk_z_top) / 2.0
    disk = Cylinder(radius=bottom_cap_outer_r, height=sheet_metal_thickness)
    disk = Pos(0, 0, disk_zc) * disk

    # --- upward lip wrapping the outer tube ----------------------------------
    # wall thickness 1.2, height 16, outer radius 78.75, from disk top upward
    lip_inner_r = bottom_cap_outer_r - sheet_metal_thickness
    lip_z_lo = disk_z_top
    lip_zc = lip_z_lo + bottom_cap_lip_height / 2.0
    lip_outer = Cylinder(radius=bottom_cap_outer_r, height=bottom_cap_lip_height)
    lip_inner = Cylinder(radius=lip_inner_r, height=bottom_cap_lip_height + PIERCE)
    lip = lip_outer - lip_inner
    lip = Pos(0, 0, lip_zc) * lip

    # FUSE disk + lip BEFORE any cuts (avoids OCP boolean failures on cuts that
    # straddle the disk/lip junction)
    cap = disk + lip

    # --- drilled vertical holes in the disk ----------------------------------
    for h_ang, h_r_pos, h_radius in bottom_cap_holes:
        a = math.radians(h_ang)
        hx = h_r_pos * math.cos(a)
        hy = h_r_pos * math.sin(a)
        tool = Cylinder(radius=h_radius, height=sheet_metal_thickness + PIERCE)
        tool = Pos(hx, hy, disk_zc) * tool
        cap = cap - tool

    # --- radial M6 (Ø6.6) holes through the lip at the bottom ring (z=-24) ---
    # mirrors in_ring_screw_hole(): the bottom ring set at z=-24, angles =
    # ring_screw_angles, hole radius = ring_screw_hole_r (3.3).
    ring_z = -24.0
    lip_mid_r = bottom_cap_outer_r - sheet_metal_thickness / 2.0
    for ang in ring_screw_angles:
        a = math.radians(ang)
        # radial cutter: cylinder axis pointing outward along (cos,sin)
        tool = Cylinder(radius=ring_screw_hole_r,
                        height=sheet_metal_thickness + PIERCE)
        # align +Z -> radial direction, then place at the lip mid-radius
        tool = Rot(Z=ang) * Rot(Y=90) * tool          # axis now along +X, rotated to angle
        tool = Pos(lip_mid_r * math.cos(a),
                   lip_mid_r * math.sin(a),
                   ring_z) * tool
        cap = cap - tool

    return cap


# =============================================================================
# 05_Hinge_Pin  — Ø5 x 30 rod, tangent to the hinge circle at 292.4 deg
# =============================================================================
def build_hinge_pin():
    # Reproduce _tangent_cyl(2.5, 30, HINGE_T_OFF) from the generator.
    _ha = math.radians(HINGE_ANGLE_DEG)
    _htx, _hty = -math.sin(_ha), math.cos(_ha)      # tangent axis direction
    t_off = HINGE_T_OFF

    pin = Cylinder(radius=HINGE_PIN_R, height=HINGE_PIN_LEN)  # axis along +Z
    # align +Z -> tangent axis (_htx, _hty, 0)
    axis_dir = Vector(_htx, _hty, 0)
    z = Vector(0, 0, 1)
    rot_axis = z.cross(axis_dir)
    ang = math.degrees(math.acos(max(-1.0, min(1.0, z.dot(axis_dir)))))
    pin = Rot(Axis((0, 0, 0), rot_axis.to_tuple()), ang) * pin
    # translate to the pivot location
    cx = HINGE_PIVOT_R * math.cos(_ha) + _htx * t_off
    cy = HINGE_PIVOT_R * math.sin(_ha) + _hty * t_off
    cz = HINGE_PIVOT_Z
    pin = Pos(cx, cy, cz) * pin
    return pin


# =============================================================================
# 12_Steel_Tray  — 3mm flat plate + bent walls (top & bottom lips, 4 sides)
# =============================================================================
def build_steel_tray():
    leg_height = 25
    platform_z = housing_bottom_z - leg_height

    tray_left_edge = -mesh_outer_r - 25
    tray_right_edge = mesh_outer_r + 35 + 160 + 20
    tray_front_edge = -100 / 2 - 20
    tray_back_edge = 100 / 2 + 20

    platform_length = tray_right_edge - tray_left_edge
    platform_width = max(mesh_outer_r * 2 + 50, tray_back_edge - tray_front_edge)
    platform_thickness = 3
    lip_height_tray = 12
    lip_thickness = 2
    platform_center_x = (tray_left_edge + tray_right_edge) / 2

    parts = []

    # base plate (top face at platform_z, thickness downward)
    base = Box(platform_length, platform_width, platform_thickness)
    base = Pos(platform_center_x, 0, platform_z - platform_thickness / 2) * base
    parts.append(base)

    def wall(ex, ey, ez, cx, cy, cz):
        b = Box(ex, ey, ez)
        return Pos(cx, cy, cz) * b

    # TOP lips (rise above the plate)
    parts.append(wall(platform_length, lip_thickness, lip_height_tray,
                      platform_center_x, -platform_width / 2 + lip_thickness / 2,
                      platform_z + lip_height_tray / 2))
    parts.append(wall(platform_length, lip_thickness, lip_height_tray,
                      platform_center_x, platform_width / 2 - lip_thickness / 2,
                      platform_z + lip_height_tray / 2))
    parts.append(wall(lip_thickness, platform_width - lip_thickness * 2, lip_height_tray,
                      tray_left_edge + lip_thickness / 2, 0,
                      platform_z + lip_height_tray / 2))
    parts.append(wall(lip_thickness, platform_width - lip_thickness * 2, lip_height_tray,
                      tray_right_edge - lip_thickness / 2, 0,
                      platform_z + lip_height_tray / 2))

    # BOTTOM lips (hang below the plate)
    parts.append(wall(platform_length, lip_thickness, lip_height_tray,
                      platform_center_x, -platform_width / 2 + lip_thickness / 2,
                      platform_z - platform_thickness - lip_height_tray / 2))
    parts.append(wall(platform_length, lip_thickness, lip_height_tray,
                      platform_center_x, platform_width / 2 - lip_thickness / 2,
                      platform_z - platform_thickness - lip_height_tray / 2))
    parts.append(wall(lip_thickness, platform_width - lip_thickness * 2, lip_height_tray,
                      tray_left_edge + lip_thickness / 2, 0,
                      platform_z - platform_thickness - lip_height_tray / 2))
    parts.append(wall(lip_thickness, platform_width - lip_thickness * 2, lip_height_tray,
                      tray_right_edge - lip_thickness / 2, 0,
                      platform_z - platform_thickness - lip_height_tray / 2))

    # FUSE everything before cutting holes
    tray = parts[0]
    for p in parts[1:]:
        tray = tray + p

    # leg screw holes (M6 clearance) through the base plate
    screw_hole_radius = 3.3
    for angle_deg in leg_angles:
        a = math.radians(angle_deg)
        hx = leg_hole_r * math.cos(a)
        hy = leg_hole_r * math.sin(a)
        tool = Cylinder(radius=screw_hole_radius,
                        height=platform_thickness + PIERCE)
        tool = Pos(hx, hy, platform_z - platform_thickness / 2) * tool
        tray = tray - tool

    return tray


# =============================================================================
# Build, export, validate
# =============================================================================
def measure(label, path):
    s = import_step(path)
    solids = s.solids()
    vol = sum(so.volume for so in solids)
    bb = s.bounding_box()
    print(f"\n--- {label} ---")
    print(f"  file: {path}")
    print(f"  solids: {len(solids)}  total volume: {vol:.1f} mm^3")
    print(f"  bbox min: ({bb.min.X:.2f}, {bb.min.Y:.2f}, {bb.min.Z:.2f})")
    print(f"  bbox max: ({bb.max.X:.2f}, {bb.max.Y:.2f}, {bb.max.Z:.2f})")
    print(f"  bbox size: ({bb.size.X:.2f} x {bb.size.Y:.2f} x {bb.size.Z:.2f})")
    return bb, vol, len(solids)


def main():
    targets = [
        ("02_Bottom_Cap", build_bottom_cap),
        ("05_Hinge_Pin", build_hinge_pin),
        ("12_Steel_Tray", build_steel_tray),
    ]
    paths = {}
    for name, fn in targets:
        print(f"Building {name} ...")
        part = fn()
        p = os.path.join(OUT, f"{name}.step")
        export_step(part, p)
        paths[name] = p

    print("\n==================== VALIDATION ====================")
    bb_cap, _, _ = measure("02_Bottom_Cap", paths["02_Bottom_Cap"])
    print(f"  cap blank dia (XY): {bb_cap.size.X:.2f} x {bb_cap.size.Y:.2f} "
          f"(spec Ø{2*bottom_cap_outer_r:.1f})")
    print(f"  cap total Z height: {bb_cap.size.Z:.2f} "
          f"(disk 1.2 + lip {bottom_cap_lip_height})")

    bb_pin, _, _ = measure("05_Hinge_Pin", paths["05_Hinge_Pin"])
    # pin is at an angle in world space; report axial length via volume->len check
    import math as _m
    pin_vol = _m.pi * HINGE_PIN_R**2 * HINGE_PIN_LEN
    print(f"  pin spec: Ø{2*HINGE_PIN_R} x {HINGE_PIN_LEN}  "
          f"(ideal vol {pin_vol:.1f} mm^3)")

    bb_tray, _, _ = measure("12_Steel_Tray", paths["12_Steel_Tray"])
    print(f"  tray extents (XY): {bb_tray.size.X:.2f} x {bb_tray.size.Y:.2f}")
    print(f"  tray total Z (plate 3 + top/bot lips 12 each): {bb_tray.size.Z:.2f}")

    print("\nDONE.")
    for k, v in paths.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
