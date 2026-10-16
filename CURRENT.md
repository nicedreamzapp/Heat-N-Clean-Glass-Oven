# CURRENT: the only files to build from (2026-10-16)

Everything older was moved OFF GitHub to the local folder `Desktop/PROJECTS/Heat-N-Clean-ARCHIVE (old, do not build from)`. Never render, measure or build from it.

| Page | What it is |
|---|---|
| viewer-base-full.html | Base, every part, cut in half, measurements |
| viewer-base-assembly.html | Base, step-by-step build |
| viewer-lid-full.html | Lid, every part, cut in half |
| viewer-lid-assembly.html | Lid, step-by-step build |
| viewer-lid-holder.html | Lid ceramic holder + ceramic lid disk on the core |
| viewer-complete.html | Whole oven, lid open on its hinge, cut in half / separated (one of the 3 links for Tianrun) |

| Oven_All_Parts_2026-09-30.png | Letter-size sheet, every part laid out, EN + 中文 (made by viewer-parts-sheet.html). NOT yet re-rendered for the 2026-10-16 change (03 raised middle, 09 pocket +1.2) |

Meshes: `viewer-full/` (base) and `viewer-lid-full/` (lid). Those are the approved shapes. `viewer-full/tray.glb` is the steel tray, unchanged since June, copied in from the archive on 2026-09-28.
Machining files: `FAB_PACKAGE_2026-10-16/` (STEP + STL + bilingual README), built by `Scripts/build_current_package.py` from `cad-source/` (Sept 9 solids for unchanged parts) plus every 2026-09-28, 09-30 and 10-16 change in code. Check with `.venv-cad/bin/python Scripts/verify_steps.py FAB_PACKAGE_2026-10-16` (every STEP must be one solid). `FAB_PACKAGE_2026-09-28` is in the archive folder.
05 top cap is a clean solid (2026-09-28 redraw, sleeves 0.2 mm clear). The lid sits on it, so every lid part is +1.2 mm except the ceramic lid disk.
Hinge: LEFT TO TIANRUN'S SHOP (Matt, 2026-09-28); the README tells them. Was: Alice's stock butt hinge was approved 2026-09-11, but the model still shows the old strap + pin, and the cap has no hinge mount.

2026-09-28 evening: 05 top cap has 4 metal slot grooves (inside = the ceramic slot exactly: 10.5 wide, R5.25 round bottom, 23.5 deep), one per slot from the ceramic to the outer tube; they cover the insulation and keep the cap one piece. 01 inner tube glass slots widened to 13.3 (round bottom) so the grooves pass. 01 STEP is now a single solid (the wire-hole patches used to come out as loose pieces).

2026-10-16: SEAT RAISE (Tianrun's plastic print on the real ceramic: ceramic top 5.06 mm below the 05 cap top, ceramic slots ~5.3 deeper than the grooves; Matt 10/12: ceramic FLUSH with the cap TOP; ceramic does not change; factory: no extra parts). Same 13 parts. 03: middle (r 36.25-52) raised 5.06, seat now z -0.44, riser at r 52, centering wall up with it; bolts, leg and wire holes not moved. 05: groove bottoms 0.24 deeper (z 67.26). 01: glass slots 0.24 lower with them. 09: lid disk pocket + shelf +1.2 (lid disk face flush with the lid bottom, sits on the flush ceramic). 02, 04, 06, 07, 08, 10, 11, 13, 14 unchanged. The 5.06 is the measured gap, not derived: the drawn ceramic stack is 96.5 tall but the gap says the real one is ~92.6, cause unknown (`Ceramic Parts/ceramic heater_CAD.step` is a generic Ø90 x 90 cup, not the measured Ø92.5 part, so it cannot settle it). Viewer ceramics now drawn as measured (core top 92.2, slot bottom 67.26). Picture: `Renders/seat_raise_before_after_2026-10-16.png`. `viewer-base-assembly-seat5.html` / `viewer-seat5/` were the 10/12 preview of this, superseded.
