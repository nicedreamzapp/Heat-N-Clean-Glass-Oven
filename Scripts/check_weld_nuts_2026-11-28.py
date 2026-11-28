"""Fit + build check for FAB_PACKAGE_2026-11-28 (weld nuts at every bolt, hinge at 292.5 on its own holes).
usage: .venv-cad/bin/python Scripts/check_weld_nuts_2026-11-28.py [FAB_PACKAGE_2026-11-28]
Measures from the CAD: part-part overlaps (closed), bolt heads + shanks vs every part (shank drawn at the M6 minor
radius 2.4, so any overlap = a hole or weld nut bore out of line), weld nut clearances to the ceramics, spacers, heater
leads and leg screws, whether each part can still slide into place past the nuts, and the lid swing on the hinge."""
import os, sys, math, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build123d import *
import hnc_params as HP
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "FAB_PACKAGE_2026-11-28")
P = {f[:-5]: import_step(os.path.join(PKG, "STEP", f)) for f in sorted(os.listdir(os.path.join(PKG, "STEP")))}
def vol(x):
    try: return sum(s.volume for s in x.solids()) if x is not None else 0.0
    except Exception: return 0.0
def ring(ri, ro, z0, z1):
    return Pos(0, 0, z0) * (Cylinder(ro, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)) - Cylinder(ri, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
def rcyl(a, r0, r1, z, rad):
    return Rot(0, 0, a) * Pos((r0 + r1) / 2, 0, z) * Rot(0, 90, 0) * Cylinder(rad, r1 - r0)
def hexr(a, r0, r1, z, s=10.0, flats_up=False):
    e = s / math.cos(math.radians(30)); hx = extrude(RegularPolygon(e / 2, 6), amount=r1 - r0)
    if flats_up: hx = Rot(0, 0, 30) * hx
    return Rot(0, 0, a) * Pos(r1, 0, z) * Rot(0, -90, 0) * hx
U = HP.body_raise; ZT = 59.0 + U; ZLL = 102.86; ZUL = 122.86
B = list(HP.ring_screw_angles); HA = HP.HINGE_ANGLE_DEG
HB = [HA - 6.0, HA + 6.0]; HL = [HA - 18.4, HA + 18.4]
R01I = HP.housing_inner_r
# bolts: (angles, head seat r, tip r, z)  head 10 AF x 4, shank to the tip
BOLTS = {"bottom": (B, 68.10, 53.0, -24.0), "seat": (B, 66.0, 51.0, 2.15), "top": (B, 67.30, 53.0, ZT),
         "lower lid": (B, 66.0, 52.0, ZLL), "upper lid": (B, 67.5, 53.0, ZUL),
         "hinge body H1": (HB, 71.16, 71.16 - 16.0, ZT), "hinge lid H2": (HL, 71.45, 71.45 - 18.0, ZLL)}
# weld nuts: (angles, wall inside face r, z, part)
NUTS = {"01 bottom": (B, R01I, -24.0), "01 top": (B, R01I, ZT), "01 hinge": (HB, R01I, ZT), "03 seat": (B, R01I - 1.0, 2.15),
        "09 lower lid": (B + HL, R01I - 1.0, ZLL), "06 upper lid": (B, R01I, ZUL)}
def nut(a, rf, z): return hexr(a, rf + 0.05 - 5.0, rf + 0.05, z, flats_up=abs(z - ZLL) < 0.01)   # 09: flats up
SPI, SPO = 62.05, 64.65
SPACERS = {"bottom": (-29.0, -19.0, -24.0, B), "seat": (-2.85, 7.15, 2.15, B), "top": (ZT - 5, ZT + 5, ZT, B + HB),
           "lower lid": (ZLL - 5, ZLL + 5, ZLL, B + HL), "upper lid": (ZUL - 5, ZUL + 5, ZUL, B)}
SP = {k: ring(SPI, SPO, z0, z1) - Compound(children=[rcyl(a, SPI - 1, SPO + 1, zb, 3.3) for a in angs]) for k, (z0, z1, zb, angs) in SPACERS.items()}
CER = {"ceramic core": ring(40.75, 46.25, 4.46, 94.86), "base disk": Pos(0, 0, -0.44) * Cylinder(46.25, 4.9, align=(Align.CENTER, Align.CENTER, Align.MIN)),
       "lid disk": Pos(0, 0, 94.86) * Cylinder(46.25, 6.0, align=(Align.CENTER, Align.CENTER, Align.MIN))}
out = []
def say(s): print(s); out.append(s)
say(f"package: {os.path.basename(PKG)}")
# 1. part vs part, closed
names = list(P); bad = 0
for a, b in itertools.combinations(names, 2):
    v = vol(P[a] & P[b])
    if v > 0.01: say(f"  OVERLAP {a} x {b}: {v:.2f} mm3"); bad += 1
for k, s in SP.items():
    for n in names:
        v = vol(s & P[n])
        if v > 0.01: say(f"  OVERLAP {k} spacer x {n}: {v:.2f} mm3"); bad += 1
say(f"1. parts + spacers closed: {bad} overlaps")
# 2. bolts
bad = 0
for k, (angs, rh, rt, z) in BOLTS.items():
    for a in angs:
        sh = rcyl(a, rt, rh, z, 2.4); hd = hexr(a, rh, rh + 4.0, z)
        for n in names:
            v1, v2 = vol(sh & P[n]), vol(hd & P[n])
            if v1 > 0.05 or v2 > 0.05:   # 0.02 = the head face lying exactly on its seat (contact)
                say(f"  {k} bolt {a:.1f}: shank {v1:.2f} / head {v2:.2f} mm3 into {n}"); bad += 1
say(f"2. bolts (head + shank at minor dia) vs all parts: {bad} clashes")
# 3. weld nut clearances
say("3. weld nut clearances (min distance, mm):")
allnuts = {k: [nut(a, rf, z) for a in angs] for k, (angs, rf, z) in NUTS.items()}
for k, ns in allnuts.items():
    c = Compound(children=ns)
    d = {n: c.distance_to(s) for n, s in CER.items()}
    sp = min(c.distance_to(s) for s in SP.values())
    say(f"  {k:13s} core {d['ceramic core']:.2f}  base disk {d['base disk']:.2f}  lid disk {d['lid disk']:.2f}  spacers {sp:.2f}")
# heater leads (2026-11-20): 03 holes Ø10 r 53.5, 04 holes Ø11.5 r 49 with the Skutt lip Ø22.1 x 3 on the floor (-31.7)
def vcyl(a, r, rad, z0, z1):
    return Pos(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), z0) * Cylinder(rad, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))
