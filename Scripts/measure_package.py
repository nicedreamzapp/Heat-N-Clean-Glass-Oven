"""Fresh-import measurement + fit check of a package. usage: measure.py <pkg> [<pkg2>]"""
import sys, os, math, json, itertools
from build123d import *
def load(pkg, n): return import_step(os.path.join(pkg, "STEP", n + ".step"))
def S(x): return Solid(x.solids()[0].wrapped)
def vcyl(s):
    out=set()
    for f in s.faces():
        if f.geom_type==GeomType.CYLINDER:
            d=f.geom_adaptor().Cylinder().Axis().Direction()
            if abs(d.Z())>0.99: 
                l=f.geom_adaptor().Cylinder().Axis().Location()
                if math.hypot(l.X(),l.Y())<0.01: out.add(round(f.radius,3))
    return sorted(out)
def radial_holes(s, rad):
    out=[]
    for f in s.faces():
        if f.geom_type==GeomType.CYLINDER and abs(f.radius-rad)<1e-3:
            d=f.geom_adaptor().Cylinder().Axis().Direction()
            if abs(d.Z())<0.01:
                vs=[math.hypot(v.X,v.Y) for v in f.vertices()]
                c=f.center(); out.append((round(math.degrees(math.atan2(c.Y,c.X))%360,1), round(min(vs),2), round(max(vs),2)))
    return out
def vholes(s, rad):
    out=[]
    for f in s.faces():
        if f.geom_type==GeomType.CYLINDER and abs(f.radius-rad)<1e-3:
            ax=f.geom_adaptor().Cylinder().Axis(); d=ax.Direction(); l=ax.Location()
            if abs(d.Z())>0.99: out.append((round(math.degrees(math.atan2(l.Y(),l.X()))%360,1), round(math.hypot(l.X(),l.Y()),2)))
    return sorted(set(out))
def rmax(s):
    return round(max(math.hypot(v.X,v.Y) for v in s.vertices()),3) if s.vertices() else None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hnc_params as HP
