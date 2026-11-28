"""Build FAB_PACKAGE_2026-11-28 from the approved design (see CURRENT.md).

2026-11-28 (Matt, 1:46 AM): stainless M6 projection weld nuts at every bolt, welded inside their part (01, 03, 06, 09),
and the 11/18 thick hinge (H1/H2/H3) moved from the 257.5 lid bolt to 292.5 on its own 2 holes per leaf (see the
WELD NUTS + HINGE block below and CURRENT.md). HNC_GEN=2026-11-12 HNC_OUT=/tmp/x rebuilds FAB_PACKAGE_2026-11-12.

2026-11-12 change (Matt, ~4 AM): his smallest glass slurper is 21 mm bowl-to-bend, so the top cap ring (ceramic OD to
the 05 cap edge) goes 28.4 -> 20.0: insulation 20.6 -> 14.6 (inner tube in DI = 6.0 vs R2), air gap 4.4 -> 3.0 (outer
tube in DO = 7.4), top cap lip past the outer tube 1.5 -> 0.5 (05 plate edge in 8.4). Not a uniform shift, so the radii
below are tied to the part they follow: inner tube (01, 06, 03 plate edge + bolt wall, 05 inner sleeve, 09 bolt wall,
leg circle, every bolt's nut), outer tube (02, 07, 04 / 08 skirts, 05 tabs, 09 plate + lip, groove ends, hinge, every
bolt's head), air gap (spacer rings, vents). Things that no longer fit and changed (see CURRENT.md 2026-11-12):
05 loses its outer skirt (a 1.2 sheet cannot hang outside the tube in a 0.5 lip; the 6 bolt tabs stay outside the tube,
bent down from ears in the plate); 04 / 08 keep their skirts 1.5 past the outer tube (they carry bolt rings); vents
Ø3.5 -> Ø3.0 (= the air gap); 03 riser at the centering wall (r 47.25, was 52), wire holes r 58 -> 53.5 and the 2 lead
holes 180/190 -> 185/195 (clear of the 172.4 seat bolt and its nut); legs r 60 -> 54.
HNC_GEN=R2 HNC_OUT=/tmp/x rebuilds FAB_PACKAGE_2026-11-08-R2 exactly (regression check).
Later on 2026-11-12 (Matt, 4:50 AM): 5 bolts per ring (G["bolt"] = hnc_params.ring_screw_angles = 41.5 + n*72, centred
between the 4 glass slots; was 6 at 52.4 + n*60) on all 5 rings; 05 has 5 tabs; hinge strap + pin turned onto the 257.5
lid bolt; heater lead holes 160/170 (185/195 sat under the 185.5 bolt); legs 77.5/221.5/293.5 (the 40 leg sat under the
41.5 bolt). Viewer bolt sets are copied from one template onto the new angles, feet and leg screws turned onto LEGS.
Later again (Matt, 5:19 AM): legs back to EVEN 120 deg at 5.5 / 125.5 / 245.5 (r 54), 12 deg off the nearest bolt, which the
smaller M5 leg screw (head Ø8.5) clears; leg holes Ø5.5 in 03 / 04 / 14; tray 1.2 lower so the 25.0 feet no longer run 1.2
into the 04 floor; feet + leg screws drawn here at true size.

2026-11-08 R2 change (Matt, calipers on the REAL ceramic): bare core 90.4, core + base plate 95.3, but the drawn room from
03's seat (z -0.44) to the 05 cap top (92.2) was 92.64, so the real ceramic stood 2.66 proud and the lid could not close.
The body gets U = hnc_params.body_raise = 2.66 taller ABOVE the seat: 03, 04, the feet, leg holes, wire holes, the bottom
and seat bolt rings do not move. 01 and 02 are 2.66 taller (at the top); their top bolt ring (59 -> 61.66), glass slots
and 01's groove passes go up 2.66. 05 and the whole lid (06, 07, 08, 09, 10, 11, 13, lid bolts, lid spacers) move up
2.66 unchanged in shape. The 02 perforation rows above the seat ring are re-spaced over the taller wall (same Ø4 @ 6 mm,
same 12 rows): the middle block is centred in its band (+1.33), the 2 rows above the top ring go up with it (+2.66).
HNC_RAISE=0 HNC_OUT=/tmp/x rebuilds the R1 (2026-11-08) package exactly, for regression checks.

Sources: cad-source/*.step are the Sept 9 solids. Since 2026-11-08 the parts whose size depends on the body radius
(01, 02, 04, 06, 07, 08) are REBUILT here from their source features (same holes, slots, perforation rows, heights);
11, 13 are moved with the hinge; 10 and 14 still come from their source solids. Every change made on 2026-09-28,
2026-09-30, 2026-10-16 and 2026-11-08 is applied below, in code, so the package can be rebuilt exactly.
(FAB_PACKAGE_2026-09-28 = this script at git commit d3b3b31; FAB_PACKAGE_2026-10-16 = commit c961d69, and this script
with HNC_SHRINK=0 rebuilds it.)

2026-11-08 change (glass slurper fit, Matt): a terp slurper must straddle the top cap ring (bowl in the chamber, male
joint outside); its bowl-to-joint gap is 31.0 mm, the ring measured 33.8 mm on the plastic print. The insulation between
the ceramic OD (r 46.25) and the inner tube goes 24.6 -> 20.6 (hnc_params.insulation_gap), so EVERY radius at or outside
the inner tube moves in SHRINK = 4.0 mm (diameters -8): 01, 02, 03 outer part + bolt wall, 04, 05, 06, 07, 08, 09 outer
parts, the leg screws, the 6 bolt lines, the hinge, the ceramic spacer rings. Sheet thicknesses, hole sizes, slot widths,
perforation size and pitch (Ø4 @ 6 mm), all heights, the ceramic heater core and the ceramic lid disk do not change.
Inside the inner tube nothing moves except the leg screws (they sit against 03's bolt wall): 03's raised seat (r 36.25-52)
and the 3 wire holes (r 58) stay put.

2026-10-16 change (Tianrun's plastic print on the REAL ceramic): with the cap on, the ceramic top sat 5.06 mm below
the top of 05 (Alice's caliper, 2026-10-12), and the ceramic glass slots ran ~5.3 mm deeper than the cap grooves.
Matt (10/12): ceramic top FLUSH with the cap TOP. Ceramic does not change; only metal:
  03  middle of the plate raised SEAT_UP (one part, no spacer), centering wall moved up with it
  05  groove bottoms lowered SLOT_DROP to meet the real ceramic slot bottom
  01  glass slots lowered SLOT_DROP with them (0.2 clearance kept)
  09  ceramic lid disk pocket + shelf up CAP_T: the disk now sits on the flush ceramic, its face level with 09's plate
Run:  .venv-cad/bin/python Scripts/build_current_package.py
      (HNC_SHRINK=0 HNC_OUT=/tmp/x  -> the 2026-10-16 geometry, for regression checks; viewers are only refreshed for
       the real build)
"""
import math, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import *
import trimesh
import hnc_params as HP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "cad-source")
GEN = os.environ.get("HNC_GEN", "2026-11-28")
NEW = GEN == "2026-11-28"   # weld nuts at every bolt + the hinge (H1/H2/H3) at 292.5 on its own holes; "2026-11-12" rebuilds FAB_PACKAGE_2026-11-12
if GEN == "R2":   # the 2026-11-08 R2 geometry (and with HNC_SHRINK / HNC_RAISE the older ones)
    G = dict(gap=20.6, air=4.4, lip=1.5, vent_r=1.75, wire_r=58.0, leads=(180.0, 190.0), step_r=52.0, skirt05=True,
             bolt=[52.4 + 60 * k for k in range(6)], legs=(40, 160, 280), hinge=292.4, leg_hr=3.3, tray_drop=0.0)
