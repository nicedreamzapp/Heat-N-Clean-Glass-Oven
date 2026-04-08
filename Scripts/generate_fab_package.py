"""
Generate a complete fabrication spec package for manufacturer quoting.
Creates a self-contained folder ready to zip and email.

Run: python generate_fab_package.py

Output: CAD Exports/Fabrication Package/
"""
import os
import sys
import csv
import shutil
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Paths ─────────────────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAD_DIR = os.path.join(PROJECT_DIR, "CAD Exports")
STL_DIR = os.path.join(CAD_DIR, "Individual Parts", "STL")
DXF_DIR = os.path.join(CAD_DIR, "Flat Patterns", "DXF")
OUT_DIR = os.path.join(CAD_DIR, "Fabrication Package")

# ── Dimensions (must match export_all_parts.py) ──────────────────
outer_diameter = 92.5
inner_diameter = 81.5
cylinder_height = 91
sheet_metal_thickness = 1.2
tray_thickness = 3.0
insulation_gap = 24.6

ceramic_outer_r = outer_diameter / 2          # 46.25
ceramic_inner_r = inner_diameter / 2          # 40.75
housing_inner_r = ceramic_outer_r + insulation_gap  # 70.85
housing_outer_r = housing_inner_r + sheet_metal_thickness  # 72.05
air_gap = 4
mesh_inner_r = housing_outer_r + air_gap      # 76.05
mesh_outer_r = mesh_inner_r + sheet_metal_thickness  # 77.25
cap_outer_r = mesh_outer_r + 1.5              # 78.75

slot_width = 10.5
slot_depth = 23.5
gaps = [46.25, 46.25, 46.25, 108.68]
circumference = math.pi * outer_diameter

housing_height = cylinder_height  # 91mm
lid_height = 35
leg_height = 25
hinge_pin_r = 2.5
hinge_pin_length = 25

# Flat pattern dimensions
inner_housing_flat_w = 2 * math.pi * housing_inner_r
inner_housing_flat_h = housing_height
outer_mesh_flat_w = 2 * math.pi * mesh_inner_r
outer_mesh_flat_h = housing_height
tray_flat_w = 477  # approximate
tray_flat_h = 285  # approximate

# ── BOM Data ─────────────────────────────────────────────────────
BOM = [
    {
        "part_no": "01A",
        "name": "Inner Housing Wall",
        "qty": 1,
        "material": "304 Stainless Steel",
        "thickness_mm": 1.2,
        "flat_size": f"{inner_housing_flat_w:.0f} x {inner_housing_flat_h:.0f} mm",
        "process": "Laser cut + roll to cylinder (R={:.1f}mm)".format(housing_inner_r),
        "notes": "4 slot cutouts (10.5x23.5mm stadium shape), 2 wire exit holes (8mm dia), 1 thermocouple hole (6mm dia at z=12mm)",
    },
    {
        "part_no": "01B",
        "name": "Outer Perforated Mesh",
        "qty": 1,
        "material": "304 Stainless Steel",
        "thickness_mm": 1.2,
        "flat_size": f"{outer_mesh_flat_w:.0f} x {outer_mesh_flat_h:.0f} mm",
        "process": "Laser cut perforations + roll to cylinder (R={:.1f}mm)".format(mesh_inner_r),
        "notes": "4mm dia holes, 6mm staggered spacing. 4 slot cutouts matching inner housing. Alternative: buy pre-perforated 304 SS sheet.",
    },
    {
        "part_no": "01C",
        "name": "Support Ring",
        "qty": 1,
        "material": "304 Stainless Steel",
        "thickness_mm": 1.2,
        "flat_size": "Annular ring + strip (see DXF)",
        "process": "Laser cut + bend",
        "notes": "Shelf ring + retaining wall. Connects inner housing to outer mesh at bottom. Weld to inner housing.",
    },
    {
        "part_no": "01D",
        "name": "Standoff Fins",
        "qty": 12,
        "material": "304 Stainless Steel",
        "thickness_mm": 1.2,
        "flat_size": "Small rectangular tabs (see DXF)",
        "process": "Laser cut",
        "notes": "12 fins welded between inner housing and outer mesh. Space evenly around circumference.",
    },
    {
        "part_no": "02",
        "name": "Bottom Cap",
        "qty": 1,
        "material": "304 Stainless Steel",
        "thickness_mm": 1.2,
        "flat_size": f"Disk OD {cap_outer_r*2:.0f}mm + lip strip + 5 tabs",
        "process": "Laser cut disk + roll 10mm lip + 5 screw tabs",
        "notes": "3x M6 clearance holes (6.6mm) for leg bolts at 40/160/280 deg. 5x M4 screw tabs for mounting to mesh shell.",
    },
    {
        "part_no": "03",
        "name": "Top Cap",
        "qty": 1,
        "material": "304 Stainless Steel",
        "thickness_mm": 1.2,
        "flat_size": f"Annular ring ID {ceramic_inner_r*2:.0f}mm OD {cap_outer_r*2:.0f}mm",
        "process": "STAMPED/FORMED compound curve + laser cut perforations + rolled lips",
        "notes": "CRITICAL: 4 U-shaped compound-curved grooves (10.5mm wide x 23.5mm deep) following ceramic element slots. "
                 "Requires custom stamping die or hydroforming. "
                 "Also has: 10mm outer lip, 3mm inner grab lip, 5mm insulation ridge at R=70.85mm, "
                 "5mm ceramic retaining ridge at R=46.25mm (between slots only), "
                 "ventilation perforations (4mm holes), 5x M4 screw tabs.",
    },
    {
        "part_no": "04",
        "name": "Lid Assembly",
        "qty": 1,
        "material": "304 Stainless Steel",
        "thickness_mm": 1.2,
        "flat_size": "6 sub-parts (see DXF)",
        "process": "Laser cut 6 sub-parts + weld together",
        "notes": "Inner cylinder, outer mesh cylinder, bottom ring, top disk, retaining wall (3.3mm), shelf. "
                 f"Handle: 2 posts + bar (4mm rod, 25mm tall, 50mm wide). Lid height: {lid_height}mm. "
                 "Hinge plate welded to lid outer wall.",
    },
    {
        "part_no": "05",
        "name": "Hinge Pin",
        "qty": 1,
        "material": "304 Stainless Steel",
        "thickness_mm": f"{hinge_pin_r*2:.0f}mm rod",
        "flat_size": f"{hinge_pin_length}mm length",
        "process": "Cut rod to length",
        "notes": "5mm diameter rod, 25mm long. Connects lid hinge to base hinge knuckles.",
    },
    {
        "part_no": "12",
        "name": "Steel Tray",
        "qty": 1,
        "material": "304 Stainless Steel",
        "thickness_mm": 3.0,
        "flat_size": f"~{tray_flat_w} x {tray_flat_h} mm",
        "process": "Laser cut + 4 brake bends (12mm lips)",
        "notes": "Base platform. 3x M6 clearance holes for leg bolts. Extended right side for controller box mounting. "
                 "Top + bottom lip bends (12mm height, 2mm thickness).",
    },
]

