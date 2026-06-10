"""
EXPORT ALL PARTS - Glass Heat Station
Builds all geometry programmatically and exports each part individually
as STL (binary) and GLB files.

Run from the Scripts/ directory:
    python export_all_parts.py
"""
import trimesh
import numpy as np
import math
import os
import sys
import shutil

# =============================================================================
# OUTPUT DIRECTORIES
# =============================================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
cad_exports_dir = os.path.join(project_dir, "CAD Exports")
output_base = os.path.join(cad_exports_dir, "Individual Parts")
stl_dir = os.path.join(output_base, "STL")
glb_dir = os.path.join(output_base, "GLB")

for d in [stl_dir, glb_dir]:
    os.makedirs(d, exist_ok=True)
    print(f"  Output dir: {d}")

print()

# =============================================================================
# CERAMIC DIMENSIONS (same across all views)
# =============================================================================
cylinder_height = 91
disk_thickness = 5.5
disk_body_h = 4.5       # body thickness (full OD portion)
disk_lip_h = 1.0        # lip thickness (reduced 76mm OD portion)
outer_diameter = 92.5
inner_diameter = 81.5

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

ceramic_outer_r = outer_diameter / 2
ceramic_inner_r = inner_diameter / 2

sheet_metal_thickness = 1.2
insulation_gap = 24.6
housing_inner_r = ceramic_outer_r + insulation_gap
housing_outer_r = housing_inner_r + sheet_metal_thickness

air_gap = 4
mesh_inner_r = housing_outer_r + air_gap
mesh_outer_r = mesh_inner_r + sheet_metal_thickness

perf_hole_r = 2
perf_spacing = 6

groove_start_height = 66.5
groove_end_height = 15.5
groove_span = groove_start_height - groove_end_height
num_wraps = 30
groove_depth = 1.0
groove_width = 1.2
pitch = groove_span / num_wraps

slot_2_end_angle = slot_positions[2] + (slot_width * scale_factor / 2 / circumference * 360)
gap_between_3_and_4 = gaps[2]
groove_seam_angle = slot_2_end_angle + (gap_between_3_and_4 * scale_factor / 2 / circumference * 360)

hole_diameter = 6.4
hole_bottom_height = 5
hole_center_height = hole_bottom_height + hole_diameter / 2
slot_3_end_angle = slot_positions[3] + (slot_width * scale_factor / 2 / circumference * 360)
hole_position_angle = slot_3_end_angle + (108.68 * (2/3) / circumference * 360)

lip_z = -(disk_thickness + sheet_metal_thickness)
ring_wall_top_z = hole_bottom_height - 2
housing_bottom_z = lip_z - 25
housing_top_z = cylinder_height

perf_mid_r = (mesh_inner_r + mesh_outer_r) / 2
perf_n_ang = int((2 * np.pi * perf_mid_r) / perf_spacing)
air_gap_mid_r = housing_outer_r + air_gap / 2

# Leg/bolt params
leg_hole_r = housing_inner_r - 5
bolt_hole_size = 6.6  # M6 clearance hole (6.6mm diameter)
leg_angles = [40, 160, 280]

# Wire/TC hole params
wire_hole_angle = groove_seam_angle
wire_hole_diameter = 8
wire_top_z = groove_start_height
wire_bot_z = groove_end_height
tc_cable_hole_z = hole_center_height
tc_cable_hole_angle = hole_position_angle

print("=" * 70)
print("EXPORT ALL PARTS - Glass Heat Station")
print("=" * 70)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def create_hollow_cylinder(inner_r, outer_r, height, sections=64):
    angles = np.linspace(0, 2*np.pi, sections, endpoint=False)
    vertices = []
    faces = []
    for z in [0, height]:
        for r in [inner_r, outer_r]:
            for angle in angles:
                vertices.append([r * np.cos(angle), r * np.sin(angle), z])
    n = sections
    for i in range(n):
        i_next = (i + 1) % n
        faces.append([i, i_next, n + i])
        faces.append([i_next, n + i_next, n + i])
        faces.append([2*n + i, 3*n + i, 2*n + i_next])
        faces.append([2*n + i_next, 3*n + i, 3*n + i_next])
        faces.append([n + i, 3*n + i, n + i_next])
        faces.append([n + i_next, 3*n + i, 3*n + i_next])
        faces.append([i, i_next, 2*n + i])
        faces.append([i_next, 2*n + i_next, 2*n + i])
    return trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))

def create_tube_along_path(points, radius, segments=8):
    vertices = []
    faces = []
    for i, point in enumerate(points):
        if i == 0:
            tangent = np.array(points[1]) - np.array(points[0])
        elif i == len(points) - 1:
            tangent = np.array(points[-1]) - np.array(points[-2])
        else:
            tangent = np.array(points[i+1]) - np.array(points[i-1])
        tangent = tangent / (np.linalg.norm(tangent) + 0.001)
        if abs(tangent[2]) < 0.9:
            up = np.array([0, 0, 1])
        else:
            up = np.array([1, 0, 0])
        right = np.cross(tangent, up)
        right = right / (np.linalg.norm(right) + 0.001)
        up = np.cross(right, tangent)
        for j in range(segments):
            theta = 2 * np.pi * j / segments
            offset = radius * (np.cos(theta) * right + np.sin(theta) * up)
            vertices.append(np.array(point) + offset)
    for i in range(len(points) - 1):
        for j in range(segments):
            v0 = i * segments + j
            v1 = i * segments + (j + 1) % segments
            v2 = (i + 1) * segments + j
            v3 = (i + 1) * segments + (j + 1) % segments
            faces.append([v0, v2, v1])
            faces.append([v1, v2, v3])
    m = trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    m.fix_normals()
    return m

# Colors
stainless_color = [195, 200, 205, 255]
stainless_dark = [175, 180, 185, 255]
ceramic_body_color = [255, 255, 255, 255]
ceramic_disk_color = [255, 255, 255, 255]
copper_color = [180, 120, 60, 255]
kanthal_color = [220, 100, 40, 255]

# =============================================================================
# SLOT/HOLE HELPER FUNCTIONS (for housing geometry)
# =============================================================================
housing_holes = [
    (wire_hole_angle, wire_top_z, wire_hole_diameter/2),
    (wire_hole_angle, wire_bot_z, wire_hole_diameter/2),
    (tc_cable_hole_angle, tc_cable_hole_z, 5),
]

def in_housing_hole(angle_deg, z):
    for h_ang, h_z, h_r in housing_holes:
        ang_diff = abs(angle_deg - h_ang)
        if ang_diff > 180: ang_diff = 360 - ang_diff
        arc_dist = ang_diff * (np.pi / 180) * housing_outer_r
        z_dist = abs(z - h_z)
        if np.sqrt(arc_dist**2 + z_dist**2) < h_r:
            return True
    return False

slot_arc_half_deg = (slot_width / 2) / ceramic_outer_r * (180 / np.pi)

_housing_slot_buffer_mm = 0.0   # match the ceramic core slot exactly (no extra width)
_housing_extra_deg = (_housing_slot_buffer_mm / housing_inner_r) * (180 / np.pi)
_housing_slot_half_deg = slot_arc_half_deg + _housing_extra_deg

def get_housing_z_offset(angle_deg):
    for slot_center in slot_positions:
        diff = abs(angle_deg - slot_center)
        if diff > 180: diff = 360 - diff
        if diff <= _housing_slot_half_deg:
            t = 1.0 - (diff / _housing_slot_half_deg)
            half_w = slot_width / 2
            straight_h = slot_depth - half_w
            return straight_h + half_w * np.sqrt(max(0, t * (2 - t)))
    return 0

def get_slot_z_offset(angle_deg):
    for slot_center in slot_positions:
        diff = abs(angle_deg - slot_center)
        if diff > 180: diff = 360 - diff
        if diff <= slot_arc_half_deg:
            t = 1.0 - (diff / slot_arc_half_deg)
            half_w = slot_width / 2
            straight_h = slot_depth - half_w
            return straight_h + half_w * np.sqrt(max(0, t * (2 - t)))
    return 0

def in_cap_slot(angle_deg):
    """True when angle is inside a ceramic slot opening."""
    for slot_center in slot_positions:
        diff = abs(angle_deg - slot_center)
        if diff > 180: diff = 360 - diff
        if diff <= slot_arc_half_deg:
            return True
    return False

def get_cap_flat_z_offset(angle_deg, r):
    """Cap top dips into the slot only on the outside of the ceramic — the
    ceramic top stays covered (flat) so the slot in the metal is flush with
    the ceramic outer wall, not extending in over the chamber."""
    if r <= ceramic_outer_r:
        return 0
    return get_slot_z_offset(angle_deg)

# Perforation hole positions
perf_holes = []
mesh_height = housing_top_z - housing_bottom_z
perf_n_z = int((mesh_height - 10) / perf_spacing)
for zi in range(perf_n_z):
    z = housing_bottom_z + 5 + zi * perf_spacing
    offset = (perf_spacing / 2) if (zi % 2) else 0
    for ai in range(perf_n_ang):
        ang = (ai / perf_n_ang) * 360 + np.degrees(offset / perf_mid_r)
        perf_holes.append((ang, z))

def in_perf(ang, z, holes, mid_r, hole_r):
    for h_ang, h_z in holes:
        ang_diff = abs(ang - h_ang)
        if ang_diff > 180: ang_diff = 360 - ang_diff
        arc = ang_diff * (np.pi / 180) * mid_r
        if np.sqrt(arc**2 + (z - h_z)**2) < hole_r:
            return True
    return False

_mesh_slot_buffer_mm = 0.0   # match the ceramic core slot exactly (no extra width)
_mesh_extra_deg = (_mesh_slot_buffer_mm / mesh_inner_r) * (180 / np.pi)
_mesh_slot_half_deg = slot_arc_half_deg + _mesh_extra_deg
_mesh_lip_clearance = 0.0    # outer slot same depth as the ceramic/inner slot (was +10mm)

def in_mesh_slot(angle_deg, z):
    half_w = slot_width / 2
    straight_h = slot_depth - half_w + _mesh_lip_clearance
    total_depth = slot_depth + _mesh_lip_clearance
    z_from_top = housing_top_z - z
    for slot_center in slot_positions:
        ang_diff = abs(angle_deg - slot_center)
        if ang_diff > 180: ang_diff = 360 - ang_diff
        if ang_diff <= _mesh_slot_half_deg:
            t = ang_diff / _mesh_slot_half_deg
            arc_dist_norm = t * half_w
            if z_from_top <= straight_h:
                return True
            elif z_from_top <= total_depth:
                z_from_arc = z_from_top - straight_h
                if arc_dist_norm**2 + z_from_arc**2 <= half_w**2:
                    return True
    return False

def in_bottom_hole(angle_deg, r):
    bottom_holes = [
        (wire_hole_angle, air_gap_mid_r, 4),
        (wire_hole_angle + 5, air_gap_mid_r, 4),
        (tc_cable_hole_angle, air_gap_mid_r, 3),
        (40, leg_hole_r, bolt_hole_size),
        (160, leg_hole_r, bolt_hole_size),
        (280, leg_hole_r, bolt_hole_size),
    ]
    for h_ang, h_r_pos, h_radius in bottom_holes:
        ang_diff = abs(angle_deg - h_ang)
        if ang_diff > 180: ang_diff = 360 - ang_diff
        arc_dist = ang_diff * (np.pi / 180) * h_r_pos
        r_dist = abs(r - h_r_pos)
        if np.sqrt(arc_dist**2 + r_dist**2) < h_radius:
            return True
    return False

# M6 screw rings that clamp the chamber together. REAL clearance holes cut through
# BOTH tube walls, lined up with the bolts in the assembly viewer:
#   top + bottom rings -> 8 screws each, hold the 2 spacer rings between the tubes
#   seat ring          -> 6 screws, come in from the outer chamber to hold the support ring
ring_screw_hole_r = 3.3                                # M6 clearance, 6.6 mm dia
# Clocked to 52.4° so NO bolt lands on a ceramic slot (slots at 6.5/77/148/218°, each ±6.5°).
# Old 30° clocking drove 3 of 6 bolts into slots. 52.4° clears every slot by ≥14° and every
# other hole (legs 40/160/280, wire 183, tc 315) by ≥10.6°. Matches viewer-chamber-assembled.html.
ring_screw_angles = [k * 60 + 52.4 for k in range(6)]  # ONE 6-bolt pattern for every ring
ring_screw_sets = [
    (ring_screw_angles,  59.0),    # top spacer ring
    (ring_screw_angles, -24.0),    # bottom: ONE ring fastens spacer + bottom cap together
    (ring_screw_angles,   2.15),   # support-ring (seat) flange
]

