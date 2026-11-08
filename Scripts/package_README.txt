Heat & Clean Glass Oven: machining files, 2026-11-08
Replaces every earlier package, including 2026-10-16. Metal parts only; we supply all ceramics.
Same 13 parts as before (01-11, 13, 14). No new parts.

What changed since 2026-10-16, and why:
  A glass terp slurper has to sit across the top cap ring: its bowl goes in the chamber and its male joint hangs
  outside. The slurper's gap between bowl and joint is 31.0 mm, but the top cap ring on your plastic print measured
  33.8 mm. So the whole oven gets 8 mm smaller in diameter (4 mm smaller in radius). The ring becomes about 29.8 mm.

  How: the insulation between the ceramic heater and the inner tube is 4 mm thinner (20.6 mm, was 24.6 mm).
  The ceramic heater core and the ceramic lid disk do NOT change. Every metal part outside the ceramic moves in 4 mm.
  Sheet thickness, hole sizes, slot widths, perforation (Ø4 at 6 mm pitch), and ALL HEIGHTS do NOT change.
  The air gap between the two tubes does not change (4.4 mm). The bolts are the same length.

  Part                         Old (2026-10-16)              New (2026-11-08)               Change
  01 Inner Wall Tube           ID 141.7 / OD 143.3           ID 133.7 / OD 135.3            -8.0 dia
  02 Outer Perforated Tube     ID 152.1 / OD 154.5           ID 144.1 / OD 146.5            -8.0 dia
                               80 holes per row              76 holes per row (6 mm pitch kept)
  03 Support Ring              OD 141.3, bolt wall 139.7     OD 133.3, bolt wall 131.7       -8.0 dia
                               leg holes on Ø128 (r 64)      leg holes on Ø120 (r 60)        -8.0 dia
                               (raised seat r 36.25-52 and the 3 wire holes at r 58: NOT changed)
  04 Bottom Cap                OD 157.5                      OD 149.5                        -8.0 dia
                               leg holes on Ø128             leg holes on Ø120               (wire holes not changed)
  05 One-Piece Top Cap         OD 157.3 (tabs 157.9)         OD 149.3 (tabs 149.95)          -8.0 dia
                               ring width ceramic to edge 32.4   28.4                        -4.0
                               4 grooves 29.1 long           4 grooves 25.1 long             -4.0 each
                               inner sleeve 139.7/141.3      131.7/133.3; vents on Ø147.7 -> Ø139.7
  06 Lid Inner Tube            ID 141.7 / OD 143.3           ID 133.7 / OD 135.3            -8.0 dia
  07 Lid Outer Perf. Tube      ID 152.1 / OD 154.5           ID 144.1 / OD 146.5            -8.0 dia
  08 Lid Top Disk              OD 157.5                      OD 149.5                        -8.0 dia (handle holes not changed)
  09 Lid Ceramic Holder        OD 154.4, wall 139.7/141.3    OD 146.4, wall 131.7/133.3      -8.0 dia
                               lip 150.1/151.7               lip 142.1/143.7  (ceramic lid disk pocket NOT changed)
                               NEW: 48 vent holes Ø3.5 in the plate at r 69.85 (Ø139.7), at exactly the same
                               angles as the 48 vent holes in 05, so air goes straight up through both when the lid
                               is closed. The outer lip has a small notch at each hole (0.55 mm deep) so it clears the
                               Ø3.5; the lip stays everywhere else and still locates 07.
  10 Lid Handle                not changed
  11 Hinge Strap, 13 Pin       moved in 4 mm with the lid bolt at 292.4 deg (hinge pivot r 77.5, was 81.5)
  14 Steel Tray                3 leg holes moved in to r 60 (were r 64). Outline not changed.
  Ceramic spacer rings (we supply): ID 136.1 / OD 144.1 (were 144.1 / 152.1), heights not changed.
  All 6 bolt lines are at the same angles (52.4 deg + n x 60) and heights; only their radius moved in 4 mm.

  Please check on your next print: the top cap ring, measured the same way as the 33.8 mm, should now be about 29.8 mm.

