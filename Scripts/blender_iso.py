# Blender -b -P blender_iso.py -- <out_dir> <stl> [<stl> ...]   : one clean iso render per STL (Workbench, white bg)
import bpy, sys, os, math, mathutils
argv = sys.argv[sys.argv.index("--") + 1:]
out, stls = argv[0], argv[1:]
os.makedirs(out, exist_ok=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "SINGLE"
sc.display.shading.single_color = (0.62, 0.68, 0.76)
sc.display.shading.show_cavity = True; sc.display.shading.cavity_type = "BOTH"
sc.display.shading.show_object_outline = True; sc.display.shading.object_outline_color = (0.1, 0.12, 0.15)
sc.display.shading.show_specular_highlight = True
sc.render.resolution_x, sc.render.resolution_y = 1400, 1100
sc.render.film_transparent = True
sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGBA"
sc.display.render_aa = "16"
for stl in stls:
    for o in list(bpy.data.objects): bpy.data.objects.remove(o, do_unlink=True)
    if hasattr(bpy.ops.wm, "stl_import"): bpy.ops.wm.stl_import(filepath=stl)
    else: bpy.ops.import_mesh.stl(filepath=stl)
    ob = bpy.context.selected_objects[0]
    bb = [ob.matrix_world @ mathutils.Vector(c) for c in ob.bound_box]
    ctr = sum(bb, mathutils.Vector()) / 8; rad = max((v - ctr).length for v in bb)
    cam_d = bpy.data.cameras.new("c"); cam_d.type = "ORTHO"; cam_d.ortho_scale = rad * 2.15
    cam = bpy.data.objects.new("c", cam_d); sc.collection.objects.link(cam); sc.camera = cam
    d = mathutils.Vector((-0.55, -0.95, 0.62)).normalized()
    cam.location = ctr + d * rad * 4
    cam.rotation_euler = (ctr - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = os.path.join(out, os.path.splitext(os.path.basename(stl))[0] + ".png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED", sc.render.filepath)
