"""
CONCEPT DRAWING: Lid with ceramic FLUSH — body level with lid bottom,
only the narrower lip extends below.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# === DIMENSIONS (matching project) ===
ceramic_od = 92.5
ceramic_outer_r = ceramic_od / 2        # 46.25
lid_ring_inner_r = ceramic_outer_r - 10  # 36.25
sheet_t = 1.2
insulation_gap = 24.6
housing_inner_r = ceramic_outer_r + insulation_gap  # 70.85
housing_outer_r = housing_inner_r + sheet_t          # 72.05
air_gap = 4
mesh_inner_r = housing_outer_r + air_gap             # 76.05
mesh_outer_r = mesh_inner_r + sheet_t                # 77.25
lid_height = 35

# Ceramic disk breakdown
disk_total = 5.5
disk_body_h = 4.5     # body thickness (full OD portion)
disk_lip_h = 1.0      # lip thickness (reduced OD portion)
lip_od = 76.0
lip_r = lip_od / 2    # 38.0

# === HELPERS ===
def dim_h(ax, y, x1, x2, text, offset=3, fontsize=7, color='blue'):
    yo = y + offset
    ax.annotate('', xy=(x1, yo), xytext=(x2, yo),
                arrowprops=dict(arrowstyle='<->', color=color, lw=0.8))
    ax.text((x1 + x2) / 2, yo + 0.5, text, ha='center', va='bottom',
            fontsize=fontsize, color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.plot([x1, x1], [y, yo], color=color, lw=0.4, ls='--')
    ax.plot([x2, x2], [y, yo], color=color, lw=0.4, ls='--')

def dim_v(ax, x, y1, y2, text, offset=3, fontsize=7, color='blue'):
    xo = x + offset
    ax.annotate('', xy=(xo, y1), xytext=(xo, y2),
                arrowprops=dict(arrowstyle='<->', color=color, lw=0.8))
    ax.text(xo + 1, (y1 + y2) / 2, text, ha='left', va='center',
            fontsize=fontsize, color=color, fontweight='bold', rotation=90,
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.9))
    ax.plot([x, xo], [y1, y1], color=color, lw=0.4, ls='--')
    ax.plot([x, xo], [y2, y2], color=color, lw=0.4, ls='--')

def leader(ax, x, y, tx, ty, text, fontsize=6.5, color='darkgreen'):
    ax.annotate(text, xy=(x, y), xytext=(tx, ty),
                fontsize=fontsize, color=color, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=color, lw=0.6),
                bbox=dict(boxstyle='round,pad=0.2', fc='lightyellow', ec=color, lw=0.5))

# =====================================================================
fig = plt.figure(figsize=(24, 14))
fig.suptitle('LID ASSEMBLY — FLUSH CERAMIC CONCEPT (Sheet 4 variant)',
             fontsize=16, fontweight='bold', y=0.98)

ax_main = fig.add_axes([0.03, 0.06, 0.50, 0.88])
ax_det  = fig.add_axes([0.57, 0.06, 0.41, 0.88])

# =====================================================================
# MAIN VIEW  (full lid cross-section, local z=0 at lid base)
# =====================================================================
ax = ax_main
ax.set_title('Section B-B  —  Ceramic flush, lip extends below',
             fontsize=11, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.set_xlim(-85, 85)
ax.set_ylim(-8, 65)
ax.grid(True, alpha=0.15)

lid_z0 = 0  # lid base

# Inner housing walls
for s in [-1, 1]:
    ax.fill([s*housing_inner_r, s*housing_outer_r,
             s*housing_outer_r, s*housing_inner_r],
            [lid_z0, lid_z0, lid_z0+lid_height, lid_z0+lid_height],
            color='#C8CCD0', ec='black', lw=1.0, hatch='///')

# Outer perforated mesh
for s in [-1, 1]:
    ax.fill([s*mesh_inner_r, s*mesh_outer_r,
             s*mesh_outer_r, s*mesh_inner_r],
            [lid_z0, lid_z0, lid_z0+lid_height, lid_z0+lid_height],
            color='#D0D4D8', ec='black', lw=1.0, hatch='...')

# Bottom ring  (ceramic_outer_r → mesh_outer_r)
for s in [-1, 1]:
    ax.fill([s*ceramic_outer_r, s*mesh_outer_r,
             s*mesh_outer_r, s*ceramic_outer_r],
            [lid_z0, lid_z0, lid_z0+sheet_t, lid_z0+sheet_t],
            color='#C8CCD0', ec='black', lw=0.8, hatch='///')

# Retaining wall — only body height minus the ring thickness
wall_bot = lid_z0 + sheet_t           # 1.2
wall_top = lid_z0 + disk_body_h       # 4.5  (body top)
for s in [-1, 1]:
    ax.fill([s*ceramic_outer_r, s*(ceramic_outer_r + sheet_t),
             s*(ceramic_outer_r + sheet_t), s*ceramic_outer_r],
            [wall_bot, wall_bot, wall_top, wall_top],
            color='#C8CCD0', ec='black', lw=1.0, hatch='///')

# Retaining shelf at body top
shelf_z = wall_top
for s in [-1, 1]:
    ax.fill([s*lid_ring_inner_r, s*ceramic_outer_r,
             s*ceramic_outer_r, s*lid_ring_inner_r],
            [shelf_z, shelf_z, shelf_z+sheet_t, shelf_z+sheet_t],
            color='#C8CCD0', ec='black', lw=0.8, hatch='///')

# --- CERAMIC DISK (flush design) ---
# Body: full OD, sits from z=0 to z=4.5  (flush with lid bottom)
ax.fill([-ceramic_outer_r, ceramic_outer_r,
         ceramic_outer_r, -ceramic_outer_r],
        [lid_z0, lid_z0, lid_z0+disk_body_h, lid_z0+disk_body_h],
        color='#F5EBD8', ec='#AA8866', lw=1.2, alpha=0.55)

# Lip: reduced OD, extends BELOW lid bottom from z=-1 to z=0
ax.fill([-lip_r, lip_r, lip_r, -lip_r],
        [lid_z0 - disk_lip_h, lid_z0 - disk_lip_h, lid_z0, lid_z0],
        color='#EDE0C8', ec='#AA8866', lw=1.2, alpha=0.65)

# Top disk
top_z = lid_z0 + lid_height
ax.fill([-mesh_outer_r, mesh_outer_r, mesh_outer_r, -mesh_outer_r],
        [top_z, top_z, top_z+sheet_t, top_z+sheet_t],
        color='#C8CCD0', ec='black', lw=1.0, hatch='///')

# Handle
handle_height = 25
handle_width = 50
handle_bar_r = 4
hb = top_z + sheet_t
for xc in [-handle_width/2, handle_width/2]:
    ax.fill([xc-handle_bar_r, xc+handle_bar_r,
             xc+handle_bar_r, xc-handle_bar_r],
            [hb, hb, hb+handle_height, hb+handle_height],
            color='#B0B0B0', ec='black', lw=1.0, hatch='///')
bar_z = hb + handle_height
ax.fill([-handle_width/2-handle_bar_r, handle_width/2+handle_bar_r,
         handle_width/2+handle_bar_r, -handle_width/2-handle_bar_r],
        [bar_z-handle_bar_r, bar_z-handle_bar_r,
         bar_z+handle_bar_r, bar_z+handle_bar_r],
        color='#B0B0B0', ec='black', lw=1.0, hatch='///')

# --- DIMENSIONS (main view) ---
dim_h(ax, top_z+sheet_t, -mesh_outer_r, mesh_outer_r,
      f'Mesh OD {mesh_outer_r*2:.1f}mm', offset=10)
dim_h(ax, lid_z0-disk_lip_h, -ceramic_outer_r, ceramic_outer_r,
      f'Body OD {ceramic_od}mm', offset=-6, color='brown')
dim_h(ax, lid_z0-disk_lip_h, -lip_r, lip_r,
      f'Lip OD {lip_od}mm', offset=-12, color='#8B4513')

dim_v(ax, mesh_outer_r, lid_z0, lid_z0+lid_height,
      f'{lid_height}mm\nlid height', offset=6)

# Body + lip breakdown
dim_v(ax, -ceramic_outer_r, lid_z0, lid_z0+disk_body_h,
      f'{disk_body_h}mm\nbody', offset=-12, fontsize=6, color='brown')
dim_v(ax, -lip_r, lid_z0-disk_lip_h, lid_z0,
      f'{disk_lip_h}mm\nlip', offset=-8, fontsize=6, color='#8B4513')

# Wall height
wall_h = wall_top - wall_bot
dim_v(ax, ceramic_outer_r+sheet_t, wall_bot, wall_top,
      f'{wall_h:.1f}mm\nwall', offset=2, fontsize=6)

leader(ax, 0, lid_z0 - disk_lip_h/2,
       -55, -5, f'Lip extends {disk_lip_h}mm\nbelow lid bottom\n({lip_od}mm OD)', color='#8B4513')
leader(ax, 0, lid_z0 + disk_body_h/2,
       -55, disk_body_h + 3, f'Body FLUSH with lid base\n({ceramic_od}mm OD)', color='brown')

leader(ax, (ceramic_outer_r+housing_inner_r)/2, lid_height/2+3,
       75, lid_height/2+8, f'Insulation gap\n{insulation_gap}mm')
leader(ax, (housing_outer_r+mesh_inner_r)/2, lid_height/2-3,
       78, lid_height/2-2, f'Air gap\n{air_gap}mm')

ax.axhline(y=0, color='red', lw=0.6, ls=':', alpha=0.5)
ax.text(-82, 0.3, 'LID BASE (z=0)', fontsize=6, color='red', fontstyle='italic')

ax.set_xlabel('Radius (mm)', fontsize=8)
ax.set_ylabel('Height from lid base (mm)', fontsize=8)

# =====================================================================
# DETAIL VIEW  (zoomed ceramic pocket — right half)
# =====================================================================
ax = ax_det
ax.set_title('DETAIL B — Flush Ceramic Pocket (4x scale)',
             fontsize=11, fontweight='bold', pad=10, color='red')
ax.set_aspect('equal')
ax.set_xlim(25, 75)
ax.set_ylim(-4, 10)
ax.grid(True, alpha=0.2)

# Bottom ring
ax.fill([ceramic_outer_r, mesh_outer_r, mesh_outer_r, ceramic_outer_r],
        [lid_z0, lid_z0, lid_z0+sheet_t, lid_z0+sheet_t],
        color='#C8CCD0', ec='black', lw=1.5, hatch='///')

# Retaining wall (shorter — only body height above ring)
ax.fill([ceramic_outer_r, ceramic_outer_r+sheet_t,
         ceramic_outer_r+sheet_t, ceramic_outer_r],
        [wall_bot, wall_bot, wall_top, wall_top],
        color='#A8B8C0', ec='black', lw=1.5, hatch='///')

# Shelf at body top
ax.fill([lid_ring_inner_r, ceramic_outer_r,
         ceramic_outer_r, lid_ring_inner_r],
        [shelf_z, shelf_z, shelf_z+sheet_t, shelf_z+sheet_t],
        color='#A8B8C0', ec='black', lw=1.5, hatch='///')

# Ceramic BODY (flush with lid base, full OD)
ax.fill([lid_ring_inner_r+1, ceramic_outer_r,
         ceramic_outer_r, lid_ring_inner_r+1],
        [lid_z0, lid_z0, lid_z0+disk_body_h, lid_z0+disk_body_h],
        color='#F5EBD8', ec='#AA8866', lw=1.2, alpha=0.6)

# Ceramic LIP (extends below, reduced OD)
ax.fill([lid_ring_inner_r+1, lip_r,
         lip_r, lid_ring_inner_r+1],
        [lid_z0-disk_lip_h, lid_z0-disk_lip_h, lid_z0, lid_z0],
        color='#EDE0C8', ec='#AA8866', lw=1.5, alpha=0.7)

# Draw the lip/body boundary clearly
ax.plot([lid_ring_inner_r+1, ceramic_outer_r], [lid_z0, lid_z0],
        color='#AA8866', lw=1.0, ls='--')

# Inner housing wall (clipped)
ax.fill([housing_inner_r, housing_outer_r, housing_outer_r, housing_inner_r],
        [-3, -3, 10, 10],
        color='#C8CCD0', ec='black', lw=1.0, hatch='///')

# Outer mesh (clipped)
ax.fill([mesh_inner_r, mesh_outer_r, mesh_outer_r, mesh_inner_r],
        [-3, -3, 10, 10],
        color='#D0D4D8', ec='black', lw=1.0, hatch='...')

# --- DETAIL DIMENSIONS ---
# Shelf width
dim_h(ax, shelf_z, lid_ring_inner_r, ceramic_outer_r,
      f'{ceramic_outer_r - lid_ring_inner_r:.0f}mm shelf', offset=1.5, fontsize=8)

# Body height
dim_v(ax, (lid_ring_inner_r+ceramic_outer_r)/2, lid_z0, lid_z0+disk_body_h,
      f'{disk_body_h}mm\nbody', offset=-8, fontsize=8, color='brown')

# Lip height
dim_v(ax, lip_r, lid_z0-disk_lip_h, lid_z0,
      f'{disk_lip_h}mm\nlip', offset=2, fontsize=8, color='#8B4513')

# Wall height
dim_v(ax, ceramic_outer_r+sheet_t, wall_bot, wall_top,
      f'{wall_h:.1f}mm\nwall', offset=2, fontsize=8)

# Sheet thickness
leader(ax, (ceramic_outer_r+mesh_outer_r)/2, lid_z0+sheet_t/2,
       58, -2, f't = {sheet_t}mm', fontsize=8)

# Radii
leader(ax, lip_r, lid_z0-disk_lip_h/2,
       30, -3, f'Lip OR = {lip_r}mm', fontsize=7.5, color='#8B4513')
leader(ax, ceramic_outer_r, wall_top+0.5,
       40, 8, f'Body OR = {ceramic_outer_r}mm', fontsize=7.5, color='brown')
leader(ax, housing_inner_r, 6,
       60, 8, f'Housing IR = {housing_inner_r}mm', fontsize=7.5)

# Z references
ax.axhline(y=0, color='red', lw=0.6, ls=':', alpha=0.5)
ax.text(26, 0.2, 'z = 0  (lid base)', fontsize=6, color='red', fontstyle='italic')
ax.text(26, -disk_lip_h-0.5, f'z = -{disk_lip_h}  (lip bottom)',
        fontsize=5.5, color='#8B4513', fontstyle='italic')
ax.text(26, disk_body_h+0.2, f'z = {disk_body_h}  (body top / shelf)',
        fontsize=5.5, color='brown', fontstyle='italic')

# Callout circle on main view
detail_cx = (lid_ring_inner_r + housing_inner_r) / 2
detail_cy = wall_bot + 2
circ = plt.Circle((detail_cx, detail_cy), 15,
                   fill=False, ec='red', lw=1.5, ls='--')
ax_main.add_patch(circ)
ax_main.text(detail_cx + 17, detail_cy + 10,
             'DETAIL B', fontsize=9, color='red', fontweight='bold')

# Save
fig.savefig('LidFlush_Concept.pdf', bbox_inches='tight', dpi=150)
print("Saved LidFlush_Concept.pdf")
plt.close(fig)