leads03 = Compound(children=[vcyl(a, 53.5, 5.0, -6.3, 4.46) for a in HP.lead_hole_angles])
lips = Compound(children=[vcyl(a, 49.0, 11.05, -31.7, -28.7) for a in HP.lead_hole_angles])
lead_col = Compound(children=[vcyl(a, 49.0 + (53.5 - 49.0) * 0.5, 4.0, -28.7, -6.3) for a in HP.lead_hole_angles])
say(f"  heater leads: seat nuts to the 03 lead-hole column (Ø10 up to the base disk) {Compound(children=allnuts['03 seat']).distance_to(leads03):.2f}; "
    f"bottom nuts to the Skutt lips {Compound(children=allnuts['01 bottom']).distance_to(lips):.2f}, to the Ø8 crimp path in the 03-04 chamber {Compound(children=allnuts['01 bottom']).distance_to(lead_col):.2f}")
legheads = Compound(children=[vcyl(a, 54.0, 4.25, -31.7, -26.7) for a in HP.leg_angles])
say(f"  bottom nuts to the M5 leg screw heads {Compound(children=allnuts['01 bottom']).distance_to(legheads):.2f}")
# 4. assembly: can each part slide into place past the nuts already welded on
say("4. slide-in checks:")
r_nut_in = R01I + 0.05 - 5.0
r03 = max(math.hypot(v.X, v.Y) for v in P["03_Support_Ring"].vertices())
say(f"  03 support ring OD r {r03:.2f} vs 01's top + hinge weld nuts (inner face r {r_nut_in:.2f}, z {ZT - 5.77:.1f}..{ZT + 5.77:.1f}) "
    f"and bottom nuts (z -29.8..-18.2): {'BLOCKED, ' + format(r03 - r_nut_in, '.2f') + ' mm radial overlap from either end' if r03 > r_nut_in else 'passes'}")
say(f"  ceramic core / base disk (r 46.25) down past 01's top nuts: radial clear {r_nut_in - 46.25:.2f}")
say(f"  06 down over the 09 wall: 06 nuts lowest z {ZUL - 5.77:.2f} vs 09 wall top 108.86 -> never meet ({ZUL - 5.77 - 108.86:.2f} above)")
say(f"  spacer rings (ID r {SPI}) over 01 (OD r {HP.housing_outer_r}): nuts are inside 01, clear {SPI - HP.housing_outer_r:.2f}")
# 5. lid swing on the hinge
a = math.radians(HA); XC = 73.55; ZS = 94.86
ax = Axis((XC * math.cos(a), XC * math.sin(a), ZS), (-math.sin(a), math.cos(a), 0))
lid = [P[n] for n in names if n[:2] in ("06", "07", "08", "09", "10") or n.startswith("H2")] + [SP["lower lid"], SP["upper lid"]]
body = [P[n] for n in names if n[:2] in ("01", "02", "05") or n.startswith("H1")] + [SP["top"]]
swing = []
for ang in (15, 45, 90, 110, 135):
    worst = max(vol(L.rotate(ax, ang) & Bd) for L in lid for Bd in body)
    swing.append(f"{ang}°: {worst:.2f}")
say("5. lid swing overlap (mm3) " + ", ".join(swing))
# also: 257.5 lid bolt head vs H2 wing (socket access)
w = P["H2_Hinge_Lid_Leaf"]; hd = hexr(257.5, 66.0, 70.0, ZLL)
say(f"  257.5 lower-lid bolt head to the H2 wing: {hd.distance_to(w):.2f} mm; 329.5 head: {hexr(329.5, 66.0, 70.0, ZLL).distance_to(w):.2f} mm")
say(f"  257.5 / 329.5 top bolt heads to H1: {hexr(257.5, 67.3, 71.3, ZT).distance_to(P['H1_Hinge_Body_Leaf']):.2f} / {hexr(329.5, 67.3, 71.3, ZT).distance_to(P['H1_Hinge_Body_Leaf']):.2f} mm")
n09 = [nut(a, R01I - 1.0, ZLL) for a in B + HL]
say(f"  09 weld nut top {max(x.bounding_box().max.Z for x in n09):.2f} vs 09 wall top 108.86; nearest 09 nut pair gap {min(n09[i].distance_to(n09[j]) for i in range(len(n09)) for j in range(i + 1, len(n09))):.2f}")
h01 = allnuts["01 hinge"]; say(f"  01 hinge weld nut pair gap {h01[0].distance_to(h01[1]):.2f}")
open(os.path.join(PKG, "fit_check.txt"), "w").write("\n".join(out) + "\n")
