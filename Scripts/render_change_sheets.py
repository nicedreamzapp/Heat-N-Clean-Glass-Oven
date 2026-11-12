"""2026-11-12 change sheets, drawn from the STEP files themselves.

  The 11-12 change: top cap ring 28.4 -> 20.0 for the smallest glass slurper (insulation 20.6 -> 14.6, air gap 4.4 -> 3.0,
  cap lip 1.4 -> 0.4), 6 -> 5 bolts per ring (41.5 + 72k), hinge onto the 257.5 bolt, legs 5.5/125.5/245.5 with M5
  screws, wire holes r 53.5 at 160/170/315, tray 1.2 lower. OLD = FAB_PACKAGE_2026-11-08-R2 (archive folder),
  NEW = FAB_PACKAGE_2026-11-12. Old = grey dashed, new = solid blue. Sections are cut from the real solids (build123d),
  iso pictures are headless Blender (Workbench) renders of the new STLs.
  (The R2 version of this script, body +2.66, is in git history before 2026-11-12.)
Run: .venv-cad/bin/python Scripts/render_change_sheets.py [<old_R2_package_dir>]
Out: Renders/change_sheet_2026-11-12.png (overview), Renders/ring_shrink_before_after_2026-11-12.png,
     Renders/change_sheets_2026-11-12/<nn>_<name>.png, change-sheets-2026-11-12.html
"""
import os, sys, math, subprocess, textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle as MRect, Circle as MCirc
from matplotlib.collections import PolyCollection, LineCollection
from build123d import *
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hnc_params as HP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG, OLDTAG = "2026-11-12", "2026-11-08-R2"
OLD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), "Heat-N-Clean-ARCHIVE (old, do not build from)", "FAB_PACKAGE_" + OLDTAG)
NEW = os.path.join(ROOT, "FAB_PACKAGE_" + TAG)
REN = os.path.join(ROOT, "Renders"); SHD = os.path.join(REN, "change_sheets_" + TAG); ISO = os.path.join(SHD, "iso")
os.makedirs(ISO, exist_ok=True)
for f in ("/System/Library/Fonts/Hiragino Sans GB.ttc", "/System/Library/Fonts/Helvetica.ttc"):
    if os.path.exists(f): font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = ["Helvetica", "Hiragino Sans GB"]
plt.rcParams["axes.unicode_minus"] = False
BLUE, BLUE_E, OLDC, RED, CER, AMB = "#7fa6d9", "#1f3f73", "#8a8a8a", "#d0202a", "#efe6cf", "#d98a00"
OLD_BOLTS = [52.4 + 60 * k for k in range(6)]
NEW_BOLTS = list(HP.ring_screw_angles)
OLD_LEGS, NEW_LEGS = [40, 160, 280], list(HP.leg_angles)
PROF = 25.0          # radial profile angle: clear of every slot, bolt, leg and wire hole, old and new

