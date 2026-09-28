#!/usr/bin/env python3
"""
Generate the fabrication quote package for the FINAL (2026-06-10) design:
two-piece top cap (shell + clamp-fit hold-down ring), bolted strap hinge,
threaded-stud handle, NO welded fastenings anywhere (tube seam welds only).

Run: python Scripts/generate_fab_package.py
Output: CAD Exports/Fabrication Package/  (+ zip next to it)
"""
import os, csv, shutil, zipfile

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAD = os.path.join(PROJECT, "CAD Exports")
STL = os.path.join(CAD, "Individual Parts", "STL")
GLB = os.path.join(CAD, "Individual Parts", "GLB")
DXF_SRC = os.path.join(CAD, "Flat Patterns", "DXF")
OUT = os.path.join(CAD, "Fabrication Package")

# ---- key dimensions (must match export_all_parts.py) ----
T = 1.2                      # sheet thickness, mm
CER_OD, CER_ID, CER_H = 92.5, 81.5, 91.0
INNER_TUBE_ID, INNER_TUBE_OD = 141.7, 144.1
OUTER_TUBE_ID, OUTER_TUBE_OD = 152.1, 154.5
TUBE_H = 122.7
SPACER_ID, SPACER_OD = 144.1, 152.1
CAP_BLANK_OD = 157.5
SKIRT_DROP, FINGER_W, FINGER_REACH = 10, 12, 36   # finger: rim down to bolt line
RING_OD = 141.7

