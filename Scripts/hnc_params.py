"""
Heat-N-Clean Glass Oven — SHARED PARAMETERS (single source of truth for STEP build)

Every constant and derived position here is copied VERBATIM from the trimesh
generator (Scripts/export_all_parts.py) so the analytic STEP solids match the
STLs the fab shops already have. Do NOT change a number without changing it in
export_all_parts.py too.

Units: millimetres. Origin: chamber axis = Z. z=0 is the ceramic-disk seat
reference used by the generator (housing_top_z = 91 is the chamber rim).
"""
import math
import numpy as np

# ── Sheet / material ───────────────────────────────────────────────
sheet_metal_thickness = 1.2          # 304SS, 1.2 mm everywhere unless noted

# ── Ceramic reference dims (drive the metal interfaces) ────────────
cylinder_height = 91
disk_thickness = 5.5
disk_body_h = 4.5
disk_lip_h = 1.0
outer_diameter = 92.5
inner_diameter = 81.5
ceramic_outer_r = outer_diameter / 2          # 46.25
ceramic_inner_r = inner_diameter / 2          # 40.75

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
insulation_gap = 24.6
housing_inner_r = ceramic_outer_r + insulation_gap      # 70.85  -> inner tube ID 141.7
housing_outer_r = housing_inner_r + sheet_metal_thickness  # 72.05 -> inner tube OD 144.1
air_gap = 4
mesh_inner_r = housing_outer_r + air_gap                # 76.05  -> outer tube ID 152.1
mesh_outer_r = mesh_inner_r + sheet_metal_thickness     # 77.25  -> outer tube OD 154.5
perf_mid_r = (mesh_inner_r + mesh_outer_r) / 2          # 76.65

# ── Z reference levels ─────────────────────────────────────────────
lip_z = -(disk_thickness + sheet_metal_thickness)       # -6.7
# 2026-08-14: REVERTED to the original -31.7 / 122.7. On 2026-08-13 this was changed to
# -43.7 / 134.7 on the false belief that the DXF flats said 134.7 and disagreed with the
# STEP. They never did — 134.7 was a bounding box that included the drawing's title text.
# The DXFs state it themselves: "Flat: 452.7 x 122.7 mm" and "Flat: 485.4 x 122.7 mm".
# 122.7 is correct and always was, and it is what Tianrun built.
housing_bottom_z = lip_z - 25                           # -31.7
housing_top_z = cylinder_height                         # 91
mesh_height = housing_top_z - housing_bottom_z          # 122.7  (outer tube height)

# ── Perforations on the outer mesh tube (Ø4 @ 6 mm) ────────────────
perf_hole_r = 2                  # Ø4 holes
perf_spacing = 6                 # 6 mm pitch
perf_n_ang = int((2 * np.pi * perf_mid_r) / perf_spacing)   # ≈ 80 per row
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
ring_screw_angles = [k * 60 + 52.4 for k in range(6)]    # 52.4, 112.4, 172.4, 232.4, 292.4, 352.4
# (angle_list, z) for each ring:
ring_screw_sets = [
    (ring_screw_angles,  59.0),    # top spacer ring
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
air_gap_mid_r = housing_outer_r + air_gap / 2               # 74.05
wire_hole_angle = groove_seam_angle
wire_hole_diameter = 8
wire_top_z = groove_start_height      # 66.5
wire_bot_z = groove_end_height        # 15.5
tc_cable_hole_angle = hole_position_angle
tc_cable_hole_z = hole_center_height  # 8.2

# ── Leg / standoff bolt holes (3) in the bottom region ─────────────
leg_hole_r = housing_inner_r - 5      # 65.85 (radius position)
bolt_hole_size = 6.6                  # Ø6.6
leg_angles = [40, 160, 280]

# ── Bottom cap (02) ────────────────────────────────────────────────
bottom_cap_lip_height = 16
bottom_cap_outer_r = mesh_outer_r + 1.5     # 78.75 -> Ø157.5 blank
bottom_cap_z = housing_bottom_z - sheet_metal_thickness   # -32.9 (underside of disk top face at +1.2)
# bottom-cap drilled holes (angle, radius position, hole radius):
bottom_cap_holes = [
    (wire_hole_angle,       air_gap_mid_r, 4),
    (wire_hole_angle + 5,   air_gap_mid_r, 4),
    (tc_cable_hole_angle,   air_gap_mid_r, 3),
    (40,  leg_hole_r, bolt_hole_size),
    (160, leg_hole_r, bolt_hole_size),
    (280, leg_hole_r, bolt_hole_size),
]

# ── Cap shell (04a) ────────────────────────────────────────────────
cap_outer_r = mesh_outer_r + 1.5            # 78.75
cap_inner_r = ceramic_inner_r               # 40.75
ceramic_grab_lip = 3
CAP_BOLT_Z = 59
CAP_BOLT_ANGLES = [52.4 + k*60 for k in range(6)]
CAP_TAB_HALF_DEG = np.degrees(6.0 / cap_outer_r)    # ~12 mm-wide fingers
CAP_TAB_BOT = 55
CAP_BOLT_HOLE_R = 1.8                         # bolt-clearance bored in each finger (radial)

# hinge (piano style) on the finger at 292.4 deg
HINGE_ANGLE_DEG = 292.4
HINGE_PIVOT_R = 81.5
HINGE_PIVOT_Z = 97
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
    "Sheet thickness (mm)": sheet_metal_thickness,
    "Glass slot W x D (mm)": f"{slot_width} x {slot_depth}",
    "Slot centers (deg)": [round(a, 2) for a in slot_positions],
    "Perf hole dia (mm)": 2*perf_hole_r,
    "Perf pitch (mm)": perf_spacing,
    "M6 hole dia (mm)": round(2*ring_screw_hole_r, 2),
    "M6 ring z-levels (mm)": [z for _, z in ring_screw_sets],
    "M6 ring angles (deg)": [round(a, 1) for a in ring_screw_angles],
    "Bottom cap blank dia (mm)": round(2*bottom_cap_outer_r, 2),
    "Bottom cap lip height (mm)": bottom_cap_lip_height,
    "Cap shell OD (mm)": round(2*cap_outer_r, 2),
    "Hinge barrel dia (mm)": 2*HINGE_BARREL_OUTER_R,
    "Hinge pin dia x len (mm)": f"{2*HINGE_PIN_R} x {HINGE_PIN_LEN}",
}

if __name__ == "__main__":
    import json
    print(json.dumps({k: (v if not isinstance(v, list) else v) for k, v in PRINCIPAL_DIMS.items()}, indent=2, default=str))
