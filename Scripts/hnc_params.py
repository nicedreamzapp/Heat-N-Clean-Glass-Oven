"""
Heat-N-Clean Glass Oven — SHARED PARAMETERS (single source of truth for the current build)

Read by Scripts/build_current_package.py (FAB_PACKAGE_2026-11-12), Scripts/build_print_set.py,
Scripts/measure_package.py and Scripts/verify_steps.py.
2026-11-08: insulation_gap 24.6 -> 20.6 (glass slurper fit); see CURRENT.md.
2026-11-08 R2: body_raise = 2.66, the body is taller ABOVE the seat so the real ceramic stack (95.3) ends flush
with the 05 cap top; see CURRENT.md.
2026-11-12: insulation_gap 20.6 -> 14.6, air gap 4.4 -> 3.0, top cap lip past the outer tube 1.5 -> 0.5 (the smallest glass
slurper, 21 mm bowl-to-bend, must straddle the top cap ring: ring 28.4 -> 20.0); see CURRENT.md.

Units: millimetres. Origin: chamber axis = Z. z=0 is the ceramic-disk seat
reference used by the generator (housing_top_z = 91 is the chamber rim).
"""
import math
import numpy as np

# ── Sheet / material ───────────────────────────────────────────────
sheet_metal_thickness = 1.2          # OUTER / structural parts: 02, 04, 05, 07, 08, 11 (304SS 1.2 mm)
# 2026-09-09 (Matt, asked 2026-08-07): INNER parts drop to 0.8 mm — they only shield the
# ceramic and carry no load. Applies to 01 inner wall, 03 support ring, 06 lid inner tube,
# 09 lid ceramic holder, 12 hold-down ring. Mating diameters are held: inner-wall ID 141.7
# (ring seats inside it), outer tube 152.1/154.5 untouched, so the air gap grows 4.0 -> 4.4.
inner_sheet_thickness = 0.8

# ── Ceramic reference dims (drive the metal interfaces) ────────────
cylinder_height = 91
disk_thickness = 5.5
disk_body_h = 4.5
disk_lip_h = 1.0
outer_diameter = 92.5
inner_diameter = 81.5
ceramic_outer_r = outer_diameter / 2          # 46.25
ceramic_inner_r = inner_diameter / 2          # 40.75

# 2026-11-08 R2 (Matt, calipers on the REAL ceramic): bare heater core 90.4 tall (= Tianrun's 10/21 number),
# core + ceramic base plate = 95.3. The 10/16 seat raise came from a gap measured on the plastic print and left the real
# ceramic 2.66 proud of the cap. Fix: everything ABOVE the seat goes up body_raise; the seat (03) and below do not move.
ceramic_core_h_real = 90.4                   # bare core, measured
ceramic_stack_real = 95.3                    # core + base plate, measured
base_disk_t_real = round(ceramic_stack_real - ceramic_core_h_real, 3)   # 4.9 base plate overall thickness
seat_z = -0.44                               # 03's raised seat face (2026-10-16, unchanged)
cap_top_z_r1 = 92.2                          # 05 cap top before R2 (tube top 91 + 1.2 cap sheet)
body_raise = round(seat_z + ceramic_stack_real - cap_top_z_r1, 3)       # 2.66 -> cap top 94.86 = ceramic top

# ── Glass slots (4 of them, from the top edge) ─────────────────────
slot_width = 10.5
slot_depth = 23.5
gaps = [46.25, 46.25, 46.25, 108.68]
circumference = math.pi * outer_diameter
scale_factor = circumference / (sum(gaps) + 4 * slot_width)

slot_positions = []
current_arc_position = 0
for i in range(4):
    center_arc = current_arc_position + (slot_width * scale_factor) / 2
    angle = (center_arc / circumference) * 360
    slot_positions.append(angle)
    current_arc_position += (slot_width + gaps[i]) * scale_factor
# slot_positions ≈ [6.54, 77.19, 147.84, 218.50] deg
slot_arc_half_deg = (slot_width * scale_factor / 2 / circumference * 360)  # ≈ 6.53 deg

