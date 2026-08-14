"""
Heat-N-Clean Glass Oven — ANALYTIC STEP build for the two-piece top cap.

Builds TRUE analytic B-rep solids (real cylinders, planes, circular holes) — NOT
meshes — so the sheet-metal shop can measure them.

  04a_Cap_Shell        — flat top disk (rim level) + Ø4 vent holes + 4 slot
                         openings + 10 mm skirt + 6 drop-tab fingers (each with a
                         radial Ø3.6 bolt-clearance hole) + a hinge finger at
                         292.4 deg that curls into two Ø8 barrels bored Ø5.2.
  04b_Cap_HoldDown_Ring — flat web ring (4 slot notches) + 3 hanging walls
                         (grab-lip / ceramic-OD flaps / chamber-edge wall). No
                         fasteners.

Coordinate system is the generator's WORLD frame (axis = Z, z=0 = ceramic seat
ref, housing_top_z = 91 the chamber rim) so the parts assemble with the rest.

Run with the CAD venv:
  .venv-cad/bin/python Scripts/build_cap_shell_ring.py
"""
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hnc_params import *  # noqa: F401,F403  shared params, do NOT hardcode

from build123d import (
    Cylinder, Box, Pos, Rot, Compound,
    export_step, import_step, Align,
)


def as_compound(part):
    """Normalize a boolean result (Solid / Compound / ShapeList of disjoint
    solids) into a single Compound so it has bbox/volume and exports as one
    multi-body STEP part."""
    if hasattr(part, "bounding_box"):
        return part
    # ShapeList of disjoint solids -> wrap
    return Compound(children=list(part))

# ----------------------------------------------------------------------------
# Geometry constants pulled from shared params (verbatim, never hardcoded here)
# ----------------------------------------------------------------------------
T = sheet_metal_thickness                       # 1.2
RIM_Z = housing_top_z                            # 91 — chamber rim / cap-flat top
LIP_DROP = 10                                    # cap_lip skirt drop (matches src lip_drop)

# Vent band radii (from src cap_vent_inner_r / outer_r)
VENT_INNER_R = housing_outer_r                    # 72.05
VENT_OUTER_R = cap_outer_r                         # 78.75

# Hinge finger center / half-width (from src _f_center / _f_half)
_F_CENTER = HINGE_ANGLE_DEG + math.degrees(HINGE_T_OFF / cap_outer_r)
_F_HALF = math.degrees(13.0 / cap_outer_r)

# Hinge pin (tangent) axis unit vector at HINGE_ANGLE_DEG
_HA = math.radians(HINGE_ANGLE_DEG)
_HTX, _HTY = -math.sin(_HA), math.cos(_HA)

EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "CAD Exports", "STEP")
os.makedirs(EXPORT_DIR, exist_ok=True)


# ----------------------------------------------------------------------------
# Small analytic helpers
# ----------------------------------------------------------------------------
def tube(r_outer, r_inner, height, z_top):
    """Analytic annular ring: outer cylinder minus inner cylinder.
    Returns a Solid whose top face is at z_top, extending DOWN by `height`."""
    z_center = z_top - height / 2.0
    outer = Cylinder(radius=r_outer, height=height,
                     align=(Align.CENTER, Align.CENTER, Align.CENTER))
    inner = Cylinder(radius=r_inner, height=height + 2.0,
                     align=(Align.CENTER, Align.CENTER, Align.CENTER))
    ring = outer - inner
    return Pos(0, 0, z_center) * ring


def radial_box(r_mid, ang_deg, z, half_w, half_h, depth):
    """A box centered at radius r_mid, angle ang_deg, height z; oriented so its
    `depth` axis points radially outward. Used to make wall/finger sectors and
    cut openings. half_w = tangential half-width, half_h = vertical half-height."""
    a = math.radians(ang_deg)
    cx, cy = r_mid * math.cos(a), r_mid * math.sin(a)
    box = Box(2 * depth, 2 * half_w, 2 * half_h,
              align=(Align.CENTER, Align.CENTER, Align.CENTER))
    # rotate about Z so the local X (depth) points radially
    box = Rot(0, 0, ang_deg) * box
    return Pos(cx, cy, z) * box


