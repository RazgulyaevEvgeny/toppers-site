/* 3D-движок карточек: ОДИН общий WebGL-рендерер на все карточки.
   Модели грузятся лениво (когда карточка рядом с экраном), рисуются в 2D-холсты карточек.
   Вращается только карточка ближе всего к центру экрана или под курсором. */
(()=>{
if(!window.THREE||window.Eng)return;
const SZ=560,MAXLIVE=24,PAR=3;
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const b64=s=>{const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u.buffer};
const still=matchMedia("(prefers-reduced-motion:reduce)").matches,AMP=.5,CB=new THREE.Vector3(1.75,1.35,3.0);
const V={};let R=null,SHT=null,lostAll=false;

function shared(){if(R)return R;const c=document.createElement("canvas");c.width=c.height=SZ;
c.className="cv3 live";R=new THREE.WebGLRenderer({canvas:c,antialias:true,alpha:true});R.outputEncoding=THREE.sRGBEncoding;R.setClearColor(0x000000,0);R.setPixelRatio(1);R.setSize(SZ,SZ,false);
c.addEventListener("webglcontextlost",e=>{e.preventDefault()});c.addEventListener("webglcontextrestored",()=>{for(const id in V)V[id].dirty=true});return R}

function geo(d){const p=new Int16Array(b64(d.p)),pf=new Float32Array(p.length);for(let i=0;i<p.length;i++)pf[i]=p[i]/30000;
const g=new THREE.BufferGeometry();g.setAttribute("position",new THREE.BufferAttribute(pf,3));g.setIndex(new THREE.BufferAttribute(new Uint16Array(b64(d.i)),1));
if(d.q){const q=new Int8Array(b64(d.q)),nf=new Float32Array(q.length);for(let i=0;i<q.length;i++)nf[i]=q[i]/127;g.setAttribute("normal",new THREE.BufferAttribute(nf,3))}else g.computeVertexNormals();return g}

function shadowTex(){if(SHT)return SHT;const sc=document.createElement("canvas");sc.width=sc.height=128;const x=sc.getContext("2d"),gr=x.createRadialGradient(64,64,0,64,64,64);gr.addColorStop(0,"rgba(30,40,120,.36)");gr.addColorStop(1,"rgba(30,40,120,0)");x.fillStyle=gr;x.fillRect(0,0,128,128);return SHT=new THREE.CanvasTexture(sc)}

function scene(geoMain){
const s=new THREE.Scene(),cam=new THREE.PerspectiveCamera(27.5,1,.1,20);
s.add(new THREE.HemisphereLight(0xffffff,0xaab3ea,.5));
const k=new THREE.DirectionalLight(0xffffff,.78);k.position.set(2,3.2,2.4);s.add(k);
const rim=new THREE.DirectionalLight(0xc9d1ff,.4);rim.position.set(-2.5,1.6,-2);s.add(rim);
const mat=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.48,metalness:0,side:THREE.DoubleSide});
const piv=new THREE.Group(),grp=new THREE.Group();piv.position.y=.44;grp.position.y=-.44;piv.add(grp);s.add(piv);
grp.add(new THREE.Mesh(geoMain,mat));
const sh=new THREE.Mesh(new THREE.PlaneGeometry(1.3,1.3),new THREE.MeshBasicMaterial({map:shadowTex(),transparent:true,depthWrite:false}));sh.rotation.x=-Math.PI/2;sh.position.y=-.006;s.add(sh);
return{s,cam,grp,piv,mat,sh}}

/* ---------- состояние карточки ---------- */
function state(id){let v=V[id];if(v)return v;
const c=document.createElement("canvas");c.width=c.height=SZ;c.className="cv3";c.setAttribute("aria-label","3D-модель, потяните, чтобы повернуть");
v=V[id]={id,c,x:c.getContext("2d"),st:"idle",tries:0,vis:false,seen:0,dirty:false,drag:false,ph:0,base:-.55,rot:-.55,o:0,col:new THREE.Color(1,1,1),tgt:new THREE.Color(1,1,1),init:false,S:null,geo:null,p:null};
c.addEventListener("pointerdown",()=>{forced=v;forcedT=performance.now()});
return v}

