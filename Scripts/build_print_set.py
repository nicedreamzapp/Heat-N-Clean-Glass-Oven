"""PRINT_SET_2026-11-08-R2: plastic fit/display print set (Matt 2026-11-08).
12 metal parts copied from FAB_PACKAGE_2026-11-08-R2 (no 14 tray this round) + 6 ceramic solids drawn here
at the measured sizes (hnc_params + the viewer meshes). Fit check places each ceramic where the viewers put it.
R2: C1 core 90.4 tall and C2 base disk 4.9 thick (Matt's calipers on the real ceramic: stack 95.3), so on the print the
core top is flush with the 05 cap top. Writes README.txt (EN + 中文) and the zip.
Run: .venv-cad/bin/python Scripts/build_print_set.py"""
import os, sys, math, shutil, json
from build123d import *
sys.path.insert(0, os.path.dirname(__file__)); import hnc_params as P
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = "2026-11-08-R2"
PKG = os.path.join(ROOT, "FAB_PACKAGE_" + TAG); OUT = os.path.join(ROOT, "PRINT_SET_" + TAG)
if os.path.isdir(OUT): shutil.rmtree(OUT)
for d in ("STL", "STEP"): os.makedirs(os.path.join(OUT, d), exist_ok=True)
METAL = ["01_Inner_Wall_Tube", "02_Outer_Perforated_Tube", "03_Support_Ring", "04_Bottom_Cap", "05_One_Piece_Top_Cap",
         "06_Lid_Inner_Tube", "07_Lid_Outer_Perforated_Tube", "08_Lid_Top_Disk", "09_Lid_Ceramic_Holder",
         "10_Lid_Handle", "11_Lid_Hinge_Strap", "13_Hinge_Pin"]
for n in METAL: shutil.copy(os.path.join(PKG, "STL", n + ".stl"), os.path.join(OUT, "STL", n + ".stl"))

def solid(x): return x if not isinstance(x, ShapeList) else Compound(children=list(x))
def cyl(r, h, z0=0): return Pos(0, 0, z0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))
def ring(ri, ro, z0, z1): return cyl(ro, z1 - z0, z0) - cyl(ri, z1 - z0, z0)
def radial(ang, r_mid, z, rad, length): return Rot(0, 0, ang) * Pos(r_mid, 0, z) * Rot(0, 90, 0) * Cylinder(rad, length)
RO, RI, H = P.ceramic_outer_r, P.ceramic_inner_r, P.ceramic_core_h_real    # 46.25 / 40.75 / 90.4 (R2: real core)
U = P.body_raise                                                              # 2.66
BOLT = P.ring_screw_angles                                                    # 52.4 + n*60

# C1 heater core: tube, 4 glass slots (10.5 wide, 23.5 deep, R5.25 round bottom) at the hnc_params angles,
# thermocouple hole Ø6.4 at 314.6 deg z 8.2, helical heater-wire groove (30 wraps z 15.5-66.5, 1.0 wide, 0.6 deep, as the viewer mesh)
core = ring(RI, RO, 0, H)
sb = H - P.slot_depth                                       # 66.9 slot bottom (23.5 from the top)
for a in P.slot_positions:
    sl = Pos(0, 0, sb + P.slot_width / 2) * Box(RO + 3, P.slot_width, H, align=(Align.MIN, Align.CENTER, Align.MIN))
    sl += Pos(0, 0, sb + P.slot_width / 2) * Rot(0, 90, 0) * Cylinder(P.slot_width / 2, RO + 3, align=(Align.CENTER, Align.CENTER, Align.MIN))
    core -= Rot(0, 0, a) * sl
core -= radial(P.hole_position_angle, (RI + RO) / 2, P.hole_center_height, P.hole_diameter / 2, 12)
GROOVE = os.environ.get("HNC_GROOVE", "1") == "1"
if GROOVE:
    pitch = (P.groove_start_height - P.groove_end_height) / P.num_wraps     # 1.7
    hx = Helix(pitch, P.groove_start_height - P.groove_end_height, RO + 0.2, center=(0, 0, P.groove_end_height))
    p0 = hx @ 0; t0 = hx % 0
    pl = Plane(origin=p0, z_dir=t0, x_dir=(p0.X, p0.Y, 0))
    with BuildSketch(pl) as sk: Rectangle(1.6, 1.0)        # radial 45.65 .. 47.25 (0.6 into the wall, helix at r 46.45)
    sw = sweep(sk.sketch, path=hx, is_frenet=True)
    core = core - sw
