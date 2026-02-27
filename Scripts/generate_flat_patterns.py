"""
GENERATE FLAT PATTERNS - Glass Heat Station
Creates DXF and SVG flat patterns for laser cutting all sheet metal parts.

DXF Layer Convention:
  CUT        (Red/1)     - Outer profile / through-cuts
  HOLE       (Green/3)   - Holes (bolt, wire, vent perforations)
  BEND       (Yellow/2)  - Bend lines (fold up/down)
  LABEL      (Cyan/4)    - Part name, material, dimensions text
  CENTERLINE (Magenta/6) - Center marks, alignment references

Requires: pip install ezdxf

Run from the Scripts/ directory:
    python generate_flat_patterns.py
"""
import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import math
import os
import sys

# =============================================================================
# OUTPUT DIRECTORIES
# =============================================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
cad_exports_dir = os.path.join(project_dir, "CAD Exports")
flat_base = os.path.join(cad_exports_dir, "Flat Patterns")
dxf_dir = os.path.join(flat_base, "DXF")
svg_dir = os.path.join(flat_base, "SVG")

for d in [dxf_dir, svg_dir]:
    os.makedirs(d, exist_ok=True)

# =============================================================================
# DIMENSIONS (from export_all_parts.py)
# =============================================================================
cylinder_height = 91
disk_thickness = 5.5
disk_body_h = 4.5
disk_lip_h = 1.0
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
hole_diameter = 6.4
hole_bottom_height = 5
hole_center_height = hole_bottom_height + hole_diameter / 2

slot_2_end_angle = slot_positions[2] + (slot_width * scale_factor / 2 / circumference * 360)
gap_between_3_and_4 = gaps[2]
groove_seam_angle = slot_2_end_angle + (gap_between_3_and_4 * scale_factor / 2 / circumference * 360)

slot_3_end_angle = slot_positions[3] + (slot_width * scale_factor / 2 / circumference * 360)
hole_position_angle = slot_3_end_angle + (108.68 * (2 / 3) / circumference * 360)

lip_z = -(disk_thickness + sheet_metal_thickness)
ring_wall_top_z = hole_bottom_height - 2
housing_bottom_z = lip_z - 25
housing_top_z = cylinder_height

slot_arc_half_deg = (slot_width / 2) / ceramic_outer_r * (180 / math.pi)

# Leg/bolt params
leg_hole_r = housing_inner_r - 5
bolt_hole_size = 6.6
leg_angles = [40, 160, 280]

# Wire/TC hole params
wire_hole_angle = groove_seam_angle
wire_hole_diameter = 8
tc_cable_hole_angle = hole_position_angle

# Cap/bottom params
perf_mid_r = (mesh_inner_r + mesh_outer_r) / 2
perf_n_ang = int((2 * math.pi * perf_mid_r) / perf_spacing)
air_gap_mid_r = housing_outer_r + air_gap / 2
bottom_cap_outer_r = mesh_outer_r + 1.5
cap_outer_r = mesh_outer_r + 1.5
bottom_cap_lip_height = 10
lip_drop = 10
ceramic_grab_lip = 3
ridge_drop = 5

# Screw tab params
screw_hole_r = 2.25  # M4 clearance hole (4.5mm diameter per ISO 273)
tab_width = 15
tab_depth = 12

# Bottom cap tab angles (same calculation as export script)
slot_arc_half_deg_scaled = (slot_width * scale_factor / 2 / circumference * 360)
bottom_cap_tab_angles = []
for i in range(3):
    slot_end = slot_positions[i] + slot_arc_half_deg_scaled
    next_slot_start = slot_positions[i + 1] - slot_arc_half_deg_scaled
    mid_angle = (slot_end + next_slot_start) / 2
    bottom_cap_tab_angles.append(mid_angle)

slot_3_end = slot_positions[3] + slot_arc_half_deg_scaled
slot_0_start = slot_positions[0] - slot_arc_half_deg_scaled + 360
large_gap_arc_deg = gaps[3] * scale_factor / circumference * 360
hinge_center = slot_3_end + large_gap_arc_deg / 2
if hinge_center >= 360:
    hinge_center -= 360
flange_4 = (slot_3_end + hinge_center) / 2
if flange_4 >= 360:
    flange_4 -= 360
bottom_cap_tab_angles.append(flange_4)
flange_5 = (hinge_center + slot_0_start) / 2
if flange_5 >= 360:
    flange_5 -= 360
bottom_cap_tab_angles.append(flange_5)

# Lid params
lid_height = 35
lid_ring_inner_r = ceramic_outer_r - 10
lid_wall_height = disk_body_h - sheet_metal_thickness  # 3.3mm flush
lid_vent_inner_r = housing_outer_r
lid_vent_outer_r = mesh_outer_r

# Tray params
tray_left_edge = -mesh_outer_r - 25
tray_right_edge = mesh_outer_r + 35 + 160 + 20
tray_front_edge = -100 / 2 - 20
tray_back_edge = 100 / 2 + 20
platform_length = tray_right_edge - tray_left_edge
platform_width = max(mesh_outer_r * 2 + 50, tray_back_edge - tray_front_edge)
platform_thickness = 3
lip_height_tray = 12
lip_thickness = 2

# Mesh height
mesh_height = housing_top_z - housing_bottom_z

# =============================================================================
# DXF LAYER SETUP
# =============================================================================
LAYER_COLORS = {
    "CUT": 1,         # Red
    "HOLE": 3,        # Green
    "BEND": 2,        # Yellow
    "LABEL": 4,       # Cyan
    "CENTERLINE": 6,  # Magenta
}


def setup_layers(doc):
    """Add standard layers with colors to a DXF document."""
    for name, color in LAYER_COLORS.items():
        doc.layers.add(name, color=color)
        if name == "BEND":
            doc.layers.get(name).dxf.linetype = "DASHED"


