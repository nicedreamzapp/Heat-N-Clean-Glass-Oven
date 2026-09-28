# Heat-N-Clean — Parts List (final design, 2026-06-10)

One kit = **25 numbered pieces**. Numbers match the labels in the
[interactive viewer](https://nicedreamzwholesale.com/heat-n-clean-viewer/all-parts.html)
(`viewer-sections.html` locally).

Zero welds anywhere. Every joint is a bolt, a nut, or a clamp fit.

## BODY (1–12)

| # | Part | Qty | Notes |
|---|------|-----|-------|
| 1 | Bottom Cap | 1 | fastened by the bottom long-bolt ring |
| 2 | Ceramic Base Disk | 1 | |
| 3 | Support Ring | 1 | |
| 4 | Ceramic Heater Core | 1 | 4 glass slots |
| 5 | Seat Spacer Ring | 1 | ceramic, 14mm tall |
| 6 | Inner Wall Tube | 1 | |
| 7 | Top Spacer Ring | 1 | ceramic, 14mm tall |
| 8 | Outer Perforated Tube | 1 | |
| 9 | Bottom Spacer Ring | 1 | ceramic, 14mm tall |
| 10 | Seat Bolts + Nuts | 6 + 6 | M6 short |
| 11 | Cap-Finger Bolts + Nuts | 6 + 6 | M6 long — also clamp the Cap Shell fingers |
| 12 | Bottom Bolts + Nuts | 6 + 6 | M6 long — also clamp the Bottom Cap |

## TOP CAP (13–14) — two pieces, no fasteners between them

| # | Part | Qty | Notes |
|---|------|-----|-------|
| 13 | Ceramic Hold-Down Ring | 1 | flat ring + 3 hanging walls; CLAMP FIT — trapped between shell and chamber, no screws |
| 14 | Cap Shell | 1 | one sheet: top, skirt, 6 drop fingers, hinge finger w/ 2 curl barrels |

## LID (15–25)

| # | Part | Qty | Notes |
|---|------|-----|-------|
| 15 | Ceramic Lid Disk | 1 | |
| 16 | Lid Ceramic Holder | 1 | |
| 17 | Lower Lid Spacer Ring | 1 | ceramic, 10mm tall |
| 18 | Lid Inner Tube | 1 | |
| 19 | Upper Lid Spacer Ring | 1 | ceramic, 10mm tall |
| 20 | Lid Outer Perforated Tube | 1 | |
| 21 | Lid Top Disk | 1 | |
| 22 | Handle | 1 | threaded studs built into the feet — no screw heads on top |
| 23 | Handle Nuts | 2 | grab the studs under the Lid Top Disk |
| 24 | Lower Lid Bolts + Nuts | 6 + 6 | M6 short |
| 25 | Upper Lid Bolts + Nuts | 6 + 6 | M6 short |

## Hinge (bolted strap — zero welds)

- Cap side: built into the Cap Shell (#14) — the finger at 292.4° runs up past the rim into 2 curled barrels
- Lid side: `05b_Lid_Hinge_Strap` — bolts under the lid's existing bolt at 292.4°, 1 barrel
- `05_Hinge_Pin` slides through all 3 barrels

## Fastener + ceramic-ring totals per kit

| Item | Count |
|------|-------|
| Ceramic spacer rings | **5** (3 body @ 14mm + 2 lid @ 10mm — same diameter, same bolt holes) |
| M6 short bolts | 18 |
| M6 long bolts | 12 |
| M6 nuts | 30 |
| Handle nuts | 2 |
| Hinge pin | 1 |

Only **3 fastener types** in the whole oven: short bolt, long bolt, nut.

> Open question: make all 5 spacer rings the same height → one ceramic ring part ×5.

## Regenerating everything

```bash
.venv/bin/python Scripts/export_all_parts.py
```

Exports every part (STL + GLB) to `CAD Exports/Individual Parts/`. The split
GLBs the viewers use live in `CAD Exports/Core Split/` and `CAD Exports/Lid Split/`.

Old fabrication package, STEP files, and the one-piece top cap were removed
2026-06-10 — they described the old design (welded bosses, 5-ear cap, plate
hinge, M4 cap screws) and need regenerating from the current model when a
shop package is next needed.
