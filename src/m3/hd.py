"""Детальная сборка: исходная сетка из 3MF -> квадратичное упрощение (fast_simplification) -> models/<id>.bin.
parts: список (v,f,lab) — lab: метка цвета на треугольник или None. colors: {метка:(r,g,b)} -> цвета вершин (флаг 1)."""
import numpy as np,struct,sys
import fast_simplification as fs
sys.path.insert(0,'/home/claude/m3')
from json2bin import write_bin
from scipy.spatial import cKDTree
def weld(v,f):
    u,inv=np.unique(np.round(v,5),axis=0,return_inverse=True); f=inv.reshape(-1)[f]
    f=f[(f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2])]; return u,f
def vnorm(v,f):
    a,b,c=v[f[:,0]],v[f[:,1]],v[f[:,2]]; fn=np.cross(b-a,c-a); n=np.zeros_like(v)
    for k in range(3): np.add.at(n,f[:,k],fn)
    l=np.linalg.norm(n,axis=1,keepdims=True); l[l==0]=1; return n/l
def build(parts,out,colors=None,budget=64000,stand=True):
    W=[weld(v,f) for v,f,_ in parts]; Ns=[]
    if stand:  # подставка: плоские грани, без размытых нормалей на рёбрах
        sv,sf=W[-1]; sv,sf=fs.simplify(sv.astype(np.float32),sf.astype(np.int32),target_count=2400); sv=sv.astype(float); sf=sf.astype(int)
        a,b,c=sv[sf[:,0]],sv[sf[:,1]],sv[sf[:,2]]; fn=np.cross(b-a,c-a); fn/=np.maximum(np.linalg.norm(fn,axis=1,keepdims=True),1e-12)
        W[-1]=(sv[sf].reshape(-1,3),np.arange(3*len(sf)).reshape(-1,3)); flatN=np.repeat(fn,3,0)
    budget-=len(W[-1][0]) if stand else 0
    tot=sum(len(v) for v,_ in (W[:-1] if stand else W))
    Vs=[];Fs=[];Ls=[];off=0
    for pi,((v,f),(_,_,lab),(ov,of,_)) in enumerate(zip(W,[(None,None,p[2]) for p in parts],parts)):
        last=stand and pi==len(W)-1
        share=len(v)+1 if last else budget*len(v)/tot
        if len(v)>share:
            v2,f2=fs.simplify(v.astype(np.float32),f.astype(np.int32),target_reduction=1-share/len(v)*0.97); v2=v2.astype(float); f2=f2.astype(int)
        else: v2,f2=v,f
        if lab is not None:
            cen=ov[of].mean(1); _,ix=cKDTree(cen).query(v2); Ls.append(lab[ix])
        Ns.append(flatN if last else vnorm(v2,f2)); Vs.append(v2);Fs.append(f2+off);off+=len(v2)
    V=np.vstack(Vs);F=np.vstack(Fs); assert len(V)<65536,len(V)
    N=np.vstack(Ns)
    mn=V.min(0);mx=V.max(0); c=np.array([(mn[0]+mx[0])/2,(mn[1]+mx[1])/2,mn[2]]); sc=1/(mx-mn).max()
    P=lambda x:np.stack([x[:,0],x[:,2],-x[:,1]],1)
    write_bin(out,np.round(P((V-c)*sc)*30000).astype("<i2").flatten(),np.round(P(N)*127).astype("i1").flatten(),F.astype("<u2").flatten(),0.0)
    if colors:
        L=np.concatenate(Ls); cols=np.array([colors[k] for k in L],np.uint8)
        b=bytearray(open(out,'rb').read()); b[12:16]=struct.pack('<I',1); b+=cols.tobytes(); open(out,'wb').write(b)
    import os; print(out,len(V),len(F),os.path.getsize(out)//1024,"KB")
def read_stl(p):
    b=open(p,'rb').read();n=int.from_bytes(b[80:84],'little')
    v=np.frombuffer(b[84:84+50*n],dtype=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")]))['v'].reshape(-1,3).astype(float)
    return v,np.arange(len(v)).reshape(-1,3)