def new_dxf():
    """Create a new DXF document with standard layers."""
    doc = ezdxf.new("R2010")
    # Add DASHED linetype if not present
    if "DASHED" not in doc.linetypes:
        doc.linetypes.add("DASHED", pattern=[0.5, 0.25, -0.25])
    setup_layers(doc)
    return doc


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def unroll_cylinder(outer_r, height):
    """Returns (width, height) for unrolled cylinder."""
    return (2 * math.pi * outer_r, height)


def angle_to_x(angle_deg, outer_r):
    """Map angular position to X on unrolled flat pattern."""
    return math.radians(angle_deg) * outer_r


def add_circle_hole(msp, cx, cy, radius, layer="HOLE"):
    """Add a circular hole to modelspace."""
    msp.add_circle((cx, cy), radius, dxfattribs={"layer": layer})


def add_rect(msp, x, y, w, h, layer="CUT"):
    """Add a rectangle outline (4 lines)."""
    pts = [
        (x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)
    ]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})


def add_bend_line(msp, x1, y1, x2, y2, label=""):
    """Add a dashed bend line with optional label."""
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "BEND"})
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        msp.add_text(
            label, height=2.5,
            dxfattribs={"layer": "LABEL", "insert": (mid_x, mid_y + 3)}
        )


def add_label(msp, x, y, text, height=3):
    """Add a text label."""
    msp.add_text(text, height=height, dxfattribs={
        "layer": "LABEL",
        "insert": (x, y),
    })


def add_centerline(msp, x1, y1, x2, y2):
    """Add a centerline mark."""
    msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "CENTERLINE"})


def add_crosshair(msp, cx, cy, size=3):
    """Add a center crosshair mark."""
    add_centerline(msp, cx - size, cy, cx + size, cy)
    add_centerline(msp, cx, cy - size, cx, cy + size)


def add_notes_block(msp, x, y, thickness=1.2):
    """Add fabrication notes block to flat pattern."""
    bend_r = thickness  # 1\u00d7T inside bend radius
    notes = [
        "NOTES:",
        "1. All dimensions in mm",
        "2. Deburr all edges and holes",
        f"3. Bend radii per callout (R{bend_r:.1f} unless noted)",
        "4. Grain direction parallel to longest dimension",
        "5. All holes \u00b10.1mm",
    ]
    line_spacing = 5
    for i, line in enumerate(notes):
        h = 3 if i == 0 else 2.5
        add_label(msp, x, y - i * line_spacing, line, h)


def add_grain_arrow(msp, x, y, length=30, vertical=False):
    """Add grain direction arrow on LABEL layer."""
    if vertical:
        msp.add_line((x, y), (x, y + length), dxfattribs={"layer": "LABEL"})
        msp.add_line((x, y + length), (x - 2, y + length - 4), dxfattribs={"layer": "LABEL"})
        msp.add_line((x, y + length), (x + 2, y + length - 4), dxfattribs={"layer": "LABEL"})
        add_label(msp, x + 3, y + length / 2, "GRAIN", 2.5)
    else:
        msp.add_line((x, y), (x + length, y), dxfattribs={"layer": "LABEL"})
        msp.add_line((x + length, y), (x + length - 4, y + 2), dxfattribs={"layer": "LABEL"})
        msp.add_line((x + length, y), (x + length - 4, y - 2), dxfattribs={"layer": "LABEL"})
        add_label(msp, x + length / 2 - 5, y + 3, "GRAIN", 2.5)


def add_bend_relief(msp, x, y, thickness=1.2, horizontal=True):
    """Add rectangular bend relief cut at bend-edge intersection.
    Relief: width = 2\u00d7T, depth = T+1mm."""
    w = 2 * thickness
    d = thickness + 1.0
    if horizontal:
        add_rect(msp, x - w / 2, y, w, d, "CUT")
    else:
        add_rect(msp, x, y - w / 2, d, w, "CUT")


def save_dxf(doc, filename):
    """Save DXF and export SVG."""
    dxf_path = os.path.join(dxf_dir, filename)
    doc.saveas(dxf_path)
    print(f"  DXF: {dxf_path}")

    # SVG export via matplotlib
    svg_filename = filename.replace(".dxf", ".svg")
    svg_path = os.path.join(svg_dir, svg_filename)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        out = MatplotlibBackend(ax)
        Frontend(ctx, out).draw_layout(doc.modelspace())
        fig.savefig(svg_path, format="svg")
        plt.close(fig)
        print(f"  SVG: {svg_path}")
    except Exception as e:
        print(f"  SVG export failed: {e}")

    return dxf_path


def get_slot_z_offset(angle_deg):
    """Calculate how deep a slot cuts at the given angle."""
    half_w = slot_width / 2
    straight_h = slot_depth - half_w
    for slot_center in slot_positions:
        diff = abs(angle_deg - slot_center)
        if diff > 180:
            diff = 360 - diff
        if diff <= slot_arc_half_deg:
            t = 1.0 - (diff / slot_arc_half_deg)
            return straight_h + half_w * math.sqrt(max(0, t * (2 - t)))
    return 0