Earlier change, 2026-10-16 (still true, sizes now as above):
  Your plastic print on the real ceramic showed the ceramic top 5.06 mm BELOW the top of the 05 top cap, and the
  ceramic glass slots about 5.3 mm deeper than the metal grooves. The ceramic does not change. We want the ceramic
  top FLUSH with the top of the metal top cap, so the lid sits flat. So only the metal changes:

  03 Support Ring: the middle of the ring (where the ceramic sits, r 36.25 to r 52) is raised 5.06 mm, with a short
     0.8 mm step wall at r 52. The ceramic seat is now at z -0.44 (was -5.5). The centering wall moves up with it.
     Still ONE part. The outer part of the ring, the 6 seat bolt holes, the 3 leg holes and the 3 wire holes do NOT
     move, so 02, 04, the bolts and the tray did not change then.
  05 Top Cap: the 4 metal glass grooves are 0.24 mm deeper (inside bottom z 67.26, was 67.5), so each groove bottom
     meets the ceramic slot bottom after the raise (5.3 - 5.06 = 0.24). Everything else on the cap is the same.
  01 Inner Wall Tube: the 4 glass slots (13.3 wide, round bottom) go 0.24 mm lower with the grooves, keeping 0.2 mm
     clearance around each groove.
  09 Lid Ceramic Holder: the pocket and top shelf that hold the ceramic lid disk are 1.2 mm higher. The ceramic lid
     disk now sits on the flush ceramic top: its flat face is level with the bottom of the lid, flush with the metal
     around it; only the raised centre goes into the ceramic.

Look at the 3D first:
  Base:  https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/viewer-base-full.html
  Lid:   https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/viewer-lid-full.html
  Whole oven, lid open: https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/viewer-complete.html

Earlier changes (already in the 2026-09-28 files, still true):
  05 Top Cap: ONE piece (not shell + ring). Flat top sits on the tube tops, open in the middle over the ceramic core.
  05 Top Cap: each of the 4 glass slots has a metal groove the exact shape of the ceramic slot (10.5 mm wide, round R5.25 bottom; depth updated 2026-10-16, see top) welded under the cap, flush with the ceramic slot and butted right against the ceramic. ONE groove per slot, from the ceramic straight out to the outer tube. The inner tube's 4 glass slots are widened (13.3 mm, round bottom) so the groove passes through, so the insulation is never open and the cap stays one piece.
     Sleeves hug the ceramic, the inner tube and the outer tube. 6 tabs come down the outside and bolt through the
     top bolts. 4 glass slots straight through, lined up with the walls. Vent holes over the gap between the tubes.
  03 Support Ring: new short wall around the edge with 6 bolt holes (the seat bolts hold it).
     3 new holes in the flat plate for the heater wires (Ø8 x2) and thermocouple (Ø6.4).
  04 Bottom Cap: 3 holes right under those (same positions). Old wire holes near the edge are closed.
  01 Inner Wall Tube: no wire slot and no thermocouple hole anymore. Solid except the glass slots and bolt holes.
  08 Lid Top Disk: 6 holes in the skirt for the upper lid bolts.
  09 Lid Ceramic Holder: pocket that wraps the ceramic lid disk edge and holds it from above; 6 bolt holes in its upright wall.
  Lid parts sit 1.2 mm higher than before, on top of the top cap.
  Hinge: use your stock stainless butt hinge (approved Sept 11). Please add its screw holes to the top cap and lid; the strap + pin in these files is only a placeholder.
  Inside parts (01, 03, 06, 09) are 0.8 mm. Outside parts are 1.2 mm. Tray 3 mm.

Fit fixes, 2026-09-30 (same files, updated):
  03 / 04 / 14: the 3 leg screw holes moved in to r 64.0 (were r 65.85; now r 60.0, see 2026-11-08) so the screw heads clear the inner tube. 04's leg holes are now Ø6.6 (were Ø13.2).
  03 / 04: the 2 heater wire holes are at 180° and 190° (were 183° and 188°, which ran together into one slot).
  03: 0.2 mm clearance to the inner tube and to the ceramic base disk.
  01: all 4 glass slots are the same 13.3 mm now (one still had a step from the old wire slot).
  04: the old wire holes are fully closed, including the side wall.
  09: the upright wall and the small outer lip sit 0.2 mm inside the lid tubes (they overlapped the tube walls).
  06 / 07: 0.8 mm shorter at the bottom; they stand on 09's plate.
  08 / 10: the handle screws on. 2 x Ø4.5 holes in the lid top disk, M4 tapped hole 10 mm deep in each handle post, M4 screws from inside the lid.
  Change sheets (2026-11-08, every part, old vs new): https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/change-sheets-2026-11-08.html


