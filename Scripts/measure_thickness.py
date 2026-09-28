"""
measure_thickness.py — measure the REAL sheet thickness of every metal part STEP
and export a GLB of each for the thickness viewer.

Method: tessellate the STEP, sample points on its surface, cast a ray inward
along the surface normal, and take the distance to the opposite face. The
median of a few thousand samples is the sheet thickness (holes, edges and
bends only move the tails, not the median).

Run: ./.venv-cad/bin/python Scripts/measure_thickness.py
Out: viewer-thickness/glb/*.glb and viewer-thickness/parts.json
"""
import os, sys, json, time
import numpy as np
import trimesh
from build123d import import_step

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAB = os.path.join(PROJ, "CAD Exports", "FAB_PACKAGE_2026-09-09", "STEP")   # 0.8 mm inner parts, built 2026-09-09
TOSEND = os.path.join(PROJ, "Factory Files", "2026-08-24 Tianrun", "TO SEND")   # gitignored working dir
OUT = os.path.join(PROJ, "viewer-thickness")
GLB = os.path.join(OUT, "glb")
os.makedirs(GLB, exist_ok=True)

# (number, label, step path, inner/outer)
PARTS = [
    ("01", "Inner Wall Tube",          os.path.join(FAB, "01_Inner_Wall_Tube.step"), "inner"),
    ("02", "Outer Perforated Tube",    os.path.join(FAB, "02_Outer_Perforated_Tube.step"), "outer"),
    ("03", "Support Ring",             os.path.join(FAB, "03_Support_Ring.step"), "inner"),
    ("04", "Bottom Cap",               os.path.join(FAB, "04_Bottom_Cap.step"), "outer"),
    ("05", "Cap Shell (top cap)",      os.path.join(FAB, "05_Cap_Shell.step"), "outer"),
    ("06", "Lid Inner Tube",           os.path.join(FAB, "06_Lid_Inner_Tube.step"), "inner"),
    ("07", "Lid Outer Perforated Tube",os.path.join(FAB, "07_Lid_Outer_Perforated_Tube.step"), "outer"),
    ("08", "Lid Top Disk",             os.path.join(FAB, "08_Lid_Top_Disk.step"), "outer"),
    ("09", "Lid Ceramic Holder",       os.path.join(FAB, "09_Lid_Ceramic_Holder.step"), "inner"),
    ("10", "Lid Handle",               os.path.join(FAB, "10_Lid_Handle.step"), "outer"),
    ("11", "Lid Hinge Strap",          os.path.join(FAB, "11_Lid_Hinge_Strap.step"), "outer"),
    ("12", "Hold-Down Ring",           os.path.join(FAB, "12_Hold_Down_Ring.step"), "inner"),
    ("13", "Hinge Pin",                os.path.join(FAB, "13_Hinge_Pin.step"), "rod"),
    ("14", "Steel Tray",               os.path.join(FAB, "14_Steel_Tray.step"), "tray"),
]

def to_trimesh(shape):
    verts, tris = shape.tessellate(0.05, 0.3)
    v = np.array([[p.X, p.Y, p.Z] for p in verts])
    f = np.array(tris)
    return trimesh.Trimesh(v, f, process=True)

def thickness(mesh, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    pts, fidx = trimesh.sample.sample_surface(mesh, n, seed=seed)
    normals = mesh.face_normals[fidx]
    # step just inside the surface, shoot inward
    origins = pts - normals * 0.02
    dirs = -normals
    ray = trimesh.ray.ray_triangle.RayMeshIntersector(mesh)
    locs, ridx, _ = ray.intersects_location(origins, dirs, multiple_hits=False)
    d = np.linalg.norm(locs - origins[ridx], axis=1) + 0.02
    d = d[(d > 0.1) & (d < 20)]
    if len(d) == 0:
        return None
    return {
        "median": float(np.median(d)),
        "p10": float(np.percentile(d, 10)),
        "p90": float(np.percentile(d, 90)),
        "samples": int(len(d)),
    }

results = []
for no, label, path, kind in PARTS:
    t0 = time.time()
    if not os.path.exists(path):
        results.append({"no": no, "label": label, "error": "file missing", "path": path}); print(no, "MISSING", path); continue
    shape = import_step(path)
    mesh = to_trimesh(shape)
    # Export the GLB from the SAME trimesh we measure — build123d's export_gltf
    # writes unwelded vertices (~6x bigger) and GitHub Pages has to serve these.
    glb = os.path.join(GLB, f"{no}.glb")
    mesh.export(glb)
    bb = mesh.bounds
    size = (bb[1] - bb[0]).tolist()
    th = thickness(mesh)
    rec = {"no": no, "label": label, "kind": kind, "file": os.path.relpath(path, PROJ),
           "bbox_mm": [round(s, 2) for s in size], "thickness": th,
           "volume_mm3": round(float(mesh.volume), 1) if mesh.is_volume else None}
    results.append(rec)
    print(no, label, "t=", th and round(th["median"], 2), "bbox", [round(s, 1) for s in size], f"{time.time()-t0:.0f}s", flush=True)
    with open(os.path.join(OUT, "parts.json"), "w") as f:
        json.dump(results, f, indent=1)

print("DONE")
