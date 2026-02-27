# Nice Dreamz Heat & Clean Glass Oven

A self-cleaning glass oven for terp slurpers, bangers, ball vape heaters, and all glass parts. Features a custom ceramic heating element housed in an insulated dual-wall stainless steel enclosure with integrated controller box.

## Project Status

| Component | Status |
|-----------|--------|
| Ceramic heating core | **Tested & Working** |
| Electrical systems | **Verified** |
| Kanthal heating wire | **Performing as expected** |
| Stainless steel housing (2-piece base + cap) | **Designed & Modeled & Exported** |
| Insulated lid assembly (1-piece metal) | **Designed & Modeled & Exported** |
| Controller box (REX-C100, SSR, timer) | **Designed & Modeled & Exported** |
| Steel platform tray | **Designed & Modeled & Exported** |
| Wiring conduits (ceramic fiber wrapped) | **Designed & Modeled** |
| Dimensioned drawings (5 sheets) | **Complete** |
| Individual part STL/OBJ/GLB exports | **Complete (16 parts x 3 formats)** |
| Assembly & fastener decisions | **PENDING — see ASSEMBLY_QUESTIONS.md** |

---

## CAD Tools & Dependencies

```bash
pip install trimesh numpy
```
- **Trimesh**: 3D mesh creation and visualization for all assemblies
- **CadQuery**: Parametric modeling for ceramic components (STEP exports)
- **Matplotlib**: 2D dimensioned technical drawings

---

## Assembly Views

| Script | What it shows | How to run |
|--------|---------------|------------|
| `view_lid_open.py` | **Complete assembled unit** - lid open 72°, tray, controller, ceramic disk in lid | `python3 view_lid_open.py` |
| `view_lid_off.py` | **Lid removed view** - hinge facing outward, all screws + wiring visible | `python3 view_lid_off.py` |
| `render_blender.py` | **Photorealistic Blender render** - PBR materials, studio lighting | See usage in script header |

**Controls:** Drag to rotate, Scroll to zoom, Right-click drag to pan

---

## Design Overview

### Ceramic Core

| Parameter | Value |
|-----------|-------|
| Outer Diameter | 92.5 mm |
| Inner Diameter | 81.5 mm |
| Height | 91 mm |
| Wall Thickness | 5.5 mm |
| Ventilation Slots | 4 slots (10.5mm wide x 23.5mm deep, stadium-shaped) |
| Slot Gaps | 46.25, 46.25, 46.25, 108.68 mm |
| Heating Groove | 30 wraps, 1.2mm wide x 1mm deep (z=15.5 to 66.5mm) |
| Thermocouple Hole | 6.4mm dia, z=8.2mm center |

### Metal Housing - Base Body (Piece 1 of 2)

All welded together as one piece:

| Layer | Description | Radius |
|-------|-------------|--------|
| Support Ring | 10mm shelf under ceramic + retaining wall to z=3mm | 36.25-70.85mm (shelf) |
| Inner Housing | 1.2mm solid wall with wire holes + slot profiles | 70.85-72.05mm |
| Air Gap | 4mm ventilation passage | 72.05-76.05mm |
| Outer Perforated Mesh | 1.2mm with 4mm perforation holes | 76.05-77.25mm |
| Bottom Disk | 1.2mm with bolt holes + wire holes | 0-77.25mm |

- **Support ring**: lip at z=-6.7mm (sits UNDER ceramic base disk), shelf extends 10mm inward (r=36.25-70.85mm), retaining wall at ceramic_outer_r up to z=3mm (2mm below TC hole)
- **Leg bolt holes**: 3 holes at 40, 160, 280 degrees (r=65.85mm)
- **Wire holes**: 2 at groove_seam_angle (r=74.05mm), 1 TC hole

### Metal Housing - Top Cap (Piece 2 of 2)

Separate piece, form-fits ceramic slot contours:

| Feature | Description |
|---------|-------------|
| Flat Ring | Dips into each slot profile, from ceramic bore to cap_outer_r |
| Outer Lip | 10mm drop with extended side flanges near all 4 slots |
| Inner Grab Lip | 3mm drop into ceramic bore |
| Chamber Ridge | 5mm drop into insulation gap |
| Vent Perforations | 4mm holes in vent chamber area (housing to outer mesh) |

### Metal Lid Assembly (1 Piece)

| Feature | Description |
|---------|-------------|
| Inner Housing | 1.2mm solid wall, 35mm tall |
| Outer Perforated Mesh | 1.2mm with 4mm holes |
| Bottom Ring | Perforated in vent area, open center at ceramic_outer_r |
| Ceramic Pocket | Side wall at ceramic_outer_r (3.3mm tall, flush design) + retaining shelf (10mm inward) |
| Top Disk | Perforated in vent area matching bottom ring |
| Handle | Bridge-style, 50mm wide, 25mm tall posts + 4mm bar |

- Ceramic lid plate sits flush with lid base — body (4.5mm, 92.5mm OD) level with bottom ring, only lip (1mm, 76mm OD) extends below. Cemented with ceramic pasting agent
- No outer flange on bottom - sits flat flush on base
- Vent perforations on bottom ring, top disk, and side mesh for full airflow

### Airflow Path

Top cap vents -> base vent chamber -> lid bottom vents -> lid vent chamber -> lid top vents + side mesh

---

## Wiring System

