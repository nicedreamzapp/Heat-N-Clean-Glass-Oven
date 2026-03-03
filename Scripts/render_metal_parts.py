"""
Render individual PNG images of each metal part for the Metal_Parts_Package.
Uses matplotlib headless (no display needed).

Run: python3 render_metal_parts.py
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assembly_config import STL_DIR

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "Metal_Parts_Package", "Part_Images")
os.makedirs(OUT_DIR, exist_ok=True)

# Parts to render: (stl_filename, output_name, color, title, elevation, azimuth)
PARTS = [
    ("01_Base_Body.stl",    "01_Chamber_Body",  "#B4BEC8", "Chamber Body (Inner Housing + Outer Mesh + Support Ring)", 25, -45),
    ("02_Bottom_Cap.stl",   "02_Bottom_Cap",    "#DCA03C", "Bottom Cap", 30, -50),
    ("03_Top_Cap.stl",      "03_Top_Cap",       "#50C850", "Top Cap (Outer Ring + Inner Collar)", 25, -45),
    ("04_Lid_Assembly.stl", "04_Lid_Assembly",   "#50A0DC", "Lid Assembly", 30, -60),
    ("14_Leg_Screws.stl",   "05_Leg_Screws_M6", "#3C3C41", "M6 Leg Screws (x3)", 25, -45),
    ("15_Cap_Screws.stl",   "06_Cap_Screws_M4", "#3C3C41", "M4 Cap Screws", 25, -45),
]


def decimate_mesh(mesh, max_faces=40000):
    """Reduce face count for rendering by taking every Nth face (preserves structure)."""
    if len(mesh.faces) <= max_faces:
        return mesh
    step = max(1, len(mesh.faces) // max_faces)
    indices = np.arange(0, len(mesh.faces), step)[:max_faces]
    return trimesh.Trimesh(vertices=mesh.vertices, faces=mesh.faces[indices])


def render_part(stl_file, out_name, color, title, elev, azim):
    """Load an STL and render it to a PNG with matplotlib."""
    fpath = os.path.join(STL_DIR, stl_file)
    if not os.path.exists(fpath):
        print(f"  MISSING: {stl_file}")
        return

    print(f"  Loading {stl_file}...", end=" ", flush=True)
    mesh = trimesh.load(fpath)
    print(f"{len(mesh.faces)} faces", end=" ", flush=True)

    # Decimate for rendering speed
    mesh = decimate_mesh(mesh)
    print(f"-> {len(mesh.faces)} rendered")

    verts = mesh.vertices
    faces = mesh.faces

    # Center the mesh
    center = (verts.max(axis=0) + verts.min(axis=0)) / 2
    verts = verts - center

    fig = plt.figure(figsize=(12, 9), facecolor='white')
    ax = fig.add_subplot(111, projection='3d', facecolor='white')

    # Build polygon collection
    triangles = verts[faces]
    poly = Poly3DCollection(triangles, alpha=0.85)
    poly.set_facecolor(color)
    poly.set_edgecolor(color)
    poly.set_linewidth(0.0)
    ax.add_collection3d(poly)

    # Set axis limits
    extent = verts.max() - verts.min()
    half = extent / 2 * 1.1
    ax.set_xlim(-half, half)
    ax.set_ylim(-half, half)
    ax.set_zlim(-half, half)

    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.view_init(elev=elev, azim=azim)

    # Clean up axes
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('lightgray')
    ax.yaxis.pane.set_edgecolor('lightgray')
    ax.zaxis.pane.set_edgecolor('lightgray')
    ax.grid(True, alpha=0.3)

    out_path = os.path.join(OUT_DIR, f"{out_name}.png")
    fig.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"    -> {out_path} ({os.path.getsize(out_path) / 1024:.0f} KB)")


print("=" * 60)
print("RENDERING METAL PART IMAGES")
print("=" * 60)

for stl_file, out_name, color, title, elev, azim in PARTS:
    render_part(stl_file, out_name, color, title, elev, azim)

# Also render a combined overview
print("\n  Rendering combined overview...", flush=True)
fig = plt.figure(figsize=(16, 10), facecolor='white')
fig.suptitle("4 Main Metal Parts + Hardware", fontsize=16, fontweight='bold')

for i, (stl_file, out_name, color, title, elev, azim) in enumerate(PARTS[:4]):
    fpath = os.path.join(STL_DIR, stl_file)
    if not os.path.exists(fpath):
        continue
    mesh = trimesh.load(fpath)
    mesh = decimate_mesh(mesh, max_faces=30000)
    verts = mesh.vertices
    faces = mesh.faces
    center = (verts.max(axis=0) + verts.min(axis=0)) / 2
    verts = verts - center

    ax = fig.add_subplot(2, 2, i + 1, projection='3d', facecolor='white')
    triangles = verts[faces]
    poly = Poly3DCollection(triangles, alpha=0.85)
    poly.set_facecolor(color)
    poly.set_edgecolor(color)
    poly.set_linewidth(0.0)
    ax.add_collection3d(poly)

    extent = verts.max() - verts.min()
    half = extent / 2 * 1.1
    ax.set_xlim(-half, half)
    ax.set_ylim(-half, half)
    ax.set_zlim(-half, half)
    # Short title for subplot
    short_title = title.split("(")[0].strip()
    ax.set_title(short_title, fontsize=11, fontweight='bold')
    ax.view_init(elev=elev, azim=azim)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('lightgray')
    ax.yaxis.pane.set_edgecolor('lightgray')
    ax.zaxis.pane.set_edgecolor('lightgray')
    ax.grid(True, alpha=0.3)

out_path = os.path.join(OUT_DIR, "00_All_4_Parts_Overview.png")
fig.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"    -> {out_path} ({os.path.getsize(out_path) / 1024:.0f} KB)")

print("\nDone! Images saved to:", OUT_DIR)

# Open all images
import subprocess
for f in sorted(os.listdir(OUT_DIR)):
    if f.endswith('.png'):
        subprocess.Popen(["open", os.path.join(OUT_DIR, f)])
