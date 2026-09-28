"""
See-through view of bottom assembly: bottom cap, tray, ceramic feet, leg screws.
Shows how the M6 bolts go through the layers and where the nuts are.

Run: python view_bottom_assembly.py
"""
import trimesh
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assembly_config import STL_DIR, OUT_DIR, open_file

def load_stl(fname, color):
    fpath = os.path.join(STL_DIR, fname)
    if not os.path.exists(fpath) or os.path.getsize(fpath) == 0:
        print(f"  MISSING: {fname}")
        return None
    m = trimesh.load(fpath)
    m.visual.face_colors = color
    print(f"  {fname}: {len(m.faces)} faces")
    return m

print("=" * 60)
print("BOTTOM ASSEMBLY — see-through view")
print("=" * 60)

# Semi-transparent so you can see the bolts inside
bottom_cap  = load_stl("02_Bottom_Cap.stl",  [220, 160, 60, 120])    # Gold, transparent
tray        = load_stl("12_Steel_Tray.stl",  [140, 145, 150, 120])   # Gray, transparent
feet        = load_stl("10_Ceramic_Feet.stl", [255, 250, 240, 150])   # White, semi-transparent
leg_screws  = load_stl("14_Leg_Screws.stl",  [255, 60, 60, 255])     # RED, fully opaque so they stand out

scene = trimesh.Scene()

if tray:
    scene.add_geometry(tray, node_name="Steel Tray")
if bottom_cap:
    scene.add_geometry(bottom_cap, node_name="Bottom Cap")
if feet:
    scene.add_geometry(feet, node_name="Ceramic Feet")
if leg_screws:
    scene.add_geometry(leg_screws, node_name="Leg Screws (M6)")

out_path = os.path.join(OUT_DIR, "Bottom_Assembly_SeeThrough.glb")
scene.export(out_path, file_type='glb')
print(f"\nExported: {out_path} ({os.path.getsize(out_path)/1024:.0f} KB)")
print()
print("GOLD (transparent)  = Bottom Cap")
print("GRAY (transparent)  = Steel Tray")
print("WHITE               = Ceramic Feet")
print("RED                 = M6 Bolts, Washers, Nuts")
print()
print("CURRENT PROBLEM: Bolt head is INSIDE the chamber (on top of")
print("bottom cap). No room to reach in and hold it while tightening.")
print("Bolt goes: head(inside) -> bottom cap -> foot -> tray -> washer -> nut(below)")
open_file(out_path)