core = solid(core)

def disk(t=6.0):   # base / lid disk as modelled: Ø92.5 body + raised centre Ø77 x 1.0 with a 0.5 taper, t overall
    pts = [(0, 0), (38.5, 0), (38.5, 1.0), (46.25, 1.5), (46.25, t), (0, t)]
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ): Polygon(*pts, align=None)
        revolve(axis=Axis.Z)
    return bp.part
def spacer(h):   # ID 136.1 / OD 144.1, 6 radial Ø6.6 holes at mid height on the bolt angles
    ri, ro = 68.05, 72.05
    s = ring(ri, ro, 0, h)
    for a in BOLT: s -= radial(a, (ri + ro) / 2, h / 2, 3.3, 8)
    return solid(s)
def foot():      # Ø20 x 20 post on a Ø28 x 5 base, Ø6.6 leg-screw hole through
    f = cyl(14, 5) + cyl(10, 20, 5)
    return solid(f - cyl(3.3, 30, -1))
CER = {"C1_Ceramic_Heater_Core": core, "C2_Ceramic_Base_Disk": disk(P.base_disk_t_real), "C3_Ceramic_Lid_Disk": disk(),
       "C5_Spacer_Ring_10mm": spacer(10), "C6_Ceramic_Foot": foot()}
info = {}
for n, s in CER.items():
    export_step(s, os.path.join(OUT, "STEP", n + ".step")); export_stl(s, os.path.join(OUT, "STL", n + ".stl"))
    bb = s.bounding_box(); info[n] = [round(bb.size.X, 1), round(bb.size.Y, 1), round(bb.size.Z, 1), len(s.solids()), round(s.volume, 1)]
    print("wrote", n, info[n])
json.dump(info, open("/tmp/print_info.json", "w"))

# ── fit check in the assembly frame (viewer positions) ─────────────────────────────────────────────────────────
if os.environ.get("HNC_FIT", "1") != "1": sys.exit(0)
metal = {n: solid(import_step(os.path.join(PKG, "STEP", n + ".step"))) for n in METAL + ["14_Steel_Tray"]}
CORE_Z = P.seat_z + P.base_disk_t_real                     # 4.46: core on the 4.9 base disk on the seat
placed = {"core": Pos(0, 0, CORE_Z) * core, "basedisk": Pos(0, 0, P.seat_z) * CER["C2_Ceramic_Base_Disk"],
          "liddisk": Pos(0, 0, 91.2 + U) * CER["C3_Ceramic_Lid_Disk"]}
# 2026-11-10 (Matt): one ring size, 10 mm x 5, each centred on its bolt line (body rings were 14 mm)
for k, z0 in (("sp_bot", -29.0), ("sp_seat", -2.85), ("sp_top", 54.0 + U)): placed[k] = Pos(0, 0, z0) * CER["C5_Spacer_Ring_10mm"]
for k, z0 in (("sp_low", 95.2 + U), ("sp_high", 115.2 + U)): placed[k] = Pos(0, 0, z0) * CER["C5_Spacer_Ring_10mm"]
cap_top = metal["05_One_Piece_Top_Cap"].bounding_box().max.Z
print("FLUSH core top", round(CORE_Z + H, 3), "cap top", round(cap_top, 3), "diff", round(CORE_Z + H - cap_top, 3))
for i, a in enumerate((40, 160, 280)):
    placed["foot%d" % i] = Pos(60 * math.cos(math.radians(a)), 60 * math.sin(math.radians(a)), -56.7) * CER["C6_Ceramic_Foot"]
for k, s in placed.items():
    bb = s.bounding_box()
    for n, m in metal.items():
        mb = m.bounding_box()
        if bb.max.Z < mb.min.Z or bb.min.Z > mb.max.Z: continue
        x = s & m; v = x.volume if x is not None else 0
        if v > 0.01: print("CLASH", k, n, round(v, 2), "mm3")
for i, a in enumerate(list(placed)):
    for b in list(placed)[i + 1:]:
        x = placed[a] & placed[b]; v = x.volume if x is not None else 0
        if v > 0.01: print("CLASH", a, b, round(v, 2), "mm3")
# bolt lines (M6 Ø6) through every spacer ring + both tubes: must hit no ceramic
zs = {"sp_bot": -24.0, "sp_seat": 2.15, "sp_top": 59.0 + U, "sp_low": 100.2 + U, "sp_high": 120.2 + U}
for k, zb in zs.items():
    for a in BOLT:
        rod = radial(a, 70.0, zb, 3.0, 14)
        x = rod & placed[k]; v = x.volume if x is not None else 0
        if v > 0.01: print("BOLT BLOCKED", k, a, round(v, 2))