# ── Tube walls (twin-wall chamber) ─────────────────────────────────
# 2026-11-08 (Matt): 24.6 -> 20.6 so a glass terp slurper (31.0 mm bowl-to-joint gap) straddles the top cap ring
# (33.8 measured on the print -> ~29.8). Every radius at or outside the inner tube moves in 4.0; thicknesses do not.
# 2026-11-12 (Matt): 20.6 -> 14.6 and the air gap 4.4 -> 3.0 and the top cap lip 1.5 -> 0.5, for his smallest slurper
# (21 mm bowl-to-bend): ring ceramic edge -> top cap edge 28.4 -> 20.0. NOT a uniform shift: inner tube in 6.0,
# outer tube in 7.4, top cap edge in 8.4.
insulation_gap = 14.6
housing_inner_r = ceramic_outer_r + insulation_gap      # 60.85  -> inner tube ID 121.7 (133.7 on 2026-11-08, 141.7 before)
housing_outer_r = housing_inner_r + inner_sheet_thickness  # 61.65 -> inner tube OD 123.3 (135.3 on 2026-11-08)
air_gap = 3.0                                           # REAL gap, inner tube OD -> outer tube ID (4.4 before 2026-11-12;
                                                        # until then this read 4 and was added to the inner tube ID + 1.2)
mesh_inner_r = housing_outer_r + air_gap                # 64.65 -> outer tube ID 129.3 (144.1 on 2026-11-08)
mesh_outer_r = mesh_inner_r + sheet_metal_thickness     # 65.85  -> outer tube OD 131.7 (146.5 on 2026-11-08)
perf_mid_r = (mesh_inner_r + mesh_outer_r) / 2          # 65.25
# Top cap lip past the outer tube OD (2026-11-12: 1.5 -> 0.5). 05's plate edge has always been 0.1 inside that line.
# The bottom cap 04 and lid top disk 08 keep their 1.2 skirts OUTSIDE the outer tube (they carry the bottom and upper
# lid bolt rings), and a 1.2 sheet + clearance cannot fit in 0.5, so they stay 1.5 past the outer tube.
top_cap_lip = 0.5
top_cap_edge_r = mesh_outer_r + top_cap_lip - 0.1       # 66.25 -> 05 ring Ø132.5, 20.0 from the ceramic OD
skirt_cap_lip = 1.5
vent_r = air_gap / 2                                    # 05 + 09 vents: Ø3.0 = the air gap (Ø3.5 before 2026-11-12, did not fit 3.0)
vent_ring_r = housing_outer_r + air_gap / 2             # 63.15, centre of the air gap
wire_hole_r = 53.5                                      # 03 / 04 lead + TC holes (r 58 before 2026-11-12: now inside 03's bolt wall)
lead_hole_angles = (160.0, 170.0)                       # heater lead holes: 160 / 170 since the 5-bolt rings (2026-11-12 later; 185 / 195
                                                        # clashed with the 185.5 bolt), 180 / 190 before 2026-11-12
seat_step_r = 47.25                                     # 03 riser = the centering wall line (52 before 2026-11-12)
leg_r = housing_inner_r - 6.85                          # 54.0 leg circle (Ø108; r 60 on 2026-11-08, r 64 before)

# ── Z reference levels ─────────────────────────────────────────────
lip_top_z = -disk_thickness                             # -5.5  ceramic seat face (held)
lip_z = lip_top_z - inner_sheet_thickness                # -6.3  (was -6.7 at 1.2)
# 2026-08-14: REVERTED to the original -31.7 / 122.7. On 2026-08-13 this was changed to
# -43.7 / 134.7 on the false belief that the DXF flats said 134.7 and disagreed with the
# STEP. They never did — 134.7 was a bounding box that included the drawing's title text.
# The DXFs state it themselves: "Flat: 452.7 x 122.7 mm" and "Flat: 485.4 x 122.7 mm".
# 122.7 is correct and always was, and it is what the fab shop built.
housing_bottom_z = -(disk_thickness + sheet_metal_thickness) - 25   # -31.7 (held, independent of the ring lip)
housing_top_z = cylinder_height + body_raise            # 93.66 tube tops (91 before 2026-11-08 R2)
mesh_height = housing_top_z - housing_bottom_z          # 125.36 (outer tube height; 122.7 before 2026-11-08 R2)

# ── Perforations on the outer mesh tube (Ø4 @ 6 mm) ────────────────
perf_hole_r = 2                  # Ø4 holes
perf_spacing = 6                 # 6 mm pitch
perf_n_ang = int((2 * np.pi * perf_mid_r) / perf_spacing)   # 76 per row (80 before 2026-11-08)
perf_n_z = int((mesh_height - 10) / perf_spacing)           # ≈ 18 rows
perf_holes = []
for zi in range(perf_n_z):
    z = housing_bottom_z + 5 + zi * perf_spacing
    offset = (perf_spacing / 2) if (zi % 2) else 0          # stagger alt rows by 3 mm
    for ai in range(perf_n_ang):
        ang = (ai / perf_n_ang) * 360 + np.degrees(offset / perf_mid_r)
        perf_holes.append((ang, z))