# =============================================================================
# PATTERN 1: Inner Housing Wall (01A_Inner_Housing_Flat.dxf)
# =============================================================================
def generate_inner_housing():
    """Unrolled inner housing cylinder with slot cutouts and wire holes."""
    print("\nPattern 1: Inner Housing Wall")
    doc = new_dxf()
    msp = doc.modelspace()

    width, height = unroll_cylinder(housing_outer_r, mesh_height)
    print(f"  Unrolled: {width:.1f} x {height:.1f} mm")

    # Outer rectangle with slot cutouts at top edge
    # Build the top edge profile with slot notches
    top_profile = []
    n_points = 720
    for i in range(n_points + 1):
        x = (i / n_points) * width
        ang = (x / width) * 360
        z_off = get_slot_z_offset(ang)
        top_profile.append((x, height - z_off))

    # Bottom edge
    bottom_pts = [(width, 0), (0, 0)]

    # Build closed profile: top (left to right) + right side + bottom (right to left) + left side
    profile = top_profile + [(width, 0), (0, 0)]
    msp.add_lwpolyline(profile, close=True, dxfattribs={"layer": "CUT"})

    # Wire exit holes (2x 8mm dia)
    wire_x = angle_to_x(wire_hole_angle, housing_outer_r)
    wire_top_y = groove_start_height - housing_bottom_z
    wire_bot_y = groove_end_height - housing_bottom_z
    add_circle_hole(msp, wire_x, wire_top_y, wire_hole_diameter / 2)
    add_circle_hole(msp, wire_x, wire_bot_y, wire_hole_diameter / 2)
    add_crosshair(msp, wire_x, wire_top_y)
    add_crosshair(msp, wire_x, wire_bot_y)

    # TC cable hole (1x 6mm dia)
    # The TC cable hole uses a 5mm radius in the 3D model's housing_holes
    tc_x = angle_to_x(tc_cable_hole_angle, housing_outer_r)
    tc_y = hole_center_height - housing_bottom_z
    add_circle_hole(msp, tc_x, tc_y, 5)
    add_crosshair(msp, tc_x, tc_y)

    # Labels
    add_label(msp, 5, -10, "01A INNER HOUSING WALL", 5)
    add_label(msp, 5, -18, "Material: 304 Stainless Steel, 1.2mm", 3)
    add_label(msp, 5, -24, "Inside Bend Radius: 1.2mm (1\u00d7T)", 3)
    add_label(msp, 5, -30, "K-Factor: 0.44", 3)
    add_label(msp, 5, -36, f"Flat: {width:.1f} x {height:.1f} mm", 3)
    add_label(msp, 5, -42, f"Rolls into cylinder, R={housing_inner_r:.2f}mm inner", 3)
    add_notes_block(msp, 5, -55)
    add_grain_arrow(msp, width / 2, -10, length=40, vertical=False)

    save_dxf(doc, "01A_Inner_Housing_Flat.dxf")


# =============================================================================
# PATTERN 2: Outer Perforated Mesh (01B_Outer_Mesh_Flat.dxf)
# =============================================================================
def generate_outer_mesh():
    """Unrolled outer mesh cylinder with perforations and slot cutouts."""
    print("\nPattern 2: Outer Perforated Mesh")
    doc = new_dxf()
    msp = doc.modelspace()

    width, height = unroll_cylinder(mesh_outer_r, mesh_height)
    print(f"  Unrolled: {width:.1f} x {height:.1f} mm")

    # Top edge profile with slot cutouts (same slots, mapped to mesh radius)
    top_profile = []
    n_points = 720
    for i in range(n_points + 1):
        x = (i / n_points) * width
        ang = (x / width) * 360
        # Use mesh radius for slot mapping
        z_off = 0
        half_w = slot_width / 2
        straight_h = slot_depth - half_w
        for slot_center in slot_positions:
            diff = abs(ang - slot_center)
            if diff > 180:
                diff = 360 - diff
            arc_dist = diff * (math.pi / 180) * mesh_inner_r
            if arc_dist <= half_w:
                z_from_top = straight_h + half_w * math.sqrt(
                    max(0, 1 - (arc_dist / half_w) ** 2))
                z_off = max(z_off, z_from_top)
        top_profile.append((x, height - z_off))

    profile = top_profile + [(width, 0), (0, 0)]
    msp.add_lwpolyline(profile, close=True, dxfattribs={"layer": "CUT"})

    # Perforation holes (staggered grid)
    perf_n_z = int((mesh_height - 10) / perf_spacing)
    hole_count = 0
    for zi in range(perf_n_z):
        y = 5 + zi * perf_spacing
        offset = (perf_spacing / 2) if (zi % 2) else 0
        for ai in range(perf_n_ang):
            x = (ai / perf_n_ang) * width + offset * (width / (2 * math.pi * perf_mid_r))
            if x > width:
                x -= width
            # Skip holes in slot areas
            ang = (x / width) * 360
            in_slot = False
            for slot_center in slot_positions:
                diff = abs(ang - slot_center)
                if diff > 180:
                    diff = 360 - diff
                arc_dist = diff * (math.pi / 180) * mesh_inner_r
                z_from_top = height - y
                if arc_dist <= slot_width / 2 and z_from_top <= slot_depth:
                    in_slot = True
                    break
            if not in_slot and 0 < x < width and 0 < y < height:
                add_circle_hole(msp, x, y, perf_hole_r)
                hole_count += 1

    print(f"  {hole_count} perforation holes")

    # Labels
    add_label(msp, 5, -10, "01B OUTER PERFORATED MESH", 5)
    add_label(msp, 5, -18, "Material: 304 Stainless Steel, 1.2mm", 3)
    add_label(msp, 5, -24, "Inside Bend Radius: 1.2mm (1\u00d7T)", 3)
    add_label(msp, 5, -30, "K-Factor: 0.44", 3)
    add_label(msp, 5, -36, f"Flat: {width:.1f} x {height:.1f} mm", 3)
    add_label(msp, 5, -42, f"Rolls into cylinder, R={mesh_inner_r:.2f}mm inner", 3)
    add_notes_block(msp, 5, -55)
    add_grain_arrow(msp, width / 2, -10, length=40, vertical=False)

    save_dxf(doc, "01B_Outer_Mesh_Flat.dxf")


