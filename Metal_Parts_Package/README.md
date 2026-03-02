# Metal Parts — Nice Dreamz Heat & Clean Glass Oven

4 sheet-metal parts + hardware.  All 304 stainless steel, 1.2 mm thick, brushed finish.

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
  4_Metal_Parts.glb        ← 3D view of all 4 parts + screws (open in any GLB viewer)
  Flat_Patterns_DXF/       ← Laser-cut files (send to CNC/laser)
  Flat_Patterns_SVG/       ← Visual previews (open in any browser)
  Dimensioned_Drawings/    ← PDF drawings with exact dimensions
```

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

- **Material:** 304 Stainless Steel
- **Thickness:** 1.2 mm (18 gauge)
- **Finish:** Brushed
