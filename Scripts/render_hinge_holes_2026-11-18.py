import trimesh, numpy as np, math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
F="FAB_PACKAGE_2026-11-12/STL/"; H="HINGE_2026-11-18/"
th=math.radians(257.5); rad=np.array([math.cos(th),math.sin(th),0])
g=[0.74,0.76,0.8]; d=[0.6,0.63,0.7]
oven=[(F+f,c) for f,c in [("02_Outer_Perforated_Tube.stl",g),("04_Bottom_Cap.stl",d),("05_One_Piece_Top_Cap.stl",d),("07_Lid_Outer_Perforated_Tube.stl",g),("08_Lid_Top_Disk.stl",d),("09_Lid_Ceramic_Holder.stl",d),("10_Lid_Handle.stl",d)]]
def redhole(z):
    c=trimesh.creation.cylinder(radius=3.3,height=4.0)
    c.apply_transform(trimesh.geometry.align_vectors([0,0,1],rad)); c.apply_translation(rad*67.0+np.array([0,0,z])); return c
hinge=[(H+"H1_Hinge_Body_Leaf.stl",[0.1,0.72,0.2]),(H+"H2_Hinge_Lid_Leaf.stl",[0.1,0.72,0.2]),(H+"H3_Hinge_Pin.stl",[1.0,0.55,0.0])]
def draw(ax,items,title):
    azim=257.5-25; elev=10
    cam=np.array([math.cos(math.radians(elev))*math.cos(math.radians(azim)),math.cos(math.radians(elev))*math.sin(math.radians(azim)),math.sin(math.radians(elev))])
    L=cam*0.7+np.array([0,0,0.5]);L/=np.linalg.norm(L)
    P=[];C=[];Dp=[]
    for m,col in items:
        P.append(m.vertices[m.faces]);C.append(np.outer(np.abs(m.face_normals@L)*0.55+0.4,col).clip(0,1));Dp.append(m.triangles_center@cam)
    P=np.concatenate(P);C=np.concatenate(C);o=np.argsort(np.concatenate(Dp))
    ax.add_collection3d(Poly3DCollection(P[o],facecolors=C[o],linewidths=0))
    c=rad*40+np.array([0,0,80.0]); r=55
    ax.set_xlim(c[0]-r,c[0]+r);ax.set_ylim(c[1]-r,c[1]+r);ax.set_zlim(c[2]-r,c[2]+r);ax.set_box_aspect((1,1,1))
    ax.view_init(elev=elev,azim=azim);ax.axis("off");ax.set_title(title,fontsize=16,weight="bold")
base=[(trimesh.load(f),c) for f,c in oven]
holes=[(redhole(61.66),[0.9,0.05,0.05]),(redhole(102.86),[0.9,0.05,0.05])]
fig=plt.figure(figsize=(17,9),facecolor="white")
fig.suptitle("Back of the oven",fontsize=20,weight="bold")
draw(fig.add_subplot(1,2,1,projection="3d"),base+holes,"1. RED = bolt holes already there\n(top one in the lid, bottom one in the body)")
draw(fig.add_subplot(1,2,2,projection="3d"),base+[(trimesh.load(f),c) for f,c in hinge],"2. Hinge bolts onto those 2 holes\nGREEN = hinge leaves, ORANGE = printed pin")
plt.tight_layout(rect=[0,0,1,0.93]); plt.savefig("Renders/hinge_holes_2026-11-18.png",dpi=80); print("ok")
