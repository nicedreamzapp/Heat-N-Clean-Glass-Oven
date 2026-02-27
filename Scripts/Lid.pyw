import pyvista as pv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
stl_path = os.path.join(script_dir, "lidbottomupdated.stl")

mesh = pv.read(stl_path)
plotter = pv.Plotter(title="Lid / Bottom - Drag to rotate, Scroll to zoom")
plotter.add_mesh(mesh, color='lightgray', show_edges=False, specular=0.5, smooth_shading=True)
plotter.enable_shadows()
plotter.show_axes()
plotter.show()
