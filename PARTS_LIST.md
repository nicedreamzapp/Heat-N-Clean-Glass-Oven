# Parts list (2026-11-12)

Generated from `FAB_PACKAGE_2026-11-12` (the only current machining files, see [CURRENT.md](CURRENT.md)) by `Scripts/make_parts_list.py`. Sizes in mm; overall size and volume measured from each STEP file.

2026-11-12: the top cap ring (ceramic OD to the 05 cap edge) is 20.0 mm (was 28.4) for the smallest glass slurper: insulation 14.6, air gap 3.0, 05 edge 0.4 past the outer tube. Heights as R2: the real ceramic stack (core 90.4 + base plate 4.9 = 95.3) ends flush with the 05 cap top. Later the same day: 5 bolts per ring (was 6), 72° apart between the 4 glass slots (41.5/113.5/185.5/257.5/329.5°); hinge on the 257.5° lid bolt; heater lead holes 160/170°; legs back to even 120° at 5.5/125.5/245.5° with M5 leg screws (Ø5.5 holes); tray 1.2 lower so the 25 mm feet meet the 04 floor exactly.

| # | Part | 零件 | Material | Key sizes | Overall (x × y × z) | Volume cm³ |
|---|---|---|---|---|---|---|
| 01 | Inner Wall Tube | 内壁管 | 0.8 mm 304/430 SS | ID 121.7 / OD 123.3, h 125.36, 4 glass slots 13.3, 15 M6 holes (5 per ring at 41.5 + n × 72°) | 123.3 × 123.3 × 125.4 | 37.17 |
| 02 | Outer Perforated Tube | 外冲孔管 | 1.2 mm 304 SS | ID 129.3 / OD 131.7 (air gap 3.0), h 125.36, Ø4 @ 6 mm perforation (68 per row), 4 slots 10.5, 15 M6 holes | 131.7 × 131.7 × 125.4 | 47.86 |
| 03 | Support Ring | 支撑环 | 0.8 mm 304/430 SS | OD 121.3, raised ceramic seat r 36.25-47.25, 5 M6, 3 leg holes Ø5.5 (M5) on Ø108 at 5.5/125.5/245.5° (even 120°), 3 wire holes r 53.5 (160/170/315°) | 121.3 × 121.3 × 14.8 | 13.08 |
| 04 | Bottom Cap | 底盖 | 1.2 mm 304 SS | OD 134.7, skirt 17.2, 5 M6, 3 leg holes Ø5.5 on Ø108, 3 wire holes r 53.5 (as 03) | 134.7 × 134.7 × 17.2 | 24.70 |
| 05 | One-Piece Top Cap | 一体顶盖 | 1.2 mm 304 SS | ring OD 132.5, width 20.0 from the ceramic, no outer skirt, 5 bolt tabs outside the tube, 4 grooves 17.7 long, 48 vents Ø3.0 on Ø126.3 | 133.9 × 133.4 × 41.2 | 19.23 |
| 06 | Lid Inner Tube | 盖子内管 | 0.8 mm 304/430 SS | ID 121.7 / OD 123.3, h 34.2, 10 M6 holes | 123.3 × 123.3 × 34.2 | 10.26 |
| 07 | Lid Outer Perforated Tube | 盖子外冲孔管 | 1.2 mm 304 SS | ID 129.3 / OD 131.7, h 34.2, Ø4 @ 6 mm perforation, 10 M6 holes | 131.7 × 131.7 × 34.2 | 12.65 |
| 08 | Lid Top Disk | 盖子顶盘 | 1.2 mm 304 SS | OD 134.7, skirt 14.2, 5 M6, 2 handle holes Ø4.5 | 134.7 × 134.7 × 14.2 | 23.40 |
| 09 | Lid Ceramic Holder | 盖子陶瓷托架 | 0.8 mm 304/430 SS | plate OD 131.6, bolt wall Ø121.3 (5 M6), lip Ø128.9, 48 vents Ø3.0 on Ø126.3 (= 05), ceramic lid disk pocket | 131.6 × 131.6 × 14.0 | 12.39 |
| 10 | Lid Handle | 提手 | Ø8 304 SS rod | 2 posts, M4 tapped 10 deep | 54.2 × 27.0 × 29.0 | 4.68 |
| 11 | Lid Hinge Strap (placeholder) | 盖子铰链片（示意） | 1.2 mm 304 SS | on the 257.5° lid bolt; factory fits its stock hinge | 27.6 × 13.6 × 14.0 | 0.63 |
| 13 | Hinge Pin (placeholder) | 铰链销（示意） | Ø5 304 SS rod | 30 long | 21.3 × 27.5 × 5.0 | 0.59 |
| 14 | Steel Tray | 钢托盘 | 3 mm steel | 3 leg holes Ø5.5 (M5) on Ø108 at 5.5/125.5/245.5° (even 120°); 1.2 lower than before, so the 25 mm feet meet the 04 floor exactly | 394.5 × 204.5 × 27.0 | 298.93 |

We supply (not in the machining package):

| Item | Qty | Size |
|---|---|---|
| Ceramic heater core | 1 | Ø92.5 / Ø81.5, 90.4 tall (measured), 4 glass slots 10.5 |
| Ceramic base disk | 1 | Ø92.5, 4.9 thick (core + base = 95.3, measured) |
| Ceramic lid disk | 1 | Ø92.5 with raised centre |
| Ceramic spacer rings | 5 | ID 124.1 / OD 129.3 (wall 2.6); all 10 mm tall (3 body + 2 lid, one size since 2026-11-10); 5 Ø6.6 holes each |
| Ceramic feet | 3 | Ø28 base / Ø20 post, 25 tall, Ø5.5 hole; on Ø108 leg circle at 5.5/125.5/245.5° (120° apart) |
| M6 bolts + nuts | 25 | 5 per ring × 5 rings (41.5° + n × 72°, between the glass slots; 6 per ring before); the wall stack is 1.4 thinner than R2 (same bolts work, or 1-2 mm shorter) |
| M4 screws | 2 | handle |
| Leg screws M5 x 40 | 3 | socket head ISO 4762, A2 stainless, + M5 washer + nut under the tray |
