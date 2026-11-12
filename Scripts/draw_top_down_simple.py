"""Simple top-down drawing of the oven wall, Matt's preferred style (2026-11-12): concentric rings, each layer's
measurement written INSIDE its ring, no side labels, no grooves, no arrows. Thin layers are drawn wider than true
scale so their text fits; the numbers are the real ones from FAB_PACKAGE_2026-11-12 (hnc_params).
Run: .venv-cad/bin/python Scripts/draw_top_down_simple.py   ->  Renders/top_down_simple_2026-11-12.png
"""
import os, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hnc_params as HP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cer_in, cer_out = 81.5 / 2, HP.ceramic_outer_r                        # chamber Ø81.5, ceramic OD 92.5
ins_out = HP.housing_inner_r                                         # inner tube ID / 2
in_out = HP.housing_outer_r                                          # inner tube OD / 2
gap_out = HP.mesh_inner_r                                            # outer tube ID / 2
out_out = gap_out + 1.2                                              # outer tube OD / 2 (1.2 sheet)
cap_out = HP.top_cap_edge_r                                          # 05 ring edge
f1 = lambda v: f"{v:.1f}"
LAYERS = [  # label, real thickness, drawn width (display units), colour, font size
    ("Ceramic", cer_out - cer_in, 48, "#e8dbc3", 18),
    ("Insulation", ins_out - cer_out, 118, "#f6e6b7", 22),
    ("Inner wall", in_out - ins_out, 38, "#9ba5b0", 18),
    ("Air gap", gap_out - in_out, 48, "#dff0fa", 18),
    ("Outer wall", out_out - gap_out, 38, "#9ba5b0", 18),
    ("Cap lip", cap_out - out_out, 38, "#d0d6de", 18),
]
fig = plt.figure(figsize=(10.4, 10.4), dpi=100); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
R = 170                                   # drawn chamber radius
radii = [R]
for _, _, w, _, _ in LAYERS: radii.append(radii[-1] + w)
for i in range(len(LAYERS) - 1, -1, -1):
    ax.add_patch(Circle((0, 0), radii[i + 1], fc=LAYERS[i][3], ec="#222", lw=1.3))
ax.add_patch(Circle((0, 0), R, fc="white", ec="#222", lw=1.3))
ax.text(0, 0, f"Chamber\n{f1(2 * cer_in)}", ha="center", va="center", fontsize=28, weight="bold", linespacing=1.15)
for i, (lab, t, w, c, fs) in enumerate(LAYERS):
    ax.text(0, (radii[i] + radii[i + 1]) / 2, f"{lab}  {f1(t)}", ha="center", va="center", fontsize=fs, weight="bold")
lim = radii[-1] + 6; ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
out = os.path.join(ROOT, "Renders", "top_down_simple_2026-11-12.png")
fig.savefig(out, dpi=100, facecolor="white"); print(out, [round(t, 2) for _, t, *_ in LAYERS])
