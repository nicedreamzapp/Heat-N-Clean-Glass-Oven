"""Hero render: CURRENT Heat-N-Clean oven (FAB_PACKAGE_2026-11-08-R2) on its steel tray (part 14) with a
CONCEPT controller box (no CAD exists for the box; sized around the parts in Controller_Setup_Guide.md:
REX-C100 PID 48x48 DIN face (PV red over SV green), DH48S-2Z 48x48 timer, rocker on/off; box 150 x 110 x 78 mm,
rubber feet, cable gland on the oven side, one cable along the tray floor up into the 315 deg thermocouple hole
(r 58) under 04). Built on Scripts/render_product_2026-11-08.py (same materials, studio, camera fit).

Geometry: viewer-full/ (base) and viewer-lid-full/ (lid) GLBs, which build_current_package.py
writes from FAB_PACKAGE_2026-11-08-R2. They are already in assembly position (z-up, mm), so nothing
is moved except the lid, which swings on the hinge (axis tangent at 292.4 deg, pivot r 77.5,
z 100.86 (98.2 before R2), the same numbers as viewer-complete.html).

Run (headless, M5):
  /Applications/Blender.app/Contents/MacOS/Blender -b -P Scripts/render_hero_tray_2026-11-08.py -- out.png
Env: LID=100 (deg open, 0 = closed)  SAMPLES=384  SCALE=100 (% of 2400x1600)  AZ=74  EL=13  XM=0.15 (side margin)  MARGIN=0.10  (finals: AZ=84, MARGIN=0.03 open / 0.05 closed)
"""
import bpy, math, os, sys, glob, time
import mathutils
from bpy_extras.object_utils import world_to_camera_view

T0 = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/oven_render.png"
LID = float(os.environ.get("LID", "100"))
SAMPLES = int(os.environ.get("SAMPLES", "384"))
SCALE = int(os.environ.get("SCALE", "100"))
TRAY = True
AZ = math.radians(float(os.environ.get("AZ", "74")))
EL = math.radians(float(os.environ.get("EL", "13")))

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
] + ([("tray", STEEL)] if TRAY else [])
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
HA = math.radians(292.4)
HC = mathutils.Vector((77.5 * math.cos(HA), 77.5 * math.sin(HA), 100.86))
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
# ---------------- concept controller box on the tray (real z-up mm, parented to root) ----------------
# Tray (14): floor top z -56.7, outline x -102.25..292.25, y -102.25..102.25; oven axis at the origin.
FLOOR_TOP = -56.7
BW, BD, BH = 150.0, 110.0, 78.0              # box width (x), depth (y), height (z), mm
FOOT_H = 4.0
BCX, BCY = 197.0, 0.0                         # centred in the free tray area (x 102..292)
BZ0 = FLOOR_TOP + FOOT_H                      # box bottom
FRONT = BCY + BD / 2                          # front panel plane (+y, faces the camera)
BOX_OBJS = []

def mat_simple(name, color, rough, metal=0.0, emit=None, estr=0.0, spec=0.5):
    m, nt, b = principled(name)
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = estr
    return m

BOX_STEEL = steel("box_steel_brushed", (0.66, 0.66, 0.67), 0.24, 0.6)
# brushing on the box runs along x (left-right), not around the oven axis
_nt = BOX_STEEL.node_tree
for n in _nt.nodes:
    if n.type == "MAPPING": n.inputs["Scale"].default_value = (0.02, 2.0, 2.0)
    if n.type == "TANGENT": n.direction_type = "RADIAL"; n.axis = "X"
BLACK_PL = mat_simple("black_plastic", (0.012, 0.012, 0.013), 0.38)
BTN_PL   = mat_simple("button_grey", (0.09, 0.09, 0.095), 0.45)
GLASS_D  = mat_simple("display_glass", (0.004, 0.004, 0.005), 0.06, spec=0.6)
RUBBER   = mat_simple("rubber", (0.015, 0.015, 0.016), 0.7, spec=0.3)
CABLE    = mat_simple("cable_jacket", (0.02, 0.02, 0.022), 0.42, spec=0.45)
NYLON    = mat_simple("gland_nylon", (0.03, 0.03, 0.032), 0.35)
SEG_RED  = mat_simple("seg_red", (0.3, 0.01, 0.0), 0.3, emit=(1.0, 0.06, 0.02), estr=9.0)
SEG_GRN  = mat_simple("seg_green", (0.0, 0.3, 0.05), 0.3, emit=(0.15, 1.0, 0.2), estr=7.0)
SEG_OFF  = mat_simple("seg_off", (0.008, 0.003, 0.002), 0.3)
ROCKER   = mat_simple("rocker_red", (0.5, 0.02, 0.01), 0.3, emit=(1.0, 0.08, 0.03), estr=1.2)