else:
    G = dict(gap=HP.insulation_gap, air=HP.air_gap, lip=HP.top_cap_lip, vent_r=HP.vent_r, wire_r=HP.wire_hole_r,
             leads=HP.lead_hole_angles, step_r=HP.seat_step_r, skirt05=True,
             bolt=list(HP.ring_screw_angles), legs=tuple(HP.leg_angles), hinge=HP.HINGE_ANGLE_DEG if NEW else HP.HINGE_ANGLE_DEG_1112,
             leg_hr=HP.leg_hole_d / 2, tray_drop=HP.tray_drop)
D = float(os.environ.get("HNC_SHRINK", 24.6 - G["gap"]))   # inner tube in vs 2026-10-16 (4.0 R2, 10.0 2026-11-12)
DO = D + (4.4 - G["air"])                                 # outer tube in (4.0 R2, 11.4 2026-11-12)
DC = DO + (1.5 - G["lip"])                                # 05 top cap edge in (4.0 R2, 12.4 2026-11-12)
OUT = os.environ.get("HNC_OUT", os.path.join(ROOT, "FAB_PACKAGE_" + GEN))
U = float(os.environ.get("HNC_RAISE", HP.body_raise))   # 2.66: everything above the seat goes up this much (R2)
UP = Pos(0, 0, U)
TOP = 91.0 + U                            # tube tops (93.66)
ZB_TOP = 59.0 + U                         # top bolt ring, moves with the cap tabs (61.66)
REAL = "HNC_OUT" not in os.environ and NEW
T = 0.8                                   # inside parts
BOLT = G["bolt"]                          # one bolt clocking for every ring: 5 x 72 deg from 41.5 (2026-11-12 later; 6 x 60 from 52.4 before)
LEAD_R03 = 4.0 if GEN == "R2" else HP.lead_hole_d03 / 2   # 2026-11-21: Ø10 so the Ø8 porcelain beads pass (Ø8 before)
WIRE = [(G["leads"][0], LEAD_R03), (G["leads"][1], LEAD_R03), (315.0, 3.2)]   # heater leads (03: the beaded lead passes), thermocouple Ø6.4
# (2026-09-30 audit: were 183/188, only 5.06 mm apart at r 58, so the two Ø8 holes merged into one slot; now 2.1 mm web)
R_WIRE = G["wire_r"]                      # inside 03's bolt wall (r 58 until 2026-11-12, then 53.5: 03's bolt wall moved to 59.85)
# 2026-11-20: in 04 the two lead holes are Ø11.5 at r 49 for Skutt porcelain kiln insulators (lip on the floor, body down)
WIRE04 = [(a, R_WIRE, r) for a, r in WIRE] if GEN == "R2" else [(a, HP.lead_hole_r04, HP.lead_hole_d / 2) if r == LEAD_R03 else (a, R_WIRE, r) for a, r in WIRE]
# 2026-09-30 audit: leg screws at r 65.85 put the M6 head's flats right on 01's inside face (70.85) and its corners
# 0.8 mm into the wall; moved in to r 64.0 (corners at 69.8, 1 mm clear) in 03, 04 and the tray.
# 2026-11-08: moved in with the tube, r 60.0 (corners 65.8, same clearance to 03's bolt wall).
# 2026-11-12: r 54.0 (head corners 59.85 = 03's bolt wall line, inner corners 48.15 clear of the r 47.25 riser).
# 2026-11-12 (5-bolt rings): legs 77.5 / 221.5 / 293.5, midway between bolts (40 / 160 / 280 before; the source tray's holes are there)
# 2026-11-12 (Matt 5:19 AM): legs back to even 120 deg, 5.5 / 125.5 / 245.5 (12 deg off the nearest bolt), M5 screws, Ø5.5 holes
LEG_R, LEG_SRC, LEGS, LEGS_SRC = 64.0 - D, 65.85, G["legs"], (40, 160, 280)
LEG_HR = G["leg_hr"]                      # leg hole radius: 2.75 (M5) since 2026-11-12 5:19 AM, 3.3 (M6) before
TRAY_Z = -G["tray_drop"]                  # 14 tray moved down 1.2 (2026-11-12): feet 25.0 = tray top -57.9 to 04 underside -32.9

# ── body / lid radii (2026-10-16 values minus D) ────────────────────────────────────────────────────────────────
R01I, R01O = 70.85 - D, 71.65 - D         # 01 / 06 inner tube (0.8)
R02I, R02O = 76.05 - DO, 77.25 - DO       # 02 / 07 outer perforated tube (1.2)
R02M = (R02I + R02O) / 2
RCAP = 78.75 - DO                         # 04 / 08 cap OD (skirt outside the outer tube: 1.5 past it, always)
R05 = 78.75 - DC                          # 05 top cap line (plate edge = R05 - 0.1): 1.5 past the tube in R2, 0.5 since 2026-11-12
R_SP_I, R_SP_O = 72.05 - D, 76.05 - DO    # ceramic spacer rings fill the air gap (0.4 off the inner tube, viewer only, we supply them)

def solid(x): return x if not isinstance(x, ShapeList) else Compound(children=list(x))
def ring(ri, ro, z0, z1):
    return Pos(0, 0, z0) * (Cylinder(ro, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))
                            - Cylinder(ri, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
def vhole(ang, r, rad, z0, z1):
    a = math.radians(ang)
    return Pos(r * math.cos(a), r * math.sin(a), z0) * Cylinder(rad, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))
def rhole(ang, r_mid, z, rad=3.3, length=8):
    return Rot(0, 0, ang) * Pos(r_mid, 0, z) * Rot(0, 90, 0) * Cylinder(rad, length)
def src(name): return solid(import_step(os.path.join(SRC, name + ".step")))
def cut_all(base, tools):
    return base - Compound(children=list(tools)) if tools else base

