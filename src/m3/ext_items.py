import re,numpy as np,struct,sys
t=open('x/3D/3dmodel.model',encoding='utf-8').read()
def mesh(oid):
    m=re.search(r'<object id="%d"[^>]*>'%oid,t); s=m.start(); e=t.index("</object>",s); b=t[s:e]
    v=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',b),dtype=np.float64)
    f=np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"',b),dtype=np.int64)
    return v,f
def T(s): a=np.array(s.split(),float); return a[:9].reshape(3,3),a[9:]
items=dict((int(o),T(tr)) for o,tr in re.findall(r'<item objectid="(\d+)" transform="([^"]+)"',t))
def wstl(path,V,F):
    tri=V[F]; n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]); l=np.linalg.norm(n,axis=1,keepdims=True); l[l==0]=1
    dt=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")]); a=np.zeros(len(F),dt); a['n']=n/l; a['v']=tri
    open(path,'wb').write(b' '*80+struct.pack('<I',len(F))+a.tobytes())
for aid,(R,tt) in items.items():
    m=re.search(r'<object id="%d"[^>]*>.*?</object>'%aid,t,re.S).group(0)
    Vs=[];Fs=[];off=0
    for j,(o,tr) in enumerate(re.findall(r'<component objectid="(\d+)" transform="([^"]+)"',m)):
        v,f=mesh(int(o)); r,c=T(tr); v=v@r+c; v=v@R+tt
        wstl(f'out/a{aid}_p{j}.stl',v,f)
        Vs.append(v);Fs.append(f+off);off+=len(v)
        print(aid,j,len(f),np.round(v.min(0),2),np.round(v.max(0),2))
    V=np.vstack(Vs);F=np.vstack(Fs); wstl(f'out/a{aid}.stl',V,F); print(aid,'size',np.round(V.max(0)-V.min(0),2))
