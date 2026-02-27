"""
Blender photorealistic render script for Heat-N-Clean Glass Oven.

Imports the GLB assembly, assigns realistic PBR materials to each part
(brushed steel, matte ceramic, glowing coil, etc.), sets up studio
lighting, and renders to PNG.

Usage (headless):
    /Applications/Blender.app/Contents/MacOS/Blender \
        --background --factory-startup --python render_blender.py -- \
        --input "CAD Exports/Assembly_LidOff.glb" \
        --output "Renders/LidOff_Hero.png" \
        --samples 256

    Or with lid open:
    /Applications/Blender.app/Contents/MacOS/Blender \
        --background --factory-startup --python render_blender.py -- \
        --input "CAD Exports/Assembly_LidOpen.glb" \
        --output "Renders/LidOpen_Hero.png" \
        --samples 256

    Options:
        --input         GLB file to import
        --output        PNG output path
        --samples       Render samples (default 256, lower=faster)
        --resolution    Width Height (default 1920 1080)
        --transparent   Transparent background (for product shots)
        --angle         Camera angle preset: front, back, top, 3/4 (default 3/4)
"""

import bpy
import sys
import os
import math
from mathutils import Vector


# ═══════════════════════════════════════════════════════════════
# Parse command-line arguments
# ═══════════════════════════════════════════════════════════════
def get_script_args():
    argv = sys.argv
    if "--" in argv:
        return argv[argv.index("--") + 1:]
    return []

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", default="CAD Exports/Assembly_LidOff.glb")
parser.add_argument("--output", default="Renders/HeatNClean_Render.png")
parser.add_argument("--samples", type=int, default=256)
parser.add_argument("--resolution", type=int, nargs=2, default=[1920, 1080])
parser.add_argument("--transparent", action="store_true")
parser.add_argument("--angle", choices=["front", "back", "top", "3/4"], default="3/4")
args = parser.parse_args(get_script_args())

# Resolve paths relative to this script's directory
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(project_dir, args.input) if not os.path.isabs(args.input) else args.input
output_path = os.path.join(project_dir, args.output) if not os.path.isabs(args.output) else args.output

# Create output directory
os.makedirs(os.path.dirname(output_path), exist_ok=True)

print(f"Input:  {input_path}")
print(f"Output: {output_path}")


# ═══════════════════════════════════════════════════════════════
# Clear scene and import GLB
# ═══════════════════════════════════════════════════════════════
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=input_path)

imported = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(f"\nImported {len(imported)} mesh objects:")
for obj in imported:
    bb = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    bmin = Vector(map(min, zip(*bb)))
    bmax = Vector(map(max, zip(*bb)))
    print(f"  {obj.name:30s}  X:[{bmin.x:7.1f},{bmax.x:7.1f}]  Y:[{bmin.y:7.1f},{bmax.y:7.1f}]  Z:[{bmin.z:7.1f},{bmax.z:7.1f}]")


# ═══════════════════════════════════════════════════════════════
# Material definitions — realistic PBR for each part
# ═══════════════════════════════════════════════════════════════

def make_material(name, base_color, metallic=0.0, roughness=0.5,
                  emission_color=None, emission_strength=0.0,
                  subsurface=0.0, subsurface_color=None, clearcoat=0.0):
    """Create a Principled BSDF material with PBR properties."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get('Principled BSDF')

    bsdf.inputs['Base Color'].default_value = base_color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness

    # Emission (for glowing coil)
    if emission_color:
        # Blender 4.x: "Emission Color" + "Emission Strength"
        # Blender 3.x: "Emission" + "Emission Strength"
        for name_try in ['Emission Color', 'Emission']:
            if name_try in bsdf.inputs:
                bsdf.inputs[name_try].default_value = emission_color
                break
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emission_strength

    # Subsurface scattering (for ceramic translucency)
    for name_try in ['Subsurface Weight', 'Subsurface']:
        if name_try in bsdf.inputs:
            bsdf.inputs[name_try].default_value = subsurface
            break

    if subsurface_color and 'Subsurface Color' in bsdf.inputs:
        bsdf.inputs['Subsurface Color'].default_value = subsurface_color

    # Clearcoat (for glossy finishes)
    for name_try in ['Coat Weight', 'Clearcoat']:
        if name_try in bsdf.inputs:
            bsdf.inputs[name_try].default_value = clearcoat
            break

    return mat


def make_brushed_steel(name="Brushed Steel", tint=(0.58, 0.59, 0.61, 1.0), roughness=0.32):
    """Brushed stainless steel with anisotropic-like noise texture."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf = nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = tint
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = roughness

    # Specular (version-safe)
    for n in ['Specular IOR Level', 'Specular']:
        if n in bsdf.inputs:
            bsdf.inputs[n].default_value = 0.6
            break

    # Noise texture stretched in one axis → brushed look
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (1.0, 40.0, 1.0)

    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 150.0
    noise.inputs['Detail'].default_value = 6.0

    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-200, -100)
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (roughness - 0.08, roughness - 0.08, roughness - 0.08, 1)
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (roughness + 0.08, roughness + 0.08, roughness + 0.08, 1)

    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Roughness'])

    return mat


