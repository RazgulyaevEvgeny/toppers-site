"""models/<id>.json (base64) -> models/<id>.bin (бинарный: заголовок 16 байт + int16 xyz + int8 нормали + uint16 индексы)."""
import sys,json,base64,struct,numpy as np,os
def write_bin(path,p,q,i,o=0.0):
    n=len(p)//3; ni=len(i)
    b=bytearray(struct.pack("<IIfI",n,ni,o,0))
    b+=p.astype("<i2").tobytes()+q.astype("i1").tobytes()
    if len(b)&1: b+=b"\0"
    b+=i.astype("<u2").tobytes()
    open(path,"wb").write(b)
if __name__=="__main__":
    for f in sys.argv[1:]:
        d=json.load(open(f))
        p=np.frombuffer(base64.b64decode(d["p"]),"<i2"); q=np.frombuffer(base64.b64decode(d["q"]),"i1"); i=np.frombuffer(base64.b64decode(d["i"]),"<u2")
        out=f[:-5]+".bin"; write_bin(out,p,q,i,float(d.get("o",0)))
        print(os.path.basename(out),os.path.getsize(f)//1024,"KB json ->",os.path.getsize(out)//1024,"KB bin")
