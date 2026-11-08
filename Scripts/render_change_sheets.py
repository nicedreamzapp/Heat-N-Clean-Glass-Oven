"""2026-11-08 R2 change sheets, drawn from the STEP files themselves.

  R2: body +U (hnc_params.body_raise = 2.66 mm) ABOVE the seat so the REAL ceramic (core 90.4 + base plate 4.9 = 95.3,
  Matt's calipers) ends flush with the 05 top cap top. OLD = FAB_PACKAGE_2026-11-08 (R1), NEW = FAB_PACKAGE_2026-11-08-R2.
  Sections are cut from the real solids (build123d), iso pictures are headless Blender renders of the new STLs.
Run: .venv-cad/bin/python Scripts/render_change_sheets.py <old_R1_package_dir>
Out: Renders/change_sheet_2026-11-08-R2.png (overview), Renders/body_raise_before_after_2026-11-08-R2.png,
     Renders/change_sheets_2026-11-08-R2/<nn>_<name>.png, change-sheets-2026-11-08-R2.html
"""
import os, sys, math, subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle as MRect
from build123d import *
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hnc_params as HP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = "2026-11-08-R2"
OLD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "FAB_PACKAGE_2026-11-08")   # only as the "before" outline
NEW = os.path.join(ROOT, "FAB_PACKAGE_" + TAG)
REN = os.path.join(ROOT, "Renders"); SHD = os.path.join(REN, "change_sheets_" + TAG); ISO = os.path.join(SHD, "iso")
os.makedirs(ISO, exist_ok=True)
for f in ("/System/Library/Fonts/Hiragino Sans GB.ttc", "/System/Library/Fonts/Helvetica.ttc"):
    if os.path.exists(f): font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = ["Helvetica", "Hiragino Sans GB"]
plt.rcParams["axes.unicode_minus"] = False
U = HP.body_raise
BLUE, BLUE_E, OLDC, RED, CER, AMB = "#7fa6d9", "#1f3f73", "#9a9a9a", "#d0202a", "#efe6cf", "#d98a00"
f2 = lambda z: f"{z:.2f}".rstrip("0").rstrip(".")