def in_ring_screw_hole(angle_deg, z, mid_r):
    for angs, h_z in ring_screw_sets:
        if abs(z - h_z) > ring_screw_hole_r:
            continue
        for h_ang in angs:
            ang_diff = abs(angle_deg - h_ang)
            if ang_diff > 180: ang_diff = 360 - ang_diff
            arc = ang_diff * (np.pi / 180) * mid_r
            if np.sqrt(arc**2 + (z - h_z)**2) < ring_screw_hole_r:
                return True
    return False

# The bottom cap fastens via the SAME bottom ring (z=-24) — one bolt passes through
# the cap lip, outer tube, ceramic spacer, and inner tube. No separate cap ring.

# =============================================================================
# PART 1A: BASE BODY - Inner housing with slots + holes
# =============================================================================
print("Building base body (inner housing)...")

housing_sections = 480
housing_z_bands = 160
housing_verts = []
housing_faces = []
housing_idx = {}

for ai in range(housing_sections):
    ang_deg = (ai / housing_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    z_off = get_housing_z_offset(ang_deg)
    for zi in range(housing_z_bands + 1):
        z = housing_bottom_z + (zi / housing_z_bands) * (housing_top_z - z_off - housing_bottom_z)
        for ri, r in enumerate([housing_inner_r, housing_outer_r]):
            housing_idx[(ai, zi, ri)] = len(housing_verts)
            housing_verts.append([r * cos_a, r * sin_a, z])

for ai in range(housing_sections):
    nai = (ai + 1) % housing_sections
    mid_ang = ((ai + 0.5) / housing_sections) * 360
    for zi in range(housing_z_bands):
        mid_z = housing_bottom_z + ((zi + 0.5) / housing_z_bands) * (housing_top_z - housing_bottom_z)
        if in_housing_hole(mid_ang, mid_z): continue
        if in_ring_screw_hole(mid_ang, mid_z, housing_outer_r): continue
        housing_faces.append([housing_idx[(ai, zi, 0)], housing_idx[(ai, zi+1, 0)], housing_idx[(nai, zi, 0)]])
        housing_faces.append([housing_idx[(nai, zi, 0)], housing_idx[(ai, zi+1, 0)], housing_idx[(nai, zi+1, 0)]])
        housing_faces.append([housing_idx[(ai, zi, 1)], housing_idx[(nai, zi, 1)], housing_idx[(ai, zi+1, 1)]])
        housing_faces.append([housing_idx[(nai, zi, 1)], housing_idx[(nai, zi+1, 1)], housing_idx[(ai, zi+1, 1)]])

for ai in range(housing_sections):
    nai = (ai + 1) % housing_sections
    housing_faces.append([housing_idx[(ai, 0, 0)], housing_idx[(nai, 0, 0)], housing_idx[(ai, 0, 1)]])
    housing_faces.append([housing_idx[(nai, 0, 0)], housing_idx[(nai, 0, 1)], housing_idx[(ai, 0, 1)]])
    housing_faces.append([housing_idx[(ai, housing_z_bands, 0)], housing_idx[(ai, housing_z_bands, 1)], housing_idx[(nai, housing_z_bands, 0)]])
    housing_faces.append([housing_idx[(nai, housing_z_bands, 0)], housing_idx[(ai, housing_z_bands, 1)], housing_idx[(nai, housing_z_bands, 1)]])

inner_housing = trimesh.Trimesh(vertices=np.array(housing_verts), faces=np.array(housing_faces))
inner_housing.fix_normals()
inner_housing.visual.face_colors = stainless_color

# =============================================================================
# PART 1B: BASE BODY - Outer perforated mesh (high resolution for rounder holes)
# =============================================================================
print("Building outer perforated mesh...")

mesh_verts = []
mesh_faces = []
mesh_idx = {}
mesh_sections = 720  # High resolution for round holes
mesh_z_bands = 240

for ai in range(mesh_sections):
    ang_deg = (ai / mesh_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    for zi in range(mesh_z_bands + 1):
        z = housing_bottom_z + (zi / mesh_z_bands) * mesh_height
        for ri, r in enumerate([mesh_inner_r, mesh_outer_r]):
            mesh_idx[(ai, zi, ri)] = len(mesh_verts)
            mesh_verts.append([r * cos_a, r * sin_a, z])

for ai in range(mesh_sections):
    nai = (ai + 1) % mesh_sections
    mid_ang = ((ai + 0.5) / mesh_sections) * 360
    for zi in range(mesh_z_bands):
        mid_z = housing_bottom_z + ((zi + 0.5) / mesh_z_bands) * mesh_height
        if in_mesh_slot(mid_ang, mid_z): continue
        if in_perf(mid_ang, mid_z, perf_holes, perf_mid_r, perf_hole_r): continue
        if in_ring_screw_hole(mid_ang, mid_z, perf_mid_r): continue
        mesh_faces.append([mesh_idx[(ai, zi, 0)], mesh_idx[(ai, zi+1, 0)], mesh_idx[(nai, zi, 0)]])
        mesh_faces.append([mesh_idx[(nai, zi, 0)], mesh_idx[(ai, zi+1, 0)], mesh_idx[(nai, zi+1, 0)]])
        mesh_faces.append([mesh_idx[(ai, zi, 1)], mesh_idx[(nai, zi, 1)], mesh_idx[(ai, zi+1, 1)]])
        mesh_faces.append([mesh_idx[(nai, zi, 1)], mesh_idx[(nai, zi+1, 1)], mesh_idx[(ai, zi+1, 1)]])

for ai in range(mesh_sections):
    nai = (ai + 1) % mesh_sections
    mid_ang = ((ai + 0.5) / mesh_sections) * 360
    mesh_faces.append([mesh_idx[(ai, 0, 0)], mesh_idx[(nai, 0, 0)], mesh_idx[(ai, 0, 1)]])
    mesh_faces.append([mesh_idx[(nai, 0, 0)], mesh_idx[(nai, 0, 1)], mesh_idx[(ai, 0, 1)]])
    if not in_mesh_slot(mid_ang, housing_top_z - 0.5):
        mesh_faces.append([mesh_idx[(ai, mesh_z_bands, 0)], mesh_idx[(ai, mesh_z_bands, 1)], mesh_idx[(nai, mesh_z_bands, 0)]])
        mesh_faces.append([mesh_idx[(nai, mesh_z_bands, 0)], mesh_idx[(ai, mesh_z_bands, 1)], mesh_idx[(nai, mesh_z_bands, 1)]])

outer_mesh = trimesh.Trimesh(vertices=np.array(mesh_verts), faces=np.array(mesh_faces))
outer_mesh.fix_normals()
outer_mesh.visual.face_colors = stainless_dark

# =============================================================================
# PART 1C: SUPPORT RING (shelf + retaining wall)
# =============================================================================
print("Building support ring...")

l_ring_inner_r = ceramic_outer_r - 10
l_ring_parts = []

horizontal_lip = create_hollow_cylinder(l_ring_inner_r, housing_inner_r, sheet_metal_thickness)
horizontal_lip.apply_translation([0, 0, lip_z])
l_ring_parts.append(horizontal_lip)

wall_bottom = lip_z + sheet_metal_thickness
wall_height = ring_wall_top_z - wall_bottom
vertical_wall = create_hollow_cylinder(ceramic_outer_r, ceramic_outer_r + sheet_metal_thickness, wall_height)
vertical_wall.apply_translation([0, 0, wall_bottom])
l_ring_parts.append(vertical_wall)

l_ring = trimesh.util.concatenate(l_ring_parts)
l_ring.visual.face_colors = stainless_color

# =============================================================================
# PART 1D: BOTTOM DISK with wire/bolt holes
# =============================================================================
print("Building bottom disk...")

bottom_disk_sections = 120
bottom_disk_radial = 25
bd_verts = []
bd_faces = []
bd_idx = {}

for ai in range(bottom_disk_sections):
    ang_deg = (ai / bottom_disk_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    for ri in range(bottom_disk_radial + 1):
        r = (ri / bottom_disk_radial) * mesh_outer_r
        for zi, z in enumerate([housing_bottom_z, housing_bottom_z + sheet_metal_thickness]):
            bd_idx[(ai, ri, zi)] = len(bd_verts)
            if r < 0.01:
                bd_verts.append([0, 0, z])
            else:
                bd_verts.append([r * cos_a, r * sin_a, z])

for ai in range(bottom_disk_sections):
    nai = (ai + 1) % bottom_disk_sections
    mid_ang = ((ai + 0.5) / bottom_disk_sections) * 360
    for ri in range(bottom_disk_radial):
        mid_r = ((ri + 0.5) / bottom_disk_radial) * mesh_outer_r
        if in_bottom_hole(mid_ang, mid_r): continue
        bd_faces.append([bd_idx[(ai, ri, 1)], bd_idx[(ai, ri+1, 1)], bd_idx[(nai, ri, 1)]])
        bd_faces.append([bd_idx[(nai, ri, 1)], bd_idx[(ai, ri+1, 1)], bd_idx[(nai, ri+1, 1)]])
        bd_faces.append([bd_idx[(ai, ri, 0)], bd_idx[(nai, ri, 0)], bd_idx[(ai, ri+1, 0)]])
        bd_faces.append([bd_idx[(nai, ri, 0)], bd_idx[(nai, ri+1, 0)], bd_idx[(ai, ri+1, 0)]])

for ai in range(bottom_disk_sections):
    nai = (ai + 1) % bottom_disk_sections
    ri = bottom_disk_radial
    bd_faces.append([bd_idx[(ai, ri, 0)], bd_idx[(ai, ri, 1)], bd_idx[(nai, ri, 0)]])
    bd_faces.append([bd_idx[(nai, ri, 0)], bd_idx[(ai, ri, 1)], bd_idx[(nai, ri, 1)]])

bottom_disk = trimesh.Trimesh(vertices=np.array(bd_verts), faces=np.array(bd_faces))
bottom_disk.fix_normals()
bottom_disk.visual.face_colors = stainless_color

# =============================================================================
# STANDOFF TABS (vent chamber spacers)
# =============================================================================
print("Creating vent chamber support fins at slot edges and corners...")

fin_thickness = sheet_metal_thickness
fin_depth = air_gap
fin_r = (housing_outer_r + mesh_inner_r) / 2

fin_angles = []
for slot_center in slot_positions:
    fin_angles.append(slot_center - slot_arc_half_deg)
    fin_angles.append(slot_center + slot_arc_half_deg)

for i in range(4):
    next_i = (i + 1) % 4
    mid = (slot_positions[i] + slot_positions[next_i]) / 2
    if slot_positions[next_i] < slot_positions[i]:
        mid = (slot_positions[i] + slot_positions[next_i] + 360) / 2
        if mid >= 360: mid -= 360
    skip = False
    for h_ang in [wire_hole_angle, wire_hole_angle + 5, tc_cable_hole_angle]:
        diff = abs(mid - h_ang)
        if diff > 180: diff = 360 - diff
        if diff < 6:
            skip = True
            break
    if not skip:
        fin_angles.append(mid)

fin_bottom_z = housing_bottom_z + 5
fin_top_z = housing_top_z - slot_depth - 2
fin_full_height = fin_top_z - fin_bottom_z
fin_center_z = (fin_bottom_z + fin_top_z) / 2

standoff_tabs = []
for ang_deg in fin_angles:
    ang_rad = np.radians(ang_deg)
    fin = trimesh.creation.box(extents=[fin_depth, fin_thickness, fin_full_height])
    fin.apply_translation([fin_r, 0, fin_center_z])
    fin.apply_transform(trimesh.transformations.rotation_matrix(ang_rad, [0, 0, 1]))
    fin.visual.face_colors = stainless_color
    standoff_tabs.append(fin)

print(f"  {len(standoff_tabs)} fins at slot edges + midpoints")

# =============================================================================
# COMBINE BASE BODY = housing + mesh + ring + standoffs (NO bottom disk)
# =============================================================================
print("Combining base body (bottom cap is separate)...")

base_body_full = trimesh.util.concatenate([inner_housing, outer_mesh, l_ring] + standoff_tabs)
base_body_full.visual.face_colors = stainless_color
base_body = base_body_full

# =============================================================================
# BOTTOM CAP (separate piece, screws on like top cap)
# =============================================================================
print("Building bottom cap with screw tabs...")

# Calculate flange positions dynamically:
# - 3 flanges centered in the 3 smaller gaps between slots
# - 2 flanges in the large gap (one each side of hinge)
slot_arc_half_deg = (slot_width * scale_factor / 2 / circumference * 360)

bottom_cap_tab_angles = []
# First 3 flanges: centered between slots 0-1, 1-2, 2-3
for i in range(3):
    slot_end = slot_positions[i] + slot_arc_half_deg
    next_slot_start = slot_positions[i+1] - slot_arc_half_deg
    mid_angle = (slot_end + next_slot_start) / 2
    bottom_cap_tab_angles.append(mid_angle)

# Last 2 flanges: in the large gap, centered between outer slots and hinge
slot_3_end = slot_positions[3] + slot_arc_half_deg
slot_0_start = slot_positions[0] - slot_arc_half_deg + 360  # wrap around
large_gap_arc_deg = gaps[3] * scale_factor / circumference * 360
hinge_center = slot_3_end + large_gap_arc_deg / 2
if hinge_center >= 360:
    hinge_center -= 360

# Flange between slot 3 end and hinge
flange_4 = (slot_3_end + hinge_center) / 2
if flange_4 >= 360:
    flange_4 -= 360
bottom_cap_tab_angles.append(flange_4)

# Flange between hinge and slot 0 start
flange_5 = (hinge_center + slot_0_start) / 2
if flange_5 >= 360:
    flange_5 -= 360
bottom_cap_tab_angles.append(flange_5)

bottom_cap_lip_height = 16   # tall enough for the M6 consolidated ring at z=-24 to sit inside the lip
bottom_cap_outer_r = mesh_outer_r + 1.5
bottom_cap_z = housing_bottom_z - sheet_metal_thickness

# Create solid disk using cylinder, then cut round holes with boolean difference
bottom_cap_disk = trimesh.creation.cylinder(
    radius=bottom_cap_outer_r,
    height=sheet_metal_thickness,
    sections=64
)
bottom_cap_disk.apply_translation([0, 0, bottom_cap_z + sheet_metal_thickness/2])

# Define holes: (angle_deg, radius_position, hole_radius)
bottom_cap_holes = [
    (wire_hole_angle, air_gap_mid_r, 4),
    (wire_hole_angle + 5, air_gap_mid_r, 4),
    (tc_cable_hole_angle, air_gap_mid_r, 3),
    (40, leg_hole_r, bolt_hole_size),
    (160, leg_hole_r, bolt_hole_size),
    (280, leg_hole_r, bolt_hole_size),
]

# Cut each hole using boolean difference
for h_ang, h_r_pos, h_radius in bottom_cap_holes:
    ang_rad = np.radians(h_ang)
    hole_x = h_r_pos * np.cos(ang_rad)
    hole_y = h_r_pos * np.sin(ang_rad)
    hole_cyl = trimesh.creation.cylinder(radius=h_radius, height=sheet_metal_thickness + 2, sections=32)
    hole_cyl.apply_translation([hole_x, hole_y, bottom_cap_z + sheet_metal_thickness/2])
    bottom_cap_disk = bottom_cap_disk.difference(hole_cyl)

# Outer lip going UP — wraps the outer tube; radial M4 screws fasten through it
bc_lip_sections = 360
bc_lip_z_bands = 20
bc_lip_verts = []
bc_lip_faces = []
bc_lip_idx = {}

for ai in range(bc_lip_sections):
    ang_deg = (ai / bc_lip_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    for zi in range(bc_lip_z_bands + 1):
        z = bottom_cap_z + sheet_metal_thickness + (zi / bc_lip_z_bands) * bottom_cap_lip_height
        for ri, r in enumerate([bottom_cap_outer_r - sheet_metal_thickness, bottom_cap_outer_r]):
            bc_lip_idx[(ai, zi, ri)] = len(bc_lip_verts)
            bc_lip_verts.append([r * cos_a, r * sin_a, z])

for ai in range(bc_lip_sections):
    nai = (ai + 1) % bc_lip_sections
    mid_ang = ((ai + 0.5) / bc_lip_sections) * 360
    for zi in range(bc_lip_z_bands):
        mid_z = bottom_cap_z + sheet_metal_thickness + ((zi + 0.5) / bc_lip_z_bands) * bottom_cap_lip_height
        # cut the SAME consolidated bottom ring (z=-24) through the lip — the bolt that
        # holds the ceramic spacer also passes through here and fastens the cap
        if in_ring_screw_hole(mid_ang, mid_z, bottom_cap_outer_r - sheet_metal_thickness/2): continue
        bc_lip_faces.append([bc_lip_idx[(ai, zi, 0)], bc_lip_idx[(ai, zi+1, 0)], bc_lip_idx[(nai, zi, 0)]])
        bc_lip_faces.append([bc_lip_idx[(nai, zi, 0)], bc_lip_idx[(ai, zi+1, 0)], bc_lip_idx[(nai, zi+1, 0)]])
        bc_lip_faces.append([bc_lip_idx[(ai, zi, 1)], bc_lip_idx[(nai, zi, 1)], bc_lip_idx[(ai, zi+1, 1)]])
        bc_lip_faces.append([bc_lip_idx[(nai, zi, 1)], bc_lip_idx[(nai, zi+1, 1)], bc_lip_idx[(ai, zi+1, 1)]])

bottom_cap_lip = trimesh.Trimesh(vertices=np.array(bc_lip_verts), faces=np.array(bc_lip_faces))
bottom_cap_lip.fix_normals()

# Bottom cap = disk + lip. It fastens via the SHARED bottom ring (z=-24): the same
# 6 M6 bolts pass through the cap lip, outer tube, ceramic spacer and inner tube.
# (Old floating vertical tabs + bosses removed — they didn't line up.)
bottom_cap = trimesh.util.concatenate([bottom_cap_disk, bottom_cap_lip])
bottom_cap.visual.face_colors = [220, 180, 140, 255]
print(f"  bottom cap: lip wraps outer tube, fastened by the shared bottom ring ({len(ring_screw_angles)} M6 at {[f'{a:.0f} deg' for a in ring_screw_angles]})")

# Add screw bosses to base body bottom edge
print("Adding screw bosses to base body bottom...")
bottom_screw_bosses = []
for ang_deg in bottom_cap_tab_angles:
    ang_rad = np.radians(ang_deg)
    boss_r = mesh_outer_r + 3
    boss_x = boss_r * np.cos(ang_rad)
    boss_y = boss_r * np.sin(ang_rad)
    boss_z = housing_bottom_z + bottom_cap_lip_height/2

    boss = trimesh.creation.cylinder(radius=5, height=bottom_cap_lip_height - 2, sections=16)
    boss.apply_translation([boss_x, boss_y, boss_z])
    boss.visual.face_colors = stainless_color
    bottom_screw_bosses.append(boss)

    thread_hole = trimesh.creation.cylinder(radius=2, height=bottom_cap_lip_height, sections=12)
    thread_hole.apply_translation([boss_x, boss_y, boss_z])
    thread_hole.visual.face_colors = [30, 30, 35, 255]
    bottom_screw_bosses.append(thread_hole)

base_body = trimesh.util.concatenate([base_body] + bottom_screw_bosses)
base_body.visual.face_colors = stainless_color

# =============================================================================
# PART 2: TOP CAP
# =============================================================================
print("Building top cap with perforations...")

cap_outer_r = mesh_outer_r + 1.5
cap_inner_r = ceramic_inner_r
ceramic_grab_lip = 3
cap_sections = 720  # High resolution for round perforations
cap_radial = 60

cap_vent_inner_r = housing_outer_r
cap_vent_outer_r = cap_outer_r
cap_vent_mid_r = (cap_vent_inner_r + cap_vent_outer_r) / 2

slot_buffer_deg = 4.0 / ceramic_outer_r * (180 / np.pi)  # 4mm buffer from slots
flange_buffer_deg = 4.0 / cap_outer_r * (180 / np.pi)  # 4mm buffer from flanges

def away_from_slots(angle_deg):
    for slot_center in slot_positions:
        diff = abs(angle_deg - slot_center)
        if diff > 180: diff = 360 - diff
        if diff < slot_arc_half_deg + slot_buffer_deg:
            return False
    return True

def away_from_flanges(angle_deg):
    for flange_ang in bottom_cap_tab_angles:
        diff = abs(angle_deg - flange_ang)
        if diff > 180: diff = 360 - diff
        if diff < flange_buffer_deg:
            return False
    return True

# Place maximum holes in each gap for best ventilation
cap_perf_holes = []

# Calculate how many radial rows fit in the vent area
cap_vent_width = cap_vent_outer_r - cap_vent_inner_r
cap_hole_spacing = perf_spacing * 0.8  # Tighter spacing for more holes
n_radial_rows = max(1, int(cap_vent_width / cap_hole_spacing))
cap_row_spacing = cap_vent_width / (n_radial_rows + 1)

for r_row in range(n_radial_rows):
    r_pos = cap_vent_inner_r + cap_row_spacing * (r_row + 1)
    offset = (cap_hole_spacing / 2) if (r_row % 2) else 0

    # Place holes in each gap - calculate max that fit
    for gap_idx in range(4):
        next_idx = (gap_idx + 1) % 4
        gap_start = slot_positions[gap_idx] + slot_arc_half_deg + slot_buffer_deg
        gap_end = slot_positions[next_idx] - slot_arc_half_deg - slot_buffer_deg
        if gap_end < gap_start:
            gap_end += 360

        # Calculate gap arc length and max holes that fit
        gap_arc_deg = gap_end - gap_start
        gap_arc_mm = gap_arc_deg * (np.pi / 180) * r_pos
        n_holes = max(1, int(gap_arc_mm / cap_hole_spacing))

        for hi in range(n_holes):
            ang = gap_start + (hi + 0.5) * (gap_end - gap_start) / n_holes + offset / cap_vent_mid_r
            if ang >= 360:
                ang -= 360
            # Skip holes that overlap with flanges
            if away_from_flanges(ang):
                cap_perf_holes.append((ang, r_pos))

print(f"  Top cap: {len(cap_perf_holes)} ventilation holes in {n_radial_rows} rows")

def in_cap_perf(angle_deg, r):
    for h_ang, h_r in cap_perf_holes:
        ang_diff = abs(angle_deg - h_ang)
        if ang_diff > 180: ang_diff = 360 - ang_diff
        arc_dist = ang_diff * (np.pi / 180) * h_r
        r_dist = abs(r - h_r)
        if np.sqrt(arc_dist**2 + r_dist**2) < perf_hole_r:
            return True
    return False

cap_verts = []
cap_faces = []
cap_idx = {}

for ai in range(cap_sections):
    ang_deg = (ai / cap_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    for ri in range(cap_radial + 1):
        r = cap_inner_r + (ri / cap_radial) * (cap_outer_r - cap_inner_r)
        z_off = get_cap_flat_z_offset(ang_deg, r)
        cap_idx[(ai, ri, 0)] = len(cap_verts)
        cap_verts.append([r * cos_a, r * sin_a, housing_top_z - z_off])
        cap_idx[(ai, ri, 1)] = len(cap_verts)
        cap_verts.append([r * cos_a, r * sin_a, housing_top_z - z_off - sheet_metal_thickness])

for ai in range(cap_sections):
    nai = (ai + 1) % cap_sections
    mid_ang = ((ai + 0.5) / cap_sections) * 360
    cap_in_slot = in_cap_slot(mid_ang)
    for ri in range(cap_radial):
        mid_r = cap_inner_r + ((ri + 0.5) / cap_radial) * (cap_outer_r - cap_inner_r)
        if in_cap_perf(mid_ang, mid_r):
            continue
        # Cutout over the ceramic slot — slot must be open from above so the
        # glass can drop into the ceramic. Outer region keeps its dip (flaps).
        if cap_in_slot and mid_r <= ceramic_outer_r:
            continue
        v0t, v0b = cap_idx[(ai, ri, 0)], cap_idx[(ai, ri, 1)]
        v1t, v1b = cap_idx[(ai, ri+1, 0)], cap_idx[(ai, ri+1, 1)]
        v2t, v2b = cap_idx[(nai, ri+1, 0)], cap_idx[(nai, ri+1, 1)]
        v3t, v3b = cap_idx[(nai, ri, 0)], cap_idx[(nai, ri, 1)]
        cap_faces.append([v0t, v1t, v3t])
        cap_faces.append([v3t, v1t, v2t])
        cap_faces.append([v0b, v3b, v1b])
        cap_faces.append([v3b, v2b, v1b])

cap_flat = trimesh.Trimesh(vertices=np.array(cap_verts), faces=np.array(cap_faces))
cap_flat.fix_normals()

# Outer lip going DOWN
lip_drop = 10
lip_sections = 360
lip_z_bands = 8
lip_verts = []
lip_faces = []
lip_idx = {}

def get_lip_z_offset(angle_deg):
    z = get_slot_z_offset(angle_deg)
    if z > 0:
        return z
    side_mm = 10.0
    side_deg = side_mm / cap_outer_r * (180 / np.pi)
    straight_h = slot_depth - slot_width / 2
    for slot_center in slot_positions:
        diff = abs(angle_deg - slot_center)
        if diff > 180: diff = 360 - diff
        if diff <= slot_arc_half_deg + side_deg:
            t = (diff - slot_arc_half_deg) / side_deg
            return straight_h * (1 - t)
    return 0

for ai in range(lip_sections):
    ang_deg = (ai / lip_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    z_off_cap = get_slot_z_offset(ang_deg)  # lip top tracks the dipped cap_flat at slots
    z_off_lip = get_lip_z_offset(ang_deg)
    extra_drop = z_off_lip - z_off_cap
    for zi in range(lip_z_bands + 1):
        z = (housing_top_z - z_off_cap) - (zi / lip_z_bands) * (lip_drop + extra_drop)
        for ri, r in enumerate([cap_outer_r - sheet_metal_thickness, cap_outer_r]):
            lip_idx[(ai, zi, ri)] = len(lip_verts)
            lip_verts.append([r * cos_a, r * sin_a, z])

for ai in range(lip_sections):
    nai = (ai + 1) % lip_sections
    for zi in range(lip_z_bands):
        lip_faces.append([lip_idx[(ai, zi, 0)], lip_idx[(ai, zi+1, 0)], lip_idx[(nai, zi, 0)]])
        lip_faces.append([lip_idx[(nai, zi, 0)], lip_idx[(ai, zi+1, 0)], lip_idx[(nai, zi+1, 0)]])
        lip_faces.append([lip_idx[(ai, zi, 1)], lip_idx[(nai, zi, 1)], lip_idx[(ai, zi+1, 1)]])
        lip_faces.append([lip_idx[(nai, zi, 1)], lip_idx[(nai, zi+1, 1)], lip_idx[(ai, zi+1, 1)]])

cap_lip = trimesh.Trimesh(vertices=np.array(lip_verts), faces=np.array(lip_faces))
cap_lip.fix_normals()

# Inner grab lip
grab_sections = 360
grab_z_bands = 4
grab_verts = []
grab_faces = []
grab_idx = {}

def _grab_in_slot(ai):
    return in_cap_slot((ai / grab_sections) * 360)

for ai in range(grab_sections):
    if _grab_in_slot(ai):
        continue  # inner grab ring breaks at slot openings so the ceramic slot is accessible
    ang_deg = (ai / grab_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    for zi in range(grab_z_bands + 1):
        z = housing_top_z - (zi / grab_z_bands) * ceramic_grab_lip
        for ri, r in enumerate([ceramic_inner_r, ceramic_inner_r + sheet_metal_thickness]):
            grab_idx[(ai, zi, ri)] = len(grab_verts)
            grab_verts.append([r * cos_a, r * sin_a, z])

for ai in range(grab_sections):
    nai = (ai + 1) % grab_sections
    if _grab_in_slot(ai) or _grab_in_slot(nai):
        continue
    for zi in range(grab_z_bands):
        grab_faces.append([grab_idx[(ai, zi, 0)], grab_idx[(ai, zi+1, 0)], grab_idx[(nai, zi, 0)]])
        grab_faces.append([grab_idx[(nai, zi, 0)], grab_idx[(ai, zi+1, 0)], grab_idx[(nai, zi+1, 0)]])
        grab_faces.append([grab_idx[(ai, zi, 1)], grab_idx[(nai, zi, 1)], grab_idx[(ai, zi+1, 1)]])
        grab_faces.append([grab_idx[(nai, zi, 1)], grab_idx[(nai, zi+1, 1)], grab_idx[(ai, zi+1, 1)]])

cap_grab = trimesh.Trimesh(vertices=np.array(grab_verts), faces=np.array(grab_faces))
cap_grab.fix_normals()

# Chamber ridge into insulation gap
ridge_drop = 5
ridge_sections = 360
ridge_z_bands = 4
ridge_verts = []
ridge_faces = []
ridge_idx = {}

for ai in range(ridge_sections):
    ang_deg = (ai / ridge_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    z_off = get_slot_z_offset(ang_deg)  # ridge dips with cap at slots (outside ceramic)
    for zi in range(ridge_z_bands + 1):
        z = (housing_top_z - z_off) - (zi / ridge_z_bands) * ridge_drop
        for ri, r in enumerate([housing_inner_r - sheet_metal_thickness, housing_inner_r]):
            ridge_idx[(ai, zi, ri)] = len(ridge_verts)
            ridge_verts.append([r * cos_a, r * sin_a, z])

for ai in range(ridge_sections):
    nai = (ai + 1) % ridge_sections
    for zi in range(ridge_z_bands):
        ridge_faces.append([ridge_idx[(ai, zi, 0)], ridge_idx[(ai, zi+1, 0)], ridge_idx[(nai, zi, 0)]])
        ridge_faces.append([ridge_idx[(nai, zi, 0)], ridge_idx[(ai, zi+1, 0)], ridge_idx[(nai, zi+1, 0)]])
        ridge_faces.append([ridge_idx[(ai, zi, 1)], ridge_idx[(nai, zi, 1)], ridge_idx[(ai, zi+1, 1)]])
        ridge_faces.append([ridge_idx[(nai, zi, 1)], ridge_idx[(nai, zi+1, 1)], ridge_idx[(ai, zi+1, 1)]])

cap_ridge = trimesh.Trimesh(vertices=np.array(ridge_verts), faces=np.array(ridge_faces))
cap_ridge.fix_normals()

# Ceramic outer retaining ridge (holds ceramic cylinder from outside at top)
# Only between slots — skip angular ranges where slots are
ceramic_ret_drop = 10  # 10mm flap hugging ceramic OD between slots — alignment + support
ceramic_ret_z_bands = 4
ceramic_ret_margin = 0  # ridge runs all the way up to the slot edge so flaps frame the slot

def in_slot_zone(ang):
    """Check if angle is within a slot opening (with margin)."""
    for sc in slot_positions:
        diff = abs(ang - sc)
        if diff > 180: diff = 360 - diff
        if diff <= slot_arc_half_deg + ceramic_ret_margin:
            return True
    return False

# Build arc segments only between slots
ceramic_ret_segments = []
ceramic_ret_verts = []
ceramic_ret_faces = []

# Walk around 360 degrees, collect contiguous non-slot arcs
in_segment = False
seg_start = None
for deg_i in range(3600):
    ang = deg_i / 10.0
    is_slot = in_slot_zone(ang)
    if not is_slot and not in_segment:
        seg_start = ang
        in_segment = True
    elif is_slot and in_segment:
        ceramic_ret_segments.append((seg_start, ang))
        in_segment = False
if in_segment:
    # Wraps around 360
    if ceramic_ret_segments and ceramic_ret_segments[0][0] == 0.0:
        # Merge with first segment
        ceramic_ret_segments[0] = (seg_start, ceramic_ret_segments[0][1] + 360)
    else:
        ceramic_ret_segments.append((seg_start, 360.0))

for seg_start_ang, seg_end_ang in ceramic_ret_segments:
    seg_steps = max(4, int((seg_end_ang - seg_start_ang) / 1.0))
    seg_idx = {}
    base_vi = len(ceramic_ret_verts)
    for si in range(seg_steps + 1):
        ang_deg = seg_start_ang + (si / seg_steps) * (seg_end_ang - seg_start_ang)
        ang_rad = np.radians(ang_deg)
        cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
        for zi in range(ceramic_ret_z_bands + 1):
            z = housing_top_z - (zi / ceramic_ret_z_bands) * ceramic_ret_drop
            for ri, r in enumerate([ceramic_outer_r, ceramic_outer_r + sheet_metal_thickness]):
                seg_idx[(si, zi, ri)] = len(ceramic_ret_verts)
                ceramic_ret_verts.append([r * cos_a, r * sin_a, z])
    for si in range(seg_steps):
        nsi = si + 1
        for zi in range(ceramic_ret_z_bands):
            ceramic_ret_faces.append([seg_idx[(si, zi, 0)], seg_idx[(si, zi+1, 0)], seg_idx[(nsi, zi, 0)]])
            ceramic_ret_faces.append([seg_idx[(nsi, zi, 0)], seg_idx[(si, zi+1, 0)], seg_idx[(nsi, zi+1, 0)]])
            ceramic_ret_faces.append([seg_idx[(si, zi, 1)], seg_idx[(nsi, zi, 1)], seg_idx[(si, zi+1, 1)]])
            ceramic_ret_faces.append([seg_idx[(nsi, zi, 1)], seg_idx[(nsi, zi+1, 1)], seg_idx[(si, zi+1, 1)]])

cap_ceramic_ridge = trimesh.Trimesh(vertices=np.array(ceramic_ret_verts), faces=np.array(ceramic_ret_faces))
cap_ceramic_ridge.fix_normals()
print(f"  Added ceramic retaining ridge ({len(ceramic_ret_segments)} segments between slots)")

# Combine cap
top_cap_full = trimesh.util.concatenate([cap_flat, cap_lip, cap_grab, cap_ridge, cap_ceramic_ridge])
top_cap = top_cap_full
top_cap.visual.face_colors = [180, 220, 140, 255]

# =============================================================================
# TOP CAP — FINAL DESIGN (2026-06-10): TWO PIECES, no welded bosses, no cap screws
#   04a_Cap_Shell        — cap_flat + skirt + 6 drop tabs reaching the top spacer
#                          bolt ring, + hinge finger (the tab at 292.4 deg keeps
#                          going UP past the rim and curls into 2 hinge barrels)
#   04b_Cap_HoldDown_Ring — flat ring w/ slot notches + 3 short walls (grips the
#                          ceramic + tucks inside the chamber wall). NO fasteners:
#                          clamped between shell and chamber when the cap bolts on.
# Fastening: the 6 EXISTING top-ring spacer bolts pass through the drop tabs.
# =============================================================================
print("Building final two-piece top cap (shell + hold-down ring)...")

def _annular_sector(r0, r1, z0, z1, a0, a1, steps=None):
    if steps is None: steps = max(6, int(a1 - a0))
    V, F = [], []
    for si in range(steps + 1):
        a = np.radians(a0 + (a1 - a0) * si / steps)
        ca, sa = np.cos(a), np.sin(a)
        for r in (r0, r1):
            for z in (z0, z1):
                V.append([r * ca, r * sa, z])
    def vi(si, ri, zi): return si * 4 + ri * 2 + zi
    for si in range(steps):
        n = si + 1
        for (ri, zi, rj, zj) in ((0,1,1,1),(1,0,0,0),(0,0,0,1),(1,1,1,0)):
            a_, b_, c_, d_ = vi(si,ri,zi), vi(si,rj,zj), vi(n,ri,zi), vi(n,rj,zj)
            F += [[a_, b_, c_], [c_, b_, d_]]
    for si in (0, steps):
        a_, b_, c_, d_ = vi(si,0,0), vi(si,0,1), vi(si,1,0), vi(si,1,1)
        F += [[a_, b_, c_], [c_, b_, d_]]
    m = trimesh.Trimesh(vertices=np.array(V), faces=np.array(F))
    m.fix_normals()
    return m

CAP_BOLT_Z = 59                               # top spacer ring bolt circle
CAP_BOLT_ANGLES = [52.4 + k*60 for k in range(6)]   # same clocking as the bolts
CAP_TAB_HALF_DEG = np.degrees(6.0 / cap_outer_r)    # ~12mm-wide fingers
CAP_TAB_TOP = housing_top_z - lip_drop + 3
CAP_TAB_BOT = 55

HINGE_ANGLE_DEG = 292.4                       # center of the big slot gap
_ha = np.radians(HINGE_ANGLE_DEG)
_htx, _hty = -np.sin(_ha), np.cos(_ha)        # hinge pin axis (tangent)
HINGE_PIVOT_R, HINGE_PIVOT_Z = 81.5, 109   # barrel at the strap TOP edge — clears the z=99 bolt head by 2.8mm
HINGE_KN_LEN = 25/3

def _tangent_cyl(radius, length, t_off, color=None):
    c = trimesh.creation.cylinder(radius=radius, height=length, sections=20)
    c.apply_transform(trimesh.geometry.align_vectors([0,0,1],[_htx,_hty,0]))
    c.apply_translation([HINGE_PIVOT_R*np.cos(_ha)+_htx*t_off,
                         HINGE_PIVOT_R*np.sin(_ha)+_hty*t_off, HINGE_PIVOT_Z])
    if color: c.visual.face_colors = color
    return c

_shell_bits = [cap_flat, cap_lip]
for _ang in CAP_BOLT_ANGLES:
    _shell_bits.append(_annular_sector(cap_outer_r - sheet_metal_thickness, cap_outer_r,
                       CAP_TAB_BOT, CAP_TAB_TOP, _ang - CAP_TAB_HALF_DEG, _ang + CAP_TAB_HALF_DEG))
    _a = np.radians(_ang)
    _h = trimesh.creation.cylinder(radius=1.8, height=4.5, sections=16)
    _h.apply_transform(trimesh.geometry.align_vectors([0,0,1],[np.cos(_a),np.sin(_a),0]))
    _h.apply_translation([(cap_outer_r - sheet_metal_thickness/2)*np.cos(_a),
                          (cap_outer_r - sheet_metal_thickness/2)*np.sin(_a), CAP_BOLT_Z])
    _h.visual.face_colors = [40, 40, 45, 255]
    _shell_bits.append(_h)
# hinge finger: strap up the outside + two curl barrels (piano-hinge style)
_shell_bits.append(_annular_sector(cap_outer_r - sheet_metal_thickness, cap_outer_r,
                   housing_top_z - lip_drop - 3, HINGE_PIVOT_Z,
                   HINGE_ANGLE_DEG - CAP_TAB_HALF_DEG, HINGE_ANGLE_DEG + CAP_TAB_HALF_DEG))
_shell_bits.append(_tangent_cyl(4, HINGE_KN_LEN, -HINGE_KN_LEN))
_shell_bits.append(_tangent_cyl(4, HINGE_KN_LEN,  HINGE_KN_LEN))
_shell_bits.append(_tangent_cyl(2.6, HINGE_KN_LEN + 0.6, -HINGE_KN_LEN, [40, 40, 45, 255]))
_shell_bits.append(_tangent_cyl(2.6, HINGE_KN_LEN + 0.6,  HINGE_KN_LEN, [40, 40, 45, 255]))

cap_shell = trimesh.util.concatenate(_shell_bits)
cap_shell.visual.face_colors = [180, 220, 140, 255]
print(f"  Cap shell: 6 drop tabs to z={CAP_BOLT_Z} bolts + hinge finger at {HINGE_ANGLE_DEG} deg")

# hold-down ring — DEAD FLAT top, walls only hang down
_web_top = housing_top_z - sheet_metal_thickness
_slot_gaps = []
_sorted_slots = sorted(slot_positions)
for _i in range(len(_sorted_slots)):
    _a0 = _sorted_slots[_i] + slot_arc_half_deg
    _a1 = (_sorted_slots[_i+1] if _i+1 < len(_sorted_slots) else _sorted_slots[0]+360) - slot_arc_half_deg
    _slot_gaps.append((_a0, _a1))
_ring_bits = []
for _a0, _a1 in _slot_gaps:
    _ring_bits.append(_annular_sector(ceramic_inner_r, ceramic_inner_r + sheet_metal_thickness,
                      _web_top - 3.0, _web_top, _a0, _a1))                       # grab lip (in the bore)
    _ring_bits.append(_annular_sector(ceramic_outer_r, ceramic_outer_r + sheet_metal_thickness,
                      _web_top - 10.0, _web_top, _a0, _a1))                      # flaps (hug ceramic OD)
    _ring_bits.append(_annular_sector(housing_inner_r - sheet_metal_thickness, housing_inner_r,
                      _web_top - 6.0, _web_top, _a0, _a1))                       # edge wall (inside chamber)
    _m0 = _a0 + 4.0; _m1 = _a1 - 4.0
    _ring_bits.append(_annular_sector(ceramic_inner_r, housing_inner_r,
                      _web_top - 2.0, _web_top, _m0, _m1))                       # flat web
hold_down_ring = trimesh.util.concatenate(_ring_bits)
hold_down_ring.visual.face_colors = [120, 170, 220, 255]
print("  Hold-down ring: flat web + 3 hanging walls, clamp-fit (no fasteners)")

top_cap = cap_shell   # legacy alias

# (2026-06-10) Welded screw bosses DELETED — the cap now fastens through its
# 6 drop tabs using the existing top spacer-ring bolts. Nothing welds to the body.

# =============================================================================
# PART 3: LID ASSEMBLY
# =============================================================================
print("Building lid assembly...")

lid_height = 35
lid_bottom_z = housing_top_z

# Lid fastening — mirrors the base: 2 shared bolt rings, bolts clocked into the slot
# gaps (same ring_screw_angles). Top ring (z+26) shares the top plate's lip; bottom
# ring (z+9) shares the ceramic-lid holder's flange.
lid_ring_zs = [lid_bottom_z + 28, lid_bottom_z + 8]   # 119 (top), 99 (bottom) — tight to the plates
def in_lid_ring_hole(angle_deg, z, mid_r):
    for hz in lid_ring_zs:
        if abs(z - hz) > ring_screw_hole_r: continue
        for ha in ring_screw_angles:
            ad = abs(angle_deg - ha)
            if ad > 180: ad = 360 - ad
            arc = ad * (np.pi / 180) * mid_r
            if np.sqrt(arc**2 + (z - hz)**2) < ring_screw_hole_r: return True
    return False

def punch_radial_holes(mesh, ring_zs, angles, hr=ring_screw_hole_r):
    """Remove faces near each (angle, z) hole — a through-hole, no boolean needed."""
    fc = mesh.triangles_center
    ang = (np.degrees(np.arctan2(fc[:, 1], fc[:, 0])) % 360)
    z = fc[:, 2]; r = np.sqrt(fc[:, 0]**2 + fc[:, 1]**2)
    keep = np.ones(len(mesh.faces), dtype=bool)
    for hz in ring_zs:
        for a in angles:
            ad = np.abs(ang - a); ad = np.minimum(ad, 360 - ad)
            arc = np.radians(ad) * r
            keep &= ~(np.sqrt(arc**2 + (z - hz)**2) < hr)
    mesh.update_faces(keep)
    return mesh

lid_inner = create_hollow_cylinder(housing_inner_r, housing_outer_r, lid_height, sections=240)
lid_inner.apply_translation([0, 0, lid_bottom_z])
# (round holes drilled in gen_lid_extras.py via boolean cutter)

# Lid outer mesh with perforations
lid_perf_holes = []
lid_perf_n_z = int((lid_height - 10) / perf_spacing)
for zi in range(lid_perf_n_z):
    z = lid_bottom_z + 5 + zi * perf_spacing
    offset = (perf_spacing / 2) if (zi % 2) else 0
    for ai in range(perf_n_ang):
        ang = (ai / perf_n_ang) * 360 + np.degrees(offset / perf_mid_r)
        lid_perf_holes.append((ang, z))

lid_mesh_verts = []
lid_mesh_faces = []
lid_mesh_idx = {}
lid_mesh_z_bands = 240  # Match main mesh resolution for round holes

for ai in range(mesh_sections):
    ang_deg = (ai / mesh_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    for zi in range(lid_mesh_z_bands + 1):
        z = lid_bottom_z + (zi / lid_mesh_z_bands) * lid_height
        for ri, r in enumerate([mesh_inner_r, mesh_outer_r]):
            lid_mesh_idx[(ai, zi, ri)] = len(lid_mesh_verts)
            lid_mesh_verts.append([r * cos_a, r * sin_a, z])

for ai in range(mesh_sections):
    nai = (ai + 1) % mesh_sections
    mid_ang = ((ai + 0.5) / mesh_sections) * 360
    for zi in range(lid_mesh_z_bands):
        mid_z = lid_bottom_z + ((zi + 0.5) / lid_mesh_z_bands) * lid_height
        if in_perf(mid_ang, mid_z, lid_perf_holes, perf_mid_r, perf_hole_r): continue
        if in_lid_ring_hole(mid_ang, mid_z, perf_mid_r): continue
        lid_mesh_faces.append([lid_mesh_idx[(ai, zi, 0)], lid_mesh_idx[(ai, zi+1, 0)], lid_mesh_idx[(nai, zi, 0)]])
        lid_mesh_faces.append([lid_mesh_idx[(nai, zi, 0)], lid_mesh_idx[(ai, zi+1, 0)], lid_mesh_idx[(nai, zi+1, 0)]])
        lid_mesh_faces.append([lid_mesh_idx[(ai, zi, 1)], lid_mesh_idx[(nai, zi, 1)], lid_mesh_idx[(ai, zi+1, 1)]])
        lid_mesh_faces.append([lid_mesh_idx[(nai, zi, 1)], lid_mesh_idx[(nai, zi+1, 1)], lid_mesh_idx[(ai, zi+1, 1)]])

for ai in range(mesh_sections):
    nai = (ai + 1) % mesh_sections
    lid_mesh_faces.append([lid_mesh_idx[(ai, 0, 0)], lid_mesh_idx[(nai, 0, 0)], lid_mesh_idx[(ai, 0, 1)]])
    lid_mesh_faces.append([lid_mesh_idx[(nai, 0, 0)], lid_mesh_idx[(nai, 0, 1)], lid_mesh_idx[(ai, 0, 1)]])
    lid_mesh_faces.append([lid_mesh_idx[(ai, lid_mesh_z_bands, 0)], lid_mesh_idx[(ai, lid_mesh_z_bands, 1)], lid_mesh_idx[(nai, lid_mesh_z_bands, 0)]])
    lid_mesh_faces.append([lid_mesh_idx[(nai, lid_mesh_z_bands, 0)], lid_mesh_idx[(ai, lid_mesh_z_bands, 1)], lid_mesh_idx[(nai, lid_mesh_z_bands, 1)]])

lid_outer = trimesh.Trimesh(vertices=np.array(lid_mesh_verts), faces=np.array(lid_mesh_faces))
lid_outer.fix_normals()

# Lid bottom ring -- perforated
lid_vent_inner_r = housing_outer_r
lid_vent_outer_r = mesh_outer_r
lid_vent_mid_r = (lid_vent_inner_r + lid_vent_outer_r) / 2

lid_bottom_perf_holes = []
lid_bperf_n_ang = int((2 * np.pi * lid_vent_mid_r) / perf_spacing)
for r_row in range(-1, 2):
    r_pos = lid_vent_mid_r + r_row * perf_spacing
    if r_pos < lid_vent_inner_r + 2 or r_pos > lid_vent_outer_r - 2:
        continue
    offset = (perf_spacing / 2) if (r_row % 2) else 0
    for ai in range(lid_bperf_n_ang):
        ang = (ai / lid_bperf_n_ang) * 360 + np.degrees(offset / lid_vent_mid_r)
        lid_bottom_perf_holes.append((ang, r_pos))

def in_lid_bottom_perf(angle_deg, r):
    for h_ang, h_r in lid_bottom_perf_holes:
        ang_diff = abs(angle_deg - h_ang)
        if ang_diff > 180: ang_diff = 360 - ang_diff
        arc_dist = ang_diff * (np.pi / 180) * h_r
        r_dist = abs(r - h_r)
        if np.sqrt(arc_dist**2 + r_dist**2) < perf_hole_r:
            return True
    return False

lbr_sections = 720  # Match main mesh for round holes
lbr_radial = 120
lbr_verts = []
lbr_faces = []
lbr_idx = {}

for ai in range(lbr_sections):
    ang_deg = (ai / lbr_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    for ri in range(lbr_radial + 1):
        r = ceramic_outer_r + (ri / lbr_radial) * (mesh_outer_r - ceramic_outer_r)
        for zi, z in enumerate([lid_bottom_z, lid_bottom_z + sheet_metal_thickness]):
            lbr_idx[(ai, ri, zi)] = len(lbr_verts)
            lbr_verts.append([r * cos_a, r * sin_a, z])

for ai in range(lbr_sections):
    nai = (ai + 1) % lbr_sections
    mid_ang = ((ai + 0.5) / lbr_sections) * 360
    for ri in range(lbr_radial):
        mid_r = ceramic_outer_r + ((ri + 0.5) / lbr_radial) * (mesh_outer_r - ceramic_outer_r)
        if in_lid_bottom_perf(mid_ang, mid_r):
            continue
        lbr_faces.append([lbr_idx[(ai, ri, 1)], lbr_idx[(ai, ri+1, 1)], lbr_idx[(nai, ri, 1)]])
        lbr_faces.append([lbr_idx[(nai, ri, 1)], lbr_idx[(ai, ri+1, 1)], lbr_idx[(nai, ri+1, 1)]])
        lbr_faces.append([lbr_idx[(ai, ri, 0)], lbr_idx[(nai, ri, 0)], lbr_idx[(ai, ri+1, 0)]])
        lbr_faces.append([lbr_idx[(nai, ri, 0)], lbr_idx[(nai, ri+1, 0)], lbr_idx[(ai, ri+1, 0)]])

for ai in range(lbr_sections):
    nai = (ai + 1) % lbr_sections
    lbr_faces.append([lbr_idx[(ai, 0, 0)], lbr_idx[(ai, 0, 1)], lbr_idx[(nai, 0, 0)]])
    lbr_faces.append([lbr_idx[(nai, 0, 0)], lbr_idx[(ai, 0, 1)], lbr_idx[(nai, 0, 1)]])
    ri = lbr_radial
    lbr_faces.append([lbr_idx[(ai, ri, 0)], lbr_idx[(nai, ri, 0)], lbr_idx[(ai, ri, 1)]])
    lbr_faces.append([lbr_idx[(nai, ri, 0)], lbr_idx[(nai, ri, 1)], lbr_idx[(ai, ri, 1)]])

lid_bottom_ring = trimesh.Trimesh(vertices=np.array(lbr_verts), faces=np.array(lbr_faces))
lid_bottom_ring.fix_normals()

# Side wall
lid_ring_inner_r = ceramic_outer_r - 10
lid_wall_bottom = lid_bottom_z + sheet_metal_thickness
lid_wall_height = disk_body_h - sheet_metal_thickness  # 3.3mm — flush: body at lid base, only lip below
lid_wall = create_hollow_cylinder(ceramic_outer_r, ceramic_outer_r + sheet_metal_thickness, lid_wall_height)
lid_wall.apply_translation([0, 0, lid_wall_bottom])

# Retaining shelf
lid_shelf_z = lid_wall_bottom + lid_wall_height
lid_shelf = create_hollow_cylinder(lid_ring_inner_r, ceramic_outer_r, sheet_metal_thickness)
lid_shelf.apply_translation([0, 0, lid_shelf_z])

# (Ceramic-lid holder flange + top-plate lip are built short, with clean drilled round
#  holes, in gen_lid_extras.py — boolean cutter, not face removal.)

# Lid top disk -- perforated
lid_top_z = lid_bottom_z + lid_height
ltd_sections = 720  # Match main mesh for round holes
ltd_radial = 120
ltd_verts = []
ltd_faces = []
ltd_idx = {}

for ai in range(ltd_sections):
    ang_deg = (ai / ltd_sections) * 360
    ang_rad = np.radians(ang_deg)
    cos_a, sin_a = np.cos(ang_rad), np.sin(ang_rad)
    for ri in range(ltd_radial + 1):
        r = (ri / ltd_radial) * mesh_outer_r
        for zi, z in enumerate([lid_top_z, lid_top_z + sheet_metal_thickness]):
            ltd_idx[(ai, ri, zi)] = len(ltd_verts)
            if r < 0.01:
                ltd_verts.append([0, 0, z])
            else:
                ltd_verts.append([r * cos_a, r * sin_a, z])

for ai in range(ltd_sections):
    nai = (ai + 1) % ltd_sections
    mid_ang = ((ai + 0.5) / ltd_sections) * 360
    for ri in range(ltd_radial):
        mid_r = ((ri + 0.5) / ltd_radial) * mesh_outer_r
        if in_lid_bottom_perf(mid_ang, mid_r):
            continue
        ltd_faces.append([ltd_idx[(ai, ri, 1)], ltd_idx[(ai, ri+1, 1)], ltd_idx[(nai, ri, 1)]])
        ltd_faces.append([ltd_idx[(nai, ri, 1)], ltd_idx[(ai, ri+1, 1)], ltd_idx[(nai, ri+1, 1)]])
        ltd_faces.append([ltd_idx[(ai, ri, 0)], ltd_idx[(nai, ri, 0)], ltd_idx[(ai, ri+1, 0)]])
        ltd_faces.append([ltd_idx[(nai, ri, 0)], ltd_idx[(nai, ri+1, 0)], ltd_idx[(ai, ri+1, 0)]])

for ai in range(ltd_sections):
    nai = (ai + 1) % ltd_sections
    ri = ltd_radial
    ltd_faces.append([ltd_idx[(ai, ri, 0)], ltd_idx[(ai, ri, 1)], ltd_idx[(nai, ri, 0)]])
    ltd_faces.append([ltd_idx[(nai, ri, 0)], ltd_idx[(ai, ri, 1)], ltd_idx[(nai, ri, 1)]])

lid_top_disk = trimesh.Trimesh(vertices=np.array(ltd_verts), faces=np.array(ltd_faces))
lid_top_disk.fix_normals()

# (Top-plate lip added in gen_lid_extras.py — short, with drilled round holes.)

# Handle — offset away from hinge toward the opening edge
lid_top_surface_z = lid_bottom_z + lid_height + sheet_metal_thickness
handle_height = 25
handle_width = 50
handle_bar_r = 4
# Shift handle 40mm from center toward the opening (opposite the hinge)
handle_offset_dist = 40
slot_4_end_angle = slot_positions[3] + (slot_width * scale_factor / 2 / circumference * 360)
large_gap_arc_deg = gaps[3] * scale_factor / circumference * 360
_hinge_angle = slot_4_end_angle + large_gap_arc_deg / 2
if _hinge_angle >= 360:
    _hinge_angle -= 360
opposite_angle = np.radians(_hinge_angle) + np.pi
handle_off_x = handle_offset_dist * np.cos(opposite_angle)
handle_off_y = handle_offset_dist * np.sin(opposite_angle)
# Handle bar runs parallel to hinge (tangent direction at hinge angle)
handle_tangent_x = -np.sin(np.radians(_hinge_angle))
handle_tangent_y = np.cos(np.radians(_hinge_angle))
print(f"  Handle offset {handle_offset_dist}mm toward opening (opposite hinge)")
hp1 = trimesh.creation.cylinder(radius=handle_bar_r, height=handle_height, sections=16)
hp1.apply_translation([handle_off_x + handle_tangent_x * handle_width/2,
                        handle_off_y + handle_tangent_y * handle_width/2,
                        lid_top_surface_z + handle_height/2])
hp2 = trimesh.creation.cylinder(radius=handle_bar_r, height=handle_height, sections=16)
hp2.apply_translation([handle_off_x - handle_tangent_x * handle_width/2,
                        handle_off_y - handle_tangent_y * handle_width/2,
                        lid_top_surface_z + handle_height/2])
hbar = trimesh.creation.cylinder(radius=handle_bar_r, height=handle_width, sections=16)
# Rotate bar to align with tangent direction (parallel to hinge)
bar_angle = np.arctan2(handle_tangent_y, handle_tangent_x)
hbar.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
hbar.apply_transform(trimesh.transformations.rotation_matrix(bar_angle, [0, 0, 1]))
hbar.apply_translation([handle_off_x, handle_off_y, lid_top_surface_z + handle_height])

lid_full = trimesh.util.concatenate([lid_inner, lid_outer, lid_bottom_ring, lid_wall, lid_shelf, lid_top_disk, hp1, hp2, hbar])
lid_assembly = lid_full
lid_assembly.visual.face_colors = [140, 180, 220, 255]

# =============================================================================
# PART 4: CERAMIC CYLINDER (loaded from STL)
# =============================================================================
print("Loading ceramic cylinder...")

ceramic_parts_dir = os.path.join(os.path.dirname(cad_exports_dir), "Ceramic Parts")
ceramic_stl_path = os.path.join(ceramic_parts_dir, "updatedcylinder.stl")
if not os.path.exists(ceramic_stl_path):
    fallback = os.path.join(cad_exports_dir, "Individual Parts", "STL", "06_Ceramic_Cylinder.stl")
    print(f"  (source missing, using fallback {os.path.basename(fallback)})")
    ceramic_stl_path = fallback
ceramic_cylinder = trimesh.load(ceramic_stl_path)
ceramic_cylinder.visual.face_colors = ceramic_body_color

# =============================================================================
# PART 5a: CERAMIC BASE DISK
# =============================================================================
print("Loading ceramic base disk...")

ceramic_disk_stl_path = os.path.join(ceramic_parts_dir, "lidbottomupdated.stl")
_disk_source_present = os.path.exists(ceramic_disk_stl_path)
if not _disk_source_present:
    fallback_base = os.path.join(cad_exports_dir, "Individual Parts", "STL", "07_Ceramic_Base_Disk.stl")
    print(f"  (disk source missing, using fallback {os.path.basename(fallback_base)} as-is)")
    ceramic_disk_stl_path = fallback_base
ceramic_base = trimesh.load(ceramic_disk_stl_path)
if _disk_source_present:
    ceramic_base.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    base_bounds = ceramic_base.bounds
    ceramic_base.apply_translation([0, 0, -base_bounds[0][2]])
    ceramic_base.apply_translation([0, 0, -disk_thickness])
ceramic_base.visual.face_colors = ceramic_disk_color

# =============================================================================
# PART 5b: CERAMIC LID DISK (same shape as base disk, sits on top of cylinder)
# =============================================================================
print("Loading ceramic lid disk...")

if _disk_source_present:
    ceramic_lid = trimesh.load(ceramic_disk_stl_path)
    ceramic_lid.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    lid_bounds = ceramic_lid.bounds
    ceramic_lid.apply_translation([0, 0, -lid_bounds[0][2]])
else:
    fallback_lid = os.path.join(cad_exports_dir, "Individual Parts", "STL", "07b_Ceramic_Lid_Disk.stl")
    ceramic_lid = trimesh.load(fallback_lid)
ceramic_lid.visual.face_colors = ceramic_disk_color

# =============================================================================
# PART 6: KANTHAL COIL
# =============================================================================
print("Building kanthal coil...")

kanthal_wire_diameter = 1.2
coil_radius = ceramic_outer_r - groove_depth/2
start_angle_rad = np.radians(groove_seam_angle)
kanthal_points = []
points_per_turn = 36

for i in range(num_wraps * points_per_turn + 1):
    t = i / points_per_turn
    angle = start_angle_rad + t * 2 * np.pi
    z = groove_end_height + t * pitch
    if z > groove_start_height: break
    kanthal_points.append([coil_radius * np.cos(angle), coil_radius * np.sin(angle), z])

kanthal_coil = create_tube_along_path(kanthal_points, kanthal_wire_diameter/2, segments=6)
kanthal_coil.visual.face_colors = kanthal_color

# =============================================================================
# PART 7: THERMOCOUPLE
# =============================================================================
print("Building thermocouple...")

hole_angle_rad = np.radians(hole_position_angle)
probe_tip_dia = 3
probe_tip_len = 4
thread_dia = 5.5
thread_len = 10
hex_nut_size = 10
hex_nut_height = 5
cable_dia = 2
hole_z = hole_center_height

tc_parts = []

probe = trimesh.creation.cylinder(radius=probe_tip_dia/2, height=probe_tip_len, sections=16)
probe.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
probe.apply_transform(trimesh.transformations.rotation_matrix(hole_angle_rad, [0, 0, 1]))
probe_radius = ceramic_outer_r - thread_len - probe_tip_len/2
probe.apply_translation([probe_radius * np.cos(hole_angle_rad), probe_radius * np.sin(hole_angle_rad), hole_z])
tc_parts.append(probe)

threaded = trimesh.creation.cylinder(radius=thread_dia/2, height=thread_len, sections=16)
threaded.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
threaded.apply_transform(trimesh.transformations.rotation_matrix(hole_angle_rad, [0, 0, 1]))
threaded_r = ceramic_outer_r - thread_len/2
threaded.apply_translation([threaded_r * np.cos(hole_angle_rad), threaded_r * np.sin(hole_angle_rad), hole_z])
tc_parts.append(threaded)

hex_nut = trimesh.creation.cylinder(radius=hex_nut_size/2, height=hex_nut_height, sections=6)
hex_nut.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
hex_nut.apply_transform(trimesh.transformations.rotation_matrix(hole_angle_rad, [0, 0, 1]))
nut_r = ceramic_outer_r + hex_nut_height/2
hex_nut.apply_translation([nut_r * np.cos(hole_angle_rad), nut_r * np.sin(hole_angle_rad), hole_z])
tc_parts.append(hex_nut)

cable_points = [
    [nut_r * np.cos(hole_angle_rad), nut_r * np.sin(hole_angle_rad), hole_z],
    [air_gap_mid_r * np.cos(hole_angle_rad), air_gap_mid_r * np.sin(hole_angle_rad), hole_z],
    [air_gap_mid_r * np.cos(hole_angle_rad), air_gap_mid_r * np.sin(hole_angle_rad), housing_bottom_z + 1],
    [air_gap_mid_r * np.cos(hole_angle_rad), air_gap_mid_r * np.sin(hole_angle_rad), housing_bottom_z - 15],
]
cable = create_tube_along_path(cable_points, cable_dia/2, segments=6)
tc_parts.append(cable)

thermocouple = trimesh.util.concatenate(tc_parts)
thermocouple.visual.face_colors = [180, 180, 190, 255]

# =============================================================================
# PART 8: CERAMIC LEGS (all 3 concatenated)
# =============================================================================
print("Building ceramic legs...")

leg_height = 25
leg_body_radius = 10
leg_flange_radius = 14
leg_flange_height = 5
insert_radius = 5
insert_height = 8

m6_clearance_r = 3.3  # M6 clearance hole radius (6.6mm diameter)

feet = []
for angle_deg in leg_angles:
    angle_rad = np.radians(angle_deg)
    leg_x = leg_hole_r * np.cos(angle_rad)
    leg_y = leg_hole_r * np.sin(angle_rad)

    body = trimesh.creation.cylinder(radius=leg_body_radius, height=leg_height - leg_flange_height, sections=32)
    body.apply_translation([leg_x, leg_y, housing_bottom_z - (leg_height - leg_flange_height)/2])
    body.visual.face_colors = ceramic_body_color

    flange = trimesh.creation.cylinder(radius=leg_flange_radius, height=leg_flange_height, sections=32)
    flange.apply_translation([leg_x, leg_y, housing_bottom_z - leg_height + leg_flange_height/2])
    flange.visual.face_colors = ceramic_body_color

    # Combine body + flange, then boolean-subtract M6 through-hole
    foot_solid = trimesh.util.concatenate([body, flange])
    bolt_hole = trimesh.creation.cylinder(radius=m6_clearance_r, height=leg_height + 2, sections=24)
    bolt_hole.apply_translation([leg_x, leg_y, housing_bottom_z - leg_height/2])
    try:
        foot_solid = foot_solid.difference(bolt_hole, engine='manifold')
    except:
        pass  # Skip if boolean fails
    foot_solid.visual.face_colors = ceramic_body_color

    feet.append(foot_solid)

# =============================================================================
# BOLTED STRAP HINGE (2026-06-10) — zero welds.
# Cap side: the shell's hinge finger (built into 04a_Cap_Shell) carries 2 barrels.
# Lid side: 05b_Lid_Hinge_Strap bolts under the lid's existing bolt at 292.4 deg
#           and carries 1 barrel between them. 05_Hinge_Pin slides through all 3.
# =============================================================================
print("Building bolted strap hinge (no welds)...")

_rotH = trimesh.transformations.rotation_matrix(_ha, [0, 0, 1])
# strap sized for a real M6: 20mm wide x 18mm tall (z 91-109), 6.6mm clearance
# hole at z=99. Barrel sits at the TOP edge (z=109) so the bolt head clears it.
_plate = trimesh.creation.box(extents=[sheet_metal_thickness, 20, 18])
_plate.apply_transform(_rotH)
_plate.apply_translation([78.15*np.cos(_ha), 78.15*np.sin(_ha), 100])
_strap_hole = trimesh.creation.cylinder(radius=3.3, height=5.0, sections=20)
_strap_hole.apply_transform(trimesh.geometry.align_vectors([0,0,1],[np.cos(_ha),np.sin(_ha),0]))
_strap_hole.apply_translation([78.15*np.cos(_ha), 78.15*np.sin(_ha), 99])
_strap_hole.visual.face_colors = [40, 40, 45, 255]
lid_hinge_strap = trimesh.util.concatenate([_plate, _tangent_cyl(4, HINGE_KN_LEN, 0), _tangent_cyl(2.6, HINGE_KN_LEN + 0.6, 0, [40, 40, 45, 255]), _strap_hole])
lid_hinge_strap.visual.face_colors = [138, 144, 152, 255]

hinge_pin = _tangent_cyl(2.5, 30, 0)
hinge_pin.visual.face_colors = [180, 185, 190, 255]
print("  Lid strap (1 bolt-on part) + pin. Cap-side barrels live on the shell.")

# =============================================================================
# PART 11: CONTROLLER BOX
# =============================================================================
print("Building controller box...")

box_width = 160
box_depth = 100
box_height = 70
box_wall = 2

control_box = trimesh.creation.box(extents=[box_width, box_depth, box_height])
control_box.visual.face_colors = [180, 185, 190, 255]

rex_bezel = trimesh.creation.box(extents=[52, 6, 52])
rex_bezel.apply_translation([-box_width/4 - 10, -box_depth/2 - 3, 5])
rex_bezel.visual.face_colors = [25, 25, 25, 255]

rex_display = trimesh.creation.box(extents=[42, 1, 18])
rex_display.apply_translation([-box_width/4 - 10, -box_depth/2 - 6, 18])
rex_display.visual.face_colors = [220, 0, 0, 255]

switch = trimesh.creation.box(extents=[20, 5, 30])
switch.apply_translation([0, -box_depth/2 - 2, 0])
switch.visual.face_colors = [30, 30, 30, 255]

switch_rocker = trimesh.creation.box(extents=[16, 3, 12])
switch_rocker.apply_translation([0, -box_depth/2 - 5, 5])
switch_rocker.visual.face_colors = [200, 50, 50, 255]

timer_bezel = trimesh.creation.box(extents=[40, 5, 40])
timer_bezel.apply_translation([35, -box_depth/2 - 2, 5])
timer_bezel.visual.face_colors = [35, 35, 35, 255]

timer_display = trimesh.creation.box(extents=[32, 1, 18])
timer_display.apply_translation([35, -box_depth/2 - 5, 12])
timer_display.visual.face_colors = [0, 150, 220, 255]

ssr = trimesh.creation.box(extents=[50, 65, 28])
ssr.apply_translation([30, 10, -10])
ssr.visual.face_colors = [35, 35, 40, 255]

ctrl_box_assembly = trimesh.util.concatenate([
    control_box, rex_bezel, rex_display, switch, switch_rocker,
    timer_bezel, timer_display, ssr
])

# Position controller box on the tray, to the right of the oven
ctrl_box_x = mesh_outer_r + 35 + box_width/2  # Right of oven with gap
ctrl_box_z = housing_bottom_z - leg_height + box_height/2  # Sitting on tray
ctrl_box_assembly.apply_translation([ctrl_box_x, 0, ctrl_box_z])

# =============================================================================
# WIRING CONDUIT - From oven to controller box
# =============================================================================
print("Building wiring conduit...")

conduit_r = 6  # Conduit outer radius
conduit_inner_r = 4.5  # Inner radius (hollow)
wire_r = 1.5  # Individual wire radius

# Wire exit point on oven (at wire_hole_angle, bottom of housing)
wire_exit_angle_rad = np.radians(wire_hole_angle)
wire_exit_x = air_gap_mid_r * np.cos(wire_exit_angle_rad)
wire_exit_y = air_gap_mid_r * np.sin(wire_exit_angle_rad)
wire_exit_z = housing_bottom_z

# Controller box connection point (left side of box, near bottom)
ctrl_conn_x = ctrl_box_x - box_width/2
ctrl_conn_y = 0
ctrl_conn_z = housing_bottom_z - leg_height + 10  # Just above tray

# Create conduit path - from oven exit down to tray, across to controller box
conduit_parts = []
conduit_color = [60, 60, 65, 255]

# 1. Vertical drop from oven exit to tray level
drop_height = abs(wire_exit_z - ctrl_conn_z)
vert_conduit = trimesh.creation.cylinder(radius=conduit_r, height=drop_height, sections=24)
vert_conduit.apply_translation([wire_exit_x, wire_exit_y, wire_exit_z - drop_height/2])
vert_conduit.visual.face_colors = conduit_color
conduit_parts.append(vert_conduit)

# Elbow at bottom of vertical drop
elbow1 = trimesh.creation.icosphere(radius=conduit_r, subdivisions=2)
elbow1.apply_translation([wire_exit_x, wire_exit_y, ctrl_conn_z])
elbow1.visual.face_colors = conduit_color
conduit_parts.append(elbow1)

# 2. Straight run from oven exit to controller box (angled across tray)
dx = ctrl_conn_x - wire_exit_x
dy = ctrl_conn_y - wire_exit_y
run_length = np.sqrt(dx**2 + dy**2)
run_angle = np.arctan2(dy, dx)
horiz_conduit = trimesh.creation.cylinder(radius=conduit_r, height=run_length, sections=24)
# Rotate from Z-axis to horizontal, then aim toward controller
horiz_conduit.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
horiz_conduit.apply_transform(trimesh.transformations.rotation_matrix(run_angle, [0, 0, 1]))
horiz_conduit.apply_translation([wire_exit_x + dx/2, wire_exit_y + dy/2, ctrl_conn_z])
horiz_conduit.visual.face_colors = conduit_color
conduit_parts.append(horiz_conduit)

# Elbow at controller box
elbow2 = trimesh.creation.icosphere(radius=conduit_r, subdivisions=2)
elbow2.apply_translation([ctrl_conn_x, ctrl_conn_y, ctrl_conn_z])
elbow2.visual.face_colors = conduit_color
conduit_parts.append(elbow2)

# 3. Short vertical piece up into controller box
final_vert = trimesh.creation.cylinder(radius=conduit_r, height=15, sections=24)
final_vert.apply_translation([ctrl_conn_x, ctrl_conn_y, ctrl_conn_z + 7.5])
final_vert.visual.face_colors = conduit_color
conduit_parts.append(final_vert)

wiring_conduit = trimesh.util.concatenate(conduit_parts)
print(f"  Conduit from oven ({wire_exit_x:.0f}, {wire_exit_y:.0f}) to controller ({ctrl_conn_x:.0f}, {ctrl_conn_y:.0f})")

# =============================================================================
# STEEL PLATFORM / TRAY WITH LIP
# =============================================================================
print("Building steel platform tray...")

platform_z = housing_bottom_z - leg_height

tray_left_edge = -mesh_outer_r - 25
tray_right_edge = mesh_outer_r + 35 + 160 + 20
tray_front_edge = -100/2 - 20
tray_back_edge = 100/2 + 20

platform_length = tray_right_edge - tray_left_edge
platform_width = max(mesh_outer_r * 2 + 50, tray_back_edge - tray_front_edge)
platform_thickness = 3
lip_height_tray = 12
lip_thickness = 2

platform_center_x = (tray_left_edge + tray_right_edge) / 2

platform_base = trimesh.creation.box(extents=[platform_length, platform_width, platform_thickness])
platform_base.apply_translation([platform_center_x, 0, platform_z - platform_thickness/2])
platform_base.visual.face_colors = [140, 145, 150, 255]

platform_parts = [platform_base]

lip_front_top = trimesh.creation.box(extents=[platform_length, lip_thickness, lip_height_tray])
lip_front_top.apply_translation([platform_center_x, -platform_width/2 + lip_thickness/2, platform_z + lip_height_tray/2])
lip_front_top.visual.face_colors = [140, 145, 150, 255]
platform_parts.append(lip_front_top)

lip_back_top = trimesh.creation.box(extents=[platform_length, lip_thickness, lip_height_tray])
lip_back_top.apply_translation([platform_center_x, platform_width/2 - lip_thickness/2, platform_z + lip_height_tray/2])
lip_back_top.visual.face_colors = [140, 145, 150, 255]
platform_parts.append(lip_back_top)

lip_left_top = trimesh.creation.box(extents=[lip_thickness, platform_width - lip_thickness*2, lip_height_tray])
lip_left_top.apply_translation([tray_left_edge + lip_thickness/2, 0, platform_z + lip_height_tray/2])
lip_left_top.visual.face_colors = [140, 145, 150, 255]
platform_parts.append(lip_left_top)

lip_right_top = trimesh.creation.box(extents=[lip_thickness, platform_width - lip_thickness*2, lip_height_tray])
lip_right_top.apply_translation([tray_right_edge - lip_thickness/2, 0, platform_z + lip_height_tray/2])
lip_right_top.visual.face_colors = [140, 145, 150, 255]
platform_parts.append(lip_right_top)

lip_front_bot = trimesh.creation.box(extents=[platform_length, lip_thickness, lip_height_tray])
lip_front_bot.apply_translation([platform_center_x, -platform_width/2 + lip_thickness/2, platform_z - platform_thickness - lip_height_tray/2])
lip_front_bot.visual.face_colors = [140, 145, 150, 255]
platform_parts.append(lip_front_bot)

lip_back_bot = trimesh.creation.box(extents=[platform_length, lip_thickness, lip_height_tray])
lip_back_bot.apply_translation([platform_center_x, platform_width/2 - lip_thickness/2, platform_z - platform_thickness - lip_height_tray/2])
lip_back_bot.visual.face_colors = [140, 145, 150, 255]
platform_parts.append(lip_back_bot)

lip_left_bot = trimesh.creation.box(extents=[lip_thickness, platform_width - lip_thickness*2, lip_height_tray])
lip_left_bot.apply_translation([tray_left_edge + lip_thickness/2, 0, platform_z - platform_thickness - lip_height_tray/2])
lip_left_bot.visual.face_colors = [140, 145, 150, 255]
platform_parts.append(lip_left_bot)

lip_right_bot = trimesh.creation.box(extents=[lip_thickness, platform_width - lip_thickness*2, lip_height_tray])
lip_right_bot.apply_translation([tray_right_edge - lip_thickness/2, 0, platform_z - platform_thickness - lip_height_tray/2])
lip_right_bot.visual.face_colors = [140, 145, 150, 255]
platform_parts.append(lip_right_bot)

# Combine platform parts first
platform_solid = trimesh.util.concatenate(platform_parts)

# Cut small screw holes in the tray for leg attachment
print("  Adding screw holes to tray for legs...")
screw_hole_radius = 3.3  # M6 clearance hole (6.6mm diameter)
for angle_deg in leg_angles:
    angle_rad = np.radians(angle_deg)
    hole_x = leg_hole_r * np.cos(angle_rad)
    hole_y = leg_hole_r * np.sin(angle_rad)
    # Create small cylinder for screw hole
    screw_hole = trimesh.creation.cylinder(radius=screw_hole_radius, height=platform_thickness + 10, sections=16)
    screw_hole.apply_translation([hole_x, hole_y, platform_z - platform_thickness/2])
    # Boolean difference to cut hole
    try:
        platform_solid = platform_solid.difference(screw_hole, engine='manifold')
    except:
        pass  # Skip if boolean fails

platform = platform_solid
platform.visual.face_colors = [140, 145, 150, 255]

# =============================================================================
# LEG MOUNTING SCREWS - Visible screws attaching legs to tray
# =============================================================================
print("Building M6 x 40mm leg mounting bolts...")
# Real M6 hex bolt dimensions
m6_head_across_flats = 10   # mm
m6_head_r = m6_head_across_flats / 2 / np.cos(np.pi/6)  # circumradius for hex
m6_head_h = 4               # mm
m6_shaft_r = 3.0            # 6mm diameter shaft
m6_shaft_h = 40             # 40mm bolt length
m6_washer_od = 12           # mm
m6_washer_r = m6_washer_od / 2
m6_washer_h = 1.6           # mm
m6_nut_across_flats = 10    # mm
m6_nut_r = m6_nut_across_flats / 2 / np.cos(np.pi/6)  # circumradius for hex
m6_nut_h = 5                # mm

bolt_color = [80, 80, 85, 255]

leg_screws = []
for angle_deg in leg_angles:
    angle_rad = np.radians(angle_deg)
    bolt_x = leg_hole_r * np.cos(angle_rad)
    bolt_y = leg_hole_r * np.sin(angle_rad)
    # Bolt head sits on top of bottom cap (inside housing)
    head_bottom_z = housing_bottom_z + sheet_metal_thickness
    head_center_z = head_bottom_z + m6_head_h / 2

    # Hex head (6 sides)
    hex_head = trimesh.creation.cylinder(radius=m6_head_r, height=m6_head_h, sections=6)
    hex_head.apply_translation([bolt_x, bolt_y, head_center_z])
    hex_head.visual.face_colors = bolt_color
    leg_screws.append(hex_head)

    # Shaft goes down from bottom of head through all layers
    shaft_center_z = head_bottom_z - m6_shaft_h / 2
    shaft = trimesh.creation.cylinder(radius=m6_shaft_r, height=m6_shaft_h, sections=24)
    shaft.apply_translation([bolt_x, bolt_y, shaft_center_z])
    shaft.visual.face_colors = bolt_color
    leg_screws.append(shaft)

    # Washer under tray
    washer_center_z = platform_z - platform_thickness - m6_washer_h / 2
    washer = trimesh.creation.cylinder(radius=m6_washer_r, height=m6_washer_h, sections=32)
    washer.apply_translation([bolt_x, bolt_y, washer_center_z])
    washer.visual.face_colors = [160, 165, 170, 255]
    leg_screws.append(washer)

    # Hex nut under washer
    nut_center_z = washer_center_z - m6_washer_h / 2 - m6_nut_h / 2
    nut = trimesh.creation.cylinder(radius=m6_nut_r, height=m6_nut_h, sections=6)
    nut.apply_translation([bolt_x, bolt_y, nut_center_z])
    nut.visual.face_colors = bolt_color
    leg_screws.append(nut)

leg_screws_combined = trimesh.util.concatenate(leg_screws)
print(f"  3x M6 x 40mm hex bolts at angles: {leg_angles}")

# (2026-06-10) M4 cap fastener screws DELETED — both caps now fasten with the
# existing M6 spacer-ring bolts (long pattern). No separate cap screws exist.

# =============================================================================
# ALL PARTS BUILT - Now concatenate feet into single mesh
# =============================================================================
print()
print("=" * 70)
print("ALL GEOMETRY BUILT - Starting export...")
print("=" * 70)

feet_combined = trimesh.util.concatenate(feet)
feet_combined.visual.face_colors = ceramic_body_color

# =============================================================================
# PARTS MANIFEST
# =============================================================================
parts = [
    ("01_Base_Body",        base_body),
    ("02_Bottom_Cap",       bottom_cap),
    ("04a_Cap_Shell",       cap_shell),
    ("04b_Cap_HoldDown_Ring", hold_down_ring),
    ("04_Lid_Assembly",     lid_assembly),
    ("05_Hinge_Pin",        hinge_pin),
    ("05b_Lid_Hinge_Strap", lid_hinge_strap),
    ("06_Ceramic_Cylinder", ceramic_cylinder),
    ("07_Ceramic_Base_Disk", ceramic_base),
    ("07b_Ceramic_Lid_Disk", ceramic_lid),
    ("08_Kanthal_Coil",     kanthal_coil),
    ("09_Thermocouple",     thermocouple),
    ("10_Ceramic_Feet",     feet_combined),
    ("11_Controller_Box",   ctrl_box_assembly),
    ("12_Steel_Tray",       platform),
    ("13_Wiring_Conduit",   wiring_conduit),
    ("14_Leg_Screws",       leg_screws_combined),
]

# =============================================================================
# EXPORT EACH PART
# =============================================================================
print()
export_results = []

for part_name, mesh in parts:
    print(f"Exporting {part_name}...")

    # Fix normals before export
    mesh.fix_normals()

    # STL (binary)
    stl_path = os.path.join(stl_dir, f"{part_name}.stl")
    mesh.export(stl_path, file_type='stl')

    # GLB (binary glTF - trimesh handles this natively)
    glb_path = os.path.join(glb_dir, f"{part_name}.glb")
    mesh.export(glb_path, file_type='glb')

    # Collect stats
    bounds = mesh.bounds
    extents = bounds[1] - bounds[0]
    export_results.append({
        'name': part_name,
        'vertices': len(mesh.vertices),
        'faces': len(mesh.faces),
        'x_mm': extents[0],
        'y_mm': extents[1],
        'z_mm': extents[2],
    })

    print(f"  -> STL: {os.path.getsize(stl_path) / 1024:.1f} KB")
    print(f"  -> GLB: {os.path.getsize(glb_path) / 1024:.1f} KB")

# =============================================================================
# COMPLETE ASSEMBLY (all parts combined)
# =============================================================================
print()
print("Building complete assembly...")

all_meshes = [m for _, m in parts]
complete_assembly = trimesh.util.concatenate(all_meshes)
complete_assembly.fix_normals()

assembly_name = "00_Complete_Assembly"
stl_path = os.path.join(stl_dir, f"{assembly_name}.stl")
glb_path = os.path.join(glb_dir, f"{assembly_name}.glb")

complete_assembly.export(stl_path, file_type='stl')
complete_assembly.export(glb_path, file_type='glb')

bounds = complete_assembly.bounds
extents = bounds[1] - bounds[0]
export_results.insert(0, {
    'name': assembly_name,
    'vertices': len(complete_assembly.vertices),
    'faces': len(complete_assembly.faces),
    'x_mm': extents[0],
    'y_mm': extents[1],
    'z_mm': extents[2],
})

print(f"  -> STL: {os.path.getsize(stl_path) / 1024:.1f} KB")
print(f"  -> GLB: {os.path.getsize(glb_path) / 1024:.1f} KB")

# =============================================================================
# COPY / VERIFY CERAMIC STL FILES
# =============================================================================
print()
print("=" * 70)
print("CERAMIC STL VERIFICATION")
print("=" * 70)

# Source ceramic STLs live in Ceramic Parts/ folder

# Verify ceramic cylinder dimensions
print()
print("Ceramic Cylinder verification:")
cyl_bounds = ceramic_cylinder.bounds
cyl_extents = cyl_bounds[1] - cyl_bounds[0]
print(f"  Bounding box: X={cyl_extents[0]:.1f}mm  Y={cyl_extents[1]:.1f}mm  Z={cyl_extents[2]:.1f}mm")
print(f"  Expected: ~{outer_diameter}mm OD, ~{inner_diameter}mm ID, ~{cylinder_height}mm height")

# Check OD (max X or Y extent should be ~92.5)
cyl_od = max(cyl_extents[0], cyl_extents[1])
cyl_height_actual = cyl_extents[2]
od_ok = abs(cyl_od - outer_diameter) < 2.0
h_ok = abs(cyl_height_actual - cylinder_height) < 2.0
print(f"  OD measured: {cyl_od:.1f}mm {'OK' if od_ok else 'MISMATCH!'}")
print(f"  Height measured: {cyl_height_actual:.1f}mm {'OK' if h_ok else 'MISMATCH!'}")

# Verify ceramic disk dimensions
print()
print("Ceramic Disk verification:")
disk_bounds = ceramic_base.bounds
disk_extents = disk_bounds[1] - disk_bounds[0]
print(f"  Bounding box: X={disk_extents[0]:.1f}mm  Y={disk_extents[1]:.1f}mm  Z={disk_extents[2]:.1f}mm")
print(f"  Expected: ~{outer_diameter}mm diameter, ~{disk_thickness}mm thick")

disk_dia = max(disk_extents[0], disk_extents[1])
disk_thick_actual = disk_extents[2]
dia_ok = abs(disk_dia - outer_diameter) < 2.0
thick_ok = abs(disk_thick_actual - disk_thickness) < 2.0
print(f"  Diameter measured: {disk_dia:.1f}mm {'OK' if dia_ok else 'MISMATCH!'}")
print(f"  Thickness measured: {disk_thick_actual:.1f}mm {'OK' if thick_ok else 'MISMATCH!'}")

# =============================================================================
# SUMMARY TABLE
# =============================================================================
print()
print("=" * 100)
print("EXPORT MANIFEST")
print("=" * 100)
print(f"{'Part Name':<30} {'Vertices':>10} {'Faces':>10} {'X (mm)':>10} {'Y (mm)':>10} {'Z (mm)':>10}")
print("-" * 100)

for r in export_results:
    print(f"{r['name']:<30} {r['vertices']:>10,} {r['faces']:>10,} {r['x_mm']:>10.1f} {r['y_mm']:>10.1f} {r['z_mm']:>10.1f}")

print("-" * 100)

total_files = (len(parts) + 1) * 2  # +1 for complete assembly, x2 formats
print(f"\nTotal files exported: {total_files}")
print(f"Output directories:")
print(f"  STL: {stl_dir}")
print(f"  GLB: {glb_dir}")
print()
print("DONE!")
