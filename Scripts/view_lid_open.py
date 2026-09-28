"""
Complete unit with lid OPEN — uses shared config from assembly_config.py.
"""
import trimesh
import numpy as np
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assembly_config import (
    OUT_DIR, STEEL, CERAMIC, oven_rotation, pivot_after_rotation,
    lid_open_angle, hinge_angle,
    load_stl, add_base_parts, add_tray_conduit_controller,
    position_lid_disk, open_file
)

print(f"Hinge at {hinge_angle:.1f}° — hinge faces -X (left), controller at +X (right)")

scene = trimesh.Scene()

# ── Base oven parts (rotated) ─────────────────────────────────────
base_mesh = add_base_parts(scene)

# ── Lid (rotated open) ───────────────────────────────────────────
lid = load_stl("04_Lid_Assembly.stl", STEEL)
ceramic_disk = load_stl("07b_Ceramic_Lid_Disk.stl", CERAMIC)

if lid:
    lid.apply_transform(oven_rotation)

    if ceramic_disk:
        # Position disk: body flush with lid bottom, lip extends into chamber
        position_lid_disk(ceramic_disk)
        ceramic_disk.apply_transform(oven_rotation)

    # Rotate lid open around hinge pivot (Y-axis — flips up and back)
    lid_rotation = trimesh.transformations.rotation_matrix(-lid_open_angle, [0, 1, 0])

    lid.apply_translation(-pivot_after_rotation)
    lid.apply_transform(lid_rotation)
    lid.apply_translation(pivot_after_rotation)

    scene.add_geometry(lid, node_name="Lid (Open)")
    print(f"  Lid (Open at {np.degrees(lid_open_angle):.0f}°)")

    if ceramic_disk:
        ceramic_disk.apply_translation(-pivot_after_rotation)
        ceramic_disk.apply_transform(lid_rotation)
        ceramic_disk.apply_translation(pivot_after_rotation)
        scene.add_geometry(ceramic_disk, node_name="Ceramic Disk (in Lid)")
        print("  Ceramic Disk (in Lid)")

# ── Tray, conduit, controller ────────────────────────────────────
add_tray_conduit_controller(scene, base_mesh)

# ── Export and open ──────────────────────────────────────────────
out_path = os.path.join(OUT_DIR, "Assembly_LidOpen.glb")
scene.export(out_path, file_type='glb')
print(f"\nExported: {out_path} ({os.path.getsize(out_path)/1024:.0f} KB)")
open_file(out_path)
print("Opened — lid OPEN, hinge faces LEFT")