METAL_PARTS = [
    # (file base, EN name, CN name, qty, process EN, process CN, notes EN, notes CN)
    ("02_Bottom_Cap", "Bottom Cap", "底盖", 1,
     "Laser cut 1.2mm 304SS disk + formed lip",
     "激光切割 1.2mm 304 不锈钢圆片 + 成型翻边",
     f"Ø{CAP_BLANK_OD} blank. Fastened ONLY by the 6 long M6 ring bolts — no screws of its own.",
     f"Ø{CAP_BLANK_OD} 毛坯。仅由 6 颗加长 M6 环形螺栓固定——本体无需任何螺钉。"),
    ("01_Base_Body", "Body Tubes (inner wall + outer perforated)", "机体筒（内壁筒 + 外冲孔筒）", 1,
     "Laser cut 1.2mm 304SS, roll to cylinder, seam weld (the ONLY welds in the product)",
     "激光切割 1.2mm 304 不锈钢，卷圆，纵缝焊接（整机唯一的焊缝）",
     f"Inner tube ID {INNER_TUBE_ID} / OD {INNER_TUBE_OD}; outer tube ID {OUTER_TUBE_ID} / OD {OUTER_TUBE_OD}; height {TUBE_H}. Outer tube perforated Ø4 holes @ 6mm pitch. 4 glass slots cut from top edge, 10.5 wide x 23.5 deep. Radial M6 bolt holes at 3 ring heights, clocked 52.4° + n·60°.",
     f"内筒内径 {INNER_TUBE_ID} / 外径 {INNER_TUBE_OD}；外筒内径 {OUTER_TUBE_ID} / 外径 {OUTER_TUBE_OD}；高 {TUBE_H}。外筒冲 Ø4 孔、孔距 6mm。顶边切 4 个玻璃槽口，宽 10.5、深 23.5。三个高度的径向 M6 螺栓孔，角度 52.4° + n·60°。"),
    ("04a_Cap_Shell", "Cap Shell", "顶盖壳", 1,
     "Laser cut 1.2mm 304SS + spin/press the 10mm skirt + bend down 6 fingers",
     "激光切割 1.2mm 304 不锈钢 + 旋压/冲压 10mm 裙边 + 折弯 6 个垂下指片",
     f"ONE sheet-metal part: flat top (vent holes Ø4, 4 slot openings), {SKIRT_DROP}mm skirt, six {FINGER_W}mm-wide fingers reaching {FINGER_REACH}mm below the rim with Ø3.6 bolt holes (these take the existing top-ring M6 bolts — NO separate cap screws). The finger at 292.4° also extends UP past the rim and curls into two Ø8 hinge barrels (piano-hinge style) for the Ø5 pin.",
     f"单件钣金：平顶（Ø4 通风孔、4 个槽口）、{SKIRT_DROP}mm 裙边、6 个宽 {FINGER_W}mm 的指片向下延伸 {FINGER_REACH}mm，带 Ø3.6 螺栓孔（共用顶部环形 M6 螺栓——无需单独顶盖螺钉）。292.4° 处指片同时向上延伸并卷成两个 Ø8 铰链卷筒（钢琴铰链式），配 Ø5 销轴。"),
    ("04b_Cap_HoldDown_Ring", "Ceramic Hold-Down Ring", "陶瓷压紧环", 1,
     "Laser cut 1.2mm 304SS ring + form 3 short walls (or machine from tube stock)",
     "激光切割 1.2mm 304 不锈钢环 + 成型 3 圈短壁（或用管料车削）",
     f"OD {RING_OD}, flat top, 4 slot notches. Three hanging walls: bore lip (3mm), ceramic-OD flaps (10mm), chamber-edge wall (6mm). NO fasteners — clamped between Cap Shell and chamber when the cap bolts down.",
     f"外径 {RING_OD}，顶面平整，4 个槽口缺口。三圈下垂短壁：内孔唇边（3mm）、贴陶瓷外径的扣片（10mm）、贴炉膛内壁的外缘壁（6mm）。无任何紧固件——顶盖锁紧时被夹持在顶盖壳与炉膛之间。"),
    ("04_Lid_Assembly", "Lid (twin-wall, same construction as body)", "上盖（双层壁，结构与机体相同）", 1,
     "Laser cut 1.2mm 304SS, roll, seam weld tubes; flat disks laser cut",
     "激光切割 1.2mm 304 不锈钢，卷圆 + 纵缝焊接；平面圆片激光切割",
     "Inner + outer perforated tubes, top disk, ceramic holder. Two M6 bolt ring heights, same clocking as body.",
     "内筒 + 外冲孔筒、顶圆片、陶瓷托。两个高度的 M6 螺栓环，角度与机体相同。"),
    ("05b_Lid_Hinge_Strap", "Lid Hinge Strap", "上盖铰链带", 1,
     "Laser cut 1.2mm 304SS strip, bend, curl one Ø8 barrel",
     "激光切割 1.2mm 304 不锈钢带，折弯，卷一个 Ø8 卷筒",
     "Small strap, 2 holes — bolts UNDER the lid's existing M6 bolt at 292.4°. Its barrel sits between the Cap Shell's two barrels. NOT welded.",
     "小钢带，2 孔——压在上盖 292.4° 处现有 M6 螺栓之下固定。其卷筒位于顶盖壳两个卷筒之间。非焊接。"),
    ("05_Hinge_Pin", "Hinge Pin", "铰链销", 1,
     "Ø5 304SS rod, 30mm, one end bent or clipped",
     "Ø5 304 不锈钢圆棒，长 30mm，一端折弯或卡簧",
     "Slides through the 3 hinge barrels.", "穿过 3 个铰链卷筒。"),
    ("12_Steel_Tray", "Steel Tray", "钢托盘", 1,
     "Laser cut 3mm 304SS + bend", "激光切割 3mm 304 不锈钢 + 折弯",
     "Unchanged from previous quote.", "与上次询价相同。"),
]

CERAMICS = [
    ("06_Ceramic_Cylinder", "Ceramic Heater Core", "陶瓷加热芯", 1,
     f"OD {CER_OD} / ID {CER_ID} / H {CER_H}, 4 slots 10.5 x 23.5"),
    ("07_Ceramic_Base_Disk", "Ceramic Base Disk", "陶瓷底片", 1, f"Ø{CER_OD} x 6"),
    ("07b_Ceramic_Lid_Disk", "Ceramic Lid Disk", "陶瓷盖片", 1, f"Ø{CER_OD} x 6"),
    ("SPACER_14", "Spacer Ring 14mm", "陶瓷垫环 14mm", 3,
     f"ID {SPACER_ID} / OD {SPACER_OD} x 14, 6x Ø6.6 radial holes @ 52.4°+n·60°"),
    ("SPACER_10", "Spacer Ring 10mm", "陶瓷垫环 10mm", 2,
     f"ID {SPACER_ID} / OD {SPACER_OD} x 10, 6x Ø6.6 radial holes @ 52.4°+n·60°"),
]

