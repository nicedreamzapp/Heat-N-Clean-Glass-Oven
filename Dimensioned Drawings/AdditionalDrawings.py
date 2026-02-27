"""
ADDITIONAL DIMENSIONED TECHNICAL DRAWINGS
- Sheet 3: Bottom Cap cross-section + top view
- Sheet 4: Lid Assembly cross-section + ceramic pocket detail
- Sheet 5: Complete Assembly Overview cross-section
Outputs PDF files for manufacturer spec sheets.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import math
import os

# Save to same directory as this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# ALL DIMENSIONS (matching CAD exactly — same as DimensionedDrawings.py)
# =============================================================================
# Ceramic
ceramic_od = 92.5
ceramic_id = 81.5
ceramic_outer_r = ceramic_od / 2   # 46.25
ceramic_inner_r = ceramic_id / 2   # 40.75
cylinder_height = 91
disk_thickness = 5.5

# Slots
slot_width = 10.5
slot_depth = 23.5
gaps = [46.25, 46.25, 46.25, 108.68]

circumference = math.pi * ceramic_od
scale_factor = circumference / (sum(gaps) + 4 * slot_width)

slot_positions = []
current_arc_position = 0
for i in range(4):
    center_arc = current_arc_position + (slot_width * scale_factor) / 2
    angle = (center_arc / circumference) * 360
    slot_positions.append(angle)
    current_arc_position += (slot_width + gaps[i]) * scale_factor

slot_arc_half_deg = (slot_width / 2) / ceramic_outer_r * (180 / np.pi)

# Housing
sheet_t = 1.2
insulation_gap = 24.6
housing_inner_r = ceramic_outer_r + insulation_gap  # 70.85
housing_outer_r = housing_inner_r + sheet_t          # 72.05

# Outer mesh
air_gap = 4
mesh_inner_r = housing_outer_r + air_gap   # 76.05
mesh_outer_r = mesh_inner_r + sheet_t       # 77.25

# Cap
cap_outer_r = mesh_outer_r + 1.5   # 64.15
cap_inner_r = ceramic_inner_r       # 40.75

# Heights
lip_z = -(disk_thickness + sheet_t)  # -6.7
housing_bottom_z = lip_z - 25       # -31.7
housing_top_z = cylinder_height      # 91

# Cap features
lip_drop = 10
ceramic_grab_lip = 3
chamber_ridge_drop = 5

# Perforations
perf_hole_r = 2
perf_spacing = 6

# Leg bolt holes
leg_hole_r = housing_inner_r - 5  # 65.85
bolt_hole_size = 6.6
leg_angles = [40, 160, 280]

# Support ring
l_ring_inner_r = ceramic_outer_r - 10  # 36.25
hole_bottom_height = 5
ring_wall_top_z = hole_bottom_height - 2  # 3mm

# Bottom cap
bottom_cap_outer_r = mesh_outer_r + 1.5  # 64.15 (same as top cap outer)
bottom_cap_lip_height = 10
bottom_cap_z = housing_bottom_z - sheet_t  # -32.9

# Round flange angles: 3 centered between the 3 smaller gaps, 2 in the large gap
bottom_cap_tab_angles = []
# First 3 flanges: centered between slots 0-1, 1-2, 2-3
for i in range(3):
    slot_end = slot_positions[i] + slot_arc_half_deg
    next_slot_start = slot_positions[i + 1] - slot_arc_half_deg
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

# Tab dimensions (from View_Assembled.py)
screw_hole_r = 2.5
tab_width = 15   # mm circumferential
tab_depth = 12   # mm radial

# Wire/TC hole angles
slot_2_end_angle = slot_positions[2] + (slot_width * scale_factor / 2 / circumference * 360)
gap_between_3_and_4 = gaps[2]
groove_seam_angle = slot_2_end_angle + (gap_between_3_and_4 * scale_factor / 2 / circumference * 360)
slot_3_end_angle = slot_positions[3] + (slot_width * scale_factor / 2 / circumference * 360)
hole_position_angle = slot_3_end_angle + (108.68 * (2 / 3) / circumference * 360)
wire_hole_diameter = 8
tc_hole_diameter = 6.4

# Lid
lid_height = 35
lid_bottom_z = housing_top_z  # 91
lid_top_z = lid_bottom_z + lid_height  # 126

# Handle
handle_height = 25
handle_width = 50  # distance between posts (center to center)
handle_bar_r = 4

# Ceramic disk pocket in lid
lid_ring_inner_r = ceramic_outer_r - 10  # 36.25
disk_body_h = 4.5       # body thickness (full OD portion)
disk_lip_h = 1.0        # lip thickness (reduced 76mm OD portion)
lip_od = 76.0
lip_r = lip_od / 2      # 38.0
lid_wall_height = disk_body_h - sheet_t  # 3.3mm — flush: body at lid base, only lip below

# Hinge
slot_4_end_angle = slot_positions[3] + (slot_width * scale_factor / 2 / circumference * 360)
large_gap_arc_deg = gaps[3] * scale_factor / circumference * 360
hinge_angle = slot_4_end_angle + large_gap_arc_deg / 2
if hinge_angle >= 360:
    hinge_angle -= 360

# Leg
leg_height = 25

# =============================================================================
# DRAWING HELPERS (same as DimensionedDrawings.py)
# =============================================================================
def dim_h(ax, y, x1, x2, text, offset=3, fontsize=7, color='blue'):
    """Horizontal dimension line with arrows."""
    yo = y + offset
    ax.annotate('', xy=(x1, yo), xytext=(x2, yo),
                arrowprops=dict(arrowstyle='<->', color=color, lw=0.8))
    ax.text((x1 + x2) / 2, yo + 1, text, ha='center', va='bottom',
            fontsize=fontsize, color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    # Extension lines
    ax.plot([x1, x1], [y, yo], color=color, lw=0.4, ls='--')
    ax.plot([x2, x2], [y, yo], color=color, lw=0.4, ls='--')

def dim_v(ax, x, y1, y2, text, offset=3, fontsize=7, color='blue'):
    """Vertical dimension line with arrows."""
    xo = x + offset
    ax.annotate('', xy=(xo, y1), xytext=(xo, y2),
                arrowprops=dict(arrowstyle='<->', color=color, lw=0.8))
    ax.text(xo + 1.5, (y1 + y2) / 2, text, ha='left', va='center',
            fontsize=fontsize, color=color, fontweight='bold', rotation=90,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.plot([x, xo], [y1, y1], color=color, lw=0.4, ls='--')
    ax.plot([x, xo], [y2, y2], color=color, lw=0.4, ls='--')

def leader(ax, x, y, tx, ty, text, fontsize=6.5, color='darkgreen'):
    """Leader line with callout text."""
    ax.annotate(text, xy=(x, y), xytext=(tx, ty),
                fontsize=fontsize, color=color, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=color, lw=0.6),
                bbox=dict(boxstyle='round,pad=0.2', fc='lightyellow', ec=color, lw=0.5))


def draw_title_block(fig, part_name, material="304 SS", thickness="1.2mm",
                     finish="#4 Brushed", scale_text="NOT TO SCALE",
                     rev="A", date="2026-02-25"):
    """Add a professional title block in lower-right of figure."""
    lines = [
        f"PART: {part_name}",
        f"MATERIAL: {material}",
        f"THICKNESS: {thickness}",
        f"FINISH: {finish}",
        f"SCALE: {scale_text}",
        "UNITS: mm",
        "PROJECTION: Third Angle",
        f"REV: {rev}    DATE: {date}",
    ]
    block_text = '\n'.join(lines)
    fig.text(0.98, 0.02, block_text, transform=fig.transFigure,
             fontsize=7, family='monospace', va='bottom', ha='right',
             bbox=dict(boxstyle='round,pad=0.4', fc='lightyellow', ec='black', lw=1.0))


def draw_tolerances_block(fig, has_bends=True):
    """Add general tolerances and units note to figure."""
    tol_text = (
        "GENERAL TOLERANCES (ISO 2768-m):\n"
        "  Linear: \u00b10.5mm\n"
        "  Angular: \u00b11\u00b0\n"
        "  Holes: \u00b10.1mm\n"
        "\n"
        "ALL DIMENSIONS IN MILLIMETERS"
    )
    if has_bends:
        tol_text += "\nAll bend radii R1.2mm (1\u00d7T) unless noted"
    fig.text(0.02, 0.02, tol_text, transform=fig.transFigure,
             fontsize=6, family='monospace', va='bottom', ha='left',
             bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='gray', lw=0.5))


def draw_bom_table(ax, x, y):
    """Draw Bill of Materials table on an axes."""
    bom = [
        ("Item", "Part", "Material", "Qty"),
        ("1", "Inner Housing", "304 SS 1.2mm", "1"),
        ("2", "Outer Mesh", "304 SS 1.2mm", "1"),
        ("3", "Support Ring", "304 SS 1.2mm", "1"),
        ("4", "Bottom Cap", "304 SS 1.2mm", "1"),
        ("5", "Top Cap", "304 SS 1.2mm", "1"),
        ("6", "Lid Assembly", "304 SS 1.2mm", "1"),
        ("7", "Steel Tray", "304 SS 3.0mm", "1"),
        ("8", "Hinge Pin", "304 SS rod 5mm", "1"),
        ("9", "Ceramic Cylinder", "Alumina", "1"),
        ("10", "Ceramic Disks", "Alumina", "2"),
        ("11", "M6\u00d740 Bolts", "Grade 8.8", "3"),
        ("12", "M4\u00d712 Screws", "A2 SS", "10"),
    ]
    row_h = 4.5
    col_widths = [12, 40, 38, 10]
    total_w = sum(col_widths)

    ax.text(x + total_w / 2, y + 3, "BILL OF MATERIALS",
            fontsize=8, fontweight='bold', ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='lightyellow', ec='black', lw=0.8))

    for row_idx, row in enumerate(bom):
        row_y = y - row_idx * row_h
        col_x = x
        weight = 'bold' if row_idx == 0 else 'normal'
        fs = 5.5 if row_idx == 0 else 5
        bg = '#E0E0E0' if row_idx == 0 else 'white'

        from matplotlib.patches import Rectangle
        ax.add_patch(Rectangle((x, row_y - row_h), total_w, row_h,
                               fill=True, fc=bg, ec='gray', lw=0.3))

        for col_idx, (cell, cw) in enumerate(zip(row, col_widths)):
            ax.text(col_x + cw / 2, row_y - row_h / 2, cell,
                    fontsize=fs, fontweight=weight,
                    ha='center', va='center', family='monospace')
            col_x += cw

    from matplotlib.patches import Rectangle as Rect
    table_h = len(bom) * row_h
    ax.add_patch(Rect((x, y - table_h), total_w, table_h,
                       fill=False, ec='black', lw=1.0))


# =============================================================================
# SHEET 3: BOTTOM CAP
# =============================================================================
fig3, (ax_bc_section, ax_bc_top) = plt.subplots(1, 2, figsize=(22, 12))
fig3.suptitle('BOTTOM CAP — DIMENSIONED DRAWING (Sheet 3)', fontsize=16, fontweight='bold', y=0.98)

# --- View A: Cross Section (side view, through one screw tab) ---
ax = ax_bc_section
ax.set_title('CROSS SECTION (through screw tab center)', fontsize=11, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-95, 95)
ax.set_ylim(-20, 25)
ax.grid(True, alpha=0.15)

# Reference: bottom cap disk sits at housing_bottom_z
# In the drawing we use a local coordinate where bottom of cap disk = 0
z_ref = 0  # bottom surface of bottom cap disk
cap_t = sheet_t  # 1.2mm

# Flat disk (cross section = full-width rectangle)
# The bottom cap spans from r=0 to bottom_cap_outer_r
# Show as full cross section (left-right)
ax.fill([-bottom_cap_outer_r, bottom_cap_outer_r, bottom_cap_outer_r, -bottom_cap_outer_r],
        [z_ref, z_ref, z_ref + cap_t, z_ref + cap_t],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')

# Outer lip going UP from top of disk
lip_bottom = z_ref + cap_t
lip_top = lip_bottom + bottom_cap_lip_height

# Left lip
ax.fill([-bottom_cap_outer_r, -bottom_cap_outer_r + cap_t,
         -bottom_cap_outer_r + cap_t, -bottom_cap_outer_r],
        [lip_bottom, lip_bottom, lip_top, lip_top],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')
# Right lip
ax.fill([bottom_cap_outer_r - cap_t, bottom_cap_outer_r,
         bottom_cap_outer_r, bottom_cap_outer_r - cap_t],
        [lip_bottom, lip_bottom, lip_top, lip_top],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')

# Screw tabs extending outward (show one on each side for the section)
tab_ext = tab_depth  # 12mm radial extension
tab_h = bottom_cap_lip_height  # tabs span full lip height

# Left tab
ax.fill([-bottom_cap_outer_r - tab_ext, -bottom_cap_outer_r,
         -bottom_cap_outer_r, -bottom_cap_outer_r - tab_ext],
        [lip_bottom, lip_bottom, lip_top, lip_top],
        color='#B0B0B0', ec='black', lw=1.0, hatch='xxx')
# Right tab
ax.fill([bottom_cap_outer_r, bottom_cap_outer_r + tab_ext,
         bottom_cap_outer_r + tab_ext, bottom_cap_outer_r],
        [lip_bottom, lip_bottom, lip_top, lip_top],
        color='#B0B0B0', ec='black', lw=1.0, hatch='xxx')

# Screw holes in tabs (shown as circles in section)
screw_cx_l = -bottom_cap_outer_r - tab_ext / 2
screw_cx_r = bottom_cap_outer_r + tab_ext / 2
screw_cy = (lip_bottom + lip_top) / 2
ax.add_patch(plt.Circle((screw_cx_l, screw_cy), screw_hole_r, fill=False, ec='red', lw=1.0))
ax.add_patch(plt.Circle((screw_cx_r, screw_cy), screw_hole_r, fill=False, ec='red', lw=1.0))

# Show wire exit holes as dashed circles in the disk (cut through)
wire_hole_r = wire_hole_diameter / 2  # 4mm
# Wire holes at air_gap_mid_r (approx 59.45mm)
air_gap_mid_r = housing_outer_r + air_gap / 2  # 59.45
# Show as breaks in the disk at +/- air_gap_mid_r
for sign in [-1, 1]:
    cx = sign * air_gap_mid_r
    ax.add_patch(plt.Circle((cx, z_ref + cap_t / 2), wire_hole_r,
                             fill=True, fc='white', ec='purple', lw=0.8, ls='--'))
    ax.text(cx, z_ref + cap_t / 2, f'{wire_hole_diameter}mm', fontsize=4,
            ha='center', va='center', color='purple')

# TC hole
tc_hole_r = tc_hole_diameter / 2  # 3.2mm
ax.add_patch(plt.Circle((0.7 * air_gap_mid_r, z_ref + cap_t / 2), tc_hole_r,
                         fill=True, fc='white', ec='purple', lw=0.8, ls='--'))
ax.text(0.7 * air_gap_mid_r, z_ref - 2.5, f'TC {tc_hole_diameter}mm', fontsize=4.5,
        ha='center', va='top', color='purple')

# Bolt holes (M6 at leg_hole_r) shown in section
for sign in [-1, 1]:
    bx = sign * leg_hole_r
    ax.add_patch(plt.Circle((bx, z_ref + cap_t / 2), bolt_hole_size / 2,
                             fill=True, fc='white', ec='darkblue', lw=0.8))
    ax.text(bx, z_ref - 2, 'M6', fontsize=4.5, ha='center', va='top', color='darkblue')

# Ghost outline of housing/mesh above (context)
for sign in [-1, 1]:
    # Housing wall
    ax.plot([sign * housing_inner_r, sign * housing_inner_r],
            [z_ref + cap_t, z_ref + 20], color='gray', lw=0.4, ls=':')
    ax.plot([sign * housing_outer_r, sign * housing_outer_r],
            [z_ref + cap_t, z_ref + 20], color='gray', lw=0.4, ls=':')
    # Mesh wall
    ax.plot([sign * mesh_inner_r, sign * mesh_inner_r],
            [z_ref + cap_t, z_ref + 20], color='gray', lw=0.4, ls=':')
    ax.plot([sign * mesh_outer_r, sign * mesh_outer_r],
            [z_ref + cap_t, z_ref + 20], color='gray', lw=0.4, ls=':')

# --- DIMENSIONS ---
# Overall diameter
dim_h(ax, z_ref, -bottom_cap_outer_r, bottom_cap_outer_r,
      f'OD {bottom_cap_outer_r * 2:.1f}mm', offset=-8)

# Mesh OD reference
dim_h(ax, z_ref, -mesh_outer_r, mesh_outer_r,
      f'Mesh OD {mesh_outer_r * 2:.1f}mm', offset=-14, fontsize=6, color='gray')

# Disk thickness
dim_v(ax, -bottom_cap_outer_r - tab_ext - 2, z_ref, z_ref + cap_t,
      f'{cap_t}mm\nsheet', offset=-8)

# Lip height
dim_v(ax, bottom_cap_outer_r, lip_bottom, lip_top,
      f'{bottom_cap_lip_height}mm\nlip', offset=4)

# Tab depth
dim_h(ax, lip_top, bottom_cap_outer_r, bottom_cap_outer_r + tab_ext,
      f'{tab_depth}mm tab', offset=3, fontsize=7)

# Tab width (annotated since we can't show in section)
leader(ax, bottom_cap_outer_r + tab_ext / 2, lip_top,
       bottom_cap_outer_r + tab_ext + 8, lip_top + 8,
       f'Round flange dia {tab_width}mm\n5x (3 between slots + 2 in gap)')

# Bolt circle
leader(ax, leg_hole_r, z_ref, leg_hole_r + 10, -10,
       f'Bolt circle R={leg_hole_r}mm\n3x M6 at 40/160/280 deg')

# Wire holes callout
leader(ax, air_gap_mid_r, z_ref + cap_t + 1, 75, 15,
       f'Wire exit holes\n2x dia {wire_hole_diameter}mm\nat R~{air_gap_mid_r:.1f}mm')

# Material callout
ax.text(-90, -17, 'MATERIAL: 304 Stainless Steel\nTHICKNESS: 1.2mm\nFINISH: #4 Brushed',
        fontsize=7, family='monospace', bbox=dict(boxstyle='round', fc='lightyellow', ec='gray'))

ax.set_xlabel('Radius (mm)', fontsize=8)
ax.set_ylabel('Height (mm)', fontsize=8)

# --- View B: Top View ---
ax = ax_bc_top
ax.set_title('BOTTOM VIEW (looking up)', fontsize=11, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-90, 90)
ax.set_ylim(-90, 90)
ax.grid(True, alpha=0.15)

# Main disk circle
disk_circle = plt.Circle((0, 0), bottom_cap_outer_r, fill=True, fc='#E0E0E0',
                          ec='black', lw=1.0)
ax.add_patch(disk_circle)

# Ghost circles for reference
for r, label, color, ls in [
    (mesh_outer_r, 'Mesh outer', '#999', ':'),
    (housing_outer_r, 'Housing outer', '#999', ':'),
    (housing_inner_r, 'Housing inner', '#999', ':'),
    (ceramic_outer_r, 'Ceramic outer', '#aa8866', '--'),
    (ceramic_inner_r, 'Ceramic inner', '#aa8866', '--'),
]:
    circle = plt.Circle((0, 0), r, fill=False, ec=color, lw=0.6, ls=ls)
    ax.add_patch(circle)

# 5 Round flanges
for i, ang_deg in enumerate(bottom_cap_tab_angles):
    ang_rad = np.radians(ang_deg)
    # Flange center at bottom_cap_outer_r + tab_depth/2 - 2
    flange_r = bottom_cap_outer_r + tab_depth / 2 - 2
    flange_cx = flange_r * np.cos(ang_rad)
    flange_cy = flange_r * np.sin(ang_rad)

    # Draw round flange as circle
    flange_circle = plt.Circle((flange_cx, flange_cy), tab_width / 2,
                                fill=True, fc='#B0B0B0', ec='black', lw=0.8, hatch='xxx')
    ax.add_patch(flange_circle)

    # Screw hole in flange
    hole_r_pos = bottom_cap_outer_r + tab_depth / 2 - 2
    sx = hole_r_pos * np.cos(ang_rad)
    sy = hole_r_pos * np.sin(ang_rad)
    ax.add_patch(plt.Circle((sx, sy), screw_hole_r, fill=False, ec='red', lw=0.8))

    # Label
    lx = (bottom_cap_outer_r + tab_depth + 3) * np.cos(ang_rad)
    ly = (bottom_cap_outer_r + tab_depth + 3) * np.sin(ang_rad)
    ax.text(lx, ly, f'F{i + 1}\n{ang_deg:.1f} deg', fontsize=5, ha='center', va='center',
            color='black', fontweight='bold')

# 3 Bolt holes (M6)
for ang_deg in leg_angles:
    ang_rad = np.radians(ang_deg)
    hx = leg_hole_r * np.cos(ang_rad)
    hy = leg_hole_r * np.sin(ang_rad)
    hole = plt.Circle((hx, hy), bolt_hole_size / 2, fill=True, fc='white', ec='darkblue', lw=1.0)
    ax.add_patch(hole)
    ax.text(hx, hy, f'M6\n{ang_deg} deg', fontsize=4.5, ha='center', va='center', color='darkblue')

# Wire exit holes
wire_hole_angles = [groove_seam_angle, groove_seam_angle + 5]
for i, wh_ang in enumerate(wire_hole_angles):
    wh_rad = np.radians(wh_ang)
    wx = air_gap_mid_r * np.cos(wh_rad)
    wy = air_gap_mid_r * np.sin(wh_rad)
    ax.add_patch(plt.Circle((wx, wy), wire_hole_diameter / 2, fill=True, fc='white',
                             ec='purple', lw=0.8))
    ax.text(wx, wy, f'W{i + 1}', fontsize=4, ha='center', va='center', color='purple')

# TC hole
tc_ang_rad = np.radians(hole_position_angle)
tcx = air_gap_mid_r * np.cos(tc_ang_rad)
tcy = air_gap_mid_r * np.sin(tc_ang_rad)
ax.add_patch(plt.Circle((tcx, tcy), tc_hole_diameter / 2, fill=True, fc='white',
                         ec='orange', lw=0.8))
ax.text(tcx, tcy, 'TC', fontsize=4, ha='center', va='center', color='orange')

# --- DIMENSIONS ---
# Overall diameter
dim_h(ax, -bottom_cap_outer_r - tab_depth, -bottom_cap_outer_r, bottom_cap_outer_r,
      f'OD {bottom_cap_outer_r * 2:.1f}mm', offset=-8)

# Bolt circle
bolt_circle = plt.Circle((0, 0), leg_hole_r, fill=False, ec='darkblue', lw=0.4, ls=':')
ax.add_patch(bolt_circle)
leader(ax, leg_hole_r * np.cos(np.radians(90)), leg_hole_r * np.sin(np.radians(90)) + 3,
       20, 82, f'Bolt circle R={leg_hole_r}mm\n3x M6 holes')

# Wire holes callout
leader(ax, wx, wy + 5, 50, 75,
       f'Wire exit holes\n2x dia {wire_hole_diameter}mm\nR={air_gap_mid_r:.1f}mm')

# TC hole callout
leader(ax, tcx, tcy, -55, -75,
       f'TC hole dia {tc_hole_diameter}mm\nR={air_gap_mid_r:.1f}mm')

# Tab callout
leader(ax, bottom_cap_outer_r + tab_depth / 2,
       bottom_cap_outer_r * np.sin(np.radians(bottom_cap_tab_angles[0])),
       78, 50, f'5x round flanges\ndia {tab_width}mm\nM5 screw holes')

ax.set_xlabel('X (mm)', fontsize=8)
ax.set_ylabel('Y (mm)', fontsize=8)

draw_title_block(fig3, "Bottom Cap", thickness="1.2mm")
draw_tolerances_block(fig3, has_bends=True)

fig3.tight_layout(rect=[0, 0.08, 1, 0.95])
fig3.savefig('BottomCap_Drawing.pdf', dpi=300, bbox_inches='tight')
print("Saved BottomCap_Drawing.pdf")

# =============================================================================
# SHEET 4: LID ASSEMBLY
# =============================================================================
fig4 = plt.figure(figsize=(24, 14))
fig4.suptitle('LID ASSEMBLY — DIMENSIONED DRAWING (Sheet 4)', fontsize=16, fontweight='bold', y=0.98)

# Left: full lid cross section. Right: ceramic pocket detail
ax_lid = fig4.add_axes([0.03, 0.06, 0.55, 0.88])
ax_det = fig4.add_axes([0.62, 0.06, 0.36, 0.88])

# ---- MAIN VIEW (full lid cross section) ----
ax = ax_lid
ax.set_title('Section B-B (through center)', fontsize=11, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-85, 85)
ax.set_ylim(-8, 65)
ax.grid(True, alpha=0.15)

# Local z: lid bottom at z=0 for this drawing
lid_z0 = 0  # = housing_top_z in global coords

# Inner housing wall (left + right)
for sign in [-1, 1]:
    ax.fill([sign * housing_inner_r, sign * housing_outer_r,
             sign * housing_outer_r, sign * housing_inner_r],
            [lid_z0, lid_z0, lid_z0 + lid_height, lid_z0 + lid_height],
            color='#C8CCD0', ec='black', lw=1.0, hatch='///')

# Outer perforated mesh (left + right)
for sign in [-1, 1]:
    ax.fill([sign * mesh_inner_r, sign * mesh_outer_r,
             sign * mesh_outer_r, sign * mesh_inner_r],
            [lid_z0, lid_z0, lid_z0 + lid_height, lid_z0 + lid_height],
            color='#D0D4D8', ec='black', lw=1.0, hatch='...')

# Bottom ring (perforated) — spans from ceramic_outer_r to mesh_outer_r
for sign in [-1, 1]:
    ax.fill([sign * ceramic_outer_r, sign * mesh_outer_r,
             sign * mesh_outer_r, sign * ceramic_outer_r],
            [lid_z0, lid_z0, lid_z0 + sheet_t, lid_z0 + sheet_t],
            color='#C8CCD0', ec='black', lw=0.8, hatch='///')

# Ceramic retaining wall at ceramic_outer_r (flush design — 3.3mm wall)
wall_bot = lid_z0 + sheet_t
wall_top = wall_bot + lid_wall_height  # sheet_t + 3.3
for sign in [-1, 1]:
    ax.fill([sign * ceramic_outer_r, sign * (ceramic_outer_r + sheet_t),
             sign * (ceramic_outer_r + sheet_t), sign * ceramic_outer_r],
            [wall_bot, wall_bot, wall_top, wall_top],
            color='#C8CCD0', ec='black', lw=1.0, hatch='///')

# Retaining shelf from lid_ring_inner_r to ceramic_outer_r (at top of wall)
shelf_z = wall_top
for sign in [-1, 1]:
    ax.fill([sign * lid_ring_inner_r, sign * ceramic_outer_r,
             sign * ceramic_outer_r, sign * lid_ring_inner_r],
            [shelf_z, shelf_z, shelf_z + sheet_t, shelf_z + sheet_t],
            color='#C8CCD0', ec='black', lw=0.8, hatch='///')

# Ceramic disk (flush — body at lid base, lip extends below)
# Body: full OD, from lid_z0 to lid_z0 + disk_body_h
ax.fill([-ceramic_outer_r, ceramic_outer_r, ceramic_outer_r, -ceramic_outer_r],
        [lid_z0, lid_z0, lid_z0 + disk_body_h, lid_z0 + disk_body_h],
        color='#F5EBD8', ec='#AA8866', lw=1.0, alpha=0.5)
# Lip: reduced OD, extends below lid base
ax.fill([-lip_r, lip_r, lip_r, -lip_r],
        [lid_z0 - disk_lip_h, lid_z0 - disk_lip_h, lid_z0, lid_z0],
        color='#EDE0C8', ec='#AA8866', lw=1.0, alpha=0.6)

# Top disk — solid from r=0 to mesh_outer_r at lid_z0 + lid_height
top_disk_z = lid_z0 + lid_height
ax.fill([-mesh_outer_r, mesh_outer_r, mesh_outer_r, -mesh_outer_r],
        [top_disk_z, top_disk_z, top_disk_z + sheet_t, top_disk_z + sheet_t],
        color='#C8CCD0', ec='black', lw=1.0, hatch='///')

# Handle: two posts + horizontal bar
handle_base_z = top_disk_z + sheet_t
post_spacing = handle_width  # 50mm apart center-to-center, but drawing shows 40mm between posts
# Actually from the CAD: handle_width = 50 (total), posts at +/- 25mm

# Left post
ax.fill([-handle_width / 2 - handle_bar_r, -handle_width / 2 + handle_bar_r,
         -handle_width / 2 + handle_bar_r, -handle_width / 2 - handle_bar_r],
        [handle_base_z, handle_base_z, handle_base_z + handle_height, handle_base_z + handle_height],
        color='#B0B0B0', ec='black', lw=1.0, hatch='///')
# Right post
ax.fill([handle_width / 2 - handle_bar_r, handle_width / 2 + handle_bar_r,
         handle_width / 2 + handle_bar_r, handle_width / 2 - handle_bar_r],
        [handle_base_z, handle_base_z, handle_base_z + handle_height, handle_base_z + handle_height],
        color='#B0B0B0', ec='black', lw=1.0, hatch='///')
# Horizontal bar
bar_z = handle_base_z + handle_height
ax.fill([-handle_width / 2 - handle_bar_r, handle_width / 2 + handle_bar_r,
         handle_width / 2 + handle_bar_r, -handle_width / 2 - handle_bar_r],
        [bar_z - handle_bar_r, bar_z - handle_bar_r, bar_z + handle_bar_r, bar_z + handle_bar_r],
        color='#B0B0B0', ec='black', lw=1.0, hatch='///')

# --- DIMENSIONS ---
# Overall outer diameter
dim_h(ax, top_disk_z + sheet_t, -mesh_outer_r, mesh_outer_r,
      f'Mesh OD {mesh_outer_r * 2:.1f}mm', offset=10)

# Housing radii
dim_h(ax, top_disk_z + sheet_t, -housing_outer_r, housing_outer_r,
      f'Housing OD {housing_outer_r * 2:.1f}mm', offset=5)

# Ceramic diameter
dim_h(ax, wall_bot, -ceramic_outer_r, ceramic_outer_r,
      f'Ceramic OD {ceramic_od}mm', offset=-5, color='brown')

# Lid height
dim_v(ax, mesh_outer_r, lid_z0, lid_z0 + lid_height,
      f'{lid_height}mm\nlid height', offset=6)

# Handle height
dim_v(ax, handle_width / 2 + handle_bar_r, handle_base_z, bar_z + handle_bar_r,
      f'{handle_height}mm\nhandle', offset=4)

# Handle width
dim_h(ax, bar_z + handle_bar_r, -handle_width / 2, handle_width / 2,
      f'{handle_width}mm handle spread', offset=5, fontsize=6)

# Post diameter
leader(ax, handle_width / 2, handle_base_z + handle_height / 2,
       handle_width / 2 + 15, handle_base_z + handle_height / 2 + 5,
       f'Post dia {handle_bar_r * 2}mm')

# Bar diameter
leader(ax, 0, bar_z + handle_bar_r,
       15, bar_z + handle_bar_r + 5,
       f'Bar dia {handle_bar_r * 2}mm')

# Wall height
dim_v(ax, -ceramic_outer_r, wall_bot, wall_top,
      f'{lid_wall_height}mm\nretaining\nwall', offset=-10, fontsize=6)

# Shelf callout
leader(ax, -lid_ring_inner_r, shelf_z + sheet_t / 2,
       -75, shelf_z + 8,
       f'Retaining shelf\nIR={lid_ring_inner_r}mm to OR={ceramic_outer_r}mm')

# Ceramic disk callout (flush design)
leader(ax, 0, lid_z0 + disk_body_h / 2,
       -40, lid_z0 + disk_body_h + 3,
       f'Body flush with lid base\n{ceramic_od}mm OD x {disk_body_h}mm', color='brown')
leader(ax, 0, lid_z0 - disk_lip_h / 2,
       -55, -5,
       f'Lip extends {disk_lip_h}mm below\n{lip_od}mm OD', color='#8B4513')

# Insulation gap
leader(ax, (ceramic_outer_r + housing_inner_r) / 2, lid_height / 2,
       75, lid_height / 2 + 8,
       f'Insulation gap\n{insulation_gap}mm')

# Air gap
leader(ax, (housing_outer_r + mesh_inner_r) / 2, lid_height / 2,
       78, lid_height / 2 - 2,
       f'Air gap\n{air_gap}mm')

# Sheet thickness
leader(ax, mesh_outer_r, lid_height * 0.3,
       78, lid_height * 0.3 - 5,
       f'Sheet t = {sheet_t}mm')

# Bottom ring callout
leader(ax, (ceramic_outer_r + mesh_outer_r) / 2, lid_z0 + sheet_t / 2,
       75, -2,
       f'Bottom ring (perf)\nCeramic OR to Mesh OR')

# Z reference
ax.text(mesh_outer_r + 2, lid_z0, f'z={housing_top_z} (body top)', fontsize=5, color='gray')
ax.text(mesh_outer_r + 2, lid_z0 + lid_height, f'z={lid_top_z} (lid top)', fontsize=5, color='gray')

# Material callout
ax.text(-82, -3.5, (
    'MATERIALS:\n'
    '  Metal: 304 SS, 1.2mm\n'
    '  Ceramic: High-alumina\n'
    '  Handle: 304 SS rod\n'
    f'  Perf: {perf_hole_r * 2}mm holes, {perf_spacing}mm spacing'
), fontsize=6.5, family='monospace',
   bbox=dict(boxstyle='round', fc='lightyellow', ec='gray'))

ax.set_xlabel('Radius (mm)', fontsize=8)
ax.set_ylabel('Height from lid base (mm)', fontsize=8)

# ---- DETAIL VIEW (zoomed ceramic pocket) ----
ax_det.set_title('DETAIL B — Ceramic Pocket (4x scale)', fontsize=11,
                 fontweight='bold', pad=10, color='red')
ax_det.set_aspect('equal')
ax_det.set_xlim(28, 72)
ax_det.set_ylim(-4, 10)
ax_det.grid(True, alpha=0.2)

# Detail callout circle on main view
detail_cx, detail_cy, detail_r = (lid_ring_inner_r + housing_inner_r) / 2, wall_bot + 3, 15
circle_call = plt.Circle((detail_cx, detail_cy), detail_r,
                          fill=False, ec='red', lw=1.5, ls='--')
ax_lid.add_patch(circle_call)
ax_lid.text(detail_cx + detail_r + 2, detail_cy + detail_r,
            'DETAIL B', fontsize=9, color='red', fontweight='bold')

# Redraw detail geometry (right half only)
# Bottom ring
ax_det.fill([ceramic_outer_r, mesh_outer_r, mesh_outer_r, ceramic_outer_r],
            [lid_z0, lid_z0, lid_z0 + sheet_t, lid_z0 + sheet_t],
            color='#C8CCD0', ec='black', lw=1.5, hatch='///')

# Retaining wall
ax_det.fill([ceramic_outer_r, ceramic_outer_r + sheet_t,
             ceramic_outer_r + sheet_t, ceramic_outer_r],
            [wall_bot, wall_bot, wall_top, wall_top],
            color='#A8B8C0', ec='black', lw=1.5, hatch='///')

# Shelf
ax_det.fill([lid_ring_inner_r, ceramic_outer_r,
             ceramic_outer_r, lid_ring_inner_r],
            [shelf_z, shelf_z, shelf_z + sheet_t, shelf_z + sheet_t],
            color='#A8B8C0', ec='black', lw=1.5, hatch='///')

# Ceramic body (flush with lid base)
ax_det.fill([lid_ring_inner_r + 1, ceramic_outer_r,
             ceramic_outer_r, lid_ring_inner_r + 1],
            [lid_z0, lid_z0, lid_z0 + disk_body_h, lid_z0 + disk_body_h],
            color='#F5EBD8', ec='#AA8866', lw=1.2, alpha=0.6)
# Ceramic lip (extends below)
ax_det.fill([lid_ring_inner_r + 1, lip_r,
             lip_r, lid_ring_inner_r + 1],
            [lid_z0 - disk_lip_h, lid_z0 - disk_lip_h, lid_z0, lid_z0],
            color='#EDE0C8', ec='#AA8866', lw=1.5, alpha=0.7)
ax_det.plot([lid_ring_inner_r + 1, ceramic_outer_r], [lid_z0, lid_z0],
            color='#AA8866', lw=1.0, ls='--')

# Inner housing wall (clipped)
ax_det.fill([housing_inner_r, housing_outer_r, housing_outer_r, housing_inner_r],
            [-2, -2, 14, 14],
            color='#C8CCD0', ec='black', lw=1.0, hatch='///')

# Outer mesh (clipped)
ax_det.fill([mesh_inner_r, mesh_outer_r, mesh_outer_r, mesh_inner_r],
            [-2, -2, 14, 14],
            color='#D0D4D8', ec='black', lw=1.0, hatch='...')

# --- DETAIL DIMENSIONS ---
# Shelf width
shelf_width = ceramic_outer_r - lid_ring_inner_r  # 10mm
dim_h(ax_det, shelf_z, lid_ring_inner_r, ceramic_outer_r,
      f'{shelf_width:.0f}mm shelf', offset=2, fontsize=8)

# Wall height
dim_v(ax_det, ceramic_outer_r + sheet_t, wall_bot, wall_top,
      f'{lid_wall_height}mm\nwall', offset=2, fontsize=8)

# Ceramic body thickness
dim_v(ax_det, (lid_ring_inner_r + ceramic_outer_r) / 2, lid_z0, lid_z0 + disk_body_h,
      f'{disk_body_h}mm\nbody', offset=-8, fontsize=8, color='brown')
# Ceramic lip thickness
dim_v(ax_det, lip_r, lid_z0 - disk_lip_h, lid_z0,
      f'{disk_lip_h}mm\nlip', offset=2, fontsize=8, color='#8B4513')

# Sheet thickness on bottom ring
leader(ax_det, (ceramic_outer_r + mesh_outer_r) / 2, lid_z0 + sheet_t / 2,
       55, -2, f't = {sheet_t}mm', fontsize=8)

# Radii callouts
leader(ax_det, lid_ring_inner_r, shelf_z + sheet_t / 2,
       30, 12, f'Shelf IR = {lid_ring_inner_r}mm', fontsize=7.5)
leader(ax_det, ceramic_outer_r, wall_top + 1,
       38, 12, f'Ceramic OR = {ceramic_outer_r}mm', fontsize=7.5)
leader(ax_det, housing_inner_r, 8,
       58, 12, f'Housing IR = {housing_inner_r}mm', fontsize=7.5)
leader(ax_det, mesh_outer_r, 5,
       66, -1, f'Mesh OR = {mesh_outer_r}mm', fontsize=7.5)

# Insulation gap
dim_h(ax_det, 10, ceramic_outer_r + sheet_t, housing_inner_r,
      f'{insulation_gap - sheet_t:.1f}mm', offset=2, fontsize=7)

# Air gap
dim_h(ax_det, 8, housing_outer_r, mesh_inner_r,
      f'{air_gap}mm', offset=-3, fontsize=7)

# Z reference labels
ax_det.text(29, lid_z0 + 0.2, f'z = {housing_top_z} (lid base)', fontsize=6, color='gray', style='italic')
ax_det.text(29, -disk_lip_h - 0.5, f'z = {housing_top_z - disk_lip_h:.1f} (lip bottom)',
            fontsize=5.5, color='#8B4513', style='italic')
ax_det.text(29, disk_body_h + 0.2, f'z = {housing_top_z + disk_body_h:.1f} (body top / shelf)',
            fontsize=5.5, color='brown', style='italic')
# Lip radius callout
leader(ax_det, lip_r, lid_z0 - disk_lip_h / 2,
       30, -3, f'Lip OR = {lip_r}mm', fontsize=7.5, color='#8B4513')

ax_det.set_xlabel('Radius (mm)', fontsize=8)
ax_det.set_ylabel('Height from lid base (mm)', fontsize=8)

draw_title_block(fig4, "Lid Assembly", thickness="1.2mm")
draw_tolerances_block(fig4, has_bends=True)

fig4.savefig('LidAssembly_Drawing.pdf', dpi=300, bbox_inches='tight')
print("Saved LidAssembly_Drawing.pdf")

# =============================================================================
# SHEET 5: COMPLETE ASSEMBLY OVERVIEW
# =============================================================================
fig5 = plt.figure(figsize=(24, 16))
fig5.suptitle('COMPLETE ASSEMBLY — CROSS SECTION OVERVIEW (Sheet 5)',
              fontsize=16, fontweight='bold', y=0.98)

# Main cross section on left, top view on right
ax_assy = fig5.add_axes([0.03, 0.06, 0.55, 0.88])
ax_plan = fig5.add_axes([0.62, 0.06, 0.36, 0.88])

# ---- MAIN ASSEMBLY CROSS SECTION ----
ax = ax_assy
ax.set_title('Section C-C (through center, full assembly)', fontsize=11, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-100, 100)
ax.set_ylim(-70, 170)
ax.grid(True, alpha=0.15)

# --- Draw base body ---
# Ceramic cylinder
ax.fill([-ceramic_outer_r, -ceramic_inner_r, -ceramic_inner_r, -ceramic_outer_r],
        [0, 0, cylinder_height, cylinder_height],
        color='#F5EBD8', ec='#AA8866', lw=0.8, alpha=0.5)
ax.fill([ceramic_inner_r, ceramic_outer_r, ceramic_outer_r, ceramic_inner_r],
        [0, 0, cylinder_height, cylinder_height],
        color='#F5EBD8', ec='#AA8866', lw=0.8, alpha=0.5)

# Ceramic base disk
ax.fill([-ceramic_outer_r, ceramic_outer_r, ceramic_outer_r, -ceramic_outer_r],
        [-disk_thickness, -disk_thickness, 0, 0],
        color='#F5EBD8', ec='#AA8866', lw=0.8, alpha=0.5)

# Inner housing
for sign in [-1, 1]:
    ax.fill([sign * housing_inner_r, sign * housing_outer_r,
             sign * housing_outer_r, sign * housing_inner_r],
            [housing_bottom_z, housing_bottom_z, housing_top_z, housing_top_z],
            color='#C8CCD0', ec='black', lw=0.6, hatch='///')

# Outer mesh
for sign in [-1, 1]:
    ax.fill([sign * mesh_inner_r, sign * mesh_outer_r,
             sign * mesh_outer_r, sign * mesh_inner_r],
            [housing_bottom_z, housing_bottom_z, housing_top_z, housing_top_z],
            color='#D0D4D8', ec='black', lw=0.6, hatch='...')

# Support ring shelf
for sign in [-1, 1]:
    ax.fill([sign * l_ring_inner_r, sign * housing_inner_r,
             sign * housing_inner_r, sign * l_ring_inner_r],
            [lip_z, lip_z, lip_z + sheet_t, lip_z + sheet_t],
            color='#C8CCD0', ec='black', lw=0.6, hatch='///')

# Retaining wall
for sign in [-1, 1]:
    ax.fill([sign * ceramic_outer_r, sign * (ceramic_outer_r + sheet_t),
             sign * (ceramic_outer_r + sheet_t), sign * ceramic_outer_r],
            [lip_z + sheet_t, lip_z + sheet_t, ring_wall_top_z, ring_wall_top_z],
            color='#C8CCD0', ec='black', lw=0.6, hatch='///')

# Bottom disk (base body)
ax.fill([-mesh_outer_r, mesh_outer_r, mesh_outer_r, -mesh_outer_r],
        [housing_bottom_z, housing_bottom_z, housing_bottom_z + sheet_t, housing_bottom_z + sheet_t],
        color='#C8CCD0', ec='black', lw=0.6, hatch='///')

# --- Top cap ---
# Flat ring
ax.fill([-cap_outer_r, -cap_inner_r, -cap_inner_r, -cap_outer_r],
        [housing_top_z, housing_top_z, housing_top_z - sheet_t, housing_top_z - sheet_t],
        color='#B8BCC0', ec='black', lw=0.6, hatch='///')
ax.fill([cap_inner_r, cap_outer_r, cap_outer_r, cap_inner_r],
        [housing_top_z, housing_top_z, housing_top_z - sheet_t, housing_top_z - sheet_t],
        color='#B8BCC0', ec='black', lw=0.6, hatch='///')

# Top cap outer lip
for sign in [-1, 1]:
    ax.fill([sign * (cap_outer_r - sheet_t), sign * cap_outer_r,
             sign * cap_outer_r, sign * (cap_outer_r - sheet_t)],
            [housing_top_z, housing_top_z, housing_top_z - lip_drop, housing_top_z - lip_drop],
            color='#B8BCC0', ec='black', lw=0.6, hatch='///')

# --- Bottom cap ---
bc_z = housing_bottom_z - sheet_t
ax.fill([-bottom_cap_outer_r, bottom_cap_outer_r, bottom_cap_outer_r, -bottom_cap_outer_r],
        [bc_z, bc_z, bc_z + sheet_t, bc_z + sheet_t],
        color='#B0B4B8', ec='black', lw=0.6, hatch='xxx')

# Bottom cap lip
for sign in [-1, 1]:
    ax.fill([sign * (bottom_cap_outer_r - sheet_t), sign * bottom_cap_outer_r,
             sign * bottom_cap_outer_r, sign * (bottom_cap_outer_r - sheet_t)],
            [bc_z + sheet_t, bc_z + sheet_t,
             bc_z + sheet_t + bottom_cap_lip_height, bc_z + sheet_t + bottom_cap_lip_height],
            color='#B0B4B8', ec='black', lw=0.6, hatch='xxx')

# --- Lid assembly ---
lid_local_z0 = housing_top_z

# Lid inner housing wall
for sign in [-1, 1]:
    ax.fill([sign * housing_inner_r, sign * housing_outer_r,
             sign * housing_outer_r, sign * housing_inner_r],
            [lid_local_z0, lid_local_z0, lid_local_z0 + lid_height, lid_local_z0 + lid_height],
            color='#D8DCE0', ec='black', lw=0.6, hatch='\\\\\\')

# Lid outer mesh
for sign in [-1, 1]:
    ax.fill([sign * mesh_inner_r, sign * mesh_outer_r,
             sign * mesh_outer_r, sign * mesh_inner_r],
            [lid_local_z0, lid_local_z0, lid_local_z0 + lid_height, lid_local_z0 + lid_height],
            color='#E0E4E8', ec='black', lw=0.6, hatch='...')

# Lid bottom ring
ax.fill([-mesh_outer_r, mesh_outer_r, mesh_outer_r, -mesh_outer_r],
        [lid_local_z0, lid_local_z0, lid_local_z0 + sheet_t, lid_local_z0 + sheet_t],
        color='#D8DCE0', ec='black', lw=0.6, hatch='\\\\\\')

# Lid ceramic disk (flush — body at lid base, lip below)
ax.fill([-ceramic_outer_r, ceramic_outer_r, ceramic_outer_r, -ceramic_outer_r],
        [lid_local_z0, lid_local_z0, lid_local_z0 + disk_body_h, lid_local_z0 + disk_body_h],
        color='#F5EBD8', ec='#AA8866', lw=0.6, alpha=0.5)
ax.fill([-lip_r, lip_r, lip_r, -lip_r],
        [lid_local_z0 - disk_lip_h, lid_local_z0 - disk_lip_h, lid_local_z0, lid_local_z0],
        color='#EDE0C8', ec='#AA8866', lw=0.6, alpha=0.6)

# Lid top disk
ax.fill([-mesh_outer_r, mesh_outer_r, mesh_outer_r, -mesh_outer_r],
        [lid_local_z0 + lid_height, lid_local_z0 + lid_height,
         lid_local_z0 + lid_height + sheet_t, lid_local_z0 + lid_height + sheet_t],
        color='#D8DCE0', ec='black', lw=0.6, hatch='\\\\\\')

# Handle
handle_base = lid_local_z0 + lid_height + sheet_t
for sign in [-1, 1]:
    ax.fill([sign * handle_width / 2 - handle_bar_r, sign * handle_width / 2 + handle_bar_r,
             sign * handle_width / 2 + handle_bar_r, sign * handle_width / 2 - handle_bar_r],
            [handle_base, handle_base, handle_base + handle_height, handle_base + handle_height],
            color='#A0A4A8', ec='black', lw=0.6, hatch='///')
# Bar
bar_z_assy = handle_base + handle_height
ax.fill([-handle_width / 2 - handle_bar_r, handle_width / 2 + handle_bar_r,
         handle_width / 2 + handle_bar_r, -handle_width / 2 - handle_bar_r],
        [bar_z_assy - handle_bar_r, bar_z_assy - handle_bar_r,
         bar_z_assy + handle_bar_r, bar_z_assy + handle_bar_r],
        color='#A0A4A8', ec='black', lw=0.6, hatch='///')

# --- Legs ---
for sign in [-1, 1]:
    leg_x = sign * leg_hole_r
    ax.fill([leg_x - 10, leg_x + 10, leg_x + 10, leg_x - 10],
            [bc_z - leg_height, bc_z - leg_height, bc_z, bc_z],
            color='#F5EBD8', ec='#AA8866', lw=0.6, alpha=0.5)
    # Flange at bottom
    ax.fill([leg_x - 14, leg_x + 14, leg_x + 14, leg_x - 14],
            [bc_z - leg_height, bc_z - leg_height, bc_z - leg_height + 5, bc_z - leg_height + 5],
            color='#F5EBD8', ec='#AA8866', lw=0.6, alpha=0.5)

# --- Hinge indicator on right side ---
hinge_x = mesh_outer_r + 12
hinge_z = housing_top_z
ax.fill([hinge_x - 6, hinge_x + 6, hinge_x + 6, hinge_x - 6],
        [hinge_z - 5, hinge_z - 5, hinge_z + 15, hinge_z + 15],
        color='#A0A0A0', ec='black', lw=0.8)
ax.add_patch(plt.Circle((hinge_x, hinge_z), 5, fill=False, ec='black', lw=1.0))
ax.add_patch(plt.Circle((hinge_x, hinge_z), 2.5, fill=True, fc='gray', ec='black', lw=0.5))

# === DIMENSIONS ===
# Full height from bottom cap to handle top
total_bottom = bc_z
total_top = bar_z_assy + handle_bar_r
dim_v(ax, -mesh_outer_r, total_bottom, total_top,
      f'{total_top - total_bottom:.1f}mm\ntotal H', offset=-18, fontsize=6)

# Base body height
dim_v(ax, mesh_outer_r, housing_bottom_z, housing_top_z,
      f'{housing_top_z - housing_bottom_z:.0f}mm\nbase body', offset=10)

# Lid height
dim_v(ax, mesh_outer_r, lid_local_z0, lid_local_z0 + lid_height,
      f'{lid_height}mm\nlid', offset=16)

# Ceramic height
dim_v(ax, ceramic_outer_r, 0, cylinder_height,
      f'{cylinder_height}mm\nceramic', offset=4, color='brown')

# Leg height
dim_v(ax, -leg_hole_r - 16, bc_z - leg_height, bc_z,
      f'{leg_height}mm\nlegs', offset=-6)

# Handle height
dim_v(ax, handle_width / 2 + handle_bar_r + 2, handle_base, bar_z_assy + handle_bar_r,
      f'{handle_height}mm\nhandle', offset=4)

# Radial dimensions at top
dim_h(ax, bar_z_assy + handle_bar_r + 2, -mesh_outer_r, mesh_outer_r,
      f'Mesh OD {mesh_outer_r * 2:.1f}mm', offset=18)
dim_h(ax, bar_z_assy + handle_bar_r + 2, -ceramic_outer_r, ceramic_outer_r,
      f'Ceramic OD {ceramic_od}mm', offset=10, color='brown')

# Interface callouts
leader(ax, housing_top_z > 0 and cap_outer_r or 0, housing_top_z,
       85, housing_top_z + 5,
       f'Top cap interface\nz={housing_top_z}')
leader(ax, housing_inner_r, housing_bottom_z,
       85, housing_bottom_z - 5,
       f'Bottom disk\nz={housing_bottom_z}')
leader(ax, bottom_cap_outer_r, bc_z + sheet_t / 2,
       90, bc_z - 10,
       f'Bottom cap\nz={bc_z:.1f}')

# Hinge callout
leader(ax, hinge_x, hinge_z, 95, hinge_z + 20,
       f'Hinge at {hinge_angle:.1f} deg\n(center of {gaps[3]}mm gap)')

# Leg callout
leader(ax, -leg_hole_r, bc_z - leg_height / 2,
       -90, bc_z - leg_height,
       f'3x ceramic legs\nat 40/160/280 deg\nR={leg_hole_r}mm')

# Insulation gap
leader(ax, (ceramic_outer_r + housing_inner_r) / 2, 50,
       -85, 60,
       f'Insulation gap {insulation_gap}mm')

# Air gap
leader(ax, (housing_outer_r + mesh_inner_r) / 2, 50,
       -85, 45,
       f'Air gap {air_gap}mm')

# Material callouts
# Base body
leader(ax, housing_outer_r, 30,
       85, 30,
       f'Base body\n304 SS, {sheet_t}mm', fontsize=5.5)
# Ceramic
leader(ax, 0, cylinder_height / 2,
       -30, cylinder_height / 2,
       f'Ceramic\nhigh-alumina', fontsize=5.5, color='brown')
# Lid
leader(ax, housing_outer_r, lid_local_z0 + lid_height / 2,
       85, lid_local_z0 + lid_height / 2,
       f'Lid assembly\n304 SS, {sheet_t}mm', fontsize=5.5)

# Z reference marks
for z_val, label in [
    (0, 'z=0 (ceramic base)'),
    (housing_top_z, f'z={housing_top_z} (body/lid interface)'),
    (housing_bottom_z, f'z={housing_bottom_z}'),
    (lip_z, f'z={lip_z} (support ring)'),
    (lid_top_z, f'z={lid_top_z} (lid top)'),
]:
    ax.plot([-mesh_outer_r - 5, -mesh_outer_r - 2], [z_val, z_val], color='gray', lw=0.4)
    ax.text(-mesh_outer_r - 6, z_val, label, fontsize=4.5, color='gray',
            ha='right', va='center', style='italic')

# Legend and materials box
ax.text(-98, -62, (
    'LEGEND:\n'
    '  /// = Stainless steel (base)\n'
    '  \\\\\\  = Stainless steel (lid)\n'
    '  ... = Perforated mesh\n'
    '  xxx = Bottom cap\n'
    '  Tan = Ceramic\n'
), fontsize=5.5, family='monospace',
   bbox=dict(boxstyle='round', fc='white', ec='gray'))

ax.text(20, -62, (
    'MATERIALS:\n'
    f'  Body/Lid/Cap: 304 SS, t={sheet_t}mm\n'
    '  Ceramic: High-alumina\n'
    '  Legs: Ceramic (heat insulating)\n'
    '  Handle: 304 SS rod\n'
    '  Hinge: 304 SS\n'
    f'  Perf mesh: {perf_hole_r * 2}mm holes, {perf_spacing}mm spacing'
), fontsize=5.5, family='monospace',
   bbox=dict(boxstyle='round', fc='lightyellow', ec='gray'))

ax.set_xlabel('Radius (mm)', fontsize=8)
ax.set_ylabel('Height (mm)', fontsize=8)

# ---- TOP/PLAN VIEW (right panel) ----
ax = ax_plan
ax.set_title('PLAN VIEW (top down) — Key Angular Positions', fontsize=11,
             fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-95, 95)
ax.set_ylim(-95, 95)
ax.grid(True, alpha=0.15)

# Draw concentric circles
for r, label, color, ls in [
    (cap_outer_r, 'Cap outer', '#333', '-'),
    (mesh_outer_r, 'Mesh outer', '#999', '-'),
    (housing_outer_r, 'Housing outer', '#999', ':'),
    (housing_inner_r, 'Housing inner', '#999', ':'),
    (ceramic_outer_r, 'Ceramic outer', '#aa8866', '--'),
    (cap_inner_r, 'Ceramic inner', '#aa8866', '--'),
]:
    circle = plt.Circle((0, 0), r, fill=False, ec=color, lw=0.6, ls=ls)
    ax.add_patch(circle)

# 4 Slots
slot_arc_half = (slot_width / 2) / ceramic_outer_r * (180 / np.pi)
for i, ang in enumerate(slot_positions):
    a1 = np.radians(ang - slot_arc_half)
    a2 = np.radians(ang + slot_arc_half)
    t_range = np.linspace(a1, a2, 20)
    xs_o = ceramic_outer_r * np.cos(t_range)
    ys_o = ceramic_outer_r * np.sin(t_range)
    inner_slot_r = ceramic_outer_r - slot_depth
    xs_i = inner_slot_r * np.cos(t_range[::-1])
    ys_i = inner_slot_r * np.sin(t_range[::-1])
    ax.fill(np.concatenate([xs_o, xs_i]), np.concatenate([ys_o, ys_i]),
            color='#FFE0B0', ec='red', lw=0.6, alpha=0.5)
    ang_rad = np.radians(ang)
    lx = (ceramic_outer_r + 5) * np.cos(ang_rad)
    ly = (ceramic_outer_r + 5) * np.sin(ang_rad)
    ax.text(lx, ly, f'S{i + 1}\n{ang:.1f} deg', fontsize=4.5, ha='center', va='center',
            color='red', fontweight='bold')

# Leg positions
for ang_deg in leg_angles:
    ang_rad = np.radians(ang_deg)
    hx = leg_hole_r * np.cos(ang_rad)
    hy = leg_hole_r * np.sin(ang_rad)
    leg_circle = plt.Circle((hx, hy), 10, fill=True, fc='#F5EBD8', ec='#AA8866',
                             lw=0.8, alpha=0.5)
    ax.add_patch(leg_circle)
    hole = plt.Circle((hx, hy), bolt_hole_size / 2, fill=False, ec='darkblue', lw=0.8)
    ax.add_patch(hole)
    ax.text(hx, hy, f'Leg\n{ang_deg} deg', fontsize=4, ha='center', va='center', color='darkblue')

# Hinge position
hinge_rad = np.radians(hinge_angle)
hinge_x_plan = mesh_outer_r * np.cos(hinge_rad)
hinge_y_plan = mesh_outer_r * np.sin(hinge_rad)
# Draw hinge bracket
hinge_outer_x = (mesh_outer_r + 12) * np.cos(hinge_rad)
hinge_outer_y = (mesh_outer_r + 12) * np.sin(hinge_rad)
ax.plot([hinge_x_plan, hinge_outer_x], [hinge_y_plan, hinge_outer_y],
        color='#404040', lw=4, solid_capstyle='butt')
ax.add_patch(plt.Circle((hinge_outer_x, hinge_outer_y), 5,
                         fill=False, ec='black', lw=1.0))
leader(ax, hinge_outer_x, hinge_outer_y,
       hinge_outer_x + 15 * np.cos(hinge_rad), hinge_outer_y + 15 * np.sin(hinge_rad),
       f'Hinge\n{hinge_angle:.1f} deg', fontsize=5.5, color='#404040')

# Screw tab positions
for i, ang_deg in enumerate(bottom_cap_tab_angles):
    ang_rad = np.radians(ang_deg)
    tab_r = bottom_cap_outer_r + tab_depth / 2
    tx = tab_r * np.cos(ang_rad)
    ty = tab_r * np.sin(ang_rad)
    ax.add_patch(plt.Circle((tx, ty), 3, fc='#B0B0B0', ec='black', lw=0.5))
    if i == 0:
        leader(ax, tx, ty, tx + 10, ty + 10,
               f'5x round flanges\n(bottom cap)', fontsize=5, color='gray')

# Dimension: outer diameter
dim_h(ax, -cap_outer_r, -cap_outer_r, cap_outer_r,
      f'Cap OD {cap_outer_r * 2:.1f}mm', offset=-8)

# Bolt circle
bolt_c = plt.Circle((0, 0), leg_hole_r, fill=False, ec='darkblue', lw=0.4, ls=':')
ax.add_patch(bolt_c)
leader(ax, leg_hole_r * np.cos(np.radians(90)),
       leg_hole_r * np.sin(np.radians(90)) + 3,
       20, 85, f'Bolt circle R={leg_hole_r}mm')

# Angular reference line (0 degrees)
ax.plot([0, cap_outer_r + 5], [0, 0], color='gray', lw=0.3, ls='-.')
ax.text(cap_outer_r + 6, 0, '0 deg', fontsize=5, color='gray', va='center')

# Large gap annotation
gap_start_rad = np.radians(slot_4_end_angle)
gap_end_rad = np.radians(slot_positions[0] - slot_arc_half_deg)
gap_mid_rad = (gap_start_rad + gap_end_rad) / 2
if gap_end_rad < gap_start_rad:
    gap_mid_rad = gap_start_rad + (gap_end_rad + 2 * np.pi - gap_start_rad) / 2
gmx = (mesh_outer_r + 20) * np.cos(gap_mid_rad)
gmy = (mesh_outer_r + 20) * np.sin(gap_mid_rad)
ax.text(gmx, gmy, f'Large gap\n{gaps[3]}mm arc', fontsize=5, ha='center', va='center',
        color='red', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='red', alpha=0.8))

ax.set_xlabel('X (mm)', fontsize=8)
ax.set_ylabel('Y (mm)', fontsize=8)

# BOM table on the plan view (right panel)
draw_bom_table(ax_plan, -90, -55)

draw_title_block(fig5, "Complete Assembly", material="Various", thickness="Various",
                 finish="Various")
draw_tolerances_block(fig5, has_bends=False)

fig5.savefig('Assembly_Drawing.pdf', dpi=300, bbox_inches='tight')
print("Saved Assembly_Drawing.pdf")

plt.show()
print("\nDone! Three additional PDF drawing sheets saved:")
print("  3. BottomCap_Drawing.pdf")
print("  4. LidAssembly_Drawing.pdf")
print("  5. Assembly_Drawing.pdf")