CAP_T = 1.2                  # top cap sheet; the lid now sits on it, so every lid part is raised by this much
SLOTS = [6.5, 77.1, 147.7, 218.3]   # glass slots (hnc_params)
LIFT = Pos(0, 0, CAP_T)
# 2026-10-16: measured on Tianrun's print of the 09-28 files over the real ceramic, not derived from the drawn ceramic
# stack (drawn 96.5 tall seat-to-top; the gap says the real one is ~92.6, cause unknown). Raise = the measured gap.
SEAT_UP = 5.06              # ceramic top was this far below the 05 cap top -> raise the seat this much
SLOT_DROP = 0.24            # Alice's 5.3 slot mismatch minus SEAT_UP: real slot bottom ends this far below the groove
SEAT_Z = -5.5 + SEAT_UP     # -0.44 = new ceramic seat face
STEP_R = G["step_r"]        # riser of the raised middle (52.0 until 2026-11-12, then 47.25 = on the centering wall line,
                            # so the leg holes and wire holes fit between it and the bolt wall)
SLOT_R = 5.25                                   # half of the 10.5 slot = radius of its round bottom
SLOT_ZC = 67.5 - SLOT_DROP + SLOT_R             # centre of the round bottom (72.51; was 72.75 before 2026-10-16), R1 frame
def u_solid(L, rad, z_top, zc=SLOT_ZC):
    return (Pos(0, 0, (zc + z_top) / 2) * Box(L, 2 * rad, z_top - zc)
            + Pos(0, 0, zc) * Rot(0, 90, 0) * Cylinder(rad, L))

# perforation rows of the Sept 9 tubes (Ø4 @ 6 mm; heights do not change). Body rows skip the 3 spacer-ring bands and
# the cap skirt; lid rows drop any hole whose centre is within 5.85 of a bolt hole centre (the source tube's rule). Holes per row = int(2*pi*r_mid / 6) (80 at
# the old r 76.65, 76 at r 72.65), every other row offset 3 mm, exactly the generator's rule.
BODY_ROWS = ([-14.7, -8.7] + [z + U / 2 for z in (9.3, 15.3, 21.3, 27.3, 33.3, 39.3, 45.3, 51.3)]
             + [z + U for z in (69.3, 75.3)])   # parity from z = -26.7 + 6*i; R2: middle block centred in the taller band
                                                 # (seat ring top 9 .. top ring bottom 52+U), top 2 rows up with the top ring
LID_ROWS = [96.0, 102.0, 108.0, 114.0]                                                 # pre-lift, parity from z = 96 + 6*i
def perf_tools(rows, z_first, bolt_z, extra=()):
    n = int(2 * math.pi * R02M / 6)
    out = []
    for z in rows:
        i = round((z - z_first) / 6)
        off = math.degrees(3.0 / R02M) if i % 2 else 0.0
        for k in range(n):
            a = k * 360.0 / n + off
            if any(math.hypot(R02M * math.radians((a - b + 180) % 360 - 180), z - bz) < 5.85 for b in BOLT for bz in bolt_z):
                continue
            if any(math.hypot(R02M * math.radians((a - b + 180) % 360 - 180), z - bz) < 5.85 for b, bz in extra):
                continue   # 2026-11-28: same rule around the hinge holes
            out.append(rhole(a, R02M, z, rad=2.0, length=4))
    return out

parts = {}
# 01 inner wall (rebuilt 2026-11-08 at r R01I-R01O): plain tube, 18 M6 holes at the 3 bolt rings, 4 glass slots.
# The Sept 9 tube's wire slot, TC hole and their mirror copies were patched shut on 2026-09-28, and its 10.5 glass slots
# lie wholly inside the 13.3 widened slots cut below, so the rebuilt tube is the same part.
t = ring(R01I, R01O, HP.housing_bottom_z, TOP)
t = cut_all(t, [rhole(a, (R01I + R01O) / 2, z) for a in BOLT for z in (ZB_TOP, -24.0, 2.15)])
parts["01_Inner_Wall_Tube"] = solid(t)
# 02 outer perforated tube (rebuilt 2026-11-08): tube, 18 M6, 4 glass slots (10.5, R5.25 bottom at z 67.5, unchanged
# depth), perforation rows. Holes first, slots last, as in the source (the slots cut through the top 2 rows).
t = ring(R02I, R02O, HP.housing_bottom_z, TOP)
t = cut_all(t, [rhole(a, R02M, z) for a in BOLT for z in (ZB_TOP, -24.0, 2.15)] + perf_tools(BODY_ROWS, -26.7, []))
t = cut_all(t, [Rot(0, 0, a) * Pos(R02M, 0, 0) * u_solid(4.0, SLOT_R, 95.0 + U, zc=67.5 + SLOT_R + U) for a in HP.slot_positions])
parts["02_Outer_Perforated_Tube"] = solid(t)
# 03 support ring: plate + disk-centering wall + bolt-on outer wall (6 seat-bolt holes) + leg holes + wire holes
# 2026-09-30 audit: plate + outer wall were line-to-line with 01's inside face and the centering wall with the
# ceramic base disk (r 46.25); both now 0.2 mm clear
# 2026-10-16: the middle (r 36.25-52) is raised SEAT_UP so the real ceramic ends flush with the 05 cap top. The outer
# part of the plate, the bolt wall, the 6 seat bolts, the leg holes and the wire holes all stay exactly where they were
# (raising the whole ring would put the bolt holes into 02's vent rows). One part: plate + riser + raised land + walls.
# 2026-11-08: plate edge and bolt wall in by D with 01 (0.2 clear kept); seat, riser, centering wall, wire holes stay.
sr = (ring(STEP_R, R01I - 0.2, -6.3, -5.5)               # outer plate: unchanged height
      + ring(STEP_R - T, STEP_R, -6.3, SEAT_Z)           # riser, 0.8 wall
      + ring(36.25, STEP_R, SEAT_Z - T, SEAT_Z)          # raised middle = the ceramic seat
      + ring(46.45, 47.25, SEAT_Z, 3.0 + SEAT_UP)        # centering wall, moved up with the seat
      + ring(R01I - 1.0, R01I - 0.2, -5.5, 8.5))         # bolt wall
for a in BOLT: sr -= rhole(a, R01I - 0.6, 2.15, length=6)
# (2026-11-20, Matt: leg holes in 03 closed; the legs are screwed onto 04 before 03 goes on, and the leg screws stand on
#  the 04 floor and never reach 03)
for a, r in WIRE: sr -= vhole(a, R_WIRE, r, -8, -4)
parts["03_Support_Ring"] = solid(sr)
# 04 bottom cap (rebuilt 2026-11-08): floor disk (1.2, z -32.9..-31.7) + skirt (1.2, up to z -15.7) at RCAP, 6 M6 in
# the skirt on the bottom bolt ring, wire/TC holes under 03's holes, 3 leg holes Ø6.6. (The Sept 9 cap's old tube-gap
# wire holes and Ø13.2 leg holes, plugged on 2026-09-30, are simply not drawn.)
bc = Pos(0, 0, -32.9) * Cylinder(RCAP, 1.2, align=(Align.CENTER, Align.CENTER, Align.MIN)) + ring(RCAP - 1.2, RCAP, -32.9, -15.7)
bc = cut_all(bc, [rhole(a, RCAP - 0.6, -24.0) for a in BOLT] + [vhole(a, rr, r, -40, -10) for a, rr, r in WIRE04]
             + [vhole(a, LEG_R, LEG_HR, -40, -10) for a in LEGS])