FASTENERS = [
    ("M6 short hex bolt", "M6 短六角螺栓", 18, "seat ring + 2 lid rings / 座环 + 上盖两环"),
    ("M6 long hex bolt", "M6 加长六角螺栓", 12, "top ring (clamps cap fingers) + bottom ring (clamps bottom cap) / 顶环（兼夹顶盖指片）+ 底环（兼夹底盖）"),
    ("M6 hex nut", "M6 六角螺母", 30, "inside the inner wall / 位于内壁内侧"),
    ("Handle nut (matches handle studs)", "提手螺母（配提手螺柱）", 2, "under the lid top disk / 位于上盖顶片之下"),
]

def spec_en():
    rows = "\n".join(
        f"| {n} | {q} | {p} | {x} |" for _, n, _, q, p, _, x, _ in METAL_PARTS)
    cer = "\n".join(f"| {n} | {q} | {d} |" for _, n, _, q, d in CERAMICS)
    fas = "\n".join(f"| {n} | {q} | {u.split(' / ')[0]} |" for n, _, q, u in FASTENERS)
    return f"""# Heat-N-Clean Glass Oven — Fabrication Spec (FINAL design, rev 2026-06-11)

This package supersedes ALL previous versions. The top cap, hinge, and every
fastening detail changed. Please quote from THIS package only.

> **Rev 2026-06-11 — please re-download.** The hinge was updated to a
> low-profile design (pivot lowered, knuckles repositioned along the hinge
> line) and the ceramic lid disk shelf is now flush. If you downloaded this
> package before June 11, discard it and re-download from the same link.
> The 3D models in THIS package are authoritative.

> **Scope: METAL PARTS ONLY.** We source all ceramic parts separately —
> please disregard them for this quote. They appear below for reference
> only, so the metal interfaces and slot positions make sense.

## Design philosophy — bolted assembly, not welded
- The ONLY welds in the product are the longitudinal seams of the rolled tubes.
- Every part attaches with M6 bolts + nuts, or is clamped. No welded bosses,
  no welded brackets, no welded hinge.
- Material: 304 stainless, 1.2mm sheet unless noted. #4 brushed on visible faces.

## Metal parts

| Part | Qty | Process | Key details |
|---|---|---|---|
{rows}

## Ceramic parts — REFERENCE ONLY, do NOT quote

We supply the ceramics ourselves. Listed only so the metal slot positions
and clearances make sense.

| Part | Qty | Dimensions (mm) |
|---|---|---|
{cer}

## Fasteners (standard hardware, quote separately or we source)

| Item | Qty/unit | Where |
|---|---|---|
{fas}

## Assembly logic (so the bolt holes make sense)
1. Tubes + spacer rings bolt together at 3 ring heights (radial M6, nut inside).
2. Bottom ring uses LONG bolts that also pass through the Bottom Cap lip.
3. Hold-Down Ring sits on the chamber top — no fasteners, it gets clamped.
4. Cap Shell drops over it; top ring LONG bolts pass through its 6 fingers.
5. Lid bolts together the same way; Hinge Strap bolts under one lid bolt;
   pin through the 3 barrels. Handle has threaded studs + 2 nuts.

## 3D files
- `3D Reference/` — STL per part + complete assembly GLB (open in any viewer)
- `DXF/` — flat patterns for the rolled/flat parts. NOTE: the Cap Shell
  flat pattern predates the 2026-06-11 hinge revision — its hinge tab is
  approximate. Please unfold the Cap Shell from the 3D model; the 3D model
  is authoritative, and we ask for your engineering CAD back before
  production in any case.

## Quote request — METAL PARTS ONLY (no ceramics)
- Unit price for the metal set at qty 50 / 100 / 500
- One-time tooling (spin/press die for the cap skirt, if needed)
- Lead time for first articles + production
"""

