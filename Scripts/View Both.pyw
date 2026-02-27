import pyvista as pv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
lid_path = os.path.join(script_dir, "lidbottomupdated.stl")
cyl_path = os.path.join(script_dir, "updatedcylinder.stl")

lid = pv.read(lid_path)
cyl = pv.read(cyl_path)

plotter = pv.Plotter(shape=(1, 2), title="Lid & Cylinder - Drag to rotate, Scroll to zoom")

plotter.subplot(0, 0)
plotter.add_text("Lid / Bottom", font_size=12)
plotter.add_mesh(lid, color='lightgray', show_edges=False, specular=0.5, smooth_shading=True)
plotter.enable_shadows()
plotter.show_axes()

plotter.subplot(0, 1)
plotter.add_text("Cylinder", font_size=12)
plotter.add_mesh(cyl, color='lightgray', show_edges=False, specular=0.5, smooth_shading=True)
plotter.enable_shadows()
plotter.show_axes()

plotter.show()
