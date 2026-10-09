import numpy as np,json
NAMES=("ghost_hat","heart","heart_mouth","ghost_scarf","pig","ghost_broom","ghost")
def load(n):
    f=np.load(f"dec_{n}_0.npz"); s=np.load(f"dec_{n}_s.npz")
    return f["v"],f["f"],s["v"],s["f"]
def normalize(n):
    fv,ff,sv,sf=load(n)
    allv=np.vstack([fv,sv]); mn=allv.min(0); mx=allv.max(0)
    c=np.array([(mn[0]+mx[0])/2,(mn[1]+mx[1])/2,mn[2]]); sc=1/ (mx-mn).max()
    # z-up (3mf) -> y-up (three): (x,y,z)->(x,z,-y)
    def tr(v): v=(v-c)*sc; return np.stack([v[:,0],v[:,2],-v[:,1]],1)
    return tr(fv),ff,tr(sv),sf,(mx-mn)
if __name__=="__main__":
    out={}
    for n in NAMES:
        fv,ff,sv,sf,ext=normalize(n)
        out[n]=dict(fv=np.round(fv,4).flatten().tolist(),ff=ff.flatten().tolist(),sv=np.round(sv,4).flatten().tolist(),sf=sf.flatten().tolist())
        print(n,np.round(ext,1))
    json.dump(out,open("prev.json","w"))
