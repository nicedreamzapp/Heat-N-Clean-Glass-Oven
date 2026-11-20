import trimesh, numpy as np, math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
F="FAB_PACKAGE_2026-11-12/STL/"; H="HINGE_2026-11-18/"
th=math.radians(257.5); rad=np.array([math.cos(th),math.sin(th),0]); tan=np.array([-math.sin(th),math.cos(th),0])
piv=rad*70.8+np.array([0,0,94.86]); ctr=rad*66
grey=[0.7,0.72,0.76]
body=[(F+"01_Inner_Wall_Tube.stl",grey),(F+"02_Outer_Perforated_Tube.stl",grey),(F+"05_One_Piece_Top_Cap.stl",[0.6,0.63,0.7]),(H+"H1_Hinge_Body_Leaf.stl",[0.15,0.7,0.25])]
lid=[(F+"06_Lid_Inner_Tube.stl",grey),(F+"07_Lid_Outer_Perforated_Tube.stl",grey),(F+"08_Lid_Top_Disk.stl",[0.6,0.63,0.7]),(F+"09_Lid_Ceramic_Holder.stl",[0.6,0.63,0.7]),(H+"H2_Hinge_Lid_Leaf.stl",[0.15,0.45,0.9])]
def mesh(f,T,crop):
    m=trimesh.load(f)
    c=m.triangles_center; d=np.hypot(c[:,0]-ctr[0],c[:,1]-ctr[1])
    if not f.startswith(H): m.update_faces(d<crop); m.remove_unreferenced_vertices()
    if T is not None: m.apply_transform(T)
    return m
def draw(ax,ang,elev,azim,crop,title):
    M=trimesh.transformations.rotation_matrix(math.radians(ang),tan,piv)
    L=np.array([math.cos(math.radians(azim)),math.sin(math.radians(azim)),0.8]);L/=np.linalg.norm(L)
    cam=np.array([math.cos(math.radians(elev))*math.cos(math.radians(azim)),math.cos(math.radians(elev))*math.sin(math.radians(azim)),math.sin(math.radians(elev))])
    polys=[];cols=[];depth=[]
    for group,T in [(body,None),(lid,M)]:
        for f,col in group:
            m=mesh(f,T,crop); v=m.vertices[m.faces]
            s=np.abs(m.face_normals@L)*0.55+0.4
            polys.append(v);cols.append(np.outer(s,col).clip(0,1));depth.append(m.triangles_center@cam)
    v=np.concatenate(polys);c=np.concatenate(cols);dp=np.concatenate(depth);o=np.argsort(dp)
    ax.add_collection3d(Poly3DCollection(v[o],facecolors=c[o],linewidths=0))
    cc=piv-rad*4+np.array([0,0,-8]); r=34
    ax.set_xlim(cc[0]-r,cc[0]+r);ax.set_ylim(cc[1]-r,cc[1]+r);ax.set_zlim(cc[2]-r,cc[2]+r);ax.set_box_aspect((1,1,1))
    ax.view_init(elev=elev,azim=azim);ax.axis("off");ax.set_title(title,fontsize=14)
fig=plt.figure(figsize=(18,7.5),facecolor="white")
fig.suptitle("NEW HINGE: green leaf bolts to the body top bolt, blue leaf bolts to the lower lid bolt, M3 pin at the seam",fontsize=15,weight="bold")
draw(fig.add_subplot(1,3,1,projection="3d"),0,15,257.5+30,40,"closed, from the back")
draw(fig.add_subplot(1,3,2,projection="3d"),0,0,257.5+90,22,"closed, side view")
draw(fig.add_subplot(1,3,3,projection="3d"),110,0,257.5+90,22,"open, side view")
plt.tight_layout(rect=[0,0,1,0.92]); plt.savefig("Renders/hinge_2026-11-18.png",dpi=85); print("ok")