加热清洁玻璃炉：加工文件，2026-11-08
替换之前所有的文件包，包括 2026-10-16。只包括金属件，陶瓷件全部由我方提供。
还是同样的13个零件（01-11、13、14）。没有新增零件。

和 2026-10-16 相比的改动和原因：
  玻璃 terp slurper 要跨放在顶盖圆环上：碗在炉膛里，公接头在外面。slurper 碗和接头之间的空隙是 31.0 mm，
  但你们塑料样品上的顶盖圆环量出来是 33.8 mm。所以整个炉子直径缩小 8 mm（半径缩小 4 mm），圆环变成约 29.8 mm。

  做法：陶瓷加热芯和内管之间的保温层薄 4 mm（20.6 mm，原来 24.6 mm）。
  陶瓷加热芯和陶瓷盖盘都不改。陶瓷外面的所有金属件都往里缩 4 mm。
  板厚、孔径、槽宽、冲孔（Ø4，孔距 6 mm）和所有高度都不改。两根管子之间的空气层不改（4.4 mm）。螺栓长度不变。

  零件                     原来（2026-10-16）               现在（2026-11-08）               变化
  01 内壁管                内径 141.7 / 外径 143.3          内径 133.7 / 外径 135.3          直径 -8.0
  02 外冲孔管              内径 152.1 / 外径 154.5          内径 144.1 / 外径 146.5          直径 -8.0
                           每排 80 个孔                     每排 76 个孔（孔距仍 6 mm）
  03 支撑环                外径 141.3，螺栓墙 139.7         外径 133.3，螺栓墙 131.7         直径 -8.0
                           脚孔在 Ø128（r 64）              脚孔在 Ø120（r 60）              直径 -8.0
                           （中间抬高的座面 r 36.25-52 和 r 58 的 3 个线孔：不改）
  04 底盖                  外径 157.5                       外径 149.5                       直径 -8.0
                           脚孔在 Ø128                      脚孔在 Ø120                      （线孔不改）
  05 一体顶盖              外径 157.3（折边片 157.9）       外径 149.3（折边片 149.95）      直径 -8.0
                           圆环宽度（陶瓷到边）32.4         28.4                             -4.0
                           4 条金属槽长 29.1                4 条金属槽长 25.1                每条 -4.0
                           内套边 139.7/141.3               131.7/133.3；通风孔圆 Ø147.7 -> Ø139.7
  06 盖子内管              内径 141.7 / 外径 143.3          内径 133.7 / 外径 135.3          直径 -8.0
  07 盖子外冲孔管          内径 152.1 / 外径 154.5          内径 144.1 / 外径 146.5          直径 -8.0
  08 盖子顶盘              外径 157.5                       外径 149.5                       直径 -8.0（提手孔不改）
  09 盖子陶瓷托架          外径 154.4，立墙 139.7/141.3     外径 146.4，立墙 131.7/133.3     直径 -8.0
                           外侧小边 150.1/151.7             142.1/143.7（陶瓷盖盘的槽位不改）
                           新增：底板上 48 个通风孔 Ø3.5，位于 r 69.85（Ø139.7），角度和 05 顶盖的 48 个通风孔完全一样，
                           盖子合上时空气直接穿过两层。外侧小边在每个孔处开一个小缺口（深 0.55 mm）让开 Ø3.5 孔；
                           其他地方小边保留，仍然给 07 定位。
  10 提手                  不改
  11 铰链片、13 销轴       跟着 292.4° 的盖子螺栓往里移 4 mm（铰链轴 r 77.5，原来 81.5）
  14 托盘                  3 个脚孔往里移到 r 60（原来 r 64）。外形不改。
  陶瓷垫圈环（我方提供）：内径 136.1 / 外径 144.1（原来 144.1 / 152.1），高度不改。
  6 条螺栓线的角度（52.4° + n x 60°）和高度都不变，只是半径往里 4 mm。

  请在下一个样品上确认：用量 33.8 mm 的同样方法量顶盖圆环，现在应该约 29.8 mm。

