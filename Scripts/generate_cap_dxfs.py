#!/usr/bin/env python3
"""Flat-pattern DXF for 04a_Cap_Shell + dimension drawing DXF for
04b_Cap_HoldDown_Ring. Writes into CAD Exports/Flat Patterns/DXF so the
fabrication package picks them up. Pure R12 ASCII DXF, no dependencies.

Layers:
  CUT  — laser cut outline + holes
  FOLD — bend/fold lines (skirt fold circle, hinge-tab fold arc)
  NOTE — text callouts
"""
import os, math

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "CAD Exports", "Flat Patterns", "DXF")

# ---- dimensions (match export_all_parts.py) ----
T = 1.2
ceramic_outer_r = 46.25
ceramic_inner_r = 40.75
housing_inner_r = 70.85
housing_outer_r = 72.05
mesh_inner_r = 76.05
mesh_outer_r = 77.25
cap_outer_r = 78.75          # rim (skirt fold line)
lip_drop = 10
SKIRT_R = cap_outer_r + lip_drop            # 88.75 unfolded skirt edge
FINGER_TIP_R = cap_outer_r + (91 - 55)      # 114.75 unfolded finger tip
FINGER_HOLE_R = cap_outer_r + (91 - 59)     # 110.75 unfolded bolt hole
FINGER_HALF_W = 6.0                          # 12mm wide fingers
HINGE_TAB_TIP_R = FINGER_TIP_R + 11 + 13.5  # extra strap + curl allowance
BOLT_ANGLES = [52.4 + k*60 for k in range(6)]
HINGE_ANGLE = 292.4

# slots (same math as the master script)
slot_width = 10.5
gaps = [46.25, 46.25, 46.25, 108.68]
circ = math.pi * 92.5
sf = circ / (sum(gaps) + 4*slot_width)
slot_positions = []
cur = 0
for i in range(4):
    slot_positions.append(((cur + (slot_width*sf)/2) / circ) * 360)
    cur += (slot_width + gaps[i]) * sf
slot_arc_half = (slot_width/2) / ceramic_outer_r * (180/math.pi)
slot_buffer = 4.0 / ceramic_outer_r * (180/math.pi)
flange_buffer = 4.0 / cap_outer_r * (180/math.pi)

# bottom-cap flange angles (used only to reproduce the vent hole skip pattern)
slot_arc_half_blank = (slot_width * sf / 2 / circ * 360)
tab_angles = []
for i in range(3):
    a0 = slot_positions[i] + slot_arc_half_blank
    a1 = slot_positions[i+1] - slot_arc_half_blank
    tab_angles.append((a0 + a1) / 2)
s3e = slot_positions[3] + slot_arc_half_blank
big = gaps[3]*sf/circ*360
hinge_c = (s3e + big/2) % 360
tab_angles.append((s3e + hinge_c) / 2)
s0s = slot_positions[0] - slot_arc_half_blank + 360
tab_angles.append(((hinge_c + s0s) / 2) % 360)

# vent holes — identical loop to the master script (66 holes, 1 row)
vent_inner, vent_outer = housing_outer_r, cap_outer_r
spacing = 6 * 0.8
n_rows = max(1, int((vent_outer - vent_inner) / spacing))
row_sp = (vent_outer - vent_inner) / (n_rows + 1)
def away_from_flanges(a):
    for f in tab_angles:
        d = abs(a - f)
        if d > 180: d = 360 - d
        if d < flange_buffer: return False
    return True
vents = []
for rr in range(n_rows):
    r_pos = vent_inner + row_sp * (rr + 1)
    off = (spacing/2) if (rr % 2) else 0
    for gi in range(4):
        ni = (gi + 1) % 4
        g0 = slot_positions[gi] + slot_arc_half + slot_buffer
        g1 = slot_positions[ni] - slot_arc_half - slot_buffer
        if g1 < g0: g1 += 360
        arc_mm = (g1 - g0) * (math.pi/180) * r_pos
        n = max(1, int(arc_mm / spacing))
        for hi in range(n):
            a = g0 + (hi + 0.5) * (g1 - g0) / n + off / ((vent_inner+vent_outer)/2)
            if a >= 360: a -= 360
            if away_from_flanges(a):
                vents.append((a, r_pos))

# ---- tiny DXF writer ----
class DXF:
    def __init__(self): self.e = []
    def _l(self, *args): self.e += [str(a) for a in args]
    def line(self, x1, y1, x2, y2, layer="CUT"):
        self._l(0,"LINE",8,layer,10,f"{x1:.3f}",20,f"{y1:.3f}",11,f"{x2:.3f}",21,f"{y2:.3f}")
    def circle(self, x, y, r, layer="CUT"):
        self._l(0,"CIRCLE",8,layer,10,f"{x:.3f}",20,f"{y:.3f}",40,f"{r:.3f}")
    def arc(self, x, y, r, a0, a1, layer="CUT"):
        self._l(0,"ARC",8,layer,10,f"{x:.3f}",20,f"{y:.3f}",40,f"{r:.3f}",50,f"{a0:.3f}",51,f"{a1:.3f}")
    def text(self, x, y, h, s, layer="NOTE"):
        self._l(0,"TEXT",8,layer,10,f"{x:.3f}",20,f"{y:.3f}",40,f"{h:.3f}",1,s)
    def save(self, path):
        out = ["0","SECTION","2","ENTITIES"] + self.e + ["0","ENDSEC","0","EOF"]
        open(path,"w").write("\n".join(out)+"\n")

def pol(r, a): a = math.radians(a); return r*math.cos(a), r*math.sin(a)

