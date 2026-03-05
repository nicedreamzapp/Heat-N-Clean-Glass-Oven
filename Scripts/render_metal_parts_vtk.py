"""
High-quality VTK renders of the 4 main metal parts.
Produces individual PNGs + a combined 2x2 overview.

Run: python3 render_metal_parts_vtk.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import vtkmodules.all as vtk

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STL_DIR = os.path.join(PROJECT_DIR, "CAD Exports", "Individual Parts", "STL")
OUT_DIR = os.path.join(PROJECT_DIR, "Metal_Parts_Package", "Part_Images")
os.makedirs(OUT_DIR, exist_ok=True)

# Resolution for individual renders
W, H = 1600, 1200

# Parts: (stl_file, output_name, title, R, G, B, elevation, azimuth, zoom)
PARTS = [
    ("01_Base_Body.stl",    "01_Chamber_Body",  "Chamber Body",    0.76, 0.78, 0.80,  25, -50, 1.0),
    ("02_Bottom_Cap.stl",   "02_Bottom_Cap",    "Bottom Cap",      0.86, 0.63, 0.24,  60, -35, 1.0),
    ("03_Top_Cap.stl",      "03_Top_Cap",       "Top Cap",         0.76, 0.78, 0.80,  30, -50, 1.0),
    ("04_Lid_Assembly.stl", "04_Lid_Assembly",   "Lid Assembly",   0.76, 0.78, 0.80,  25, -55, 1.0),
]

# Back/other side views: same parts, rotated ~180 degrees
PARTS_BACK = [
    ("01_Base_Body.stl",    "01_Chamber_Body_Back",  "Chamber Body — Back",    0.76, 0.78, 0.80,  25, 130, 1.0),
    ("02_Bottom_Cap.stl",   "02_Bottom_Cap_Back",    "Bottom Cap — Underside", 0.86, 0.63, 0.24, -50, -35, 1.0),
    ("03_Top_Cap.stl",      "03_Top_Cap_Back",       "Top Cap — Back",         0.76, 0.78, 0.80,  30, 130, 1.0),
    ("04_Lid_Assembly.stl", "04_Lid_Assembly_Back",   "Lid Assembly — Inside", 0.76, 0.78, 0.80, -25, 125, 1.0),
]


def render_part(stl_file, out_name, title, r, g, b, elev, azim, zoom):
    """Render a single STL part to PNG using VTK."""
    fpath = os.path.join(STL_DIR, stl_file)
    if not os.path.exists(fpath):
        print(f"  MISSING: {stl_file}")
        return None

    print(f"  Rendering {stl_file}...", end=" ", flush=True)

    # Read STL
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fpath)
    reader.Update()

    # Compute normals for smooth shading
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(reader.GetOutputPort())
    normals.SetFeatureAngle(30.0)
    normals.SplittingOn()
    normals.ComputePointNormalsOn()
    normals.Update()

    # Mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())

    # Actor with metallic appearance
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    prop = actor.GetProperty()
    prop.SetColor(r, g, b)
    prop.SetSpecular(0.5)
    prop.SetSpecularPower(40)
    prop.SetDiffuse(0.7)
    prop.SetAmbient(0.15)
    prop.SetInterpolationToPhong()

    # Renderer
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(1.0, 1.0, 1.0)

    # Add title text
    text = vtk.vtkTextActor()
    text.SetInput(title)
    text.GetTextProperty().SetFontSize(28)
    text.GetTextProperty().SetColor(0.15, 0.15, 0.15)
    text.GetTextProperty().SetBold(True)
    text.GetTextProperty().SetFontFamilyToArial()
    text.SetPosition(30, H - 50)
    ren.AddActor2D(text)

    # Subtle gradient background
    ren.SetBackground2(0.92, 0.93, 0.95)
    ren.GradientBackgroundOn()

    # Key light
    light1 = vtk.vtkLight()
    light1.SetPosition(200, 200, 400)
    light1.SetFocalPoint(0, 0, 0)
    light1.SetIntensity(0.9)
    light1.SetColor(1.0, 0.98, 0.95)
    ren.AddLight(light1)

    # Fill light
    light2 = vtk.vtkLight()
    light2.SetPosition(-200, -100, 200)
    light2.SetFocalPoint(0, 0, 0)
    light2.SetIntensity(0.4)
    light2.SetColor(0.9, 0.92, 1.0)
    ren.AddLight(light2)

    # Rim light
    light3 = vtk.vtkLight()
    light3.SetPosition(0, -200, -100)
    light3.SetFocalPoint(0, 0, 0)
    light3.SetIntensity(0.25)
    ren.AddLight(light3)

    # Render window (offscreen)
    renWin = vtk.vtkRenderWindow()
    renWin.SetOffScreenRendering(1)
    renWin.SetSize(W, H)
    renWin.AddRenderer(ren)

    # Camera
    ren.ResetCamera()
    cam = ren.GetActiveCamera()
    cam.Elevation(elev)
    cam.Azimuth(azim)
    cam.Zoom(zoom)
    ren.ResetCameraClippingRange()
    # Expand clipping range to prevent cut-off
    near, far = cam.GetClippingRange()
    cam.SetClippingRange(near * 0.1, far * 10)

    renWin.Render()

    # Capture to PNG
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(renWin)
    w2i.SetInputBufferTypeToRGBA()
    w2i.Update()

    out_path = os.path.join(OUT_DIR, f"{out_name}.png")
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(out_path)
    writer.SetInputConnection(w2i.GetOutputPort())
    writer.Write()

    size_kb = os.path.getsize(out_path) / 1024
    print(f"{size_kb:.0f} KB -> {out_path}")

    renWin.Finalize()
    return out_path


def render_combined_view():
    """Render all 4 parts in a single 2x2 grid scene."""
    print("  Rendering combined 2x2 overview...", end=" ", flush=True)

    renWin = vtk.vtkRenderWindow()
    renWin.SetOffScreenRendering(1)
    renWin.SetSize(W * 2, H * 2)

    # Viewports: (xmin, ymin, xmax, ymax)
    viewports = [
        (0.0, 0.5, 0.5, 1.0),  # top-left
        (0.5, 0.5, 1.0, 1.0),  # top-right
        (0.0, 0.0, 0.5, 0.5),  # bottom-left
        (0.5, 0.0, 1.0, 0.5),  # bottom-right
    ]

    for i, (stl_file, out_name, title, r, g, b, elev, azim, zoom) in enumerate(PARTS):
        fpath = os.path.join(STL_DIR, stl_file)
        if not os.path.exists(fpath):
            continue

        reader = vtk.vtkSTLReader()
        reader.SetFileName(fpath)
        reader.Update()

        normals = vtk.vtkPolyDataNormals()
        normals.SetInputConnection(reader.GetOutputPort())
        normals.SetFeatureAngle(30.0)
        normals.SplittingOn()
        normals.ComputePointNormalsOn()
        normals.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(normals.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        prop = actor.GetProperty()
        prop.SetColor(r, g, b)
        prop.SetSpecular(0.5)
        prop.SetSpecularPower(40)
        prop.SetDiffuse(0.7)
        prop.SetAmbient(0.15)
        prop.SetInterpolationToPhong()

        ren = vtk.vtkRenderer()
        ren.SetViewport(*viewports[i])
        ren.AddActor(actor)
        ren.SetBackground(1.0, 1.0, 1.0)
        ren.SetBackground2(0.92, 0.93, 0.95)
        ren.GradientBackgroundOn()

        # Label
        text = vtk.vtkTextActor()
        text.SetInput(title)
        text.GetTextProperty().SetFontSize(32)
        text.GetTextProperty().SetColor(0.15, 0.15, 0.15)
        text.GetTextProperty().SetBold(True)
        text.GetTextProperty().SetFontFamilyToArial()
        text.SetPosition(20, H - 50)
        ren.AddActor2D(text)

        # Lights
        light1 = vtk.vtkLight()
        light1.SetPosition(200, 200, 400)
        light1.SetFocalPoint(0, 0, 0)
        light1.SetIntensity(0.9)
        ren.AddLight(light1)

        light2 = vtk.vtkLight()
        light2.SetPosition(-200, -100, 200)
        light2.SetFocalPoint(0, 0, 0)
        light2.SetIntensity(0.4)
        ren.AddLight(light2)

        renWin.AddRenderer(ren)
        ren.ResetCamera()
        cam = ren.GetActiveCamera()
        cam.Elevation(elev)
        cam.Azimuth(azim)
        cam.Zoom(zoom)
        ren.ResetCameraClippingRange()
        near, far = cam.GetClippingRange()
        cam.SetClippingRange(near * 0.1, far * 10)

    renWin.Render()

    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(renWin)
    w2i.SetInputBufferTypeToRGBA()
    w2i.Update()

    out_path = os.path.join(OUT_DIR, "00_All_4_Metal_Parts.png")
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(out_path)
    writer.SetInputConnection(w2i.GetOutputPort())
    writer.Write()

    size_kb = os.path.getsize(out_path) / 1024
    print(f"{size_kb:.0f} KB -> {out_path}")

    renWin.Finalize()
    return out_path


print("=" * 60)
print("HIGH-QUALITY METAL PART RENDERS (VTK)")
print("=" * 60)

paths = []
print("\n--- Front views ---")
for args in PARTS:
    p = render_part(*args)
    if p:
        paths.append(p)

print("\n--- Back views ---")
for args in PARTS_BACK:
    p = render_part(*args)
    if p:
        paths.append(p)

combined = render_combined_view()
if combined:
    paths.append(combined)

print(f"\n{len(paths)} images saved to: {OUT_DIR}")

# Build PDF with all views (2 pages per part: front + back)
print("\nBuilding PDF...", end=" ", flush=True)
try:
    from PIL import Image
    pdf_images = []
    # Order: front1, back1, front2, back2, ...
    for i in range(len(PARTS)):
        front_path = os.path.join(OUT_DIR, f"{PARTS[i][1]}.png")
        back_path = os.path.join(OUT_DIR, f"{PARTS_BACK[i][1]}.png")
        if os.path.exists(front_path):
            pdf_images.append(Image.open(front_path).convert('RGB'))
        if os.path.exists(back_path):
            pdf_images.append(Image.open(back_path).convert('RGB'))

    if pdf_images:
        pdf_path = os.path.join(OUT_DIR, "4_Metal_Parts.pdf")
        pdf_images[0].save(pdf_path, save_all=True, append_images=pdf_images[1:], resolution=150)
        print(f"{os.path.getsize(pdf_path)/1024:.0f} KB -> {pdf_path}")
except ImportError:
    print("(Pillow not installed, skipping PDF)")

print("\nDone!")

# Open them
import subprocess
for p in paths:
    subprocess.Popen(["open", p])