def radial_hole(r_mid, ang_deg, z, radius, length=8.0):
    """Analytic cylinder lying along the radial direction (a real round hole)."""
    a = math.radians(ang_deg)
    cx, cy = r_mid * math.cos(a), r_mid * math.sin(a)
    # cylinder default axis = Z; rotate so axis points radially (about Y then Z)
    cyl = Rot(0, 90, 0) * Cylinder(radius=radius, height=length,
                                   align=(Align.CENTER, Align.CENTER, Align.CENTER))
    cyl = Rot(0, 0, ang_deg) * cyl
    return Pos(cx, cy, z) * cyl


def tangent_barrel(radius, length, t_off):
    """Analytic cylinder whose axis is the hinge tangent line, centered at
    HINGE_PIVOT_R / HINGE_PIVOT_Z and slid sideways t_off along that line."""
    # axis direction (_HTX, _HTY, 0). Default cylinder axis = +Z.
    # align +Z to (_HTX,_HTY,0): that vector lies in the XY plane, so rotate
    # -90 deg about X to bring Z into the XY plane (-> +Y), then rotate about Z.
    cyl = Cylinder(radius=radius, height=length,
                   align=(Align.CENTER, Align.CENTER, Align.CENTER))
    cyl = Rot(-90, 0, 0) * cyl            # +Z -> +Y
    ang = math.degrees(math.atan2(_HTY, _HTX)) - 90.0  # +Y -> (_HTX,_HTY)
    cyl = Rot(0, 0, ang) * cyl
    cx = HINGE_PIVOT_R * math.cos(_HA) + _HTX * t_off
    cy = HINGE_PIVOT_R * math.sin(_HA) + _HTY * t_off
    return Pos(cx, cy, HINGE_PIVOT_Z) * cyl


