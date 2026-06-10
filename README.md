# Nice Dreamz Heat & Clean Glass Oven

**The perfect heat, every time. Drop in your terp slurper, banger, or ball vape -- the oven heats the entire barrel evenly to your exact target temperature. When you're done, crank it up and burn off all the char and resin too.**

![Nice Dreamz Heat & Clean Glass Oven - Lid Open](Renders/LidOpen_Product.png)

Heat & Clean is a precision ceramic oven that heats your glass pieces to the perfect dabbing or vaping temperature -- no torch, no guessing, no hot spots. Set your temp, drop in your piece, and get a perfect session every time. And when your glass gets gunked up? Same oven, higher temp, walk away. Comes back looking brand new.

**See every part in 3D:** https://nicedreamzwholesale.com/heat-n-clean-viewer/all-parts.html
**Full parts list:** [PARTS_LIST.md](PARTS_LIST.md) · **Shop quote package:** `CAD Exports/Heat-N-Clean_Fabrication_Package.zip` (bilingual EN/中文)

---

## The Problem

Torches and coil heaters can't evenly heat modern glass pieces.

| | |
|---|---|
| ![Torch only heats the bottom](Reference%20Photos/ref_torch_problem.png) | ![Coil wraps only cover half the barrel](Reference%20Photos/ref_coil_problem.png) |

**With a torch**, only the bottom dish and a small portion of the barrel gets heated. You're guessing at temperature every single time -- too hot and you scorch it, too cool and you waste product.

**With a coil heater**, even a 10-wrap coil only covers half the barrel. The top half never reaches temp. Uneven heat means uneven flavor.

---

## The Solution

The Heat & Clean oven surrounds the **entire piece** in even, controlled heat.

| | |
|---|---|
| ![Full barrel heating](Reference%20Photos/ref_full_barrel_heating.png) | ![Terp slurper dimensions](Reference%20Photos/ref_slurper_dimensions.png) |

The 91mm tall ceramic chamber heats the **whole barrel** -- top to bottom, all the way around. Tower-style terp slurpers with 80mm barrels fit completely inside. Set your exact target temperature and hit it every time. Lower temps, better flavor, zero waste.

---

## Two Modes, One Device

### Heating Mode
Drop in your terp slurper, banger, or ball vape heater. Set your preferred dabbing or vaping temperature -- most sessions run in the 500-600 F sweet spot. The PID controller brings it to temp and holds it perfectly. Pull it out, attach it, and enjoy a perfect session every time.

### Cleaning Mode
Crank the temperature up. Walk away. The oven burns off all char, resin, and buildup. Come back to glass that looks brand new. No chemicals, no scrubbing, no soaking. The 6-hour auto-shutoff timer means you can set it and forget it.

---

## Built To Be Built — zero welds, all bolts

The entire oven assembles with **M6 bolts and nuts**. The only welds in the
product are the seams of the rolled tubes. No welded brackets, no welded
bosses, no welded hinge. 25 numbered pieces per kit, 3 fastener types total.

- **Two-piece top cap** -- a laser-cut-and-formed shell (flat top, skirt, 6
  drop fingers that bolt to the existing spacer-ring bolts) plus a clamp-fit
  hold-down ring that grips the ceramic with **zero fasteners of its own** --
  it gets sandwiched when the cap bolts down.
- **Bolted strap hinge** -- the cap shell carries two curled knuckles on its
  hinge finger; a small strap bolts under one of the lid's existing bolts and
  carries the third knuckle; a 5mm pin ties them together. Low-profile: the
  knuckles sit just above the rim, slid sideways along the hinge line so they
  clear the bolt head.
- **Flush ceramic lid face** -- the ceramic disk sits dead flush with the
  lid's bottom plane. No recess, no proud lip.
- **Handle with threaded studs** -- no screw heads on the lid top; two nuts
  grab the studs from underneath.

## The design journey (June 2026)

This repo went through a full manufacturability redesign, live, with every
decision reviewed against 3D renders before any shop quotes:

1. The original one-piece top cap had four concentric walls hanging under it
   -- unmakeable from sheet, ~$500+ machined from billet. It became two cheap
   parts (shell + clamp ring).