# ── Fastener Summary ─────────────────────────────────────────────
FASTENERS = [
    ("M6 x 40mm hex bolt", 3, "Leg mounting (through tray + foot + bottom cap)"),
    ("M6 nut", 3, "Leg mounting"),
    ("M6 washer (12mm OD)", 3, "Under tray for leg bolts"),
    ("M4 x 12mm pan head screw", 10, "Cap mounting (5 per cap x 2 caps)"),
]


def main():
    print("=" * 60)
    print("FABRICATION SPEC PACKAGE GENERATOR")
    print("=" * 60)

    # Create output directories
    os.makedirs(os.path.join(OUT_DIR, "DXF"), exist_ok=True)
    os.makedirs(os.path.join(OUT_DIR, "3D Reference"), exist_ok=True)
    print(f"\nOutput: {OUT_DIR}")

    # ── 1. Generate BOM.csv ──────────────────────────────────────
    bom_path = os.path.join(OUT_DIR, "BOM.csv")
    with open(bom_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "part_no", "name", "qty", "material", "thickness_mm",
            "flat_size", "process", "notes"
        ])
        writer.writeheader()
        for row in BOM:
            writer.writerow(row)
    print(f"  BOM.csv ({len(BOM)} parts)")

    # ── 2. Copy DXF flat patterns ────────────────────────────────
    dxf_files = [
        "01A_Inner_Housing_Flat.dxf",
        "01B_Outer_Mesh_Flat.dxf",
        "01C_Support_Ring_Flat.dxf",
        "02_Bottom_Cap_Flat.dxf",
        "03_Top_Cap_Flat.dxf",
        "04_Lid_Flat_Patterns.dxf",
        "12_Steel_Tray_Flat.dxf",
    ]
    copied_dxf = 0
    for fname in dxf_files:
        src = os.path.join(DXF_DIR, fname)
        dst = os.path.join(OUT_DIR, "DXF", fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied_dxf += 1
        else:
            print(f"  WARNING: Missing DXF: {fname}")
    print(f"  DXF flat patterns: {copied_dxf}/{len(dxf_files)} copied")

    # ── 3. Copy 3D reference files ───────────────────────────────
    stl_files = [
        "00_Complete_Assembly.stl",
        "01_Base_Body.stl",
        "02_Bottom_Cap.stl",
        "03_Top_Cap.stl",
        "04_Lid_Assembly.stl",
        "12_Steel_Tray.stl",
    ]
    copied_3d = 0
    for fname in stl_files:
        src = os.path.join(STL_DIR, fname)
        dst = os.path.join(OUT_DIR, "3D Reference", fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied_3d += 1
        else:
            print(f"  WARNING: Missing STL: {fname}")
    print(f"  3D reference STLs: {copied_3d}/{len(stl_files)} copied")

    # Copy assembly GLBs
    glb_files = [
        "Assembly_LidClosed.glb",
        "4_Metal_Parts.glb",
    ]
    for fname in glb_files:
        src = os.path.join(CAD_DIR, fname)
        dst = os.path.join(OUT_DIR, "3D Reference", fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied_3d += 1
        else:
            print(f"  WARNING: Missing GLB: {fname}")
    print(f"  Assembly GLBs: copied")

    # ── 4. Generate FABRICATION_SPEC.md ──────────────────────────
    spec_path = os.path.join(OUT_DIR, "FABRICATION_SPEC.md")
    with open(spec_path, "w", encoding="utf-8") as f:
        f.write("""# Nice Dreamz Heat & Clean Glass Oven
# Fabrication Specification Package

**Project:** Precision ceramic heating oven for glass pieces
**Company:** Nice Dreamz
**Quote Request:** 100 units, all sheet metal parts
**Date:** 2026-02-26

---

## FABRICATION FLEXIBILITIES — READ FIRST

We are flexible on the items below. Please use the cheapest equivalent option that
meets the listed constraints — the goal is to keep cost down without compromising
the parts that customers actually see or that mate against the ceramic chamber.

### 1. Perforation pattern (outer mesh)
- **Flexible:** hole size, spacing, and exact pattern.
- **Stock pre-perforated 304 SS sheet acceptable** — use whatever pattern you already
  carry in 1.2 mm thickness, target **35–45% open area**.
- Current drawings show Ø4 mm holes on 6 mm staggered centers as a reference only.
- **Hold:** outer mesh OD (154.5 mm), overall height, slot cutout positions, and
  seam location.

### 2. Material grade — hidden internal parts
- **Inner housing, support ring, and standoff fins** may be substituted to
  **430 stainless** instead of 304. Must still tolerate **870 °F continuous** service.
- **Hold 304 stainless** on all visible parts: outer perforated mesh, top cap,
  lid exterior, and steel tray.

### 3. Surface finish — hidden surfaces
- **Mill finish acceptable** on any surface that is not visible from the outside
  of the assembled product.
- **Hold #4 brushed finish** on: outer mesh, top cap, lid exterior, tray top.

### 4. Bend radius
- **Bottom cap lip, steel tray brake bends, and lid sub-parts:** 1.2–2.0 mm
  inside bend radius acceptable — use your standard tooling.
- **Hold 1.2 mm (1× T)** on the top cap only — its lips and ridges must mate
  cleanly with the ceramic.

### 5. Top cap construction — TWO-PIECE WELDED PREFERRED
- **Build the top cap as a flat ring with 4 welded U-channel pieces** in the
  slot positions instead of one stamped piece. **No custom stamping die required.**
- Weld seams on the top surface are acceptable as long as they are cleanly finished
  (ground flush, brushed to match).

### 6. Welding method
- **Shop's choice** on hidden seams — TIG, spot, laser, whatever is most efficient
  for your shop.
- **Visible welds must look clean:** top cap channels, outer mesh seam, hinge knuckles.

### 7. Standoff fin count
- Currently drawn with 12 standoff fins between inner housing and outer mesh.
- **8–10 fins acceptable** if structurally sufficient to maintain concentricity
  and the 4 mm air gap.

### 8. Leg bolt rotational position
- 3 legs evenly spaced (120° apart) at R = 65.85 mm — locked.
- **Exact rotation flexible** — the 40° / 160° / 280° angles shown on the drawing
  are a reference. Use whatever rotation is easiest for your tooling.

---

## 1. Order Summary

| Item | Detail |
|------|--------|
| Quantity | 100 units |
| Material | 304 Stainless Steel |
| Finish | Brushed / No. 4 finish |
| Sheet Thickness | 1.2mm (18 gauge) — all parts except tray |
| Tray Thickness | 3.0mm |
| Tolerances | +/- 0.5mm general, +/- 0.2mm on hole positions |

---

## 2. Bill of Materials (per unit)

| Part # | Name | Qty | Thickness | Process |
|--------|------|-----|-----------|---------|
""")
        for row in BOM:
            f.write(f"| {row['part_no']} | {row['name']} | {row['qty']} | {row['thickness_mm']}mm | {row['process']} |\n")

        f.write(f"""
**Total sheet metal parts per unit: {sum(r['qty'] for r in BOM)}**

See `BOM.csv` for complete details including flat pattern sizes and fabrication notes.

---

## 3. Critical Dimensions

| Dimension | Value | Description |
|-----------|-------|-------------|
| Ceramic OD | {outer_diameter} mm | Outer diameter of ceramic cylinder |
| Ceramic ID | {inner_diameter} mm | Inner bore (chamber opening) |
| Chamber Height | {cylinder_height} mm | Height of ceramic cylinder |
| Sheet Thickness | {sheet_metal_thickness} mm | All metal parts except tray |
| Tray Thickness | {tray_thickness} mm | Steel tray platform |
| Inner Housing R | {housing_inner_r} mm | Inner housing cylinder radius |
| Outer Housing R | {housing_outer_r} mm | Outer housing cylinder radius |
| Mesh Inner R | {mesh_inner_r} mm | Perforated mesh inner radius |
| Mesh Outer R | {mesh_outer_r} mm | Perforated mesh outer radius |
| Cap Outer R | {cap_outer_r} mm | Top/bottom cap outer radius |
| Insulation Gap | {insulation_gap} mm | Gap between ceramic and inner housing |
| Air Gap | {air_gap} mm | Gap between inner housing and mesh |
| Overall Outer Dia | {mesh_outer_r * 2} mm | Outer diameter of mesh shell |
| Lid Height | {lid_height} mm | Lid assembly total height |
| Leg Height | {leg_height} mm | Ceramic foot height |

---

## 4. Bend Specifications

| Parameter | Value |
|-----------|-------|
| Inside Bend Radius | 1.2mm (1x material thickness) |
| K-Factor | 0.44 |
| Tray Bend Radius | 3.0mm (1x material thickness) |

---

## 5. Part-by-Part Fabrication Notes

### 01A — Inner Housing Wall
- Flat rectangle rolled into cylinder at R={housing_inner_r}mm
- 4 stadium-shaped slot cutouts: {slot_width}mm wide x {slot_depth}mm deep
- 2 wire exit holes: 8mm diameter
- 1 thermocouple hole: 6mm diameter at z=12mm from bottom
- Seam weld along length after rolling

### 01B — Outer Perforated Mesh
- Flat rectangle rolled into cylinder at R={mesh_inner_r}mm
- Hundreds of 4mm diameter laser-cut holes in 6mm staggered pattern
- 4 slot cutouts matching inner housing positions
- **Alternative:** Purchase pre-perforated 304 SS sheet (4mm holes, 6mm stagger) and laser cut outline + slots only — significant cost saving
- Seam weld along length after rolling

### 01C — Support Ring
- Annular ring shelf connecting inner housing to outer mesh at bottom
- Includes retaining wall strip
- Weld to inner housing wall

### 01D — Standoff Fins (x12)
- Small rectangular tabs welded between inner housing and outer mesh
- Maintain concentricity and air gap spacing
- Evenly spaced around circumference

### 02 — Bottom Cap
- Flat disk (OD {cap_outer_r*2:.0f}mm) with 10mm rolled lip
- 3x M6 clearance holes (6.6mm dia) at 40, 160, 280 degrees for leg bolts
- 5x screw tabs with M4 holes for mounting to mesh shell
- Tabs extend radially outward from disk edge

### 03 — Top Cap (MOST COMPLEX PART)
**This part requires custom tooling (stamping die or hydroforming).**

- Annular ring from ID {ceramic_inner_r*2:.0f}mm to OD {cap_outer_r*2:.0f}mm
- **4 U-shaped compound-curved grooves** following ceramic element slot positions
  - Each groove: {slot_width}mm wide, {slot_depth}mm deep, stadium-shaped profile
  - Grooves dip down from the flat ring surface following the ceramic cylinder's slot contours
  - These are the most complex features — the ring surface undulates following 4 slot profiles
- 10mm outer lip (bent down around outside edge)
- 3mm inner grab lip at R={ceramic_inner_r}mm (holds ceramic disk from above)
- 5mm insulation ridge at R={housing_inner_r}mm (drops into insulation gap)
- 5mm ceramic retaining ridge at R={ceramic_outer_r}mm (between slots only — holds ceramic cylinder)
- Ventilation perforations: 4mm holes in flat areas between grooves
- 5x screw tabs with M4 holes for mounting to mesh shell

### 04 — Lid Assembly
- 6 laser-cut sub-parts welded together:
  1. Inner cylinder wall
  2. Outer mesh cylinder wall (perforated)
  3. Bottom ring
  4. Top disk
  5. Retaining wall (3.3mm height)
  6. Shelf ring
- Handle: 2 upright posts (4mm rod, 25mm tall) + crossbar (4mm rod, 50mm wide)
- Handle aligned parallel to hinge axis
- Hinge plate welded to outer wall
- Total height: {lid_height}mm

### 05 — Hinge Pin
- 5mm diameter stainless steel rod
- 25mm length
- Cut to length, deburr ends

### 12 — Steel Tray
- 3.0mm thick flat platform (~{tray_flat_w}x{tray_flat_h}mm)
- 4 brake bends forming 12mm tall lips on all sides (top and bottom lips)
- 3x M6 clearance holes matching leg positions
- Extended right side for controller box mounting area
- Corner relief cuts for clean bending

---

## 6. Fastener Specifications

| Fastener | Qty/Unit | Purpose |
|----------|----------|---------|
""")
        for name, qty, purpose in FASTENERS:
            f.write(f"| {name} | {qty} | {purpose} |\n")

        f.write(f"""
**Note:** Fasteners are sourced separately. Holes in sheet metal parts must match above specifications.

---

## 7. Assembly Overview

The oven assembles in this order:
1. **Chamber sub-assembly** (factory welded): Inner housing + outer mesh + standoff fins + support ring
2. **Bottom cap** screws onto chamber bottom with 5x M4 screws
3. **Top cap** screws onto chamber top with 5x M4 screws
4. **Lid** attaches via hinge pin to base hinge knuckles (welded to chamber)
5. **Ceramic internals** (cylinder, disks, coil, thermocouple) drop into chamber — sourced separately
6. **Legs** bolt through bottom cap and tray with M6 bolts
7. **Tray** sits under oven, controller box mounts to extended right side

---

## 8. Surface Finish

- All visible surfaces: **Brushed / No. 4 finish** (directional grain)
- Internal surfaces (inside chamber): standard mill finish acceptable
- No paint or coating required
- Deburr all laser-cut edges

---

## 9. DXF File Convention

All DXF flat patterns use the following layer convention:

| Layer | Color | Line Style | Meaning |
|-------|-------|------------|---------|
| CUT | Red (1) | Solid | Outer profiles and through-cuts |
| HOLE | Green (3) | Solid | Holes and perforations |
| BEND | Yellow (2) | Dashed | Fold/bend lines |
| LABEL | Cyan (4) | Solid | Part names and dimensions (do not cut) |
| CENTERLINE | Magenta (6) | Solid | Center marks and references (do not cut) |

---

## 10. File Manifest

| Folder | Contents |
|--------|----------|
| `DXF/` | 7 flat pattern files — laser cutting templates for all parts |
| `3D Reference/` | STL files of individual parts + GLB assembly views |
| `BOM.csv` | Bill of materials spreadsheet |
| `FABRICATION_SPEC.md` | This document |

---

## 11. Contact

**Nice Dreamz**
Quote request for 100 units of all sheet metal parts listed above.

**Sending to:** sales@tianruntools.com

Please provide:
1. Per-unit price at 100 qty
2. Any one-time tooling fees (top cap is now spec'd as welded sub-parts —
   no stamping die required, but flag any other tooling costs)
3. Lead time
4. Shipping estimate (sea freight to USA)

**Please review the FABRICATION FLEXIBILITIES section above** when preparing your
quote — there are several places where we have given you room to substitute
cheaper stock material or skip custom tooling.
""")

    print(f"  FABRICATION_SPEC.md generated")

    # ── 5. Generate FABRICATION_SPEC_中文.md (Chinese mirror) ──────
    spec_cn_path = os.path.join(OUT_DIR, "FABRICATION_SPEC_中文.md")
    with open(spec_cn_path, "w", encoding="utf-8") as f:
        f.write("""# Nice Dreamz 加热与清洁玻璃烤箱
# 制造规格说明书

**项目：** 玻璃配件精密陶瓷加热烤箱
**公司：** Nice Dreamz
**报价请求：** 100 件,所有钣金部件
**日期：** 2026-02-26

---

## 制造灵活性 — 请先阅读

以下项目我们可以灵活处理。请使用满足约束条件的最便宜的等效方案 ——
目标是降低成本,同时不影响客户实际看到的部件或与陶瓷腔体配合的部件。

### 1. 冲孔图案(外网)
- **灵活:** 孔的大小、间距和具体图案。
- **可使用现货预冲孔 304 不锈钢板** —— 使用您库存中 1.2 mm 厚度的任何
  图案,目标 **35–45% 开孔率**。
- 当前图纸显示 Ø4 mm 孔、6 mm 交错中心距,仅供参考。
- **必须保持:** 外网外径(154.5 mm)、整体高度、槽口位置和接缝位置。

### 2. 材料等级 —— 隐藏内部部件
- **内壳、支撑环和支撑筋** 可以使用 **430 不锈钢** 替代 304。
  必须仍能耐受 **870 °F(约 466 °C)连续** 工作温度。
- **必须保持 304 不锈钢** 用于所有可见部件:外冲孔网、顶盖、
  盖子外部和钢托盘。

### 3. 表面处理 —— 隐藏表面
- 任何从产品外部不可见的表面,**可接受毛坯轧制(mill finish)**。
- **必须保持 #4 拉丝处理** 用于:外网、顶盖、盖子外部、托盘顶部。

### 4. 折弯半径
- **底盖凸缘、钢托盘折弯和盖子子部件:** 可接受 1.2–2.0 mm
  内折弯半径 —— 使用您的标准模具。
- **仅顶盖必须保持 1.2 mm(1× T)** —— 其凸缘和凸起必须与陶瓷干净配合。

### 5. 顶盖结构 —— 优先选择两件焊接式
- **将顶盖制作成扁平环加 4 个 U 型槽焊接件**,焊接在槽位置,
  替代单件冲压件。**无需定制冲压模具。**
- 顶面焊缝可接受,只要打磨平整并刷拉丝处理与基材匹配。

### 6. 焊接方法
- **由车间自行选择** 隐藏接缝的焊接方法 —— TIG 焊、点焊、激光焊等。
- **可见焊缝必须美观:** 顶盖通道、外网接缝、铰链关节。

### 7. 支撑筋数量
- 当前图纸显示内壳与外网之间有 12 个支撑筋。
- 如果结构上足以保持同心度和 4 mm 空气间隙,**8–10 个支撑筋亦可接受**。

### 8. 腿部螺栓旋转位置
- 3 条腿在 R = 65.85 mm 半径上等距分布(120° 间距)—— 锁定。
- **精确旋转角度可灵活处理** —— 图纸上的 40° / 160° / 280°
  仅供参考。使用最便于您加工的任何旋转角度。

---

## 1. 订单概要

| 项目 | 详情 |
|------|------|
| 数量 | 100 件 |
| 材料 | 304 不锈钢(隐藏部件可用 430,见上方灵活性) |
| 表面处理 | 拉丝 / No. 4 处理(可见部件) |
| 板材厚度 | 1.2 mm(18 号规格)—— 除托盘外所有部件 |
| 托盘厚度 | 3.0 mm |
| 公差 | 一般 ±0.5 mm,孔位 ±0.2 mm |

---

## 2. 物料清单(每件)

| 部件号 | 名称 | 数量 | 厚度 | 工艺 |
|--------|------|-----|------|------|
""")
        # Translated process names
        process_cn = {
            "Laser cut + roll into cylinder + seam weld": "激光切割 + 卷成圆筒 + 接缝焊接",
            "Laser cut perforated sheet + roll + seam weld": "激光切割冲孔板 + 卷圆 + 接缝焊接",
            "Laser cut + form ring + weld to inner housing": "激光切割 + 成型圆环 + 焊接到内壳",
            "Laser cut tabs + weld to inner housing & outer mesh": "激光切割支撑筋 + 焊接到内壳和外网",
            "Laser cut disk + roll 10mm lip + 5 screw tabs": "激光切割圆盘 + 折 10mm 凸缘 + 5 个螺丝凸耳",
            "STAMPED/FORMED compound curve + laser cut perforations + rolled lips": "扁平环 + 4 个 U 型槽焊接件(灵活性 #5,无需冲压模具)+ 卷边",
            "Laser cut 6 sub-parts + weld together": "激光切割 6 个子部件 + 焊接组合",
            "Cut rod to length": "棒材切割至所需长度",
            "Laser cut + 4 brake bends (12mm lips)": "激光切割 + 4 处折弯(12mm 凸缘)",
        }
        part_name_cn = {
            "Inner Housing Wall": "内壳壁",
            "Outer Perforated Mesh": "外冲孔网",
            "Support Ring": "支撑环",
            "Standoff Fins": "支撑筋",
            "Bottom Cap": "底盖",
            "Top Cap": "顶盖",
            "Lid Assembly": "盖子组件",
            "Hinge Pin": "铰链销",
            "Steel Tray": "钢托盘",
        }
        for row in BOM:
            cn_name = part_name_cn.get(row['name'], row['name'])
            cn_proc = process_cn.get(row['process'], row['process'])
            f.write(f"| {row['part_no']} | {cn_name} | {row['qty']} | {row['thickness_mm']}mm | {cn_proc} |\n")

        f.write(f"""
**每件总钣金部件数: {sum(r['qty'] for r in BOM)}**

完整详情请参见 `BOM.csv`,包括平面图案尺寸和制造说明。

---

## 3. 关键尺寸

| 尺寸 | 数值 | 描述 |
|------|------|------|
| 陶瓷外径 | {outer_diameter} mm | 陶瓷圆筒外径 |
| 陶瓷内径 | {inner_diameter} mm | 内孔(腔体开口)|
| 腔体高度 | {cylinder_height} mm | 陶瓷圆筒高度 |
| 板材厚度 | {sheet_metal_thickness} mm | 除托盘外所有金属部件 |
| 托盘厚度 | {tray_thickness} mm | 钢托盘平台 |
| 内壳半径 | {housing_inner_r} mm | 内壳圆筒半径 |
| 外壳半径 | {housing_outer_r} mm | 外壳圆筒半径 |
| 网内半径 | {mesh_inner_r} mm | 冲孔网内半径 |
| 网外半径 | {mesh_outer_r} mm | 冲孔网外半径 |
| 顶/底盖外半径 | {cap_outer_r} mm | 顶盖/底盖外半径 |
| 隔热间隙 | {insulation_gap} mm | 陶瓷与内壳之间的间隙 |
| 空气间隙 | {air_gap} mm | 内壳与冲孔网之间的间隙 |
| 整体外径 | {mesh_outer_r * 2} mm | 冲孔网外壳的外径 |
| 盖子高度 | {lid_height} mm | 盖子组件总高度 |
| 腿部高度 | {leg_height} mm | 陶瓷腿高度 |

---

## 4. 折弯规格

| 参数 | 数值 |
|------|------|
| 内折弯半径 | 1.2 mm(1 倍材料厚度)|
| K 因子 | 0.44 |
| 托盘折弯半径 | 3.0 mm(1 倍材料厚度)|

注:可对底盖、托盘和盖子子部件灵活处理(见上方灵活性 #4)。

---

## 5. 各部件制造说明

### 01A —— 内壳壁
- 长方形板材卷成 R={housing_inner_r}mm 圆筒
- 4 处长椭圆形槽切口:{slot_width}mm 宽 × {slot_depth}mm 深
- 2 个走线出口孔:8mm 直径
- 1 个热电偶孔:6mm 直径,距底部 z=12mm 高度
- 卷成型后沿长度方向接缝焊接

### 01B —— 外冲孔网
- 长方形板材卷成 R={mesh_inner_r}mm 圆筒
- 大量 4mm 直径激光切割孔,6mm 交错图案
- 4 处槽口与内壳位置匹配
- **替代方案(推荐):** 购买现货预冲孔 304 不锈钢板(任何 35–45% 开孔率
  的图案均可),仅激光切割外形与槽口 —— 大幅节约成本
- 卷成型后沿长度方向接缝焊接

### 01C —— 支撑环
- 环形支撑环,在底部连接内壳与外网
- 包含一段保持壁
- 焊接到内壳壁

### 01D —— 支撑筋(×12,可减至 8–10)
- 焊接在内壳与外网之间的小型矩形支撑筋
- 用于保持同心度和空气间隙
- 沿圆周均匀分布

### 02 —— 底盖
- 平面圆盘(外径 {cap_outer_r*2:.0f}mm)+ 10mm 卷边
- 3 个 M6 通孔(6.6mm 直径),用于腿部螺栓
  (旋转角度灵活,见灵活性 #8)
- 5 个 M4 螺丝凸耳,用于安装到外网壳

### 03 —— 顶盖(灵活性 #5:两件焊接式)
**不再需要定制冲压模具。**

- 扁平环,内径 {ceramic_inner_r*2:.0f}mm,外径 {cap_outer_r*2:.0f}mm
- **4 个 U 型槽焊接件**,焊接在陶瓷加热槽位置
  - 每个槽件:{slot_width}mm 宽 × {slot_depth}mm 深,长椭圆形截面
  - 焊接到扁平环,焊缝打磨光洁并拉丝至与基材匹配
- 10mm 外卷边
- R={ceramic_inner_r}mm 处 3mm 内抓边(从上方固定陶瓷圆盘)
- R={housing_inner_r}mm 处 5mm 隔热脊(进入隔热间隙)
- R={ceramic_outer_r}mm 处 5mm 陶瓷保持脊(仅在槽之间)
- 通风孔:槽之间扁平区域的 4mm 孔
- 5 个 M4 螺丝凸耳,用于安装到外网壳

### 04 —— 盖子组件
- 6 个激光切割子部件焊接而成:
  1. 内圆筒壁
  2. 外冲孔圆筒壁
  3. 底环
  4. 顶圆盘
  5. 保持壁(3.3mm)
  6. 支撑环
- 把手:2 个立柱(4mm 棒,25mm 高)+ 横杆(4mm 棒,50mm 宽)
- 把手平行于铰链轴线
- 铰链板焊接到外壁
- 总高度:{lid_height}mm

### 05 —— 铰链销
- 5mm 直径不锈钢棒
- 25mm 长度
- 切割至长度,两端去毛刺

### 12 —— 钢托盘
- 3.0mm 厚扁平平台(约 {tray_flat_w}×{tray_flat_h}mm)
- 4 处折弯,在四边形成 12mm 高的凸缘(顶部和底部凸缘)
- 3 个 M6 通孔与腿部位置匹配
- 右侧加长用于安装控制器盒
- 折弯处带角部释放切口

---

## 6. 紧固件规格

| 紧固件 | 每件数量 | 用途 |
|--------|---------|------|
""")
        fastener_cn = {
            "M6 x 40mm hex bolt": "M6 × 40mm 六角螺栓",
            "M6 nut": "M6 螺母",
            "M6 washer (12mm OD)": "M6 垫圈(外径 12mm)",
            "M4 x 12mm pan head screw": "M4 × 12mm 盘头螺丝",
        }
        purpose_cn = {
            "Leg mounting (through tray + foot + bottom cap)": "腿部安装(穿过托盘 + 腿 + 底盖)",
            "Leg mounting": "腿部安装",
            "Under tray for leg bolts": "托盘下方用于腿部螺栓",
            "Cap mounting (5 per cap x 2 caps)": "顶/底盖安装(每盖 5 颗 × 2 盖)",
        }
        for name, qty, purpose in FASTENERS:
            cn_name = fastener_cn.get(name, name)
            cn_purpose = purpose_cn.get(purpose, purpose)
            f.write(f"| {cn_name} | {qty} | {cn_purpose} |\n")

        f.write(f"""
**注:** 紧固件单独采购。钣金部件上的孔必须符合上述规格。

---

## 7. 装配概要

烤箱按以下顺序装配:
1. **腔体子组件**(厂内焊接):内壳 + 外网 + 支撑筋 + 支撑环
2. **底盖** 用 5 颗 M4 螺丝拧到腔体底部
3. **顶盖** 用 5 颗 M4 螺丝拧到腔体顶部
4. **盖子** 通过铰链销与腔体焊接的铰链关节连接
5. **陶瓷内件**(圆筒、圆盘、线圈、热电偶)放入腔体 —— 单独采购
6. **腿部** 通过底盖和托盘用 M6 螺栓固定
7. **托盘** 放置于烤箱下方,控制器盒安装在右侧加长部分

---

## 8. 表面处理

- 所有可见表面:**拉丝 / No. 4 处理**(定向纹理)
- 隐藏内部表面:可接受标准毛坯轧制(灵活性 #3)
- 无需油漆或涂层
- 所有激光切割边缘需去毛刺

---

## 9. DXF 文件约定

所有 DXF 平面图案使用以下图层约定:

| 图层 | 颜色 | 线型 | 含义 |
|------|------|------|------|
| CUT | 红色(1)| 实线 | 外轮廓和通孔切割 |
| HOLE | 绿色(3)| 实线 | 孔和冲孔 |
| BEND | 黄色(2)| 虚线 | 折弯线 |
| LABEL | 青色(4)| 实线 | 部件名称和尺寸(请勿切割)|
| CENTERLINE | 品红(6)| 实线 | 中心标记和参考(请勿切割)|

---

## 10. 文件清单

| 文件夹/文件 | 内容 |
|------|------|
| `DXF/` | 7 个平面图案文件 —— 所有部件的激光切割模板 |
| `3D Reference/` | 各部件 STL 文件 + GLB 装配视图 |
| `BOM.csv` | 物料清单电子表格 |
| `FABRICATION_SPEC.md` | 英文规格说明书 |
| `FABRICATION_SPEC_中文.md` | 本文档 |

---

## 11. 联系方式

**Nice Dreamz**
请求以上所列全部钣金部件的 100 件报价。

**发送至:** sales@tianruntools.com

请提供以下信息:
1. 100 件数量的单件价格
2. 任何一次性模具费用(顶盖现规格为焊接子部件,无需冲压模具,
   但请告知任何其他模具成本)
3. 交货期
4. 海运至美国的运费估算

**准备报价时,请查阅上方"制造灵活性"部分** ——
我们已在多处为您留出空间,可替换更便宜的现货材料或省略定制模具。
""")

    print(f"  FABRICATION_SPEC_中文.md generated")

    # ── 6. Generate EMAIL_BODY.md (copy/paste email body) ─────────
    email_path = os.path.join(OUT_DIR, "EMAIL_BODY.md")
    with open(email_path, "w", encoding="utf-8") as f:
        f.write("""# Email Body — Copy & Paste Into Email Client

**To:** sales@tianruntools.com
**Subject:** 报价请求 — 304 不锈钢钣金件 100 件 / Quote Request — 304 SS Sheet Metal, 100 Units

---

## 中文版本(主体)

您好,

我是 Nice Dreamz 公司的 Matt。我们正在为一款新产品 ——
"加热与清洁玻璃烤箱" —— 寻找钣金件制造商,希望贵司能够提供报价。

**订单概要:**
- 产品:精密陶瓷加热烤箱(玻璃配件用)
- 数量:**100 件**(首批)
- 材料:304 不锈钢,1.2 mm 厚度,#4 拉丝处理
- 工艺:激光切割 + 折弯 + 焊接

附件中包含完整规格包(`Fabrication_Package.zip`),其中有:
- 完整规格说明书(中英文双语版)
- 7 个 DXF 激光切割文件
- 尺寸图 PDF
- BOM 物料清单
- 3D 装配预览(GLB 格式)

**完整项目文件**(包括陶瓷部件、控制器、参考照片等)请访问我们的 GitHub:
https://github.com/nicedreamzapp/Heat-N-Clean-Glass-Oven

---

### 我们的灵活性 —— 帮助您降低报价

为了让贵司能够给出最具竞争力的报价,我们在以下 8 个方面给予了灵活性。
**请尽量使用现货材料和标准工艺,以降低成本:**

1. **冲孔图案(外网):** 可使用您库存的任何 304 预冲孔板材
   (35–45% 开孔率即可),无需为我们定制冲孔。

2. **隐藏部件材料:** 内壳、支撑环、支撑筋可改用 **430 不锈钢**
   代替 304(只需耐受 870 °F 连续工作)。

3. **隐藏表面处理:** 看不见的表面可使用毛坯轧制(mill finish),
   无需拉丝。

4. **折弯半径:** 底盖、托盘和盖子子部件可使用您标准模具的
   1.2–2.0 mm 范围。

5. **顶盖工艺:** 不需要冲压模具!请将顶盖做成 **扁平环 + 4 个
   U 型槽焊接件**,大幅降低开模成本。

6. **焊接方法:** 隐藏接缝由贵司自行选择(TIG、点焊、激光焊均可),
   仅可见焊缝需打磨美观。

7. **支撑筋数量:** 当前图纸有 12 个,**8–10 个** 即可。

8. **腿部螺栓位置:** 3 条腿等距分布即可,旋转角度灵活。

---

请提供以下报价信息:
1. 100 件的单件价格
2. 任何一次性模具费用(顶盖已改为焊接式,不再需要冲压模具)
3. 交货期
4. 海运至美国的运费估算

如有任何疑问请随时联系我。期待与贵司的合作!

谢谢,
Matt
Nice Dreamz

---

## English Version (For Reference)

Hello,

I'm Matt from Nice Dreamz. We're looking for a sheet metal fabricator
for a new product — the **Heat & Clean Glass Oven** — and would like to
request a quote.

**Order summary:**
- Product: Precision ceramic heating oven (for glass accessories)
- Quantity: **100 units** (first batch)
- Material: 304 Stainless Steel, 1.2 mm thickness, #4 brushed finish
- Process: Laser cut + brake bend + weld

The attached `Fabrication_Package.zip` contains:
- Full specification document (bilingual EN/CN)
- 7 DXF laser cut files
- Dimensioned drawing PDFs
- BOM spreadsheet
- 3D assembly preview (GLB)

**Full project files** (ceramic parts, controller, reference photos, etc.)
are on our GitHub: https://github.com/nicedreamzapp/Heat-N-Clean-Glass-Oven

### Our Flexibilities — To Help You Lower the Quote

To get the most competitive quote, we are flexible on the following
**8 items**. Please use stock materials and standard processes wherever
possible to reduce cost:

1. **Perforation pattern (outer mesh):** Use any 304 pre-perforated
   sheet you stock (35–45% open area). No custom perforation needed.

2. **Hidden parts material:** Inner housing, support ring, and standoff
   fins may use **430 stainless** instead of 304 (must tolerate 870 °F
   continuous service).

3. **Hidden surface finish:** Mill finish acceptable on any surface
   not visible from the outside.

4. **Bend radius:** Bottom cap, tray, and lid sub-parts may use your
   standard tooling in the 1.2–2.0 mm range.

5. **Top cap construction:** **No stamping die required!** Build the
   top cap as a **flat ring + 4 welded U-channel pieces** — major
   tooling cost saving.

6. **Welding method:** Shop's choice on hidden seams (TIG, spot, laser).
   Only visible welds need to be cleanly finished.

7. **Standoff fin count:** Currently drawn with 12 — **8 to 10 is fine**.

8. **Leg bolt position:** 3 legs evenly spaced — exact rotation angles
   are flexible.

---

Please provide:
1. Per-unit price at 100 qty
2. Any one-time tooling fees (top cap is now welded — no stamping die)
3. Lead time
4. Shipping estimate (sea freight to USA)

Please reach out with any questions. Looking forward to working with you!

Thanks,
Matt
Nice Dreamz
""")

    print(f"  EMAIL_BODY.md generated")

    # ── Summary ──────────────────────────────────────────────────
    total_files = copied_dxf + copied_3d + 4  # +4 for BOM.csv, SPEC.md, SPEC_中文.md, EMAIL_BODY.md
    pkg_size = 0
    for dirpath, dirnames, filenames in os.walk(OUT_DIR):
        for fn in filenames:
            pkg_size += os.path.getsize(os.path.join(dirpath, fn))

    print(f"\n{'=' * 60}")
    print(f"PACKAGE READY: {OUT_DIR}")
    print(f"  Total files: {total_files}")
    print(f"  Package size: {pkg_size / 1024 / 1024:.1f} MB")
    print(f"{'=' * 60}")
    print(f"\nZip this folder and email to manufacturer for quoting.")


if __name__ == "__main__":
    main()