# no, file, EN, ZH, material EN, ZH, status ("changed" | "moved" | "same")
PARTS = [
 ("01", "01_Inner_Wall_Tube", "Inner Wall Tube", "内壁管", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", "changed"),
 ("02", "02_Outer_Perforated_Tube", "Outer Perforated Tube", "外冲孔管", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "changed"),
 ("03", "03_Support_Ring", "Support Ring", "支撑环", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", "changed"),
 ("04", "04_Bottom_Cap", "Bottom Cap", "底盖", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "changed"),
 ("05", "05_One_Piece_Top_Cap", "One-Piece Top Cap", "一体顶盖", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "changed"),
 ("06", "06_Lid_Inner_Tube", "Lid Inner Tube", "盖子内管", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", "changed"),
 ("07", "07_Lid_Outer_Perforated_Tube", "Lid Outer Perforated Tube", "盖子外冲孔管", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "changed"),
 ("08", "08_Lid_Top_Disk", "Lid Top Disk", "盖子顶盘", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "changed"),
 ("09", "09_Lid_Ceramic_Holder", "Lid Ceramic Holder", "盖子陶瓷托架", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", "changed"),
 ("10", "10_Lid_Handle", "Lid Handle", "提手", "304 SS rod Ø8", "304 不锈钢棒 Ø8", "same"),
 ("11", "11_Lid_Hinge_Strap", "Lid Hinge Strap (placeholder)", "盖子铰链片（示意）", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "moved"),
 ("13", "13_Hinge_Pin", "Hinge Pin (placeholder)", "铰链销（示意）", "304 SS rod Ø5", "304 不锈钢棒 Ø5", "moved"),
 ("14", "14_Steel_Tray", "Steel Tray", "钢托盘", "steel, 3 mm", "钢，3 mm", "changed"),
 ("S", "Ceramic_Spacer_Ring", "Ceramic Spacer Rings ×5 (we supply)", "陶瓷垫环 ×5（我方提供）", "ceramic, 10 mm", "陶瓷，10 mm", "changed"),
]
STAT = {"changed": ("CHANGED · 已改", RED, "#fff1f0"), "moved": ("MOVED · 移位", AMB, "#fff7e0"),
        "same": ("no change · 不改", "#888", "#f0f0f0")}

def spacer(old):
    ri, ro, angs = (68.05, 72.05, OLD_BOLTS) if old else (HP.housing_outer_r + 0.4, HP.mesh_inner_r, NEW_BOLTS)
    z0 = 56.66
    s = Pos(0, 0, z0) * (Cylinder(ro, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)) - Cylinder(ri, 10, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    for a in angs:
        s -= Rot(0, 0, a) * Pos((ri + ro) / 2, 0, z0 + 5) * Rot(0, 90, 0) * Cylinder(3.3, 8)
    return s

_cache = {}
def load(pkg, name):
    k = (pkg, name)
    if k not in _cache:
        if name == "Ceramic_Spacer_Ring": _cache[k] = spacer(pkg == OLD)
        else:
            s = import_step(os.path.join(pkg, "STEP", name + ".step")); _cache[k] = Solid(s.solids()[0].wrapped)
    return _cache[k]

def section(shape, ang=None, z=None):
    """cut faces as (triangles, edges): radial plane at ang -> (r, z); plane z -> plan (x, y)"""
    if z is None:
        s = Rot(0, 0, -ang) * shape; cut = Plane.XZ * Rectangle(900, 900); f2 = lambda v: (v.X, v.Z)
    else:
        s = shape; cut = Plane.XY.offset(z) * Rectangle(900, 900); f2 = lambda v: (v.X, v.Y)
    r = s & cut
    out = []
    for f in (r.faces() if r is not None else []):
        vs, tris = f.tessellate(0.02, 0.2)
        P = np.array([f2(v) for v in vs])
        T = np.array([[P[i] for i in t] for t in tris]) if tris else np.zeros((0, 3, 2))
        E = [np.array([f2(e @ t) for t in np.linspace(0, 1, max(2, int(e.length / 0.3)))]) for e in f.edges()]
        out.append((T, E))
    return out

def draw(ax, sec, new=True, lw=1.0):
    for T, E in sec:
        if new and len(T): ax.add_collection(PolyCollection(T, facecolor=BLUE, edgecolor=BLUE, linewidth=0.5, zorder=2))
        ax.add_collection(LineCollection(E, colors=BLUE_E if new else OLDC, linewidths=lw if new else lw * 1.1,
                                         linestyles="solid" if new else (0, (4, 2.5)), zorder=3 if new else 4))

def ticks(ax, angs, r, color, ls, lab=None):
    for a in angs:
        t = math.radians(a)
        ax.plot([0.88 * r * math.cos(t), 1.12 * r * math.cos(t)], [0.88 * r * math.sin(t), 1.12 * r * math.sin(t)], color=color, lw=1.0, ls=ls, zorder=6)
        if lab: ax.text(1.2 * r * math.cos(t), 1.2 * r * math.sin(t), f"{a:g}°", fontsize=6, color=color, ha="center", va="center", zorder=7)

def table(ax, rows, x, y, fs=9):
    c1, c2 = x + 0.25, x + 0.36
    ax.text(x, y, "Feature · 位置", fontsize=fs, weight="bold"); ax.text(c1, y, "Old · 旧", fontsize=fs, weight="bold", color="#666")
    ax.text(c2, y, "New · 新", fontsize=fs, weight="bold", color=BLUE_E)
    for i, (en, zh, o, n) in enumerate(rows):
        yy = y - 0.036 * (i + 1)
        ax.text(x, yy, f"{en}\n{zh}", fontsize=fs - 1.2, va="center")
        ax.text(c1, yy, o, fontsize=fs - 0.3, va="center", color="#666"); ax.text(c2, yy, n, fontsize=fs - 0.3, va="center", color=BLUE_E, weight="bold")

B6, B5 = "6 per ring · 52.4°+60°", "5 per ring · 41.5°+72°"
SUMMARY = {
 "01": [("Inside Ø", "内径", "133.7", "121.7"), ("Outside Ø", "外径", "135.3", "123.3"), ("M6 holes", "M6 孔", "18 (6 ×3 rings)", "15 (5 ×3 rings)"),
        ("Bolt angles", "螺栓角度", B6, B5), ("Height, slots", "高度、玻璃槽", "125.36, 4 slots", "same · 不变")],
 "02": [("Inside Ø", "内径", "144.1", "129.3"), ("Outside Ø", "外径", "146.5", "131.7"), ("Perforation per row", "每排冲孔", "76 × Ø4", "68 × Ø4 (same 6 mm pitch, rows)"),
        ("M6 holes", "M6 孔", "18 (6 ×3 rings)", "15 (5 ×3 rings)"), ("Height, slots", "高度、玻璃槽", "125.36, 4 slots", "same · 不变")],
 "03": [("Plate + bolt wall Ø", "底板 + 螺栓壁直径", "133.3", "121.3"), ("Riser", "立边", "r 52", "on the centering wall r 46.45-47.25"),
        ("Leg holes", "脚孔", "Ø6.6 r 60 @ 40/160/280°", "Ø5.5 r 54 @ 5.5/125.5/245.5°"),
        ("Wire holes", "线孔", "r 58 @ 180/190/315°", "r 53.5 @ 160/170/315°"), ("Seat M6 holes", "座圈 M6 孔", "6", "5")],
 "04": [("Outside Ø", "外径", "149.5", "134.7"), ("Leg holes", "脚孔", "Ø6.6 r 60 @ 40/160/280°", "Ø5.5 r 54 @ 5.5/125.5/245.5°"),
        ("Wire holes", "线孔", "r 58 @ 180/190/315°", "r 53.5 @ 160/170/315°"), ("Bottom M6 holes", "底圈 M6 孔", "6", "5"), ("Height", "高度", "17.2", "same · 不变")],
 "05": [("Ring Ø", "顶环外径", "149.3", "132.5"), ("Ring width (ceramic → edge)", "环宽（陶瓷 → 边）", "28.4", "20.0"),
        ("Vents (48, same angles)", "通气孔（48 个，角度不变）", "Ø3.5 at r 69.85", "Ø3.0 at r 63.15"),
        ("Outer skirt / tabs", "外裙边 / 折边片", "skirt + 6 tabs", "no skirt, 5 tabs"), ("Metal grooves (×4)", "金属槽（×4）", "25.1 long", "17.6 long")],
 "06": [("Inside Ø", "内径", "133.7", "121.7"), ("Outside Ø", "外径", "135.3", "123.3"), ("M6 holes", "M6 孔", "12 (6 ×2 rings)", "10 (5 ×2 rings)"), ("Height", "高度", "34.2", "same · 不变")],
 "07": [("Inside Ø", "内径", "144.1", "129.3"), ("Outside Ø", "外径", "146.5", "131.7"), ("M6 holes", "M6 孔", "12 (6 ×2 rings)", "10 (5 ×2 rings)"),
        ("Perforation", "冲孔", "Ø4 @ 6", "Ø4 @ 6, skips around the new holes"), ("Height", "高度", "34.2", "same · 不变")],
 "08": [("Outside Ø", "外径", "149.5", "134.7"), ("M6 holes", "M6 孔", "6", "5"), ("Height", "高度", "14.2", "same · 不变")],
 "09": [("Plate Ø", "底板直径", "146.4", "131.6"), ("Bolt wall Ø", "螺栓壁直径", "133.3", "121.3"), ("Outer lip Ø", "外沿直径", "143.7", "128.9"),
        ("Vents (48)", "通气孔（48 个）", "Ø3.5 at r 69.85", "Ø3.0 at r 63.15"), ("M6 holes", "M6 孔", "6", "5")],
 "10": [("Shape, position", "形状、位置", "—", "same · 不变")],
 "11": [("Hinge bolt", "铰链螺栓", "292.4°", "257.5°"), ("Pivot", "铰链轴", "r 77.5, z 100.86", "r 70.1, z 100.86"), ("Shape", "形状", "—", "same · 不变")],
 "13": [("Hinge bolt", "铰链螺栓", "292.4°", "257.5°"), ("Pivot", "铰链轴", "r 77.5, z 100.86", "r 70.1, z 100.86"), ("Shape", "形状", "—", "same · 不变")],
 "14": [("Leg holes", "脚孔", "Ø6.6 r 60", "Ø5.5 r 54"), ("Leg angles", "脚角度", "40 / 160 / 280°", "5.5 / 125.5 / 245.5°"), ("Position", "位置", "floor top z -56.7", "1.2 lower, z -57.9"),
        ("Outline, thickness", "外形、厚度", "394.5 × 204.5, 3", "same · 不变")],
 "S":  [("Inside Ø", "内径", "136.1", "124.1"), ("Outside Ø", "外径", "144.1", "129.3"), ("M6 holes", "M6 孔", "6", "5"), ("Height (all 5 rings)", "高度（5 个）", "10", "same · 不变")],
}
# per part: profile panel (radial cut at PROF, r/z window) + plan panel (z_old, z_new, half-width, title)
PANELS = {
 "01": dict(prof=((55, 72), (-35, 98)), plan=(-24, -24, 78, "plan cut at the bottom bolt ring z -24 · 底圈螺栓 z -24 平面剖")),
 "02": dict(prof=((58, 78), (-35, 98)), plan=(-24, -24, 80, "plan cut at the bottom bolt ring z -24 · 底圈螺栓 z -24 平面剖")),
 "03": dict(prof=((34, 70), (-8, 10)), plan=(-5.9, -5.9, 72, "plan cut through the plate · 底板平面剖")),
 "04": dict(prof=((30, 80), (-34, -14)), plan=(-32.3, -32.3, 80, "plan cut through the floor · 底面平面剖")),
 "05": dict(prof=((40, 80), (80, 97)), plan=(94.4, 94.4, 80, "plan cut through the ring plate · 顶环平面剖")),
 "06": dict(prof=((55, 72), (94, 132)), plan=(102.86, 102.86, 78, "plan cut at the lower lid bolts z 102.86 · 盖子下圈螺栓平面剖")),
 "07": dict(prof=((58, 78), (94, 132)), plan=(102.86, 102.86, 80, "plan cut at the lower lid bolts z 102.86 · 盖子下圈螺栓平面剖")),
 "08": dict(prof=((30, 80), (115, 133)), plan=(122.86, 122.86, 80, "plan cut at the upper lid bolts z 122.86 · 盖子上圈螺栓平面剖")),
 "09": dict(prof=((40, 78), (93, 110)), plan=(95.3, 95.3, 80, "plan cut through the plate · 底板平面剖")),
 "10": dict(prof=None, plan=(140, 140, 40, "plan cut through the posts · 提手脚平面剖")),
 "11": dict(prof=None, plan=(101.86, 101.86, 90, "plan cut through the strap · 铰链片平面剖")),
 "13": dict(prof=None, plan=(100.86, 100.86, 90, "plan cut through the pin · 销轴平面剖")),
 "14": dict(prof=None, plan=(-58.2, -59.4, 80, "plan cut through the tray floor (centre) · 托盘底面平面剖（中心）")),
 "S":  dict(prof=((58, 78), (52, 72)), plan=(61.66, 61.66, 80, "plan cut at the bolt holes · 螺栓孔平面剖")),
}
HEAD_EN = "Change 2026-11-12: top cap ring 28.4 → 20.0 mm for the smallest glass slurper, 5 bolts per ring, legs 120° apart with M5 screws"
HEAD_ZH = "改动 2026-11-12：顶环 28.4 → 20.0 mm（适配最小玻璃吸管），每圈 5 个螺栓，三脚 120° 均布、M5 螺丝"
NOTE_EN = ("The smallest glass slurper is 21 mm bowl to bend, so the ring from the ceramic to the cap edge goes 28.4 → 20.0: insulation 20.6 → 14.6, "
           "air gap 4.4 → 3.0, cap lip 1.4 → 0.4. Overall Ø149.5 → 134.7. Every bolt ring has 5 M6 bolts 72° apart (41.5 + 72k), between the glass slots. "
           "Hinge on the 257.5° lid bolt. Legs 5.5 / 125.5 / 245.5° at r 54 with M5 × 40 screws. Wire holes r 53.5 at 160 / 170 / 315°. Tray 1.2 lower. "
           "NOT changed: heights, sheet thicknesses, glass slot widths, the handle, the tray outline, the ceramics.")
NOTE_ZH = ("最小玻璃吸管碗到弯头 21 mm，所以陶瓷到顶盖边的环宽 28.4 → 20.0：保温层 20.6 → 14.6，空气层 4.4 → 3.0，顶盖外沿 1.4 → 0.4。整机外径 149.5 → 134.7。"
           "每圈 5 个 M6 螺栓，间隔 72°（41.5 + 72k），在玻璃槽之间。铰链在 257.5° 盖子螺栓上。三脚 5.5 / 125.5 / 245.5°，r 54，M5 × 40 螺丝。"
           "线孔 r 53.5，160 / 170 / 315°。托盘低 1.2。不改：高度、板厚、玻璃槽宽、提手、托盘外形、陶瓷。")

def iso_renders():
    stls = [os.path.join(NEW, "STL", p[1] + ".stl") for p in PARTS if p[0] != "S"]
    sp = os.path.join(ISO, "Ceramic_Spacer_Ring.stl"); export_stl(load(NEW, "Ceramic_Spacer_Ring"), sp)
    subprocess.run(["/Applications/Blender.app/Contents/MacOS/Blender", "-b", "-P", os.path.join(ROOT, "Scripts", "blender_iso.py"), "--", ISO] + stls + [sp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(sp)

def header(bg, no, en, zh, status):
    lab, col, _ = STAT[status]
    bg.add_patch(MRect((0.03, 0.925), 0.94, 0.06, fc="#1f3f73", ec="none"))
    bg.text(0.05, 0.965, f"{no}  {en}", color="white", fontsize=17, weight="bold", va="center")
    bg.text(0.05, 0.94, zh, color="white", fontsize=13, va="center")
    bg.text(0.95, 0.965, lab, color="#ffd34d", fontsize=13, weight="bold", va="center", ha="right")
    bg.text(0.95, 0.94, "Change 2026-11-12 · 改动", color="white", fontsize=10, va="center", ha="right")
    bg.text(0.05, 0.905, HEAD_EN, fontsize=8.0); bg.text(0.05, 0.89, HEAD_ZH, fontsize=8.0)

def footer(bg, no, en, zh, mat_en, mat_zh, idx, total):
    bg.add_patch(MRect((0.07, 0.071), 0.03, 0.008, fc=BLUE, ec=BLUE_E)); bg.text(0.105, 0.075, "New 2026-11-12 · 新", fontsize=8, va="center")
    bg.plot([0.30, 0.33], [0.075, 0.075], color=OLDC, ls=(0, (4, 2.5)), lw=1.3); bg.text(0.335, 0.075, "Old 2026-11-08 R2 · 旧", fontsize=8, va="center")
    bg.plot([0.58, 0.61], [0.075, 0.075], color=RED, lw=1.2); bg.text(0.615, 0.075, "new bolt / leg angles · 新角度", fontsize=8, va="center")
    bg.add_patch(MRect((0.03, 0.015), 0.94, 0.048, fc="none", ec="#333", lw=0.8))
    for x in (0.25, 0.55, 0.80): bg.plot([x, x], [0.015, 0.063], color="#333", lw=0.6)
    bg.text(0.04, 0.05, "Part · 零件", fontsize=6.5, color="#666"); bg.text(0.04, 0.028, f"{no}  {en}\n{zh}", fontsize=7, va="center")
    bg.text(0.26, 0.05, "Material / thickness · 材料 / 厚度", fontsize=6.5, color="#666"); bg.text(0.26, 0.028, f"{mat_en}\n{mat_zh}", fontsize=7, va="center")
    bg.text(0.56, 0.05, "Package · 文件包", fontsize=6.5, color="#666"); bg.text(0.56, 0.028, f"FAB_PACKAGE_{TAG}\nHeat & Clean Glass Oven", fontsize=7, va="center")
    bg.text(0.81, 0.05, "Sheet · 页", fontsize=6.5, color="#666"); bg.text(0.81, 0.028, f"{idx} / {total}\nmm · 单位 mm", fontsize=7, va="center")

def plan_ax(ax, no, old, new, zo, zn, hw, title):
    draw(ax, section(new, z=zn), True, lw=0.8); draw(ax, section(old, z=zo), False, lw=0.8)
    if no in ("01", "02", "03", "04", "06", "07", "08", "09", "S"):
        ticks(ax, OLD_BOLTS, hw * 0.83, OLDC, (0, (3, 2))); ticks(ax, NEW_BOLTS, hw * 0.83, RED, "solid", lab=True)
    if no in ("11", "13"):   # context: lid outline (08, Ø134.7 new / Ø149.5 old) and the hinge bolt angle
        ax.add_patch(MCirc((0, 0), 67.35, fill=False, ec="#c9d6ea", lw=1.0)); ax.add_patch(MCirc((0, 0), 74.75, fill=False, ec="#ccc", lw=0.8, ls=(0, (4, 2.5))))
        ticks(ax, [292.4], hw * 0.83, OLDC, (0, (3, 2)), lab=True); ticks(ax, [257.5], hw * 0.83, RED, "solid", lab=True)
        ax.text(0, 0, "lid outline · 盖子外形\nnew Ø134.7 · old Ø149.5", fontsize=7, ha="center", va="center", color="#667")
    if no in ("03", "04", "14"):
        for a in NEW_LEGS: ax.text(54 * math.cos(math.radians(a)) * 0.78, 54 * math.sin(math.radians(a)) * 0.78, f"leg {a:g}°\n脚", fontsize=5.5, color=RED, ha="center", va="center")
    for a in (HP.slot_positions if no in ("01", "02", "05", "06", "07") else []):
        t = math.radians(a); ax.text(hw * 0.97 * math.cos(t), hw * 0.97 * math.sin(t), "slot\n槽", fontsize=5.5, color="#555", ha="center", va="center")
    ax.set_xlim(-hw, hw); ax.set_ylim(-hw, hw); ax.set_aspect("equal")
    ax.set_title(title, fontsize=8.5, loc="left"); ax.tick_params(labelsize=6.5); ax.grid(color="#eee", lw=0.5)

def part_sheet(p, idx, total):
    no, fn, en, zh, mat_en, mat_zh, status = p
    fig = plt.figure(figsize=(8.5, 11), dpi=200)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    header(bg, no, en, zh, status)
    iso = os.path.join(ISO, fn + ".png")
    if os.path.exists(iso):
        a = fig.add_axes([0.03, 0.62, 0.40, 0.245]); a.imshow(plt.imread(iso)); a.axis("off")
        bg.text(0.05, 0.86, "New part (3D) · 新零件", fontsize=8.5, color="#444")
    table(bg, SUMMARY[no], 0.45, 0.858)
    bg.text(0.45, 0.858 - 0.036 * (len(SUMMARY[no]) + 1) + 0.008, "Everything not listed: no change · 未列出的都不改", fontsize=8.5, color="#444", va="top")
    old, new = load(OLD, fn), load(NEW, fn)
    pp = PANELS[no]
    if pp["prof"]:
        ax = fig.add_axes([0.08, 0.13, 0.30, 0.45])
        draw(ax, section(new, ang=PROF), True); draw(ax, section(old, ang=PROF), False)
        ax.set_xlim(*pp["prof"][0]); ax.set_ylim(*pp["prof"][1])
        ax.set_title(f"Section at {PROF:g}° (radial) · {PROF:g}° 径向剖", fontsize=8.5, loc="left")
        ax.set_xlabel("distance from oven centre (mm) · 距中心", fontsize=7.5); ax.set_ylabel("height z (mm) · 高度", fontsize=7.5)
        ax.tick_params(labelsize=6.5); ax.grid(color="#eee", lw=0.5)
        pax = fig.add_axes([0.44, 0.13, 0.52, 0.45])
    else:
        pax = fig.add_axes([0.15, 0.13, 0.70, 0.45])
    zo, zn, hw, title = pp["plan"]
    plan_ax(pax, no, old, new, zo, zn, hw, title)
    footer(bg, no, en, zh, mat_en, mat_zh, idx, total)
    out = os.path.join(SHD, f"{no}_{fn.split('_', 1)[1] if no != 'S' else fn}.png")
    fig.savefig(out, dpi=200); plt.close(fig); print("sheet", out)
    return out

def overview(total):
    fig = plt.figure(figsize=(8.5, 11), dpi=200)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    bg.add_patch(MRect((0.03, 0.915), 0.94, 0.07, fc="#1f3f73", ec="none"))
    bg.text(0.05, 0.965, "Heat & Clean Glass Oven · 加热清洁玻璃炉", color="white", fontsize=15, weight="bold", va="center")
    bg.text(0.05, 0.937, f"Change sheet 2026-11-12 · 改动总表   (page 1 / {total})", color="white", fontsize=10, va="center")
    bg.text(0.05, 0.897, HEAD_EN, fontsize=7.8, weight="bold"); bg.text(0.05, 0.881, HEAD_ZH, fontsize=8.4, weight="bold")
    y = 0.864
    for line in textwrap.wrap(NOTE_EN, 150): bg.text(0.05, y, line, fontsize=7.2); y -= 0.0125
    for line in textwrap.wrap(NOTE_ZH, 75): bg.text(0.05, y, line, fontsize=7.2); y -= 0.0125
    cols, rows = 4, 4; x0, y0, w, h = 0.035, 0.07, 0.93 / cols, (y - 0.075) / rows
    for i, p in enumerate(PARTS):
        no, fn, en, zh, _, _, status = p
        lab, col, fc = STAT[status]
        c, r = i % cols, i // cols
        X, Y = x0 + c * w, y0 + (rows - 1 - r) * h
        bg.add_patch(FancyBboxPatch((X + 0.004, Y + 0.004), w - 0.008, h - 0.008, boxstyle="round,pad=0,rounding_size=0.008",
                                    fc=fc, ec=col, lw=1.4 if status != "same" else 0.8))
        iso = os.path.join(ISO, fn + ".png")
        if os.path.exists(iso):
            a = fig.add_axes([X + 0.015, Y + 0.075, w - 0.03, h - 0.105]); im = plt.imread(iso)
            if status == "same": im = np.dstack([np.repeat(im[..., :3].mean(axis=2, keepdims=True), 3, axis=2) * 0.6 + 0.4, im[..., 3:]])
            a.imshow(im); a.axis("off")
        bg.text(X + 0.012, Y + h - 0.018, f"{no}", fontsize=11, weight="bold", color=BLUE_E if status != "same" else "#888")
        bg.text(X + w - 0.012, Y + h - 0.018, lab, fontsize=6.2, ha="right", weight="bold", color=col)
        bg.text(X + 0.012, Y + 0.058, f"{en}\n{zh}", fontsize=6.2, va="center", color="#111" if status != "same" else "#888")
        if status != "same":
            k = SUMMARY[no][0]
            bg.text(X + 0.012, Y + 0.022, f"{k[0]} {k[2]} → {k[3]}", fontsize=5.6, va="center", color=col)
    bg.text(0.05, 0.045, "Red = new shape (new drawing) · 红 = 形状改   Amber = same part, new place · 橙 = 零件不变，位置改   Grey = no change · 灰 = 不改", fontsize=7.2)
    bg.text(0.05, 0.03, "Bolts: 25 M6 (5 per ring ×5 rings, was 30), same heights. Leg screws M5 × 40 (were M6). · 螺栓：25 个 M6（每圈 5 个），高度不变；脚螺丝 M5 × 40", fontsize=7.2)
    out = os.path.join(REN, f"change_sheet_{TAG}.png"); fig.savefig(out, dpi=200); plt.close(fig); print("overview", out)

def before_after(idx, total):
    names = [p[1] for p in PARTS if p[0] in ("01", "02", "03", "04", "05")]
    fig = plt.figure(figsize=(8.5, 11), dpi=200)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    header(bg, "A", "Assembly: the top cap ring, before and after", "装配：顶环改前改后", "changed")
    # left: base wall stack section at PROF, old dashed over new solid, ceramic beige
    ax = fig.add_axes([0.08, 0.49, 0.86, 0.34])
    for n in names:
        draw(ax, section(load(NEW, n), ang=PROF), True, lw=0.8); draw(ax, section(load(OLD, n), ang=PROF), False, lw=0.8)
    z0, z1 = HP.seat_z + HP.base_disk_t_real, HP.seat_z + HP.ceramic_stack_real
    ax.add_patch(MRect((40.75, z0), 5.5, z1 - z0, fc=CER, ec="#8a7a55", lw=0.6, zorder=1))
    ytxt = 101
    ax.annotate("", xy=(46.25, ytxt - 3), xytext=(66.25, ytxt - 3), arrowprops=dict(arrowstyle="<->", lw=1.1, color=BLUE_E))
    ax.text(56.25, ytxt - 1.5, "ring 20.0 (new) · 新环宽", fontsize=8, ha="center", color=BLUE_E, weight="bold")
    ax.annotate("", xy=(46.25, ytxt + 3), xytext=(74.65, ytxt + 3), arrowprops=dict(arrowstyle="<->", lw=1.0, color=OLDC))
    ax.text(60.45, ytxt + 4.5, "ring 28.4 (old) · 旧环宽", fontsize=8, ha="center", color="#555")
    for (x, y), t, (tx, ty) in (((53.25, 40), "insulation 14.6 (was 20.6)\n保温层 14.6（旧 20.6）", (68.5, 52)),
                                ((63.15, 25), "air gap 3.0 (was 4.4)\n空气层 3.0（旧 4.4）", (68.5, 22))):
        ax.annotate(t, xy=(x, y), xytext=(tx, ty), fontsize=7.5, va="center", zorder=9,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=RED, lw=0.8),
                    arrowprops=dict(arrowstyle="-|>", color="#333", lw=0.8, mutation_scale=8))
    ax.set_xlim(36, 80); ax.set_ylim(-36, 110); ax.set_aspect("auto")
    ax.set_title(f"Base wall at {PROF:g}°: old dashed, new solid (not to scale across) · 底座壁 {PROF:g}° 剖：虚线旧，实线新", fontsize=9.5, loc="left")
    ax.set_xlabel("distance from oven centre (mm) · 距中心", fontsize=7.5); ax.tick_params(labelsize=6.5); ax.grid(color="#eee", lw=0.5)
    # bottom: plan of the bolt + leg pattern
    pax = fig.add_axes([0.06, 0.10, 0.42, 0.33])
    for r, c, ls in ((74.75, OLDC, (0, (4, 2.5))), (67.35, BLUE_E, "solid")): pax.add_patch(MCirc((0, 0), r, fill=False, ec=c, ls=ls, lw=1.0))
    pax.add_patch(MCirc((0, 0), 46.25, fc=CER, ec="#8a7a55", lw=0.6))
    for a in OLD_BOLTS: pax.plot(69.85 * math.cos(math.radians(a)), 69.85 * math.sin(math.radians(a)), "o", mfc="none", mec=OLDC, ms=6)
    for a in NEW_BOLTS: pax.plot(63.15 * math.cos(math.radians(a)), 63.15 * math.sin(math.radians(a)), "o", color=RED, ms=5); pax.text(80 * math.cos(math.radians(a)), 80 * math.sin(math.radians(a)), f"{a:g}°", fontsize=6, color=RED, ha="center", va="center")
    for a in OLD_LEGS: pax.plot(60 * math.cos(math.radians(a)), 60 * math.sin(math.radians(a)), "^", mfc="none", mec=OLDC, ms=6)
    for a in NEW_LEGS: pax.plot(54 * math.cos(math.radians(a)), 54 * math.sin(math.radians(a)), "^", color=BLUE_E, ms=6)
    pax.set_xlim(-90, 90); pax.set_ylim(-90, 90); pax.set_aspect("equal"); pax.axis("off")
    pax.set_title("Bolts ● and legs ▲ from above · 螺栓和脚俯视", fontsize=8.5, loc="left")
    bg.text(0.52, 0.40, "Bolts · 螺栓", fontsize=9, weight="bold")
    bg.text(0.52, 0.38, "old: 6 per ring at 52.4° + 60° (30 total)\n旧：每圈 6 个，52.4° + 60°（共 30）", fontsize=7.5, va="top", color="#555")
    bg.text(0.52, 0.345, "new: 5 per ring at 41.5° + 72° (25 total),\nbetween the glass slots\n新：每圈 5 个，41.5° + 72°（共 25），在玻璃槽之间", fontsize=7.5, va="top", color=RED)
    bg.text(0.52, 0.28, "Legs · 脚", fontsize=9, weight="bold")
    bg.text(0.52, 0.26, "old: r 60 at 40 / 160 / 280°, M6\n旧：r 60，40 / 160 / 280°，M6", fontsize=7.5, va="top", color="#555")
    bg.text(0.52, 0.225, "new: r 54 at 5.5 / 125.5 / 245.5°, M5 × 40\n新：r 54，5.5 / 125.5 / 245.5°，M5 × 40", fontsize=7.5, va="top", color=BLUE_E)
    bg.text(0.52, 0.18, "Overall Ø 149.5 → 134.7 (bottom cap + lid)\nØ 132.5 at the top cap ring\n整机外径 149.5 → 134.7；顶环 132.5", fontsize=7.5, va="top", weight="bold")
    bg.add_patch(MRect((0.03, 0.015), 0.94, 0.048, fc="none", ec="#333", lw=0.8))
    bg.text(0.04, 0.038, f"FAB_PACKAGE_{TAG} · Heat & Clean Glass Oven · sheet {idx} / {total} · mm · every part cut from its STEP file", fontsize=7.5, va="center")
    out = os.path.join(REN, f"ring_shrink_before_after_{TAG}.png"); fig.savefig(out, dpi=200); plt.close(fig); print("before/after", out)
    return out

def html(sheets):
    rows = "\n".join(f'<a href="{os.path.relpath(s, ROOT)}"><img src="{os.path.relpath(s, ROOT)}" loading="lazy"></a>' for s in sheets)
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Heat &amp; Clean Glass Oven: change sheets 2026-11-12</title>
<style>body{{margin:0;font-family:-apple-system,"PingFang SC",sans-serif;background:#eef1f5;color:#111}}
header{{padding:18px 22px;background:#1f3f73;color:#fff}} h1{{margin:0 0 6px;font-size:22px}} p{{margin:4px 0;font-size:15px}}
nav{{padding:10px 22px;font-size:15px}} nav a{{margin-right:14px}}
main{{display:flex;flex-direction:column;align-items:center;gap:18px;padding:18px}} main img{{width:min(100%,900px);background:#fff;box-shadow:0 2px 10px #0002}}</style></head>
<body><header><h1>Change 2026-11-12 · 改动 2026-11-12</h1><p>{HEAD_EN}</p><p>{HEAD_ZH}</p><p>{NOTE_EN}<br>{NOTE_ZH}</p></header>
<nav><a href="viewer-oven.html">Whole oven 3D · 整机</a><a href="viewer-base-full.html">Base · 底座</a><a href="viewer-lid-full.html">Lid · 盖子</a>
<a href="FAB_PACKAGE_{TAG}/README.txt">README</a></nav>
<main>
{rows}
</main></body></html>"""
    open(os.path.join(ROOT, f"change-sheets-{TAG}.html"), "w", encoding="utf-8").write(page)

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    if not os.environ.get("NO_ISO"): iso_renders()
    shown = [p for p in PARTS if p[6] != "same"]
    total = 2 + len(shown)
    sheets = []
    if not only or only == "overview": overview(total)
    if not only or only == "ba": sheets.append(before_after(2, total))
    for i, p in enumerate(shown):
        if only and only not in ("sheets", p[0]): continue
        sheets.append(part_sheet(p, i + 3, total))
    if not only:
        html([os.path.join(REN, f"change_sheet_{TAG}.png")] + sheets)