# =============================================================================
# PATTERN 3: Bottom Cap (02_Bottom_Cap_Flat.dxf)
# =============================================================================
def generate_bottom_cap():
    """Bottom cap: disk with holes + outer lip strip + screw flanges."""
    print("\nPattern 3: Bottom Cap")
    doc = new_dxf()
    msp = doc.modelspace()

    # --- Main disk (centered at origin) ---
    msp.add_circle((0, 0), bottom_cap_outer_r, dxfattribs={"layer": "CUT"})
    add_crosshair(msp, 0, 0, 5)

    # M6 leg holes
    for ang_deg in leg_angles:
        hx = leg_hole_r * math.cos(math.radians(ang_deg))
        hy = leg_hole_r * math.sin(math.radians(ang_deg))
        add_circle_hole(msp, hx, hy, bolt_hole_size / 2)
        add_crosshair(msp, hx, hy)

    # Wire holes
    wh_x = air_gap_mid_r * math.cos(math.radians(wire_hole_angle))
    wh_y = air_gap_mid_r * math.sin(math.radians(wire_hole_angle))
    add_circle_hole(msp, wh_x, wh_y, 4)
    add_crosshair(msp, wh_x, wh_y)

    wh2_x = air_gap_mid_r * math.cos(math.radians(wire_hole_angle + 5))
    wh2_y = air_gap_mid_r * math.sin(math.radians(wire_hole_angle + 5))
    add_circle_hole(msp, wh2_x, wh2_y, 4)
    add_crosshair(msp, wh2_x, wh2_y)

    # TC cable hole
    tc_x = air_gap_mid_r * math.cos(math.radians(tc_cable_hole_angle))
    tc_y = air_gap_mid_r * math.sin(math.radians(tc_cable_hole_angle))
    add_circle_hole(msp, tc_x, tc_y, 3)
    add_crosshair(msp, tc_x, tc_y)

    # --- Outer lip strip (placed below disk) ---
    lip_y_offset = -(bottom_cap_outer_r + 20)
    lip_circ = 2 * math.pi * (bottom_cap_outer_r - sheet_metal_thickness / 2)
    add_rect(msp, 0, lip_y_offset, lip_circ, bottom_cap_lip_height, "CUT")
    add_bend_line(msp, 0, lip_y_offset, lip_circ, lip_y_offset, "BEND UP 90\u00b0")
    add_label(msp, lip_circ / 2 - 30, lip_y_offset + bottom_cap_lip_height + 3,
              f"OUTER LIP - {lip_circ:.1f} x {bottom_cap_lip_height} mm", 2.5)
    # Bend reliefs at lip strip ends
    add_bend_relief(msp, 0, lip_y_offset, sheet_metal_thickness, horizontal=False)
    add_bend_relief(msp, lip_circ, lip_y_offset, sheet_metal_thickness, horizontal=False)

    # --- 5x screw flanges (placed below lip strip) ---
    flange_y_offset = lip_y_offset - 30
    for idx, ang_deg in enumerate(bottom_cap_tab_angles):
        fx = idx * (tab_width + 10)
        fy = flange_y_offset
        add_rect(msp, fx, fy, tab_width, tab_depth, "CUT")
        add_bend_line(msp, fx, fy + tab_depth, fx + tab_width, fy + tab_depth,
                      "BEND 90\u00b0")
        # M4 screw hole at center
        add_circle_hole(msp, fx + tab_width / 2, fy + tab_depth / 2, screw_hole_r)
        add_crosshair(msp, fx + tab_width / 2, fy + tab_depth / 2, 2)
        add_label(msp, fx + 1, fy - 4, f"Flange {idx + 1} ({ang_deg:.0f}\u00b0)", 2)
        # Bend reliefs at flange bend line ends
        add_bend_relief(msp, fx, fy + tab_depth, sheet_metal_thickness, horizontal=True)
        add_bend_relief(msp, fx + tab_width, fy + tab_depth, sheet_metal_thickness, horizontal=True)

    # Labels
    add_label(msp, -bottom_cap_outer_r, -(bottom_cap_outer_r + 8),
              "02 BOTTOM CAP", 5)
    add_label(msp, -bottom_cap_outer_r, -(bottom_cap_outer_r + 16),
              "Material: 304 Stainless Steel, 1.2mm", 3)
    add_label(msp, -bottom_cap_outer_r, -(bottom_cap_outer_r + 22),
              "Inside Bend Radius: 1.2mm (1\u00d7T)", 3)
    add_label(msp, -bottom_cap_outer_r, -(bottom_cap_outer_r + 28),
              "K-Factor: 0.44", 3)
    add_label(msp, -bottom_cap_outer_r, -(bottom_cap_outer_r + 34),
              f"Disk OD: {2 * bottom_cap_outer_r:.1f} mm", 3)
    add_notes_block(msp, -bottom_cap_outer_r, -(bottom_cap_outer_r + 47))
    add_grain_arrow(msp, -bottom_cap_outer_r + 20, -(bottom_cap_outer_r + 2), length=40, vertical=False)

    save_dxf(doc, "02_Bottom_Cap_Flat.dxf")