def spec_cn():
    rows = "\n".join(
        f"| {cn} | {q} | {pcn} | {xcn} |" for _, _, cn, q, _, pcn, _, xcn in METAL_PARTS)
    cer = "\n".join(f"| {cn} | {q} | {d} |" for _, _, cn, q, d in CERAMICS)
    fas = "\n".join(f"| {cn} | {q} | {u.split(' / ')[-1]} |" for _, cn, q, u in FASTENERS)
    return f"""# Heat-N-Clean 玻璃烤炉 — 加工规格书（最终设计版，2026-06-11 修订）

本资料包取代之前所有版本。顶盖、铰链及所有紧固方式均已更改，请仅按本包报价。

> **2026-06-11 修订 —— 请重新下载。** 铰链已改为低位设计（转轴高度降低、
> 卷筒沿铰链轴线移位），上盖陶瓷片托面改为平齐。如您在 6 月 11 日之前
> 下载过本资料包，请删除旧版，并通过原链接重新下载。本包内的 3D 模型
> 为最终依据。

> **报价范围：仅金属件。** 所有陶瓷件由我方另行采购，本次询价请忽略
> 陶瓷件。下文列出陶瓷件仅供参考，便于理解金属件的配合关系与槽口位置。

## 设计思路 —— 螺栓装配，非焊接
- 整机唯一的焊缝是卷圆筒体的纵向接缝。
- 所有零件均用 M6 螺栓 + 螺母连接，或为夹持配合。无焊接凸台、
  无焊接支架、无焊接铰链。
- 材料：304 不锈钢，未注明处板厚 1.2mm。可见面 #4 拉丝。

## 金属件

| 零件 | 数量 | 工艺 | 要点 |
|---|---|---|---|
{rows}

## 陶瓷件 —— 仅供参考，无需报价

陶瓷件由我方自行供应。列出仅为便于理解金属件的槽口位置与配合间隙。

| 零件 | 数量 | 尺寸 (mm) |
|---|---|---|
{cer}

## 紧固件（标准件，可单独报价或由我方采购）

| 项目 | 单台用量 | 位置 |
|---|---|---|
{fas}

## 装配逻辑（便于理解孔位）
1. 筒体与陶瓷垫环在 3 个高度用径向 M6 螺栓连接，螺母在内侧。
2. 底部一环使用加长螺栓，同时穿过底盖翻边将其固定。
3. 陶瓷压紧环放在炉膛顶部——无紧固件，靠夹持固定。
4. 顶盖壳罩上后，顶部一环的加长螺栓穿过其 6 个指片锁紧。
5. 上盖同样用螺栓装配；铰链带压在上盖一颗螺栓下固定；
   销轴穿过 3 个卷筒。提手自带螺柱，配 2 颗螺母。

## 3D 文件
- `3D Reference/` —— 每个零件的 STL + 整机 GLB
- `DXF/` —— 卷板/平板件展开图。注意：顶盖壳展开图为 2026-06-11 铰链
  修订之前的版本，其铰链翻边仅供参考。请贵司钣金工程师按 3D 模型
  重新展开；一切以 3D 模型为准，且投产前请将贵司工程图发回我方确认。

## 报价请求 —— 仅金属件（不含陶瓷件）
- 金属件整套 50 / 100 / 500 台的单价
- 一次性模具费（如顶盖裙边需旋压/冲压模）
- 首件及量产交期
"""

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "3D Reference"))
    os.makedirs(os.path.join(OUT, "DXF"))

    open(os.path.join(OUT, "FABRICATION_SPEC.md"), "w").write(spec_en())
    open(os.path.join(OUT, "FABRICATION_SPEC_中文.md"), "w").write(spec_cn())

    with open(os.path.join(OUT, "BOM.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["part", "name_en", "name_cn", "qty", "material"])
        for base, en, cn, q, *_ in METAL_PARTS:
            w.writerow([base, en, cn, q, "304SS"])
        for base, en, cn, q, d in CERAMICS:
            w.writerow([base, en, cn, q, "ceramic — REFERENCE ONLY, do not quote / 仅供参考，无需报价"])
        for en, cn, q, u in FASTENERS:
            w.writerow(["", en, cn, q, "A2 stainless"])

    for base, *_ in METAL_PARTS:
        src = os.path.join(STL, base + ".stl")
        if os.path.exists(src):
            shutil.copy(src, os.path.join(OUT, "3D Reference"))
    shutil.copy(os.path.join(GLB, "00_Complete_Assembly.glb"), os.path.join(OUT, "3D Reference"))
    for f in os.listdir(DXF_SRC):
        shutil.copy(os.path.join(DXF_SRC, f), os.path.join(OUT, "DXF"))

    zpath = os.path.join(CAD, "Heat-N-Clean_Fabrication_Package.zip")
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(OUT):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, CAD))
    print("Package:", OUT)
    print("Zip:", zpath, f"({os.path.getsize(zpath)/1e6:.1f} MB)")

if __name__ == "__main__":
    main()
