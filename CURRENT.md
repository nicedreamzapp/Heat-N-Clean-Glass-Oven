# CURRENT: the only files to build from (2026-09-28)

Everything older was moved OFF GitHub to the local folder `Desktop/PROJECTS/Heat-N-Clean-ARCHIVE (old, do not build from)`. Never render, measure or build from it.

| Page | What it is |
|---|---|
| viewer-base-full.html | Base, every part, cut in half, measurements |
| viewer-base-assembly.html | Base, step-by-step build |
| viewer-lid-full.html | Lid, every part, cut in half |
| viewer-lid-assembly.html | Lid, step-by-step build |
| viewer-lid-holder.html | Lid ceramic holder + ceramic lid disk on the core |
| viewer-complete.html | Whole oven, lid open on its hinge, cut in half / separated (one of the 3 links for Tianrun) |

| Oven_All_Parts_2026-09-28.png | Letter-size sheet, every part laid out, EN + 中文 (made by viewer-parts-sheet.html) |

Meshes: `viewer-full/` (base) and `viewer-lid-full/` (lid). Those are the approved shapes. `viewer-full/tray.glb` is the steel tray, unchanged since June, copied in from the archive on 2026-09-28.
Machining files: `FAB_PACKAGE_2026-09-28/` (STEP + STL + bilingual README), built by `Scripts/build_current_package.py` from `cad-source/` (Sept 9 solids for unchanged parts) plus every 2026-09-28 change in code.
05 top cap is a clean solid (2026-09-28 redraw, sleeves 0.2 mm clear). The lid sits on it, so every lid part is +1.2 mm except the ceramic lid disk.
Hinge: LEFT TO TIANRUN'S SHOP (Matt, 2026-09-28); the README tells them. Was: Alice's stock butt hinge was approved 2026-09-11, but the model still shows the old strap + pin, and the cap has no hinge mount.
