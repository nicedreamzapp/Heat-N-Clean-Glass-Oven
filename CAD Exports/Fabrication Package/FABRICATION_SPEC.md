# Nice Dreamz Heat & Clean Glass Oven
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
| 01A | Inner Housing Wall | 1 | 1.2mm | Laser cut + roll to cylinder (R=70.8mm) |
| 01B | Outer Perforated Mesh | 1 | 1.2mm | Laser cut perforations + roll to cylinder (R=76.0mm) |
| 01C | Support Ring | 1 | 1.2mm | Laser cut + bend |
| 01D | Standoff Fins | 12 | 1.2mm | Laser cut |
| 02 | Bottom Cap | 1 | 1.2mm | Laser cut disk + roll 10mm lip + 5 screw tabs |
| 03 | Top Cap | 1 | 1.2mm | STAMPED/FORMED compound curve + laser cut perforations + rolled lips |
| 04 | Lid Assembly | 1 | 1.2mm | Laser cut 6 sub-parts + weld together |
| 05 | Hinge Pin | 1 | 5mm rodmm | Cut rod to length |
| 12 | Steel Tray | 1 | 3.0mm | Laser cut + 4 brake bends (12mm lips) |

**Total sheet metal parts per unit: 20**

See `BOM.csv` for complete details including flat pattern sizes and fabrication notes.

---

## 3. Critical Dimensions

| Dimension | Value | Description |
|-----------|-------|-------------|
| Ceramic OD | 92.5 mm | Outer diameter of ceramic cylinder |
| Ceramic ID | 81.5 mm | Inner bore (chamber opening) |
| Chamber Height | 91 mm | Height of ceramic cylinder |
| Sheet Thickness | 1.2 mm | All metal parts except tray |
| Tray Thickness | 3.0 mm | Steel tray platform |
| Inner Housing R | 70.85 mm | Inner housing cylinder radius |
| Outer Housing R | 72.05 mm | Outer housing cylinder radius |
| Mesh Inner R | 76.05 mm | Perforated mesh inner radius |
| Mesh Outer R | 77.25 mm | Perforated mesh outer radius |
| Cap Outer R | 78.75 mm | Top/bottom cap outer radius |
| Insulation Gap | 24.6 mm | Gap between ceramic and inner housing |
| Air Gap | 4 mm | Gap between inner housing and mesh |
| Overall Outer Dia | 154.5 mm | Outer diameter of mesh shell |
| Lid Height | 35 mm | Lid assembly total height |
| Leg Height | 25 mm | Ceramic foot height |

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
- Flat rectangle rolled into cylinder at R=70.85mm
- 4 stadium-shaped slot cutouts: 10.5mm wide x 23.5mm deep
- 2 wire exit holes: 8mm diameter
- 1 thermocouple hole: 6mm diameter at z=12mm from bottom
- Seam weld along length after rolling

### 01B — Outer Perforated Mesh
- Flat rectangle rolled into cylinder at R=76.05mm
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
- Flat disk (OD 158mm) with 10mm rolled lip
- 3x M6 clearance holes (6.6mm dia) at 40, 160, 280 degrees for leg bolts
- 5x screw tabs with M4 holes for mounting to mesh shell
- Tabs extend radially outward from disk edge

### 03 — Top Cap (MOST COMPLEX PART)
**This part requires custom tooling (stamping die or hydroforming).**

- Annular ring from ID 82mm to OD 158mm
- **4 U-shaped compound-curved grooves** following ceramic element slot positions
  - Each groove: 10.5mm wide, 23.5mm deep, stadium-shaped profile
  - Grooves dip down from the flat ring surface following the ceramic cylinder's slot contours
  - These are the most complex features — the ring surface undulates following 4 slot profiles
- 10mm outer lip (bent down around outside edge)
- 3mm inner grab lip at R=40.75mm (holds ceramic disk from above)
- 5mm insulation ridge at R=70.85mm (drops into insulation gap)
- 5mm ceramic retaining ridge at R=46.25mm (between slots only — holds ceramic cylinder)
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
- Total height: 35mm

### 05 — Hinge Pin
- 5mm diameter stainless steel rod
- 25mm length
- Cut to length, deburr ends

### 12 — Steel Tray
- 3.0mm thick flat platform (~477x285mm)
- 4 brake bends forming 12mm tall lips on all sides (top and bottom lips)
- 3x M6 clearance holes matching leg positions
- Extended right side for controller box mounting area
- Corner relief cuts for clean bending

---

## 6. Fastener Specifications

| Fastener | Qty/Unit | Purpose |
|----------|----------|---------|
| M6 x 40mm hex bolt | 3 | Leg mounting (through tray + foot + bottom cap) |
| M6 nut | 3 | Leg mounting |
| M6 washer (12mm OD) | 3 | Under tray for leg bolts |
| M4 x 12mm pan head screw | 10 | Cap mounting (5 per cap x 2 caps) |

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