parts["04_Bottom_Cap"] = solid(bc)
# 05 one-piece top cap, redrawn clean 2026-09-28 from the pre-June cap's layout:
#   flat top (1.2) sitting ON the tube tops, open in the middle so the ceramic core top stays bare for the lid disk;
#   sleeves hugging the ceramic, the inner tube and the outer tube (0.2 mm clearance each);
#   6 tabs down the outside to the top bolt line (Ø6.6 at z 59); 4 glass slots straight through, lined up with the walls;
#   vent holes over the gap between the tubes. The 5 old screw ears are gone (nothing screws into them anymore).
# (OCC fails cutting the slots through the fused cap, so each ring gets its slots first, then everything fuses)
# 2026-11-08: plate edge, inner-tube sleeve, skirt, tabs and vents in by D; the ceramic sleeve stays at the ceramic.
SB0, SB1 = 43.42, 83.32 - DO                    # slot cutter: from inside the ceramic sleeve to past the skirt
def slot_box(a): return Rot(0, 0, a) * Pos((SB0 + SB1) / 2, 0, 86.13) * Box(SB1 - SB0, 10.5, 16.3)
rings = []
# 2026-11-12: the plate edge is only 0.4 past the outer tube, so the outer skirt is gone; the 6 tabs stay outside the
# tube and now run up to the plate top (ears in the plate, bent down).
for ri, ro, z0, z1 in [(46.45, R05 - 0.1, 91.0, 91.0 + CAP_T),      # top plate
                       (46.45, 47.65, 81.0, 91.2),                   # sleeve around the ceramic core
                       (R01I - 1.0, R01I - 0.2, 86.0, 91.2)] + ([
                       (R02O + 0.2, RCAP - 0.1, 81.0, 91.2)] if G["skirt05"] else []):   # skirt outside the outer tube
    r = ring(ri, ro, z0, z1)
    for a in SLOTS: r = r - slot_box(a)
    rings.append(r)
cap = rings[0]
for r in rings[1:]: cap = cap + r
R_TAB = RCAP - 0.7                              # tab mid-sheet = outer tube OD + 0.8 (78.05 before 2026-11-08)
TAB_Z1 = 81.2 if G["skirt05"] else 91.0 + CAP_T   # tab top: into the skirt (R2) / up to the plate top (2026-11-12)
for a in BOLT:
    cap = cap + Rot(0, 0, a) * Pos(R_TAB, 0, (51.0 + TAB_Z1) / 2) * Box(CAP_T, 14.0, TAB_Z1 - 51.0) - rhole(a, R_TAB, 59.0, length=6)
R_VENT = (R01O + R02I) / 2                      # vents over the middle of the air gap (69.85 R2, 63.15 2026-11-12)
VENT_ANGLES = [k * 6.0 for k in range(60) if min(abs((k * 6.0 - s_ + 180) % 360 - 180) for s_ in SLOTS) > 9]   # 48
VENT_R = G["vent_r"]                            # Ø3.5 until 2026-11-12, then Ø3.0 = the 3.0 air gap
for a in VENT_ANGLES:
    cap = cap - vhole(a, R_VENT, VENT_R, 90.0, 93.0)
# 2026-09-28 (Matt): metal slot grooves, the SAME shape as the ceramic's glass slot. The slot in the core and both
# tubes is 10.5 wide with a round bottom (R5.25, lowest point z 67.5). Each groove's inside is exactly that profile,
# so it lines up flush with the ceramic slot and butts right up against the ceramic (0.2 mm). 1.2 sheet wraps it.
# Insulation is never open, and the grooves bridge each slot so the cap stays ONE piece.
def groove(a, r0, r1):
    L, rm = r1 - r0, (r0 + r1) / 2
    g = u_solid(L, SLOT_R + CAP_T, 91.0 + CAP_T) - u_solid(L + 2, SLOT_R, 95.0)
    return Rot(0, 0, a) * Pos(rm, 0, 0) * g
G_END = 75.55 - DO                               # groove end: corners clear the outer tube (sqrt(71.85^2 - 6.45^2) = 71.56 >= 71.55)
for a in SLOTS:   # ONE groove per slot (Matt): ceramic -> just short of the outer tube, straight through the inner tube.
    cap = cap + groove(a, 46.45, G_END)
# the inner tube's 4 glass slots are widened to let the groove pass: groove outside (R6.45) + 0.2 clearance
for a in SLOTS:
    parts["01_Inner_Wall_Tube"] = solid(parts["01_Inner_Wall_Tube"] - UP * (Rot(0, 0, a) * Pos((R01I + R01O) / 2, 0, 0) * u_solid(6.0, SLOT_R + CAP_T + 0.2, 95.0)))
# 05 is drawn above in the R1 frame (tube top 91) and moved up U as one piece (R2): same part, sits on the taller tubes
parts["05_One_Piece_Top_Cap"] = solid(UP * cap)
# 2026-09-30 audit: 09's bottom plate (z 92.2-93.0) sat in the same band as both lid tube bottoms, so the tubes are
# shortened 0.8 mm from the bottom and stand ON 09's plate.
LID_FLOOR = 91.0 + CAP_T + T                    # 93.0 = top of 09's plate
def above(z): return Pos(0, 0, z) * Cylinder(100, 100, align=(Align.CENTER, Align.CENTER, Align.MIN))
LID_BOLT_Z = (99.0, 119.0)                      # pre-lift (100.2 / 120.2 in place)
# 06 / 07 lid tubes (rebuilt 2026-11-08 like 01 / 02; source z 91-126 before the lift)
t = cut_all(ring(R01I, R01O, 91.0, 126.0), [rhole(a, (R01I + R01O) / 2, z) for a in BOLT for z in LID_BOLT_Z])
parts["06_Lid_Inner_Tube"] = solid(UP * (LIFT * t & above(LID_FLOOR)))   # R2: the whole lid goes up U with the cap
t = cut_all(ring(R02I, R02O, 91.0, 126.0), [rhole(a, R02M, z) for a in BOLT for z in LID_BOLT_Z] + perf_tools(LID_ROWS, 96.0, LID_BOLT_Z,
    extra=[(b, LID_BOLT_Z[0]) for b in (HP.hinge_hole_angles if NEW else [])]))