# ============ 04a Cap Shell flat blank ============
d = DXF()
# outline: rim arcs at SKIRT_R between tabs, tab side lines + tip arcs
tabs = [(a, FINGER_TIP_R) for a in BOLT_ANGLES if abs(a - HINGE_ANGLE) > 0.1]
tabs.append((HINGE_ANGLE, HINGE_TAB_TIP_R))
tabs.sort()
for i,(a,tip) in enumerate(tabs):
    half = math.degrees(FINGER_HALF_W / SKIRT_R)
    na, ntip = tabs[(i+1) % len(tabs)]
    nhalf = math.degrees(FINGER_HALF_W / SKIRT_R)
    # arc from end of this tab to start of next
    a_end = a + half
    a_next = na - nhalf + (360 if na < a else 0)
    d.arc(0, 0, SKIRT_R, a_end % 360, a_next % 360)
    # tab: two radial lines + tip arc
    for s in (-1, 1):
        x1, y1 = pol(SKIRT_R, a + s*half)
        x2, y2 = pol(tip,     a + s*half)
        d.line(x1, y1, x2, y2)
    d.arc(0, 0, tip, (a - half) % 360, (a + half) % 360)
# bore
d.circle(0, 0, ceramic_inner_r)
# 4 slot cutouts: bore edge -> ceramic_outer_r wedges
for sc in slot_positions:
    for s in (-1, 1):
        x1, y1 = pol(ceramic_inner_r, sc + s*slot_arc_half)
        x2, y2 = pol(ceramic_outer_r, sc + s*slot_arc_half)
        d.line(x1, y1, x2, y2)
    d.arc(0, 0, ceramic_outer_r, (sc - slot_arc_half) % 360, (sc + slot_arc_half) % 360)
# vent holes + finger bolt holes
for a, r in vents:
    x, y = pol(r, a); d.circle(x, y, 2.0)
for a in BOLT_ANGLES:
    x, y = pol(FINGER_HOLE_R, a); d.circle(x, y, 1.8)
# fold lines
d.circle(0, 0, cap_outer_r, layer="FOLD")                       # skirt fold, 90 deg down
x, y = pol(FINGER_TIP_R, HINGE_ANGLE)
hh = math.degrees(FINGER_HALF_W / FINGER_TIP_R)
d.arc(0, 0, FINGER_TIP_R, (HINGE_ANGLE - hh) % 360, (HINGE_ANGLE + hh) % 360, layer="FOLD")
# notes
d.text(-150, SKIRT_R + 52, 5, "04a CAP SHELL FLAT BLANK - 304SS 1.2mm - DIMS IN MM")
d.text(-150, SKIRT_R + 44, 4, "FOLD layer: circle R78.75 = skirt fold 90deg DOWN (10mm drop)")
d.text(-150, SKIRT_R + 37, 4, "6 fingers fold down with skirt; bolt holes D3.6 land at 32mm below rim")
d.text(-150, SKIRT_R + 30, 4, f"HINGE TAB at {HINGE_ANGLE}deg: fold 180deg UP at FOLD arc, then curl last 13.5mm")
d.text(-150, SKIRT_R + 23, 4, "into two D8 barrels for D5 pin (piano hinge style)")
d.text(-150, SKIRT_R + 16, 4, "FORM (no cut): top dips 23.5mm at the 4 slot zones for R>46.25 - see 3D model")
d.save(os.path.join(OUT_DIR, "04a_Cap_Shell_Flat.dxf"))
print("04a_Cap_Shell_Flat.dxf:", len(vents), "vent holes")

# ============ 04b Hold-Down Ring drawing (top view + wall callouts) ============
d = DXF()
for r in (ceramic_inner_r, ceramic_inner_r + T, ceramic_outer_r, ceramic_outer_r + T,
          housing_inner_r - T, housing_inner_r):
    # rings broken at the 4 slot notches
    segs = []
    ss = sorted(slot_positions)
    for i in range(4):
        a0 = ss[i] + slot_arc_half
        a1 = (ss[i+1] if i+1 < 4 else ss[0] + 360) - slot_arc_half
        segs.append((a0 % 360, a1 % 360))
    for a0, a1 in segs:
        d.arc(0, 0, r, a0, a1)
for sc in slot_positions:   # notch edges
    for s in (-1, 1):
        x1, y1 = pol(ceramic_inner_r, sc + s*slot_arc_half)
        x2, y2 = pol(housing_inner_r, sc + s*slot_arc_half)
        d.line(x1, y1, x2, y2)
d.text(-150, housing_inner_r + 40, 5, "04b CERAMIC HOLD-DOWN RING - 304SS - TOP VIEW - DIMS IN MM")
d.text(-150, housing_inner_r + 32, 4, "FLAT TOP. Three walls hang DOWN from it:")
d.text(-150, housing_inner_r + 25, 4, "  R40.75-41.95 bore lip, 3mm deep")
d.text(-150, housing_inner_r + 18, 4, "  R46.25-47.45 ceramic flaps, 10mm deep")
d.text(-150, housing_inner_r + 11, 4, "  R69.65-70.85 chamber edge wall, 6mm deep")
d.text(-150, housing_inner_r + 4, 4, "Web 2mm thick. 4 notches match ceramic slots. NO fastener holes -")
d.text(-150, housing_inner_r - 3, 4, "part is CLAMPED between cap shell and chamber. 3D model authoritative.")
d.save(os.path.join(OUT_DIR, "04b_HoldDown_Ring_Drawing.dxf"))
print("04b_HoldDown_Ring_Drawing.dxf written")
