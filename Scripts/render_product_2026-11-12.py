"""Photoreal product render of the CURRENT Heat-N-Clean oven (FAB_PACKAGE_2026-11-12).

Geometry: viewer-full/ (base) and viewer-lid-full/ (lid) GLBs, which build_current_package.py
writes from FAB_PACKAGE_2026-11-12. They are already in assembly position (z-up, mm), so nothing
is moved except the lid, which swings on the hinge (axis tangent at 257.5 deg, pivot r 70.1,
z 100.86 (98.2 before R2), the same numbers as viewer-complete.html).

Run (headless, M5):
  /Applications/Blender.app/Contents/MacOS/Blender -b -P Scripts/render_product_2026-11-12.py -- out.png
Env: LID=100 (deg open, 0 = closed)  SAMPLES=512  SCALE=100 (% of 2400x1600)  TRAY=0  AZ=78  EL=14
2026-11-12 finals: LID=100 / LID=0 with AZ=43.1 (the 11-08 AZ 78 turned with the hinge 292.4 -> 257.5, same look) -> Renders/product_2026-11-12/
"""
import bpy, math, os, sys, glob, time
import mathutils
from bpy_extras.object_utils import world_to_camera_view

T0 = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/oven_render.png"
LID = float(os.environ.get("LID", "100"))
SAMPLES = int(os.environ.get("SAMPLES", "512"))
SCALE = int(os.environ.get("SCALE", "100"))
TRAY = os.environ.get("TRAY", "0") == "1"
AZ = math.radians(float(os.environ.get("AZ", "78")))
EL = math.radians(float(os.environ.get("EL", "14")))

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
col = scene.collection

