"""STL -> models/<id>.json  (плавная пересборка через воксели + marching cubes).
Подставка и фигурка объединяются в одну гладкую сетку: пилообразные края, дыры и «рваные» глаза
от прежнего кластерного упрощения исчезают, нормали считаются по сглаженному полю.
Запуск: python3 stl_to_model.py file.stl <id> [vox_mm=0.1] [step=2] [sigma_vox=1.2] [xmin:xmax — взять только часть по оси X]"""
import sys,json,base64,numpy as np
from scipy import ndimage
from skimage.measure import marching_cubes

def read_stl(path):
    b=open(path,"rb").read(); n=int.from_bytes(b[80:84],"little")
    a=np.frombuffer(b[84:84+50*n],dtype=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")]))
    V=a["v"].reshape(-1,3).astype(np.float64)
    u,inv=np.unique(np.round(V,4),axis=0,return_inverse=True)
    return u,inv.reshape(-1,3)

def shell_points(v,f,h):
    """Плотные точки на всех треугольниках (шаг <= h), чтобы оболочка была замкнутой."""
    a,b,c=v[f[:,0]],v[f[:,1]],v[f[:,2]]
    L=np.maximum.reduce([np.linalg.norm(b-a,axis=1),np.linalg.norm(c-b,axis=1),np.linalg.norm(a-c,axis=1)])
    n=np.maximum(1,np.ceil(L/h).astype(int)); pts=[v]
    for k in np.unique(n):
        m=n==k; A,B,C=a[m],b[m],c[m]
        ij=[(i,j) for i in range(k+1) for j in range(k+1-i)]
        for i,j in ij:
            w1,w2=i/k,j/k; pts.append(A*(1-w1-w2)+B*w1+C*w2)
    return np.vstack(pts)

def build(path,vox=0.1,step=2,sigma=1.0,xr=None):
    v,f=read_stl(path)
    if xr:
        cx=v[f][:,:,0].mean(1); f=f[(cx>=xr[0])&(cx<xr[1])]
        u=np.unique(f); rm=-np.ones(len(v),int); rm[u]=np.arange(len(u)); v=v[u]; f=rm[f]
    mn=v.min(0); mx=v.max(0)
    pad=4
    pts=shell_points(v,f,vox*0.6)
    idx=np.floor((pts-mn)/vox).astype(int)+pad
    shape=tuple(idx.max(0)+pad+1)
    shell=np.zeros(shape,bool); shell[idx[:,0],idx[:,1],idx[:,2]]=True
    pass
    lab,_=ndimage.label(~shell)                              # 6-связная заливка снаружи
    outside=lab==lab[0,0,0]
    inside=~outside
    # знаковое поле расстояния: гладкое, без «ступенек» вокселей
    sdf=(ndimage.distance_transform_edt(outside)-ndimage.distance_transform_edt(inside)).astype(np.float32)
    sdf=ndimage.gaussian_filter(sdf,sigma)
    vv,ff,nn,_=marching_cubes(sdf,level=0.0,spacing=(vox,)*3,step_size=step)
    vv=vv+mn-pad*vox
    # ориентация граней: положительный объём = наружу
    vol=np.einsum("ij,ij->i",vv[ff[:,0]],np.cross(vv[ff[:,1]],vv[ff[:,2]])).sum()/6
    if vol<0: ff=ff[:,::-1]
    # нормали должны смотреть наружу (по росту поля расстояния)
    fn=np.cross(vv[ff[:,1]]-vv[ff[:,0]],vv[ff[:,2]]-vv[ff[:,0]]); mv=np.zeros_like(vv)
    for k in range(3): np.add.at(mv,ff[:,k],fn)
    if (mv*nn).sum()<0: nn=-nn
    return vv,ff,nn,mn,mx

if __name__=="__main__":
    path,mid=sys.argv[1],sys.argv[2]
    vox=float(sys.argv[3]) if len(sys.argv)>3 else .1
    step=int(sys.argv[4]) if len(sys.argv)>4 else 2
    sg=float(sys.argv[5]) if len(sys.argv)>5 else 1.2
    xr=tuple(float(t) for t in sys.argv[6].split(':')) if len(sys.argv)>6 else None
    vv,ff,nn,mn,mx=build(path,vox,step,sg,xr)
    print("mesh verts",len(vv),"tris",len(ff),flush=True)
    assert len(vv)<65536,"слишком много вершин: увеличьте step или vox"
    c=np.array([(mn[0]+mx[0])/2,(mn[1]+mx[1])/2,mn[2]]); sc=1/(mx-mn).max()
    P=lambda x:np.stack([x[:,0],x[:,2],-x[:,1]],1)
    V=P((vv-c)*sc); N=P(nn); N/=np.maximum(np.linalg.norm(N,axis=1,keepdims=True),1e-9)
    F=ff.copy()
    o=float(sys.argv[7]) if len(sys.argv)>7 else 0.0
    sys.path.insert(0,"/home/claude/m3")
    from json2bin import write_bin
    write_bin("/home/claude/proj/models/%s.bin"%mid,np.round(V*30000).astype("<i2").flatten(),np.round(N*127).astype("i1").flatten(),F.astype("<u2").flatten(),o)
    print("ok",mid,len(V),len(F),"o=",o)
