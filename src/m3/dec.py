import numpy as np
def clean(v,f):
    # weld duplicate verts (3mf usually indexed already)
    f=f[(f[:,0]!=f[:,1])&(f[:,1]!=f[:,2])&(f[:,0]!=f[:,2])]
    used=np.unique(f); remap=-np.ones(len(v),int); remap[used]=np.arange(len(used))
    return v[used],remap[f]
def cluster(v,f,cell,reg=4e-2):
    mn=v.min(0)-1e-6
    ijk=np.floor((v-mn)/cell).astype(np.int64)
    key=(ijk[:,0]*100003+ijk[:,1])*100019+ijk[:,2]
    uk,inv=np.unique(key,return_inverse=True)
    n=len(uk)
    # face planes -> quadrics
    a=v[f[:,0]];b=v[f[:,1]];c=v[f[:,2]]
    nn=np.cross(b-a,c-a); area=np.linalg.norm(nn,axis=1)/2
    ok=area>1e-12
    nu=np.zeros_like(nn); nu[ok]=nn[ok]/(2*area[ok,None])
    d=-(nu*a).sum(1)
    p=np.concatenate([nu,d[:,None]],1)           # plane
    Q=(p[:,:,None]*p[:,None,:])*area[:,None,None]  # per-face quadric
    Qv=np.zeros((len(v),4,4))
    for k in range(3): np.add.at(Qv,f[:,k],Q/3)
    Qc=np.zeros((n,4,4)); np.add.at(Qc,inv,Qv)
    cnt=np.bincount(inv,minlength=n).astype(float)
    mean=np.zeros((n,3)); np.add.at(mean,inv,v); mean/=cnt[:,None]
    A=Qc[:,:3,:3]; bvec=-Qc[:,:3,3]
    tr=np.trace(A,axis1=1,axis2=2)/3+1e-12
    A2=A+np.eye(3)*(reg*tr)[:,None,None]
    # regularise toward mean: (A+λI)x = b+λ mean
    lam=(reg*tr)[:,None]
    rhs=bvec+lam*mean
    try: x=np.linalg.solve(A2,rhs[:,:,None])[:,:,0]
    except np.linalg.LinAlgError: x=mean
    # clamp to cell neighbourhood of mean
    x=np.clip(x,mean-.6*cell,mean+.6*cell)
    nf=inv[f]
    nf=nf[(nf[:,0]!=nf[:,1])&(nf[:,1]!=nf[:,2])&(nf[:,0]!=nf[:,2])]
    # dedupe faces
    s=np.sort(nf,1); _,ix=np.unique(s,axis=0,return_index=True); nf=nf[np.sort(ix)]
    return clean(x,nf)
def decimate(v,f,target):
    v,f=clean(v,f)
    ext=(v.max(0)-v.min(0)).max()
    lo,hi=ext/600,ext/6
    best=None
    for _ in range(22):
        mid=(lo*hi)**.5
        nv,nf=cluster(v,f,mid)
        if len(nf)>target: lo=mid
        else: hi=mid; best=(nv,nf)
    return best
