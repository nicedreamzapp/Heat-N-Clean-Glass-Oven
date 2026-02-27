"""
Complete unit with lid CLOSED — uses shared config from assembly_config.py.
"""
import trimesh
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assembly_config import (
    OUT_DIR, STEEL, CERAMIC, oven_rotation, hinge_angle,
    load_stl, add_base_parts, add_tray_conduit_controller,
    position_lid_disk, open_file
)

print(f"Hinge at {hinge_angle:.1f}° — hinge faces -X (left), controller at +X (right)")

scene = trimesh.Scene()

# ── Base oven parts (rotated) ─────────────────────────────────────
base_mesh = add_base_parts(scene)

# ── Lid + ceramic disk (closed, on top) ──────────────────────────
lid = load_stl("04_Lid_Assembly.stl", STEEL)
if lid:
    lid.apply_transform(oven_rotation)
    scene.add_geometry(lid, node_name="Lid (Closed)")
    print("  Lid (Closed)")

ceramic_disk = load_stl("07b_Ceramic_Lid_Disk.stl", CERAMIC)
if ceramic_disk:
    # Position disk: body flush with lid bottom, lip extends into chamber
    position_lid_disk(ceramic_disk)
    ceramic_disk.apply_transform(oven_rotation)
    scene.add_geometry(ceramic_disk, node_name="Ceramic Lid Disk")
    print("  Ceramic Lid Disk")

# ── Tray, conduit, controller ────────────────────────────────────
add_tray_conduit_controller(scene, base_mesh)

# ── Export and open ──────────────────────────────────────────────
out_path = os.path.join(OUT_DIR, "Assembly_LidClosed.glb")
scene.export(out_path, file_type='glb')
print(f"\nExported: {out_path} ({os.path.getsize(out_path)/1024:.0f} KB)")
open_file(out_path)
print("Opened — lid CLOSED, hinge faces LEFT")
