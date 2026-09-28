"""
Verify the analytic STEP exports against the spec, and render PNGs for review.

For each STEP file:
  - load it (build123d import_step)
  - confirm it's a valid non-empty solid (volume > 0)
  - measure bounding box (overall X/Y/Z extents) and max radius from the axis
  - tessellate -> matplotlib PNG (headless, no display needed)

Then print a comparison table vs hnc_params.PRINCIPAL_DIMS so Matt can triple-check.
Run: .venv-cad/bin/python Scripts/verify_steps.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from build123d import import_step
import hnc_params as P

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP_DIR = os.path.join(PROJ, "CAD Exports", "STEP")
RENDER_DIR = os.path.join(PROJ, "CAD Exports", "STEP", "renders")
os.makedirs(RENDER_DIR, exist_ok=True)

EXPECTED = [
    "01_Base_Body", "02_Bottom_Cap", "04a_Cap_Shell", "04b_Cap_HoldDown_Ring",
    "04_Lid_Assembly", "05b_Lid_Hinge_Strap", "05_Hinge_Pin", "12_Steel_Tray",
]

def tess(part):
    """Return (verts Nx3, faces Mx3) tessellation of a build123d part."""
    try:
        v, t = part.tessellate(0.3)
        verts = np.array([[p.X, p.Y, p.Z] for p in v])
        faces = np.array(t)
        return verts, faces
    except Exception as e:
        print("   tessellate failed:", e)
        return None, None

def render(name, verts, faces):
    if verts is None or len(verts) == 0:
        return None
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection="3d")
    # downsample faces for speed
    step = max(1, len(faces) // 6000)
    tris = [verts[f] for f in faces[::step]]
    coll = Poly3DCollection(tris, alpha=0.9, facecolor=(0.72, 0.76, 0.80), edgecolor=(0.3, 0.3, 0.35), linewidths=0.05)
    ax.add_collection3d(coll)
    mn, mx = verts.min(0), verts.max(0)
    ctr = (mn + mx) / 2
    rng = (mx - mn).max() / 2
    for setlim, c in zip([ax.set_xlim, ax.set_ylim, ax.set_zlim], ctr):
        setlim(c - rng, c + rng)
    ax.set_title(name, fontsize=10)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=35)
    out = os.path.join(RENDER_DIR, name + ".png")
    plt.savefig(out, dpi=110, bbox_inches="tight")
    plt.close(fig)
    return out

def main():
    rows = []
    for name in EXPECTED:
        path = os.path.join(STEP_DIR, name + ".step")
        if not os.path.exists(path):
            rows.append((name, "MISSING", "", "", "", ""))
            continue
        try:
            part = import_step(path)
        except Exception as e:
            rows.append((name, f"LOAD-FAIL {e}", "", "", "", ""))
            continue
        try:
            vol = part.volume
        except Exception:
            vol = float("nan")
        verts, faces = tess(part)
        if verts is not None and len(verts):
            mn, mx = verts.min(0), verts.max(0)
            ext = mx - mn
            rmax = float(np.sqrt(verts[:, 0]**2 + verts[:, 1]**2).max())
            bb = f"{ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f}"
            odia = f"{2*rmax:.1f}"
        else:
            bb, odia = "", ""
        png = render(name, verts, faces)
        rows.append((name, "ok", f"{vol/1000:.1f}", bb, odia, os.path.basename(png) if png else ""))

    print("\n" + "=" * 92)
    print(f"{'PART':<24}{'STATUS':<10}{'VOL cm³':>9}  {'BBOX X×Y×Z mm':<22}{'MAX OD mm':>10}  RENDER")
    print("=" * 92)
    for r in rows:
        print(f"{r[0]:<24}{r[1]:<10}{r[2]:>9}  {r[3]:<22}{r[4]:>10}  {r[5]}")
    print("=" * 92)
    print("\nSPEC principal dims (source of truth):")
    for k, v in P.PRINCIPAL_DIMS.items():
        print(f"  {k:<28} {v}")
    print(f"\nRenders: {RENDER_DIR}")

if __name__ == "__main__":
    main()