let LIVE=null,forced=null,forcedT=0;
(function(){const c=shared().domElement,P=new Map();
c.addEventListener("pointerdown",e=>{const v=LIVE;if(!v||v.st!=="ready")return;P.set(e.pointerId,[e.clientX,e.clientY]);v.drag=true;forcedT=performance.now();try{c.setPointerCapture(e.pointerId)}catch(_){}});
c.addEventListener("pointermove",e=>{const v=LIVE,o=P.get(e.pointerId);if(!o||!v)return;const dx=e.clientX-o[0];P.set(e.pointerId,[e.clientX,e.clientY]);v.rot+=dx*.012;v.dirty=true;forcedT=performance.now()});
const up=e=>{P.delete(e.pointerId);const v=LIVE;if(P.size||!v||!v.drag)return;v.drag=false;v.base=v.rot-AMP*Math.sin(v.ph)};
c.addEventListener("pointerup",up);c.addEventListener("pointercancel",up)})();
function setCol(v,hex,now){v.tgt.set(hex).convertSRGBToLinear();if(now||v.st!=="ready")v.col.copy(v.tgt);v.dirty=true}

/* ---------- ленивая загрузка ---------- */
const Q={list:[],busy:0};
function want(v){if(v.st==="loading"||v.st==="ready"||v.tries>=3||!v.url)return;if(!Q.list.includes(v)){Q.list.push(v);pump()}}
function pump(){while(Q.busy<PAR&&Q.list.length){
let bi=0,bd=1e9;Q.list.forEach((v,i)=>{const r=v.c.getBoundingClientRect(),d=Math.abs(r.top+r.height/2-innerHeight/2)+(v.vis?0:1e4);if(d<bd){bd=d;bi=i}});
const v=Q.list.splice(bi,1)[0];if(v.st==="loading"||v.st==="ready")continue;
Q.busy++;v.st="loading";
fetch(v.url).then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>{
v.o=d.o||0;v.geo=geo(d);v.S=scene(v.geo);v.base=v.rot=-.55+v.o;v.col.copy(v.tgt);v.st="ready";v.dirty=true;v.seen=performance.now();evict()})
.catch(()=>{v.st="idle";v.tries++;if(v.tries<3)setTimeout(()=>want(v),1500*v.tries)})
.finally(()=>{Q.busy--;pump()})}}
function evict(){const live=Object.values(V).filter(v=>v.st==="ready");if(live.length<=MAXLIVE)return;
live.filter(v=>!v.vis).sort((a,b)=>a.seen-b.seen).slice(0,live.length-MAXLIVE).forEach(v=>{try{v.geo.dispose();v.S.sh.geometry.dispose()}catch(e){}v.S=v.geo=null;v.st="idle";v.tries=0})}

/* ---------- привязка к карточкам ---------- */
const io=new IntersectionObserver(es=>es.forEach(e=>{const v=V[e.target.dataset.v];if(!v)return;v.vis=e.isIntersecting;if(v.vis){v.seen=performance.now();want(v);v.dirty=true}}),{rootMargin:"350px 0px"});
const watched=new WeakSet();
function mount(){document.querySelectorAll(".ph[data-v]").forEach(ph=>{const id=ph.dataset.v,m=byId(id),v=state(id);v.url=m.m3;
if(v.c.parentNode!==ph)ph.prepend(v.c);
const hx=colorsOf(m)[sel[id]].c;if(hx!==v.hex){v.hex=hx;setCol(v,hx,!v.init)}v.init=true;if(v.shown)ph.classList.add("ready");
if(!watched.has(ph)){watched.add(ph);io.observe(ph)}});
if(big&&!$("#m3").hidden)refreshBig()}