2. Welded mounting bosses became drop fingers that reuse the spacer-ring
   bolts. The welded plate hinge became the bolted strap hinge.
3. Design review by eye caught and fixed, in order: a missing bolt hole in
   the strap, a strap too small for M6 hardware, a bolt-head/knuckle
   collision (fixed by sliding the knuckles sideways), painted-on holes that
   weren't really cut (now real boolean-cut holes), and a recessed ceramic
   lid face (now flush). The commit log tells the whole story.
4. Open question for first articles: hinge strap stiffness with the lid
   hanging open. Cheap fixes ready if needed: 1.5mm strap stock or a second
   bolt hole.

---

## Features

- **Precision PID temperature control** -- REX-C100 controller holds your target temp within a few degrees
- **Locked-down interface** -- just set your temp and go, no confusing menus
- **Triple safety system** -- software limit (870 F) + overheat alarm (900 F) + thermal fuse (930 F)
- **6-hour auto-shutoff** -- DH48S timer relay cuts power automatically
- **Insulated dual-wall construction** -- 31mm ceramic-to-outer-wall gap keeps exterior cool to the touch
- **Perforated mesh exterior** -- full airflow ventilation with clean stainless steel look
- **Ceramic feet** -- heat-insulating legs keep the steel tray cool
- **Bolted strap hinge** -- lid swings open past vertical for easy loading; flush ceramic disk seals the chamber
- **Clamp-fit hold-down ring** -- keeps the ceramic core centered and seated with no fasteners of its own

---

## What's Inside

![Nice Dreamz Heat & Clean Glass Oven - Lid Removed](Renders/LidOff_Product.png)

| Component | Material |
|-----------|----------|
| Heating chamber | High-alumina ceramic cylinder (92.5mm OD) |
| Heating element | Kanthal wire coil (30 wraps) |
| Inner housing | 1.2mm 304 stainless steel |
| Outer mesh | 1.2mm perforated 304 stainless steel |
| Insulation gap | 24.6mm air gap between ceramic and housing |
| Spacer rings | 5x ceramic (3x 14mm body + 2x 10mm lid) |
| Controller | REX-C100 PID + SSR + DH48S timer |
| Legs | 3x ceramic feet with M6 mounting |

---

## Specifications

| Spec | Value |
|------|-------|
| Chamber ID | 81.5 mm (3.2 in) |
| Chamber height | 91 mm (3.6 in) |
| Outer diameter | 154.5 mm (6.1 in) |
| Temperature range | 100 - 870 F |
| Power | 120V AC |
| Auto-shutoff | 6 hours |
| Wall thickness | 31 mm (ceramic to outer mesh) |
| Body material | 304 stainless steel, brushed finish |

---

## Works With

- Tower-style terp slurpers (up to 80mm barrel)
- Standard bangers
- Ball vape heaters
- Any glass piece that fits the 81.5mm chamber

---

## License

All rights reserved. Nice Dreamz 2026.

---

## Project Structure

```
PARTS_LIST.md                   -- the 25-piece kit, numbered like the viewer labels
Scripts/
  export_all_parts.py           -- THE master: generates every part (STL/GLB), final design
  generate_fab_package.py       -- builds the bilingual shop quote package + zip
  generate_cap_dxfs.py          -- cap shell flat blank + hold-down ring drawing (DXF)
  generate_flat_patterns.py     -- laser-cut flat patterns for the other parts

viewer-*.html                   -- interactive 3D viewers (serve repo root, e.g. python3 -m http.server)
  viewer-sections.html          -- all 25 pieces, separated + named (hosted: /heat-n-clean-viewer/all-parts.html)
  viewer-metal-parts.html       -- the 13 metal parts a shop quotes
  viewer-topcap-fastening.html  -- full assembly; fasten/open-lid animations
  viewer-hinge-closeup.html     -- strap hinge close-up, attach animation
  viewer-full-assembly.html     -- every piece, apart/together
  viewer-capshell.html          -- the cap shell alone

CAD Exports/
  Individual Parts/STL|GLB/     -- every part, final design
  Core Split/ · Lid Split/      -- the split parts the viewers load
  Flat Patterns/DXF|SVG/        -- laser-cut patterns
  Fabrication Package/          -- spec EN + 中文, BOM, DXF, 3D refs (zip alongside)
```
