"""
DIMENSIONED TECHNICAL DRAWINGS
- Top Cap: cross-section + top view with all measurements
- Metal Body: cross-section with all layers dimensioned
Outputs PDF files for manufacturer spec sheets.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# =============================================================================
# ALL DIMENSIONS (matching CAD exactly)
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
lip_z = -(disk_thickness + sheet_t)  # -6.7 — ring sits UNDER ceramic base
housing_bottom_z = lip_z - 25  # -30.5
housing_top_z = cylinder_height  # 91

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

# Support ring
l_ring_inner_r = ceramic_outer_r - 10  # 36.25 — extends 10mm under ceramic
# Retaining wall: up to 2mm below thermocouple hole bottom (hole_bottom=5mm)
hole_bottom_height = 5
ring_wall_top_z = hole_bottom_height - 2  # 3mm

# =============================================================================
# DRAWING HELPERS
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


# =============================================================================
# SHEET 1: TOP CAP
# =============================================================================
fig1, (ax_section, ax_top) = plt.subplots(1, 2, figsize=(22, 12))
fig1.suptitle('TOP CAP — DIMENSIONED DRAWING', fontsize=16, fontweight='bold', y=0.98)

# --- View A: Cross Section (side view, cut through slot center) ---
ax = ax_section
ax.set_title('CROSS SECTION (through slot center)', fontsize=11, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-80, 80)
ax.set_ylim(-40, 15)
ax.grid(True, alpha=0.15)

z_top = 0  # Reference: top of cap at z=0 for drawing

# Draw the flat cap ring (cross section = two rectangles, left and right)
# Left side
ax.fill([-cap_outer_r, -cap_inner_r, -cap_inner_r, -cap_outer_r],
        [z_top, z_top, z_top - sheet_t, z_top - sheet_t],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')
# Right side
ax.fill([cap_inner_r, cap_outer_r, cap_outer_r, cap_inner_r],
        [z_top, z_top, z_top - sheet_t, z_top - sheet_t],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')

# Slot form-fit dip (at slot center, full depth)
slot_dip = -slot_depth
# Left slot dip
ax.fill([-cap_outer_r, -cap_inner_r, -cap_inner_r, -cap_outer_r],
        [slot_dip, slot_dip, slot_dip - sheet_t, slot_dip - sheet_t],
        color='#A0A0A0', ec='black', lw=1.0, hatch='///', alpha=0.5)
# Right slot dip
ax.fill([cap_inner_r, cap_outer_r, cap_outer_r, cap_inner_r],
        [slot_dip, slot_dip, slot_dip - sheet_t, slot_dip - sheet_t],
        color='#A0A0A0', ec='black', lw=1.0, hatch='///', alpha=0.5)

# Outer lip (left)
ax.fill([-cap_outer_r, -cap_outer_r + sheet_t, -cap_outer_r + sheet_t, -cap_outer_r],
        [z_top, z_top, z_top - lip_drop, z_top - lip_drop],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')
# Outer lip (right)
ax.fill([cap_outer_r - sheet_t, cap_outer_r, cap_outer_r, cap_outer_r - sheet_t],
        [z_top, z_top, z_top - lip_drop, z_top - lip_drop],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')

# Outer lip at slot (extends deeper)
lip_at_slot = slot_dip - lip_drop
ax.plot([-cap_outer_r, -cap_outer_r], [z_top - lip_drop, lip_at_slot], 'k-', lw=0.8, ls=':')
ax.plot([cap_outer_r, cap_outer_r], [z_top - lip_drop, lip_at_slot], 'k-', lw=0.8, ls=':')

# Inner grab lip (left)
ax.fill([-cap_inner_r - sheet_t, -cap_inner_r, -cap_inner_r, -cap_inner_r - sheet_t],
        [z_top - sheet_t, z_top - sheet_t, z_top - sheet_t - ceramic_grab_lip, z_top - sheet_t - ceramic_grab_lip],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')
# Inner grab lip (right)
ax.fill([cap_inner_r, cap_inner_r + sheet_t, cap_inner_r + sheet_t, cap_inner_r],
        [z_top - sheet_t, z_top - sheet_t, z_top - sheet_t - ceramic_grab_lip, z_top - sheet_t - ceramic_grab_lip],
        color='#C0C0C0', ec='black', lw=1.0, hatch='///')

# Chamber ridge (left) at housing_inner_r
ridge_x_l = -housing_inner_r
ax.fill([ridge_x_l - sheet_t, ridge_x_l, ridge_x_l, ridge_x_l - sheet_t],
        [z_top - sheet_t, z_top - sheet_t, z_top - sheet_t - chamber_ridge_drop, z_top - sheet_t - chamber_ridge_drop],
        color='#B0B0B0', ec='black', lw=1.0, hatch='///')
# Chamber ridge (right)
ridge_x_r = housing_inner_r
ax.fill([ridge_x_r, ridge_x_r + sheet_t, ridge_x_r + sheet_t, ridge_x_r],
        [z_top - sheet_t, z_top - sheet_t, z_top - sheet_t - chamber_ridge_drop, z_top - sheet_t - chamber_ridge_drop],
        color='#B0B0B0', ec='black', lw=1.0, hatch='///')

# --- DIMENSIONS ---
# Overall diameter
dim_h(ax, z_top, -cap_outer_r, cap_outer_r, f'OD {cap_outer_r*2:.1f}mm', offset=8)

# Inner bore
dim_h(ax, z_top, -cap_inner_r, cap_inner_r, f'Bore {cap_inner_r*2:.1f}mm', offset=4)

# Outer lip drop
dim_v(ax, cap_outer_r, z_top, z_top - lip_drop, f'{lip_drop}mm\nlip', offset=4)

# Inner grab lip
dim_v(ax, -cap_inner_r, z_top - sheet_t, z_top - sheet_t - ceramic_grab_lip,
      f'{ceramic_grab_lip}mm\ngrab', offset=-8)

# Chamber ridge
dim_v(ax, housing_inner_r, z_top - sheet_t, z_top - sheet_t - chamber_ridge_drop,
      f'{chamber_ridge_drop}mm\nridge', offset=5)

# Sheet thickness
leader(ax, (cap_inner_r + cap_outer_r)/2, z_top - sheet_t/2,
       (cap_inner_r + cap_outer_r)/2 + 5, -8, f't = {sheet_t}mm')

# Slot depth
dim_v(ax, -cap_outer_r - 2, z_top, slot_dip, f'{slot_depth}mm\nslot depth', offset=-10)

# Housing inner r callout
leader(ax, ridge_x_r, z_top - sheet_t - 2, ridge_x_r + 12, -15,
       f'Housing IR\n{housing_inner_r}mm R')

# Cap outer r callout
leader(ax, cap_outer_r, z_top - 5, cap_outer_r + 8, -20,
       f'Cap OR\n{cap_outer_r:.1f}mm R')

# Ceramic inner r callout
leader(ax, cap_inner_r, z_top - 2, cap_inner_r + 10, -12,
       f'Ceramic IR\n{cap_inner_r}mm R')

# Material callout
ax.text(-75, -35, 'MATERIAL: 304 Stainless Steel\nTHICKNESS: 1.2mm\nFINISH: #4 Brushed',
        fontsize=7, family='monospace', bbox=dict(boxstyle='round', fc='lightyellow', ec='gray'))

ax.set_xlabel('Radius (mm)', fontsize=8)
ax.set_ylabel('Height (mm)', fontsize=8)

# --- View B: Top View ---
ax = ax_top
ax.set_title('TOP VIEW', fontsize=11, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-85, 85)
ax.set_ylim(-85, 85)
ax.grid(True, alpha=0.15)

# Draw concentric circles
for r, label, color, ls in [
    (cap_outer_r, 'Cap outer', '#333', '-'),
    (mesh_outer_r, 'Mesh outer', '#999', ':'),
    (housing_outer_r, 'Housing outer', '#999', ':'),
    (housing_inner_r, 'Housing inner', '#999', ':'),
    (ceramic_outer_r, 'Ceramic outer', '#aa8866', '--'),
    (cap_inner_r, 'Ceramic inner', '#aa8866', '--'),
]:
    circle = plt.Circle((0, 0), r, fill=False, ec=color, lw=0.8, ls=ls)
    ax.add_patch(circle)

# Perforation zone (hatched ring between housing_outer_r and cap_outer_r)
theta = np.linspace(0, 2*np.pi, 100)
# Light shading for vent zone
for t in np.linspace(0, 2*np.pi, 60):
    r1, r2 = housing_outer_r, cap_outer_r
    ax.plot([r1*np.cos(t), r2*np.cos(t)], [r1*np.sin(t), r2*np.sin(t)],
            color='lightblue', lw=0.3, alpha=0.5)

# Draw 4 slots as stadium shapes on the ceramic circle
import math
circumference = math.pi * ceramic_od
gaps = [46.25, 46.25, 46.25, 108.68]
scale_factor = circumference / (sum(gaps) + 4 * slot_width)
slot_positions = []
current_arc = 0
for i in range(4):
    center_arc = current_arc + (slot_width * scale_factor) / 2
    angle = (center_arc / circumference) * 360
    slot_positions.append(angle)
    current_arc += (slot_width + gaps[i]) * scale_factor

slot_arc_half = (slot_width / 2) / ceramic_outer_r * (180 / np.pi)

for i, ang in enumerate(slot_positions):
    ang_rad = np.radians(ang)
    # Draw slot as a wedge on the top view
    a1 = np.radians(ang - slot_arc_half)
    a2 = np.radians(ang + slot_arc_half)
    t_range = np.linspace(a1, a2, 20)
    # Outer arc
    xs_o = ceramic_outer_r * np.cos(t_range)
    ys_o = ceramic_outer_r * np.sin(t_range)
    # Inner arc (slot goes inward by slot_depth)
    inner_slot_r = ceramic_outer_r - slot_depth
    xs_i = inner_slot_r * np.cos(t_range[::-1])
    ys_i = inner_slot_r * np.sin(t_range[::-1])
    ax.fill(np.concatenate([xs_o, xs_i]), np.concatenate([ys_o, ys_i]),
            color='#FFE0B0', ec='red', lw=0.8, alpha=0.6)
    # Label
    lx = (ceramic_outer_r + 5) * np.cos(ang_rad)
    ly = (ceramic_outer_r + 5) * np.sin(ang_rad)
    ax.text(lx, ly, f'S{i+1}\n{ang:.1f}°', fontsize=5.5, ha='center', va='center',
            color='red', fontweight='bold')

# Leg bolt holes
for ang_deg in [40, 160, 280]:
    ang_rad = np.radians(ang_deg)
    hx = leg_hole_r * np.cos(ang_rad)
    hy = leg_hole_r * np.sin(ang_rad)
    hole = plt.Circle((hx, hy), bolt_hole_size / 2, fill=False, ec='darkblue', lw=1.0)
    ax.add_patch(hole)
    ax.text(hx, hy, f'M6\n{ang_deg}°', fontsize=4.5, ha='center', va='center', color='darkblue')

# Dimension: outer diameter
dim_h(ax, -cap_outer_r, -cap_outer_r, cap_outer_r,
      f'OD {cap_outer_r*2:.1f}mm', offset=-8, fontsize=7)

# Dimension: bore
dim_h(ax, cap_inner_r, -cap_inner_r, cap_inner_r,
      f'Bore {cap_inner_r*2:.1f}mm', offset=5, fontsize=7)

# Dimension: ceramic OD
dim_h(ax, 0, -ceramic_outer_r, ceramic_outer_r,
      f'Ceramic OD {ceramic_od}mm', offset=2, fontsize=6, color='brown')

# Bolt circle
leader(ax, leg_hole_r * np.cos(np.radians(90)), leg_hole_r * np.sin(np.radians(90)) + 3,
       20, 78, f'Bolt circle R={leg_hole_r}mm\n3x M6 holes')

# Vent zone
leader(ax, (housing_outer_r + cap_outer_r)/2, 0, 75, 30,
       f'Vent perf zone\n4mm holes, 6mm spacing')

# Slot dimension
leader(ax, ceramic_outer_r * np.cos(np.radians(slot_positions[0])),
       ceramic_outer_r * np.sin(np.radians(slot_positions[0])),
       -70, 60, f'4x slots\n{slot_width}mm W x {slot_depth}mm D')

ax.set_xlabel('X (mm)', fontsize=8)
ax.set_ylabel('Y (mm)', fontsize=8)

draw_title_block(fig1, "Top Cap", thickness="1.2mm")
draw_tolerances_block(fig1, has_bends=True)
fig1.tight_layout(rect=[0, 0.08, 1, 0.95])
fig1.savefig('TopCap_Drawing.pdf', dpi=300, bbox_inches='tight')
print("Saved TopCap_Drawing.pdf")

# =============================================================================
# SHEET 2: METAL BODY CROSS SECTION + L-RING DETAIL
# =============================================================================
fig2 = plt.figure(figsize=(24, 14))
fig2.suptitle('METAL BODY ASSEMBLY — CROSS SECTION', fontsize=16, fontweight='bold', y=0.98)

# Left: full cross section.  Right: zoomed L-ring / bottom detail
ax = fig2.add_axes([0.03, 0.06, 0.55, 0.88])   # main view
ax_det = fig2.add_axes([0.62, 0.06, 0.36, 0.88])  # detail view

# ---- MAIN VIEW (full body) ----
ax.set_title('Section A-A (through center)', fontsize=11, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-95, 95)
ax.set_ylim(-50, 110)
ax.grid(True, alpha=0.15)

def draw_body_cross_section(a, lw_scale=1.0):
    """Draw all body cross-section geometry on given axes."""
    lw = 0.8 * lw_scale

    # Ceramic cylinder
    a.fill([-ceramic_outer_r, -ceramic_inner_r, -ceramic_inner_r, -ceramic_outer_r],
           [0, 0, cylinder_height, cylinder_height],
           color='#F5EBD8', ec='#AA8866', lw=lw, alpha=0.5)
    a.fill([ceramic_inner_r, ceramic_outer_r, ceramic_outer_r, ceramic_inner_r],
           [0, 0, cylinder_height, cylinder_height],
           color='#F5EBD8', ec='#AA8866', lw=lw, alpha=0.5)

    # Inner housing
    for sign in [-1, 1]:
        a.fill([sign*housing_inner_r, sign*housing_outer_r, sign*housing_outer_r, sign*housing_inner_r],
               [housing_bottom_z, housing_bottom_z, housing_top_z, housing_top_z],
               color='#C8CCD0', ec='black', lw=lw, hatch='///')

    # Outer mesh
    for sign in [-1, 1]:
        a.fill([sign*mesh_inner_r, sign*mesh_outer_r, sign*mesh_outer_r, sign*mesh_inner_r],
               [housing_bottom_z, housing_bottom_z, housing_top_z, housing_top_z],
               color='#D0D4D8', ec='black', lw=lw, hatch='...')

    # Support ring — flat shelf under ceramic
    for sign in [-1, 1]:
        a.fill([sign*l_ring_inner_r, sign*housing_inner_r, sign*housing_inner_r, sign*l_ring_inner_r],
               [lip_z, lip_z, lip_z + sheet_t, lip_z + sheet_t],
               color='#C8CCD0', ec='black', lw=lw, hatch='///')

    # Retaining wall — holds ceramic in place
    for sign in [-1, 1]:
        a.fill([sign*ceramic_outer_r, sign*(ceramic_outer_r + sheet_t),
                sign*(ceramic_outer_r + sheet_t), sign*ceramic_outer_r],
               [lip_z + sheet_t, lip_z + sheet_t, ring_wall_top_z, ring_wall_top_z],
               color='#C8CCD0', ec='black', lw=lw, hatch='///')

    # Bottom disk
    a.fill([-mesh_outer_r, mesh_outer_r, mesh_outer_r, -mesh_outer_r],
           [housing_bottom_z, housing_bottom_z, housing_bottom_z + sheet_t, housing_bottom_z + sheet_t],
           color='#C8CCD0', ec='black', lw=lw, hatch='///')

    # Ceramic base disk
    a.fill([-ceramic_outer_r, ceramic_outer_r, ceramic_outer_r, -ceramic_outer_r],
           [-disk_thickness, -disk_thickness, 0, 0],
           color='#F5EBD8', ec='#AA8866', lw=lw, alpha=0.5)

# Draw on main view
draw_body_cross_section(ax)

# --- MAIN VIEW DIMENSIONS ---
# Radial dimensions (top)
dim_h(ax, housing_top_z, -ceramic_outer_r, ceramic_outer_r,
      f'Ceramic OD {ceramic_od}mm', offset=14, color='brown')
dim_h(ax, housing_top_z, -ceramic_inner_r, ceramic_inner_r,
      f'Ceramic ID {ceramic_id}mm', offset=8, color='brown')
dim_h(ax, housing_top_z, -housing_outer_r, housing_outer_r,
      f'Housing OD {housing_outer_r*2:.1f}mm', offset=3)
dim_h(ax, housing_top_z, -mesh_outer_r, mesh_outer_r,
      f'Mesh OD {mesh_outer_r*2:.1f}mm', offset=20)

# Vertical dimensions (right side)
dim_v(ax, mesh_outer_r, housing_bottom_z, housing_top_z,
      f'{housing_top_z - housing_bottom_z:.0f}mm\nhousing H', offset=8)
dim_v(ax, ceramic_outer_r, 0, cylinder_height,
      f'{cylinder_height}mm\nceramic H', offset=4, color='brown')

# Gap dimensions
leader(ax, (ceramic_outer_r + housing_inner_r) / 2, cylinder_height / 2,
       75, 70, f'Insulation gap\n{insulation_gap}mm')
leader(ax, (housing_outer_r + mesh_inner_r) / 2, cylinder_height / 2,
       80, 50, f'Air gap\n{air_gap}mm')
leader(ax, housing_outer_r, cylinder_height * 0.7,
       78, 35, f'Sheet t = {sheet_t}mm')

# Wire holes
leader(ax, -housing_outer_r + 2, 15.5,
       -85, 45, f'Wire holes\n2x Ø8mm at\nz=15.5, z=66.5mm')

# Perf pattern
leader(ax, mesh_outer_r, 40,
       85, 20, f'Perf mesh\n4mm holes\n6mm spacing\nstaggered')

# Z callouts
ax.text(mesh_outer_r + 2, housing_top_z, f'z={housing_top_z}', fontsize=5, color='gray')
ax.text(mesh_outer_r + 2, housing_bottom_z, f'z={housing_bottom_z}', fontsize=5, color='gray')
ax.text(mesh_outer_r + 2, 0, 'z=0', fontsize=5, color='gray')
ax.text(mesh_outer_r + 2, lip_z, f'z={lip_z}', fontsize=5, color='gray')

# Detail callout circle on main view (around L-ring/bottom area)
detail_cx, detail_cy, detail_r = 0, -12, 35
circle_call = plt.Circle((detail_cx, detail_cy), detail_r,
                          fill=False, ec='red', lw=1.5, ls='--')
ax.add_patch(circle_call)
ax.text(detail_cx + detail_r + 2, detail_cy + detail_r,
        'DETAIL A', fontsize=9, color='red', fontweight='bold')

ax.set_xlabel('Radius (mm)', fontsize=8)
ax.set_ylabel('Height (mm)', fontsize=8)

# ---- DETAIL VIEW (zoomed L-ring / bottom) ----
ax_det.set_title('DETAIL A — Support Ring & Bottom (4x scale)', fontsize=11,
                 fontweight='bold', pad=10, color='red')
ax_det.set_aspect('equal')
# Zoom to show from just inside ceramic to just outside mesh, z from -35 to 15
ax_det.set_xlim(-5, 72)
ax_det.set_ylim(-38, 15)
ax_det.grid(True, alpha=0.2)

# Redraw geometry on detail view (right-half only for clarity)
# Ceramic cylinder wall (right side, clipped to zoom range)
ax_det.fill([ceramic_inner_r, ceramic_outer_r, ceramic_outer_r, ceramic_inner_r],
            [-5.5, -5.5, 15, 15],
            color='#F5EBD8', ec='#AA8866', lw=1.2, alpha=0.5)

# Ceramic base disk (right half)
ax_det.fill([0, ceramic_outer_r, ceramic_outer_r, 0],
            [-disk_thickness, -disk_thickness, 0, 0],
            color='#F5EBD8', ec='#AA8866', lw=1.2, alpha=0.5)

# Inner housing (right side, clipped)
ax_det.fill([housing_inner_r, housing_outer_r, housing_outer_r, housing_inner_r],
            [housing_bottom_z, housing_bottom_z, 15, 15],
            color='#C8CCD0', ec='black', lw=1.2, hatch='///')

# Outer mesh (right side, clipped)
ax_det.fill([mesh_inner_r, mesh_outer_r, mesh_outer_r, mesh_inner_r],
            [housing_bottom_z, housing_bottom_z, 15, 15],
            color='#D0D4D8', ec='black', lw=1.2, hatch='...')

# Support ring shelf (right side) — extends 10mm under ceramic
ax_det.fill([l_ring_inner_r, housing_inner_r, housing_inner_r, l_ring_inner_r],
            [lip_z, lip_z, lip_z + sheet_t, lip_z + sheet_t],
            color='#A8B8C0', ec='black', lw=1.5, hatch='///')

# Retaining wall (right side) — holds ceramic laterally
ax_det.fill([ceramic_outer_r, ceramic_outer_r + sheet_t,
             ceramic_outer_r + sheet_t, ceramic_outer_r],
            [lip_z + sheet_t, lip_z + sheet_t, ring_wall_top_z, ring_wall_top_z],
            color='#A8B8C0', ec='black', lw=1.5, hatch='///')

# Bottom disk (right half)
ax_det.fill([0, mesh_outer_r, mesh_outer_r, 0],
            [housing_bottom_z, housing_bottom_z, housing_bottom_z + sheet_t, housing_bottom_z + sheet_t],
            color='#C8CCD0', ec='black', lw=1.2, hatch='///')

# --- DETAIL DIMENSIONS ---
# Support ring total width
ring_width = housing_inner_r - l_ring_inner_r  # 20mm total
under_ceramic = ceramic_outer_r - l_ring_inner_r  # 10mm under ceramic
dim_h(ax_det, lip_z, l_ring_inner_r, housing_inner_r,
      f'{ring_width:.0f}mm ring', offset=-4, fontsize=8)

# 10mm under ceramic callout
dim_h(ax_det, lip_z, l_ring_inner_r, ceramic_outer_r,
      f'{under_ceramic:.0f}mm\nunder ceramic', offset=-9, fontsize=7)

# Retaining wall height
wall_bottom_z = lip_z + sheet_t
dim_v(ax_det, ceramic_outer_r, wall_bottom_z, ring_wall_top_z,
      f'{ring_wall_top_z - wall_bottom_z:.1f}mm\nwall', offset=-7, fontsize=8)

# Ring depth below ceramic base
dim_v(ax_det, housing_inner_r, lip_z, 0,
      f'{abs(lip_z)}mm\nbelow base', offset=4, fontsize=8)

# Ceramic base disk thickness
dim_v(ax_det, ceramic_outer_r / 2, -disk_thickness, 0,
      f'{disk_thickness}mm\nceramic disk', offset=-10, fontsize=8, color='brown')

# Bottom disk to ring
dim_v(ax_det, mesh_outer_r, housing_bottom_z, lip_z,
      f'25mm\nbottom to ring', offset=4, fontsize=8)

# Sheet thickness on ring
leader(ax_det, (l_ring_inner_r + housing_inner_r)/2, lip_z + sheet_t/2,
       38, 10, f't = {sheet_t}mm\n(all sheet metal)', fontsize=8)

# Radii callouts
leader(ax_det, l_ring_inner_r, lip_z, 10, -18,
       f'Ring IR = {l_ring_inner_r}mm', fontsize=7.5)
leader(ax_det, ceramic_outer_r, 8, 10, 13,
       f'Ceramic OR = {ceramic_outer_r}mm', fontsize=7.5)
leader(ax_det, housing_inner_r, 8, 58, 13,
       f'Housing IR = {housing_inner_r}mm', fontsize=7.5)
leader(ax_det, mesh_outer_r, housing_bottom_z + 3, 66, -15,
       f'Mesh OR = {mesh_outer_r}mm', fontsize=7.5)

# Insulation gap in detail
dim_h(ax_det, 10, ceramic_outer_r, housing_inner_r,
      f'{insulation_gap}mm gap', offset=3, fontsize=8)

# Air gap in detail
dim_h(ax_det, 7, housing_outer_r, mesh_inner_r,
      f'{air_gap}mm air', offset=-4, fontsize=7)

# Bottom disk radius
dim_h(ax_det, housing_bottom_z, 0, mesh_outer_r,
      f'R = {mesh_outer_r}mm', offset=-5, fontsize=7)

# Bolt holes callout
leader(ax_det, leg_hole_r, housing_bottom_z,
       40, -33, f'3x M6 leg bolt holes\nR = {leg_hole_r}mm\nat 40°, 160°, 280°', fontsize=7.5)

# Z reference labels
ax_det.text(1, 0.5, 'z = 0 (ceramic base)', fontsize=6, color='gray', style='italic')
ax_det.text(1, lip_z - 1.5, f'z = {lip_z} (ring)', fontsize=6, color='gray', style='italic')
ax_det.text(1, housing_bottom_z - 2, f'z = {housing_bottom_z} (bottom)', fontsize=6, color='gray', style='italic')
ax_det.text(1, ring_wall_top_z + 0.5, f'z = {ring_wall_top_z} (wall top, 2mm below TC hole)', fontsize=6, color='gray', style='italic')

ax_det.set_xlabel('Radius (mm)', fontsize=8)
ax_det.set_ylabel('Height (mm)', fontsize=8)

# Material / legend box below main view
ax.text(-90, -45, (
    'MATERIALS:\n'
    '  Body/Mesh/Disk: 304 Stainless Steel, 1.2mm\n'
    '  Ceramic: High-alumina ceramic\n'
    f'  Perf holes: Ø{perf_hole_r*2}mm, {perf_spacing}mm spacing\n'
    f'  Leg bolts: 3x M6 at {leg_hole_r}mm radius'
), fontsize=6.5, family='monospace',
   bbox=dict(boxstyle='round', fc='lightyellow', ec='gray'))

ax.text(55, -45, (
    'LEGEND:\n'
    '  /// = Stainless steel\n'
    '  ... = Perforated mesh\n'
    '  Tan = Ceramic\n'
), fontsize=6.5, family='monospace',
   bbox=dict(boxstyle='round', fc='white', ec='gray'))

draw_title_block(fig2, "Metal Body Assembly", thickness="1.2mm")
draw_tolerances_block(fig2, has_bends=True)
fig2.savefig('MetalBody_Drawing.pdf', dpi=300, bbox_inches='tight')
print("Saved MetalBody_Drawing.pdf")

plt.show()
print("\nDone! Two PDF drawing sheets saved:")
print("  1. TopCap_Drawing.pdf")
print("  2. MetalBody_Drawing.pdf")