for i, a in enumerate((40, 160, 280)):
    rod = Pos(60 * math.cos(math.radians(a)), 60 * math.sin(math.radians(a)), -70) * cyl(3.0, 44)
    x = rod & placed["foot%d" % i]; v = x.volume if x is not None else 0
    if v > 0.01: print("LEG SCREW BLOCKED", i, round(v, 2))
print("fit check done")

# ── README (EN + 中文) from the files themselves, then the zip ─────────────────────────────────────────────────────
import trimesh
NAMES = {"01_Inner_Wall_Tube": ("Inner Wall Tube", "内壁管", 1), "02_Outer_Perforated_Tube": ("Outer Perforated Tube", "外冲孔管", 1),
         "03_Support_Ring": ("Support Ring", "支撑环", 1), "04_Bottom_Cap": ("Bottom Cap", "底盖", 1),
         "05_One_Piece_Top_Cap": ("One-Piece Top Cap", "一体顶盖", 1), "06_Lid_Inner_Tube": ("Lid Inner Tube", "盖子内管", 1),
         "07_Lid_Outer_Perforated_Tube": ("Lid Outer Perforated Tube", "盖子外冲孔管", 1), "08_Lid_Top_Disk": ("Lid Top Disk", "盖子顶盘", 1),
         "09_Lid_Ceramic_Holder": ("Lid Ceramic Holder", "盖子陶瓷托架", 1), "10_Lid_Handle": ("Lid Handle", "提手", 1),
         "11_Lid_Hinge_Strap": ("Lid Hinge Strap (placeholder)", "铰链片(示意)", 1), "13_Hinge_Pin": ("Hinge Pin (placeholder)", "铰链销(示意)", 1),
         "C1_Ceramic_Heater_Core": ("Ceramic Heater Core", "陶瓷加热芯", 1), "C2_Ceramic_Base_Disk": ("Ceramic Base Disk", "陶瓷底盘", 1),
         "C3_Ceramic_Lid_Disk": ("Ceramic Lid Disk", "陶瓷盖盘", 1),
         "C5_Spacer_Ring_10mm": ("Ceramic Spacer Ring 10 mm", "陶瓷垫圈 10mm", 5), "C6_Ceramic_Foot": ("Ceramic Foot", "陶瓷脚", 3)}
rows, big = [], (0, None)
for n, (en, zh, q) in NAMES.items():
    ext = trimesh.load(os.path.join(OUT, "STL", n + ".stl")).extents
    rows.append(f"{n + '.stl':<36}{en + ' ' + zh:<44}{q:>3}     {ext[0]:.1f} x {ext[1]:.1f} x {ext[2]:.1f}")
    if ext.max() > big[0]: big = (ext.max(), ext, n)