def measure(pkg):
    M={}
    names=[n[:-5] for n in sorted(os.listdir(pkg+"/STEP"))]
    P={n:S(load(pkg,n)) for n in names}
    # R2 (2026-11-08): everything above the seat is U higher; U is read from the package itself (05 cap top - 92.2)
    U=round(P["05_One_Piece_Top_Cap"].bounding_box().max.Z-92.2,3); M["body_raise_U"]=U
    for n,s in P.items():
        bb=s.bounding_box()
        M[n]={"OD":round(max(bb.max.X-bb.min.X, bb.max.Y-bb.min.Y),2),"vcyl_r":vcyl(s),"vol":round(s.volume,1),
              "z":(round(bb.min.Z,2),round(bb.max.Z,2))}
        bh=radial_holes(s,3.3)
        if bh: M[n]["M6_hole_r_mid"]=sorted(set(round((a+b)/2,2) for _,a,b in bh))
        vh=sorted(set(vholes(s,3.3)+vholes(s,4.0)+vholes(s,3.2)))
        if vh: M[n]["vert_holes(ang,r)"]=vh
    cap=P["05_One_Piece_Top_Cap"]
    plate=cap & (Pos(0,0,91.6+U)*Box(400,400,0.4))
    M["cap_plate_outer_r_incl_tab_ears"]=rmax(plate)
    # 2026-11-12: the ring is measured on a line at 30 deg (between a glass slot and a bolt tab), where the glass sits
    edge=rmax(plate & (Rot(0,0,30)*Pos(60,0,91.6+U)*Box(40,0.5,1)))
    M["cap_plate_edge_r_at_30deg"]=edge
    M["cap_ring_width_ceramicOD_to_cap_edge"]=round(edge-46.25,2)
    tab=cap & (Pos(0,0,70+U)*Box(400,400,1))
    M["cap_tab_outer_r"]=rmax(tab)
    # groove length: inside U face r range at slot 6.5
    for f in cap.faces():
        if f.geom_type==GeomType.CYLINDER and abs(f.radius-5.25)<1e-3:
            vs=[math.hypot(v.X,v.Y) for v in f.vertices()]; M["groove_inside_r_range"]=(round(min(vs),2),round(max(vs),2)); M["groove_length"]=round(max(vs)-min(vs),2); break
    i01=min(r for r in M["01_Inner_Wall_Tube"]["vcyl_r"]); o01=max(M["01_Inner_Wall_Tube"]["vcyl_r"])
    i02=min(M["02_Outer_Perforated_Tube"]["vcyl_r"]); o02=max(M["02_Outer_Perforated_Tube"]["vcyl_r"])
    M["insulation_ceramicOD_to_01ID"]=round(i01-46.25,2); M["air_gap_01OD_to_02ID"]=round(i02-o01,2)
    M["wall_01"]=round(o01-i01,2); M["wall_02"]=round(o02-i02,2)
    M["perf_holes_02"]=sum(1 for f in P["02_Outer_Perforated_Tube"].faces() if f.geom_type==GeomType.CYLINDER and abs(f.radius-2)<1e-3)
    # collisions between parts (assembled)
    col=[]
    names_c=[n for n in names if n!="14_Steel_Tray"]
    for a,b in itertools.combinations(names_c,2):
        A,B=P[a],P[b]
        ba,bb_=A.bounding_box(),B.bounding_box()
        if ba.max.Z<bb_.min.Z-0.01 or bb_.max.Z<ba.min.Z-0.01 or ba.max.X<bb_.min.X or bb_.max.X<ba.min.X or ba.max.Y<bb_.min.Y or bb_.max.Y<ba.min.Y: continue
        try:
            r_=A&B; v=sum(x.volume for x in r_.solids()) if r_ is not None else 0.0
        except Exception as e: v=str(e)[:40]
        if not (isinstance(v,float) and v<0.01): col.append((a,b,round(v,3)))
    M["part_overlaps(>0.01mm3)"]=col
    # ceramic core and spacer rings vs parts
    # ceramic core as drawn in the viewers: R2 = the real one (base plate 4.9 on the seat, core 90.4 on it); R1 = 5.06..92.2
    cz0,ch=(HP.seat_z+HP.base_disk_t_real,HP.ceramic_core_h_real) if U>0.01 else (5.06,87.14)
    core=Pos(0,0,cz0)*(Cylinder(46.25,ch,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(40.75,ch,align=(Align.CENTER,Align.CENTER,Align.MIN)))
    bd=Pos(0,0,HP.seat_z)*(Cylinder(46.25,cz0-HP.seat_z,align=(Align.CENTER,Align.CENTER,Align.MIN)))
    sp_i,sp_o=o01+0.4,i02   # spacer rings fill the air gap, 0.4 off the inner tube
    # 2026-11-10: all five rings 10 mm, centred on their bolt lines
    spacers={"sp_bot":(-29,-19),"sp_seat":(-2.85,7.15),"sp_top":(54+U,64+U),"sp_low":(95.2+U,105.2+U),"sp_high":(115.2+U,125.2+U)}
    M["spacer_ring_ID/OD"]=(round(2*sp_i,2),round(2*sp_o,2))
    extra=[]
    for n,s in P.items():
        v=(s&core).volume
        if v>0.01: extra.append(("ceramic_core",n,round(v,3)))
        v=(s&bd).volume
        if v>0.01: extra.append(("ceramic_base_plate",n,round(v,3)))
        for k,(z0,z1) in spacers.items():
            sp=Pos(0,0,z0)*(Cylinder(sp_o,z1-z0,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(sp_i,z1-z0,align=(Align.CENTER,Align.CENTER,Align.MIN)))
            v=(s&sp).volume
            if v>0.01: extra.append((k,n,round(v,3)))
    M["ceramic/spacer_overlaps"]=extra
    # bolt lines: a Ø6.2 rod along each bolt axis must hit NO metal (holes line up in every wall it crosses)
    BOLT=[52.4+60*k for k in range(6)]
    bad=[]
    ZS=(59.0+U,-24.0,2.15,100.2+U,120.2+U)
    for z in ZS:
        for a in BOLT:
            r0,r1=i01-9,o02+8   # from inside the nut to outside the head
            rod=Rot(0,0,a)*Pos((r0+r1)/2,0,z)*Rot(0,90,0)*Cylinder(3.1,r1-r0)
            for n,s in P.items():
                v=(s&rod).volume
                if v>0.01: bad.append((z,a,n,round(v,2)))
    M["bolt_line_blocked"]=bad
    walls={}
    for z in ZS:
        rod=Rot(0,0,52.4)*Pos(70,0,z)*Rot(0,90,0)*Cylinder(4.5,40)
        walls[z]=[n[:2] for n,s in P.items() if (s&rod).volume>0.01]
    M["bolt_stack_parts"]=walls
    # vertical: leg screws, wires through 03/04/14
    vb=[]
    legr=[r for a,r in M["03_Support_Ring"]["vert_holes(ang,r)"] if a in (40.0,160.0,280.0)]
    for a in (40,160,280):
        r=legr[0]
        rod=Pos(r*math.cos(math.radians(a)),r*math.sin(math.radians(a)),-80)*Cylinder(3.1,80,align=(Align.CENTER,Align.CENTER,Align.MIN))
        for n,s in P.items():
            v=(s&rod).volume
            if v>0.01: vb.append(("leg",a,n,round(v,2)))
    wires=[(a,r,3.9) for a,r in vholes(P["03_Support_Ring"],4.0)]+[(a,r,3.1) for a,r in vholes(P["03_Support_Ring"],3.2)]
    M["wire_holes_03(ang,r)"]=[(a,r) for a,r,_ in wires]
    for a,wr,rr in wires:
        rod=Pos(wr*math.cos(math.radians(a)),wr*math.sin(math.radians(a)),-40)*Cylinder(rr,40,align=(Align.CENTER,Align.CENTER,Align.MIN))
        for n,s in P.items():
            v=(s&rod).volume
            if v>0.01: vb.append(("wire",a,n,round(v,2)))
    M["vertical_lines_blocked"]=vb
    M["leg_r"]=legr[0]
    # R2 fit checks: ceramic top vs cap top, lid seat, vents 05 vs 09, groove bottoms vs ceramic slot bottoms, tube tops
    cap_top=round(cap.bounding_box().max.Z,3); core_top=round(cz0+ch,3)
    M["seat_z / core bottom / core top / cap top"]=(HP.seat_z if U>0.01 else -0.44, round(cz0,3), core_top, cap_top)
    M["ceramic_top_minus_cap_top"]=round(core_top-cap_top,3)
    M["lid_09_bottom_minus_cap_top"]=round(P["09_Lid_Ceramic_Holder"].bounding_box().min.Z-cap_top,3)
    vr=sorted({round(f.radius,3) for f in cap.faces() if f.geom_type==GeomType.CYLINDER and f.radius<2.5
               and abs(f.geom_adaptor().Cylinder().Axis().Direction().Z())>0.99
               and math.hypot(f.geom_adaptor().Cylinder().Axis().Location().X(),f.geom_adaptor().Cylinder().Axis().Location().Y())>50})
    M["vent_radius"]=vr
    v05=vholes(cap,vr[0]); v09=vholes(P["09_Lid_Ceramic_Holder"],vr[0])
    M["vent_ring_r"]=sorted({r for _,r in v05})
    off=max(min(math.hypot(r1*math.cos(math.radians(a1))-r2*math.cos(math.radians(a2)),r1*math.sin(math.radians(a1))-r2*math.sin(math.radians(a2))) for a2,r2 in v09) for a1,r1 in v05)
    M["vents_05/09_count, max_offset_mm"]=(len(v05),len(v09),round(off,3))
    zs=[]
    for f in cap.faces():
        if f.geom_type==GeomType.CYLINDER and abs(f.radius-5.25)<1e-3: zs.append(f.bounding_box().min.Z)
    M["05_groove_inside_bottom_z"]=round(min(zs),3) if zs else None
    M["tube_tops_01/02"]=(round(P["01_Inner_Wall_Tube"].bounding_box().max.Z,3),round(P["02_Outer_Perforated_Tube"].bounding_box().max.Z,3))
    M["tube_heights_01/02"]=tuple(round(P[n].bounding_box().size.Z,3) for n in ("01_Inner_Wall_Tube","02_Outer_Perforated_Tube"))
    for n in ("11_Lid_Hinge_Strap","13_Hinge_Pin"):
        c=P[n].center(); M[n+"_center_r_ang"]=(round(math.hypot(c.X,c.Y),2),round(math.degrees(math.atan2(c.Y,c.X))%360,2))
    return M
res={p:measure(p) for p in sys.argv[1:]}
json.dump(res,open("/tmp/measure.json","w"),indent=1,default=str)
for p,M in res.items():
    print("=====",p)
    for k,v in M.items(): print(" ",k,":",v)
