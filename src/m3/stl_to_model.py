import numpy as np,json,base64
from scipy.spatial import cKDTree
def vnormals(v,f):
    a,b,c=v[f[:,0]],v[f[:,1]],v[f[:,2]]
    fn=np.cross(b-a,c-a)  # area-weighted
    n=np.zeros_like(v)
    for k in range(3): np.add.at(n,f[:,k],fn)
    l=np.linalg.norm(n,axis=1,keepdims=True); l[l==0]=1
    return n/l
def part(rawv,rawf,dv,df):
    n0=vnormals(rawv,rawf)
    _,ix=cKDTree(rawv).query(dv); nn=n0[ix]
    # fix winding of decimated faces to agree with vertex normals
    a,b,c=dv[df[:,0]],dv[df[:,1]],dv[df[:,2]]
    g=np.cross(b-a,c-a); avg=nn[df].sum(1)
    flip=(g*avg).sum(1)<0
    df=df.copy(); df[flip,1],df[flip,2]=df[flip,2].copy(),df[flip,1].copy()
    return nn,df,flip.mean()

import sys,json,base64,numpy as np
sys.path.insert(0,"/home/claude/m3")
from dec import decimate
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
def read_stl(path):
    b=open(path,"rb").read(); n=int.from_bytes(b[80:84],"little")
    a=np.frombuffer(b[84:84+50*n],dtype=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")]))
    V=a["v"].reshape(-1,3).astype(np.float64)
    u,inv=np.unique(np.round(V,4),axis=0,return_inverse=True)
    return u,inv.reshape(-1,3)
def components(v,f):
    e=np.vstack([f[:,[0,1]],f[:,[1,2]]])
    g=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(v),len(v)))
    nc,lab=connected_components(g,directed=False); fl=lab[f[:,0]]
    out=[]
    for c in range(nc):
        m=fl==c
        if m.sum()<50: continue
        ff=f[m]; used=np.unique(ff); rm=-np.ones(len(v),int); rm[used]=np.arange(len(used))
        out.append((v[used],rm[ff]))
    out.sort(key=lambda t:-len(t[1]))   # 0 = фигурка, 1 = подставка
    return out
if __name__=="__main__":
    path,mid=sys.argv[1],sys.argv[2]
    ft=int(sys.argv[3]) if len(sys.argv)>3 else 30000
    st=int(sys.argv[4]) if len(sys.argv)>4 else 2500
    v,f=read_stl(path); comps=components(v,f)
    print("components",[len(c[1]) for c in comps],flush=True)
    targets=[ft]+[st]*(len(comps)-1)
    parts=[((rv,rf),decimate(rv,rf,t)) for (rv,rf),t in zip(comps,targets)]
    allv=np.vstack([p[1][0] for p in parts]); mn=allv.min(0); mx=allv.max(0)
    c=np.array([(mn[0]+mx[0])/2,(mn[1]+mx[1])/2,mn[2]]); sc=1/(mx-mn).max()
    P=lambda x:np.stack([x[:,0],x[:,2],-x[:,1]],1)
    V=[];N=[];F=[];off=0
    for (rv,rf),(dv,df) in parts:
        nn,df2,fr=part(rv,rf,dv,df); print("part",len(df2),"flipped %.1f%%"%(fr*100),flush=True)
        V.append(P((dv-c)*sc));N.append(P(nn));F.append(df2+off);off+=len(dv)
    V=np.vstack(V);N=np.vstack(N);F=np.vstack(F)
    assert len(V)<65536
    out={"p":base64.b64encode(np.round(V*30000).astype("<i2").tobytes()).decode(),
         "q":base64.b64encode(np.round(N*127).astype("i1").tobytes()).decode(),
         "i":base64.b64encode(F.astype("<u2").flatten().tobytes()).decode()}
    json.dump(out,open("/home/claude/proj/models/%s.json"%mid,"w")); print("ok",mid,len(V),len(F))