parts["07_Lid_Outer_Perforated_Tube"] = solid(UP * (LIFT * t & above(LID_FLOOR)))
# 08 lid top disk (rebuilt 2026-11-08): plate z 126.0-127.2 + skirt down to 113.0 (before the lift), at RCAP
# 6 holes in the skirt for the upper lid bolts
td = Pos(0, 0, 126.0) * Cylinder(RCAP, 1.2, align=(Align.CENTER, Align.CENTER, Align.MIN)) + ring(RCAP - 1.2, RCAP, 113.0, 127.2)
for a in BOLT: td -= rhole(a, RCAP - 0.65, 119.0)
# 2026-09-30 (Matt): the handle screws on. One Ø4.5 hole under each handle post; each post gets an M4 tapped hole
# (Ø3.3 drill, 10 deep) and a screw comes up from inside the lid. Posts were drawn 0.2 into the disk; now they sit on it.
HANDLE_POSTS = [(-38.36, 27.46), (7.87, 46.51)]
for x, y in HANDLE_POSTS: td -= Pos(x, y, 126.6) * Cylinder(2.25, 10)   # plate is z 126.0-127.2 before the lift
parts["08_Lid_Top_Disk"] = solid(UP * LIFT * td)
# 09 lid ceramic holder: sits on the top cap (z 92.2). The ceramic lid disk still rests on the core top (z 91,
# raised center down in the bore), so the pocket wraps its edge from the lid bottom up and the shelf stays at the
# disk's top (z 96.05); the disk's lower 1.2 mm passes through the cap's center opening. Disk glued in.
Z0 = 91.0 + CAP_T
wall_ri = 46.25 + 0.2
# 2026-09-30 audit: the upright bolt wall was drawn at r 70.7-71.5, inside 06's wall (r 70.85-71.65), and the small
# outer lip at r 76.4-77.2 was inside 07's wall (r 76.05-77.25). Both now sit 0.2 mm inside their tube.
UP_RO = R01I - 0.2                              # 06 inner face - 0.2
LIP_RO = R02I - 0.2                             # 07 inner face - 0.2
PLATE_RO = R02O - 0.05                          # 77.2 before 2026-11-08
# 2026-10-16: the ceramic top is now flush with the cap top (z 92.2), so the lid disk sits 1.2 higher: its flat face
# is level with the underside of 09's plate (flush with the metal), only its raised centre goes into the ceramic.
SHELF = 96.05 + CAP_T                           # 97.25
h = (ring(38.8, wall_ri + T, SHELF, SHELF + T) + ring(wall_ri, wall_ri + T, Z0, SHELF + T)
     + ring(wall_ri, PLATE_RO, Z0, Z0 + T) + ring(UP_RO - T, UP_RO, Z0 + T, 105.0 + CAP_T) + ring(LIP_RO - T, LIP_RO, Z0 + T, 94.0 + CAP_T))