# =============================================================================
# PATTERN 4: Top Cap (03_Top_Cap_Flat.dxf)
# =============================================================================
def generate_top_cap():
    """Top cap: annular disk with vent holes + outer lip + grab lip + ridge + flanges."""
    print("\nPattern 4: Top Cap")
    doc = new_dxf()
    msp = doc.modelspace()

    # --- Annular disk (centered at origin) ---
    msp.add_circle((0, 0), cap_outer_r, dxfattribs={"layer": "CUT"})
    msp.add_circle((0, 0), ceramic_inner_r, dxfattribs={"layer": "CUT"})
    add_crosshair(msp, 0, 0, 5)

    # Ventilation holes in vent zones
    cap_vent_inner_r = housing_outer_r
    cap_vent_outer_r = cap_outer_r
    cap_hole_spacing = perf_spacing * 0.8
    cap_vent_width = cap_vent_outer_r - cap_vent_inner_r
    n_radial_rows = max(1, int(cap_vent_width / cap_hole_spacing))
    cap_row_spacing = cap_vent_width / (n_radial_rows + 1)

    slot_buffer_deg = 4.0 / ceramic_outer_r * (180 / math.pi)
    flange_buffer_deg = 4.0 / cap_outer_r * (180 / math.pi)

    hole_count = 0
    for r_row in range(n_radial_rows):
        r_pos = cap_vent_inner_r + cap_row_spacing * (r_row + 1)
        offset_ang = (cap_hole_spacing / 2 / r_pos) * (180 / math.pi) if (r_row % 2) else 0

        for gap_idx in range(4):
            next_idx = (gap_idx + 1) % 4
            gap_start = slot_positions[gap_idx] + slot_arc_half_deg + slot_buffer_deg
            gap_end = slot_positions[next_idx] - slot_arc_half_deg - slot_buffer_deg
            if gap_end < gap_start:
                gap_end += 360

            gap_arc_mm = (gap_end - gap_start) * (math.pi / 180) * r_pos
            n_holes = max(1, int(gap_arc_mm / cap_hole_spacing))

            for hi in range(n_holes):
                ang = gap_start + (hi + 0.5) * (gap_end - gap_start) / n_holes + offset_ang
                if ang >= 360:
                    ang -= 360
                # Check flange clearance
                clear = True
                for fa in bottom_cap_tab_angles:
                    diff = abs(ang - fa)
                    if diff > 180:
                        diff = 360 - diff
                    if diff < flange_buffer_deg:
                        clear = False
                        break
                if clear:
                    hx = r_pos * math.cos(math.radians(ang))
                    hy = r_pos * math.sin(math.radians(ang))
                    add_circle_hole(msp, hx, hy, perf_hole_r)
                    hole_count += 1

    print(f"  {hole_count} ventilation holes")

    # --- Outer lip strip ---
    lip_y_offset = -(cap_outer_r + 20)
    lip_circ = 2 * math.pi * (cap_outer_r - sheet_metal_thickness / 2)
    add_rect(msp, 0, lip_y_offset, lip_circ, lip_drop, "CUT")
    add_bend_line(msp, 0, lip_y_offset + lip_drop, lip_circ, lip_y_offset + lip_drop,
                  "BEND DOWN 90\u00b0")
    add_label(msp, lip_circ / 2 - 30, lip_y_offset - 5,
              f"OUTER LIP - {lip_circ:.1f} x {lip_drop} mm", 2.5)
    # Bend reliefs at outer lip strip ends
    add_bend_relief(msp, 0, lip_y_offset, sheet_metal_thickness, horizontal=False)
    add_bend_relief(msp, lip_circ, lip_y_offset, sheet_metal_thickness, horizontal=False)

    # --- Inner grab lip strip ---
    grab_y_offset = lip_y_offset - 25
    grab_circ = 2 * math.pi * (ceramic_inner_r + sheet_metal_thickness / 2)
    add_rect(msp, 0, grab_y_offset, grab_circ, ceramic_grab_lip, "CUT")
    add_bend_line(msp, 0, grab_y_offset + ceramic_grab_lip,
                  grab_circ, grab_y_offset + ceramic_grab_lip, "BEND DOWN 90\u00b0")
    add_label(msp, grab_circ / 2 - 30, grab_y_offset - 5,
              f"INNER GRAB LIP - {grab_circ:.1f} x {ceramic_grab_lip} mm", 2.5)
    # Bend reliefs at inner grab lip strip ends
    add_bend_relief(msp, 0, grab_y_offset, sheet_metal_thickness, horizontal=False)
    add_bend_relief(msp, grab_circ, grab_y_offset, sheet_metal_thickness, horizontal=False)

    # --- Chamber ridge strip ---
    ridge_y_offset = grab_y_offset - 20
    ridge_circ = 2 * math.pi * (housing_inner_r - sheet_metal_thickness / 2)
    add_rect(msp, 0, ridge_y_offset, ridge_circ, ridge_drop, "CUT")
    add_bend_line(msp, 0, ridge_y_offset + ridge_drop,
                  ridge_circ, ridge_y_offset + ridge_drop, "BEND DOWN 90\u00b0")
    add_label(msp, ridge_circ / 2 - 30, ridge_y_offset - 5,
              f"CHAMBER RIDGE - {ridge_circ:.1f} x {ridge_drop} mm", 2.5)
    # Bend reliefs at chamber ridge strip ends
    add_bend_relief(msp, 0, ridge_y_offset, sheet_metal_thickness, horizontal=False)
    add_bend_relief(msp, ridge_circ, ridge_y_offset, sheet_metal_thickness, horizontal=False)

    # --- 5x screw flanges ---
    flange_y_offset = ridge_y_offset - 30
    for idx, ang_deg in enumerate(bottom_cap_tab_angles):
        fx = idx * (tab_width + 10)
        fy = flange_y_offset
        add_rect(msp, fx, fy, tab_width, tab_depth, "CUT")
        add_bend_line(msp, fx, fy + tab_depth, fx + tab_width, fy + tab_depth,
                      "BEND 90\u00b0")
        add_circle_hole(msp, fx + tab_width / 2, fy + tab_depth / 2, screw_hole_r)
        add_crosshair(msp, fx + tab_width / 2, fy + tab_depth / 2, 2)
        add_label(msp, fx + 1, fy - 4, f"Flange {idx + 1} ({ang_deg:.0f}\u00b0)", 2)
        # Bend reliefs at flange bend line ends
        add_bend_relief(msp, fx, fy + tab_depth, sheet_metal_thickness, horizontal=True)
        add_bend_relief(msp, fx + tab_width, fy + tab_depth, sheet_metal_thickness, horizontal=True)

    # Labels
    add_label(msp, -cap_outer_r, cap_outer_r + 8, "03 TOP CAP", 5)
    add_label(msp, -cap_outer_r, cap_outer_r + 3,
              "Material: 304 Stainless Steel, 1.2mm", 3)
    add_label(msp, -cap_outer_r, cap_outer_r - 3,
              "Inside Bend Radius: 1.2mm (1\u00d7T)", 3)
    add_label(msp, -cap_outer_r, cap_outer_r - 9,
              "K-Factor: 0.44", 3)
    add_label(msp, -cap_outer_r, cap_outer_r - 15,
              f"Annulus: ID={2 * ceramic_inner_r:.1f}, OD={2 * cap_outer_r:.1f} mm", 3)
    add_notes_block(msp, -cap_outer_r, cap_outer_r - 28)
    add_grain_arrow(msp, -cap_outer_r + 20, cap_outer_r + 14, length=40, vertical=False)

    save_dxf(doc, "03_Top_Cap_Flat.dxf")