# ── M6 clamp-bolt rings (Ø6.6 radial holes through BOTH walls) ─────
ring_screw_hole_r = 3.3                                  # M6 clearance, Ø6.6
# 2026-11-12 (Matt, 4:50 AM): 5 bolts per ring, 72 deg apart, centred between the 4 glass slots (6.54/77.19/147.84/218.50),
# every bolt >= 33 deg from a slot. Was 6 per ring at 52.4 + n*60 (52.4, 112.4, 172.4, 232.4, 292.4, 352.4).
ring_screw_angles = [41.5 + 72 * k for k in range(5)]   # 41.5, 113.5, 185.5, 257.5, 329.5
# (angle_list, z) for each ring:
ring_screw_sets = [
    (ring_screw_angles,  59.0 + body_raise),    # top spacer ring (61.66; 59.0 before R2, it moves up with the cap)
    (ring_screw_angles, -24.0),    # bottom ring (also clamps the bottom cap lip)
    (ring_screw_angles,   2.15),   # seat / support-ring flange
]

# ── Heater groove on the INNER housing (helical channel) ───────────
groove_start_height = 66.5
groove_end_height = 15.5
num_wraps = 30
groove_depth = 1.0
groove_width = 1.2

# ── Functional through-holes in the inner housing / bottom ─────────
slot_2_end_angle = slot_positions[2] + (slot_width * scale_factor / 2 / circumference * 360)
groove_seam_angle = slot_2_end_angle + (gaps[2] * scale_factor / 2 / circumference * 360)
slot_3_end_angle = slot_positions[3] + (slot_width * scale_factor / 2 / circumference * 360)
hole_position_angle = slot_3_end_angle + (108.68 * (2/3) / circumference * 360)
hole_diameter = 6.4
hole_bottom_height = 5
hole_center_height = hole_bottom_height + hole_diameter / 2  # 8.2
air_gap_mid_r = housing_outer_r + air_gap / 2               # 63.15 (old generator only)
wire_hole_angle = groove_seam_angle
wire_hole_diameter = 8
wire_top_z = groove_start_height      # 66.5
wire_bot_z = groove_end_height        # 15.5
tc_cable_hole_angle = hole_position_angle
tc_cable_hole_z = hole_center_height  # 8.2

# ── Leg / standoff bolt holes (3) in the bottom region ─────────────
leg_hole_r = leg_r                    # 54.0 (the package value, build_current_package.py)
bolt_hole_size = 6.6                  # Ø6.6 (M6 clearance; the bolt rings)
# 2026-11-12 (Matt, 5:19 AM: "smaller screws, everything can be adjusted and thought out for perfection"): legs back to
# EVEN 120 deg, M5 leg screws. 3 legs on 120 deg vs 5 bolts on 72 deg: the best a leg can be from its nearest bolt is
# 12 deg (legs at 41.5 + 12 + 24n). Of the two such patterns, 5.5 / 125.5 / 245.5 is the one far from the wire holes
# (34.5 deg from the 160 lead, 69.5 from the 315 TC; 29.5 / 149.5 / 269.5 puts a foot 10.5 deg from the 160 lead).
# Two legs are 12 deg from a bolt (5.5: 36 from both), which at r 54 needs the smaller M5 head (Ø8.5) next to an M6 nut.
# Was 77.5 / 221.5 / 293.5 (uneven, M6) earlier on 2026-11-12, 40 / 160 / 280 before.
leg_angles = [5.5, 125.5, 245.5]
leg_screw = "M5 x 40 socket head cap screw ISO 4762, A2 stainless, + M5 washer + M5 nut"
leg_hole_d = 5.5                      # M5 clearance (ISO 273 medium) in 03, 04, 14 and the feet (Ø6.6 for M6 before)
tray_drop = 1.2                       # 14 tray 1.2 lower than the Sept 9 solid, so the 25.0 feet fit exactly between the
                                      # tray top (-57.9) and the 04 floor underside (-32.9); they were 1.2 into the 04 floor

# ── Bottom cap (02) ────────────────────────────────────────────────
bottom_cap_lip_height = 16
bottom_cap_outer_r = mesh_outer_r + skirt_cap_lip   # 67.35 -> Ø134.7 (149.5 on 2026-11-08, 157.5 before)
bottom_cap_z = housing_bottom_z - sheet_metal_thickness   # -32.9 (underside of disk top face at +1.2)
# bottom-cap drilled holes (angle, radius position, hole radius):
bottom_cap_holes = [
    (wire_hole_angle,       air_gap_mid_r, 4),
    (wire_hole_angle + 5,   air_gap_mid_r, 4),
    (tc_cable_hole_angle,   air_gap_mid_r, 3),
    *[(a, leg_hole_r, leg_hole_d / 2) for a in leg_angles],
]

