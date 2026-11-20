import trimesh, numpy as np, math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Ellipse
F="FAB_PACKAGE_2026-11-12/STL/"; H="HINGE_2026-11-18/"
th=math.radians(257.5); rad=np.array([math.cos(th),math.sin(th),0]); tan=np.array([-math.sin(th),math.cos(th),0])
piv=rad*70.8+np.array([0,0,94.86])
g=[0.72,0.74,0.78]; d=[0.58,0.61,0.68]
body=[(F+"02_Outer_Perforated_Tube.stl",g),(F+"04_Bottom_Cap.stl",d),(F+"05_One_Piece_Top_Cap.stl",d),(H+"H1_Hinge_Body_Leaf.stl",[0.1,0.75,0.2])]
lid=[(F+"07_Lid_Outer_Perforated_Tube.stl",g),(F+"08_Lid_Top_Disk.stl",d),(F+"09_Lid_Ceramic_Holder.stl",d),(F+"10_Lid_Handle.stl",d),(H+"H2_Hinge_Lid_Leaf.stl",[0.1,0.75,0.2])]
cache={}
def load(f):
    if f not in cache: cache[f]=trimesh.load(f)
    return cache[f].copy()
def draw(ax,ang,title):
    azim=257.5-35; elev=18
    M=trimesh.transformations.rotation_matrix(math.radians(ang),tan,piv)
    cam=np.array([math.cos(math.radians(elev))*math.cos(math.radians(azim)),math.cos(math.radians(elev))*math.sin(math.radians(azim)),math.sin(math.radians(elev))])
    L=cam*0.6+np.array([0,0,0.6]);L/=np.linalg.norm(L)
    P=[];C=[];Dp=[]
    for grp,T in [(body,None),(lid,M)]:
        for f,col in grp:
            m=load(f)
            if T is not None: m.apply_transform(T)
            P.append(m.vertices[m.faces]);C.append(np.outer(np.abs(m.face_normals@L)*0.55+0.4,col).clip(0,1));Dp.append(m.triangles_center@cam)
    P=np.concatenate(P);C=np.concatenate(C);o=np.argsort(np.concatenate(Dp))
    ax.add_collection3d(Poly3DCollection(P[o],facecolors=C[o],linewidths=0))
    c=np.array([0,0,50.0])+rad*25; r=100
    ax.set_xlim(c[0]-r,c[0]+r);ax.set_ylim(c[1]-r,c[1]+r);ax.set_zlim(c[2]-r,c[2]+r);ax.set_box_aspect((1,1,1))
    ax.view_init(elev=elev,azim=azim);ax.axis("off");ax.set_title(title,fontsize=17,weight="bold")
fig=plt.figure(figsize=(16,8.5),facecolor="white")
fig.suptitle("The hinge (GREEN) on the whole oven, seen from the back",fontsize=19,weight="bold")
draw(fig.add_subplot(1,2,1,projection="3d"),0,"Lid closed")
draw(fig.add_subplot(1,2,2,projection="3d"),100,"Lid open")
plt.tight_layout(rect=[0,0,1,0.93]); plt.savefig("Renders/hinge_whole_oven_2026-11-18.png",dpi=80); print("ok")
