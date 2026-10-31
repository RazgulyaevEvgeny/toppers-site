# затемнение впадин для старых (воксельных) моделей: читаем .bin, добавляем цвета вершин
import struct,numpy as np,sys,os
from hd import cavity
for p in sys.argv[1:]:
    b=open(p,'rb').read(); n,ni,o,fl=struct.unpack('<IIfI',b[:16])
    if fl&1: print('skip',p); continue
    V=np.frombuffer(b,'<i2',3*n,16).reshape(-1,3)/30000*20; N=np.frombuffer(b,'i1',3*n,16+6*n).reshape(-1,3)/127.
    N=N/np.maximum(np.linalg.norm(N,axis=1,keepdims=True),1e-9)
    ao=cavity(V,N); cols=np.repeat(np.round(255*ao)[:,None],3,1).astype(np.uint8)
    off=16+9*n; off+=off&1; end=off+2*ni
    nb=bytearray(b[:end]); nb[12:16]=struct.pack('<I',1); nb+=cols.tobytes(); open(p,'wb').write(nb)
    print(os.path.basename(p),n,round(float((ao<.95).mean()),3))