# ---------------- materials ----------------
def principled(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree, m.node_tree.nodes["Principled BSDF"]

def steel(name, color, rough, aniso, rough_var=0.06):
    m, nt, b = principled(name)
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = 1.0
    b.inputs["Anisotropic"].default_value = aniso
    # brushing runs around the oven axis (local -Y is up in the imported mesh data)
    tg = nt.nodes.new("ShaderNodeTangent"); tg.direction_type = "RADIAL"; tg.axis = "Y"
    nt.links.new(tg.outputs["Tangent"], b.inputs["Tangent"])
    # fine streaky roughness variation + micro bump = brushed grain
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = (2.0, 0.02, 2.0)
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3.0; nz.inputs["Detail"].default_value = 8.0
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["To Min"].default_value = rough - rough_var; mr.inputs["To Max"].default_value = rough + rough_var
    nt.links.new(nz.outputs["Fac"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.03; bp.inputs["Distance"].default_value = 0.0002
    nt.links.new(nz.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m

def ceramic(name):
    m, nt, b = principled(name)
    b.inputs["Base Color"].default_value = (0.80, 0.795, 0.775, 1)
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Roughness"].default_value = 0.62
    b.inputs["Subsurface Weight"].default_value = 0.08
    b.inputs["Subsurface Radius"].default_value = (0.6, 0.55, 0.5)
    b.inputs["Subsurface Scale"].default_value = 0.5
    b.inputs["Specular IOR Level"].default_value = 0.35
    nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 400.0
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.04
    nt.links.new(nz.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m

def ceramic_lid(name):
    # lid underside faces the key light head-on: a touch lower + warmer albedo keeps its shading
    m = ceramic(name)
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.66, 0.63, 0.58, 1)
    return m

def dark_metal(name):
    m, nt, b = principled(name)
    b.inputs["Base Color"].default_value = (0.10, 0.10, 0.105, 1)
    b.inputs["Metallic"].default_value = 1.0
    b.inputs["Roughness"].default_value = 0.34
    return m

STEEL   = steel("steel_304_brushed", (0.66, 0.66, 0.67), 0.26, 0.65)
STEEL_I = steel("steel_304_inner",   (0.55, 0.55, 0.56), 0.34, 0.5)
CERAMIC = ceramic("alumina_white")
DARK    = steel("fastener_steel", (0.50, 0.50, 0.51), 0.22, 0.4)   # brushed/polished steel bolts + nuts
CERAMIC_LID = ceramic_lid("alumina_lid_disk")

# ---------------- import the current assembly ----------------
B = lambda f: os.path.join(ROOT, "viewer-full", f + ".glb")
L = lambda f: os.path.join(ROOT, "viewer-lid-full", f + ".glb")
BASE_PARTS = [  # (file, material)
    ("feet", CERAMIC), ("legscrews", DARK), ("04", STEEL), ("spacer_bot", CERAMIC), ("bolts_bot", DARK),
    ("03", STEEL_I), ("basedisk", CERAMIC), ("spacer_seat", CERAMIC), ("bolts_seat", DARK),
    ("01", STEEL_I), ("core", CERAMIC), ("spacer_top", CERAMIC), ("bolts_top", DARK),
    ("02", STEEL), ("cap", STEEL),
] + ([("tray", STEEL_I)] if TRAY else [])
LID_PARTS = [
    ("09", STEEL), ("liddisk", CERAMIC_LID), ("06", STEEL_I), ("spacer_low", CERAMIC), ("bolts_low", DARK),
    ("07", STEEL), ("spacer_high", CERAMIC), ("08", STEEL), ("bolts_high", DARK), ("10", STEEL),
    ("11", STEEL), ("13", STEEL),
]

def empty(name, parent=None, loc=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); col.objects.link(e)
    e.parent = parent; e.location = loc
    return e

root = empty("oven_root"); root.scale = (0.001,) * 3          # mm -> m
HA = math.radians(257.5)
HC = mathutils.Vector((70.1 * math.cos(HA), 70.1 * math.sin(HA), 100.86))
HAX = mathutils.Vector((-math.sin(HA), math.cos(HA), 0))
lid_pivot = empty("lid_pivot", root, HC)
lid_pivot.rotation_mode = "AXIS_ANGLE"
lid_pivot.rotation_axis_angle = (math.radians(LID), *HAX)
lid_inner = empty("lid_inner", lid_pivot, -HC)

def zfix(parent):
    # the GLBs carry z-up mm coords; the glTF importer assumes y-up, so undo its swap
    e = empty("zfix", parent); e.rotation_euler = (math.radians(-90), 0, 0)
    return e
zb, zl = zfix(root), zfix(lid_inner)

MISSING = []
def import_part(path, mat, par):
    if not os.path.exists(path):
        MISSING.append(path); return
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = set(bpy.data.objects) - before
    for o in new:
        if o.parent is None:
            o.parent = par
        if o.type == "MESH":
            o.data.materials.clear(); o.data.materials.append(mat)
            if not o.data.has_custom_normals:
                o.data.set_sharp_from_angle(angle=math.radians(35))
                o.data.shade_smooth()
            o["part"] = os.path.basename(path)

for f, m in BASE_PARTS: import_part(B(f), m, zb)
for f, m in LID_PARTS:  import_part(L(f), m, zl)
bpy.context.view_layer.update()
print("MISSING:", MISSING)

def bbox(objs):
    mn = mathutils.Vector((1e9,) * 3); mx = -mn
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ mathutils.Vector(c)
            mn = mathutils.Vector(map(min, mn, w)); mx = mathutils.Vector(map(max, mx, w))
    return mn, mx

HIDE = [] if TRAY else ["legscrews.glb"]
for o in [o for o in bpy.data.objects if o.type == "MESH" and o.get("part") in HIDE]:
    o.hide_render = True; o.hide_viewport = True
meshes = [o for o in bpy.data.objects if o.type == "MESH" and o.get("part") not in HIDE]
lidm = [o for o in meshes if o.get("part", "") and os.path.dirname(o.get("part")) == ""
        and any(o.get("part") == p + ".glb" for p, _ in LID_PARTS)]
mn, mx = bbox(meshes)
lmn, lmx = bbox(lidm)
print("BBOX all (m)", [round(v, 4) for v in mn], [round(v, 4) for v in mx])
print("BBOX lid (m)", [round(v, 4) for v in lmn], [round(v, 4) for v in lmx])
FLOOR_Z = mn.z
T_IMPORT = time.time() - T0

# ---------------- studio: dark charcoal cyclorama ----------------
def cyc(width=6.0, depth=4.0, radius=0.9, height=3.0, seg=24):
    prof = [(-depth, 0.0)]
    for i in range(seg + 1):
        a = -math.pi / 2 + (math.pi / 2) * i / seg
        prof.append((radius * math.cos(a) + 0.0 + 1.2 - radius * 0, radius + radius * math.sin(a)))
    prof = [(-depth, 0.0), (1.2, 0.0)] + [(1.2 + radius * math.cos(-math.pi/2 + (math.pi/2)*i/seg),
            radius + radius * math.sin(-math.pi/2 + (math.pi/2)*i/seg)) for i in range(1, seg + 1)] + [(1.2 + radius, height)]
    verts, faces = [], []
    for x in (-width / 2, width / 2):
        for (d, z) in prof:
            verts.append((x, d, z))
    n = len(prof)
    for i in range(n - 1):
        faces.append((i, i + 1, n + i + 1, n + i))
    me = bpy.data.meshes.new("cyc"); me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new("cyc", me); col.objects.link(o)
    for p in me.polygons: p.use_smooth = True
    return o

backdrop = cyc()
# back wall faces the camera: rotate so the sweep rises behind the oven, opposite the camera azimuth
backdrop.rotation_euler = (0, 0, AZ + math.pi / 2)   # local +Y (the wall) ends up at AZ+180, behind the oven
backdrop.location = (0, 0, FLOOR_Z)
m, nt, b = principled("charcoal_backdrop")
b.inputs["Base Color"].default_value = (0.018, 0.019, 0.021, 1)
b.inputs["Roughness"].default_value = 0.5
b.inputs["Specular IOR Level"].default_value = 0.25
backdrop.data.materials.append(m)

# ---------------- lights: 3-point softbox + top strip ----------------
def area(name, az_deg, el_deg, dist, size, power, shape="RECTANGLE", sy=None, color=(1, 1, 1)):
    l = bpy.data.lights.new(name, "AREA"); l.energy = power; l.color = color
    l.shape = shape; l.size = size; l.spread = math.radians(float(os.environ.get("SPREAD", "55")))
    if sy: l.size_y = sy
    o = bpy.data.objects.new(name, l); col.objects.link(o)
    a, e = math.radians(az_deg), math.radians(el_deg)
    tgt = mathutils.Vector((0, 0, 0.06))
    o.location = tgt + dist * mathutils.Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    d = tgt - o.location
    o.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return o

az = math.degrees(AZ)
area("key",  az - 55, 35, 0.9, 0.7, 15, sy=1.0)                         # big softbox, camera-left-ish
fill = area("fill", az + 60, 18, 1.1, 1.4, 12, sy=1.0, color=(0.93, 0.96, 1.0))  # broad cool fill
rims = [area("rim",  az + 150, 40, 0.8, 0.25, 30, sy=1.2),               # strips behind, edge light
        area("rim2", az - 150, 40, 0.8, 0.25, 22, sy=1.2)]
# rim lights only touch the oven, so the floor never mirrors them back at the camera
oven_coll = bpy.data.collections.new("oven_only")
for o in meshes:
    if "tray" not in o.get("part", ""):   # the flat tray floor would mirror the rims as a white sheet
        oven_coll.objects.link(o)
for r_ in rims:
    r_.light_linking.receiver_collection = oven_coll
# with the lid open, 09's flat underside plate mirrors the fill straight at the camera (reads as a white sheet): fill skips 09
fill_coll = bpy.data.collections.new("fill_receivers")
for o in meshes + [backdrop]:
    if o.get("part") != "09.glb":
        fill_coll.objects.link(o)
fill.light_linking.receiver_collection = fill_coll
area("top",  az, 80, 0.8, 0.6, 6, sy=0.6)                               # soft top for the cap

world = bpy.data.worlds.new("w"); scene.world = world; world.use_nodes = True
wn = world.node_tree
env = wn.nodes.new("ShaderNodeTexEnvironment")
h = glob.glob("/Applications/Blender.app/Contents/Resources/*/datafiles/studiolights/world/studio.exr")
if h:
    env.image = bpy.data.images.load(h[0])
    wn.links.new(env.outputs["Color"], wn.nodes["Background"].inputs["Color"])
wn.nodes["Background"].inputs["Strength"].default_value = 0.12

# ---------------- camera: low 3/4, auto-fit ----------------
cam_d = bpy.data.cameras.new("cam"); cam_d.lens = 80
cam = bpy.data.objects.new("cam", cam_d); col.objects.link(cam); scene.camera = cam
RX, RY = 2400 * SCALE // 100, 1600 * SCALE // 100
scene.render.resolution_x, scene.render.resolution_y = RX, RY
ctr = (mn + mx) / 2
corners = [o.matrix_world @ mathutils.Vector(c) for o in meshes for c in o.bound_box]  # per-part boxes: tighter fit
dirv = mathutils.Vector((math.cos(EL) * math.cos(AZ), math.cos(EL) * math.sin(AZ), math.sin(EL)))
MARGIN = float(os.environ.get("MARGIN", "0.20"))
def place(dist):
    cam.location = ctr + dist * dirv
    cam.rotation_euler = (ctr - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
def fit_dist():
    lo, hi = 0.2, 5.0
    for _ in range(40):
        mid = (lo + hi) / 2; place(mid)
        ok = all(0.05 <= p.x <= 0.95 and MARGIN <= p.y <= 1 - MARGIN
                 for p in (world_to_camera_view(scene, cam, c) for c in corners))
        if ok: hi = mid
        else: lo = mid
    place(hi); return hi
for _ in range(4):   # fit, then lens-shift so the product sits centred, refit
    hi = fit_dist()
    pr = [world_to_camera_view(scene, cam, c) for c in corners]
    cx = (min(p.x for p in pr) + max(p.x for p in pr)) / 2 - 0.5
    cy = (min(p.y for p in pr) + max(p.y for p in pr)) / 2 - 0.5
    cam_d.shift_x += cx
    cam_d.shift_y += cy * RY / RX
hi = fit_dist()
cam_d.dof.use_dof = True; cam_d.dof.focus_distance = hi; cam_d.dof.aperture_fstop = float(os.environ.get("FSTOP", "22"))   # deep focus: whole product sharp
print("CAM dist", round(hi, 3), "loc", [round(v, 3) for v in cam.location])

# ---------------- render ----------------
scene.render.engine = "CYCLES"
cp = bpy.context.preferences.addons["cycles"].preferences
cp.compute_device_type = "METAL"; cp.refresh_devices()
for d in cp.devices: d.use = True
scene.cycles.device = "GPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.005
scene.cycles.use_denoising = True
scene.cycles.denoiser = "OPENIMAGEDENOISE"
scene.cycles.max_bounces = 12; scene.cycles.glossy_bounces = 8
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = float(os.environ.get("EXPOSURE", "-1.6"))
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_depth = "8"
raw = OUT.replace(".png", "_raw.png")
scene.render.filepath = raw
T1 = time.time()
bpy.ops.render.render(write_still=True)
T_RENDER = time.time() - T1

# ---------------- light post: vignette only (pixels of the product untouched in shape) ----------------
import numpy as np
img = bpy.data.images.load(raw)
w, hgt = img.size
px = np.array(img.pixels[:], dtype=np.float32).reshape(hgt, w, 4)
yy, xx = np.mgrid[0:hgt, 0:w]
nx = (xx / w - 0.5) * 2; ny = (yy / hgt - 0.45) * 2
r = np.sqrt((nx * 0.85) ** 2 + ny ** 2)
v = 1.0 - 0.38 * np.clip((r - 0.45) / 0.9, 0, 1) ** 1.6
px[..., :3] *= v[..., None]
img.pixels[:] = px.ravel()
img.filepath_raw = OUT; img.file_format = "PNG"; img.save()
print(f"TIMES import {T_IMPORT:.1f}s render {T_RENDER:.1f}s total {time.time()-T0:.1f}s")
print("RENDERED:", OUT)
