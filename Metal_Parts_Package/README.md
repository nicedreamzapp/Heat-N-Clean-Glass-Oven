# Metal Parts — Nice Dreamz Heat & Clean Glass Oven

4 sheet-metal parts + hardware.  All 304 stainless steel, 1.2 mm thick, brushed finish.

---

## Fabrication Flexibilities — Read First

We are flexible on the items below. Use the cheapest equivalent that meets the
listed constraints — the goal is to keep cost down without compromising the
parts customers actually see or that mate against the ceramic chamber.

| # | Item | Flexible | Hold |
|---|------|----------|------|
| 1 | **Perforation pattern (outer mesh)** | Hole size, spacing, exact pattern. Stock pre-perforated 304 SS sheet acceptable, target 35–45% open area. | Outer mesh OD (154.5 mm), height, slot positions, seam location. |
| 2 | **Material grade — hidden parts** | Inner housing, support ring, standoff fins may use **430 stainless** instead of 304 (must tolerate 870 °F continuous). | 304 stainless on outer mesh, top cap, lid exterior, steel tray. |
| 3 | **Surface finish — hidden surfaces** | Mill finish acceptable on any surface not visible from outside. | #4 brushed on outer mesh, top cap, lid exterior, tray top. |
| 4 | **Bend radius** | 1.2–2.0 mm inside bend radius on bottom cap lip, tray brake bends, lid sub-parts — use standard tooling. | 1.2 mm (1× T) on top cap only. |
| 5 | **Top cap construction** | **Two-piece welded preferred** — flat ring + 4 welded U-channel pieces in slot positions. **No stamping die required.** | Weld seams ground flush and brushed to match. |
| 6 | **Welding method** | Shop's choice on hidden seams (TIG, spot, laser). | Visible welds clean: top cap channels, outer mesh seam, hinge knuckles. |
| 7 | **Standoff fin count** | 8–10 fins acceptable instead of the 12 drawn, if structurally sufficient. | Maintain 4 mm air gap and concentricity. |
| 8 | **Leg bolt rotational position** | Exact rotation flexible — drawn at 40° / 160° / 280° but any 120°-spaced rotation is fine. | 3 legs, evenly spaced, at R = 65.85 mm. |

---

## The 4 Parts

| # | Part | DXF File | Notes |
|---|------|----------|-------|
| 1 | **Chamber — Inner Housing** | `01A_Inner_Housing_Flat.dxf` | Rolled cylinder with slots |
| 2 | **Chamber — Outer Mesh** | `01B_Outer_Mesh_Flat.dxf` | Perforated ventilation wrap |
| 3 | **Chamber — Support Ring** | `01C_Support_Ring_Flat.dxf` | Connects inner housing to outer mesh |
| 4 | **Bottom Cap** | `02_Bottom_Cap_Flat.dxf` | Disc that seals the bottom |
| 5 | **Top Cap** | `03_Top_Cap_Flat.dxf` | Ring + collar at the top |
| 6 | **Lid Assembly** | `04_Lid_Flat_Patterns.dxf` | Hinged lid (multiple sub-parts in one DXF) |

Parts 1-3 make up the **chamber body** (one assembly piece).

---

## Hinge Assembly

The hinge is **built into the chamber body and lid** — the knuckle tabs are part of their flat patterns. No separate hinge bracket to fabricate.

**How it goes together:**

1. When you roll/bend the chamber body and lid, the hinge tabs form into small cylinders (knuckles)
2. The **chamber body has 2 knuckles** (outer pair, spaced 8.3 mm apart)
3. The **lid has 1 knuckle** (center) that slots between the two body knuckles
4. Slide a **5 mm diameter stainless steel pin** (29 mm long) through all three knuckles to connect them

**Hinge pin spec:**
- 5 mm diameter x 29 mm long
- 304 stainless steel rod (or dowel pin)
- Standard hardware — not laser-cut

**Result:** Lid flips open 95° (clamshell style), hinged at the back of the oven.

See `Dimensioned_Drawings/LidAssembly_Drawing.pdf` for the hinge location and dimensions.

---

## Hardware (standard, not fabricated)

- **Hinge Pin** — 5 mm dia x 29 mm, stainless steel rod
- **M6 Leg Screws** — 3x, mount ceramic feet to bottom cap
- **M4 Cap Screws** — secure top cap to chamber body

---

## What's in This Folder

```
Metal_Parts_Package/
  README.md                ← You are here
  4_Metal_Parts.glb        ← 3D view of all 4 parts + screws
  view_parts.py            ← Run this to open the 3D view (python3 view_parts.py)
  Flat_Patterns_DXF/       ← Laser-cut files (send to CNC/laser)
  Flat_Patterns_SVG/       ← Visual previews (open in any browser)
  Dimensioned_Drawings/    ← PDF drawings with exact dimensions
```

## Part Images

See `Part_Images/` for rendered views of each part:

| File | Part |
|------|------|
| `00_All_4_Metal_Parts.png` | All 4 parts in one image |
| `01_Chamber_Body.png` | Chamber body — front |
| `01_Chamber_Body_Back.png` | Chamber body — back (open interior) |
| `02_Bottom_Cap.png` | Bottom cap — top |
| `02_Bottom_Cap_Back.png` | Bottom cap — underside |
| `03_Top_Cap.png` | Top cap — front |
| `03_Top_Cap_Back.png` | Top cap — back (inner structure) |
| `04_Lid_Assembly.png` | Lid — outside |
| `04_Lid_Assembly_Back.png` | Lid — inside |
| `4_Metal_Parts.pdf` | **Printable PDF** — all 4 parts, front + back (8 pages) |

## Interactive 3D View

**Option A:** Run `python3 view_parts.py` — opens the 3D model automatically.

**Option B:** Drag `4_Metal_Parts.glb` into https://gltf-viewer.donmccurdy.com

## DXF Layer Convention

| Layer | Color | Meaning |
|-------|-------|---------|
| CUT | Red | Outer profiles, through-cuts |
| HOLE | Green | Bolt holes, vent perforations |
| BEND | Yellow | Fold/bend lines |
| LABEL | Cyan | Part names, dimensions (do not cut) |
| CENTERLINE | Magenta | Alignment marks (do not cut) |

---

## Material Spec

- **Material:** 304 Stainless Steel (430 acceptable on hidden internal parts — see Flexibilities)
- **Thickness:** 1.2 mm (18 gauge)
- **Finish:** Brushed (#4) on visible surfaces; mill finish acceptable on hidden surfaces

---

## Quote Recipient

**Sending to:** sales@tianruntools.com (Tianrun Tools)