# =============================================================================
# PATTERN 5: Support Ring (01C_Support_Ring_Flat.dxf)
# =============================================================================
def generate_support_ring():
    """Support ring: annular shelf + retaining wall strip."""
    print("\nPattern 5: Support Ring")
    doc = new_dxf()
    msp = doc.modelspace()

    l_ring_inner_r = ceramic_outer_r - 10
    ring_wall_r = ceramic_outer_r + sheet_metal_thickness / 2
    wall_bottom = lip_z + sheet_metal_thickness
    wall_height = ring_wall_top_z - wall_bottom

    # --- Annular disk ---
    msp.add_circle((0, 0), housing_inner_r, dxfattribs={"layer": "CUT"})
    msp.add_circle((0, 0), l_ring_inner_r, dxfattribs={"layer": "CUT"})
    add_crosshair(msp, 0, 0, 5)

    # --- Retaining wall strip ---
    wall_y_offset = -(housing_inner_r + 15)
    wall_circ = 2 * math.pi * ring_wall_r
    add_rect(msp, 0, wall_y_offset, wall_circ, wall_height, "CUT")
    add_bend_line(msp, 0, wall_y_offset + wall_height,
                  wall_circ, wall_y_offset + wall_height, "BEND UP 90\u00b0")
    add_label(msp, wall_circ / 2 - 30, wall_y_offset - 5,
              f"RETAINING WALL - {wall_circ:.1f} x {wall_height:.1f} mm", 2.5)
    # Bend reliefs at retaining wall strip ends
    add_bend_relief(msp, 0, wall_y_offset, sheet_metal_thickness, horizontal=False)
    add_bend_relief(msp, wall_circ, wall_y_offset, sheet_metal_thickness, horizontal=False)

    # Labels
    add_label(msp, -housing_inner_r, housing_inner_r + 8,
              "01C SUPPORT RING", 5)
    add_label(msp, -housing_inner_r, housing_inner_r + 3,
              "Material: 304 Stainless Steel, 1.2mm", 3)
    add_label(msp, -housing_inner_r, housing_inner_r - 3,
              "Inside Bend Radius: 1.2mm (1\u00d7T)", 3)
    add_label(msp, -housing_inner_r, housing_inner_r - 9,
              "K-Factor: 0.44", 3)
    add_label(msp, -housing_inner_r, housing_inner_r - 15,
              f"Annulus: ID={2 * l_ring_inner_r:.1f}, OD={2 * housing_inner_r:.1f} mm", 3)
    add_notes_block(msp, -housing_inner_r, housing_inner_r - 28)
    add_grain_arrow(msp, -housing_inner_r + 20, housing_inner_r + 14, length=40, vertical=False)

    save_dxf(doc, "01C_Support_Ring_Flat.dxf")


# =============================================================================
# PATTERN 6: Steel Tray (12_Steel_Tray_Flat.dxf)
# =============================================================================
def generate_steel_tray():
    """Steel tray: flat base rectangle with lip tabs and leg holes."""
    print("\nPattern 6: Steel Tray")
    doc = new_dxf()
    msp = doc.modelspace()

    # Base rectangle
    add_rect(msp, 0, 0, platform_length, platform_width, "CUT")

    # Center of tray = where oven sits
    oven_cx = -tray_left_edge  # offset from left edge to X=0
    oven_cy = platform_width / 2

    # M6 leg holes
    for ang_deg in leg_angles:
        hx = oven_cx + leg_hole_r * math.cos(math.radians(ang_deg))
        hy = oven_cy + leg_hole_r * math.sin(math.radians(ang_deg))
        add_circle_hole(msp, hx, hy, bolt_hole_size / 2)
        add_crosshair(msp, hx, hy)

    # Lip tabs - top edge (bend up)
    n_tabs_long = 4
    tab_len = (platform_length - (n_tabs_long + 1) * 5) / n_tabs_long
    for i in range(n_tabs_long):
        tx = 5 + i * (tab_len + 5)
        ty = platform_width
        add_rect(msp, tx, ty, tab_len, lip_height_tray, "CUT")
        add_bend_line(msp, tx, ty, tx + tab_len, ty, "BEND UP")

    # Lip tabs - bottom edge (bend down)
    for i in range(n_tabs_long):
        tx = 5 + i * (tab_len + 5)
        ty = -lip_height_tray
        add_rect(msp, tx, ty, tab_len, lip_height_tray, "CUT")
        add_bend_line(msp, tx, ty + lip_height_tray, tx + tab_len, ty + lip_height_tray,
                      "BEND DOWN")

    # Lip tabs - left edge (bend up)
    n_tabs_short = 2
    tab_len_s = (platform_width - (n_tabs_short + 1) * 5) / n_tabs_short
    for i in range(n_tabs_short):
        tx = -lip_height_tray
        ty = 5 + i * (tab_len_s + 5)
        add_rect(msp, tx, ty, lip_height_tray, tab_len_s, "CUT")
        add_bend_line(msp, 0, ty, 0, ty + tab_len_s, "BEND UP")

    # Lip tabs - right edge (bend down)
    for i in range(n_tabs_short):
        tx = platform_length
        ty = 5 + i * (tab_len_s + 5)
        add_rect(msp, tx, ty, lip_height_tray, tab_len_s, "CUT")
        add_bend_line(msp, tx, ty, tx, ty + tab_len_s, "BEND DOWN")

    # Corner relief notches (small squares at corners)
    notch_size = lip_height_tray
    corners = [
        (0, 0),
        (platform_length, 0),
        (0, platform_width),
        (platform_length, platform_width),
    ]
    for i, (cx, cy) in enumerate(corners):
        nx = cx - notch_size if cx > 0 else cx
        ny = cy - notch_size if cy > 0 else cy
        add_rect(msp, nx, ny, notch_size, notch_size, "CUT")
        add_label(msp, nx + 1, ny + notch_size / 2, f"CORNER RELIEF {i + 1}", 1.5)

    # Labels
    add_label(msp, 10, -lip_height_tray - 12, "12 STEEL TRAY", 5)
    add_label(msp, 10, -lip_height_tray - 20,
              "Material: 304 Stainless Steel, 3.0mm", 3)
    add_label(msp, 10, -lip_height_tray - 26,
              "Inside Bend Radius: 3.0mm (1\u00d7T)", 3)
    add_label(msp, 10, -lip_height_tray - 32,
              "K-Factor: 0.44", 3)
    add_label(msp, 10, -lip_height_tray - 38,
              f"Flat: {platform_length:.1f} x {platform_width:.1f} mm", 3)
    add_label(msp, 10, -lip_height_tray - 44,
              f"Lip height: {lip_height_tray} mm (top: bend up, bottom: bend down)", 3)
    add_notes_block(msp, 10, -lip_height_tray - 57, thickness=3.0)
    add_grain_arrow(msp, platform_length / 2 - 20, -lip_height_tray - 6, length=40, vertical=False)

    save_dxf(doc, "12_Steel_Tray_Flat.dxf")


