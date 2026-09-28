"""Photoreal cutaway of the BASE only: one-piece top cap, tubes, ceramic spacers, base disk, heater core,
support ring, bottom cap, feet, and the 18 ring bolts. The half facing the camera is sliced off so the
25 mm space under the base disk and every bolt path are visible.
Run:
  /Applications/Blender.app/Contents/MacOS/Blender -b -P Scripts/render_base_cutaway_blender.py -- out.png
"""
import bpy, bmesh, math, os, sys, glob
from mathutils import Vector, Matrix
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VF = lambda n: os.path.join(ROOT, "viewer-full", n + ".glb")
OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/base_cutaway.png"
CUT = os.environ.get("CUT", "1") == "1"
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def mat(name, color, metallic, rough):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough; return m
STEEL   = mat("steel",   (0.62, 0.63, 0.66), 1.0, 0.28)
STEEL_D = mat("steel_d", (0.48, 0.47, 0.46), 1.0, 0.38)
CAPM    = mat("capm",    (0.30, 0.45, 0.70), 0.9, 0.30)   # bottom cap tinted blue so it reads at a glance
CERAMIC = mat("ceramic", (0.93, 0.91, 0.86), 0.0, 0.6)
BOLT    = mat("bolt",    (0.12, 0.12, 0.13), 0.8, 0.35)
FLOOR   = mat("floor",   (0.85, 0.85, 0.87), 0.0, 0.5)

PARTS = [("04", CAPM), ("03", STEEL_D), ("01", STEEL_D), ("02", STEEL), ("cap", STEEL),
         ("spacer_bot", CERAMIC), ("spacer_seat", CERAMIC), ("spacer_top", CERAMIC),
         ("basedisk", CERAMIC), ("core", CERAMIC), ("feet", CERAMIC), ("legscrews", BOLT),
         ("bolts_bot", BOLT), ("bolts_seat", BOLT), ("bolts_top", BOLT)]
root = bpy.data.objects.new("root", None); bpy.context.collection.objects.link(root)
for name, m in PARTS:
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=VF(name))
    for o in set(bpy.data.objects) - before:
        if o.type != "MESH": continue
        # trimesh GLBs hold z-up millimetres; the importer turned them y-up -> undo that and bake it in
        o.parent = None; o.rotation_mode = "XYZ"
        mw = o.matrix_world.copy()
        o.data.transform(Matrix.Rotation(-math.pi/2, 4, 'X') @ mw); o.matrix_world.identity()
        o.data.materials.clear(); o.data.materials.append(m)
        for p in o.data.polygons: p.use_smooth = False
        if CUT:   # slice off the half with y < 0 (toward the camera)
            bm = bmesh.new(); bm.from_mesh(o.data)
            bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0,0,0), plane_no=(0,-1,0), clear_outer=True)
            bm.to_mesh(o.data); bm.free()
        o.parent = root
# detect up axis from the heater core: it must stand 91 mm tall in Z
zs = [ (o.matrix_world @ Vector(c)).z for o in root.children for c in o.bound_box ]
print("Z span", min(zs), max(zs))
root.scale = (0.001, 0.001, 0.001)
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, -0.0572)); bpy.context.object.data.materials.append(FLOOR)
def area(n, loc, rot, size, power):
    l = bpy.data.lights.new(n, "AREA"); l.size = size; l.energy = power
    o = bpy.data.objects.new(n, l); o.location = loc; o.rotation_euler = rot; bpy.context.collection.objects.link(o)
area("key",  (0.35, -0.7, 0.6), (math.radians(45), 0, math.radians(25)), 0.8, 140)
area("fill", (-0.6, -0.5, 0.3), (math.radians(65), 0, math.radians(-50)), 1.5, 60)
area("top",  (0, 0.1, 0.8), (0, 0, 0), 0.6, 60)
w = bpy.data.worlds.new("w"); scene.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.9, 0.9, 0.92, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.6
cam = bpy.data.cameras.new("cam"); cam.lens = 70
co = bpy.data.objects.new("cam", cam); bpy.context.collection.objects.link(co); scene.camera = co
co.location = (0.12, -0.62, 0.16)
t = bpy.data.objects.new("t", None); t.location = (0, 0, 0.022); bpy.context.collection.objects.link(t)
c = co.constraints.new("TRACK_TO"); c.target = t; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
scene.render.engine = "CYCLES"; scene.cycles.samples = 96
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences; prefs.compute_device_type = "METAL"; prefs.get_devices()
    for d in prefs.devices: d.use = True
    scene.cycles.device = "GPU"
except Exception as e: print("GPU fallback", e)
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 1800, 1400
scene.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in scene.view_settings.bl_rna.properties["view_transform"].enum_items] else "Filmic"
scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("WROTE", OUT)