for a in BOLT: h -= rhole(a, UP_RO - T / 2, 99.0 + CAP_T, length=6)
# 2026-11-08 (Matt, option C): 09's plate covered the 05 cap vents when the lid is closed. 48 Ø3.5 holes through the
# plate at the SAME radius and angles as the 05 vents (the lid is drawn closed, in the body's frame), so air goes
# straight up. A Ø3.5 at r 69.85 reaches r 71.6, 0.55 into the outer lip (r 71.05-71.85), so the same cylinder runs up
# through the lip: a local notch at each hole, the lip stays everywhere else and still locates 07 (07 ID 72.05).
for a in VENT_ANGLES: h -= vhole(a, R_VENT, VENT_R, Z0 - 1.0, 94.0 + CAP_T + 1.0)
parts["09_Lid_Ceramic_Holder"] = solid(UP * h)
hd = Pos(0, 0, CAP_T + 0.2) * src("10_Lid_Handle")   # bottom of the posts at 128.4 = top of 08 (handle at r < 52: unchanged)
for x, y in HANDLE_POSTS: hd -= Pos(x, y, 128.4) * Cylinder(1.65, 10.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
parts["10_Lid_Handle"] = solid(UP * hd)
# 11 strap + 13 pin (placeholder hinge, Tianrun fits their stock hinge): moved in D along the 292.4° bolt line, so the
# strap's bolt hole stays on its lid bolt and the pin stays in the barrels (pivot r 81.5 -> 77.5)
# 2026-11-12 (5-bolt rings): then turned about the axis onto the 257.5° lid bolt (G["hinge"]); the source solids are at 292.4
HA = math.radians(292.4)
HMOVE = Pos(-DO * math.cos(HA), -DO * math.sin(HA), 0)   # the strap sits on the lid outer tube
HROT = Rot(0, 0, G["hinge"] - 292.4)
parts["11_Lid_Hinge_Strap"] = solid(HROT * UP * HMOVE * LIFT * src("11_Lid_Hinge_Strap"))
parts["13_Hinge_Pin"] = solid(HROT * UP * HMOVE * LIFT * src("13_Hinge_Pin"))
tr = src("14_Steel_Tray")   # floor z -59.7 to -56.7 (outline 204.5 wide, well clear of the cap: not resized)
for a in LEGS_SRC: tr += vhole(a, LEG_SRC, 3.5, -59.7, -56.7)   # plug the source tray's holes
for a in LEGS: tr -= vhole(a, LEG_R, LEG_HR, -62, -54)
parts["14_Steel_Tray"] = solid(Pos(0, 0, TRAY_Z) * tr if TRAY_Z else tr)

# ── 2026-11-28 (Matt 1:46 AM "Yes, make it real"): WELD NUTS + HINGE AT 292.5 ──────────────────────────────────────
# Every M6 bolt threads into a stainless M6 projection weld nut (DIN 929, A2) that the factory welds to the inside face
# of its part, so every bolt goes in from outside and comes back out for service. The nut is PART of its part
# (weldment): one solid in the STEP / STL, drawn orange in the viewers from that part's first step.
#   01: bottom ring 5 + top ring 5 + hinge body leaf 2 = 12      03: seat ring 5 (on the bolt wall)
#   09: lower lid ring 5 + hinge lid leaf 2 = 7 (on the bolt wall) 06: upper lid ring 5            total 29
# Hinge = the 11/18 thick hinge (H1 body leaf, H2 lid leaf, H3 pin; Scripts/build_hinge_2026-11-18.py) turned from the
# 257.5 lid bolt to 292.5 = the middle of the slot-free arc (slots 218.50 and 6.54), on its own 2 radial M6 holes per leaf:
#   H1 at 292.5 -/+ 6.0 on the top ring line (z 61.66): H1, a new 05 hinge pad (the 05 skirt carried down like the bolt
#      tabs, 28 wide), 02, the top spacer ring, 01 -> weld nuts in 01. Ø13 spot faces on H1's flat outer face, back now curved.
#   H2 at 292.5 -/+ 18.4 on the lower lid ring line (z 102.86): H2, 07, the lower lid spacer, 06, the 09 wall -> weld nuts
#      on 09. The holes cannot be under the knuckles (the bolt head would sit in the body knuckles), so H2 gets two curved
#      wings beside the knuckles and the pin head (r 66.05-71.45, 14-24 deg off centre), the holes go through the wings.
WELD = {}
HANG = G["hinge"]
ZLL, ZUL = 99.0 + CAP_T + U, 119.0 + CAP_T + U          # lid bolt lines in place (102.86 / 122.86)
HB = [HANG + d for d in (-6.0, 6.0)]                     # H1 holes (286.5 / 298.5) = HP.hinge_hole_angles
HL = [HANG + d for d in (-18.4, 18.4)]                   # H2 holes (274.1 / 310.9)
WN = HP.weld_nut
def weld_nut(a, r_face, z, flats_up=False):
    """hex weld nut, face on the inside face r_face of its wall (0.05 into it so it fuses), corners up (flats up on 09,
    where a corner would come within 0.23 of the wall's top edge; flats up = 1.0), M6 bore"""
    e = WN["s"] / math.cos(math.radians(30))
    hx = extrude(RegularPolygon(e / 2, 6), amount=WN["m"]) - Cylinder(WN["bore"] / 2, 40)
    if flats_up: hx = Rot(0, 0, 30) * hx
    return Rot(0, 0, a) * Pos(r_face + 0.05, 0, z) * Rot(0, -90, 0) * hx     # local +Z -> inward, local +X (a corner) -> up
if NEW:
    assert [round(x, 2) for x in HB] == [round(x, 2) for x in HP.hinge_hole_angles]
    R01M = (R01I + R01O) / 2
    parts["01_Inner_Wall_Tube"] = solid(cut_all(parts["01_Inner_Wall_Tube"], [rhole(a, R01M, ZB_TOP) for a in HB]))
    parts["02_Outer_Perforated_Tube"] = solid(cut_all(parts["02_Outer_Perforated_Tube"], [rhole(a, R02M, ZB_TOP) for a in HB]))
    parts["06_Lid_Inner_Tube"] = solid(cut_all(parts["06_Lid_Inner_Tube"], [rhole(a, R01M, ZLL) for a in HL]))
    parts["07_Lid_Outer_Perforated_Tube"] = solid(cut_all(parts["07_Lid_Outer_Perforated_Tube"], [rhole(a, R02M, ZLL) for a in HL]))
    parts["09_Lid_Ceramic_Holder"] = solid(cut_all(parts["09_Lid_Ceramic_Holder"], [rhole(a, UP_RO - T / 2, ZLL, length=6) for a in HL]))
    # 05 hinge pad: the skirt (r R02O+0.2 .. RCAP-0.1) carried down to the tab bottom over the H1 width, 2 holes
    pad = ring(R02O + 0.2, RCAP - 0.1, 51.0 + U, 81.2 + U) & (Rot(0, 0, HANG) * Pos(80.0, 0, 66.1 + U) * Box(40.0, 28.0, 30.2))
    pad = cut_all(pad, [rhole(a, RCAP - 0.7, ZB_TOP, length=6) for a in HB])
    parts["05_One_Piece_Top_Cap"] = solid(parts["05_One_Piece_Top_Cap"] + pad)
    WELD["01_Inner_Wall_Tube"] = [weld_nut(a, R01I, z) for z in (-24.0, ZB_TOP) for a in BOLT] + [weld_nut(a, R01I, ZB_TOP) for a in HB]
    WELD["03_Support_Ring"] = [weld_nut(a, R01I - 1.0, 2.15) for a in BOLT]
    WELD["09_Lid_Ceramic_Holder"] = [weld_nut(a, UP_RO - T, ZLL, flats_up=True) for a in BOLT + HL]
    WELD["06_Lid_Inner_Tube"] = [weld_nut(a, R01I, ZUL) for a in BOLT]
    # ---- hinge, drawn on +X then turned to HANG (numbers as Scripts/build_hinge_2026-11-18.py) ----
    ZS = 91.0 + CAP_T + U                                 # 94.86 seam = pin height
    XB0, XL0, XO = 67.45, 66.05, 71.45
    RK, XC, W, GK, HM = 6.0, 73.55, 28.0, 0.5, 6.0
    def hbox(x0, x1, y0, y1, z0, z1): return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)
    def knuck(y0, y1): return Pos(XC, (y0 + y1) / 2, ZS) * Rot(90, 0, 0) * Cylinder(RK, y1 - y0)
    def curve(p_, r): return (p_ & (Cylinder(200, 400) - Cylinder(r, 400))).clean()
    def fuse(*ps):
        o = ps[0]
        for q in ps[1:]: o = o.fuse(q)
        return o.clean()
    def biggest(p_): return max(p_.solids(), key=lambda x: x.volume)
    yo0 = HM + GK; kb_top = ZS - RK - GK
    bl = [curve(hbox(63.0, XO, -W / 2, W / 2, 54.66, kb_top), XB0)]          # back now curved (sits on the 05 pad, 0.2)
    for a_, b_ in [(-W / 2, -yo0), (yo0, W / 2)]:
        bl += [curve(hbox(63.0, XO, a_, b_, kb_top - 0.5, ZS), XB0), hbox(XC - 0.01, XC + RK, a_, b_, ZS - RK, ZS), curve(knuck(a_, b_), XB0 + 0.1)]
    h1 = fuse(*bl)
    for d in (-6.0, 6.0):
        h1 = h1 - Rot(0, 0, d) * Pos(66.0, 0, ZB_TOP) * Rot(0, 90, 0) * Cylinder(3.3, 20)
        sf0 = (XO - 6.5 * math.sin(math.radians(6.0))) / math.cos(math.radians(6.0))     # spot face: flat Ø13 seat square to the bolt
        h1 = h1 - Rot(0, 0, d) * Pos(sf0 + 5.0, 0, ZB_TOP) * Rot(0, 90, 0) * Cylinder(6.5, 10.0)
    H1_SEAT = sf0
    h2 = fuse(curve(hbox(63.0, XO, -W / 2, W / 2, ZS + RK + GK, 108.86), XL0), curve(hbox(63.0, XO, -HM, HM, ZS + 0.1, ZS + RK + GK + 0.5), XL0),
              hbox(XC - 0.01, XC + RK, -HM, HM, ZS, ZS + RK), curve(knuck(-HM, HM), XL0 + 0.1))
    def sector(r0, r1, a0, a1, z0, z1):   # annulus between two angles (a1 - a0 < 180)
        hp = lambda a, sgn: Rot(0, 0, a) * Pos(0, sgn * 100.0, (z0 + z1) / 2) * Box(400.0, 200.0, z1 - z0 + 2)
        return ring(r0, r1, z0, z1) & hp(a0, 1) & hp(a1, -1)
    # wings: 14-24 deg below the knuckle top line (clear of the body knuckles), joined to the plate above it from 10 deg
    wings = [sector(XL0, XO, 14.0, 24.0, ZS + 0.5, 108.86), sector(XL0, XO, -24.0, -14.0, ZS + 0.5, 108.86),
             sector(XL0, XO, 10.0, 14.5, ZS + RK + GK, 108.86), sector(XL0, XO, -14.5, -10.0, ZS + RK + GK, 108.86)]
    h2 = fuse(h2, *wings)
    for d in (-18.4, 18.4):
        h2 = h2 - Rot(0, 0, d) * Pos(66.0, 0, ZLL) * Rot(0, 90, 0) * Cylinder(3.3, 20)
    pinhole = lambda dd: Pos(XC, 0, ZS) * Rot(90, 0, 0) * Cylinder(dd / 2, W + 4)
    h1 = biggest(h1 - pinhole(6.1)); h2 = biggest(h2 - pinhole(6.4))
    h3 = Pos(XC, 0, ZS) * Rot(90, 0, 0) * Cylinder(3.0, W + 1) + Pos(XC, -(W / 2 + 0.5 + 0.75), ZS) * Rot(90, 0, 0) * Cylinder(5.0, 1.5)
    HR = Rot(0, 0, HANG)
    for k in ("11_Lid_Hinge_Strap", "13_Hinge_Pin"): parts.pop(k)
    parts["H1_Hinge_Body_Leaf"] = solid(HR * h1); parts["H2_Hinge_Lid_Leaf"] = solid(HR * h2); parts["H3_Hinge_Pin"] = solid(HR * h3)
    PLAIN = dict(parts)                                   # the parts without their nuts (viewer body meshes)
    for k, nuts in WELD.items():
        w_ = parts[k]
        for n_ in nuts: w_ = w_ + n_
        parts[k] = solid(w_)

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "STEP")); os.makedirs(os.path.join(OUT, "STL"))
shutil.copy(os.path.join(ROOT, "Scripts", "package_README.txt"), os.path.join(OUT, "README.txt"))
if NEW: shutil.copy(os.path.join(ROOT, "Scripts", "BUILD_PLAN_2026-11-28.md"), os.path.join(OUT, "BUILD_PLAN.md"))
for name, shape in parts.items():
    export_step(shape, os.path.join(OUT, "STEP", name + ".step"))
    export_stl(shape, os.path.join(OUT, "STL", name + ".stl"))
    print("wrote", name, round(shape.volume, 1))