def add_obj(name, me, mat, bevel=0.0, seg=3, smooth=False):
    o = bpy.data.objects.new(name, me); col.objects.link(o); o.parent = root
    me.materials.append(mat)
    if smooth:
        for p in me.polygons: p.use_smooth = True
    if bevel > 0:
        md = o.modifiers.new("bevel", "BEVEL"); md.width = bevel; md.segments = seg; md.limit_method = "ANGLE"
        wn = o.modifiers.new("wn", "WEIGHTED_NORMAL"); wn.keep_sharp = True
        for p in me.polygons: p.use_smooth = True
    o["part"] = "controller_box"
    BOX_OBJS.append(o)
    return o

def add_box(name, cx, cy, cz, sx, sy, sz, mat, bevel=0.0, seg=3):
    import bmesh
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = mathutils.Vector((cx + v.co.x * sx, cy + v.co.y * sy, cz + v.co.z * sz))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return add_obj(name, me, mat, bevel, seg)

def add_cyl(name, loc, r, depth, mat, axis="Z", verts=48, r2=None, bevel=0.0):
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=r, radius2=(r if r2 is None else r2), depth=depth)
    rot = {"Z": mathutils.Matrix.Identity(3), "X": mathutils.Matrix.Rotation(math.radians(90), 3, "Y"),
           "Y": mathutils.Matrix.Rotation(math.radians(-90), 3, "X")}[axis]
    for v in bm.verts: v.co = rot @ v.co + mathutils.Vector(loc)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    return add_obj(name, me, mat, bevel, 2, smooth=(bevel == 0))

# enclosure + rubber feet
add_box("ctrl_enclosure", BCX, BCY, BZ0 + BH / 2, BW, BD, BH, BOX_STEEL, bevel=3.0, seg=4)
for fx in (-1, 1):
    for fy in (-1, 1):
        add_cyl("ctrl_foot", (BCX + fx * (BW / 2 - 14), BCY + fy * (BD / 2 - 14), FLOOR_TOP + FOOT_H / 2), 7.0, FOOT_H, RUBBER)

# front panel: viewer at +y looks toward -y, so the viewer's right is world -x
SEGS = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc",
        "7": "abc", "8": "abcdefg", "9": "abcdfg", " ": ""}
def seven_seg(text, right_x, cz, h, mat, y):
    """digits drawn right-aligned ending at world x = right_x (viewer's right), face at y."""
    w, t = h * 0.55, h * 0.13
    pitch = w + h * 0.32
    chars = [c for c in text if c != "."]
    dots = [i - 1 for i, c in enumerate([c for c in text]) if c == "."]
    n = len(chars)
    for i, ch in enumerate(chars):
        cx = right_x + (n - 1 - i) * pitch + w / 2          # viewer-left of the right edge = +x
        L, R = cx + w / 2, cx - w / 2                       # viewer-left / viewer-right x
        geo = {"a": (cx, cz + h / 2, w, t), "g": (cx, cz, w, t), "d": (cx, cz - h / 2, w, t),
               "f": (L, cz + h / 4, t, h / 2), "b": (R, cz + h / 4, t, h / 2),
               "e": (L, cz - h / 4, t, h / 2), "c": (R, cz - h / 4, t, h / 2)}
        for sname, (x, z, sx, sz) in geo.items():
            on = sname in SEGS[ch]
            add_box("seg", x, y + 0.15, z, sx * 0.92 if sx > t else sx, 0.3, sz * 0.88 if sz > t else sz,
                    mat if on else SEG_OFF)
    for di in dots:
        k = sum(1 for c in text[:text.index(".")] if c != ".") - 1
        cx = right_x + (n - 1 - k) * pitch + w / 2
        add_box("seg_dp", cx - w / 2 - h * 0.16, y + 0.15, cz - h / 2, t, 0.3, t, mat)