# ── Create all materials ──────────────────────────────────────

# Main housing — brushed stainless steel
mat_housing = make_brushed_steel(
    "Housing Steel", tint=(0.58, 0.59, 0.61, 1.0), roughness=0.32
)

# Caps — slightly different steel tone
mat_caps = make_brushed_steel(
    "Cap Steel", tint=(0.55, 0.56, 0.58, 1.0), roughness=0.28
)

# Lid — polished steel with clearcoat
mat_lid = make_brushed_steel(
    "Lid Steel", tint=(0.60, 0.61, 0.63, 1.0), roughness=0.25
)

# Hinge pin — darker steel
mat_hinge = make_material(
    "Hinge Pin", base_color=(0.45, 0.46, 0.48, 1.0),
    metallic=1.0, roughness=0.4
)

# Screws — dark oxidized steel
mat_screws = make_material(
    "Screws", base_color=(0.15, 0.15, 0.17, 1.0),
    metallic=1.0, roughness=0.55
)

# Ceramic cylinder and disks — warm matte white
mat_ceramic = make_material(
    "Ceramic", base_color=(0.92, 0.90, 0.85, 1.0),
    metallic=0.0, roughness=0.85,
    subsurface=0.03, subsurface_color=(0.95, 0.90, 0.82, 1.0)
)

# Ceramic feet — slightly darker/warmer
mat_feet = make_material(
    "Ceramic Feet", base_color=(0.88, 0.85, 0.80, 1.0),
    metallic=0.0, roughness=0.9,
    subsurface=0.02
)

# Kanthal coil — orange glow (like it's heated)
mat_coil = make_material(
    "Kanthal Coil", base_color=(0.8, 0.25, 0.02, 1.0),
    metallic=1.0, roughness=0.6,
    emission_color=(1.0, 0.45, 0.05, 1.0), emission_strength=5.0
)

# Thermocouple — green-tinted metal
mat_thermocouple = make_material(
    "Thermocouple", base_color=(0.35, 0.50, 0.35, 1.0),
    metallic=0.8, roughness=0.45
)

# Controller box — light gray steel
mat_controller = make_brushed_steel(
    "Controller", tint=(0.62, 0.63, 0.65, 1.0), roughness=0.35
)

# Steel tray — matte steel
mat_tray = make_brushed_steel(
    "Tray Steel", tint=(0.50, 0.51, 0.53, 1.0), roughness=0.45
)

# Wiring conduit — dark rubber/plastic look
mat_conduit = make_material(
    "Conduit", base_color=(0.08, 0.08, 0.10, 1.0),
    metallic=0.0, roughness=0.75
)


# ═══════════════════════════════════════════════════════════════
# Assign materials to parts by name matching
# ═══════════════════════════════════════════════════════════════

MATERIAL_MAP = [
    # (pattern in object name, material) — checked in order, first match wins
    ("base body",       mat_housing),
    ("bottom cap",      mat_caps),
    ("top cap",         mat_caps),
    ("ceramic cylinder", mat_ceramic),
    ("ceramic base",    mat_ceramic),
    ("ceramic disk",    mat_ceramic),
    ("lid",             mat_lid),
    ("hinge",           mat_hinge),
    ("kanthal",         mat_coil),
    ("coil",            mat_coil),
    ("thermocouple",    mat_thermocouple),
    ("ceramic feet",    mat_feet),
    ("feet",            mat_feet),
    ("controller",      mat_controller),
    ("tray",            mat_tray),
    ("conduit",         mat_conduit),
    ("wiring",          mat_conduit),
    ("leg screw",       mat_screws),
    ("cap screw",       mat_screws),
    ("screw",           mat_screws),
]

