# Parts list (2026-11-28)

Generated from `FAB_PACKAGE_2026-11-28` (the only current machining files, see [CURRENT.md](CURRENT.md)) by `Scripts/make_parts_list.py`. Sizes in mm; overall size and volume measured from each STEP file.

2026-11-28: every M6 bolt threads into a stainless M6 projection weld nut (DIN 929, A2) welded inside its part at the factory: 29 total (01 ×12, 03 ×5, 06 ×5, 09 ×7), so no loose nuts and every bolt goes in from outside; 03 must go into 01 before 01's top nuts are welded. The real hinge H1/H2/H3 replaces placeholders 11/13 and is centred at 292.5° on its own 2 bolts per leaf. Build plan: [FAB_PACKAGE_2026-11-28/BUILD_PLAN.md](FAB_PACKAGE_2026-11-28/BUILD_PLAN.md).

2026-11-12: the top cap ring (ceramic OD to the 05 cap edge) is 20.0 mm (was 28.4) for the smallest glass slurper: insulation 14.6, air gap 3.0, 05 edge 0.4 past the outer tube. Heights as R2: the real ceramic stack (core 90.4 + base plate 4.9 = 95.3) ends flush with the 05 cap top. Later the same day: 5 bolts per ring (was 6), 72° apart between the 4 glass slots (41.5/113.5/185.5/257.5/329.5°); hinge on the 257.5° lid bolt; heater lead holes 160/170°; legs back to even 120° at 5.5/125.5/245.5° with M5 leg screws (Ø5.5 holes); tray 1.2 lower so the 25 mm feet meet the 04 floor exactly.

