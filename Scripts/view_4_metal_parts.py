"""
The 4 main metal parts side by side:
  1. Bottom Cap
  2. Chamber (base body)
  3. Top Cap
  4. Lid

Run: python view_4_metal_parts.py
"""
import trimesh
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assembly_config import STL_DIR, OUT_DIR, open_file

def load_stl(fname):
    fpath = os.path.join(STL_DIR, fname)
    if not os.path.exists(fpath) or os.path.getsize(fpath) == 0:
        print(f"  MISSING: {fname}")
        return None
    m = trimesh.load(fpath)
    print(f"  {fname}: {len(m.faces)} faces")
    return m

print("=" * 60)
print("4 MAIN METAL PARTS — side by side")
print("=" * 60)

bottom_cap = load_stl("02_Bottom_Cap.stl")
chamber = load_stl("01_Base_Body.stl")
top_cap = load_stl("03_Top_Cap.stl")
lid = load_stl("04_Lid_Assembly.stl")

# Color each part differently
if bottom_cap:
    bottom_cap.visual.face_colors = [220, 160, 60, 255]   # Gold
if chamber:
    chamber.visual.face_colors = [180, 190, 200, 255]      # Steel gray
if top_cap:
    top_cap.visual.face_colors = [80, 200, 80, 255]        # Green
if lid:
    lid.visual.face_colors = [80, 160, 220, 255]           # Blue

scene = trimesh.Scene()
spacing = 200  # mm between each part

# Center them all at roughly the same Z
parts = [
    (bottom_cap, -spacing * 1.5, "1. Bottom Cap"),
    (chamber,    -spacing * 0.5, "2. Chamber (base body)"),
    (top_cap,     spacing * 0.5, "3. Top Cap"),
    (lid,         spacing * 1.5, "4. Lid"),
]

for mesh, x_offset, label in parts:
    if mesh:
        copy = mesh.copy()
        copy.apply_translation([x_offset, 0, 0])
        scene.add_geometry(copy, node_name=label)

out_path = os.path.join(OUT_DIR, "4_Metal_Parts.glb")
scene.export(out_path, file_type='glb')
print(f"\nExported: {out_path} ({os.path.getsize(out_path)/1024:.0f} KB)")
print()
print("Left to right:")
print("  1. GOLD   = Bottom Cap")
print("  2. GRAY   = Chamber (base body)")
print("  3. GREEN  = Top Cap")
print("  4. BLUE   = Lid")
open_file(out_path)
