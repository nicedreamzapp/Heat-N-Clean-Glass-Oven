"""PREVIEW ONLY (2026-10-12): the 03 support ring with its middle raised so the ceramic sits flush with the top cap.
Writes viewer-seat5/ (a copy of viewer-full with 03, basedisk and core changed). Does NOT touch the FAB package.
Run:  .venv-cad/bin/python Scripts/build_seat_raise_preview.py
"""
import math, os
import numpy as np, trimesh
from build123d import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "viewer-seat5")
UP = 5.06                 # Alice's caliper, 2026-10-12: ceramic top sits 5.06 below the cap top (to be confirmed)
SLOT_DROP = 0.24          # his 5.3 slot mismatch minus the 5.06 raise: the real slot ends this far below the groove
T = 0.8
BOLT = [52.4 + 60 * k for k in range(6)]
WIRE = [(180.0, 4.0), (190.0, 4.0), (315.0, 3.2)]
A = (Align.CENTER, Align.CENTER, Align.MIN)
def ring(ri, ro, z0, z1): return Pos(0, 0, z0) * (Cylinder(ro, z1 - z0, align=A) - Cylinder(ri, z1 - z0, align=A))
def vhole(ang, r, rad, z0, z1):
    a = math.radians(ang); return Pos(r * math.cos(a), r * math.sin(a), z0) * Cylinder(rad, z1 - z0, align=A)
def rhole(ang, r_mid, z, rad=3.3, length=8): return Rot(0, 0, ang) * Pos(r_mid, 0, z) * Rot(0, 90, 0) * Cylinder(rad, length)

STEP_R = 52.0             # the riser: outside the ceramic's centering wall (47.25), inside the wire holes (54.0)
sr = (ring(STEP_R, 70.65, -6.3, -5.5)                      # outer part of the plate: unchanged height
      + ring(STEP_R - T, STEP_R, -6.3, -5.5 + UP)          # riser
      + ring(36.25, STEP_R, -5.5 + UP - T, -5.5 + UP)      # raised middle = the ceramic seat
      + ring(46.45, 47.25, -5.5 + UP, 3.0 + UP)            # centering wall, moved up with the seat
      + ring(69.85, 70.65, -5.5, 8.5))                     # bolt wall: unchanged
for a in BOLT: sr -= rhole(a, 70.25, 2.15, length=6)
for a in (40, 160, 280): sr -= vhole(a, 64.0, 3.3, -8, -4)
for a, r in WIRE: sr -= vhole(a, 58.0, r, -8, -4)
export_stl(sr, "/tmp/03_raised.stl"); trimesh.load("/tmp/03_raised.stl").export(os.path.join(OUT, "03.glb"))
print("03 solids:", len(sr.solids()), "z %.2f..%.2f" % (sr.bounding_box().min.Z, sr.bounding_box().max.Z))

def mesh(f):
    sc = trimesh.load(os.path.join(ROOT, "viewer-full", f + ".glb"))
    return sc.dump(concatenate=True) if isinstance(sc, trimesh.Scene) else sc
d = mesh("basedisk"); print("basedisk z", d.bounds[:, 2]); d.apply_translation([0, 0, UP]); d.export(os.path.join(OUT, "basedisk.glb"))
c = mesh("core"); z0, z1 = c.bounds[:, 2]; print("core z", z0, z1)
# the real ceramic is shorter than drawn: remap heights so the top lands flush with the cap top (92.2), the slot
# bottoms land where Alice measured them, and the foot stands on the raised seat's base disk
slot = 67.5; v = c.vertices.copy(); z = v[:, 2]
lo = z <= slot
v[lo, 2] = (z0 + UP) + (z[lo] - z0) * ((slot - SLOT_DROP) - (z0 + UP)) / (slot - z0)
v[~lo, 2] = (slot - SLOT_DROP) + (z[~lo] - slot) * (92.2 - (slot - SLOT_DROP)) / (z1 - slot)
c.vertices = v; print("core now z", c.bounds[:, 2]); c.export(os.path.join(OUT, "core.glb"))
