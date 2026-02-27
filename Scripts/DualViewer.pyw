"""
DUAL VIEWER - Ceramic Core + Sheet Metal Housing
Interactive viewer with transparency controls

Controls:
- Drag to rotate
- Scroll to zoom
- Right-click drag to pan
- Sliders adjust transparency
"""
import pyvista as pv
import numpy as np
import os

# =============================================================================
# PARAMETERS - ADJUST THESE TO MATCH YOUR DESIGN
# =============================================================================

# Ceramic core (from your existing design)
ceramic_od = 92.5
ceramic_id = 81.5
ceramic_height = 91
ceramic_wall = 5.5

# Lid
lid_od = 92.5
lid_thickness = 5.5

# Insulation gap
insulation_thickness = 15

# Housing
housing_gap = 3
sheet_metal = 1.5
housing_inner_dia = ceramic_od + (insulation_thickness * 2) + (housing_gap * 2)
housing_outer_dia = housing_inner_dia + (sheet_metal * 2)
housing_height = ceramic_height + lid_thickness + 15  # Extra clearance at top

# Base plate
base_plate_dia = housing_outer_dia + 20
base_plate_thick = sheet_metal

# =============================================================================
# CREATE GEOMETRY
# =============================================================================

def create_ceramic_core():
    """Create the ceramic cylinder + lid"""
    # Outer cylinder
    outer = pv.Cylinder(radius=ceramic_od/2, height=ceramic_height,
                        center=(0, 0, ceramic_height/2), direction=(0, 0, 1),
                        resolution=64)
    # Inner bore (to subtract)
    inner = pv.Cylinder(radius=ceramic_id/2, height=ceramic_height + 2,
                        center=(0, 0, ceramic_height/2), direction=(0, 0, 1),
                        resolution=64)

    # Boolean difference for hollow cylinder
    ceramic_cyl = outer.boolean_difference(inner)

    # Lid on top
    lid = pv.Cylinder(radius=lid_od/2, height=lid_thickness,
                      center=(0, 0, ceramic_height + lid_thickness/2), direction=(0, 0, 1),
                      resolution=64)

    # Combine
    ceramic = ceramic_cyl.merge(lid)
    return ceramic

def create_housing():
    """Create the sheet metal housing"""
    # Base plate
    base = pv.Cylinder(radius=base_plate_dia/2, height=base_plate_thick,
                       center=(0, 0, -base_plate_thick/2), direction=(0, 0, 1),
                       resolution=64)

    # Housing wall (outer)
    wall_outer = pv.Cylinder(radius=housing_outer_dia/2, height=housing_height,
                             center=(0, 0, housing_height/2), direction=(0, 0, 1),
                             resolution=64)
    # Housing wall (inner)
    wall_inner = pv.Cylinder(radius=housing_inner_dia/2, height=housing_height + 2,
                             center=(0, 0, housing_height/2), direction=(0, 0, 1),
                             resolution=64)

    # Boolean difference for hollow wall
    wall = wall_outer.boolean_difference(wall_inner)

    # Combine base + wall
    housing = base.merge(wall)
    return housing

def create_insulation():
    """Create the insulation layer (visual only)"""
    ins_outer = pv.Cylinder(radius=(ceramic_od/2 + insulation_thickness),
                            height=ceramic_height + lid_thickness,
                            center=(0, 0, (ceramic_height + lid_thickness)/2),
                            direction=(0, 0, 1), resolution=64)
    ins_inner = pv.Cylinder(radius=ceramic_od/2 + 0.5,
                            height=ceramic_height + lid_thickness + 2,
                            center=(0, 0, (ceramic_height + lid_thickness)/2),
                            direction=(0, 0, 1), resolution=64)

    insulation = ins_outer.boolean_difference(ins_inner)
    return insulation

# =============================================================================
# CREATE MESHES
# =============================================================================
print("Creating geometry...")
ceramic = create_ceramic_core()
housing = create_housing()
insulation = create_insulation()
print("Done!")

# =============================================================================
# INTERACTIVE VIEWER
# =============================================================================

plotter = pv.Plotter(title="Glass Heat Station - Dual Viewer")
plotter.set_background('white')

# Add meshes with initial opacity
ceramic_actor = plotter.add_mesh(ceramic, color='coral', opacity=1.0,
                                  smooth_shading=True, specular=0.5,
                                  label='Ceramic Core')

insulation_actor = plotter.add_mesh(insulation, color='lightyellow', opacity=0.3,
                                     smooth_shading=True,
                                     label='Insulation')

housing_actor = plotter.add_mesh(housing, color='silver', opacity=0.6,
                                  smooth_shading=True, specular=0.8, metallic=True,
                                  label='Sheet Metal Housing')

# Add axes
plotter.show_axes()
plotter.add_axes(interactive=True)

# =============================================================================
# OPACITY SLIDERS
# =============================================================================

def update_ceramic_opacity(value):
    ceramic_actor.GetProperty().SetOpacity(value)

def update_housing_opacity(value):
    housing_actor.GetProperty().SetOpacity(value)

def update_insulation_opacity(value):
    insulation_actor.GetProperty().SetOpacity(value)

# Ceramic opacity slider
plotter.add_slider_widget(
    update_ceramic_opacity,
    [0, 1], value=1.0,
    title="Ceramic",
    pointa=(0.02, 0.1), pointb=(0.18, 0.1),
    style='modern'
)

# Housing opacity slider
plotter.add_slider_widget(
    update_housing_opacity,
    [0, 1], value=0.6,
    title="Housing",
    pointa=(0.02, 0.2), pointb=(0.18, 0.2),
    style='modern'
)

# Insulation opacity slider
plotter.add_slider_widget(
    update_insulation_opacity,
    [0, 1], value=0.3,
    title="Insulation",
    pointa=(0.02, 0.3), pointb=(0.18, 0.3),
    style='modern'
)

# =============================================================================
# INFO TEXT
# =============================================================================
info_text = f"""
DIMENSIONS:
Ceramic: {ceramic_od}mm OD x {ceramic_height}mm H
Insulation: {insulation_thickness}mm thick
Housing: {housing_outer_dia:.1f}mm OD x {housing_height}mm H

CONTROLS:
- Drag to rotate
- Scroll to zoom
- Right-drag to pan
- Sliders adjust transparency
"""

plotter.add_text(info_text, position='upper_right', font_size=9, color='black')

# =============================================================================
# SHOW
# =============================================================================
print("\nOpening viewer...")
print("- Drag to rotate")
print("- Scroll to zoom")
print("- Use sliders to adjust transparency")
plotter.show()
