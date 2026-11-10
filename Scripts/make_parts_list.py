"""Writes PARTS_LIST.md from FAB_PACKAGE_2026-11-08-R2 (sizes measured from each STEP).  Run: .venv-cad/bin/python Scripts/make_parts_list.py"""
import os, sys, math
from build123d import *
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"; TAG="2026-11-08-R2"; P=R+f"FAB_PACKAGE_{TAG}/STEP/"
rows=[("01","Inner Wall Tube","内壁管","0.8 mm 304/430 SS","ID 133.7 / OD 135.3, h 125.36 (R2: +2.66), 4 glass slots 13.3, 18 M6 holes"),
("02","Outer Perforated Tube","外冲孔管","1.2 mm 304 SS","ID 144.1 / OD 146.5, h 125.36 (R2: +2.66), Ø4 @ 6 mm perforation, 4 slots 10.5, 18 M6 holes"),
("03","Support Ring","支撑环","0.8 mm 304/430 SS","OD 133.3, raised ceramic seat r 36.25-52, 6 M6, 3 leg holes Ø6.6 on Ø120, 3 wire holes r 58"),
("04","Bottom Cap","底盖","1.2 mm 304 SS","OD 149.5, skirt 17.2, 6 M6, 3 leg holes on Ø120, 3 wire holes r 58"),
("05","One-Piece Top Cap","一体顶盖","1.2 mm 304 SS","ring OD 149.3, width 28.4 from the ceramic, 6 bolt tabs, 4 grooves 25.1 long, 48 vents Ø3.5 on Ø139.7"),
("06","Lid Inner Tube","盖子内管","0.8 mm 304/430 SS","ID 133.7 / OD 135.3, h 34.2, 12 M6 holes"),
("07","Lid Outer Perforated Tube","盖子外冲孔管","1.2 mm 304 SS","ID 144.1 / OD 146.5, h 34.2, Ø4 @ 6 mm perforation, 12 M6 holes"),
("08","Lid Top Disk","盖子顶盘","1.2 mm 304 SS","OD 149.5, skirt 14.2, 6 M6, 2 handle holes Ø4.5"),
("09","Lid Ceramic Holder","盖子陶瓷托架","0.8 mm 304/430 SS","plate OD 146.4, bolt wall Ø133.3 (6 M6), lip Ø143.7, 48 vents Ø3.5 on Ø139.7 (= 05), ceramic lid disk pocket"),
("10","Lid Handle","提手","Ø8 304 SS rod","2 posts, M4 tapped 10 deep"),
("11","Lid Hinge Strap (placeholder)","盖子铰链片（示意）","1.2 mm 304 SS","factory fits its stock hinge"),
("13","Hinge Pin (placeholder)","铰链销（示意）","Ø5 304 SS rod","30 long"),
("14","Steel Tray","钢托盘","3 mm steel","3 leg holes Ø6.6 on Ø120")]
out=[f"# Parts list ({TAG})","",f"Generated from `FAB_PACKAGE_{TAG}` (the only current machining files, see [CURRENT.md](CURRENT.md)) by `Scripts/make_parts_list.py`. Sizes in mm; overall size and volume measured from each STEP file.","",
"R2: the body is 2.66 mm taller above the ceramic seat (01 and 02 are 125.36 tall), so the real ceramic stack (core 90.4 + base plate 4.9 = 95.3) ends flush with the 05 cap top. 05 and every lid part are the same parts, 2.66 higher.","",
"| # | Part | 零件 | Material | Key sizes | Overall (x × y × z) | Volume cm³ |","|---|---|---|---|---|---|---|"]
for no,en,zh,mat,key in rows:
    fn=[f for f in os.listdir(P) if f.startswith(no+"_")][0]; s=import_step(P+fn); bb=s.bounding_box()
    out.append(f"| {no} | {en} | {zh} | {mat} | {key} | {bb.max.X-bb.min.X:.1f} × {bb.max.Y-bb.min.Y:.1f} × {bb.max.Z-bb.min.Z:.1f} | {s.volume/1000:.2f} |")
out+=["","We supply (not in the machining package):","","| Item | Qty | Size |","|---|---|---|",
"| Ceramic heater core | 1 | Ø92.5 / Ø81.5, 90.4 tall (measured), 4 glass slots 10.5 |",
"| Ceramic base disk | 1 | Ø92.5, 4.9 thick (core + base = 95.3, measured) |",
"| Ceramic lid disk | 1 | Ø92.5 with raised centre |",
"| Ceramic spacer rings | 5 | ID 136.1 / OD 144.1; all 10 mm tall (3 body + 2 lid, one size since 2026-11-10); 6 Ø6.6 holes each |",
"| Ceramic feet | 3 | on Ø120 leg circle |",
"| M6 bolts + nuts | 30 | 6 per ring × 5 rings, same lengths as before |",
"| M4 screws | 2 | handle |",
"| Leg screws M6 | 3 | |",""]
open(R+"PARTS_LIST.md","w",encoding="utf-8").write("\n".join(out)); print("parts list ok")
