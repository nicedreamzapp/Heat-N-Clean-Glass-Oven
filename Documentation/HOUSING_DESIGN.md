# Heat-N-Clean Stainless Housing - Design Document

## Working Prototype Notes
**Status:** Ugly but working for 4 months - needs refinement

---

## Layer Structure (Bottom Up)

```
┌─────────────────────────────────────┐
│           TOP OPENING               │  Glass/work surface access
├─────────────────────────────────────┤
│     STAINLESS TOP RING              │  Finished edge
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │      CERAMIC FABRIC         │    │  Insulation layer (thick)
│  │  ┌─────────────────────┐    │    │
│  │  │                     │    │    │
│  │  │   CERAMIC HEATER    │    │    │  Core heating element
│  │  │      CYLINDER       │    │    │  - Kanthal wire in groove
│  │  │                     │    │    │  - 92.5mm OD x 91mm H
│  │  │                     │    │    │
│  │  └─────────────────────┘    │    │
│  │      CERAMIC FABRIC         │    │
│  └─────────────────────────────┘    │
│        STAINLESS SHELL              │  Outer housing
├─────────────────────────────────────┤
│       CERAMIC FABRIC BASE           │  Bottom insulation
├─────────────────────────────────────┤
│      STAINLESS BOTTOM PLATE         │  Base plate
├─────────────────────────────────────┤
│            FEET                     │  Airflow underneath
└─────────────────────────────────────┘
```

---

## Components List

### 1. CERAMIC FABRIC INSULATION
- **Material:** Ceramic fiber blanket (2300°F rated)
- **Thickness:** TBD from prototype measurements
- **Locations:**
  - [ ] Wrapped around ceramic cylinder (sides)
  - [ ] Under ceramic cylinder (bottom)
  - [ ] Top ring area (if needed)

### 2. STAINLESS STEEL HOUSING
- **Material:** 18 gauge stainless (1.2mm)
- **Parts:**
  - Bottom plate
  - Cylindrical wall
  - Top ring/flange
  - Feet (4x)

### 3. ELECTRICAL PENETRATIONS

#### Thermocouple (1x)
- **Type:** K-type thermocouple
- **Wire size:** ~3mm diameter typical
- **Hole size:** TBD (need compression fitting or ceramic grommet?)
- **Position:** TBD from prototype photos

#### Kanthal Heating Wire (1 pair = 2 wires)
- **From:** Ceramic heater grooves
- **To:** Ceramic terminal block (outside housing)
- **Hole size:** TBD
- **Position:** TBD from prototype photos

#### Ceramic Terminal Block
- **Purpose:** Kanthal wire → Regular wire transition
- **Location:** Outside housing (mounted to housing or separate?)
- **Connection to:** REX PID controller

---

## REX Controller Wiring

```
[CERAMIC HEATER]
      │
      │ Kanthal wire (high temp)
      │
      ▼
[CERAMIC TERMINAL] ──── mounted outside housing
      │
      │ Regular wire (lower temp)
      │
      ▼
[REX CONTROLLER] ──── PID temperature control
      │
      │
      ▼
[THERMOCOUPLE] ──────── feedback loop to controller
```

---

## TODO: Measurements Needed from Prototype

### Ceramic Fabric
- [ ] Thickness of insulation used
- [ ] How many layers wrapped around cylinder?
- [ ] Bottom insulation thickness
- [ ] Total outer diameter with insulation

### Hole Positions
- [ ] Thermocouple entry point (which side? what height?)
- [ ] Kanthal wire exit point (bottom? side?)
- [ ] Distance between Kanthal holes (terminal spacing)

### Ceramic Terminal
- [ ] Terminal block dimensions
- [ ] Mounting method (screws? welded bracket?)
- [ ] Wire gauge Kanthal → terminal
- [ ] Wire gauge terminal → REX controller

### Overall Fit
- [ ] Current housing inner dimensions
- [ ] Clearance issues?
- [ ] Heat spots or problems?

---

## Photos Needed

1. **Overall prototype** - how it looks assembled
2. **Inside view** - ceramic fabric arrangement
3. **Wire exits** - where Kanthal comes out
4. **Thermocouple position** - where it enters
5. **Ceramic terminal** - close-up of connection
6. **Bottom** - how it sits, feet/airflow

---

## Design Goals

- [ ] Clean, professional appearance
- [ ] Proper insulation (no hot spots on housing)
- [ ] Safe electrical routing
- [ ] Easy assembly/disassembly for maintenance
- [ ] Repeatable manufacturing (sheet metal + welding)

---

## Next Steps

1. **Take photos** of current prototype
2. **Measure** key dimensions
3. **Update this document** with actual values
4. **Regenerate CAD** with correct dimensions
5. **Flat patterns** for fabrication
