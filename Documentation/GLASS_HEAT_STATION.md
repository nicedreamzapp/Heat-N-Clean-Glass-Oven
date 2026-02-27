# Glass Heat Station - Design Specification

## Product Purpose
Uniformly heat Tower Style Terp Slurper barrels (80mm) for low-temperature dabs.

**Problem solved:** Torches only heat the bottom dish. Coils only heat half the barrel. This heats the WHOLE barrel.

---

## Reference Design (from renders)

```
        ┌───────────┐
        │  HINGED   │ ← Lid (opens for loading)
        │    LID    │
        ├───────────┤
        ║═══════════║ ← Horizontal grooves/fins
        ║═══════════║   (heat dissipation + aesthetics)
        ║═══════════║
        ║═══════════║
        ║═══════════║
        ╠═══════════╣
┌───────┴───────────┴───────┐
│    [REX CONTROLLER]       │ ← Base plate with PID
│     PV: 980  SV: 1050     │
└───────────────────────────┘
```

---

## Core Components

### 1. CERAMIC HEATER (existing design)
| Parameter | Value |
|-----------|-------|
| Outer Diameter | 92.5mm |
| Inner Diameter | 81.5mm (heating chamber bore) |
| Height | 91mm |
| Wall Thickness | 5.5mm |
| Heating Element | Kanthal wire in helical groove |
| Wraps | 30 |

### 2. STAINLESS HOUSING
| Parameter | Value | Notes |
|-----------|-------|-------|
| Style | Cylindrical with horizontal grooves | Like the render |
| Material | 304 Stainless Steel | Brushed finish |
| Lid | Hinged, spring-loaded? | Easy one-hand operation |

### 3. INSULATION
| Parameter | Value |
|-----------|-------|
| Material | Ceramic fiber blanket |
| Location | Between ceramic core and housing |
| Purpose | Keep housing touchable, retain heat in chamber |

### 4. BASE PLATE
| Parameter | Value |
|-----------|-------|
| Material | Stainless or aluminum |
| Features | Mounts housing + REX controller |
| Wiring | Internal routing to controller |

### 5. REX PID CONTROLLER
| Parameter | Value |
|-----------|-------|
| Model | REX-C100 or similar |
| Display | PV (current temp) / SV (set temp) |
| Input | K-type thermocouple |
| Output | SSR to Kanthal heater |

---

## Electrical System

```
┌─────────────────┐
│  CERAMIC CORE   │
│  (Kanthal wire) │
└────────┬────────┘
         │ High-temp wire
         ▼
┌─────────────────┐
│ CERAMIC TERMINAL│ ← Inside or outside housing
└────────┬────────┘
         │ Regular wire
         ▼
┌─────────────────┐      ┌─────────────────┐
│  SSR (Solid     │◄─────│  REX CONTROLLER │
│  State Relay)   │      │  (PID control)  │
└────────┬────────┘      └────────▲────────┘
         │                        │
         │ AC Power               │ Thermocouple
         ▼                        │ feedback
    [WALL OUTLET]          ┌──────┴──────┐
                           │ THERMOCOUPLE │
                           │ (in chamber) │
                           └─────────────┘
```

---

## Design Tasks

### Housing Shell
- [ ] Horizontal groove pattern (how many? spacing?)
- [ ] Wall thickness for rigidity
- [ ] Inner diameter to fit insulation + ceramic core
- [ ] Top flange for lid mounting

### Lid
- [ ] Hinge mechanism (piano hinge? custom?)
- [ ] Spring or detent to hold open
- [ ] Insulated underside
- [ ] Handle/knob

### Base Plate
- [ ] Dimensions to fit housing + controller
- [ ] Controller cutout
- [ ] Wire routing channels
- [ ] Feet/rubber pads

### Wiring Penetrations
- [ ] Thermocouple entry point
- [ ] Kanthal wire exit (to terminals)
- [ ] Controller power in
- [ ] Heater power routing

---

## OBSERVED FROM PROTOTYPE PHOTOS (Jan 2026)

### What's Working
- [x] Ceramic core heats evenly (beautiful orange glow)
- [x] Can heat 4+ slurpers simultaneously
- [x] Thermocouple positioned correctly (dark probe visible)
- [x] Ventilation slots in ceramic allow heat flow
- [x] Stainless housing contains the heat
- [x] Wiring exits at bottom

### What Needs Refinement
- [ ] Ceramic fiber insulation is loose/stuffed - needs containment ring
- [ ] Wiring exposed at bottom - needs clean routing/cover
- [ ] No finished lid - insulation bulges out top
- [ ] Thermocouple wire needs proper grommet
- [ ] Power wires need ceramic terminal housing

### Observed Layout from Photos
```
TOP VIEW (proto_heated_top_view.png):
    ┌─────────────────┐
    │  ░░░░░░░░░░░░░  │ ← Loose ceramic fiber (needs containment)
    │ ░┌───────────┐░ │
    │ ░│ O  O  O  O│░ │ ← 4 slurpers heating in 81.5mm bore
    │ ░│    ╳      │░ │ ← Thermocouple probe
    │ ░└───────────┘░ │
    │  ░░░░░░░░░░░░░  │
    └────────┬────────┘
             │ wires exit here

SIDE VIEW (proto_heated_side_view.png):
    ┌─────────────────┐
    │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│ ← Ceramic fiber (currently stuffed)
    │▓┌─────────────┐▓│
    │▓│█████████████│▓│ ← Ceramic core (glowing orange)
    │▓│█████████████│▓│
    │▓│█ SLURPERS █│▓│
    │▓│█████████████│▓│
    │▓└──┬──────┬───┘▓│ ← Vent slots visible
    │▓▓▓▓│▓▓▓▓▓▓│▓▓▓▓▓│
    ├────┴──────┴─────┤ ← Stainless housing cylinder
    │  ⚡ wiring ⚡   │ ← Red power wire, ceramic terminal
    └─────────────────┘
```

---

## Files to Create

| File | Description |
|------|-------------|
| `housing_grooved.py` | Housing with horizontal fin pattern |
| `lid_hinged.py` | Hinged lid design |
| `base_plate.py` | Base with controller cutout |
| `full_assembly.py` | Everything together |
| `flat_patterns/` | Sheet metal cut files |

---

## Next Steps

1. Confirm terp slurper barrel dimensions
2. Design grooved housing exterior
3. Design hinged lid mechanism
4. Design base plate with controller mount
5. Generate flat patterns for fabrication