之前的改动，2026-10-16（仍然有效，尺寸以上面为准）：
  你们用真陶瓷试装的塑料样品显示：装上顶盖后，陶瓷顶面比 05 顶盖的顶面低 5.06 mm；陶瓷的玻璃槽比金属槽深约 5.3 mm。
  陶瓷不改。我们要陶瓷顶面和金属顶盖的顶面齐平，这样盖子才能平放。所以只改金属件：

  03 支撑环：中间放陶瓷的部分（r 36.25 到 r 52）抬高 5.06 mm，在 r 52 处有一圈 0.8 mm 的台阶。陶瓷座面现在在
     z -0.44（原来 -5.5）。定位墙跟着一起抬高。仍然是一整件。外圈、6 个座圈螺栓孔、3 个脚孔、3 个线孔都不动，
     所以当时 02、04、螺栓和托盘都不用改。
  05 顶盖：4 个金属玻璃槽加深 0.24 mm（槽内底 z 67.26，原来 67.5），抬高之后槽底正好对齐陶瓷槽底
     （5.3 - 5.06 = 0.24）。顶盖其他地方不变。
  01 内壁管：4 个玻璃槽（宽 13.3，圆底）跟着金属槽降低 0.24 mm，金属槽四周仍留 0.2 mm 间隙。
  09 盖子陶瓷托架：放陶瓷盖盘的槽位和上面的挡边抬高 1.2 mm。陶瓷盖盘现在放在齐平的陶瓷顶面上：平面和盖子底面
     一样高，和周围的金属齐平；只有中间凸起的部分伸进陶瓷里。

请先看3D：
  底座：https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/viewer-base-full.html
  盖子：https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/viewer-lid-full.html
  整机（盖子打开）：https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/viewer-complete.html

之前的改动（2026-09-28 文件里已有，仍然有效）：
  05 顶盖：改成一整件（不是外壳加压环）。平顶放在两根管子上面，中间对着陶瓷芯是开口的。
  05 顶盖：4个玻璃槽下面各焊一个金属槽，形状与陶瓷槽完全一样（宽10.5毫米，R5.25圆底；深度2026-10-16已更新，见上），紧贴陶瓷。每个槽是一整条，从陶瓷一直到外管。内管的4个玻璃槽加宽到13.3毫米（圆底），让金属槽穿过，保温棉不外露，顶盖仍是一整件。
     套边分别贴住陶瓷、内管和外管。6个折边片沿外侧往下，用最上面一排螺栓固定。4个玻璃槽直通，和管壁的槽对齐。两根管子之间的位置有通风孔。
  03 支撑环：边缘加一圈矮墙，上面有6个螺栓孔（用座圈螺栓固定）。平板上加3个孔：加热丝 Ø8 两个，热电偶 Ø6.4 一个。
  04 底盖：在这3个孔正下方加3个孔（位置相同）。靠边缘的旧线孔封掉。
  01 内壁管：不再有线槽和热电偶孔。除了玻璃槽和螺栓孔，其他地方都是实心的。
  08 盖子顶盘：裙边上加6个孔，用于盖子上排螺栓。
  09 盖子陶瓷托架：包住陶瓷盖盘边缘、从上方固定的槽位；立墙上有6个螺栓孔。
  盖子所有零件比以前高1.2mm，放在顶盖上面。
  铰链：用你们的现成不锈钢合页（9月11日已确认）。请在顶盖和盖子上加它的螺丝孔；文件里的铰链片和销只是示意。
  内部件（01、03、06、09）厚度0.8mm，外部件1.2mm，托盘3mm。

装配修正，2026-09-30（同一批文件，已更新）：
  03 / 04 / 14：3个脚螺丝孔往里移到 r 64.0（原来 r 65.85；现在 r 60.0，见 2026-11-08），螺丝头不再碰内管。04 的脚孔改为 Ø6.6（原来 Ø13.2）。
  03 / 04：2个加热线孔在 180° 和 190°（原来 183° 和 188°，两孔连成一条槽）。
  03：和内管、陶瓷底盘之间留 0.2mm 间隙。
  01：4个玻璃槽现在都是 13.3mm（其中一个还留着旧线槽的台阶）。
  04：旧线孔完全封住，包括侧壁。
  09：立墙和外侧小边都在盖子管子里面 0.2mm（原来和管壁重叠）。
  06 / 07：底部短 0.8mm，立在 09 的底板上。
  08 / 10：提手用螺丝固定。盖子顶盘上开 2 个 Ø4.5 孔，提手每个脚上攻 M4 螺纹孔（深 10mm），M4 螺丝从盖子里面往上拧。
  改动图（2026-11-08，每个零件，新旧对比）：https://nicedreamzapp.github.io/Heat-N-Clean-Glass-Oven/change-sheets-2026-11-08.html