if not REAL: sys.exit(0)

# ── the viewers show exactly these parts ─────────────────────────────────────────────────────────────────────────
VIEW = {"01_Inner_Wall_Tube": "viewer-full/01", "02_Outer_Perforated_Tube": "viewer-full/02", "03_Support_Ring": "viewer-full/03",
        "04_Bottom_Cap": "viewer-full/04",
        "05_One_Piece_Top_Cap": "viewer-full/cap", "06_Lid_Inner_Tube": "viewer-lid-full/06", "07_Lid_Outer_Perforated_Tube": "viewer-lid-full/07",
        "08_Lid_Top_Disk": "viewer-lid-full/08", "09_Lid_Ceramic_Holder": "viewer-lid-full/09", "10_Lid_Handle": "viewer-lid-full/10",
        "H1_Hinge_Body_Leaf": "viewer-full/h1", "H2_Hinge_Lid_Leaf": "viewer-lid-full/h2", "H3_Hinge_Pin": "viewer-lid-full/h3"}
# 2026-11-28: a part with weld nuts is ONE glb with two meshes, "body" and "weldnuts" (the viewers paint the weldnuts
# mesh orange), so the nuts can never show up, or be left out, apart from their part.
_tmp = os.path.join(OUT, "_v.stl")
def _shape_mesh(shape):
    export_stl(shape, _tmp); m = trimesh.load(_tmp); os.remove(_tmp); return m
for name, dst in VIEW.items():
    sc = trimesh.Scene(); sc.add_geometry(_shape_mesh(PLAIN[name]), node_name="body", geom_name="body")
    if name in WELD: sc.add_geometry(_shape_mesh(Compound(children=WELD[name])), node_name="weldnuts", geom_name="weldnuts")
    sc.export(os.path.join(ROOT, dst + ".glb"))
for old in ("viewer-lid-full/11.glb", "viewer-lid-full/13.glb"):   # the placeholder strap + pin (11-12 and before)
    if os.path.exists(os.path.join(ROOT, old)): os.remove(os.path.join(ROOT, old))
import numpy as np
def _mesh(fp):
    sc = trimesh.load(fp); return sc.to_geometry() if isinstance(sc, trimesh.Scene) else sc
def snap_bodies(fp, r_target=None, dr=None):
    """move every separate body radially (no scaling): to r_target, or by dr relative to where it is drawn now"""
    sc = trimesh.load(fp); ms = sc.to_geometry() if isinstance(sc, trimesh.Scene) else sc
    out = []
    for c in ms.split(only_watertight=False):
        cx, cy = c.bounds.mean(axis=0)[:2]; r = math.hypot(cx, cy)
        if r > 1:
            m = (r_target - r) if r_target is not None else dr
            c.apply_translation([cx / r * m, cy / r * m, 0])
        out.append(c)
    trimesh.util.concatenate(out).export(fp)
# 2026-11-12 (Matt 5:19 AM): feet + leg screws are drawn here at true size on LEGS (they used to be old meshes turned
# and snapped). Foot: Ø28 x 5 base + Ø20 x 20 post (= C6 in the print set), Ø5.5 hole, from the tray top to the 04 floor
# underside. Leg screw: M5 x 40 socket head cap screw (ISO 4762: head Ø8.5 x 5) standing on the 04 floor top (z -31.7),
# down through 04, the foot and the tray, M5 washer (Ø10 x 1) + M5 nut (8 AF x 4.7) under the tray.
Z04_BOT, Z04_TOP = -32.9, -31.7
TRAY_TOP = -56.7 + TRAY_Z
def _cyl_mesh(r, z0, z1, x, y, sections=48):
    m = trimesh.creation.cylinder(radius=r, height=z1 - z0, sections=sections); m.apply_translation([x, y, (z0 + z1) / 2]); return m
def _tube_mesh(ri, ro, z0, z1, x, y):
    m = trimesh.creation.annulus(r_min=ri, r_max=ro, height=z1 - z0, sections=48); m.apply_translation([x, y, (z0 + z1) / 2]); return m
feet, screws = [], []
for a in LEGS:
    x, y = LEG_R * math.cos(math.radians(a)), LEG_R * math.sin(math.radians(a))
    feet += [_tube_mesh(LEG_HR, 14.0, TRAY_TOP, TRAY_TOP + 5.0, x, y), _tube_mesh(LEG_HR, 10.0, TRAY_TOP + 5.0, Z04_BOT, x, y)]
    zt = TRAY_TOP - 3.0                                         # tray underside
    nut = _cyl_mesh(8.0 / math.sqrt(3), zt - 1.0 - 4.7, zt - 1.0, x, y, sections=6)
    nut.apply_transform(trimesh.transformations.rotation_matrix(math.radians(a), [0, 0, 1], [x, y, 0]))
    screws += [_cyl_mesh(4.25, Z04_TOP, Z04_TOP + 5.0, x, y),          # head
               _cyl_mesh(2.5, Z04_TOP - 40.0, Z04_TOP, x, y),         # shank M5 x 40
               _tube_mesh(2.7, 5.0, zt - 1.0, zt, x, y), nut]          # washer, nut