for obj in imported:
    name_lower = obj.name.lower()
    assigned = False
    for pattern, mat in MATERIAL_MAP:
        if pattern in name_lower:
            obj.data.materials.clear()
            obj.data.materials.append(mat)
            print(f"  {obj.name} → {mat.name}")
            assigned = True
            break
    if not assigned:
        # Default to housing steel
        obj.data.materials.clear()
        obj.data.materials.append(mat_housing)
        print(f"  {obj.name} → Housing Steel (default)")

    # Smooth shading for all parts
    for poly in obj.data.polygons:
        poly.use_smooth = True


# ═══════════════════════════════════════════════════════════════
# Studio lighting — three-point + fill
# ═══════════════════════════════════════════════════════════════

# Bright studio background
world = bpy.data.worlds.new("Studio")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.7, 0.7, 0.72, 1.0)
    bg.inputs['Strength'].default_value = 1.5


def add_area_light(name, location, rotation, energy, size=2.0, color=(1, 1, 1)):
    light_data = bpy.data.lights.new(name=name, type='AREA')
    light_data.energy = energy
    light_data.size = size
    light_data.color = color[:3]
    light_obj = bpy.data.objects.new(name, light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = location
    light_obj.rotation_euler = rotation
    return light_obj


# Compute scene center and size for light positioning
min_co = Vector((float('inf'),) * 3)
max_co = Vector((float('-inf'),) * 3)
for obj in imported:
    for corner in obj.bound_box:
        wc = obj.matrix_world @ Vector(corner)
        min_co = Vector(map(min, min_co, wc))
        max_co = Vector(map(max, max_co, wc))

center = (min_co + max_co) / 2
scene_size = (max_co - min_co).length
print(f"\nScene bounds:")
print(f"  min: ({min_co.x:.1f}, {min_co.y:.1f}, {min_co.z:.1f})")
print(f"  max: ({max_co.x:.1f}, {max_co.y:.1f}, {max_co.z:.1f})")
print(f"  center: ({center.x:.1f}, {center.y:.1f}, {center.z:.1f})")
print(f"  size: {scene_size:.1f}")
light_dist = scene_size * 2.5

# ── Axis mapping after GLB import ──────────────────────────────
# Blender X = left-right (oven at X≈0, controller at X≈180)
# Blender Y = inverted vertical (-Y is UP, +Y is DOWN/ground)
# Blender Z = front-back (symmetric)
# Oven opening faces -Y (upward). Tray is at max Y (bottom).

# Key light — upper right (above = more negative Y)
add_area_light("Key_Light",
    location=(center.x + light_dist * 0.6, center.y - light_dist * 0.7, center.z + light_dist * 0.3),
    rotation=(math.radians(50), 0, math.radians(130)),
    energy=scene_size * 800,
    size=scene_size * 2.0,
    color=(1.0, 0.97, 0.95))

# Fill light — opposite side
add_area_light("Fill_Light",
    location=(center.x - light_dist * 0.6, center.y - light_dist * 0.3, center.z - light_dist * 0.4),
    rotation=(math.radians(65), 0, math.radians(-120)),
    energy=scene_size * 400,
    size=scene_size * 2.5,
    color=(0.95, 0.97, 1.0))

# Rim light — behind and above
add_area_light("Rim_Light",
    location=(center.x + light_dist * 0.1, center.y - light_dist * 0.5, center.z + light_dist * 0.6),
    rotation=(math.radians(-40), 0, math.radians(180)),
    energy=scene_size * 500,
    size=scene_size * 1.5,
    color=(1.0, 1.0, 1.0))

# Bottom bounce — below scene (positive Y = below)
add_area_light("Bounce_Light",
    location=(center.x, center.y + light_dist * 0.3, center.z),
    rotation=(math.radians(-80), 0, 0),
    energy=scene_size * 200,
    size=scene_size * 3.0,
    color=(0.9, 0.92, 0.95))

# Top light — above scene (negative Y = above)
add_area_light("Top_Light",
    location=(center.x, center.y - light_dist * 0.8, center.z),
    rotation=(math.radians(0), 0, 0),
    energy=scene_size * 300,
    size=scene_size * 3.0,
    color=(1.0, 1.0, 1.0))

# Ground plane — at bottom of scene (max Y = ground level)
# Rotate 90° around X so plane is in XZ (horizontal)
bpy.ops.mesh.primitive_plane_add(size=scene_size * 5, location=(center.x, max_co.y, center.z))
ground = bpy.context.active_object
ground.name = "Ground"
ground.rotation_euler = (math.radians(90), 0, 0)

# Ground material — light matte surface
ground_mat = make_material("Ground", (0.75, 0.75, 0.77, 1.0), roughness=0.95)
ground.data.materials.clear()
ground.data.materials.append(ground_mat)


# ═══════════════════════════════════════════════════════════════
# Camera setup
# ═══════════════════════════════════════════════════════════════

cam_data = bpy.data.cameras.new("Camera")
cam_data.lens = 65  # slight telephoto, less distortion for product shots
cam_data.clip_start = 0.01
cam_data.clip_end = scene_size * 20
cam_obj = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Camera distance — zoom out enough to see entire scene
cam_dist = scene_size * 2.2

# Camera angle presets — axes: X=left-right, Y=inverted vertical, Z=front-back
# "up" = -Y, "front" = -Z (arbitrary, shows oven from side)
angle_presets = {
    "3/4":  (0.15, -0.35, -0.92),   # product photo — front, slight side, looking down into chamber
    "front": (0.0, -0.35, -1.0),    # straight front, looking down into chamber
    "back":  (0.0, -0.12, 1.0),     # from behind
    "top":   (0.1, -1.0, -0.2),     # bird's eye (looking down from above = far -Y)
}

direction = Vector(angle_presets[args.angle]).normalized()
cam_obj.location = center + direction * cam_dist
print(f"\nCamera position: ({cam_obj.location.x:.1f}, {cam_obj.location.y:.1f}, {cam_obj.location.z:.1f})")
print(f"Camera distance: {cam_dist:.1f}")
print(f"Direction: ({direction.x:.3f}, {direction.y:.3f}, {direction.z:.3f})")

# Point camera at scene center — build rotation with -Y as "up"
from mathutils import Matrix
forward = (center - cam_obj.location).normalized()
world_up = Vector((0, -1, 0))  # -Y is up in our scene
right = forward.cross(world_up).normalized()
cam_up = right.cross(forward).normalized()
rot_mat = Matrix((right, cam_up, -forward)).transposed().to_3x3()
cam_obj.rotation_euler = rot_mat.to_euler()

# Depth of field (subtle, for product feel)
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = (center - cam_obj.location).length
cam_data.dof.aperture_fstop = 8.0  # sharp but with slight falloff


# ═══════════════════════════════════════════════════════════════
# Render settings
# ═══════════════════════════════════════════════════════════════

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = args.resolution[0]
scene.render.resolution_y = args.resolution[1]
scene.render.resolution_percentage = 100

# Output
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '16'
scene.render.film_transparent = args.transparent

# Cycles settings
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
try:
    scene.cycles.denoiser = 'OPENIMAGEDENOISE'
except:
    pass

# Try GPU rendering (Metal on Mac, CUDA/OptiX on PC)
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for compute_type in ['METAL', 'OPTIX', 'HIP', 'CUDA']:
        try:
            prefs.compute_device_type = compute_type
            prefs.get_devices()
            for device in prefs.devices:
                device.use = True
            scene.cycles.device = 'GPU'
            print(f"\nGPU rendering: {compute_type}")
            break
        except:
            continue
    else:
        print("\nNo GPU found, using CPU")
        scene.cycles.device = 'CPU'
except:
    scene.cycles.device = 'CPU'

# Color management — filmic for photorealistic look
scene.view_settings.view_transform = 'Filmic'
scene.view_settings.look = 'Medium High Contrast'

# Output path
scene.render.filepath = output_path

print(f"\nRendering at {args.resolution[0]}x{args.resolution[1]}, {args.samples} samples...")
print(f"Camera angle: {args.angle}")

# Render
bpy.ops.render.render(write_still=True)

print(f"\nDone! Saved to: {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024:.0f} KB")