pieces = sum(q for _, _, q in NAMES.values()); files = len(NAMES)
bd = P.base_disk_t_real
txt = f"""HEAT & CLEAN GLASS OVEN - PLASTIC PRINT SET {TAG}
加热清洁玻璃烤炉 - 塑料打印套件 {TAG}

PLASTIC FIT / DISPLAY MODEL ONLY, NOT HEAT RATED. Do not heat or use it as an oven.
仅用于塑料试装 / 展示模型，不耐热。请勿加热或当作烤炉使用。

R2 (replaces the earlier 2026-11-08 print set): the body is {U} mm taller above the ceramic seat, so the real ceramic
(core 90.4 + base plate {bd} = 95.3 mm, measured with calipers) ends flush with the top of the 05 top cap and the lid closes.
C1 is now 90.4 tall (was 91) and C2 is {bd} thick (was 6.0). On this print the C1 top is flush with the 05 cap top.
R2（替换之前的 2026-11-08 打印套件）：陶瓷座面以上的机体加高 {U} mm，真陶瓷（加热芯 90.4 + 底盘 {bd} = 95.3 mm，卡尺实测）
顶面和 05 顶盖顶面齐平，盖子可以合上。C1 现在高 90.4（原来 91），C2 厚 {bd}（原来 6.0）。打印件上 C1 顶面和 05 顶盖顶面齐平。

All files in mm, true size (scale 100%). Metal parts are placed in their assembled position; the slicer can re-centre them.
所有文件单位为毫米，1:1 真实尺寸（100% 比例）。金属件按装配位置导出，切片软件可重新居中。
Metal parts copy the machining package FAB_PACKAGE_{TAG}. Sheet walls are 0.8 / 1.2 mm thick: print at true size, fine nozzle or resin.
金属件来自加工包 FAB_PACKAGE_{TAG}。板壁厚 0.8 / 1.2 mm：按真实尺寸打印，用细喷嘴或光固化。
Ceramic parts (C1-C6) are drawn at the measured ceramic sizes; STEP files for them are in STEP/.
陶瓷件（C1-C6）按实测陶瓷尺寸绘制，其 STEP 文件在 STEP/ 文件夹。

TOTAL: {pieces} pieces, {files} files.   合计：{pieces} 件，{files} 个文件。
Largest part {big[1][0]:.1f} x {big[1][1]:.1f} x {big[1][2]:.1f} mm ({big[2]}): every part fits a 256 x 256 x 256 mm bed.
最大零件 {big[1][0]:.1f} x {big[1][1]:.1f} x {big[1][2]:.1f} mm：全部零件可放入 256 x 256 x 256 mm 打印平台。

File                                Part / 零件                              Qty 数量  Size mm (x*y*z)
""" + "\n".join(rows) + f"""

Ceramic details / 陶瓷细节:
C1: OD 92.5 / ID 81.5, h {H}; 4 glass slots 10.5 wide x {P.slot_depth} deep, R5.25 round bottom, at 6.5 / 77.1 / 147.7 / 218.3 deg;
    thermocouple hole 6.4 at 314.6 deg, 8.2 high; heater-wire groove: helix, 30 turns from 15.5 to 66.5 high, 1.0 wide, 0.6 deep.
    外径 92.5 / 内径 81.5，高 {H}；4 个玻璃槽 宽 10.5 x 深 {P.slot_depth}，底部 R5.25 圆弧，角度 6.5 / 77.1 / 147.7 / 218.3 度；
    热电偶孔 6.4，314.6 度，高 8.2；加热丝螺旋槽：30 圈，高 15.5 至 66.5，宽 1.0，深 0.6。
C2: OD 92.5, {bd} overall: {bd - 1.5:.1f} body + raised centre 77.0 x 1.0 with a 0.5 taper. 外径 92.5，总厚 {bd}（{bd - 1.5:.1f} 主体 + 中间凸台 77.0 x 1.0，0.5 斜边）。
C3: OD 92.5, 6.0 overall: 4.5 body + raised centre 77.0 x 1.0 with a 0.5 taper. 外径 92.5，总厚 6.0（4.5 主体 + 中间凸台 77.0 x 1.0，0.5 斜边）。
C5 (all 5 rings, 3 body + 2 lid, 10 mm tall): ID 136.1 / OD 144.1, 6 radial holes 6.6 at mid height, at 52.4 + n x 60 deg. C5（全部 5 个垫圈，机体 3 个 + 盖子 2 个，高 10 mm）：内径 136.1 / 外径 144.1，6 个径向孔 6.6，位于中间高度，角度 52.4 + n x 60 度。
C6: post 20 x 20 on a base 28 x 5, leg screw hole 6.6 through. 立柱 20 x 20，底座 28 x 5，通孔 6.6 用于脚螺丝。

FASTENERS NOT INCLUDED, BUY THEM: 30 M6 bolts + nuts, 2 M4 screws (handle), 3 leg screws (M6).
紧固件不包含，请购买：30 套 M6 螺栓 + 螺母，2 个 M4 螺丝（提手），3 个脚螺丝（M6）。

Part 14 Steel Tray is NOT in this round (it stays in the design).
14 号钢托盘本次不打印（仍保留在设计中）。

Hinge 11 + 13 are placeholders; the real hinge is the factory's stock hinge.
11 和 13 铰链为示意件，实际使用工厂标准铰链。
"""
open(os.path.join(OUT, "README.txt"), "w", encoding="utf-8").write(txt)
ZIP = os.path.join(os.environ.get("HNC_ZIPDIR", "/tmp"), f"Heat-N-Clean_Print_Set_{TAG}.zip")   # uploaded to the wholesale site, not committed
if os.path.exists(ZIP): os.remove(ZIP)
import zipfile
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, _, fs in os.walk(OUT):
        for f in sorted(fs): z.write(os.path.join(dp, f), os.path.relpath(os.path.join(dp, f), ROOT))
print("README + zip", ZIP, os.path.getsize(ZIP))
