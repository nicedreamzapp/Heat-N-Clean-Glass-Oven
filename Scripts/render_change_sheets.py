"""2026-11-08 change sheets + before/after cross-section, drawn from the STEP files themselves.

  OLD = the 2026-10-16 package, NEW = FAB_PACKAGE_2026-11-08. Sections are cut from the real solids (build123d),
  iso pictures are headless Blender renders of the new STLs (Scripts/blender_iso.py).
Run: .venv-cad/bin/python Scripts/render_change_sheets.py [<old_package_dir>]
Out: Renders/shrink_insulation_before_after_2026-11-08.png, Renders/change_sheet_2026-11-08.png,
     Renders/change_sheets_2026-11-08/<nn>_<name>.png, change-sheets-2026-11-08.html
"""
import os, sys, math, subprocess, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle as MRect
from build123d import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), "Heat-N-Clean-ARCHIVE (old, do not build from)", "FAB_PACKAGE_2026-10-16")   # only as the "before" outline
NEW = os.path.join(ROOT, "FAB_PACKAGE_2026-11-08")
REN = os.path.join(ROOT, "Renders"); SHD = os.path.join(REN, "change_sheets_2026-11-08"); ISO = os.path.join(SHD, "iso")
os.makedirs(ISO, exist_ok=True)
for f in ("/System/Library/Fonts/Hiragino Sans GB.ttc", "/System/Library/Fonts/Helvetica.ttc"):
    if os.path.exists(f): font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = ["Helvetica", "Hiragino Sans GB"]
plt.rcParams["axes.unicode_minus"] = False
D = 4.0
BLUE, BLUE_E, OLDC, RED, CER = "#7fa6d9", "#1f3f73", "#9a9a9a", "#d0202a", "#efe6cf"

