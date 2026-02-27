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

Please provide:
1. Per-unit price at 100 qty
2. Tooling cost for top cap stamping die (one-time)
3. Lead time
4. Shipping estimate (sea freight to USA)
""")

    print(f"  FABRICATION_SPEC.md generated")

    # ── Summary ──────────────────────────────────────────────────
    total_files = copied_dxf + copied_3d + 2  # +2 for BOM.csv and SPEC.md
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
