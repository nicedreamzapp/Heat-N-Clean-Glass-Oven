"""
View the 4 main metal parts in 3D.

Just run:  python3 view_parts.py

Opens 4_Metal_Parts.glb in your default 3D viewer.
If you don't have one, drag the .glb file into https://gltf-viewer.donmccurdy.com
"""
import os
import sys
import subprocess

glb = os.path.join(os.path.dirname(os.path.abspath(__file__)), "4_Metal_Parts.glb")

if not os.path.exists(glb):
    print(f"ERROR: {glb} not found")
    sys.exit(1)

print("Opening 4_Metal_Parts.glb ...")
print()
print("  GOLD       = Bottom Cap")
print("  GRAY       = Chamber (base body)")
print("  GREEN      = Top Cap")
print("  BLUE       = Lid")
print("  DARK STEEL = Screws (M6 leg + M4 cap)")
print()
print("Tip: If nothing opens, drag 4_Metal_Parts.glb into https://gltf-viewer.donmccurdy.com")

if sys.platform == 'darwin':
    subprocess.Popen(["open", glb])
elif sys.platform == 'win32':
    os.startfile(glb)
else:
    subprocess.Popen(["xdg-open", glb])