/* ---------- кадр ---------- */
function paint(v){const r=shared();v.S.mat.color.copy(v.col);v.S.grp.rotation.y=v.rot;v.S.piv.rotation.x=0;v.S.cam.position.copy(CB);v.S.cam.lookAt(0,.44,0);v.S.cam.aspect=1;v.S.cam.updateProjectionMatrix();r.render(v.S.s,v.S.cam);
if(!v.shown){v.shown=true}const ph=v.c.parentNode;ph&&ph.classList.add("ready")}
function snap(v){paint(v);v.x.clearRect(0,0,SZ,SZ);v.x.drawImage(R.domElement,0,0);v.dirty=false}
function draw(v){snap(v)}
let lastT=0;
function frame(t){requestAnimationFrame(frame);if(document.hidden)return;const dt=lastT?Math.min(t-lastT,60):16;lastT=t;
const vis=[];let near=null,bd=1e9,hov=null;
for(const id in V){const v=V[id];if(!v.vis||v.st!=="ready"||!v.c.isConnected)continue;const rc=v.c.getBoundingClientRect();if(rc.bottom<0||rc.top>innerHeight||!rc.width)continue;vis.push(v);const d=Math.hypot(rc.left+rc.width/2-innerWidth/2,rc.top+rc.height/2-innerHeight/2);if(d<bd){bd=d;near=v}if(!hov&&v.c.parentNode.matches(":hover"))hov=v}
if(forced&&(!forced.vis||performance.now()-forcedT>4000)&&!(LIVE&&LIVE.drag))forced=null;
let act=hov||(forced&&forced.st==="ready"?forced:null)||near;if(LIVE&&LIVE.drag)act=LIVE;
let snapped=false;
if(act!==LIVE){if(LIVE&&LIVE.S&&LIVE.c.isConnected){snap(LIVE);snapped=true}if(LIVE)LIVE.c.classList.remove("hid");LIVE=act;if(LIVE)LIVE.dirty=true}
if(LIVE){if(R.domElement.parentNode!==LIVE.c.parentNode)LIVE.c.after(R.domElement);LIVE.c.classList.add("hid")}
let budget=2;
for(const v of vis){
if(!v.col.equals(v.tgt)){v.col.lerp(v.tgt,.2);if(Math.abs(v.col.r-v.tgt.r)+Math.abs(v.col.g-v.tgt.g)+Math.abs(v.col.b-v.tgt.b)<.004)v.col.copy(v.tgt);v.dirty=true}
if(v===LIVE){if(!v.drag&&!still){v.ph+=dt/1500;v.rot=v.base+AMP*Math.sin(v.ph);v.dirty=true}continue}
if(v.dirty&&budget>0){budget--;snap(v);snapped=true}}
if(LIVE&&LIVE.S&&(LIVE.dirty||snapped)){paint(LIVE);LIVE.dirty=false}}
requestAnimationFrame(frame);

/* ---------- миниатюра для корзины ---------- */
const TH={};
function thumb(m,hex){const v=V[m.id];if(!v||v.st!=="ready")return m.img;const k=m.id+hex;if(TH[k])return TH[k];
const oc=v.col.clone(),or=v.rot;v.col.set(hex).convertSRGBToLinear();v.rot=-.55+v.o;draw(v);
const c=document.createElement("canvas");c.width=c.height=200;const x=c.getContext("2d"),g=x.createRadialGradient(100,70,0,100,70,160);g.addColorStop(0,"#dfe1e7");g.addColorStop(.6,"#caced6");g.addColorStop(1,"#b9bcc6");x.fillStyle=g;x.fillRect(0,0,200,200);
x.drawImage(R.domElement,SZ*.12,SZ*.06,SZ*.76,SZ*.76,0,0,200,200);
v.col.copy(oc);v.rot=or;v.dirty=true;if(LIVE)LIVE.dirty=true;return TH[k]=c.toDataURL("image/jpeg",.86)}

