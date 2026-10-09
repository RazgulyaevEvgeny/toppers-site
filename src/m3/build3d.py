import numpy as np,json,base64
from scipy.spatial import cKDTree
from dec import decimate
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
def load(n,j):
    d=np.load(f"raw_{n}_{j}.npz"); return d["v"],d["f"]
def dloaded(n,suffix): d=np.load(f"dec_{n}_{suffix}.npz"); return d["v"],d["f"]
jobs={}
for n in ("ghost_hat","ghost","pig","heart"):
    jobs[n]={"fig":(load(n,0),dloaded(n,0)),"stand":(load(n,1),dloaded(n,"s"))}
n="heart_mouth"
jobs["heart_knit"]={"fig":(load(n,0),decimate(*load(n,0),46000)),"mouth":(load(n,1),decimate(*load(n,1),2000)),"stand":(load(n,2),decimate(*load(n,2),2500))}
for n in ("ghost_scarf","ghost_broom"):
    jobs[n]={"fig":(load(n,0),decimate(*load(n,0),30000)),"stand":(load(n,1),decimate(*load(n,1),2500))}
out={}
for name,parts in jobs.items():
    res={}
    allv=np.vstack([p[1][0] for p in parts.values()]); mn=allv.min(0); mx=allv.max(0)
    c=np.array([(mn[0]+mx[0])/2,(mn[1]+mx[1])/2,mn[2]]); sc=1/(mx-mn).max()
    P=lambda v:np.stack([v[:,0],v[:,2],-v[:,1]],1)
    for k,((rv,rf),(dv,df)) in parts.items():
        nn,df2,fr=part(rv,rf,dv,df)
        res[k]=(P((dv-c)*sc),P(nn),df2)
        print(name,k,len(df2),"flipped %.1f%%"%(fr*100),flush=True)
    def enc(items):
        V=np.vstack([x[0] for x in items]);N=np.vstack([x[1] for x in items]);off=0;F=[]
        for x in items: F.append(x[2]+off); off+=len(x[0])
        F=np.vstack(F)
        return {"p":base64.b64encode(np.round(V*30000).astype("<i2").tobytes()).decode(),"q":base64.b64encode(np.round(N*127).astype("i1").tobytes()).decode(),"i":base64.b64encode(F.astype("<u2").flatten().tobytes()).decode()}
    body=[res["fig"],res["stand"]]+([res["mouth"]] if "mouth" in res else [])
    out[name]=enc(body)
out["heart_knit"]["o"]=1.0
json.dump(out,open("m3d.json","w")); print(len(json.dumps(out)))
