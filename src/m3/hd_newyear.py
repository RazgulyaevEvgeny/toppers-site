from hd import *
for a,n in (("a3","snowman"),("a6","gift"),("a9","tree"),("a12","santa")):
    build([read_stl(f"/tmp/claude-0/ny/out/{a}_p0.stl")+(None,),read_stl(f"/tmp/claude-0/ny/out/{a}_p1.stl")+(None,)],f"{n}.bin")
import re,numpy as np
from hd import *
def T(s): a=np.array(s.split(),float); return a[:9].reshape(3,3),a[9:]
def decode(s,default):
    nib=[int(ch,16) for ch in reversed(s)]; pos=[0]; acc={}
    def node(w):
        c=nib[pos[0]]; pos[0]+=1; sp=c&3
        if sp==0:
            st=c>>2
            if st==3: st=nib[pos[0]]+3; pos[0]+=1
            st=st or default; acc[st]=acc.get(st,0)+w
        else:
            for _ in range(sp+1): node(w/(sp+1))
    node(1.0); return max(acc,key=acc.get)
def load(path,aid,EXT):
    t=open(path,encoding='utf-8').read()
    m=re.search(r'<object id="%d"[^>]*>.*?</object>'%aid,t,re.S).group(0); parts=[]
    for o,tr in re.findall(r'<component objectid="(\d+)" transform="([^"]+)"',m):
        o=int(o); s=re.search(r'<object id="%d"[^>]*>'%o,t).start(); e=t.index("</object>",s); b=t[s:e]
        v=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',b),dtype=np.float64)
        trs=re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"(?: paint_color="([0-9A-Fa-f]+)")?',b)
        f=np.array([x[:3] for x in trs],dtype=np.int64); L=np.array([decode(x[3],EXT[o]) if x[3] else EXT[o] for x in trs])
        r,c=T(tr); parts.append((v@r+c,f,L))
    return parts
W=(245,245,245);K=(28,28,28);R=(225,30,36)
build(load('/tmp/claude-0/duck/x/3D/3dmodel.model',10,{1:4,2:1,3:1,4:3,5:3,6:2,7:2,8:1,9:1}),'santa_duck.bin',{1:R,2:W,3:K,4:(254,216,1)})
build(load('/tmp/claude-0/bear/x/3D/3dmodel.model',3,{1:5,2:1}),'bear_scarf.bin',{1:W,2:K,3:K,4:R,5:W})