trimesh.util.concatenate(feet).export(os.path.join(ROOT, "viewer-full", "feet.glb"))
trimesh.util.concatenate(screws).export(os.path.join(ROOT, "viewer-full", "legscrews.glb"))
trimesh.load(os.path.join(OUT, "STL", "14_Steel_Tray.stl")).export(os.path.join(ROOT, "viewer-full", "tray.glb"))
# bolts (2026-11-28): shank + hex head only; the nut is a weld nut that belongs to its part (above). Every bolt is drawn
# at true size: head 10 AF x 4 on its seat, shank Ø6 to the same tip as the 11-12 bolts (past the weld nut).
# key: (angles, head seat r, tip r, axis z)
def _hex_mesh(a, r0, r1, z):
    m = trimesh.creation.cylinder(radius=10.0 / math.sqrt(3), height=r1 - r0, sections=6)
    m.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]))   # axis -> X, a corner up
    m.apply_translation([(r0 + r1) / 2, 0, z]); m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(a), [0, 0, 1])); return m
def _shank_mesh(a, r0, r1, z):
    m = trimesh.creation.cylinder(radius=3.0, height=r1 - r0, sections=24)
    m.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]))
    m.apply_translation([(r0 + r1) / 2, 0, z]); m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(a), [0, 0, 1])); return m
BOLT_SETS = {"viewer-full/bolts_bot": (BOLT, 68.10, 53.0, -24.0), "viewer-full/bolts_seat": (BOLT, 66.0, 51.0, 2.15),
             "viewer-full/bolts_top": (BOLT, 67.30, 53.0, ZB_TOP), "viewer-lid-full/bolts_low": (BOLT, 66.0, 52.0, ZLL),
             "viewer-lid-full/bolts_high": (BOLT, 67.5, 53.0, ZUL),
             "viewer-full/bolts_hinge": (HB, H1_SEAT, H1_SEAT - 16.0, ZB_TOP),          # M6 x 16, into the 01 weld nuts
             "viewer-lid-full/bolts_hinge_lid": (HL, XO, XO - 18.0, ZLL)}              # M6 x 18, into the 09 weld nuts
for key, (angs, rh, rt, zz) in BOLT_SETS.items():
    new = trimesh.Scene()
    for i_, ang in enumerate(angs):
        nm = "b%d_%s" % (i_, ("%.1f" % ang).rstrip("0").rstrip("."))
        new.add_geometry(trimesh.util.concatenate([_shank_mesh(ang, rt, rh, zz), _hex_mesh(ang, rh, rh + 4.0, zz)]), node_name=nm, geom_name=nm)
    new.export(os.path.join(ROOT, key + ".glb"))
# ceramic spacer rings between the tubes (we supply them; not in the machining package): rebuilt at the new size,
# 6 Ø6.6 bolt holes on their bolt ring. 2026-11-10 (Matt): all five rings 10 mm, centred on their bolts (body rings were 14)
SPACERS = {"viewer-full/spacer_bot": (-29.0, -19.0, -24.0), "viewer-full/spacer_seat": (-2.85, 7.15, 2.15),
           "viewer-full/spacer_top": (54.0 + U, 64.0 + U, 59.0 + U), "viewer-lid-full/spacer_low": (95.2 + U, 105.2 + U, 100.2 + U),
           "viewer-lid-full/spacer_high": (115.2 + U, 125.2 + U, 120.2 + U)}   # R2: top + lid rings up U
_tmp = os.path.join(OUT, "_spacer.stl")
for key, (z0, z1, zb) in SPACERS.items():
    extra = HB if key.endswith("spacer_top") else HL if key.endswith("spacer_low") else []   # 2026-11-28: hinge bolts pass the top + lower lid rings
    sp = cut_all(ring(R_SP_I, R_SP_O, z0, z1), [rhole(a, (R_SP_I + R_SP_O) / 2, zb, length=6) for a in BOLT + extra])
    export_stl(solid(sp), _tmp); trimesh.load(_tmp).export(os.path.join(ROOT, key + ".glb"))
os.remove(_tmp)
# Ceramics in the viewers. R2 (2026-11-08): drawn at the REAL measured size. Base plate = the C2 print profile at its real
# 4.9 thickness (rebuilt here), on the seat; core 90.4 tall on it, top at seat + 95.3 = the cap top; its 4 slot bottoms
# stay level with the 05 groove bottoms (both up U). Lid disk: same shape, up U. All placed by absolute height (idempotent).
CORE_Z0 = SEAT_Z + HP.base_disk_t_real                  # 4.46
CORE_TOP = SEAT_Z + HP.ceramic_stack_real               # 94.86 (= 91 + CAP_T + U)
CORE_SLOT = 67.5 - SLOT_DROP + U                        # 69.92, groove inside bottom
with BuildPart() as _bp:
    with BuildSketch(Plane.XZ):
        Polygon(*[(0, 0), (38.5, 0), (38.5, 1.0), (46.25, 1.5), (46.25, HP.base_disk_t_real), (0, HP.base_disk_t_real)], align=None)
    revolve(axis=Axis.Z)
_tmp = os.path.join(OUT, "_bd.stl"); export_stl(Pos(0, 0, SEAT_Z) * _bp.part, _tmp)
trimesh.load(_tmp).export(os.path.join(ROOT, "viewer-full", "basedisk.glb")); os.remove(_tmp)
fp = os.path.join(ROOT, "viewer-lid-full", "liddisk.glb"); m = _mesh(fp)
m.apply_translation([0, 0, (90.0 + CAP_T + U) - m.bounds[0, 2]]); m.export(fp)   # drawn z 90-96 on a z 91 core top (R1 frame)
fp = os.path.join(ROOT, "viewer-full", "core.glb"); c = _mesh(fp); z0, z1 = c.bounds[:, 2]
KNOWN = {91.0: (0.0, 67.5), 92.2: (SEAT_UP, 67.5 - SLOT_DROP), round(CORE_TOP, 3): (CORE_Z0, CORE_SLOT)}   # top -> (bottom, slot)
k = min(KNOWN, key=lambda t_: abs(t_ - z1)); assert abs(k - z1) < 1e-3 and abs(KNOWN[k][0] - z0) < 1e-3, ("unknown core mesh", z0, z1)
if abs(z1 - CORE_TOP) > 1e-3:
    slot = KNOWN[k][1]
    v = c.vertices.copy(); z = v[:, 2]; lo = z <= slot
    v[lo, 2] = CORE_Z0 + (z[lo] - z0) * (CORE_SLOT - CORE_Z0) / (slot - z0)
    v[~lo, 2] = CORE_SLOT + (z[~lo] - slot) * (CORE_TOP - CORE_SLOT) / (z1 - slot)
    c.vertices = v; c.export(fp)
print("viewer meshes refreshed from the package; core", round(CORE_Z0, 2), "..", round(CORE_TOP, 2), "slot", round(CORE_SLOT, 2))