# status: "changed" = new shape (new drawing), "moved" = same shape, sits U higher, "same" = no change
PARTS = [  # no, file, EN, ZH, material EN, ZH, status
 ("01", "01_Inner_Wall_Tube", "Inner Wall Tube", "内壁管", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", "changed"),
 ("02", "02_Outer_Perforated_Tube", "Outer Perforated Tube", "外冲孔管", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "changed"),
 ("03", "03_Support_Ring", "Support Ring", "支撑环", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", "same"),
 ("04", "04_Bottom_Cap", "Bottom Cap", "底盖", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "same"),
 ("05", "05_One_Piece_Top_Cap", "One-Piece Top Cap", "一体顶盖", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "moved"),
 ("06", "06_Lid_Inner_Tube", "Lid Inner Tube", "盖子内管", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", "moved"),
 ("07", "07_Lid_Outer_Perforated_Tube", "Lid Outer Perforated Tube", "盖子外冲孔管", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "moved"),
 ("08", "08_Lid_Top_Disk", "Lid Top Disk", "盖子顶盘", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "moved"),
 ("09", "09_Lid_Ceramic_Holder", "Lid Ceramic Holder", "盖子陶瓷托架", "304 or 430 SS, 0.8 mm", "304 或 430 不锈钢，0.8 mm", "moved"),
 ("10", "10_Lid_Handle", "Lid Handle", "提手", "304 SS rod Ø8", "304 不锈钢棒 Ø8", "moved"),
 ("11", "11_Lid_Hinge_Strap", "Lid Hinge Strap (placeholder)", "盖子铰链片（示意）", "304 SS, 1.2 mm", "304 不锈钢，1.2 mm", "moved"),
 ("13", "13_Hinge_Pin", "Hinge Pin (placeholder)", "铰链销（示意）", "304 SS rod Ø5", "304 不锈钢棒 Ø5", "moved"),
 ("14", "14_Steel_Tray", "Steel Tray", "钢托盘", "steel, 3 mm", "钢，3 mm", "same"),
 ("S", "Ceramic_Spacer_Ring", "Ceramic Spacer Rings: top + 2 lid (we supply)", "陶瓷垫环：顶部 + 盖子 2 个（我方提供）", "ceramic, 14 mm + 10 mm ×2", "陶瓷，14 mm + 10 mm ×2", "moved"),
]
STAT = {"changed": ("CHANGED · 已改", RED, "#fff1f0"), "moved": (f"MOVED UP {f2(U)} · 上移 {f2(U)}", AMB, "#fff7e0"),
        "same": ("no change · 不改", "#888", "#f0f0f0")}

def load(pkg, name):
    if name == "Ceramic_Spacer_Ring":      # top body spacer ring, as drawn in the viewers
        u = 0.0 if pkg == OLD else U
        ri, ro = 68.05, 72.05
        s = Pos(0, 0, 52 + u) * (Cylinder(ro, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)) - Cylinder(ri, 14, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        for a in [52.4 + 60 * k for k in range(6)]:
            s -= Rot(0, 0, a) * Pos((ri + ro) / 2, 0, 59 + u) * Rot(0, 90, 0) * Cylinder(3.3, 6)
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

def table(ax, rows, x, y, fs=9):
    c1, c2, c3 = x + 0.245, x + 0.335, x + 0.425
    ax.text(x, y, "Feature · 位置", fontsize=fs, weight="bold"); ax.text(c1, y, "Old · 旧", fontsize=fs, weight="bold", color="#666")
    ax.text(c2, y, "New · 新", fontsize=fs, weight="bold", color=BLUE_E); ax.text(c3, y, "Δ", fontsize=fs, weight="bold", color=RED)
    for i, (en, zh, o, n, d) in enumerate(rows):
        yy = y - 0.04 * (i + 1)
        ax.text(x, yy, f"{en}\n{zh}", fontsize=fs - 0.8, va="center")
        ax.text(c1, yy, o, fontsize=fs + 1, va="center", color="#666"); ax.text(c2, yy, n, fontsize=fs + 1, va="center", color=BLUE_E, weight="bold")
        ax.text(c3, yy, d, fontsize=fs + 1, va="center", color=RED, weight="bold")

# ── ceramics (beige): OLD = as drawn in R1 (core 5.06-92.2, base disk 6.0); NEW = the real one (base 4.9 + core 90.4) ──
CER_OLD = dict(bd=(-0.44, 5.56), core=(5.06, 92.2))
CER_NEW = dict(bd=(HP.seat_z, HP.seat_z + HP.base_disk_t_real), core=(HP.seat_z + HP.base_disk_t_real, HP.seat_z + HP.ceramic_stack_real))
def ceramic(ax, c, new=True, off=0.0, both=False):
    xs = [(40.75, 46.25)] + ([(-46.25, -40.75)] if both else [])
    for x0, x1 in xs:
        X0 = math.copysign(math.sqrt(max(x0 * x0 - off * off, 0)), x0) if off else x0
        X1 = math.copysign(math.sqrt(max(x1 * x1 - off * off, 0)), x1) if off else x1
        z0, z1 = c["core"]
        ax.add_patch(MRect((X0, z0), X1 - X0, z1 - z0, fc=CER if new else "none", ec="#8a7a55" if new else "#b08a3c",
                           lw=0.7, ls="solid" if new else (0, (4, 2.5)), zorder=1 if new else 5))

# panels: list of dict(ang, off, xlim, ylim, calls=[(new_xy, old_xy, text, label_xy)], title)
def spec(no):
    T = 91.0
    if no == "01": return [
        dict(ang=52.4, xlim=(58, 92), ylim=(40, 100), cer=False, calls=[
            ((67.25, T + U), (67.25, T), f"Top edge z {f2(T)} → {f2(T+U)}  (+{f2(U)})\nHeight 122.7 → {f2(122.7+U)}\n顶边 z {f2(T)} → {f2(T+U)}，高 122.7 → {f2(122.7+U)}", (73, 95)),
            ((67.25, 59 + U), (67.25, 59.0), f"Top M6 holes z 59 → {f2(59+U)}  (+{f2(U)})\n上排 M6 孔 z 59 → {f2(59+U)}", (73, 66)),
            ((67.25, 45), None, "Bottom + seat M6 rings (z −24, 2.15),\nbottom edge z −31.7: no change\n下排和座圈 M6 孔、底边：不变", (73, 47))],
            title="at 52.4° (bolt line) · 52.4° 螺栓线"),
        dict(ang=6.5, xlim=(58, 92), ylim=(40, 100), cer=False, calls=[
            ((67.25, 65.86 + U), (67.25, 65.86), f"Glass slot bottom (13.3 wide) z 65.86 → {f2(65.86+U)}\n玻璃槽底 z 65.86 → {f2(65.86+U)}  (+{f2(U)})", (73, 58))],
            title="at 6.5° (glass slot) · 6.5° 玻璃槽")]
    if no == "02": return [
        dict(ang=52.4, xlim=(58, 92), ylim=(40, 100), cer=False, calls=[
            ((72.65, T + U), (72.65, T), f"Top edge z {f2(T)} → {f2(T+U)}  (+{f2(U)})\nHeight 122.7 → {f2(122.7+U)}\n顶边 z {f2(T)} → {f2(T+U)}，高 122.7 → {f2(122.7+U)}", (77, 95)),
            ((72.65, 59 + U), (72.65, 59.0), f"Top M6 holes z 59 → {f2(59+U)}\n上排 M6 孔 z 59 → {f2(59+U)}", (77, 66)),
            ((72.65, 42), None, "Bottom + seat M6 rings, rows 1-2\n(below the seat ring): no change\n下排和座圈 M6 孔、第 1-2 排：不变", (75, 45))],
            title="at 52.4° (bolt line) · 52.4° 螺栓线"),
        dict(ang=HP.slot_positions[0], xlim=(58, 92), ylim=(40, 100), cer=False, calls=[
            ((72.65, 67.5 + U), (72.65, 67.5), f"Glass slot bottom z 67.5 → {f2(67.5+U)}  (+{f2(U)})\nslot depth 23.5: no change\n玻璃槽底 z 67.5 → {f2(67.5+U)}，槽深 23.5 不变", (75, 57))],
            title=f"at {HP.slot_positions[0]:.1f}° (glass slot) · 玻璃槽")]
    if no == "05":
        X = lambda r: math.sqrt(r * r - 5.85 ** 2)
        return [dict(ang=6.5, off=5.85, xlim=(36, 94), ylim=(58, 102), cer=True, calls=[
            ((X(60), 92.2 + U), (X(60), 92.2), f"Whole cap +{f2(U)}, same part. Cap top z 92.2 → {f2(92.2+U)}\n= real ceramic top (seat −0.44 + 95.3)\n整个顶盖上移 {f2(U)}，零件不变；顶面 = 真陶瓷顶面", (55, 99)),
            ((X(60), 67.26 + U), (X(60), 67.26), f"Groove bottom z 67.26 → {f2(67.26+U)}\n金属槽底 z 67.26 → {f2(67.26+U)}", (66, 62)),
            ((X(74.65), 53.66 + 10), (X(74.65), 51 + 10), f"Tabs + M6 holes z 59 → {f2(59+U)}\n折边片和 M6 孔 z 59 → {f2(59+U)}", (77, 76))],
            title="along the glass slot at 6.5°, through the groove wall · 沿 6.5° 玻璃槽（金属槽侧壁）")]
    lid = lambda ylim, calls: [dict(ang=52.4, xlim=(40, 92), ylim=ylim, cer=True, calls=calls, title="at 52.4° (bolt line) · 52.4° 螺栓线")]
    same = lambda xy, lab: (xy, (xy[0], xy[1] - U), f"Whole part +{f2(U)}, shape unchanged\n整个零件上移 {f2(U)}，形状不变", lab)
    if no == "06": return lid((88, 136), [same((67.25, 129.86), (73, 133)), ((67.25, 102.86), (67.25, 100.2), f"M6 holes z 100.2 / 120.2 → {f2(100.2+U)} / {f2(120.2+U)}\nM6 孔 z 100.2 / 120.2 → {f2(100.2+U)} / {f2(120.2+U)}", (73, 94))])
    if no == "07": return lid((88, 136), [same((72.65, 129.86), (75, 133)), ((72.65, 102.86), (72.65, 100.2), f"M6 holes z 100.2 / 120.2 → {f2(100.2+U)} / {f2(120.2+U)}\nM6 孔 z 100.2 / 120.2 → {f2(100.2+U)} / {f2(120.2+U)}", (75, 94))])
    if no == "08": return lid((108, 138), [same((60, 131.06), (62, 135.5)), ((74.15, 122.86), (74.15, 120.2), f"M6 holes z 120.2 → {f2(120.2+U)}\nM6 孔 z 120.2 → {f2(120.2+U)}", (78, 113))])
    if no == "09": return [dict(ang=54.0, xlim=(34, 92), ylim=(86, 114), cer=True, calls=[
            same((60, 92.2 + U + 0.4), (62, 111)),
            ((46.45, 92.2 + U), None, f"Sits on the cap top z {f2(92.2+U)}; ceramic lid disk on the\nflush ceramic top: no change in fit\n放在顶盖顶面 z {f2(92.2+U)}；配合不变", (35, 89))], title="at 54° · 54°")]
    if no == "10": return [dict(ang=144.4, xlim=(20, 70), ylim=(124, 166), cer=False, calls=[same((47.2, 160.06), (52, 163))], title="through a handle post at 144.4° · 144.4° 提手脚")]
    if no == "11": return [dict(ang=292.4, xlim=(55, 100), ylim=(86, 116), cer=False, calls=[same((74.5, 106.2 + U), (80, 113))], title="at 292.4° (hinge) · 292.4° 铰链")]
    if no == "13": return [dict(ang=302.64, xlim=(60, 95), ylim=(88, 112), cer=False, calls=[
            ((78.75, 98.2 + U), (78.75, 98.2), f"Pivot z 98.2 → {f2(98.2+U)}  (plan position unchanged)\n铰链轴 z 98.2 → {f2(98.2+U)}（平面位置不变）", (80, 108))], title="through the pin at 302.6° · 302.6° 销轴")]
    if no == "S": return [dict(ang=52.4, xlim=(60, 88), ylim=(46, 76), cer=False, calls=[
            ((70.05, 52 + U), (70.05, 52), f"Top ring z 52-66 → {f2(52+U)}-{f2(66+U)}; lid rings +{f2(U)} too\nsize + holes: no change\n顶部垫环上移 {f2(U)}；盖子垫环也上移；尺寸和孔不变", (61, 73)),
            ((70.05, 59 + U), (70.05, 59), "", (75, 50))], title="top spacer ring at 52.4° · 顶部垫环")]
    return None

ROWS_OLD = [9.3, 15.3, 21.3, 27.3, 33.3, 39.3, 45.3, 51.3, 69.3, 75.3]
SUMMARY = {
 "01": [("Height", "高度", "122.7", f2(122.7 + U), f"+{f2(U)}"), ("Top edge z", "顶边 z", "91", f2(91 + U), f"+{f2(U)}"),
        ("Top M6 ring z (6 holes)", "上排 M6 孔 z", "59", f2(59 + U), f"+{f2(U)}"), ("Glass slot bottom z (×4)", "玻璃槽底 z（×4）", "65.86", f2(65.86 + U), f"+{f2(U)}")],
 "02": [("Height", "高度", "122.7", f2(122.7 + U), f"+{f2(U)}"), ("Top M6 ring z (6 holes)", "上排 M6 孔 z", "59", f2(59 + U), f"+{f2(U)}"),
        ("Glass slot bottom z (×4)", "玻璃槽底 z（×4）", "67.5", f2(67.5 + U), f"+{f2(U)}"),
        ("Perf rows 3-10: first z", "冲孔 3-10 排：首排 z", "9.3", f2(9.3 + U / 2), f"+{f2(U / 2)}"),
        ("Perf rows 11-12: first z", "冲孔 11-12 排：首排 z", "69.3", f2(69.3 + U), f"+{f2(U)}")],
 "05": [("Bottom z", "底 z", "51", f2(51 + U), f"+{f2(U)}"), ("Top z", "顶 z", "92.2", f2(92.2 + U), f"+{f2(U)}"), ("Shape", "形状", "—", "same", "0")],
 "06": [("Bottom z", "底 z", "93", f2(93 + U), f"+{f2(U)}"), ("Top z", "顶 z", "127.2", f2(127.2 + U), f"+{f2(U)}"), ("Shape", "形状", "—", "same", "0")],
 "07": [("Bottom z", "底 z", "93", f2(93 + U), f"+{f2(U)}"), ("Top z", "顶 z", "127.2", f2(127.2 + U), f"+{f2(U)}"), ("Shape", "形状", "—", "same", "0")],
 "08": [("Bottom z", "底 z", "114.2", f2(114.2 + U), f"+{f2(U)}"), ("Top z", "顶 z", "128.4", f2(128.4 + U), f"+{f2(U)}"), ("Shape", "形状", "—", "same", "0")],
 "09": [("Bottom z", "底 z", "92.2", f2(92.2 + U), f"+{f2(U)}"), ("Top z", "顶 z", "106.2", f2(106.2 + U), f"+{f2(U)}"), ("Shape", "形状", "—", "same", "0")],
 "10": [("Bottom z", "底 z", "128.4", f2(128.4 + U), f"+{f2(U)}"), ("Top z", "顶 z", "157.4", f2(157.4 + U), f"+{f2(U)}"), ("Shape", "形状", "—", "same", "0")],
 "11": [("Bottom z", "底 z", "92.2", f2(92.2 + U), f"+{f2(U)}"), ("Top z", "顶 z", "106.2", f2(106.2 + U), f"+{f2(U)}"), ("Shape", "形状", "—", "same", "0")],
 "13": [("Pivot z", "铰链轴 z", "98.2", f2(98.2 + U), f"+{f2(U)}"), ("Shape", "形状", "—", "same", "0")],
 "S":  [("Top ring bottom z", "顶部垫环底 z", "52", f2(52 + U), f"+{f2(U)}"), ("Lid ring 1 bottom z", "盖子垫环 1 底 z", "95.2", f2(95.2 + U), f"+{f2(U)}"),
        ("Lid ring 2 bottom z", "盖子垫环 2 底 z", "115.2", f2(115.2 + U), f"+{f2(U)}"), ("Size, holes", "尺寸、孔", "—", "same", "0")],
}
HEAD_EN = f"Change 2026-11-08 R2: body +{f2(U)} mm above the seat so the real ceramic (95.3 mm with base plate) sits flush with the top cap"
HEAD_ZH = f"改动 2026-11-08 R2：座面以上机体加高 {f2(U)} mm，让真陶瓷（连底盘 95.3 mm）和顶盖齐平"
NOTE_EN = (f"Measured on the real ceramic: core 90.4 + base plate 4.9 = 95.3 mm; the R1 cap top left 92.64 mm, so the ceramic stood {f2(U)} mm proud and the lid could not close. "
           f"Only 01 and 02 change shape (+{f2(U)} taller). 05 and the whole lid are the same parts, {f2(U)} higher. 03, 04, 14, the seat and every bolt below it: no change.")
NOTE_ZH = (f"真陶瓷实测：加热芯 90.4 + 底盘 4.9 = 95.3 mm；R1 顶盖只留 92.64 mm，陶瓷高出 {f2(U)} mm，盖子合不上。"
           f"只有 01、02 形状改（加高 {f2(U)}）。05 和整个盖子零件不变，只是高 {f2(U)}。03、04、14、座面和下面的螺栓：不改。")

def iso_renders():
    stls = [os.path.join(NEW, "STL", p[1] + ".stl") for p in PARTS if p[0] != "S"]
    sp = os.path.join(ISO, "Ceramic_Spacer_Ring.stl")
    export_stl(load(NEW, "Ceramic_Spacer_Ring"), sp)
    subprocess.run(["/Applications/Blender.app/Contents/MacOS/Blender", "-b", "-P", os.path.join(ROOT, "Scripts", "blender_iso.py"), "--", ISO] + stls + [sp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(sp)

def header(bg, no, en, zh, status):
    lab, col, _ = STAT[status]
    bg.add_patch(MRect((0.03, 0.925), 0.94, 0.06, fc="#1f3f73", ec="none"))
    bg.text(0.05, 0.965, f"{no}  {en}", color="white", fontsize=17, weight="bold", va="center")
    bg.text(0.05, 0.94, zh, color="white", fontsize=13, va="center")
    bg.text(0.95, 0.965, lab, color="#ffd34d", fontsize=13, weight="bold", va="center", ha="right")
    bg.text(0.95, 0.94, "Change 2026-11-08 R2 · 改动", color="white", fontsize=10, va="center", ha="right")
    bg.text(0.05, 0.905, HEAD_EN, fontsize=8.3); bg.text(0.05, 0.89, HEAD_ZH, fontsize=8.3)

def footer(bg, no, en, zh, mat_en, mat_zh, idx, total):
    bg.add_patch(MRect((0.07, 0.071), 0.03, 0.008, fc=BLUE, ec=BLUE_E)); bg.text(0.105, 0.075, "New R2 · 新", fontsize=8, va="center")
    bg.plot([0.22, 0.25], [0.075, 0.075], color=OLDC, ls=(0, (4, 2.5)), lw=1.3); bg.text(0.255, 0.075, "Old 2026-11-08 (R1) · 旧", fontsize=8, va="center")
    bg.add_patch(MRect((0.43, 0.071), 0.03, 0.008, fc=CER, ec="#8a7a55")); bg.text(0.465, 0.075, "real ceramic 95.3 · 真陶瓷", fontsize=8, va="center")
    bg.annotate("", xy=(0.70, 0.075), xytext=(0.66, 0.075), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6)); bg.text(0.705, 0.075, "where it moved · 移动位置", fontsize=8, va="center")
    bg.add_patch(MRect((0.03, 0.015), 0.94, 0.048, fc="none", ec="#333", lw=0.8))
    for x in (0.25, 0.55, 0.80): bg.plot([x, x], [0.015, 0.063], color="#333", lw=0.6)
    bg.text(0.04, 0.05, "Part · 零件", fontsize=6.5, color="#666"); bg.text(0.04, 0.028, f"{no}  {en}\n{zh}", fontsize=7, va="center")
    bg.text(0.26, 0.05, "Material / thickness · 材料 / 厚度", fontsize=6.5, color="#666"); bg.text(0.26, 0.028, f"{mat_en}\n{mat_zh}", fontsize=7, va="center")
    bg.text(0.56, 0.05, "Package · 文件包", fontsize=6.5, color="#666"); bg.text(0.56, 0.028, f"FAB_PACKAGE_{TAG}\nHeat & Clean Glass Oven", fontsize=7, va="center")
    bg.text(0.81, 0.05, "Sheet · 页", fontsize=6.5, color="#666"); bg.text(0.81, 0.028, f"{idx} / {total}\nmm, not to scale · 单位 mm", fontsize=7, va="center")

def part_sheet(p, idx, total):
    no, fn, en, zh, mat_en, mat_zh, status = p
    panels = spec(no)
    fig = plt.figure(figsize=(8.5, 11), dpi=200)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    header(bg, no, en, zh, status)
    iso = os.path.join(ISO, fn + ".png")
    if os.path.exists(iso):
        a = fig.add_axes([0.03, 0.615, 0.42, 0.25]); a.imshow(plt.imread(iso)); a.axis("off")
        bg.text(0.05, 0.86, "New part (3D) · 新零件", fontsize=8.5, color="#444")
    table(bg, SUMMARY[no], 0.48, 0.858)
    bg.text(0.48, 0.858 - 0.04 * (len(SUMMARY[no]) + 1) + 0.005, "Everything not listed: no change · 未列出的都不改", fontsize=8.5, color="#444", va="top")
    old = load(OLD, fn); new = load(NEW, fn)
    n = len(panels); W = 0.87 / n
    for k, sp in enumerate(panels):
        ax = fig.add_axes([0.08 + k * W + (0.03 if n > 1 and k else 0), 0.135, W - (0.04 if n > 1 else 0), 0.455])
        off = sp.get("off", 0.0)
        so, sn = section(old, ang=sp["ang"], off=off), section(new, ang=sp["ang"], off=off)
        if sp.get("cer"):
            ceramic(ax, CER_NEW, True, off); ceramic(ax, CER_OLD, False, off)
        draw(ax, sn, True); draw(ax, so, False)
        for new_xy, old_xy, text, lab in sp["calls"]:
            if text: callout(ax, new_xy, text, lab, old_xy, fs=7.5 if n > 1 else 8.5)
            elif old_xy is not None:
                ax.annotate("", xy=new_xy, xytext=old_xy, arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6, mutation_scale=11), zorder=8)
        ax.set_xlim(*sp["xlim"]); ax.set_ylim(*sp["ylim"])
        ax.set_aspect("auto" if n > 1 else "equal")
        ax.set_title("Section " + sp["title"], fontsize=8.5 if n > 1 else 10, loc="left")
        ax.set_xlabel("distance from oven centre (mm) · 距中心", fontsize=7.5); ax.set_ylabel("height z (mm) · 高度", fontsize=7.5)
        ax.tick_params(labelsize=7); ax.grid(color="#eee", lw=0.5)
    footer(bg, no, en, zh, mat_en, mat_zh, idx, total)
    out = os.path.join(SHD, f"{no}_{fn.split('_', 1)[1] if no != 'S' else fn}.png")
    fig.savefig(out, dpi=200); plt.close(fig); print("sheet", out)
    return out

def overview(total):
    fig = plt.figure(figsize=(8.5, 11), dpi=200)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    bg.add_patch(MRect((0.03, 0.915), 0.94, 0.07, fc="#1f3f73", ec="none"))
    bg.text(0.05, 0.965, "Heat & Clean Glass Oven · 加热清洁玻璃炉", color="white", fontsize=15, weight="bold", va="center")
    bg.text(0.05, 0.937, f"Change sheet 2026-11-08 R2 · 改动总表   (page 1 / {total})", color="white", fontsize=10, va="center")
    bg.text(0.05, 0.897, HEAD_EN, fontsize=8.2, weight="bold"); bg.text(0.05, 0.881, HEAD_ZH, fontsize=8.6, weight="bold")
    import textwrap
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
            bg.text(X + 0.012, Y + 0.022, f"{k[0]} {k[2]} → {k[3]} ({k[4]})", fontsize=5.8, va="center", color=col)
    bg.text(0.05, 0.045, "Red = new shape (new drawing) · 红 = 形状改   Amber = same part, sits higher · 橙 = 零件不变，位置升高   Grey = no change · 灰 = 不改", fontsize=7.2)
    bg.text(0.05, 0.03, "Bolts: same M6 bolts and lengths. Top ring and both lid rings +" + f2(U) + "; bottom and seat rings: no change · 螺栓不变；上排和盖子螺栓上移，下排和座圈螺栓不动", fontsize=7.2)
    out = os.path.join(REN, f"change_sheet_{TAG}.png"); fig.savefig(out, dpi=200); plt.close(fig); print("overview", out)

def before_after(idx, total):
    names = [p[1] for p in PARTS if p[0] not in ("S", "14", "10", "11", "13")]
    fig = plt.figure(figsize=(8.5, 11), dpi=200)
    bg = fig.add_axes([0, 0, 1, 1]); bg.axis("off"); bg.set_xlim(0, 1); bg.set_ylim(0, 1)
    header(bg, "A", "Assembly: real ceramic vs top cap", "装配：真陶瓷和顶盖", "changed")
    real = (HP.seat_z + HP.base_disk_t_real, HP.seat_z + HP.ceramic_stack_real)
    for k, (pkg, lab, c, u) in enumerate(((OLD, "BEFORE (R1) · 改前", CER_OLD, 0.0), (NEW, "AFTER (R2) · 改后", CER_NEW, U))):
        secs = [section(load(pkg, n), ang=52.4) for n in names]
        cap_top = 92.2 + u; d = real[1] - cap_top
        for row in (0, 1):
            ax = fig.add_axes([0.07 + k * 0.47, 0.47, 0.42, 0.40] if row == 0 else [0.07 + k * 0.47, 0.14, 0.42, 0.27])
            for sc in secs: draw(ax, sc, True, lw=0.6 if row == 0 else 1.0)
            for x0 in (40.75, -46.25):
                ax.add_patch(MRect((x0, real[0]), 5.5, real[1] - real[0], fc=CER, ec="#8a7a55", lw=0.6, zorder=1))
            ax.add_patch(MRect((-46.25, HP.seat_z), 92.5, HP.base_disk_t_real, fc=CER, ec="#8a7a55", lw=0.6, zorder=1))
            ax.axhline(cap_top, color=BLUE_E, lw=0.7, ls=":"); ax.axhline(real[1], color=RED, lw=0.7, ls=":")
            if row == 0:
                ax.annotate("", xy=(-20, HP.seat_z), xytext=(-20, real[1]), arrowprops=dict(arrowstyle="<->", lw=1.0))
                ax.text(-18.5, 50, "real ceramic stack 95.3\n(core 90.4 + base 4.9)\n真陶瓷 95.3", fontsize=7.5, va="center")
                ax.annotate("", xy=(14, HP.seat_z), xytext=(14, cap_top), arrowprops=dict(arrowstyle="<->", lw=1.0, color=BLUE_E))
                ax.text(15.5, 20, f"seat → cap top\n座面 → 顶盖顶\n{cap_top - HP.seat_z:.2f}", fontsize=7.5, va="center", color=BLUE_E)
                ax.set_title(lab, fontsize=12, weight="bold", loc="left")
                ax.set_xlim(-82, 82); ax.set_ylim(-40, 112); ax.set_aspect("equal")
            else:
                ax.text(52, real[1] + 0.5, f"ceramic top z {real[1]:.2f}", fontsize=7.5, color=RED, va="bottom")
                ax.text(52, cap_top - 0.5, f"cap top z {cap_top:.2f}", fontsize=7.5, color=BLUE_E, va="top")
                msg = (f"ceramic {d:.2f} mm ABOVE the cap: lid cannot close\n陶瓷高出 {d:.2f} mm，盖子合不上" if d > 0.01
                       else "ceramic top flush with the cap top (0.00)\n陶瓷顶面和顶盖顶面齐平")
                ax.text(55, 81, msg, ha="center", fontsize=8, weight="bold", color=RED if d > 0.01 else "#1d6b2c",
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=RED if d > 0.01 else "#1d6b2c"))
                ax.set_title("Detail at the top cap · 顶盖局部", fontsize=9, loc="left")
                ax.set_xlim(30, 80); ax.set_ylim(76, 100); ax.set_aspect("equal")
            ax.grid(color="#eee", lw=0.5); ax.tick_params(labelsize=6.5)
    bg.text(0.05, 0.105, "Section through the bolt line at 52.4°, every part cut from its STEP file (lid off). Beige = the real ceramic as measured.", fontsize=7.5)
    bg.text(0.05, 0.09, "52.4° 螺栓线剖视（不含盖子），每个零件都从 STEP 文件切出。米色 = 实测真陶瓷。", fontsize=7.5)
    bg.add_patch(MRect((0.03, 0.015), 0.94, 0.048, fc="none", ec="#333", lw=0.8))
    bg.text(0.04, 0.038, f"FAB_PACKAGE_{TAG} · Heat & Clean Glass Oven · sheet {idx} / {total} · mm", fontsize=7.5, va="center")
    out = os.path.join(REN, f"body_raise_before_after_{TAG}.png"); fig.savefig(out, dpi=200); plt.close(fig); print("before/after", out)
    return out

def html(sheets):
    rows = "\n".join(f'<a href="{os.path.relpath(s, ROOT)}"><img src="{os.path.relpath(s, ROOT)}" loading="lazy"></a>' for s in sheets)
    page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Heat &amp; Clean Glass Oven: change sheets 2026-11-08 R2</title>
<style>body{{margin:0;font-family:-apple-system,"PingFang SC",sans-serif;background:#eef1f5;color:#111}}
header{{padding:18px 22px;background:#1f3f73;color:#fff}} h1{{margin:0 0 6px;font-size:22px}} p{{margin:4px 0;font-size:15px}}
nav{{padding:10px 22px;font-size:15px}} nav a{{margin-right:14px}}
main{{display:flex;flex-direction:column;align-items:center;gap:18px;padding:18px}} main img{{width:min(100%,900px);background:#fff;box-shadow:0 2px 10px #0002}}</style></head>
<body><header><h1>Change 2026-11-08 R2 · 改动 2026-11-08 R2</h1><p>{HEAD_EN}</p><p>{HEAD_ZH}</p><p>{NOTE_EN}<br>{NOTE_ZH}</p></header>
<nav><a href="viewer-complete.html">Whole oven 3D · 整机</a><a href="viewer-base-full.html">Base · 底座</a><a href="viewer-lid-full.html">Lid · 盖子</a>
<a href="FAB_PACKAGE_{TAG}/README.txt">README</a></nav>
<main>
{rows}
</main></body></html>"""
    open(os.path.join(ROOT, f"change-sheets-{TAG}.html"), "w", encoding="utf-8").write(page)

if __name__ == "__main__":
    only = os.environ.get("ONLY")
    if not os.environ.get("NO_ISO"): iso_renders()
    changed = [p for p in PARTS if p[6] != "same"]
    total = 2 + len(changed)
    sheets = []
    if not only or only == "overview": overview(total)
    if not only or only == "ba": sheets.append(before_after(2, total))
    for i, p in enumerate(changed):
        if only and only not in ("sheets", p[0]): continue
        sheets.append(part_sheet(p, i + 3, total))
    if not only:
        html([os.path.join(REN, f"change_sheet_{TAG}.png")] + sheets)