# ── Cap shell (04a) ────────────────────────────────────────────────
cap_outer_r = mesh_outer_r + skirt_cap_lip   # 67.35 (04 / 08 skirts)
cap_inner_r = ceramic_inner_r               # 40.75
ceramic_grab_lip = 3
CAP_BOLT_Z = 59 + body_raise
CAP_BOLT_ANGLES = list(ring_screw_angles)
CAP_TAB_HALF_DEG = np.degrees(6.0 / cap_outer_r)    # ~12 mm-wide fingers
CAP_TAB_BOT = 55
CAP_BOLT_HOLE_R = 1.8                         # bolt-clearance bored in each finger (radial)

# hinge (placeholder) on the lid bolt at 257.5 deg since the 5-bolt rings (2026-11-12): the back bolt nearest the old
# 292.4 (the back, opposite the handle); 292.4 before
HINGE_ANGLE_DEG = 257.5
HINGE_PIVOT_R = 81.5 - (24.6 - insulation_gap) - (4.4 - air_gap)   # 70.1 (77.5 on 2026-11-08, 81.5 before): moves with the outer tube
HINGE_PIVOT_Z = 97 + body_raise
HINGE_T_OFF = 14
HINGE_KN_LEN = 25/3                           # ≈ 8.333 each knuckle
HINGE_BARREL_OUTER_R = 4                       # Ø8 barrels
HINGE_BARREL_BORE_R = 2.6                       # Ø5.2 bore for the Ø5 pin
HINGE_FINGER_HALF_DEG = np.degrees(13.0 / cap_outer_r)

# ── Hold-down ring (04b) — flat web + 3 hanging walls ──────────────
HD_WEB_TOP = housing_top_z - sheet_metal_thickness    # 89.8
HD_GRAB_LIP_DROP = 3.0       # bore lip, at ceramic_inner_r
HD_FLAP_DROP = 10.0          # ceramic-OD flaps, at ceramic_outer_r
HD_EDGE_WALL_DROP = 6.0      # chamber-edge wall, at housing_inner_r
HD_WEB_DROP = 2.0            # flat web thickness band

# ── Hinge pin (05) ─────────────────────────────────────────────────
HINGE_PIN_R = 2.5            # Ø5 rod
HINGE_PIN_LEN = 30

# ── Convenience: principal manufacturing dimensions (for the report)
PRINCIPAL_DIMS = {
    "Inner tube ID (mm)": round(2*housing_inner_r, 2),
    "Inner tube OD (mm)": round(2*housing_outer_r, 2),
    "Outer tube ID (mm)": round(2*mesh_inner_r, 2),
    "Outer tube OD (mm)": round(2*mesh_outer_r, 2),
    "Outer tube height (mm)": round(mesh_height, 2),
    "Body raise above the seat, R2 (mm)": body_raise,
    "Ceramic stack, seat to cap top (mm)": ceramic_stack_real,
    "Sheet thickness outer (mm)": sheet_metal_thickness,
    "Sheet thickness inner (mm)": inner_sheet_thickness,
    "Glass slot W x D (mm)": f"{slot_width} x {slot_depth}",
    "Slot centers (deg)": [round(a, 2) for a in slot_positions],
    "Perf hole dia (mm)": 2*perf_hole_r,
    "Perf pitch (mm)": perf_spacing,
    "M6 hole dia (mm)": round(2*ring_screw_hole_r, 2),
    "M6 ring z-levels (mm)": [z for _, z in ring_screw_sets],
    "M6 ring angles (deg)": [round(a, 1) for a in ring_screw_angles],
    "Bottom cap blank dia (mm)": round(2*bottom_cap_outer_r, 2),
    "Bottom cap lip height (mm)": bottom_cap_lip_height,
    "Top cap 05 ring OD (mm)": round(2*top_cap_edge_r, 2),
    "Ring width ceramic OD to top cap edge (mm)": round(top_cap_edge_r - ceramic_outer_r, 2),
    "Bottom cap 04 / lid disk 08 OD (mm)": round(2*cap_outer_r, 2),
    "Hinge barrel dia (mm)": 2*HINGE_BARREL_OUTER_R,
    "Hinge pin dia x len (mm)": f"{2*HINGE_PIN_R} x {HINGE_PIN_LEN}",
}

if __name__ == "__main__":
    import json
    print(json.dumps({k: (v if not isinstance(v, list) else v) for k, v in PRINCIPAL_DIMS.items()}, indent=2, default=str))
