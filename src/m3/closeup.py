"""Крупный план 3D-модели из models/<id>.json или из плотной сетки для сравнения.
python3 closeup.py out.png json_path [rot] [camY] [dist]"""
import sys,json,subprocess,time,base64
from playwright.sync_api import sync_playwright
out,js=sys.argv[1],sys.argv[2]
rot=float(sys.argv[3]) if len(sys.argv)>3 else -0.55
cy=float(sys.argv[4]) if len(sys.argv)>4 else .74
dist=float(sys.argv[5]) if len(sys.argv)>5 else .45
html='''<!doctype html><body style="margin:0;background:#dfe3ee"><canvas id=c width=900 height=900></canvas>
<script src="three.min.js"></script><script>
function b64(s){const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u.buffer}
fetch("%s").then(r=>r.json()).then(d=>{
const p=new Int16Array(b64(d.p)),pf=new Float32Array(p.length);for(let i=0;i<p.length;i++)pf[i]=p[i]/30000;
const g=new THREE.BufferGeometry();g.setAttribute("position",new THREE.BufferAttribute(pf,3));
g.setIndex(new THREE.BufferAttribute(new Uint16Array(b64(d.i)),1));
if(d.q){const q=new Int8Array(b64(d.q)),nf=new Float32Array(q.length);for(let i=0;i<q.length;i++)nf[i]=q[i]/127;g.setAttribute("normal",new THREE.BufferAttribute(nf,3))}else g.computeVertexNormals();
const r=new THREE.WebGLRenderer({canvas:c,antialias:true,preserveDrawingBuffer:true});r.setClearColor(0xdfe3ee);
const s=new THREE.Scene(),cam=new THREE.PerspectiveCamera(30,1,.01,10);
const m=new THREE.Mesh(g,new THREE.MeshStandardMaterial({color:0xc8ccd8,roughness:.6}));m.rotation.y=%f;s.add(m);
s.add(new THREE.HemisphereLight(0xffffff,0x8890a8,.45));const l=new THREE.DirectionalLight(0xffffff,.7);l.position.set(1,1.5,2);s.add(l);
cam.position.set(0,%f,%f);cam.lookAt(0,%f,0);r.render(s,cam);window.done=1})
</script>'''%(js.split("/")[-1],rot,cy+0.05,dist,cy)
import os
d=os.path.dirname(os.path.abspath(js)); open(d+"/_cu.html","w").write(html)
import shutil; shutil.copy("/home/claude/proj/three.min.js",d+"/three.min.js")
srv=subprocess.Popen(["python3","-m","http.server","8797","-d",d],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=b.new_page(viewport={"width":900,"height":900})
        pg.goto("http://localhost:8797/_cu.html"); pg.wait_for_function("window.done",timeout=60000); pg.locator("canvas").screenshot(path=out); b.close()
finally: srv.terminate(); os.remove(d+"/_cu.html")
