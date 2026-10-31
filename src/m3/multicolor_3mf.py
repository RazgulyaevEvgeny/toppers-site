import re,sys,numpy as np,struct
sys.path.insert(0,'/home/claude/m3')
import stl_to_model2 as S
from json2bin import write_bin
from scipy.spatial import cKDTree
t=open('x/3D/3dmodel.model',encoding='utf-8').read()
def mesh(oid):
    m=re.search(r'<object id="%d"[^>]*>'%oid,t); s=m.start(); e=t.index("</object>",s); b=t[s:e]
    v=np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"',b),dtype=np.float64)
    f=np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"',b),dtype=np.int64); return v,f
def T(s): a=np.array(s.split(),float); return a[:9].reshape(3,3),a[9:]
EXT={1:4,2:1,3:1,4:3,5:3,6:2,7:2,8:1,9:1}
COL={1:(230,30,36),2:(250,250,250),3:(28,28,28),4:(254,216,1)}
m=re.search(r'<object id="10"[^>]*>.*?</object>',t,re.S).group(0)
Vs=[];Fs=[];off=0;pts=[];lab=[]
for o,tr in re.findall(r'<component objectid="(\d+)" transform="([^"]+)"',m):
    v,f=mesh(int(o)); r,c=T(tr); v=v@r+c
    Vs.append(v);Fs.append(f+off);off+=len(v)
    p=S.shell_points(v,f,0.08); pts.append(p); lab.append(np.full(len(p),EXT[int(o)]))
V=np.vstack(Vs);F=np.vstack(Fs)
tri=V[F]; dt=np.dtype([("n","<f4",3),("v","<f4",(3,3)),("a","<u2")]); a=np.zeros(len(F),dt); a['v']=tri
open('duck.stl','wb').write(b' '*80+struct.pack('<I',len(F))+a.tobytes())
print('size',V.max(0)-V.min(0))
vox=float(sys.argv[1]) if len(sys.argv)>1 else .12
vv,ff,nn,mn,mx=S.build('duck.stl',vox,1,1.0)
print('verts',len(vv)); assert len(vv)<65536
_,ix=cKDTree(np.vstack(pts)).query(vv); L=np.concatenate(lab)[ix]
cols=np.array([COL[k] for k in L],np.uint8)
c=np.array([(mn[0]+mx[0])/2,(mn[1]+mx[1])/2,mn[2]]); sc=1/(mx-mn).max()
P=lambda x:np.stack([x[:,0],x[:,2],-x[:,1]],1)
Vn=P((vv-c)*sc); N=P(nn); N/=np.maximum(np.linalg.norm(N,axis=1,keepdims=True),1e-9)
write_bin('santa_duck.bin',np.round(Vn*30000).astype("<i2").flatten(),np.round(N*127).astype("i1").flatten(),ff.astype("<u2").flatten(),0.0)
# append colors, set flag
b=bytearray(open('santa_duck.bin','rb').read()); b[12:16]=struct.pack('<I',1); b+=cols.tobytes(); open('santa_duck.bin','wb').write(b)
print('ok',len(b),np.bincount(L))