# ============================================================================
# 04a — CAP SHELL
# ============================================================================
def build_cap_shell():
    # --- flat top disk: outer cap_outer_r, bore cap_inner_r, thickness T at rim ---
    flat = tube(cap_outer_r, cap_inner_r, T, RIM_Z)

    # --- 10 mm skirt (cap_lip) hanging down at the rim ---
    # outer wall ring, outer = cap_outer_r, thickness T, from rim down LIP_DROP
    skirt = tube(cap_outer_r, cap_outer_r - T, LIP_DROP, RIM_Z)
    shell = flat + skirt

    # --- inner ceramic grab-lip (3mm) hanging at the bore ---
    grab = tube(cap_inner_r + T, cap_inner_r, ceramic_grab_lip, RIM_Z)
    shell = shell + grab

    # --- SIX drop-tab fingers (~12mm wide) at CAP_BOLT_ANGLES ---
    # Each finger: annular sector (cap_outer_r-T .. cap_outer_r) from CAP_TAB_BOT
    # up to just under the rim. Spec: fingers reach 36mm below the rim (z=55).
    CAP_TAB_TOP = RIM_Z - LIP_DROP + 3            # matches src CAP_TAB_TOP = 84
    tab_h = CAP_TAB_TOP - CAP_TAB_BOT
    tab_zc = (CAP_TAB_TOP + CAP_TAB_BOT) / 2.0
    tab_half_w_mm = 6.0                           # CAP_TAB_HALF_DEG = 6mm/r each side -> ~12mm wide
    for ang in CAP_BOLT_ANGLES:
        finger = tube(cap_outer_r, cap_outer_r - T, tab_h, CAP_TAB_TOP)
        # keep only the angular sector via intersection with a radial box
        sector = radial_box(cap_outer_r - T / 2, ang, tab_zc,
                            half_w=tab_half_w_mm, half_h=tab_h / 2 + 1, depth=T + 2)
        finger = finger & sector
        # radial bolt-clearance hole Ø3.6 at CAP_BOLT_Z
        hole = radial_hole(cap_outer_r - T / 2, ang, CAP_BOLT_Z,
                           radius=CAP_BOLT_HOLE_R, length=4 * T + 4)
        finger = finger - hole
        shell = shell + finger

    # --- HINGE FINGER at 292.4 deg: strap up the outside past the rim ---
    finger_top = HINGE_PIVOT_Z                    # 97
    finger_bot = RIM_Z - LIP_DROP - 3             # 78 (src housing_top_z - lip_drop - 3)
    fh = finger_top - finger_bot
    fzc = (finger_top + finger_bot) / 2.0
    hinge_finger = tube(cap_outer_r, cap_outer_r - T, fh, finger_top)
    hinge_sector = radial_box(cap_outer_r - T / 2, _F_CENTER, fzc,
                              half_w=13.0, half_h=fh / 2 + 1, depth=T + 2)
    hinge_finger = hinge_finger & hinge_sector
    shell = shell + hinge_finger

    # --- TWO hinge barrels (Ø8) bored Ø5.2 on the tangent axis ---
    for off in (HINGE_T_OFF - HINGE_KN_LEN, HINGE_T_OFF + HINGE_KN_LEN):
        barrel = tangent_barrel(HINGE_BARREL_OUTER_R, HINGE_KN_LEN, off)
        bore = tangent_barrel(HINGE_BARREL_BORE_R, HINGE_KN_LEN + 2.0, off)
        shell = as_compound(shell + (barrel - bore))

    # --- vent holes Ø4 in the flat top (ring of holes in each slot gap) ---
    # away from slots and away from the drop-tab/hinge flange angles. Vertical
    # cylinders bored through the flat disk.
    avoid_flanges = list(CAP_BOLT_ANGLES) + [_F_CENTER]
    flange_buffer_deg = math.degrees(6.0 / cap_outer_r)
    slot_buffer_deg = math.degrees(4.0 / ceramic_outer_r)

    def away_from_slots(a):
        for sc in slot_positions:
            d = abs(a - sc)
            if d > 180:
                d = 360 - d
            if d < slot_arc_half_deg + slot_buffer_deg:
                return False
        return True

    def away_from_flanges(a):
        for fa in avoid_flanges:
            d = abs(a - fa)
            if d > 180:
                d = 360 - d
            if d < flange_buffer_deg:
                return False
        return True

    vent_holes = []
    n_rows = 2                                     # two radial rings of vents
    band = VENT_OUTER_R - VENT_INNER_R
    row_sp = band / (n_rows + 1)
    for row in range(n_rows):
        r_pos = VENT_INNER_R + row_sp * (row + 1)
        # how many around: ~ every 7 deg, but only in the open gaps
        for k in range(int(360 / 7)):
            a = k * 7.0
            if away_from_slots(a) and away_from_flanges(a):
                vent_holes.append((a, r_pos))
    for (a, r_pos) in vent_holes:
        ar = math.radians(a)
        v = Cylinder(radius=perf_hole_r, height=T + 4,
                     align=(Align.CENTER, Align.CENTER, Align.CENTER))
        v = Pos(r_pos * math.cos(ar), r_pos * math.sin(ar), RIM_Z - T / 2) * v
        shell = as_compound(shell - v)

    # --- 4 slot openings cut in the top (over the ceramic slots, r<=ceramic_outer_r) ---
    # Open from above so glass drops into the ceramic. Cut a radial box from the
    # bore out to ceramic_outer_r at each slot center, full width of the slot.
    slot_box_half_w = slot_width / 2 + 0.5
    for sc in slot_positions:
        cut = radial_box(r_mid=(cap_inner_r + ceramic_outer_r) / 2, ang_deg=sc,
                         z=RIM_Z, half_w=slot_box_half_w,
                         half_h=ceramic_grab_lip + T + 2,
                         depth=(ceramic_outer_r - cap_inner_r) / 2 + 2)
        shell = as_compound(shell - cut)

    return as_compound(shell)