/* ---------- большой просмотр ---------- */
document.body.insertAdjacentHTML("beforeend",'<div class="m3" id="m3" hidden role="dialog" aria-modal="true" aria-label="Просмотр 3D-модели"><div class="m3b"><div class="m3h"><b id="m3t"></b><button class="m3x" id="m3x" aria-label="Закрыть">✕</button></div><div class="m3c v3" id="m3c"></div><div class="m3f"><div id="m3s"></div><p>Потяните, чтобы повернуть. Колёсико или щипок для масштаба.</p></div></div></div>');
let big=null;
function openBig(id){const v=state(id),m=byId(id);v.url=m.m3;closeBig();
const go=()=>{if(v.st!=="ready")return;
const c=document.createElement("canvas");c.className="cv3 big";c.setAttribute("aria-label","3D-модель, потяните, чтобы повернуть");
const r=new THREE.WebGLRenderer({canvas:c,antialias:true,alpha:true});r.outputEncoding=THREE.sRGBEncoding;r.setClearColor(0x000000,0);
const S=scene(v.geo),b={id,c,r,S,zoom:.8,tilt:0,rot:-.55+v.o,base:-.55+v.o,ph:0,drag:false,manual:false,w:0,h:0,col:v.col.clone(),tgt:v.col.clone(),raf:0,lt:0};big=b;
const place=()=>{S.cam.position.copy(CB).multiplyScalar(b.zoom);S.cam.lookAt(0,.44,0)};place();
const P=new Map();let pd=0;const dist=()=>{const a=[...P.values()];return Math.hypot(a[0][0]-a[1][0],a[0][1]-a[1][1])};
c.addEventListener("pointerdown",e=>{P.set(e.pointerId,[e.clientX,e.clientY]);b.drag=true;b.manual=true;try{c.setPointerCapture(e.pointerId)}catch(_){}if(P.size===2)pd=dist()});
c.addEventListener("pointermove",e=>{const o=P.get(e.pointerId);if(!o)return;const dx=e.clientX-o[0],dy=e.clientY-o[1];P.set(e.pointerId,[e.clientX,e.clientY]);
if(P.size>=2){const nd=dist();if(pd){b.zoom=clamp(b.zoom*pd/nd,.4,1.4);place()}pd=nd;return}
b.rot+=dx*.012;b.tilt=clamp(b.tilt+dy*.008,-.6,.6)});
const up=e=>{P.delete(e.pointerId);if(P.size)return;pd=0;b.drag=false};
c.addEventListener("pointerup",up);c.addEventListener("pointercancel",up);
c.addEventListener("wheel",e=>{e.preventDefault();b.manual=true;b.zoom=clamp(b.zoom*(1+e.deltaY*.0012),.4,1.4);place()},{passive:false});
$("#m3t").textContent=m.name;$("#m3c").innerHTML='<div class="bls"><i class="bl b1"></i><i class="bl b2"></i><i class="bl b3"></i><i class="bl b4"></i></div><canvas class="spoil"></canvas>';$("#m3c").append(c);
$("#m3").hidden=false;document.documentElement.style.overflow="hidden";
b.col.set(colorsOf(m)[sel[id]].c).convertSRGBToLinear();b.tgt.copy(b.col);refreshBig();setTimeout(()=>$("#m3x").focus(),30);
const loop=t=>{if(big!==b)return;b.raf=requestAnimationFrame(loop);
const w=c.clientWidth,h=c.clientHeight;if(w!==b.w||h!==b.h){b.w=w;b.h=h;r.setPixelRatio(Math.min(devicePixelRatio||1,2));r.setSize(w,h,false);S.cam.aspect=w/h;S.cam.updateProjectionMatrix()}
if(!b.col.equals(b.tgt)){b.col.lerp(b.tgt,.2);if(Math.abs(b.col.r-b.tgt.r)+Math.abs(b.col.g-b.tgt.g)+Math.abs(b.col.b-b.tgt.b)<.004)b.col.copy(b.tgt)}
const dt=b.lt?Math.min(t-b.lt,60):16;b.lt=t;if(!b.drag&&!b.manual&&!still){b.ph+=dt/1500;b.rot=b.base+AMP*Math.sin(b.ph)}
S.mat.color.copy(b.col);S.grp.rotation.y=b.rot;S.piv.rotation.x=b.tilt;r.render(S.s,S.cam)};
b.raf=requestAnimationFrame(loop)};
if(v.st==="ready")go();else{want(v);const t0=Date.now(),w=setInterval(()=>{if(v.st==="ready"){clearInterval(w);go()}else if(Date.now()-t0>15000)clearInterval(w)},120)}}
function refreshBig(){if(!big)return;const m=byId(big.id);$("#m3s").innerHTML=swatches(m);big.tgt.set(colorsOf(m)[sel[m.id]].c).convertSRGBToLinear()}
function closeBig(){const b=big;if(b){big=null;cancelAnimationFrame(b.raf);b.c.remove();try{b.r.forceContextLoss();b.r.dispose()}catch(e){}}$("#m3").hidden=true;document.documentElement.style.overflow=""}
document.addEventListener("click",e=>{const z=e.target.closest("[data-z3]");if(z){openBig(z.dataset.z3);return}if(e.target.id==="m3"||e.target.closest("#m3x"))closeBig()});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!$("#m3").hidden)closeBig()});

window.Eng={mount,thumb,V,ready:true,
/* для сборки постеров: загрузить модель и вернуть картинку */
async poster(id,hex,url){const v=state(id);v.url=url;v.tries=0;want(v);for(let i=0;i<200&&v.st!=="ready";i++)await new Promise(r=>setTimeout(r,50));if(v.st!=="ready")throw new Error("not loaded "+id);
const c=document.createElement("canvas");c.width=c.height=420;const x=c.getContext("2d");v.col.set(hex).convertSRGBToLinear();v.rot=-.55+v.o;draw(v);x.drawImage(R.domElement,0,0,420,420);return c.toDataURL("image/webp",.82)}};
if(window.__engReady)window.__engReady();
mount();
})();