# =============================================================================
# PATTERN 7: Lid Parts (04_Lid_Flat_Patterns.dxf) — multiple shapes
# =============================================================================
def generate_lid_patterns():
    """All lid flat patterns in one DXF file, spaced apart."""
    print("\nPattern 7: Lid Parts (combined)")
    doc = new_dxf()
    msp = doc.modelspace()

    y_cursor = 0  # Track vertical placement

    # --- Lid inner cylinder ---
    lid_inner_w, lid_inner_h = unroll_cylinder(housing_outer_r, lid_height)
    add_rect(msp, 0, y_cursor, lid_inner_w, lid_inner_h, "CUT")
    add_label(msp, 5, y_cursor + lid_inner_h + 3,
              f"LID INNER CYLINDER - {lid_inner_w:.1f} x {lid_inner_h} mm", 3)
    add_label(msp, 5, y_cursor - 6,
              f"Rolls to R={housing_inner_r:.2f}mm inner", 2.5)
    y_cursor += lid_inner_h + 25

    # --- Lid outer mesh ---
    lid_outer_w, lid_outer_h = unroll_cylinder(mesh_outer_r, lid_height)
    add_rect(msp, 0, y_cursor, lid_outer_w, lid_outer_h, "CUT")

    # Perforation holes on lid outer mesh
    lid_perf_n_z = int((lid_height - 10) / perf_spacing)
    hole_count = 0
    for zi in range(lid_perf_n_z):
        y = y_cursor + 5 + zi * perf_spacing
        offset = (perf_spacing / 2) if (zi % 2) else 0
        for ai in range(perf_n_ang):
            x = (ai / perf_n_ang) * lid_outer_w + offset * (
                lid_outer_w / (2 * math.pi * perf_mid_r))
            if x > lid_outer_w:
                x -= lid_outer_w
            if 0 < x < lid_outer_w and y_cursor < y < y_cursor + lid_outer_h:
                add_circle_hole(msp, x, y, perf_hole_r)
                hole_count += 1

    add_label(msp, 5, y_cursor + lid_outer_h + 3,
              f"LID OUTER MESH - {lid_outer_w:.1f} x {lid_outer_h} mm ({hole_count} perf holes)", 3)
    add_label(msp, 5, y_cursor - 6,
              f"Rolls to R={mesh_inner_r:.2f}mm inner", 2.5)
    y_cursor += lid_outer_h + 25

    # --- Lid bottom ring (annular with perf holes) ---
    ring_cx = mesh_outer_r + 10
    ring_cy = y_cursor + mesh_outer_r + 5
    msp.add_circle((ring_cx, ring_cy), mesh_outer_r, dxfattribs={"layer": "CUT"})
    msp.add_circle((ring_cx, ring_cy), ceramic_outer_r, dxfattribs={"layer": "CUT"})
    add_crosshair(msp, ring_cx, ring_cy, 5)

    # Perf holes on bottom ring
    lid_vent_mid_r = (lid_vent_inner_r + lid_vent_outer_r) / 2
    lid_bperf_n_ang = int((2 * math.pi * lid_vent_mid_r) / perf_spacing)
    ring_holes = 0
    for r_row in range(-1, 2):
        r_pos = lid_vent_mid_r + r_row * perf_spacing
        if r_pos < lid_vent_inner_r + 2 or r_pos > lid_vent_outer_r - 2:
            continue
        offset = (perf_spacing / 2) if (r_row % 2) else 0
        for ai in range(lid_bperf_n_ang):
            ang = (ai / lid_bperf_n_ang) * 360 + (offset / lid_vent_mid_r) * (180 / math.pi)
            hx = ring_cx + r_pos * math.cos(math.radians(ang))
            hy = ring_cy + r_pos * math.sin(math.radians(ang))
            add_circle_hole(msp, hx, hy, perf_hole_r)
            ring_holes += 1

    add_label(msp, ring_cx - mesh_outer_r, ring_cy + mesh_outer_r + 5,
              f"LID BOTTOM RING ({ring_holes} perf holes)", 3)
    add_label(msp, ring_cx - mesh_outer_r, ring_cy - mesh_outer_r - 8,
              f"ID={2 * ceramic_outer_r:.1f}, OD={2 * mesh_outer_r:.1f} mm", 2.5)
    y_cursor = ring_cy + mesh_outer_r + 20

    # --- Lid top disk (circle with perf holes + handle mount) ---
    disk_cx = mesh_outer_r + 10
    disk_cy = y_cursor + mesh_outer_r + 5
    msp.add_circle((disk_cx, disk_cy), mesh_outer_r, dxfattribs={"layer": "CUT"})
    add_crosshair(msp, disk_cx, disk_cy, 5)

    # Perf holes on top disk (same pattern as bottom ring)
    disk_holes = 0
    for r_row in range(-1, 2):
        r_pos = lid_vent_mid_r + r_row * perf_spacing
        if r_pos < lid_vent_inner_r + 2 or r_pos > lid_vent_outer_r - 2:
            continue
        offset = (perf_spacing / 2) if (r_row % 2) else 0
        for ai in range(lid_bperf_n_ang):
            ang = (ai / lid_bperf_n_ang) * 360 + (offset / lid_vent_mid_r) * (180 / math.pi)
            hx = disk_cx + r_pos * math.cos(math.radians(ang))
            hy = disk_cy + r_pos * math.sin(math.radians(ang))
            add_circle_hole(msp, hx, hy, perf_hole_r)
            disk_holes += 1

    # Handle mount holes (2 holes for handle posts, 50mm apart, offset 40mm toward opening)
    handle_width = 50
    handle_offset_dist = 40
    slot_4_end = slot_positions[3] + (slot_width * scale_factor / 2 / circumference * 360)
    large_gap_arc = gaps[3] * scale_factor / circumference * 360
    hinge_ang = slot_4_end + large_gap_arc / 2
    if hinge_ang >= 360:
        hinge_ang -= 360
    opposite_ang = math.radians(hinge_ang + 180)
    h_off_x = handle_offset_dist * math.cos(opposite_ang)
    h_off_y = handle_offset_dist * math.sin(opposite_ang)
    add_circle_hole(msp, disk_cx - handle_width / 2 + h_off_x, disk_cy + h_off_y, 4)
    add_circle_hole(msp, disk_cx + handle_width / 2 + h_off_x, disk_cy + h_off_y, 4)
    add_crosshair(msp, disk_cx - handle_width / 2 + h_off_x, disk_cy + h_off_y, 2)
    add_crosshair(msp, disk_cx + handle_width / 2 + h_off_x, disk_cy + h_off_y, 2)

    add_label(msp, disk_cx - mesh_outer_r, disk_cy + mesh_outer_r + 5,
              f"LID TOP DISK ({disk_holes} perf holes + handle mounts)", 3)
    add_label(msp, disk_cx - mesh_outer_r, disk_cy - mesh_outer_r - 8,
              f"OD={2 * mesh_outer_r:.1f} mm", 2.5)
    y_cursor = disk_cy + mesh_outer_r + 20

    # --- Lid retaining wall (strip) ---
    wall_circ = 2 * math.pi * (ceramic_outer_r + sheet_metal_thickness / 2)
    add_rect(msp, 0, y_cursor, wall_circ, lid_wall_height, "CUT")
    add_bend_line(msp, 0, y_cursor + lid_wall_height,
                  wall_circ, y_cursor + lid_wall_height, "BEND UP 90\u00b0")
    add_label(msp, 5, y_cursor + lid_wall_height + 3,
              f"LID RETAINING WALL - {wall_circ:.1f} x {lid_wall_height:.1f} mm", 3)
    # Bend reliefs at lid retaining wall strip ends
    add_bend_relief(msp, 0, y_cursor, sheet_metal_thickness, horizontal=False)
    add_bend_relief(msp, wall_circ, y_cursor, sheet_metal_thickness, horizontal=False)
    y_cursor += lid_wall_height + 20

    # --- Lid shelf (annular) ---
    shelf_cx = ceramic_outer_r + 10
    shelf_cy = y_cursor + ceramic_outer_r + 5
    msp.add_circle((shelf_cx, shelf_cy), ceramic_outer_r, dxfattribs={"layer": "CUT"})
    msp.add_circle((shelf_cx, shelf_cy), lid_ring_inner_r, dxfattribs={"layer": "CUT"})
    add_crosshair(msp, shelf_cx, shelf_cy, 5)

    add_label(msp, shelf_cx - ceramic_outer_r, shelf_cy + ceramic_outer_r + 5,
              f"LID SHELF", 3)
    add_label(msp, shelf_cx - ceramic_outer_r, shelf_cy - ceramic_outer_r - 8,
              f"ID={2 * lid_ring_inner_r:.1f}, OD={2 * ceramic_outer_r:.1f} mm", 2.5)

    # Overall label
    add_label(msp, 0, -15, "04 LID FLAT PATTERNS", 5)
    add_label(msp, 0, -23, "Material: 304 Stainless Steel, 1.2mm", 3)
    add_label(msp, 0, -29, "Inside Bend Radius: 1.2mm (1\u00d7T)", 3)
    add_label(msp, 0, -35, "K-Factor: 0.44", 3)
    add_label(msp, 0, -41, "All parts for lid assembly", 3)
    add_notes_block(msp, 0, -54)
    add_grain_arrow(msp, 120, -15, length=40, vertical=False)

    save_dxf(doc, "04_Lid_Flat_Patterns.dxf")


