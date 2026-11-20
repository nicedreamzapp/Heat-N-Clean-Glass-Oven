from build123d import *
import math, os
# THICK hinge 2026-11-18 (Matt 2:25a: 2-3x beefier). Same bolt holes as before.
TH=257.5; ZS=94.86; ZB=61.66; ZL=102.86
XB0=67.45; XL0=66.05; XO=71.45          # body leaf 4.0 thick, lid leaf 5.4 thick, flush outside
R=6.0; XC=73.55; PIN=6.0                 # knuckle OD 12, 6 mm pin, knuckle clears 05 lip (r67.25) by 0.3
W=28.0; G=0.5; HM=6.0                    # 28 wide, middle (lid) knuckle 12 wide over the bolt
def box(x0,x1,y0,y1,z0,z1):
    return Pos((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)*Box(x1-x0,y1-y0,z1-z0)
def knuck(y0,y1):
    return Pos(XC,(y0+y1)/2,ZS)*Rot(90,0,0)*Cylinder(R,y1-y0)
def bolt(z,x0,x1):
    return Pos((x0+x1)/2,0,z)*Rot(0,90,0)*Cylinder(3.3,x1-x0+12)
def curve(p,r):   # inner face follows the round body
    keep = Cylinder(200,400) - Cylinder(r,400)
    return (p & keep).clean()
def fuse(*ps):
    out=ps[0]
    for q in ps[1:]: out=out.fuse(q)
    return out.clean()
yo0=HM+G; kb_top=ZS-R-G
bl=[curve(box(XB0,XO,-W/2,W/2,54.66,kb_top),XB0)]
for a,b in [(-W/2,-yo0),(yo0,W/2)]:
    bl += [curve(box(XB0,XO,a,b,kb_top-0.5,ZS),XB0), box(XC-0.01,XC+R,a,b,ZS-R,ZS), curve(knuck(a,b),XB0+0.1)]
body = fuse(*bl)
body -= bolt(ZB,60,XO)
lid = fuse(curve(box(63.0,XO,-W/2,W/2,ZS+R+G,108.86),XL0), curve(box(63.0,XO,-HM,HM,ZS+0.1,ZS+R+G+0.5),XL0),
      box(XC-0.01,XC+R,-HM,HM,ZS,ZS+R), curve(knuck(-HM,HM),XL0+0.1))
lid -= bolt(ZL,60,XO)
hole=lambda d: Pos(XC,0,ZS)*Rot(90,0,0)*Cylinder(d/2,W+4)
body -= hole(6.1); lid -= hole(6.4)
pin = Pos(XC,0,ZS)*Rot(90,0,0)*Cylinder(3.0,W+1) + Pos(XC,-(W/2+0.5+0.75),ZS)*Rot(90,0,0)*Cylinder(5.0,1.5)
pin = Rot(0,0,TH)*pin
def one(p,n):
    sol=p.solids() if hasattr(p,'solids') else [x for q in p for x in q.solids()]
    print(n,'pieces',[round(x.volume,2) for x in sol])
    return max(sol,key=lambda x:x.volume)
body=one(body,'body'); lid=one(lid,'lid')
body = Rot(0,0,TH)*body; lid = Rot(0,0,TH)*lid
os.makedirs("HINGE_2026-11-18",exist_ok=True)
for n,p in [("H1_Hinge_Body_Leaf",body),("H2_Hinge_Lid_Leaf",lid),("H3_Hinge_Pin",pin)]:
    export_step(p,f"HINGE_2026-11-18/{n}.step"); export_stl(p,f"HINGE_2026-11-18/{n}.stl")
    bb=p.bounding_box(); print(n,"solids",len(p.solids()),"vol %.0f"%p.volume,"z %.2f..%.2f"%(bb.min.Z,bb.max.Z))
parts={}
for f in ["01_Inner_Wall_Tube","02_Outer_Perforated_Tube","05_One_Piece_Top_Cap","06_Lid_Inner_Tube","07_Lid_Outer_Perforated_Tube","08_Lid_Top_Disk","09_Lid_Ceramic_Holder"]:
    s=import_step(f"FAB_PACKAGE_2026-11-12/STEP/{f}.step"); parts[f]=s
    for n,p in [("body",body),("lid",lid),("pin",pin)]:
        r=(s & p); v=r.volume if r is not None else 0
        if v>0.001: print("CLASH",n,f,"%.3f"%v)
for a,b,n in [(pin,lid,"pin-lid"),(pin,body,"pin-body"),(body,lid,"body-lid")]:
    r=a&b; print(n, 0 if r is None else round(r.volume,3))
# open swing: lid leaf + lid parts rotated about the pin, vs body parts
ax=Axis((XC*math.cos(math.radians(TH)),XC*math.sin(math.radians(TH)),ZS),(-math.sin(math.radians(TH)),math.cos(math.radians(TH)),0))
lidset=[lid]+[parts[k] for k in ["06_Lid_Inner_Tube","07_Lid_Outer_Perforated_Tube","08_Lid_Top_Disk","09_Lid_Ceramic_Holder"]]
bodyset=[body]+[parts[k] for k in ["01_Inner_Wall_Tube","02_Outer_Perforated_Tube","05_One_Piece_Top_Cap"]]
for ang in [-15,-45,-90,15,45,90,135]:
    worst=0
    for sgn in [1]:
        for L in lidset:
            Lr=L.rotate(ax,sgn*ang)
            for B in bodyset:
                r=Lr&B; v=sum(x.volume for x in r.solids()) if r is not None else 0; worst=max(worst,v)
    print("open",ang,"overlap %.2f"%worst)
print("done")
