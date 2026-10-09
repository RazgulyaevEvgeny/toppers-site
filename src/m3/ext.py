import re,numpy as np
X="/home/claude/m3/x"
main=open(X+"/3D/3dmodel.model",encoding="utf-8").read()
cache={}
def mesh(path,oid):
    if path not in cache: cache[path]=open(X+path,encoding="utf-8").read()
    t=cache[path]
    m=re.search(r'<object id="%d"[^>]*>'%oid,t); s=m.start(); e=t.index("</object>",s); b=t[s:e]
    v=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',b),dtype=np.float64)
    f=np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"',b),dtype=np.int64)
    return v,f
def parts(aid):
    m=re.search(r'<object id="%d"[^>]*>.*?</object>'%aid,main,re.S).group(0)
    out=[]
    for c in re.finditer(r'<component p:path="([^"]+)" objectid="(\d+)"[^>]*transform="([^"]+)"',m):
        p,o,tr=c.group(1),int(c.group(2)),np.array(c.group(3).split(),dtype=float)
        v,f=mesh(p,o); out.append((v@tr[:9].reshape(3,3)+tr[9:],f))
    return out
if __name__=="__main__":
    names={66:"ghost_hat",32:"heart",20:"heart_mouth",10:"ghost_scarf",16:"pig",8:"ghost_broom",6:"ghost"}
    for aid,n in names.items():
        for i,(v,f) in enumerate(parts(aid)):
            np.savez(f"/home/claude/m3/raw_{n}_{i}.npz",v=v,f=f)
            print(n,i,len(f),np.round(v.min(0),1).tolist(),np.round(v.max(0),1).tolist(),flush=True)
