"""
Single source of truth for assembly view parameters.
Both view_lid_open.py and view_lid_off.py import from here.
Change values HERE — they propagate to all views automatically.
"""
import trimesh
import numpy as np
import os
import math

# ── Paths ─────────────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL_DIR = os.path.join(PROJECT_DIR, "CAD Exports", "Individual Parts", "STL")
OUT_DIR = os.path.join(PROJECT_DIR, "CAD Exports")

# ── Ceramic / housing dimensions ──────────────────────────────────
outer_diameter = 92.5
inner_diameter = 81.5
disk_thickness = 5.5
cylinder_height = 91

ceramic_outer_r = outer_diameter / 2
sheet_metal_thickness = 1.2
insulation_gap = 24.6
housing_inner_r = ceramic_outer_r + insulation_gap
housing_outer_r = housing_inner_r + sheet_metal_thickness
air_gap = 4
mesh_inner_r = housing_outer_r + air_gap
mesh_outer_r = mesh_inner_r + sheet_metal_thickness

# ── Lid dimensions ────────────────────────────────────────────────
housing_top_z = cylinder_height  # 91
lid_bottom_z = housing_top_z
lid_height = 35
disk_body_h = 4.5
disk_lip_h = 1.0
lid_wall_height = disk_body_h - sheet_metal_thickness  # 3.3mm
lid_shelf_z = lid_bottom_z + sheet_metal_thickness + lid_wall_height

# ── Hinge angle calculation ───────────────────────────────────────
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
slot_4_end_angle = slot_positions[3] + slot_arc_half_deg
large_gap_arc_deg = gaps[3] * scale_factor / circumference * 360
hinge_angle = slot_4_end_angle + large_gap_arc_deg / 2
if hinge_angle >= 360:
    hinge_angle -= 360
hinge_angle_rad = np.radians(hinge_angle)

# ── Hinge geometry ────────────────────────────────────────────────
hinge_depth = 12
pivot_r = mesh_outer_r + hinge_depth

# ── Oven rotation (hinge faces -X, controller at +X) ─────────────
rotate_angle = np.radians(180 - hinge_angle)
oven_rotation = trimesh.transformations.rotation_matrix(rotate_angle, [0, 0, 1])

# After rotation, hinge pivot is at -X
pivot_after_rotation = np.array([-pivot_r, 0, housing_top_z])

# ── Lid open angle ────────────────────────────────────────────────
lid_open_angle = np.radians(95)  # flips up and back, back faces side

# ── Colors ────────────────────────────────────────────────────────
STEEL       = [195, 200, 205, 255]
CERAMIC     = [255, 250, 240, 255]
HINGE_PIN   = [180, 185, 190, 255]
COIL        = [255, 140, 0,   255]
THERMOCOUPLE = [100, 200, 100, 255]
FEET        = [240, 235, 225, 255]
SCREW_DARK  = [60,  60,  65,  255]
TRAY        = [165, 170, 175, 255]
CTRL_BOX    = [185, 190, 195, 255]
CONDUIT     = [60,  60,  65,  255]

# ── Part lists ────────────────────────────────────────────────────
# Base oven parts (no lid, no lid disk)
BASE_PARTS = [
    ("01_Base_Body.stl",        STEEL,          "Base Body"),
    ("02_Bottom_Cap.stl",       STEEL,          "Bottom Cap"),
    ("03_Top_Cap.stl",          STEEL,          "Top Cap"),
    ("05_Hinge_Pin.stl",        HINGE_PIN,      "Hinge Pin"),
    ("06_Ceramic_Cylinder.stl", CERAMIC,        "Ceramic Cylinder"),
    ("07_Ceramic_Base_Disk.stl", CERAMIC,       "Ceramic Base Disk"),
    ("08_Kanthal_Coil.stl",     COIL,           "Kanthal Coil"),
    ("09_Thermocouple.stl",     THERMOCOUPLE,   "Thermocouple"),
    ("10_Ceramic_Feet.stl",     FEET,           "Ceramic Feet"),
    ("14_Leg_Screws.stl",       SCREW_DARK,     "Leg Screws (M6)"),
    ("15_Cap_Screws.stl",       SCREW_DARK,     "Cap Screws (M4)"),
]

# ── Helper functions ──────────────────────────────────────────────
def load_stl(fname, color):
    """Load an STL file and apply color."""
    fpath = os.path.join(STL_DIR, fname)
    if not os.path.exists(fpath) or os.path.getsize(fpath) == 0:
        print(f"  MISSING: {fname}")
        return None
    m = trimesh.load(fpath)
    m.visual.face_colors = color
    return m


def add_base_parts(scene):
    """Add all base oven parts (rotated) to the scene. Returns base_mesh."""
    base_mesh = None
    for fname, color, label in BASE_PARTS:
        m = load_stl(fname, color)
        if m:
            m.apply_transform(oven_rotation)
            scene.add_geometry(m, node_name=label)
            print(f"  {label}")
            if "Base" in label and "Body" in label:
                base_mesh = m
    return base_mesh


def add_tray_conduit_controller(scene, base_mesh):
    """Add tray, conduit, and controller box to scene."""
    tray = load_stl("12_Steel_Tray.stl", TRAY)
    if tray:
        scene.add_geometry(tray, node_name="Steel Tray")
        print("  Steel Tray")

    conduit = load_stl("13_Wiring_Conduit.stl", CONDUIT)
    if conduit:
        scene.add_geometry(conduit, node_name="Wiring Conduit")
        print("  Wiring Conduit")

    ctrl = load_stl("11_Controller_Box.stl", CTRL_BOX)
    if ctrl and base_mesh and tray:
        bb = base_mesh.bounds
        tb = tray.bounds
        cb = ctrl.bounds
        cs = cb[1] - cb[0]
        cc = (cb[0] + cb[1]) / 2
        ctrl.apply_translation([
            bb[1][0] + 35 + cs[0]/2 - cc[0],
            -cc[1],
            tb[1][2] + cs[2]/2 - cc[2]
        ])
        scene.add_geometry(ctrl, node_name="Controller Box")
        print("  Controller Box")


def position_lid_disk(ceramic_disk):
    """Flip and position ceramic lid disk so body is flush with lid bottom,
    lip extends 1mm down into the chamber."""
    # Exported STL has disk at z=0 with lip facing UP
    # Flip so lip faces DOWN
    flip = trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])
    ceramic_disk.apply_transform(flip)
    # After flip: body from z=-4.5 to z=0, lip from z=-5.5 to z=-4.5
    # Translate so body bottom is flush with lid bottom (z=91)
    # body: 91 to 95.5, lip: 90 to 91 (1mm into chamber)
    ceramic_disk.apply_translation([0, 0, lid_bottom_z + disk_body_h])
    return ceramic_disk


def open_file(path):
    """Open a file with the system default viewer."""
    import sys
    if sys.platform == 'win32':
        os.startfile(path)
    else:
        import subprocess
        subprocess.Popen(["open", path])
