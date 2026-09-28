"""
EXPLODED VIEW - All parts spaced vertically to show assembly order.
Exports a single GLB with every piece visible and separated.
"""
import trimesh
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
stl_dir = os.path.join(project_dir, "CAD Exports", "Individual Parts", "STL")
glb_dir = os.path.join(project_dir, "CAD Exports", "Individual Parts", "GLB")
out_path = os.path.join(project_dir, "CAD Exports", "Exploded_Assembly.glb")

# Oven rotation (hinge at -X) - same calc as assembly_config
import math
outer_diameter = 92.5
slot_width = 10.5
gaps = [46.25, 46.25, 46.25, 108.68]
circumference = math.pi * outer_diameter
scale_factor = circumference / (sum(gaps) + 4 * slot_width)
slot_positions = []
current_arc_position = 0
for i in range(4):
    center_arc = current_arc_position + (slot_width * scale_factor) / 2
    angle = (center_arc / circumference) * 360
    slot_positions.append(angle)
    current_arc_position += (slot_width + gaps[i]) * scale_factor
slot_arc_half_deg = (slot_width * scale_factor / 2 / circumference * 360)
slot_4_end = slot_positions[3] + slot_arc_half_deg
large_gap_arc = gaps[3] * scale_factor / circumference * 360
hinge_angle = slot_4_end + large_gap_arc / 2
if hinge_angle >= 360:
    hinge_angle -= 360
rotate_angle = np.radians(180 - hinge_angle)
oven_rot = trimesh.transformations.rotation_matrix(rotate_angle, [0, 0, 1])

# Parts in assembly order (bottom to top) with Z offsets for spacing
# (filename, color, label, is_oven_part, extra_z_shift)
GAP = 35  # mm gap between exploded layers

parts_order = [
    ("12_Steel_Tray.stl",              [165, 170, 175, 255], "Steel Tray",              False, 0),
    ("14_Leg_Screws.stl",              [60, 60, 65, 255],    "Leg Screws",              True,  GAP * 1),
    ("10_Ceramic_Feet.stl",            [240, 235, 225, 255], "Ceramic Feet",            True,  GAP * 2),
    ("02_Bottom_Cap.stl",              [220, 180, 140, 255], "Bottom Cap",              True,  GAP * 3),
    ("01_Base_Body.stl",               [195, 200, 205, 255], "Base Body",               True,  GAP * 4),
    ("07_Ceramic_Base_Disk.stl",       [255, 250, 240, 255], "Ceramic Base Disk",       True,  GAP * 5),
    ("06_Ceramic_Cylinder.stl",        [255, 250, 240, 255], "Ceramic Cylinder",        True,  GAP * 6),
    ("08_Kanthal_Coil.stl",            [255, 140, 0, 255],   "Kanthal Coil",            True,  GAP * 7),
    ("09_Thermocouple.stl",            [100, 200, 100, 255], "Thermocouple",            True,  GAP * 8),
    ("03A_Top_Cap_Outer_Ring.stl",     [180, 220, 140, 255], "Top Cap Outer Ring (A)",  True,  GAP * 9),
    ("03B_Top_Cap_Inner_Collar.stl",   [160, 210, 170, 255], "Top Cap Inner Collar (B)",True,  GAP * 10),
    ("15_Cap_Screws.stl",              [60, 60, 65, 255],    "Cap Screws",              True,  GAP * 11),
    ("05_Hinge_Pin.stl",               [180, 185, 190, 255], "Hinge Pin",               True,  GAP * 12),
    ("04_Lid_Assembly.stl",            [140, 180, 220, 255], "Lid Assembly",            True,  GAP * 13),
    ("07b_Ceramic_Lid_Disk.stl",       [255, 250, 240, 255], "Ceramic Lid Disk",        True,  GAP * 14),
]

scene = trimesh.Scene()
print("Building exploded view...")

for fname, color, label, is_oven, z_shift in parts_order:
    fpath = os.path.join(stl_dir, fname)
    if not os.path.exists(fpath):
        print(f"  SKIP (missing): {fname}")
        continue
    m = trimesh.load(fpath)
    m.visual.face_colors = color
    if is_oven:
        m.apply_transform(oven_rot)
    m.apply_translation([0, 0, z_shift])
    scene.add_geometry(m, node_name=label)
    print(f"  {label}: Z+{z_shift}mm")

# Also add controller + conduit (not shifted, they sit beside the oven)
for fname, color, label in [
    ("11_Controller_Box.stl", [185, 190, 195, 255], "Controller Box"),
    ("13_Wiring_Conduit.stl", [60, 60, 65, 255], "Wiring Conduit"),
]:
    fpath = os.path.join(stl_dir, fname)
    if os.path.exists(fpath):
        m = trimesh.load(fpath)
        m.visual.face_colors = color
        scene.add_geometry(m, node_name=label)
        print(f"  {label}: no shift (beside oven)")

scene.export(out_path, file_type='glb')
print(f"\nExported: {out_path}")
print(f"  Size: {os.path.getsize(out_path) / 1024:.0f} KB")