# =============================================================================
# MAIN
# =============================================================================
def main():
    print("=" * 70)
    print("GENERATE FLAT PATTERNS - Glass Heat Station")
    print("=" * 70)
    print(f"DXF output: {dxf_dir}")
    print(f"SVG output: {svg_dir}")

    generate_inner_housing()
    generate_outer_mesh()
    generate_bottom_cap()
    generate_top_cap()
    generate_support_ring()
    generate_steel_tray()
    generate_lid_patterns()

    # Summary
    print("\n" + "=" * 70)
    print("FLAT PATTERN SUMMARY")
    print("=" * 70)
    print(f"{'Pattern':<40} {'File':<35}")
    print("-" * 75)
    patterns = [
        ("Inner Housing Wall", "01A_Inner_Housing_Flat"),
        ("Outer Perforated Mesh", "01B_Outer_Mesh_Flat"),
        ("Support Ring", "01C_Support_Ring_Flat"),
        ("Bottom Cap", "02_Bottom_Cap_Flat"),
        ("Top Cap", "03_Top_Cap_Flat"),
        ("Lid Parts (combined)", "04_Lid_Flat_Patterns"),
        ("Steel Tray", "12_Steel_Tray_Flat"),
    ]
    for desc, fname in patterns:
        dxf_exists = os.path.exists(os.path.join(dxf_dir, f"{fname}.dxf"))
        svg_exists = os.path.exists(os.path.join(svg_dir, f"{fname}.svg"))
        status = ""
        if dxf_exists:
            status += "DXF"
        if svg_exists:
            status += "+SVG"
        print(f"  {desc:<38} {fname:<33} {status}")
    print("-" * 75)
    print("\nDONE!")


if __name__ == "__main__":
    main()