# ============================================================================
# 04b — CAP HOLD-DOWN RING
# ============================================================================
def build_hold_down_ring():
    web_top = HD_WEB_TOP                            # 89.8

    # slot gaps (between slots) — sectors get web + walls
    sorted_slots = sorted(slot_positions)
    slot_gaps = []
    for i in range(len(sorted_slots)):
        a0 = sorted_slots[i] + slot_arc_half_deg
        a1 = (sorted_slots[i + 1] if i + 1 < len(sorted_slots)
              else sorted_slots[0] + 360) - slot_arc_half_deg
        slot_gaps.append((a0, a1))

    ring = None

    def sector(r_in, r_out, z_top, drop, a0, a1):
        """Analytic annular sector: a tube intersected with an angular wedge box."""
        amid = (a0 + a1) / 2.0
        half = (a1 - a0) / 2.0
        t = tube(r_out, r_in, drop, z_top)
        zc = z_top - drop / 2.0
        # wedge: wide enough box rotated to amid. Use generous radial depth.
        # tangential half-width at r_out:
        half_w = r_out * math.tan(math.radians(half)) + r_out * 0.05
        # build a box wide enough; angular wedge via two cutting planes instead
        # of a single box to keep the arc edges correct:
        # simpler & robust: intersect with many thin radial wedge -> use a
        # cylindrical wedge approximated by a large box rotated, then trim ends.
        depth = (r_out - r_in) / 2 + 5
        rmid = (r_in + r_out) / 2
        wide = radial_box(rmid, amid, zc, half_w=max(half_w, 1.0),
                          half_h=drop / 2 + 1, depth=depth)
        s = t & wide
        return s

    for (a0, a1) in slot_gaps:
        # grab lip in the bore (ceramic_inner_r), drop HD_GRAB_LIP_DROP (3)
        grab = sector(ceramic_inner_r, ceramic_inner_r + T, web_top, HD_GRAB_LIP_DROP, a0, a1)
        # ceramic-OD flaps (ceramic_outer_r), drop HD_FLAP_DROP (10)
        flap = sector(ceramic_outer_r, ceramic_outer_r + T, web_top, HD_FLAP_DROP, a0, a1)
        # chamber-edge wall (housing_inner_r), drop HD_EDGE_WALL_DROP (6)
        edge = sector(housing_inner_r - T, housing_inner_r, web_top, HD_EDGE_WALL_DROP, a0, a1)
        # flat web between ceramic_inner_r and housing_inner_r, inset 4 deg each end
        m0, m1 = a0 + 4.0, a1 - 4.0
        web = sector(ceramic_inner_r, housing_inner_r, web_top, HD_WEB_DROP, m0, m1)
        for piece in (grab, flap, edge, web):
            ring = piece if ring is None else as_compound(ring + piece)

    return as_compound(ring)


# ============================================================================
# BUILD + EXPORT + VALIDATE
# ============================================================================
def measure(part, label):
    bb = part.bounding_box()
    vol = part.volume
    print(f"  [{label}] solids={len(part.solids())}  volume={vol:.1f} mm^3")
    print(f"        bbox X[{bb.min.X:.2f},{bb.max.X:.2f}] "
          f"Y[{bb.min.Y:.2f},{bb.max.Y:.2f}] Z[{bb.min.Z:.2f},{bb.max.Z:.2f}]")
    print(f"        OD ~ {bb.max.X - bb.min.X:.2f} mm")
    return bb, vol


def main():
    print("=" * 70)
    print("Building 04a_Cap_Shell (analytic) ...")
    shell = build_cap_shell()
    measure(shell, "cap_shell pre-export")
    shell_path = os.path.join(EXPORT_DIR, "04a_Cap_Shell.step")
    export_step(shell, shell_path)
    print(f"  -> {shell_path}")

    print("=" * 70)
    print("Building 04b_Cap_HoldDown_Ring (analytic) ...")
    ring = build_hold_down_ring()
    measure(ring, "hold_down_ring pre-export")
    ring_path = os.path.join(EXPORT_DIR, "04b_Cap_HoldDown_Ring.step")
    export_step(ring, ring_path)
    print(f"  -> {ring_path}")

    return shell_path, ring_path


if __name__ == "__main__":
    main()
