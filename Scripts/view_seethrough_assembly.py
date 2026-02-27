"""
Full assembly — all parts see-through using PBR materials with alpha blend.
Lets you see through every part to the internals.

Run: python view_seethrough_assembly.py
"""
import trimesh
from trimesh.visual.material import PBRMaterial
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assembly_config import STL_DIR, OUT_DIR, open_file, oven_rotation

def load_stl_transparent(fname, rgb, alpha=0.15):
    """Load STL and apply a PBR material with proper alpha blending."""
    fpath = os.path.join(STL_DIR, fname)
    if not os.path.exists(fpath) or os.path.getsize(fpath) == 0:
        print(f"  MISSING: {fname}")
        return None
    m = trimesh.load(fpath)
    # Normalize RGB to 0-1 range
    r, g, b = rgb[0]/255, rgb[1]/255, rgb[2]/255
    mat = PBRMaterial(
        baseColorFactor=[r, g, b, alpha],
        alphaMode='BLEND',
        metallicFactor=0.3,
        roughnessFactor=0.6,
        doubleSided=True,
    )
    m.visual = trimesh.visual.TextureVisuals(material=mat)
    print(f"  {fname}: {len(m.faces)} faces (alpha={alpha})")
    return m

print("=" * 60)
print("FULL ASSEMBLY — all parts see-through")
print("=" * 60)

scene = trimesh.Scene()

# Oven body parts — need oven_rotation so hinge faces side
rotated_parts = [
    ("01_Base_Body.stl",         [180, 190, 200], 0.25, "Base Body"),
    ("02_Bottom_Cap.stl",        [220, 160, 60],  0.30, "Bottom Cap"),
    ("03_Top_Cap.stl",           [80, 200, 80],   0.30, "Top Cap"),
    ("04_Lid_Assembly.stl",      [80, 160, 220],  0.25, "Lid Assembly"),
    ("05_Hinge_Pin.stl",         [180, 185, 190], 0.30, "Hinge Pin"),
    ("06_Ceramic_Cylinder.stl",  [255, 250, 240], 0.20, "Ceramic Cylinder"),
    ("07_Ceramic_Base_Disk.stl", [255, 250, 240], 0.20, "Ceramic Base Disk"),
    ("08_Kanthal_Coil.stl",      [255, 140, 0],   0.30, "Kanthal Coil"),
    ("09_Thermocouple.stl",      [100, 200, 100], 0.30, "Thermocouple"),
    ("10_Ceramic_Feet.stl",      [240, 235, 225], 0.30, "Ceramic Feet"),
    ("14_Leg_Screws.stl",        [255, 40, 40],   0.30, "Leg Screws (M6)"),
    ("15_Cap_Screws.stl",        [255, 40, 40],   0.30, "Cap Screws (M4)"),
]

# Tray, conduit, controller — already positioned, no rotation
static_parts = [
    ("12_Steel_Tray.stl",       [165, 170, 175], 0.30, "Steel Tray"),
    ("13_Wiring_Conduit.stl",    [60, 60, 65],    0.30, "Wiring Conduit"),
    ("11_Controller_Box.stl",    [185, 190, 195], 0.30, "Controller Box"),
]

for fname, rgb, alpha, label in rotated_parts:
    m = load_stl_transparent(fname, rgb, alpha)
    if m:
        m.apply_transform(oven_rotation)
        scene.add_geometry(m, node_name=label)

for fname, rgb, alpha, label in static_parts:
    m = load_stl_transparent(fname, rgb, alpha)
    if m:
        scene.add_geometry(m, node_name=label)

out_path = os.path.join(OUT_DIR, "SeeThrough_Assembly.glb")
scene.export(out_path, file_type='glb')
print(f"\nExported: {out_path} ({os.path.getsize(out_path)/1024:.0f} KB)")
print()
print("All parts SEE-THROUGH (PBR alpha blend)")
open_file(out_path)
