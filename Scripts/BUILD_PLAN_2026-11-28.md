# Build plan, 2026-11-28: weld nuts at every bolt, hinge at 292.5°

Package: `FAB_PACKAGE_2026-11-28`. 3D build animation: [viewer-oven.html#build](https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/viewer-oven.html#build) (the "Old vs new" button shows the table below). All numbers are measured from the CAD by `Scripts/check_weld_nuts_2026-11-28.py` (output in `fit_check.txt` next to this file).

## Old way vs new way

| Bolt row | Before (2026-11-12) | Now (2026-11-28) |
|---|---|---|
| Bottom row ×5 | The nuts sat inside 01 and were sealed under 03 for good. | Welded inside 01. You bolt from outside, and you can take it apart later. |
| Seat row ×5 | You had to hold the nuts behind the 03 wall from inside the tube. | Welded to the 03 wall. Bolts from outside. |
| Top row ×5 | Impossible: the nuts were buried behind the core and 14.6 mm of insulation. | Welded inside the top of 01, so the core, insulation and cap go in first and the bolts go in last. |
| Lower lid row ×5 | You held the nuts behind the 09 wall. | Welded to 09. |
| Upper lid row ×5 | You held the nuts inside 06. | Welded inside 06. |
| Hinge | On a lid bolt at 257.5°. | Centred at 292.5° in the slot-free arc, on its own 2 holes per leaf, with weld nuts. |

The shop welds all 29 nuts at the factory before shipping. Assembly is about 5-6 min vs 45-60+ (an estimate), and the oven can be taken apart for service.

旧方法和新方法：底圈 ×5：以前螺母在 01 里面，被 03 永久封住；现在焊在 01 里面，从外面拧螺栓，以后能拆。座圈 ×5：以前要从管子里面扶住 03 墙后面的螺母；现在焊在 03 墙上。顶圈 ×5：以前装不了，螺母埋在加热芯和 14.6 mm 保温棉后面；现在焊在 01 顶部里面，先装加热芯、保温棉和顶盖，最后装螺栓。盖子下圈 ×5：以前要扶住 09 墙后面的螺母；现在焊在 09 上。盖子上圈 ×5：以前要在 06 里面扶住螺母；现在焊在 06 里面。合页：以前在 257.5° 的盖子螺栓上；现在中心在没有玻璃槽那段弧的 292.5°，每片有自己的 2 个孔和焊接螺母。工厂在出厂前焊好全部 29 颗螺母。装配约 5-6 分钟，以前 45-60 分钟以上（估计），而且可以拆开维修。

## Weld nuts

M6 hex projection weld nut, DIN 929, A2 (304) stainless (10 across flats, 5 thick), face on the inside face of the wall, centred on the bolt hole. One corner up, except on 09 (flats up, see below).

| Part | Weld nuts | Where |
|---|---|---|
| 01 Inner Wall Tube | 12 | bottom ring 5 (z -24.0), top ring 5 (z 61.66), hinge 2 (z 61.66 at 286.5° / 298.5°) |
| 03 Support Ring | 5 | inside the bolt wall, seat ring z 2.15 |
| 09 Lid Ceramic Holder | 7 | inside the bolt wall: lower lid ring 5 + hinge 2 (z 102.86 at 274.1° / 310.9°) |
| 06 Lid Inner Tube | 5 | upper lid ring, z 122.86 |

Bolts: 25 ring bolts (as before) + hinge 2 × M6 x 16 (H1) + 2 × M6 x 18 (H2). No loose nuts.

## Factory order this needs

03 (OD r 60.65) cannot pass 01's weld nuts (they reach in to r 55.90, a 4.75 mm overlap) from either end. So: weld 01's 5 bottom nuts, drop 03 into 01 from the top, then weld 01's 5 top nuts and 2 hinge nuts. 03 stays inside 01 for good but still bolts and unbolts with its 5 seat bolts. Until the seat bolts are in, 03 is loose between the nut rows; hold it at the seat holes with a pad or a 25 mm block under it.

## Build steps (same as the animation)

1. 04 bottom cap on the bench, rim up; the 2 Skutt insulators into the lead holes.
2. 3 ceramic feet + M5 leg screws onto 04.
3. 01 (12 weld nuts, 03 already inside) stands in 04.
4. Bottom ceramic spacer over 01. 5. 02 over everything.
6. 5 bottom bolts from outside into the 01 weld nuts.
7. Seat spacer into the 3.0 mm gap. 8. 5 seat bolts into the 03 weld nuts.
9. Top spacer into the gap. 10. Ceramic base disk on 03. 11. Core, wiring, crimps down into the chamber under 03, side insulation.
12. 05 top cap (tabs + hinge pad down the outside). 13. 5 top bolts last, into the 01 weld nuts.
14. H1 body leaf at 292.5°: 2 × M6 x 16 into its 01 weld nuts.
15. Lid: 09 (7 weld nuts). 16. 06 (5 weld nuts) over the 09 wall. 17. Lower lid spacer. 18. 07.
19. 5 lower lid bolts into the 09 weld nuts. 20. Upper lid spacer. 21. 08. 22. 5 upper lid bolts into the 06 weld nuts.
23. Handle. 24. Lid insulation, glue the lid disk. 25. H2 lid leaf: 2 × M6 x 18 through its wings into its 09 weld nuts.
26. Lid onto the hinge, pin H3. 27. Close.

## Tight spots and build challenges (measured)

| # | Where | Measured | Status / recommended fix |
|---|---|---|---|
| 1 | 03 into 01 past the weld nuts | 4.75 mm radial overlap, blocked from both ends | Needs Matt's OK: factory loads 03 into 01 before welding the top nuts (above). Other way: notch 03 and move the seat bolts off the 01 nut angles (changes 01, 02, 03, spacers). |
| 2 | Skutt insulator lips (Ø22.1 on the 04 floor) to the 01 bottom weld nuts | 0.53 mm | Same envelope as the old loose nuts. Turn 01 so the holes line up before it drops; check against a real insulator (its size is not published). |
| 3 | 01 hinge weld nut pair (286.5° / 298.5°) | 1.74 mm between the two nuts | Fine for projection welding one at a time. If the shop wants more room, H1 must get wider. |
| 4 | 03 heater lead holes to the nearest seat weld nut | 2.10 mm | OK, the beaded lead goes straight up. |
| 5 | M5 leg screw heads to the 01 bottom weld nuts | 2.70 mm | OK (unchanged). |
| 6 | 09 weld nut top to the 09 wall top edge | 1.00 mm (was 0.23 with a corner up) | Fixed: 09 nuts are flats up. |
| 7 | 03 weld nut top to the 03 wall top edge | 0.58 mm | OK; flats up would cut the lead-hole gap in item 4. |
| 8 | 06 weld nut top to the 08 plate underside / 01 bottom nut to the 04 floor | 1.23 / 1.93 mm | OK. |
| 9 | Weld nuts to the ceramics | core 9.65 (01 top), base disk 8.65 and core 8.65 (03 seat), lid disk 8.65 (09) | OK. The side insulation is 9.6 thick at each nut instead of 14.6: pack around the nuts. |
| 10 | Spacer rings over 01 | 0.40 mm radial (nuts are inside 01) | OK. Seat and top spacers are still loose until their bolts go in (the old fiddly step). |
| 11 | 06 down over the 09 wall | 06 nuts stay 8.23 mm above the wall top | OK. |
| 12 | Tool access | every bolt head is outside; nearest: H2 wing 7.69 mm from the 257.5° lower lid bolt head, 9.99 from the 329.5° one; H1 22.0 / 24.3 mm from the top bolt heads | OK for a thin-wall 10 mm socket. |
| 13 | Lid opening on the hinge | 0.00 mm³ overlap at 15, 45, 90, 110, 135° | OK. |
| 14 | Bolts | every shank (at the M6 minor diameter) lines up with its holes and weld nut; no head touches a part | OK. |