| # | Part | 零件 | Material | Key sizes | Overall (x × y × z) | Volume cm³ |
|---|---|---|---|---|---|---|
| 01 | Inner Wall Tube | 内壁管 | 0.8 mm 304/430 SS | ID 121.7 / OD 123.3, h 125.36, 4 glass slots 13.3, 17 M6 holes (5 per ring at 41.5 + n × 72° + 2 hinge at 286.5/298.5°); WELDMENT: 12 M6 weld nuts welded inside (bottom 5, top 5, hinge 2) | 123.3 × 123.3 × 125.4 | 41.04 |
| 02 | Outer Perforated Tube | 外冲孔管 | 1.2 mm 304 SS | ID 129.3 / OD 131.7 (air gap 3.0), h 125.36, Ø4 @ 6 mm perforation (68 per row), 4 slots 10.5, 17 M6 holes (15 + 2 hinge) | 131.7 × 131.7 × 125.4 | 47.78 |
| 03 | Support Ring | 支撑环 | 0.8 mm 304/430 SS | OD 121.3, raised ceramic seat r 36.25-47.25, 5 M6 in the bolt wall; WELDMENT: 5 M6 weld nuts welded inside the bolt wall; no leg holes (since 11-20); heater lead holes Ø10 at 145/173°, TC hole Ø6.4 at 315°, all r 53.5 | 121.3 × 121.3 × 14.8 | 14.72 |
| 04 | Bottom Cap | 底盖 | 1.2 mm 304 SS | OD 134.7, skirt 17.2, 5 M6, 3 leg holes Ø5.5 on Ø108, heater lead holes Ø11.5 at r 49 (145/173°, Skutt insulators), TC hole r 53.5 (315°) | 134.7 × 134.7 × 17.2 | 24.57 |
| 05 | One-Piece Top Cap | 一体顶盖 | 1.2 mm 304 SS | ring OD 134.5, outer skirt (lip) back since 11-16, 5 bolt tabs + hinge pad (28 wide at 292.5°, 2 M6), 4 grooves, 48 vents Ø3.0 on Ø126.3 | 134.9 × 134.5 × 41.2 | 24.20 |
| 06 | Lid Inner Tube | 盖子内管 | 0.8 mm 304/430 SS | ID 121.7 / OD 123.3, h 34.2, 12 M6 holes (10 + 2 hinge); WELDMENT: 5 M6 weld nuts welded inside (upper lid ring) | 123.3 × 123.3 × 34.2 | 11.84 |
| 07 | Lid Outer Perforated Tube | 盖子外冲孔管 | 1.2 mm 304 SS | ID 129.3 / OD 131.7, h 34.2, Ø4 @ 6 mm perforation, 12 M6 holes (10 + 2 hinge) | 131.7 × 131.7 × 34.2 | 12.69 |
| 08 | Lid Top Disk | 盖子顶盘 | 1.2 mm 304 SS | OD 134.7, skirt 14.2, 5 M6, 2 handle holes Ø4.5 | 134.7 × 134.7 × 14.2 | 23.40 |
| 09 | Lid Ceramic Holder | 盖子陶瓷托架 | 0.8 mm 304/430 SS | plate OD 131.6, bolt wall Ø121.3 (7 M6: 5 + 2 hinge at 274.1/310.9°), lip Ø128.9, 48 vents Ø3.0 on Ø126.3 (= 05), ceramic lid disk pocket; WELDMENT: 7 M6 weld nuts welded inside the bolt wall | 131.6 × 131.6 × 14.0 | 14.62 |
| 10 | Lid Handle | 提手 | Ø8 304 SS rod | 2 posts, M4 tapped 10 deep | 54.2 × 27.0 × 29.0 | 4.68 |
| H1 | Hinge Body Leaf | 合页本体页 | 304 SS | at 292.5° on the 05 hinge pad, 28 wide, 2 radial M6 (286.5/298.5°) with Ø13 spot faces, 2 outer knuckles Ø12 | 31.1 × 23.3 × 46.2 | 5.40 |
| H2 | Hinge Lid Leaf | 合页盖子页 | 304 SS | middle knuckle Ø12 + 2 side wings, 2 radial M6 (274.1/310.9°) into the 09 weld nuts | 53.7 × 30.3 × 20.0 | 4.14 |
| H3 | Hinge Pin | 合页销 | Ø6 304 SS rod | 29 long + Ø10 x 1.5 head; H1 holes Ø6.1, H2 Ø6.4 | 31.2 × 19.1 × 10.0 | 0.94 |
| 14 | Steel Tray | 钢托盘 | 3 mm steel | 3 leg holes Ø5.5 (M5) on Ø108 at 5.5/125.5/245.5° (even 120°); 1.2 lower than before, so the 25 mm feet meet the 04 floor exactly | 394.5 × 204.5 × 27.0 | 298.93 |

We supply (not in the machining package):

| Item | Qty | Size |
|---|---|---|
| Ceramic heater core | 1 | Ø92.5 / Ø81.5, 90.4 tall (measured), 4 glass slots 10.5 |
| Ceramic base disk | 1 | Ø92.5, 4.9 thick (core + base = 95.3, measured) |
| Ceramic lid disk | 1 | Ø92.5 with raised centre |
| Ceramic spacer rings | 5 | ID 124.1 / OD 129.3 (wall 2.6); all 10 mm tall (3 body + 2 lid, one size since 2026-11-10); 5 Ø6.6 holes each, the top and the lower lid ring +2 hinge holes |
| Ceramic feet | 3 | Ø28 base / Ø20 post, 25 tall, Ø5.5 hole; on Ø108 leg circle at 5.5/125.5/245.5° (120° apart) |
| M6 bolts, A2 stainless | 29 | 25 ring bolts (5 per ring × 5 rings, 41.5° + n × 72°) + hinge: 2 × M6 x 16 (H1) + 2 × M6 x 18 (H2). NO loose nuts: each bolt threads into a weld nut |
| M6 projection weld nuts, DIN 929, A2 stainless | 29 | welded by the factory inside 01 (12), 03 (5), 06 (5), 09 (7); part of those parts in the files |
| M4 screws | 2 | handle |
| Leg screws M5 x 40 | 3 | socket head ISO 4762, A2 stainless, + M5 washer + nut under the tray |
