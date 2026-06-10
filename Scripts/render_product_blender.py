"""Photoreal product render of the REAL Heat-N-Clean geometry.

Imports the actual exported GLBs (exact dimensions), assigns physically
based materials (brushed stainless / matte ceramic / black handle), studio
lighting, Cycles GPU render.

Run:
  /Applications/Blender.app/Contents/MacOS/Blender -b -P Scripts/render_product_blender.py -- out.png
"""
import bpy, math, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLB = lambda *p: os.path.join(ROOT, "CAD Exports", *p)
OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/oven_render.png"

# ---------- clean scene ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------- materials ----------
def make_mat(name, color, metallic, rough, bump=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = rough
    if bump > 0:   # subtle brushed-metal texture
        nt = m.node_tree
        noise = nt.nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 900.0
        noise.inputs["Detail"].default_value = 2.0
        bumpn = nt.nodes.new("ShaderNodeBump")
        bumpn.inputs["Strength"].default_value = bump
        nt.links.new(noise.outputs["Fac"], bumpn.inputs["Height"])
        nt.links.new(bumpn.outputs["Normal"], bsdf.inputs["Normal"])
    return m

STEEL    = make_mat("steel",    (0.58, 0.59, 0.62), 1.0, 0.26, bump=0.05)
STEEL_D  = make_mat("steel_d",  (0.44, 0.45, 0.48), 1.0, 0.36, bump=0.05)
CERAMIC  = make_mat("ceramic",  (0.93, 0.92, 0.88), 0.0, 0.55)
HANDLE   = make_mat("handle",   (0.05, 0.05, 0.06), 0.2, 0.45)
BOLT     = make_mat("bolt",     (0.55, 0.55, 0.58), 1.0, 0.22)
FLOOR_M  = make_mat("floor",    (0.42, 0.43, 0.45), 0.0, 0.45)

# ---------- import parts (exact CAD, mm coordinates) ----------
PARTS = [
    # (path, z offset mm, material)
    (GLB("Core Split", "1_Inner_Wall_Tube.glb"),        0,   STEEL_D),
    (GLB("Core Split", "2_Outer_Perforated_Tube.glb"),  0,   STEEL),
    (GLB("Core Split", "3_Support_Ring_Full.glb"),      0,   STEEL_D),
    (GLB("Core Split", "02_Bottom_Cap.glb"),            0,   STEEL),
    (GLB("Core Split", "06_Ceramic_Cylinder.glb"),      0,   CERAMIC),
    (GLB("Core Split", "6_Ceramic_Base_Disk.glb"),      0,   CERAMIC),
    (GLB("Core Split", "4_Spacer_Ring.glb"),           59,   CERAMIC),
    (GLB("Core Split", "4_Spacer_Ring.glb"),          -24,   CERAMIC),
    (GLB("Core Split", "4_Spacer_Ring.glb"),          2.15,  CERAMIC),
    (GLB("Individual Parts", "GLB", "04a_Cap_Shell.glb"),        0, STEEL),
    (GLB("Individual Parts", "GLB", "04b_Cap_HoldDown_Ring.glb"),0, STEEL_D),
    (GLB("Lid Split", "1_Lid_Inner_Tube.glb"),           0,  STEEL_D, True),
    (GLB("Lid Split", "2_Lid_Outer_Perforated_Tube.glb"),0,  STEEL, True),
    (GLB("Lid Split", "3_Lid_Top_Disk.glb"),             0,  STEEL, True),
    (GLB("Lid Split", "4_Lid_Ceramic_Holder.glb"),       0,  STEEL_D, True),
    (GLB("Lid Split", "5_Lid_Handle.glb"),               0,  HANDLE, True),
    (GLB("Lid Split", "4_Lid_Spacer.glb"),              99,  CERAMIC, True),
    (GLB("Lid Split", "4_Lid_Spacer.glb"),             119,  CERAMIC, True),
    (GLB("Individual Parts", "GLB", "07b_Ceramic_Lid_Disk.glb"), 91, CERAMIC, True),
    (GLB("Individual Parts", "GLB", "05b_Lid_Hinge_Strap.glb"),  0, STEEL_D, True),
    (GLB("Individual Parts", "GLB", "05_Hinge_Pin.glb"),         0, BOLT),
    (GLB("Individual Parts", "GLB", "12_Steel_Tray.glb"),        0, STEEL),
    (GLB("Individual Parts", "GLB", "10_Ceramic_Feet.glb"),      0, CERAMIC),
    (GLB("Individual Parts", "GLB", "11_Controller_Box.glb"),    0, HANDLE),
]

LID_OPEN_DEG = float(os.environ.get("LID_OPEN", "0"))   # 0 = closed, e.g. 110 = open

root = bpy.data.objects.new("oven_root", None)
bpy.context.collection.objects.link(root)

# hinge pivot (mm, true z-up coords) — the lid swings on this
_HA = math.radians(292.4)
_axis_t = (-math.sin(_HA), math.cos(_HA), 0)
lid_pivot = bpy.data.objects.new("lid_pivot", None)
lid_pivot.location = (81.5*math.cos(_HA), 81.5*math.sin(_HA), 97)
lid_pivot.rotation_mode = "AXIS_ANGLE"
lid_pivot.rotation_axis_angle = (math.radians(LID_OPEN_DEG), *_axis_t)
lid_pivot.parent = root
bpy.context.collection.objects.link(lid_pivot)

def import_glb(path, dz, mat, lid=False):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    par = lid_pivot if lid else root
    for o in set(bpy.data.objects) - before:
        if o.type == "MESH":
            o.parent = par
            o.rotation_mode = "XYZ"   # importer leaves QUATERNION mode; euler is ignored without this
            o.rotation_euler = (math.radians(-90), 0, 0)   # data is glTF y-up; stand it upright
            loc = (0, 0, dz)
            if lid:   # express relative to the pivot
                loc = (-lid_pivot.location.x, -lid_pivot.location.y, dz - lid_pivot.location.z)
            o.location = loc
            o.data.materials.clear()
            o.data.materials.append(mat)
            for poly in o.data.polygons:
                poly.use_smooth = True
        elif o.type == "EMPTY":
            o.parent = par

for entry in PARTS:
    path, dz, mat = entry[0], entry[1], entry[2]
    lid = len(entry) > 3 and entry[3]
    if os.path.exists(path):
        import_glb(path, dz, mat, lid)
    else:
        print("MISSING:", path)

# ---------- procedural bolts (same numbers as the design) ----------
bolt_root = bpy.data.objects.new("bolt_root", None)
bpy.context.collection.objects.link(bolt_root)
OFF = math.radians(52.4)
def bolt_ring(z, long_, lid=False):
    par = lid_pivot if lid else bolt_root
    for k in range(6):
        a = OFF + k * math.pi / 3
        ca, sa = math.cos(a), math.sin(a)
        sx = 73.5 if long_ else 72.5
        hx = 80.6 if long_ else 78.6
        ln = 13 if long_ else 9.5
        for rad, dep, vx, rx in ((1.5, ln, 16, sx), (3.2, 2.8, 6, hx)):
            bpy.ops.mesh.primitive_cylinder_add(radius=rad, depth=dep, vertices=vx)
            o = bpy.context.object
            o.parent = par
            px, py, pz = rx*ca, rx*sa, z
            if lid:
                px -= lid_pivot.location.x; py -= lid_pivot.location.y; pz -= lid_pivot.location.z
            o.rotation_euler = (0, math.pi/2, a)
            o.location = (px, py, pz)
            o.data.materials.append(BOLT)

for z, lng, lid in [(59, True, False), (-24, True, False), (2.15, False, False),
                    (99, False, True), (119, False, True)]:
    bolt_ring(z, lng, lid)

# ---------- scale mm -> m ----------
root.scale = (0.001, 0.001, 0.001)
bolt_root.scale = (0.001, 0.001, 0.001)
scene.view_settings.exposure = -0.35

# ---------- floor ----------
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, -0.0615))
floor = bpy.context.object
floor.data.materials.append(FLOOR_M)