| Component | Description |
|-----------|-------------|
| Kanthal Wire | Runs from coil ends to housing holes only |
| Ceramic Terminal Blocks | Small blocks inside air gap (kanthal to copper transition) |
| 16-Gauge Copper Wire | From terminal blocks, down through air gap |
| Ceramic Fiber Wrap | Around all internal wiring |
| External Conduits | Power + TC conduits from oven base to controller box |
| Grommets | Rubber grommets where conduits enter box bottom |

### Controller Box

| Component | Position |
|-----------|----------|
| REX-C100 PID Controller | Front panel, left |
| On/Off Rocker Switch | Front panel, center |
| 6hr Electrical Timer | Front panel, right |
| SSR Indicator LED | Front panel, below timer |
| Fuse Holder | Front panel, bottom right |
| SSR (Solid State Relay) | Inside box |
| Box Size | 160 x 100 x 70mm |

---

## Ceramic Legs

| Parameter | Value |
|-----------|-------|
| Count | 3 |
| Positions | 40, 160, 280 degrees |
| Body | 20mm dia ceramic, 20mm tall |
| Flange | 28mm dia base, 5mm thick |
| Mounting | M6 threaded insert at top, bolt through bottom disk |
| Platform | M5 screw through flange into steel tray |

---

## Key Dimensions Summary

| Parameter | Value |
|-----------|-------|
| Sheet Metal | 1.2mm (18 gauge stainless) |
| Ceramic OD | 92.5mm |
| Insulation Gap | 24.6mm |
| Housing Inner R | 70.85mm |
| Housing Outer R | 72.05mm |
| Air Gap | 4mm |
| Mesh Inner R | 76.05mm |
| Mesh Outer R | 77.25mm |
| Wall Thickness (ceramic to mesh) | 31mm |
| Support Ring lip_z | -6.7mm |
| Housing Bottom Z | -31.7mm |
| Lid Height | 35mm |

---

## Project Structure

```
CAD-Project/
├── README.md                             # Product showcase (Nice Dreamz branding)
├── view_lid_open.py                      # Lid open assembly view (72°)
├── view_lid_off.py                       # Lid removed view with all screws + wiring
├── render_blender.py                     # Blender photorealistic render script
├── Controller_Setup_Guide.md             # REX-C100 programming guide
│
├── CAD Exports/
│   ├── Assembly_LidOpen.glb              # Full assembly, lid open
│   ├── Assembly_LidOff.glb               # Full assembly, lid removed
│   ├── Individual Parts/
│   │   ├── STL/                          # 16 parts as binary STL
│   │   ├── OBJ/                          # 16 parts as OBJ
│   │   └── 3MF/                          # 16 parts as GLB
│   └── Flat Patterns/
│       ├── DXF/                          # Flat patterns for laser/waterjet
│       └── SVG/                          # Flat patterns for viewing
│
├── Ceramic Parts/
│   └── [6 STEP files - precision ceramic CAD]
│
├── Dimensioned Drawings/
│   ├── DimensionedDrawings.py            # Top Cap + Metal Body drawings
│   └── AdditionalDrawings.py             # Bottom Cap + Lid + Assembly drawings
│
├── Documentation/
│   ├── README.md                         # Technical design reference
│   ├── ASSEMBLY_QUESTIONS.md             # Fabrication decisions
│   ├── GLASS_HEAT_STATION.md             # Original design document
│   └── HOUSING_DESIGN.md                 # Housing design details
│
├── Reference Photos/                     # Problem/solution reference images
│
├── Renders/                              # Blender product renders (PNG)
│
└── Scripts/
    ├── export_all_parts.py               # Exports all 16 parts in STL/OBJ/GLB
    └── generate_flat_patterns.py         # DXF/SVG flat patterns for fabrication
```

---

## Regenerating Views & Exports

```bash
# Lid open assembly GLB
python3 view_lid_open.py

# Lid removed assembly GLB
python3 view_lid_off.py

# Export all 16 parts as STL/OBJ/GLB
python3 Scripts/export_all_parts.py

# Generate flat patterns (DXF + SVG)
python3 Scripts/generate_flat_patterns.py

# Blender photorealistic render
/Applications/Blender.app/Contents/MacOS/Blender \
    --background --factory-startup --python render_blender.py -- \
    --input "CAD Exports/Assembly_LidOpen.glb" \
    --output "Renders/LidOpen_Product.png" \
    --samples 256 --angle "3/4"
```

---

## Next Steps

1. **Answer ASSEMBLY_QUESTIONS.md** — 10 questions about screws, nuts, welds, mounting
2. **Update CAD** with exact fastener specs based on answers
3. **Blender rendering** — import GLB files for photorealistic product shots
4. **Send to fabrication** — STL files ready, drawings ready

---

## Notes

- All views build metal parts programmatically (no STL dependencies for metal)
- Ceramic STLs verified: cylinder 92.5mm OD x 91mm H, disk 92.5mm x 6mm
- Metal base is 2 pieces (body + top cap), lid metal is 1 piece
- Bottom cap is separate screw-on piece
- Ceramic lid plate cemented into lid pocket with ceramic pasting agent
- Hinge at center of widest gap (108.68mm, ~292.4°)
- Lid opens to 60° on hinge, kiln rotated so hinge faces -X

---

## License

Personal project - All rights reserved.
