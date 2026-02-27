"""
Top cap sitting on the ceramic cylinder — no chamber, nothing else.
Just these 2 parts so you can see how they fit together.

Run: python view_topcap_ceramic.py
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
print("TOP CAP + CERAMIC CYLINDER (nothing else)")
print("=" * 60)

top_cap = load_stl("03_Top_Cap.stl", [80, 200, 80, 200])       # Green, slightly transparent
ceramic = load_stl("06_Ceramic_Cylinder.stl", [255, 255, 255, 255])  # White

scene = trimesh.Scene()

if ceramic:
    scene.add_geometry(ceramic, node_name="Ceramic Cylinder")
if top_cap:
    scene.add_geometry(top_cap, node_name="Top Cap")

out_path = os.path.join(OUT_DIR, "TopCap_on_Ceramic.glb")
scene.export(out_path, file_type='glb')
print(f"\nExported: {out_path} ({os.path.getsize(out_path)/1024:.0f} KB)")
print()
print("GREEN = Top Cap")
print("WHITE = Ceramic Cylinder")
print()
print("The cap now has a 5mm retaining ridge on the outside of the")
print("ceramic cylinder to hold it in place from above.")
open_file(out_path)