# ---------- lights ----------
def area(name, loc, rot, size, power):
    l = bpy.data.lights.new(name, "AREA")
    l.size = size
    l.energy = power
    o = bpy.data.objects.new(name, l)
    o.location = loc
    o.rotation_euler = rot
    bpy.context.collection.objects.link(o)

area("key",  (0.55, -0.65, 0.75), (math.radians(35), 0, math.radians(40)), 1.0, 220)
area("fill", (-0.8, -0.35, 0.45), (math.radians(60), 0, math.radians(-60)), 1.8, 60)
area("rim",  (0.15, 0.9, 0.55),  (math.radians(-50), 0, 0), 0.9, 160)

world = bpy.data.worlds.new("w")
scene.world = world
world.use_nodes = True
_wn = world.node_tree
_env = _wn.nodes.new("ShaderNodeTexEnvironment")
_hdri = glob.glob("/Applications/Blender.app/Contents/Resources/*/datafiles/studiolights/world/studio.exr")
if _hdri:
    _env.image = bpy.data.images.load(_hdri[0])
    _wn.links.new(_env.outputs["Color"], _wn.nodes["Background"].inputs["Color"])
    _wn.nodes["Background"].inputs["Strength"].default_value = 0.9
else:
    _wn.nodes["Background"].inputs["Color"].default_value = (0.16, 0.17, 0.20, 1)
    _wn.nodes["Background"].inputs["Strength"].default_value = 0.35
scene.render.film_transparent = False

# ---------- camera ----------
cam = bpy.data.cameras.new("cam")
cam.lens = 85
cam_o = bpy.data.objects.new("cam", cam)
cam_o.location = (0.58, -0.60, 0.40)
bpy.context.collection.objects.link(cam_o)
scene.camera = cam_o
tgt = bpy.data.objects.new("tgt", None)
tgt.location = (0, 0, 0.075)
bpy.context.collection.objects.link(tgt)
tr = cam_o.constraints.new("TRACK_TO")
tr.target = tgt

if os.environ.get("PROBE"):
    for o in bpy.data.objects:
        if o.type == "MESH":
            mats = [m.name if m else "None" for m in o.data.materials]
            print("PROBE", o.name[:40], mats, "verts", len(o.data.vertices))
    import sys as _s; _s.exit(0)

# ---------- render settings ----------
scene.render.engine = "CYCLES"
scene.cycles.device = "GPU"
prefs = bpy.context.preferences.addons.get("cycles")
if prefs:
    cp = prefs.preferences
    cp.compute_device_type = "METAL"
    for d in cp.get_devices_for_type("METAL"):
        d.use = True
scene.cycles.samples = 110
scene.cycles.use_denoising = True
scene.render.resolution_x = 1600
scene.render.resolution_y = 1200
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("RENDERED:", OUT)