ZP = BZ0 + BH / 2 + 2.0                               # instrument row centre height
# REX-C100 (48 x 48 DIN), viewer-left
PIDX = BCX + BW / 2 - 10 - 24
add_box("rex_bezel", PIDX, FRONT + 1.5, ZP, 48, 3.0, 48, BLACK_PL, bevel=1.0)
add_box("rex_window", PIDX, FRONT + 3.05, ZP + 5, 40, 0.3, 30, GLASS_D)
seven_seg(" 498", PIDX - 18, ZP + 12.5, 10.0, SEG_RED, FRONT + 3.1)
seven_seg(" 500", PIDX - 18, ZP - 1.0, 7.0, SEG_GRN, FRONT + 3.1)
for i in range(4):
    add_box("rex_btn", PIDX + 15 - i * 10, FRONT + 3.4, ZP - 17, 7, 1.0, 4.5, BTN_PL, bevel=0.6)
# DH48S-2Z timer (48 x 48 DIN), middle
TMX = PIDX - 48 - 8
add_box("dh_bezel", TMX, FRONT + 1.5, ZP, 48, 3.0, 48, BLACK_PL, bevel=1.0)
add_box("dh_window", TMX, FRONT + 3.05, ZP + 7, 38, 0.3, 20, GLASS_D)
seven_seg("5.59", TMX - 15, ZP + 7, 10.0, SEG_RED, FRONT + 3.1)
for i in range(4):
    add_box("dh_btn", TMX + 15 - i * 10, FRONT + 3.4, ZP - 12, 6, 1.0, 6, BTN_PL, bevel=0.6)
# illuminated rocker on/off, viewer-right
RKX = TMX - 24 - 8 - 8
add_box("rocker_bezel", RKX, FRONT + 1.0, ZP, 16, 2.0, 26, BLACK_PL, bevel=0.8)
add_box("rocker", RKX, FRONT + 2.6, ZP, 12, 2.2, 21, ROCKER, bevel=0.8)

# cable gland on the oven-side (-x) face, low and toward the back
GZ = BZ0 + 18.0
GY = BCY + 5.0
XS = BCX - BW / 2
add_cyl("gland_nut", (XS - 2.0, GY, GZ), 10.0, 4.0, NYLON, axis="X", verts=6)
add_cyl("gland_body", (XS - 9.0, GY, GZ), 8.0, 10.0, NYLON, axis="X", r2=5.5)
# cable: gland -> down to the tray floor -> under the cap -> up into the thermocouple hole (315 deg, r 58)
CR = 2.75
TCX, TCY = 58 * math.cos(math.radians(315)), 58 * math.sin(math.radians(315))
FZ = FLOOR_TOP + CR
pts = [(XS - 8, GY, GZ), (XS - 20, GY, GZ - 1), (XS - 30, GY - 2, FZ + 6), (XS - 40, GY - 5, FZ),
       (80, -12, FZ), (TCX + 14, TCY + 2, FZ), (TCX + 3, TCY, FZ + 7), (TCX, TCY, FZ + 16), (TCX, TCY, -26.0)]
cu = bpy.data.curves.new("cable", "CURVE"); cu.dimensions = "3D"
sp = cu.splines.new("BEZIER"); sp.bezier_points.add(len(pts) - 1)
for bp_, p in zip(sp.bezier_points, pts):
    bp_.co = p; bp_.handle_left_type = bp_.handle_right_type = "AUTO"
cu.bevel_depth = CR; cu.bevel_resolution = 6; cu.resolution_u = 24; cu.use_fill_caps = True
co = bpy.data.objects.new("cable", cu); col.objects.link(co); co.parent = root
cu.materials.append(CABLE); co["part"] = "controller_box"; BOX_OBJS.append(co)

bpy.context.view_layer.update()
meshes += BOX_OBJS
print("BOX objs", len(BOX_OBJS))

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
    tgt = (mn + mx) / 2
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
MARGIN = float(os.environ.get("MARGIN", "0.10"))
XM = float(os.environ.get("XM", "0.15"))
def place(dist):
    cam.location = ctr + dist * dirv
    cam.rotation_euler = (ctr - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
def fit_dist():
    lo, hi = 0.2, 5.0
    for _ in range(40):
        mid = (lo + hi) / 2; place(mid)
        ok = all(XM <= p.x <= 1 - XM and MARGIN <= p.y <= 1 - MARGIN
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