PARTS = [  # no, file, EN, ZH, material/thickness EN, ZH, changed
 ("01", "01_Inner_Wall_Tube", "Inner Wall Tube", "内壁管", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", True),
 ("02", "02_Outer_Perforated_Tube", "Outer Perforated Tube", "外冲孔管", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", True),
 ("03", "03_Support_Ring", "Support Ring", "支撑环", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", True),
 ("04", "04_Bottom_Cap", "Bottom Cap", "底盖", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", True),
 ("05", "05_One_Piece_Top_Cap", "One-Piece Top Cap", "一体顶盖", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", True),
 ("06", "06_Lid_Inner_Tube", "Lid Inner Tube", "盖子内管", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", True),
 ("07", "07_Lid_Outer_Perforated_Tube", "Lid Outer Perforated Tube", "盖子外冲孔管", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", True),
 ("08", "08_Lid_Top_Disk", "Lid Top Disk", "盖子顶盘", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", True),
 ("09", "09_Lid_Ceramic_Holder", "Lid Ceramic Holder", "盖子陶瓷托架", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", True),
 ("10", "10_Lid_Handle", "Lid Handle", "提手", "304 SS rod Ø8", "304 不锈钢棒 Ø8", False),
 ("11", "11_Lid_Hinge_Strap", "Lid Hinge Strap (placeholder)", "盖子铰链片（示意）", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", True),
 ("13", "13_Hinge_Pin", "Hinge Pin (placeholder)", "铰链销（示意）", "304 SS rod Ø5", "304 不锈钢棒 Ø5", True),
 ("14", "14_Steel_Tray", "Steel Tray", "钢托盘", "steel, 3 mm", "钢，3 mm", True),
 ("S", "Ceramic_Spacer_Ring", "Ceramic Spacer Rings ×5 (we supply)", "陶瓷垫环 ×5（我方提供）", "ceramic, 14 mm ×3 + 10 mm ×2", "陶瓷，14 mm ×3 + 10 mm ×2", True),
]

def load(pkg, name):
    if name == "Ceramic_Spacer_Ring":      # top body spacer ring, as drawn in the viewers
        ri, ro = (72.05, 76.05) if pkg == OLD else (68.05, 72.05)
        s = Pos(0, 0, 52) * (Cylinder(ro, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)) - Cylinder(ri, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        for a in [52.4 + 60 * k for k in range(6)]:
            s -= Rot(0, 0, a) * Pos((ri + ro) / 2, 0, 59) * Rot(0, 90, 0) * Cylinder(3.3, 6)
        return s
    s = import_step(os.path.join(pkg, "STEP", name + ".step"))
    return Solid(s.solids()[0].wrapped)

def section(shape, ang=None, z=None, off=0.0):
    """faces of the cut: list of (triangles[N,3,2], edges[list of (M,2)]) in (r, z) or plan (x, y) coordinates.
    off: cut plane parallel to the radial plane at ang, shifted sideways by off (to cut along a slot wall)"""
    if z is None:
        s = Pos(0, off, 0) * (Rot(0, 0, -ang) * shape); cut = Plane.XZ * Rectangle(600, 600)
        f2 = lambda v: (v.X, v.Z)
    else:
        s = shape; cut = Plane.XY.offset(z) * Rectangle(900, 900)
        f2 = lambda v: (v.X, v.Y)
    r = s & cut
    out = []
    for f in (r.faces() if r is not None else []):
        vs, tris = f.tessellate(0.02, 0.2)
        P = np.array([f2(v) for v in vs])
        T = np.array([[P[i] for i in t] for t in tris]) if tris else np.zeros((0, 3, 2))
        E = []
        for e in f.edges():
            n = max(2, int(e.length / 0.3))
            E.append(np.array([f2(e @ t) for t in np.linspace(0, 1, n)]))
        out.append((T, E))
    return out

def draw(ax, sec, new=True, lw=1.0):
    from matplotlib.collections import PolyCollection, LineCollection
    for T, E in sec:
        if new and len(T): ax.add_collection(PolyCollection(T, facecolor=BLUE, edgecolor=BLUE, linewidth=0.1, zorder=2))
        ax.add_collection(LineCollection(E, colors=BLUE_E if new else OLDC, linewidths=lw if new else lw * 1.1,
                                         linestyles="solid" if new else (0, (4, 2.5)), zorder=3 if new else 4))

def callout(ax, xy_new, text, txy, xy_old=None, fs=8.5):
    if xy_old is not None and abs(xy_old[0] - xy_new[0]) + abs(xy_old[1] - xy_new[1]) > 0.1:
        ax.annotate("", xy=xy_new, xytext=xy_old, arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6, mutation_scale=11), zorder=8)
        ax.plot(*xy_old, marker="o", ms=3, color=OLDC, zorder=8)
    ax.annotate(text, xy=xy_new, xytext=txy, fontsize=fs, color="#111", zorder=9, ha="left", va="center",
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=RED, lw=1.0),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=0.9, mutation_scale=9, shrinkA=0, shrinkB=2))

# ── per-part drawing specs: view, section, callouts [(new_xy, old_xy, text, label_xy)] ──────────────────────────────
def spec(no):
    tube = lambda z0, z1, ri, ro, zb, extra: dict(
        ang=52.4, xlim=(56, 92), ylim=(z0 - 6, z1 + 6),
        calls=[((ri - D, z0 + 0.25 * (z1 - z0)), (ri, z0 + 0.25 * (z1 - z0)), f"ID Ø{2*ri:.1f} → Ø{2*(ri-D):.1f}  (−8.0)\n内径 Ø{2*ri:.1f} → Ø{2*(ri-D):.1f}", (79, z0 + 0.18 * (z1 - z0))),
               ((ro - D, z0 + 0.45 * (z1 - z0)), (ro, z0 + 0.45 * (z1 - z0)), f"OD Ø{2*ro:.1f} → Ø{2*(ro-D):.1f}  (−8.0)\n外径 Ø{2*ro:.1f} → Ø{2*(ro-D):.1f}", (79, z0 + 0.42 * (z1 - z0))),
               (((ri + ro) / 2 - D, zb), ((ri + ro) / 2, zb), "M6 holes: same angles + heights,\nmoved in 4.0 with the wall\nM6 孔：角度和高度不变，随管壁内移 4.0", (79, zb + 0.08 * (z1 - z0)))] + extra)
    if no == "01": return tube(-31.7, 91.0, 70.85, 71.65, 59.0, [((66.85, 0), None, "Height 122.7, wall 0.8, glass slots 13.3: no change\n高 122.7，壁厚 0.8，玻璃槽 13.3：不变", (57, -40))])
    if no == "06": return tube(93.0, 127.2, 70.85, 71.65, 120.2, [((66.85, 96), None, "Height 34.2, wall 0.8: no change\n高 34.2，壁厚 0.8：不变", (57, 88))])
    if no == "02": return tube(-31.7, 91.0, 76.05, 77.25, 59.0, [((73.25, 21.3), None, "Perforation Ø4 @ 6 mm kept:\n80 → 76 holes per row\n冲孔 Ø4、孔距 6 mm 不变：每排 80 → 76 孔", (79, 8))])
    if no == "07": return tube(93.0, 127.2, 76.05, 77.25, 120.2, [((73.25, 109.2), None, "Perforation Ø4 @ 6 mm kept, fewer holes per row\n冲孔 Ø4、孔距 6 mm 不变，每排孔数减少", (57, 88))])
    if no == "03": return dict(ang=40, xlim=(30, 80), ylim=(-16, 16), calls=[
        ((66.65, 4.0), (70.65, 4.0), "Bolt wall OD Ø141.3 → Ø133.3  (−8.0)\n螺栓墙外径 Ø141.3 → Ø133.3", (68.5, 12.5)),
        ((60.0, -5.9), (64.0, -5.9), "Leg holes Ø6.6 on Ø128 → Ø120\n脚孔 Ø6.6，孔位圆 Ø128 → Ø120", (66, -12.5)),
        ((44, 0.6), None, "Raised seat (r 36.25–52) + wire holes (r 58): no change\n抬高座面（r 36.25–52）和线孔（r 58）：不变", (30.5, -12.5))])
    if no == "04": return dict(ang=40, xlim=(40, 92), ylim=(-40, -8), calls=[
        ((74.75, -20), (78.75, -20), "OD Ø157.5 → Ø149.5  (−8.0)\n外径 Ø157.5 → Ø149.5", (80, -12)),
        ((74.15, -24.0), (78.15, -24.0), "6 × M6 holes in the skirt, moved in 4.0\n裙边 6 个 M6 孔，内移 4.0", (79, -29)),
        ((60.0, -32.3), (64.0, -32.3), "Leg holes on Ø128 → Ø120\n脚孔位圆 Ø128 → Ø120", (55, -37.5)),
        ((48, -32.3), None, "Wire holes (r 58): no change\n线孔（r 58）：不变", (41, -14))])
    if no == "05":   # cut along the slot, through the groove's side wall (5.85 off the slot centreline): x = sqrt(r^2 - 5.85^2)
        X = lambda r: math.sqrt(r * r - 5.85 ** 2)
        return dict(ang=6.5, off=5.85, xlim=(36, 94), ylim=(58, 100), calls=[
        ((X(74.65), 91.6), (X(78.65), 91.6), "Ring OD Ø157.3 → Ø149.3  (−8.0)\n圆环外径 Ø157.3 → Ø149.3", (79, 97.5)),
        ((X(71.55), 72.0), (X(75.55), 72.0), "Groove length 29.1 → 25.1  (−4.0)\n金属槽长度 29.1 → 25.1", (77, 64)),
        ((X(66.65), 88.0), (X(70.65), 88.0), "Inner sleeve Ø141.3 → Ø133.3\n内套边 Ø141.3 → Ø133.3", (77, 81)),
        ((X(46.45), 92.2), None, "Ring width, ceramic edge → cap edge: 32.4 → 28.4  (−4.0)\n圆环宽度（陶瓷边到顶盖边）：32.4 → 28.4", (37, 97.5)),
        ((X(47.0), 84), None, "Ceramic sleeve + groove profile (10.5, R5.25): no change\n陶瓷套边和槽形（10.5，R5.25）：不变", (37, 61)),
    ], ring=True)
    if no == "08": return dict(ang=52.4, xlim=(40, 92), ylim=(108, 134), calls=[
        ((74.75, 118), (78.75, 118), "OD Ø157.5 → Ø149.5  (−8.0)\n外径 Ø157.5 → Ø149.5", (80, 131)),
        ((74.15, 120.2), (78.15, 120.2), "6 × M6 holes, moved in 4.0\n6 个 M6 孔，内移 4.0", (79, 112)),
        ((48, 128.4), None, "Handle holes Ø4.5: no change\n提手孔 Ø4.5：不变", (41, 132))])
    if no == "09": return dict(ang=52.4, xlim=(34, 92), ylim=(86, 112), calls=[
        ((73.2, 92.6), (77.2, 92.6), "Plate OD Ø154.4 → Ø146.4  (−8.0)\n底板外径 Ø154.4 → Ø146.4", (79, 88.5)),
        ((66.65, 103.5), (70.65, 103.5), "Bolt wall Ø141.3 → Ø133.3, 6 × M6 moved in 4.0\n立墙 Ø141.3 → Ø133.3，6 个 M6 内移 4.0", (70, 109.5)),
        ((71.85, 94.6), (75.85, 94.6), "Outer lip Ø151.7 → Ø143.7\n外侧小边 Ø151.7 → Ø143.7", (79, 97)),
        ((46.45, 96), None, "Ceramic lid disk pocket: no change\n陶瓷盖盘槽位：不变", (35, 109.5))])
    if no == "11": return dict(z=99.0, plan=True, xlim=(10, 60), ylim=(-90, -55), calls=[
        ((74.15 * math.cos(math.radians(292.4)), 74.15 * math.sin(math.radians(292.4))),
         (78.15 * math.cos(math.radians(292.4)), 78.15 * math.sin(math.radians(292.4))),
         "Moved in 4.0 along the 292.4° lid bolt\n沿 292.4° 盖子螺栓内移 4.0", (11, -60))])
    if no == "13": return dict(z=98.2, plan=True, xlim=(25, 60), ylim=(-92, -50), calls=[
        ((40.3, -73.0), (41.8, -76.7), "Moved in 4.0 with the strap (pivot r 81.5 → 77.5)\n随铰链片内移 4.0（铰链轴 r 81.5 → 77.5）", (26, -54))])
    if no == "14": return dict(z=-58.2, plan=True, xlim=(-110, 120), ylim=(-110, 110), calls=[
        ((60 * math.cos(math.radians(40)), 60 * math.sin(math.radians(40))), (64 * math.cos(math.radians(40)), 64 * math.sin(math.radians(40))),
         "3 leg holes Ø6.6 on Ø128 → Ø120\n3 个脚孔 Ø6.6，孔位圆 Ø128 → Ø120", (55, 95)),
        ((-95, 0), None, "Outline + thickness: no change\n外形和厚度：不变", (-105, -98))])
    if no == "S": return dict(ang=52.4, xlim=(60, 88), ylim=(46, 72), calls=[
        ((68.05, 54), (72.05, 54), "ID Ø144.1 → Ø136.1  (−8.0)\n内径 Ø144.1 → Ø136.1", (77, 50)),
        ((72.05, 63), (76.05, 63), "OD Ø152.1 → Ø144.1  (−8.0)\n外径 Ø152.1 → Ø144.1", (77, 68)),
        ((70.05, 59), (74.05, 59), "Heights 14 / 10 + 6 bolt holes: no change\n高度 14 / 10 和 6 个螺栓孔：不变", (61, 69.5))])
    return None

SUMMARY = {  # (EN, ZH) rows for the change table on each sheet
 "01": [("ID", "内径", "141.7", "133.7", "−8.0"), ("OD", "外径", "143.3", "135.3", "−8.0"), ("M6 hole circle", "M6 孔位圆", "Ø142.5", "Ø134.5", "−8.0")],
 "02": [("ID", "内径", "152.1", "144.1", "−8.0"), ("OD", "外径", "154.5", "146.5", "−8.0"), ("Holes per row (Ø4 @ 6)", "每排孔数（Ø4，孔距 6）", "80", "76", "−4")],
 "03": [("OD (bolt wall)", "外径（螺栓墙）", "141.3", "133.3", "−8.0"), ("Bolt wall ID", "螺栓墙内径", "139.7", "131.7", "−8.0"), ("Leg hole circle", "脚孔位圆", "Ø128", "Ø120", "−8.0")],
 "04": [("OD", "外径", "157.5", "149.5", "−8.0"), ("Skirt ID", "裙边内径", "155.1", "147.1", "−8.0"), ("Leg hole circle", "脚孔位圆", "Ø128", "Ø120", "−8.0")],
 "05": [("Ring OD", "圆环外径", "157.3", "149.3", "−8.0"), ("Ring width (ceramic → edge)", "圆环宽度（陶瓷到边）", "32.4", "28.4", "−4.0"),
        ("Groove length (×4)", "金属槽长度（×4）", "29.1", "25.1", "−4.0"), ("Inner sleeve OD", "内套边外径", "141.3", "133.3", "−8.0"), ("Vent circle", "通风孔位圆", "Ø147.7", "Ø139.7", "−8.0")],
 "06": [("ID", "内径", "141.7", "133.7", "−8.0"), ("OD", "外径", "143.3", "135.3", "−8.0")],
 "07": [("ID", "内径", "152.1", "144.1", "−8.0"), ("OD", "外径", "154.5", "146.5", "−8.0")],
 "08": [("OD", "外径", "157.5", "149.5", "−8.0"), ("Skirt ID", "裙边内径", "155.1", "147.1", "−8.0")],
 "09": [("Plate OD", "底板外径", "154.4", "146.4", "−8.0"), ("Bolt wall OD", "立墙外径", "141.3", "133.3", "−8.0"), ("Outer lip OD", "外侧小边外径", "151.7", "143.7", "−8.0")],
 "11": [("Bolt hole radius", "螺栓孔半径", "r 78.15", "r 74.15", "−4.0")],
 "13": [("Hinge pivot radius", "铰链轴半径", "r 81.5", "r 77.5", "−4.0")],
 "14": [("Leg hole circle", "脚孔位圆", "Ø128", "Ø120", "−8.0")],
 "S":  [("ID", "内径", "144.1", "136.1", "−8.0"), ("OD", "外径", "152.1", "144.1", "−8.0")],
}
HEAD_EN = "Change 2026-11-08: insulation 24.6 → 20.6 mm so the glass slurper (31 mm gap) fits; top cap ring 33.8 → ~30 mm"
HEAD_ZH = "改动 2026-11-08：保温层 24.6 → 20.6 mm，让玻璃 slurper（31 mm 空隙）放得下；顶盖圆环 33.8 → 约 30 mm"
NOTE_EN = "All body and lid diameters −8.0 mm. Heights, sheet thickness, hole sizes, slot widths, ceramic core and ceramic lid disk: no change."
NOTE_ZH = "机体和盖子所有直径 −8.0 mm。高度、板厚、孔径、槽宽、陶瓷芯和陶瓷盖盘：都不改。"

def iso_renders():
    stls = [os.path.join(NEW, "STL", p[1] + ".stl") for p in PARTS if p[0] != "S"]
    sp = os.path.join(ISO, "Ceramic_Spacer_Ring.stl")
    export_stl(load(NEW, "Ceramic_Spacer_Ring"), sp)
    subprocess.run(["/Applications/Blender.app/Contents/MacOS/Blender", "-b", "-P", os.path.join(ROOT, "Scripts", "blender_iso.py"), "--", ISO] + stls + [sp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(sp)

def table(ax, rows, x, y, fs=9):
    c1, c2, c3 = x + 0.245, x + 0.335, x + 0.425
    ax.text(x, y, "Feature · 位置", fontsize=fs, weight="bold"); ax.text(c1, y, "Old · 旧", fontsize=fs, weight="bold", color="#666")
    ax.text(c2, y, "New · 新", fontsize=fs, weight="bold", color=BLUE_E); ax.text(c3, y, "Δ", fontsize=fs, weight="bold", color=RED)
    for i, (en, zh, o, n, d) in enumerate(rows):
        yy = y - 0.04 * (i + 1)
        ax.text(x, yy, f"{en}\n{zh}", fontsize=fs - 0.8, va="center")
        ax.text(c1, yy, o, fontsize=fs + 1, va="center", color="#666"); ax.text(c2, yy, n, fontsize=fs + 1, va="center", color=BLUE_E, weight="bold")
        ax.text(c3, yy, d, fontsize=fs + 1, va="center", color=RED, weight="bold")

def part_sheet(p, idx, total):
    no, fn, en, zh, mat_en, mat_zh, changed = p
    sp = spec(no)
    fig = plt.figure(figsize=(8.5, 11), dpi=200)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    bg.add_patch(MRect((0.03, 0.925), 0.94, 0.06, fc="#1f3f73", ec="none"))
    bg.text(0.05, 0.965, f"{no}  {en}", color="white", fontsize=17, weight="bold", va="center")
    bg.text(0.05, 0.94, zh, color="white", fontsize=13, va="center")
    bg.text(0.95, 0.965, "CHANGED · 已改", color="#ffd34d", fontsize=13, weight="bold", va="center", ha="right")
    bg.text(0.95, 0.94, "Change 2026-11-08 · 改动", color="white", fontsize=10, va="center", ha="right")
    bg.text(0.05, 0.905, HEAD_EN, fontsize=8.6); bg.text(0.05, 0.89, HEAD_ZH, fontsize=8.6)
    iso = os.path.join(ISO, fn + ".png")
    if os.path.exists(iso):
        a = fig.add_axes([0.03, 0.615, 0.42, 0.25]); a.imshow(plt.imread(iso)); a.axis("off")
        bg.text(0.05, 0.86, "New part (3D) · 新零件", fontsize=8.5, color="#444")
    table(bg, SUMMARY[no], 0.48, 0.858)
    bg.text(0.48, 0.858 - 0.04 * (len(SUMMARY[no]) + 1) + 0.005, "Everything not listed: no change · 未列出的都不改", fontsize=8.5, color="#444", va="top")
    ax = fig.add_axes([0.08, 0.135, 0.87, 0.455]); ax.set_aspect("equal")
    old = load(OLD, fn); new = load(NEW, fn)
    if sp.get("plan"):
        so, sn = section(old, z=sp["z"]), section(new, z=sp["z"]); title = f"Plan section at z {sp['z']} (looking down) · 平面剖视（俯视）"
        xl, yl = "x (mm)", "y (mm)"
    else:
        off = sp.get("off", 0.0)
        so, sn = section(old, ang=sp["ang"], off=off), section(new, ang=sp["ang"], off=off)
        if off:
            title = f"Section along the glass slot at {sp['ang']}°, through the groove wall · 沿 {sp['ang']}° 玻璃槽剖视（金属槽侧壁）"
            xl = "distance from oven centre along the slot (mm) · 沿槽到中心距离"
        else:
            title = f"Half-section at {sp['ang']}° · 半剖视 {sp['ang']}°"; xl = "radius from oven centre (mm) · 距中心半径"
        yl = "height z (mm) · 高度"
        xc = math.sqrt(46.25 ** 2 - off ** 2)
        ax.axvline(xc, color="#b08a3c", lw=0.8, ls=":", zorder=1); ax.text(xc + 0.15, sp["ylim"][0] + 0.5, "ceramic OD r 46.25\n陶瓷外径", fontsize=6.5, color="#8a6a2a")
    draw(ax, sn, True); draw(ax, so, False)
    for new_xy, old_xy, text, lab in sp["calls"]:
        callout(ax, new_xy, text, lab, old_xy)
    if sp.get("ring"):
        X = lambda r: math.sqrt(r * r - sp.get("off", 0.0) ** 2)
        ax.annotate("", xy=(X(46.25), 94.5), xytext=(X(74.65), 94.5), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.2))
        ax.text((X(46.25) + X(74.65)) / 2, 95.0, "28.4", color=RED, fontsize=9, ha="center", weight="bold")
    if (sp["ylim"][1] - sp["ylim"][0]) > 1.6 * (sp["xlim"][1] - sp["xlim"][0]):   # tall tubes: stretch sideways so the wall shows
        ax.set_aspect("auto"); title += "  (sideways scale stretched · 横向放大)"
    ax.set_xlim(*sp["xlim"]); ax.set_ylim(*sp["ylim"]); ax.set_title(title, fontsize=10, loc="left")
    ax.set_xlabel(xl, fontsize=8); ax.set_ylabel(yl, fontsize=8); ax.tick_params(labelsize=7); ax.grid(color="#eee", lw=0.5)
    # legend + title block
    bg.add_patch(MRect((0.07, 0.071), 0.03, 0.008, fc=BLUE, ec=BLUE_E)); bg.text(0.105, 0.075, "New 2026-11-08 · 新", fontsize=8, va="center")
    bg.plot([0.25, 0.28], [0.075, 0.075], color=OLDC, ls=(0, (4, 2.5)), lw=1.3); bg.text(0.285, 0.075, "Old 2026-10-16 · 旧", fontsize=8, va="center")
    bg.annotate("", xy=(0.47, 0.075), xytext=(0.43, 0.075), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6)); bg.text(0.475, 0.075, "where it moved · 移动位置", fontsize=8, va="center")
    bg.add_patch(MRect((0.03, 0.015), 0.94, 0.048, fc="none", ec="#333", lw=0.8))
    for x in (0.25, 0.55, 0.80): bg.plot([x, x], [0.015, 0.063], color="#333", lw=0.6)
    bg.text(0.04, 0.05, "Part · 零件", fontsize=6.5, color="#666"); bg.text(0.04, 0.028, f"{no}  {en}\n{zh}", fontsize=7, va="center")
    bg.text(0.26, 0.05, "Material / thickness · 材料 / 厚度", fontsize=6.5, color="#666"); bg.text(0.26, 0.028, f"{mat_en}\n{mat_zh}", fontsize=7, va="center")
    bg.text(0.56, 0.05, "Package · 文件包", fontsize=6.5, color="#666"); bg.text(0.56, 0.028, "FAB_PACKAGE_2026-11-08\nHeat & Clean Glass Oven", fontsize=7, va="center")
    bg.text(0.81, 0.05, "Sheet · 页", fontsize=6.5, color="#666"); bg.text(0.81, 0.028, f"{idx} / {total}\nmm, not to scale · 单位 mm", fontsize=7, va="center")
    out = os.path.join(SHD, f"{no}_{fn.split('_', 1)[1] if no != 'S' else fn}.png")
    fig.savefig(out, dpi=200); plt.close(fig); print("sheet", out)
    return out

def overview(total):
    fig = plt.figure(figsize=(8.5, 11), dpi=200)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    bg.add_patch(MRect((0.03, 0.915), 0.94, 0.07, fc="#1f3f73", ec="none"))
    bg.text(0.05, 0.965, "Heat & Clean Glass Oven · 加热清洁玻璃炉", color="white", fontsize=15, weight="bold", va="center")
    bg.text(0.05, 0.937, "Change sheet 2026-11-08 · 改动总表   (page 1 / " + str(total) + ")", color="white", fontsize=10, va="center")
    bg.text(0.05, 0.897, HEAD_EN, fontsize=8.8, weight="bold"); bg.text(0.05, 0.880, HEAD_ZH, fontsize=8.8, weight="bold")
    bg.text(0.05, 0.862, NOTE_EN, fontsize=7.6); bg.text(0.05, 0.848, NOTE_ZH, fontsize=7.6)
    cols, rows = 4, 4; x0, y0, w, h = 0.035, 0.07, 0.93 / cols, 0.765 / rows
    for i, p in enumerate(PARTS):
        no, fn, en, zh, _, _, changed = p
        c, r = i % cols, i // cols
        X, Y = x0 + c * w, y0 + (rows - 1 - r) * h
        bg.add_patch(FancyBboxPatch((X + 0.004, Y + 0.004), w - 0.008, h - 0.008, boxstyle="round,pad=0,rounding_size=0.008",
                                    fc="#fff7e0" if changed else "#f0f0f0", ec=RED if changed else "#bbbbbb", lw=1.4 if changed else 0.8))
        iso = os.path.join(ISO, fn + ".png")
        if os.path.exists(iso):
            a = fig.add_axes([X + 0.015, Y + 0.075, w - 0.03, h - 0.105]); im = plt.imread(iso)
            if not changed: im = np.dstack([np.repeat(im[..., :3].mean(axis=2, keepdims=True), 3, axis=2) * 0.6 + 0.4, im[..., 3:]])
            a.imshow(im); a.axis("off")
        bg.text(X + 0.012, Y + h - 0.018, f"{no}", fontsize=11, weight="bold", color=BLUE_E if changed else "#888")
        bg.text(X + w - 0.012, Y + h - 0.018, "CHANGED · 已改" if changed else "no change · 不改", fontsize=6.5, ha="right",
                weight="bold", color=RED if changed else "#888")
        bg.text(X + 0.012, Y + 0.058, f"{en}\n{zh}", fontsize=6.4, va="center", color="#111" if changed else "#888")
        if changed:
            k = SUMMARY[no][0]; extra = SUMMARY[no][1] if len(SUMMARY[no]) > 1 else None
            line = f"{k[0]} {k[2]} → {k[3]} ({k[4]})" + (f"\n{extra[0]} {extra[2]} → {extra[3]} ({extra[4]})" if extra else "")
            bg.text(X + 0.012, Y + 0.022, line, fontsize=6.0, va="center", color=RED)
    bg.text(0.05, 0.045, "Red frame = changed (see its own sheet) · 红框 = 已改（见单独一页）   Grey = no change · 灰色 = 不改", fontsize=7.5)
    bg.text(0.05, 0.03, "Bolts: same M6 bolts, same length, same angles (52.4° + n×60°) and heights · 螺栓：同样的 M6，同样长度、角度和高度", fontsize=7.5)
    out = os.path.join(REN, "change_sheet_2026-11-08.png"); fig.savefig(out, dpi=200); plt.close(fig); print("overview", out)

def before_after():
    names = [p[1] for p in PARTS if p[0] not in ("S", "14", "10", "11", "13")]
    fig, axs = plt.subplots(1, 2, figsize=(16, 9), dpi=150, sharey=True)
    for ax, pkg, lab in ((axs[0], OLD, "BEFORE 2026-10-16 · 改前"), (axs[1], NEW, "AFTER 2026-11-08 · 改后")):
        d = 0 if pkg == OLD else D
        for n in names:
            draw(ax, section(load(pkg, n), ang=52.4), True, lw=0.6)
        for sgn in (1, -1):   # ceramics (not changed): core, base disk, lid disk; spacer rings (moved)
            ax.add_patch(MRect((sgn * 40.75 if sgn > 0 else -46.25, 5.06), 5.5, 87.14, fc=CER, ec="#8a7a55", lw=0.6, zorder=1))
            for z0, z1 in ((-31, -17), (-5, 9), (52, 66), (95.2, 105.2), (115.2, 125.2)):
                ax.add_patch(MRect((sgn * (72.05 - d) if sgn > 0 else -(76.05 - d), z0), 4.0, z1 - z0, fc=CER, ec="#8a7a55", lw=0.5, zorder=1))
        ax.add_patch(MRect((-46.25, -0.44), 92.5, 6.0, fc=CER, ec="#8a7a55", lw=0.6, zorder=1))
        ax.add_patch(MRect((-46.25, 92.2), 92.5, 5.0, fc=CER, ec="#8a7a55", lw=0.6, zorder=1))
        R = 78.75 - d; ring = (78.65 - d) - 46.25
        ax.annotate("", xy=(-R, -42), xytext=(R, -42), arrowprops=dict(arrowstyle="<->", lw=1.2))
        ax.text(0, -46.5, f"Ø{2*R:.1f} overall (caps) · 总外径", ha="center", fontsize=11, weight="bold")
        ax.annotate("", xy=(46.25, 101.5), xytext=(78.65 - d, 101.5), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.4))
        ax.text((46.25 + 78.65 - d) / 2, 103.5, f"top cap ring {ring:.1f}\n顶盖圆环 {ring:.1f}", ha="center", color=RED, fontsize=10, weight="bold", va="bottom")
        ins = (70.85 - d) - 46.25
        ax.annotate("", xy=(-46.25, 40), xytext=(-(70.85 - d), 40), arrowprops=dict(arrowstyle="<->", color="#1d6b2c", lw=1.2))
        ax.text(-(46.25 + 70.85 - d) / 2, 43, f"insulation {ins:.1f}\n保温层 {ins:.1f}", ha="center", color="#1d6b2c", fontsize=10, weight="bold", va="bottom")
        ax.annotate("", xy=(71.65 - d, 30), xytext=(76.05 - d, 30), arrowprops=dict(arrowstyle="<->", lw=0.9))
        ax.text(76.05 - d + 1.5, 30, "air gap 4.4\n空气层 4.4", fontsize=8.5, va="center")
        ax.set_title(lab, fontsize=15, weight="bold", loc="left")
        ax.set_aspect("equal"); ax.set_xlim(-95, 95); ax.set_ylim(-52, 165); ax.grid(color="#eee", lw=0.5); ax.tick_params(labelsize=8)
        ax.axvline(0, color="#aaa", lw=0.5, ls="-.")
    fig.suptitle(HEAD_EN + "\n" + HEAD_ZH, fontsize=12.5, weight="bold")
    fig.text(0.5, 0.015, "Section through the bolt line at 52.4°, every part cut from its STEP file. Ceramics (beige) do not change; spacer rings move in with the tubes. "
             "· 52.4° 螺栓线剖视，每个零件都从 STEP 文件切出。陶瓷（米色）不改；垫环随管子内移。", ha="center", fontsize=8.5)
    out = os.path.join(REN, "shrink_insulation_before_after_2026-11-08.png"); fig.savefig(out, dpi=150, bbox_inches="tight"); plt.close(fig); print("before/after", out)

def html(sheets):
    rows = "\n".join(f'<a href="{os.path.relpath(s, ROOT)}"><img src="{os.path.relpath(s, ROOT)}" loading="lazy"></a>' for s in sheets)
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Heat &amp; Clean Glass Oven: change sheets 2026-11-08</title>
<style>body{{margin:0;font-family:-apple-system,"PingFang SC",sans-serif;background:#eef1f5;color:#111}}
header{{padding:18px 22px;background:#1f3f73;color:#fff}} h1{{margin:0 0 6px;font-size:22px}} p{{margin:4px 0;font-size:15px}}
nav{{padding:10px 22px;font-size:15px}} nav a{{margin-right:14px}}
main{{display:flex;flex-direction:column;align-items:center;gap:18px;padding:18px}} main img{{width:min(100%,900px);background:#fff;box-shadow:0 2px 10px #0002}}</style></head>
<body><header><h1>Change 2026-11-08 · 改动 2026-11-08</h1><p>{HEAD_EN}</p><p>{HEAD_ZH}</p><p>{NOTE_EN}<br>{NOTE_ZH}</p></header>
<nav><a href="viewer-complete.html">Whole oven 3D · 整机</a><a href="viewer-base-full.html">Base · 底座</a><a href="viewer-lid-full.html">Lid · 盖子</a>
<a href="Renders/shrink_insulation_before_after_2026-11-08.png">Before / after section · 改前改后剖视</a><a href="FAB_PACKAGE_2026-11-08/README.txt">README</a></nav>
<main>
{rows}
</main></body></html>"""
    open(os.path.join(ROOT, "change-sheets-2026-11-08.html"), "w", encoding="utf-8").write(page)

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    if not os.environ.get("NO_ISO"): iso_renders()
    changed = [p for p in PARTS if p[6]]
    total = 1 + len(changed)
    sheets = []
    if not only or only == "overview": overview(total)
    if not only or only == "ba": before_after()
    for i, p in enumerate(changed):
        if only and only not in ("sheets", p[0]): continue
        sheets.append(part_sheet(p, i + 2, total))
    if not only:
        html([os.path.join(REN, "change_sheet_2026-11-08.png")] + sheets)
