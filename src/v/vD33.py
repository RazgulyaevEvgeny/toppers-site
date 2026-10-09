from common import *
from illus import SVG as ILL
LOGO=open('/home/claude/v/logo_blue.b64').read()

import common
def _r(txt,a,b,tag):
    assert a in txt,tag
    return txt.replace(a,b,1)
CP=common.CORE_POST
CP=_r(CP,r'''$("#barL").textContent=`Корзина: ${cnt} шт`;''',r'''$("#barL").textContent=cnt||"";''',"barL")
CP=_r(CP,'if(!L.length)$("#ov").classList.remove("on");','',"ov")
CP=_r(CP,'if(a==="add")cart[k]=Math.max(st,minOf(m)-T);','if(a==="add")cart[k]=addQty(m,k);',"add")
CP=_r(CP,'const b=bad();','const b=bad(),lo=L.length>0&&cnt<CONFIG.minQty,nc=L.some(l=>l.m.custom)&&!$("#cdesc").value.trim(),blk=lo||nc||!L.length;',"bad")
CP=_r(CP,'.join(", ")}`:"";','.join(", ")}`:nc?"Опишите, какую модель вы хотите заказать":"";',"warn")
CP=_r(CP,'$("#wa").classList.toggle("off",b.length>0);','$("#wa").classList.toggle("off",blk);',"off")
CP=_r(CP,'$("#wa").href=b.length?"#":','$("#wa").href=blk?"#":',"href")
CP=_r(CP,r'''s+=`\nИтого: ${fmt(tot)}`''',r'''const cd=$("#cdesc").value.trim();if(cu&&cd)s+=`\nОписание своей модели: ${cd}`;s+=`\nИтого: ${fmt(tot)}`''',"msg")
CP=_r(CP,'const ls=MODELS.filter(','$("#customBox").hidden=!L.some(l=>l.m.custom);if(!L.length)$("#list").innerHTML=\'<p class="empty">Корзина пока пуста. Добавьте модели из каталога.</p>\';\nconst ls=MODELS.filter(',"list")
CP=_r(CP,'$("#note").oninput=render;','$("#note").oninput=$("#cdesc").oninput=render;',"oninput")
CP=_r(CP,'$("#warn").textContent=b.length?`Не хватает до минимума: ${b.map(m=>`${m.name} (от ${minOf(m)} шт)`).join(", ")}`:nc?','$("#warn").textContent=lo?`В корзине ${cnt} шт. Минимальный заказ — ${CONFIG.minQty} шт, оформить меньше нельзя. Добавьте в корзину ещё моделек: нужно ещё ${CONFIG.minQty-cnt} шт.`:nc?',"warn2")
CP=_r(CP,'$("#barR").textContent=fmt(tot);','',"barR2")
CP=_r(CP,'<img src="${l.m.img}" alt="">','<img src="${th3(l.m,c.c)}" alt="">',"th3")
CP=_r(CP,'$("#grid").innerHTML=MODELS.map(card).join("");','renderGrid();mount3d();watchVis();',"mount")
CP=_r(CP,'<div class="qty"><button data-a="dec" data-k="${l.k}"','<div class="ctl"><div class="qty"><button data-a="dec" data-k="${l.k}"',"ctl1")
CP=_r(CP,'aria-label="Больше">+</button></div></div>`}).join("")','aria-label="Больше">+</button></div><button class="del" data-a="del" data-k="${l.k}" aria-label="Удалить позицию" title="Удалить"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 12.2a2 2 0 0 0 2 1.8h6a2 2 0 0 0 2-1.8L18 7M9 7V4.5A1.5 1.5 0 0 1 10.5 3h3A1.5 1.5 0 0 1 15 4.5V7"/></svg></button></div></div>`}).join("")',"ctl2")
CP=_r(CP,'if(a==="add")cart[k]=addQty(m,k);','if(a==="del")delete cart[k];if(a==="add")cart[k]=addQty(m,k);',"del")
CP=_r(CP,'if(a==="add")cart[k]=addQty(m,k);','if(a==="add"){const v=addQty(m);if(!v)return;cart[k]=q+v;draft[m.id]="";added=k;clearTimeout(addedT);addedT=setTimeout(()=>{added=null;syncDraft()},1300)}',"addq")
CP=_r(CP,'renderGrid();mount3d();watchVis();','renderGrid();syncDraft();mount3d();watchVis();',"sync")
common.CORE_POST=CP
CPRE=common.CORE_PRE
CPRE=_r(CPRE,'const minOf=m=>m.minQty||CONFIG.minQty','const minOf=m=>0',"minOf")
CPRE=_r(CPRE,'noPrice:true,minQty:100,step:50,','noPrice:true,',"cust")
CPRE=_r(CPRE,'const bad=()=>MODELS.filter(m=>{const T=total(m.id);return T&&T<minOf(m)});','const bad=()=>[];',"bad")
_i=CPRE.index("colors:["); _j=CPRE.index("],",_i)+1
CPRE=CPRE[:_i]+'colors:[{n:"Белый",c:"#ffffff"},{n:"Жёлтый",c:"#f5b800"},{n:"Оранжевый",c:"#ff7a0d"},{n:"Красный",c:"#ff3b30"},{n:"Розовый",c:"#f0537f"},{n:"Бордовый",c:"#a02b50"},{n:"Чёрный",c:"#262626"},{n:"Синий",c:"#2563eb",na:1},{n:"Фиолетовый",c:"#7c3aed",na:1},{n:"Зелёный",c:"#16a34a",na:1}]'+CPRE[_j:]
import re,json,os
def fixmodels(t):
    cat=json.load(open(os.environ.get('PROJ','/home/claude/proj')+'/catalog.json',encoding='utf-8'))
    def ln(c):
        tiers=",".join("{from:%d,price:%d}"%(a,b) for a,b in c["tiers"])
        return '  {id:%s,name:%s,def:"Белый",tiers:[%s],img:%s,m3:%s%s},'%(json.dumps(c["id"]),json.dumps(c["name"],ensure_ascii=False),tiers,json.dumps("posters/%s.webp"%c["id"]),json.dumps("models/%s.bin"%c["id"]),(",fix:"+json.dumps(c["fix"],ensure_ascii=False)) if c.get("fix") else "")
    i=t.index("const MODELS=["); j=t.index("\n];",i)
    blk=t[i:j]; cu=[l for l in blk.split("\n") if l.strip().startswith('{id:"custom"')][0].rstrip(",")
    return t[:i]+"const MODELS=[\n"+"\n".join(ln(c) for c in cat)+"\n"+cu+t[j:]
CPRE=fixmodels(CPRE)
common.CORE_PRE=CPRE
HP=common.HELPERS
a=HP.index("const ctrl=");b=HP.index("\n",a)
HP=HP[:a]+r'''const draft={};
const dget=m=>draft[m.id]===undefined?CONFIG.minQty:draft[m.id];
const qbox=m=>{if(!m.custom&&colorsOf(m)[sel[m.id]].na)return `<button class="add" disabled>Цвета нет в наличии</button>`;return `<div class="addrow"><div class="qty dq"><button type="button" data-dq="-1" data-m="${m.id}" aria-label="Меньше">−</button><span class="qw"><input class="qn qp" type="text" inputmode="numeric" placeholder="0" data-m="${m.id}" aria-label="Сколько штук добавить" autocomplete="off"><span>шт</span></span><button type="button" data-dq="1" data-m="${m.id}" aria-label="Больше">+</button></div><button class="add" data-a="add" data-m="${m.id}" data-k="${key(m.id,sel[m.id])}"><span class="al">Добавить</span></button></div>`};
const ctrl=(m,s)=>qbox(m);'''+HP[b:]
HP=_r(HP,' От ${minOf(m)} шт, шаг ${stepOf(m)} шт.','',"ct")
HP=_r(HP,'s.T&&pick(tiersOf(m),s.T)===x','s.T>=x.from&&pick(tiersOf(m),s.T)===x',"ison")
HP=_r(HP,'<button class="dot${i===sel[m.id]?" on":""}"','<button class="dot${i===sel[m.id]?" on":""}${c.na?" na":""}"',"na")
HP=_r(HP,'title="${c.n}"></button>','title="${c.n}${c.na?" — нет в наличии":""}"></button>',"natitle")
HP=_r(HP,'<div class="cn">Цвет: ${cs[sel[m.id]].n}</div>','<div class="cn">Цвет: ${cs[sel[m.id]].n}${cs[sel[m.id]].na?" · <b class=\\"nas\\">нет в наличии</b>":""}</div>',"cn")
_a=HP.index("const photo=");_b=HP.index("\n",_a)
HP=HP[:_a]+r'''const photo=m=>{const i=MODELS.indexOf(m),ea=i<8,im=`<img ${ea?(i<4?'fetchpriority="high"':''):'loading="lazy"'} decoding="async" width="420" height="420" src="${m.img}" alt="${m.name}, топпер на крышке стакана">`;
if(!(m.m3&&gl3)||m.custom)return im;const c=colorsOf(m)[sel[m.id]].c;return `<span class="pt">${im}<i class="tn" style="background:${c};-webkit-mask-image:url(${m.img});mask-image:url(${m.img})"></i></span>`};'''+HP[_b:]
common.HELPERS=HP
common.CART_MARKUP=r'''<div class="bar" id="bar"><button id="openCart" aria-label="Открыть корзину"><span class="cic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4h2.5l2 11h10l2-8H7"/><circle cx="9.5" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/></svg><span id="barL"></span></span></button></div>
<div class="ov" id="ov"><div class="sheet" role="dialog" aria-label="Корзина">
<h2>Ваш заказ <button class="x" id="close" aria-label="Закрыть">✕</button></h2>
<div id="list"></div>
<div class="leads" id="leads"></div>
<div class="tot"><span>Итого</span><span id="total"></span></div>
<label for="who">Как мы можем к вам обращаться</label><input id="who" autocomplete="name" placeholder="Имя">
<label for="cafe">Название кофейни</label><input id="cafe" autocomplete="organization">
<div id="customBox" hidden><label for="cdesc">Опишите, какую модель вы хотите заказать</label><textarea id="cdesc" rows="3" placeholder="Например: логотип нашей кофейни или персонаж по вашему рисунку"></textarea><p class="hint" style="text-align:left;margin-top:6px">Макет или фото отправите в WhatsApp сразу после заказа.</p></div>
<label for="note">Комментарий</label><textarea id="note" rows="2"></textarea>
<div id="warn"></div>
<a class="wa" id="wa" target="_blank" rel="noopener">Отправить заказ в WhatsApp</a>
<p class="hint">Откроется WhatsApp с готовым текстом заказа, останется нажать «Отправить».</p>
</div></div>'''
FONTS="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap"
CSS=r'''
/* Вариант D2: синяя рама, белый скруглённый лист, гигантский плотный заголовок, серые плитки товара, пилюли. Без чёрных заливок: синий для действий, белый для подложек, чёрный только в тексте. Анимации: появление шапки, плавающие кружки, появление карточек при прокрутке, мерцающий блюр на плитке своей модели. */
:root{--blue:#4358ef;--blue-d:#3346d8;--sky:#7d8cff;--ink:#0a0b14;--paper:#ffffff;--tile:#f2f3f9;--tile-2:#e4e6f4;--muted:#5b5f7b;--line:#e3e5f1;--f:"Inter Tight","Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--fb:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--ease:cubic-bezier(.2,.9,.25,1);color-scheme:light}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font:400 16px/1.5 var(--fb);padding-inline:16px;padding-block:16px 104px}
@media(min-width:760px){body{padding-inline:40px;padding-block:28px 112px}}
.shell{max-width:1200px;margin:0 auto}
button{font:inherit;color:inherit;cursor:pointer;border:0;transition:background-color .15s,color .15s,opacity .15s,scale .15s,translate .2s}
button:focus-visible,input:focus-visible,textarea:focus-visible,a:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
.bar button:focus-visible{outline-color:var(--ink);outline-offset:6px}
/* шапка */
.nav{display:flex;align-items:center;justify-content:space-between;gap:12px}
.logo{height:clamp(52px,12vw,76px);width:auto;display:block;border-radius:12px}
.pills{display:flex;gap:8px}
.pill{display:inline-flex;align-items:center;min-height:44px;padding:0 18px;border-radius:999px;background:var(--tile);color:var(--ink);font:600 14px var(--f);text-decoration:none;white-space:nowrap;transition:background-color .2s,translate .2s}
.pill{border:0;cursor:pointer}
.pill.on{background:var(--blue);color:#fff}.pill.on:hover{background:var(--blue-d)}
.mx{display:inline;margin-left:.3em}
.pill:hover{background:var(--tile-2);translate:0 -2px}
/* первый экран */
.hero{position:relative;--mega:clamp(56px,calc(15vw - 22px),166px);padding-top:clamp(28px,5vw,56px);display:grid;grid-template-columns:minmax(0,1fr) clamp(200px,28%,380px);column-gap:clamp(8px,2vw,24px)}
.hero-l{grid-column:1;grid-row:1;min-width:0}
.hand-w{grid-column:2;grid-row:1;position:relative;min-height:200px}
h1{margin:0;font-family:var(--f);font-weight:800;letter-spacing:-.05em;color:var(--ink)}
h1 .w1{display:block;white-space:nowrap;font-size:var(--mega);line-height:.84;margin-left:-.045em}
.lt{display:inline-block;animation:rise 1.1s var(--ease) both;animation-delay:calc(var(--i)*70ms + 80ms);transition:translate .35s cubic-bezier(.3,1.6,.5,1),rotate .35s cubic-bezier(.3,1.6,.5,1)}
@media(hover:hover){.lt:hover{translate:0 -.05em;rotate:-3deg}}
h1 .w2{display:block;color:var(--blue);font-size:clamp(26px,5.4vw,72px);line-height:1;letter-spacing:-.045em;margin-top:.2em;white-space:nowrap;animation:up .9s .55s var(--ease) both}
h1 .w2:empty{display:none}
.bub{position:absolute;right:0;top:calc(clamp(28px,5vw,56px) + var(--mega)*.6);display:flex;align-items:flex-start;pointer-events:none;--d:clamp(80px,13vw,180px)}
.bub i{display:block;width:var(--d);height:var(--d);margin-left:calc(var(--d)*-.26);animation:pop .9s cubic-bezier(.2,1.4,.3,1) both;animation-delay:calc(.5s + var(--k)*.14s)}
.bub i:first-child{margin-left:0;rotate:-8deg}
.bub i:nth-child(2){translate:0 32%;rotate:5deg}
.bub i:nth-child(3){translate:0 -6%;rotate:-3deg}
.bub b{display:block;width:100%;height:100%;border-radius:50%;border:clamp(4px,.55vw,8px) solid var(--paper);overflow:hidden;background:var(--tile);box-shadow:0 12px 32px rgba(10,11,20,.2);animation:fl 5.5s ease-in-out infinite alternate;animation-delay:calc(var(--k)*-1.7s)}
.bub img{width:100%;height:100%;object-fit:cover;display:block;scale:1.18}
.hero-foot{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:22px 32px;margin-top:clamp(28px,4vw,44px)}
#tag{margin:0;max-width:46ch;font-size:clamp(15px,1.6vw,18px);line-height:1.5;color:var(--muted);animation:up .9s .75s var(--ease) both}
.btns{display:flex;flex-wrap:wrap;gap:10px;animation:up .9s .9s var(--ease) both}
.btn{display:inline-flex;align-items:center;gap:10px;min-height:52px;padding:0 24px;border-radius:999px;font:600 15px var(--f);text-decoration:none;white-space:nowrap;transition:background-color .2s,translate .2s,scale .15s}
.btn svg{width:16px;height:16px;flex:none;transition:translate .25s}
.btn:hover{translate:0 -2px}.btn:active{scale:.97}
.btn:hover svg{translate:0 3px}
.btn.blue{background:var(--blue);color:#fff}.btn.blue:hover{background:var(--blue-d)}
.btn.line{border:1.5px solid var(--ink);color:var(--ink)}.btn.line:hover{background:var(--tile)}
.btn.white{background:#fff;color:var(--blue)}.btn.white:hover{background:#eef0ff}
/* каталог */
.cat{padding-top:clamp(40px,6vw,80px);scroll-margin-top:16px}
.cat-h{display:flex;flex-direction:column;gap:20px;margin-bottom:clamp(24px,4vw,40px)}
h2.big{margin:0;align-self:flex-start;font:800 clamp(30px,4.4vw,52px)/1 var(--f);letter-spacing:-.04em;color:var(--blue);border:2.5px solid var(--blue);border-radius:999px;padding:.16em .62em .22em}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{display:inline-flex;align-items:center;min-height:40px;padding:0 16px;border-radius:999px;border:1.5px solid var(--ink);font:500 14px var(--f);white-space:nowrap}
.chip.fill{background:var(--blue);border-color:var(--blue);color:#fff}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:44px 20px}
@media(min-width:1000px){.grid{grid-template-columns:repeat(4,minmax(0,1fr))}}
.item{display:flex;flex-direction:column;gap:14px;min-width:0;scroll-margin-top:16px}
.ph{position:relative;aspect-ratio:1/1;max-width:100%;border-radius:28px;overflow:hidden;background:var(--tile);isolation:isolate}
.ph img{width:100%;height:100%;object-fit:cover;display:block;transition:scale .8s var(--ease)}
@media(hover:hover){.item:hover .ph img{scale:1.07}}
/* цена-наклейка на фото */
.price{position:absolute;left:12px;bottom:12px;z-index:3;display:inline-flex;align-items:baseline;gap:3px;background:var(--paper);color:var(--ink);border-radius:999px;padding:8px 15px 9px;font:800 21px/1 var(--f);letter-spacing:-.035em;font-variant-numeric:tabular-nums;box-shadow:0 8px 22px rgba(10,11,20,.18);white-space:nowrap}
.price small{font:600 13px var(--fb);letter-spacing:0;color:var(--muted)}
.price.on{background:var(--blue);color:#fff}.price.on small{color:rgba(255,255,255,.85)}
.price.pop,#barR.pop{animation:popin .5s cubic-bezier(.2,1.4,.3,1)}
h3{margin:2px 0 0;font:700 24px/1.08 var(--f);letter-spacing:-.035em;min-width:0}
/* плитка своей модели: мерцающий блюр как в Telegram */
.ph.slot,.shot{background:linear-gradient(135deg,#4358ef,#7d8cff)}
.bls{position:absolute;inset:0;animation:hue 9s ease-in-out infinite alternate}
.bl{position:absolute;display:block;border-radius:50%;filter:blur(26px)}
.bl.b1{width:72%;height:72%;left:-12%;top:-12%;background:#b5beff;animation:d1 9s ease-in-out infinite alternate}
.bl.b2{width:60%;height:60%;right:-10%;top:8%;background:#f0537f;opacity:.75;animation:d2 11s ease-in-out infinite alternate}
.bl.b3{width:58%;height:58%;left:14%;bottom:-16%;background:#f58220;opacity:.7;animation:d3 13s ease-in-out infinite alternate}
.bl.b4{width:46%;height:46%;right:8%;bottom:4%;background:#ffffff;opacity:.55;animation:d1 10s ease-in-out infinite alternate-reverse}
canvas.spoil{position:absolute;inset:0;width:100%;height:100%;z-index:1}
.ph.slot .pl,.shot .pl{position:absolute;z-index:2;left:50%;top:50%;translate:-50% -50%;width:38%;aspect-ratio:1/1;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;background:rgba(255,255,255,.26);border:1.5px solid rgba(255,255,255,.6);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.ph.slot .pl svg,.shot .pl svg{width:52%;height:52%}
.slot .price{font-size:15px;font-weight:700;padding:8px 14px}
.desc{margin:0;font-size:14px;line-height:1.5;color:var(--muted)}
.cap{font-size:13px;color:var(--muted);margin-bottom:-6px}
.tiers{display:grid;grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:6px}
.tp{background:var(--tile);border-radius:16px;padding:9px 10px;display:flex;flex-direction:column;gap:1px}
.tp span{font-size:12px;color:var(--muted);white-space:nowrap}
.tp b{font:700 16px var(--f);letter-spacing:-.02em;font-variant-numeric:tabular-nums;white-space:nowrap}
.tp.on{background:var(--blue);color:#fff}.tp.on span{color:#fff;opacity:.88}
.sw{display:flex;flex-wrap:wrap;gap:8px}
.dot{width:28px;height:28px;border-radius:50%;background:var(--c);padding:0;position:relative;box-shadow:inset 0 0 0 1px rgba(10,11,20,.22);transition:scale .15s,box-shadow .15s}
.dot::after{content:"";position:absolute;inset:-6px}
.dot:hover{scale:1.15}.dot:active{scale:.9}
.dot.on{box-shadow:0 0 0 2px var(--paper),0 0 0 4px var(--ink)}
.cn{font-size:13px;color:var(--muted);margin-top:-4px}
.act{display:flex;flex-direction:column;gap:8px;margin-top:auto}
.add{height:52px;border-radius:999px;background:var(--blue);color:#fff;font:600 15px var(--f);padding:0 18px;white-space:nowrap}
.add:hover{background:var(--blue-d)}.add:active{scale:.97}
.qty{display:flex;align-items:center;justify-content:space-between;height:52px;border-radius:999px;background:var(--tile);padding:4px}
.qty button{width:44px;height:44px;border-radius:50%;background:var(--paper);font:600 20px var(--f);flex:none}
.qty button:hover{background:var(--blue);color:#fff}.qty button:active{scale:.88}
.qty span{font:600 15px var(--f);font-variant-numeric:tabular-nums;white-space:nowrap}
.sub{font-size:13px;color:var(--muted)}
.sub.warn{color:var(--blue);font-weight:600}
/* низ страницы */
.foot{position:relative;overflow:hidden;isolation:isolate;margin-top:clamp(56px,9vw,112px);background:var(--blue);color:#fff;border-radius:32px;padding:clamp(24px,5vw,56px)}
@media(min-width:760px){.foot{border-radius:36px}}
.foot .bl{filter:blur(48px)}
.bl.f1{width:62%;aspect-ratio:1/1;right:-12%;top:-40%;background:#9aa6ff;opacity:.85;animation:d1 12s ease-in-out infinite alternate}
.bl.f2{width:52%;aspect-ratio:1/1;left:-14%;bottom:-50%;background:#2a3bc4;opacity:.9;animation:d2 14s ease-in-out infinite alternate}
.bl.f3{width:36%;aspect-ratio:1/1;right:18%;bottom:-30%;background:#f0537f;opacity:.5;animation:d3 16s ease-in-out infinite alternate}
.foot-in{position:relative;z-index:1;display:flex;flex-direction:column;gap:28px}
.foot b{display:block;font:800 clamp(32px,7vw,88px)/.92 var(--f);letter-spacing:-.05em;max-width:12ch;text-wrap:balance}
.foot-r{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 24px}
.foot p{margin:0;max-width:38ch;color:rgba(255,255,255,.9);font-size:15px}
.foot .btn:hover svg{translate:2px -2px}
.foot .btn:focus-visible{outline-color:#fff}
/* корзина */
.bar{position:fixed;right:0;bottom:0;padding:0 16px calc(16px + env(safe-area-inset-bottom,0px));z-index:20;pointer-events:none}
.bar button{pointer-events:auto;display:flex;align-items:center;gap:8px;background:none;padding:0;border-radius:999px;font:600 16px var(--f);color:#fff}
.cic{position:relative;width:60px;height:60px;border-radius:50%;background:var(--blue);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 3px #fff,0 12px 30px rgba(34,46,160,.45);transition:background-color .15s,scale .15s}
.cic svg{width:26px;height:26px}
.bar button:hover .cic{background:var(--blue-d);scale:1.06}.bar button:active .cic{scale:.94}
#barR{display:none;background:#fff;color:var(--blue);border-radius:999px;padding:12px 18px;font:700 15px var(--f);white-space:nowrap;box-shadow:0 8px 24px rgba(34,46,160,.25),0 0 0 1px var(--line);font-variant-numeric:tabular-nums}
.bar.on #barR{display:inline-flex}
#barL{position:absolute;top:-6px;right:-6px;min-width:24px;height:24px;padding:0 6px;border-radius:12px;background:#fff;color:var(--blue);font:700 12px/24px var(--f);text-align:center;box-shadow:0 0 0 2px var(--blue)}
#barL:empty{display:none}
.empty{margin:14px 0 0;padding:18px;border-radius:20px;background:var(--tile);color:var(--muted);font-size:14px}
.addrow{display:flex;flex-direction:column;gap:8px}.addrow .add{min-width:0;padding:0 10px}.add.ok{background:#1fa463}.add.ok:hover,.add.ok:disabled{background:#1fa463;color:#fff}.qp::placeholder{color:#9096a8;opacity:1}.qp{width:54px}
.qw{display:inline-flex;align-items:center;gap:4px;flex:none}
.pre{background:var(--tile);border-radius:999px;height:52px;padding:0 14px}
.qn{width:46px;text-align:center;border:0;background:transparent;font:700 16px var(--f);padding:0;border-radius:8px;color:var(--ink);font-variant-numeric:tabular-nums}
.qn:focus{outline:2px solid var(--blue);outline-offset:2px;background:var(--paper)}
.qw span{font:600 13px var(--fb);color:var(--muted)}
.qty .qw{flex:1;justify-content:center}
.ov{position:fixed;inset:0;background:rgba(30,42,150,.58);-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px);display:none;z-index:30}
.ov.on{display:block;animation:fade .3s both}
.sheet{position:absolute;left:0;right:0;bottom:0;max-width:560px;margin:0 auto;max-height:92%;overflow:auto;background:var(--paper);color:var(--ink);border-radius:32px 32px 0 0;padding:22px 18px calc(22px + env(safe-area-inset-bottom,0px))}
.ov.on .sheet{animation:sheetUp .5s var(--ease) both}
@media(min-width:760px){.sheet{top:16px;right:16px;bottom:16px;left:auto;margin:0;width:480px;max-width:calc(100% - 32px);max-height:none;border-radius:36px;padding:28px}.ov.on .sheet{animation-name:sheetIn}}
.sheet h2{margin:0 0 10px;font:800 clamp(36px,7vw,46px)/1 var(--f);letter-spacing:-.05em;display:flex;justify-content:space-between;align-items:center}
.x{background:var(--tile);width:44px;height:44px;border-radius:50%;font-size:16px;letter-spacing:0}
.x:hover{background:var(--tile-2);rotate:90deg}
.row{display:grid;grid-template-columns:60px minmax(0,1fr) auto;gap:12px;align-items:center;padding:10px;border-radius:24px;background:var(--tile);margin-top:8px}
.rp{width:60px;height:60px;border-radius:16px;background:var(--paper);overflow:hidden;display:flex;align-items:center;justify-content:center;color:var(--blue)}
.rp img{width:100%;height:100%;object-fit:cover}.rp i{font-style:normal;font-size:28px;font-weight:800}
.row b{display:block;font:700 16px var(--f);letter-spacing:-.02em}.row small{color:var(--muted);font-size:13px}
.row .qty{height:auto;padding:3px;gap:2px;background:var(--paper)}
.row .qty button{width:34px;height:34px;font-size:17px;background:var(--tile)}
.row .qty button:hover{background:var(--blue);color:#fff}
.row .qty span{min-width:48px;text-align:center;font-size:14px}
.mini{display:inline-block;width:11px;height:11px;border-radius:50%;background:var(--c);box-shadow:inset 0 0 0 1px rgba(10,11,20,.3);margin-right:5px;vertical-align:-1px}
.leads{margin-top:12px;font-size:14px;line-height:1.6;color:var(--muted);padding:14px 16px;border-radius:20px;border:1.5px solid var(--line)}
.leads:empty{display:none}.leads b{color:var(--ink)}
.tot{display:flex;justify-content:space-between;align-items:baseline;gap:12px;font:800 32px var(--f);letter-spacing:-.045em;padding-block:20px 4px;font-variant-numeric:tabular-nums}
.tot span:first-child{font:600 15px var(--fb);letter-spacing:0;color:var(--muted)}
label{display:block;font:600 14px var(--fb);margin:14px 0 6px}
input,textarea{width:100%;font:inherit;font-size:16px;padding:14px 16px;border-radius:18px;border:2px solid transparent;background:var(--tile);color:var(--ink);transition:border-color .2s,background-color .2s}
input:focus,textarea:focus{border-color:var(--blue);outline:none;background:var(--paper)}
#warn{color:var(--blue);font-weight:600;font-size:13px;margin-top:8px}
.wa{display:flex;align-items:center;justify-content:center;min-height:60px;margin-top:16px;background:var(--blue);color:#fff;text-decoration:none;font:700 17px var(--f);border-radius:999px;transition:background-color .2s,scale .15s,opacity .2s}
.wa:hover{background:var(--blue-d)}.wa:active{scale:.98}
.wa.off{opacity:.35;pointer-events:none}
.hint{font-size:12px;color:var(--muted);margin:10px 0 0;text-align:center}
/* анимации */
/* вторая страница */
.why-hero{--mega:clamp(56px,18vw,250px);padding-top:clamp(28px,5vw,56px)}
.wh{margin:0;font-family:var(--f);font-weight:800;letter-spacing:-.05em}
.wh .w1{display:block;font-size:var(--mega);line-height:.84;margin-left:-.045em}
.wh .w2{display:block;color:var(--blue);font-size:clamp(26px,5.4vw,72px);line-height:1;letter-spacing:-.045em;margin-top:.2em;text-wrap:balance}
.why-lead{margin:clamp(20px,3vw,32px) 0 0;max-width:52ch;font-size:clamp(16px,1.7vw,19px);color:var(--muted)}
.why-sec{padding-top:clamp(48px,8vw,96px)}
h2.sec{margin:0 0 clamp(20px,3vw,32px);font:800 clamp(34px,6vw,76px)/.92 var(--f);letter-spacing:-.05em;text-wrap:balance}
.adv-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.adv{display:flex;flex-direction:column;gap:12px;padding:26px;border-radius:30px;background:var(--tile);min-height:230px;min-width:0}
.adv h3{margin:auto 0 0;font-size:26px}
.adv p{margin:0;color:var(--muted);font-size:15px;line-height:1.5}
.adv .ic{width:52px;height:52px;border-radius:50%;background:var(--paper);color:var(--blue);display:flex;align-items:center;justify-content:center}
.adv .ic svg{width:26px;height:26px}
.adv.blue{background:var(--blue);color:#fff}.adv.blue p{color:rgba(255,255,255,.88)}.adv.blue .ic{background:rgba(255,255,255,.2);color:#fff}
.shots{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.shot img{width:100%;height:100%;object-fit:cover;object-position:50% 20%;display:block;transition:scale .8s var(--ease)}
@media(hover:hover){.shot:hover img{scale:1.06}}
.shot{position:relative;aspect-ratio:4/5;border-radius:28px;overflow:hidden;isolation:isolate;margin:0}
/* график роста */
.growth{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(16px,3vw,40px);align-items:center}
.why-lead2{margin:0;font-size:clamp(16px,1.6vw,18px);color:var(--muted);max-width:44ch}
.g-steps{list-style:none;margin:20px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px;counter-reset:s}
.g-steps li{counter-increment:s;display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 16px 0 6px;border-radius:999px;border:1.5px solid var(--ink);font:500 14px var(--f)}
.g-steps li::before{content:counter(s);width:28px;height:28px;border-radius:50%;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font:700 13px var(--f)}
.g-note{margin:18px 0 0;font-size:13px;color:var(--muted)}
.g-chart{background:var(--tile);border-radius:30px;padding:clamp(16px,2.6vw,28px)}
.legend{display:flex;flex-wrap:wrap;gap:8px 20px;margin-bottom:8px;font:600 14px var(--f)}
.legend span{display:inline-flex;align-items:center;gap:8px}
.lg{width:22px;height:5px;border-radius:3px;background:#9aa0bd}.lg.on{background:var(--blue)}
.gsvg{display:block;width:100%;height:auto;overflow:visible}
.gl line{stroke:var(--tile-2);stroke-width:2}.gx text{font:500 22px var(--fb);fill:var(--muted)}
.mk{stroke:var(--muted);stroke-width:2;stroke-dasharray:6 6}.mt{font:600 22px var(--f);fill:var(--ink)}
.ar{fill:var(--blue);opacity:.1}
.ln0{fill:none;stroke:#9aa0bd;stroke-width:5;stroke-linecap:round}
.ln1{fill:none;stroke:var(--blue);stroke-width:7;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:0}
.dt{fill:var(--blue);stroke:#fff;stroke-width:5}
.growth .ln1{animation:draw 1.8s .3s var(--ease) both}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
.calc-grid{display:none}
.calc-in,.calc-out{background:var(--tile);border-radius:30px;padding:clamp(20px,3vw,32px)}
.calc-in label:first-child{margin-top:0}
.calc-in input{background:var(--paper);font:700 20px var(--f);letter-spacing:-.02em}
.hint2{margin:16px 0 0;font-size:13px;line-height:1.5;color:var(--muted)}.hint2 b{color:var(--ink)}
.bars{display:grid;grid-template-columns:1fr 1fr;gap:16px;height:240px}
.bc{display:flex;flex-direction:column;min-width:0}
.bw{flex:1;display:flex;align-items:flex-end}
.bar1{width:100%;height:50%;min-height:4px;border-radius:20px 20px 8px 8px;background:var(--tile-2);transition:height .7s var(--ease)}
.bar1.on{background:var(--blue)}
.bv{margin-top:10px;font:800 clamp(18px,2.2vw,26px)/1 var(--f);letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.cap2{font-size:13px;color:var(--muted);margin-top:4px}
.kpi{margin:20px 0 0;display:grid;gap:8px}
.kpi div{display:flex;justify-content:space-between;align-items:baseline;gap:12px;background:var(--paper);border-radius:18px;padding:12px 16px}
.kpi dt{font-size:14px;color:var(--muted)}.kpi dd{margin:0;font:700 18px var(--f);letter-spacing:-.02em;font-variant-numeric:tabular-nums;white-space:nowrap}
.kpi .net{background:var(--blue)}.kpi .net dt{color:rgba(255,255,255,.9)}.kpi .net dd{color:#fff;font-size:22px}
.why-cta{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;margin-top:clamp(48px,8vw,96px)}
.why-cta p{margin:0;font:800 clamp(26px,4vw,48px)/1 var(--f);letter-spacing:-.045em;max-width:16ch}
/* рука со стаканом */
.hand{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;object-position:right center;pointer-events:none;animation:handIn 1.1s .45s var(--ease) both,bob 5s 1.6s ease-in-out infinite}
@keyframes bob{0%,100%{translate:0 0}50%{translate:0 -8px}}
@keyframes handIn{from{translate:0 40px;rotate:5deg}to{translate:0 0;rotate:0deg}}
@keyframes rise{from{transform:translateY(.2em) rotate(7deg)}to{transform:none}}
@keyframes up{from{translate:0 24px}to{translate:0 0}}
@keyframes pop{from{scale:.2}to{scale:1}}
@keyframes fl{from{translate:0 -6px}to{translate:0 8px}}
@keyframes popin{0%{scale:.75}60%{scale:1.14}100%{scale:1}}
@keyframes barIn{from{translate:0 150%}to{translate:0 0}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes sheetUp{from{translate:0 100%}to{translate:0 0}}
@keyframes sheetIn{from{translate:110% 0}to{translate:0 0}}
@keyframes d1{0%{translate:-8% -6%;scale:1}50%{translate:26% 16%;scale:1.25}100%{translate:10% 38%;scale:.9}}
@keyframes d2{0%{translate:6% 10%;scale:1}50%{translate:-30% 30%;scale:1.2}100%{translate:-12% -14%;scale:.85}}
@keyframes d3{0%{translate:-10% 8%;scale:.9}50%{translate:30% -22%;scale:1.2}100%{translate:-22% -30%;scale:1}}
@keyframes hue{from{filter:hue-rotate(-22deg)}to{filter:hue-rotate(26deg)}}
@keyframes rv{from{translate:0 28px;scale:.985}to{translate:0 0;scale:1}}
@supports (animation-timeline:view()){.item,h2.big,.chips,.adv,.shot,.g-chart{animation:rv linear both;animation-timeline:view();animation-range:entry 0% entry 45%}}
/* телефон: правила в конце, чтобы перекрыть остальные */
@media(max-width:759px){.bub{position:static;margin-top:18px;padding-bottom:34px;--d:clamp(72px,18vw,120px)}
.adv-grid,.calc-grid{grid-template-columns:minmax(0,1fr)}
.shots{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.growth{grid-template-columns:minmax(0,1fr)}
.adv{min-height:0}.adv h3{margin-top:8px;font-size:22px}}
@media(max-width:519px){.pill.opt{display:none}
h1 .w2{font-size:24px}
.bub{--d:68px}
.btns{width:100%}.btn{flex:1 1 100%;justify-content:center}
.row{grid-template-columns:52px minmax(0,1fr);row-gap:6px}.rp{width:52px;height:52px;grid-row:1/3}.row .ctl{grid-column:2;justify-self:start}}
@media(max-width:559px){.grid{gap:32px 12px}
.item{gap:10px}.ph{border-radius:22px}
.price{left:8px;bottom:8px;padding:6px 11px 7px;font-size:16px}.price small{font-size:11px}.slot .price{font-size:12px;padding:6px 11px}
h3{font-size:19px}
.cap{font-size:12px;margin-bottom:-2px}
.tiers{grid-template-columns:1fr;gap:4px}.tp{flex-direction:row;justify-content:space-between;align-items:baseline;padding:7px 11px;border-radius:13px}.tp b{font-size:15px}
.sw{display:grid;grid-template-columns:repeat(3,28px);gap:8px 14px}
.cn{font-size:12px}
.add{height:46px;font-size:14px;padding:0 8px}
.qty{height:46px;padding:3px}.qty button{width:38px;height:38px}.qty span{font-size:14px}
.desc{font-size:13px}.sub{font-size:12px}
.ph.slot .pl{width:44%}}
/* телефон: компактный масштаб, ближе к компьютерной версии */
@media(max-width:759px){
.hero{display:block}.hand-w{float:right;width:clamp(112px,34vw,142px);aspect-ratio:420/520;min-height:0;margin:0 0 6px 8px}.hero-foot{display:block;margin-top:8px}
body{font-size:14px;padding-block:12px 88px}
.nav{flex-wrap:nowrap;gap:8px}
.logo{height:clamp(36px,10.5vw,44px);border-radius:9px}
.pills{gap:6px;flex:none}.pill{min-height:34px;padding:0 12px;font-size:13px}
.hero,.why-hero{padding-top:22px}.why-hero{--mega:clamp(44px,13.5vw,64px)}.hero{--mega:clamp(40px,11.8vw,56px)}
h1 .w2{font-size:clamp(16px,4.9vw,20px);margin-top:.35em}
.wh .w2{font-size:clamp(18px,5.6vw,24px);margin-top:.35em}
.bub{--d:clamp(52px,14vw,64px);margin-top:12px;padding-bottom:22px}
.bub b{border-width:3px}
#tag,.why-lead{font-size:13.5px;line-height:1.5;margin-top:0}.why-lead{margin-top:14px}#tag{font-size:12px;line-height:1.45;opacity:.85}
.hero-foot{margin-top:6px}
.cat{padding-top:36px}.cat-h{gap:12px;margin-bottom:18px}
h2.big{font-size:clamp(26px,7.6vw,32px);border-width:2px}
.chip{min-height:32px;padding:0 12px;font-size:12.5px}
.grid{gap:26px 10px}
.item{gap:8px}.ph{border-radius:18px}
.price{left:6px;bottom:6px;padding:5px 9px 6px;font-size:14px}.price small{font-size:10px}.slot .price{font-size:11px;padding:5px 9px}
h3{font-size:16px;margin-top:0}
.cap{font-size:11px;margin-bottom:-2px}
.tp{padding:6px 10px;border-radius:11px}.tp span{font-size:11px}.tp b{font-size:13.5px}
.sw{grid-template-columns:repeat(3,24px);gap:7px 12px}.dot{width:24px;height:24px}.dot::after{inset:-5px}
.cn{font-size:11px;margin-top:-2px}
.add{height:40px;font-size:12.5px}.qty{height:40px}.qty button{width:32px;height:32px;font-size:17px}.qty span{font-size:12.5px}
.desc{font-size:12px}.sub{font-size:11px}
.ph.slot .pl{width:40%}
.foot{margin-top:40px;padding:22px;border-radius:24px}.foot b{font-size:clamp(26px,8vw,34px)}.foot p{font-size:13px}
.foot-r{gap:14px}.btn{min-height:44px;padding:0 18px;font-size:13.5px}
/* вторая страница */
.why-sec{padding-top:36px}
h2.sec{font-size:clamp(26px,7.4vw,32px);margin-bottom:14px}
.adv-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.adv{padding:14px;gap:8px;border-radius:20px;min-height:0}
.adv .ic{width:34px;height:34px}.adv .ic svg{width:18px;height:18px}
.adv h3{font-size:15px;margin-top:6px}.adv p{font-size:12px;line-height:1.45}
.shots{gap:10px}.shot{border-radius:18px}
.g-chart{border-radius:20px;padding:14px}.legend{font-size:12px;gap:6px 14px}
.why-lead2{font-size:13.5px}.g-steps li{min-height:34px;font-size:12.5px;padding:0 12px 0 5px}.g-steps li::before{width:24px;height:24px;font-size:12px}
.g-note{font-size:11.5px}
.why-cta{margin-top:36px}.why-cta p{font-size:24px}
/* корзина */
.bar{padding:0 14px calc(12px + env(safe-area-inset-bottom,0px))}.cic{width:54px;height:54px}.cic svg{width:24px;height:24px}#barR{padding:10px 15px;font-size:14px}
.pre{height:40px;padding:0 9px}.qn{width:40px}.qw span{font-size:11.5px}.addrow{gap:5px}.addrow .add{padding:0 6px}
.sheet{padding:18px 16px calc(18px + env(safe-area-inset-bottom,0px));border-radius:26px 26px 0 0}
.sheet h2{font-size:30px}.x{width:38px;height:38px}
.row{padding:8px;border-radius:18px;margin-top:6px}.row b{font-size:14px}.row small{font-size:12px}
.tot{font-size:26px}.leads{font-size:12.5px;padding:10px 12px}
label{font-size:13px;margin:10px 0 5px}input,textarea{padding:11px 13px;font-size:15px;border-radius:14px}
.wa{min-height:50px;font-size:15px;margin-top:12px}.hint{font-size:11px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}html{scroll-behavior:auto}}
input,textarea,.qn{font-size:16px}
html,body,button,a,input,textarea,.qty,.qty *,.pill,.add{touch-action:manipulation}
button{-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent}
.qn{-webkit-user-select:text;user-select:text}

.shell{overflow-x:clip}
.hero{min-height:clamp(300px,36vw,500px)}
.hero-l{position:relative;z-index:1}
.hand-w{grid-column:auto;grid-row:auto;position:absolute;z-index:0;right:-1%;top:-2%;height:min(150%,600px);width:auto;aspect-ratio:420/520;min-height:0;rotate:11deg;transform-origin:55% 60%;pointer-events:none}
.hand{translate:0 0}
.hand.bk{filter:blur(7px);opacity:.6;-webkit-mask-image:linear-gradient(to right,#000 0,#000 16%,transparent 42%);mask-image:linear-gradient(to right,#000 0,#000 16%,transparent 42%)}
.hand.fr{-webkit-mask-image:linear-gradient(to right,transparent 6%,#000 30%);mask-image:linear-gradient(to right,transparent 6%,#000 30%)}
.hand{object-position:right center}
.row .ctl{display:flex;align-items:center;gap:6px}
.del{width:40px;height:40px;border-radius:50%;background:#fdeaec;color:#e4121e;display:inline-flex;align-items:center;justify-content:center;flex:none;transition:background-color .15s,color .15s,scale .15s}
.del svg{width:20px;height:20px}
.del:hover{background:#e4121e;color:#fff}.del:active{scale:.92}
@media(max-width:759px){
.hero{display:block;min-height:clamp(250px,74vw,330px)}
.hand-w{float:none;margin:0;right:-5vw;top:2px;width:58vw;height:auto;min-height:0}
.hero-foot{margin-top:6px}#tag{max-width:46vw}
.del{width:36px;height:36px}.del svg{width:18px;height:18px}
}

/* текст растянут по высоте стакана */
.hero{--pt:clamp(24px,3.6vw,48px);padding-top:var(--pt);padding-bottom:0;min-height:0;height:clamp(340px,30.5vw,450px);align-items:stretch}
.hero-l{display:flex;flex-direction:column;justify-content:space-between;height:100%}
.hero-foot{margin-top:24px}
.hand-w{top:calc(var(--pt) - 3%);height:104%;right:1%}
.cat{padding-top:clamp(22px,3vw,40px)}
@media(max-width:759px){
.hero{--pt:16px;display:block;height:auto;min-height:0}
.hero-l{height:auto;display:block}
.hand-w{top:6px;height:auto;width:56vw;right:-5vw}
.hero-foot{margin-top:6px}
.cat{padding-top:22px}
}

.v3{position:relative;isolation:isolate;background:linear-gradient(140deg,#d6d9df 0,#c6c9d1 55%,#b6b9c3 100%)}
.v3 .bls{animation:none}
.v3 .bl{filter:blur(24px)}
.v3 .bl.b1{background:#e2e4ea;opacity:.7}.v3 .bl.b2{background:#9296a2;opacity:.45}.v3 .bl.b3{background:#c8cbd3;opacity:.5}.v3 .bl.b4{background:#f0f1f5;opacity:.45}
.v3 canvas.spoil{z-index:0;opacity:.55}
.v3::after{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;opacity:.16;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n' x='0' y='0' width='100%25' height='100%25'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .5 0 0 0 0 .5 0 0 0 1.1 -.1'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");background-size:180px 180px}
.sw{padding:4px 4px 4px 5px}
.cv3{position:absolute;inset:0;width:100%;height:100%;display:block;z-index:1;touch-action:pan-y;cursor:grab;-webkit-user-select:none;user-select:none}
.cv3:active{cursor:grabbing}
.ph.v3 .price{z-index:3;pointer-events:none}
.b3d{position:absolute;z-index:3;top:10px;right:10px;display:inline-flex;align-items:center;gap:5px;padding:7px 11px 7px 9px;border-radius:999px;background:#fff;color:var(--blue);font:700 12px/1 var(--f);letter-spacing:.03em;box-shadow:0 4px 14px rgba(34,46,160,.22);transition:scale .15s,background-color .15s,color .15s}
.b3d svg{width:14px;height:14px}
.b3d:hover{background:var(--blue);color:#fff}.b3d:active{scale:.94}
.m3{position:fixed;inset:0;z-index:80;background:rgba(18,26,94,.5);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);display:flex;align-items:center;justify-content:center;padding:12px;overflow:auto}
.m3[hidden]{display:none}
html.mo{background:#6b72b2}html.mo body{background:transparent}html.mo .shell,html.mo .bar{visibility:hidden}html.mo .m3{background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none}
.m3b{width:min(100%,calc(100vh - 260px),720px);background:var(--paper);border-radius:28px;padding:14px 14px 16px;box-shadow:0 30px 80px rgba(10,16,70,.4);animation:m3in .35s var(--ease) both}
@keyframes m3in{from{opacity:0;scale:.92;translate:0 16px}}
.m3h{display:flex;align-items:center;justify-content:space-between;padding:2px 4px 12px}.m3h b{font:800 22px var(--f);letter-spacing:-.03em}
.m3x{width:40px;height:40px;border-radius:50%;background:var(--tile);font-size:16px;flex:none}.m3x:hover{background:var(--blue);color:#fff}
.m3c{position:relative;aspect-ratio:1/1;border-radius:22px;overflow:hidden;}
.cv3.big{touch-action:none}
.m3q{margin-top:12px}.m3q .addrow{flex-direction:row;flex-wrap:wrap}.m3q .addrow .qty{flex:1 1 150px}.m3q .addrow .add{flex:1.5 1 160px}.m3q .sub{margin-top:8px;text-align:center}.m3f{padding:12px 4px 0}.m3f .cn{margin-top:8px}.m3f p{margin:10px 0 0;font-size:12.5px;color:var(--muted)}
@media(max-width:759px){.m3b{border-radius:22px;padding:10px 10px 14px}.m3h b{font-size:18px}.b3d{top:8px;right:8px;padding:6px 9px 6px 8px;font-size:11px}}

.tg{position:absolute;z-index:3;top:10px;left:10px;display:inline-flex;align-items:center;gap:5px;padding:6px 12px 6px 9px;border-radius:999px;background:rgba(255,255,255,.9);color:var(--ink);font:700 12px/1 var(--f);box-shadow:0 4px 14px rgba(10,16,70,.22);pointer-events:none;white-space:nowrap}
.tg i{font-style:normal;font-size:14px;line-height:1}
.tg.hit{background:var(--blue);color:#fff}
@media(max-width:759px){
.tg{top:8px;left:8px;gap:3px;padding:5px 9px 5px 7px;font-size:10.5px}.tg i{font-size:12px}
.b3d{top:8px;right:8px;padding:5px 8px 5px 7px;font-size:10px;gap:3px}.b3d svg{width:12px;height:12px}
}

.tg{top:10px;left:10px;gap:4px;padding:4px 8px 4px 6px;border-radius:8px;background:rgba(255,255,255,.88);font:700 11px/1.15 var(--f);letter-spacing:.01em;box-shadow:0 2px 8px rgba(10,16,70,.2);}
.tg i{font-size:12px}
.b3d{top:10px;right:10px;gap:4px;padding:4px 8px 4px 6px;border-radius:8px;font-size:11px;line-height:1.15;box-shadow:0 2px 8px rgba(10,16,70,.2)}
.b3d svg{width:12px;height:12px}
.sw{display:grid;grid-template-columns:repeat(5,28px);gap:10px 14px}
.dot.na::before{content:"";position:absolute;left:-3px;right:-3px;top:50%;height:2px;background:#fff;box-shadow:0 0 0 1px rgba(10,11,20,.5);transform:rotate(-45deg);border-radius:2px;z-index:1}
.dot.na{opacity:.6}.dot.na.on{opacity:1}
.nas{color:#d4263b;font-weight:600}
.add:disabled{background:var(--tile);color:#9096a8;cursor:not-allowed}.add:disabled:hover{background:var(--tile)}.add:disabled:active{scale:1}
@media(max-width:759px){
.tg{top:7px;left:7px;gap:3px;padding:3px 6px 3px 5px;border-radius:7px;font-size:9.5px}.tg i{font-size:10.5px}
.b3d{top:7px;right:7px;gap:3px;padding:3px 6px 3px 5px;border-radius:7px;font-size:9.5px}.b3d svg{width:10px;height:10px}
.sw{grid-template-columns:repeat(5,23px);gap:8px 8px}.dot{width:23px;height:23px}
}

.tg{padding:0;width:26px;height:26px;justify-content:center;border-radius:8px}.tg i{font-size:14px}
@media(max-width:759px){.tg{width:22px;height:22px;padding:0;border-radius:7px}.tg i{font-size:12px}}
.bls.off,.bls.off .bl{animation-play-state:paused}
.v3 .bls .bl{will-change:auto}

.ph.slot .shd{position:absolute;z-index:1;left:50%;top:46%;width:42%;height:auto;translate:-50% -50%;rotate:-7deg;fill:#14197a;opacity:.34;filter:blur(3px);pointer-events:none}
#custom .act{margin-top:0}
@media(max-width:759px){.ph.slot .shd{width:48%}}

.ph.v3{background:radial-gradient(closest-side at 50% 54%,#e6e8ee 0,rgba(230,232,238,.75) 52%,rgba(230,232,238,0) 100%);border-radius:0;overflow:visible}
.ph.v3::after{display:none}
.ph.v3 .b3d{top:6px;right:6px;gap:5px;padding:7px 12px 7px 9px;border-radius:12px;font-size:13px;box-shadow:0 0 0 1px rgba(10,16,70,.07),0 1px 3px rgba(10,16,70,.14)}
.ph.v3 .b3d svg{width:15px;height:15px}
.ph.v3 .price{left:4px;bottom:4px;box-shadow:0 0 0 1px rgba(10,11,20,.07),0 1px 3px rgba(10,11,20,.12)}
@media(max-width:759px){
.ph.v3 .b3d{top:4px;right:4px;gap:4px;padding:6px 10px 6px 8px;border-radius:11px;font-size:12px}.ph.v3 .b3d svg{width:13px;height:13px}
.ph.v3 .price{left:2px;bottom:2px;box-shadow:0 0 0 1px rgba(10,11,20,.08)}
}

.tp{padding:6px 10px;border-radius:13px}.tp span{font-size:11.5px}.tp b{font-size:15px}.tiers{gap:5px}
@media(max-width:759px){
.tiers{grid-template-columns:repeat(var(--n),minmax(0,1fr));gap:4px}
.tp{flex-direction:column;justify-content:flex-start;align-items:flex-start;gap:0;padding:4px 7px 5px;border-radius:10px}
.tp span{font-size:9.5px;line-height:1.25}.tp b{font-size:12.5px;line-height:1.2;letter-spacing:-.03em}
.cap{font-size:10.5px;margin-bottom:-4px}
}

@media(max-width:759px){
.tp{flex-direction:row;align-items:baseline;justify-content:center;gap:4px;padding:4px 4px 5px;border-radius:9px}
.tp span{font-size:9.5px}.tp b{font-size:12px}
.cap{font-size:10px;margin-bottom:-5px}
}

.tp b i{font-style:normal}
@media(max-width:759px){
.tp b i{display:none}
.tp{padding:4px 2px 5px;gap:3px;white-space:nowrap}.tp span{font-size:9.5px}.tp b{font-size:12.5px}
}
.foot-b{display:flex;flex-wrap:wrap;gap:10px}
.btn.ghost{border:1.5px solid rgba(255,255,255,.75);color:#fff}.btn.ghost:hover{background:rgba(255,255,255,.16)}
.btn.ghost svg{width:18px;height:18px}.btn.ghost:hover svg{translate:0 0;scale:1.1}
@media(max-width:759px){.foot-b{width:100%}.foot-b .btn{flex:1 1 100%;justify-content:center}}

.cv3.hid{visibility:hidden}
.ph .cv3{opacity:0;transition:opacity .45s}
.ph.ready .cv3{opacity:1}
.ph.v3 img{scale:1!important}
.pt{position:absolute;inset:0;display:block}
.pt img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.pt .tn{position:absolute;inset:0;mix-blend-mode:multiply;-webkit-mask-size:cover;mask-size:cover;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;-webkit-mask-position:center;mask-position:center}
.ph.v3.ready .pt{opacity:0;visibility:hidden;transition:opacity 0s linear .6s,visibility 0s linear .6s}
.ph .cv3.live{opacity:1;transition:none}
.shell>*:not(.nav){transition:opacity .6s ease}
html.boot .shell>*:not(.nav){opacity:0}
html.boot .shell>*:not(.nav) *,html.boot .shell>*:not(.nav) *::before,html.boot .shell>*:not(.nav) *::after{animation-play-state:paused!important}
.item{content-visibility:auto;contain-intrinsic-size:auto 600px}
'''
ARROW='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2v11M3 8.5 8 13.5l5-5"/></svg>'
ARROW_UR='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 12.5l9-9M5 3.5h7.5V11"/></svg>'
IC=lambda p:'<span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+p+'</svg></span>'
BLOBS='<div class="bls"><i class="bl b1"></i><i class="bl b2"></i><i class="bl b3"></i><i class="bl b4"></i></div><canvas class="spoil"></canvas>'
CAM='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg>'
def ADV(cls,ic,h,p): return f'<article class="adv {cls}">{IC(ic)}<h3>{h}</h3><p>{p}</p></article>'
import base64
HAND='data:image/webp;base64,'+base64.b64encode(open('/home/claude/v/hand_m.webp','rb').read()).decode()
REFS=['data:image/jpeg;base64,'+base64.b64encode(open(f'/home/claude/v/ref{i}.jpg','rb').read()).decode() for i in range(4)]
def _sm(pts):
    d=f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for k in range(len(pts)-1):
        p0=pts[max(k-1,0)];p1=pts[k];p2=pts[k+1];p3=pts[min(k+2,len(pts)-1)]
        c1=(p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6);c2=(p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6)
        d+=f' C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d
_X=lambda i:40+i*108
_Y=lambda v:290-(v-90)*3.857
_with=[(_X(i),_Y(v)) for i,v in enumerate([100,100,106,118,134,152])]
_wo=[(_X(i),_Y(v)) for i,v in enumerate([100,100,100,101,101,102])]
_pw=_sm(_with);_pn=_sm(_wo)
_grid=''.join(f'<line x1="40" x2="580" y1="{y}" y2="{y}"/>' for y in (20,87.5,155,222.5,290))
_xl=''.join(f'<text x="{_X(i)}" y="326" text-anchor="middle">Мес. {i+1}</text>' for i in range(6))
CHART=('<svg class="gsvg" viewBox="0 0 600 340" role="img" aria-label="Условный график: продажи с топперами растут быстрее, чем без них">'
 f'<g class="gl">{_grid}</g><g class="gx">{_xl}</g>'
 f'<line class="mk" x1="{_X(1)}" x2="{_X(1)}" y1="20" y2="290"/><text class="mt" x="{_X(1)+10}" y="44">Появились топперы</text>'
 f'<path class="ar" d="{_pw} L{_X(5)},290 L{_X(0)},290 Z"/>'
 f'<path class="ln0" d="{_pn}"/><path class="ln1" pathLength="1" d="{_pw}"/>'
 f'<circle class="dt" cx="{_with[-1][0]}" cy="{_with[-1][1]:.1f}" r="9"/></svg>')
WHY='<div data-page="why" hidden>'+\
'<section class="why-hero"><h2 class="wh"><span class="w1">Зачем</span><span class="w2">нужны топперы в кофейне</span></h2><p class="why-lead">Топпер делает стакан заметным: гость видит ваш бренд у себя в руках, а не только на вывеске.</p></section>'+\
'<section class="why-sec"><div class="adv-grid">'+\
ADV('blue','<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>','Стакан запоминается','Фигурка на крышке отличает ваш кофе от десятков одинаковых стаканов на улице и в офисе.')+\
ADV('','<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>','Повод для фото','Милую фигурку хочется снять. Гости сами показывают ваш кофе в историях и чатах.')+\
ADV('','<path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3M18 3v4h-4M6 21v-4h4"/>','Причина вернуться','Моделей несколько, их можно собрать в серию. Гость заходит снова за новой.')+\
ADV('','<rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/>','Сезон и акции','Тыква к Хэллоуину, сердечко к 14 февраля. Меняйте модели под праздники и акции.')+\
ADV('','<path d="M12 3l2.5 5.5L20 9l-4 4 1 6-5-3-5 3 1-6-4-4 5.5-.5z"/>','Ваш логотип','Напечатаем вашего персонажа или логотип по макету. Тираж от 100 шт.')+\
ADV('','<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>','Недорого','<span id="advPrice"></span>')+\
'</div></section>'+\
'<section class="why-sec"><h2 class="sec">Как это выглядит в кофейнях</h2><div class="shots">'+''.join(f'<figure class="shot"><img src="{d}" alt="Топпер на крышке стакана"></figure>' for d in REFS)+'</div></section>'+\
'<section class="why-sec"><div class="growth"><div class="g-text"><h2 class="sec">Рост продаж</h2><p class="why-lead2">Стакан с топпером замечают, им делятся, за ним возвращаются. Так со временем растут продажи кофейни.</p><ol class="g-steps"><li>Гость заметил</li><li>Сфотографировал</li><li>Вернулся за новой</li></ol><p class="g-note">График условный, для наглядности. Это не гарантия результата.</p></div><div class="g-chart"><div class="legend"><span><i class="lg on"></i>С топперами</span><span><i class="lg"></i>Без топперов</span></div>'+CHART+'</div></div></section>'+\
'<div class="why-cta"><p>Выберите модели для своей кофейни</p><button class="btn blue" data-tab="catalog">Открыть каталог</button></div>'+\
'</div>'
BODY=f'''<div class="shell">
<header class="nav"><img class="logo" src="{LOGO}" alt="Студия брендирования Разгуляев"><nav class="pills" aria-label="Страницы"><button class="pill on" data-tab="catalog">Каталог</button><button class="pill" data-tab="why">Зачем <span class="mx">нужны</span></button><button class="pill opt" data-go="custom">Своя модель</button></nav></header>
<div data-page="catalog"><section class="hero"><div class="hand-w" aria-hidden="true">{ILL.replace("<svg ","<svg class=\"hand bk\" ",1).replace('role="img" aria-label="Стакан кофе с тремя милыми топперами на крышке"',"")}{ILL.replace("<svg ","<svg class=\"hand fr\" ",1)}</div><div class="hero-l"><h1 id="brand"></h1>
<div class="hero-foot"><p id="tag"></p></div></div></section>
<section class="cat" id="catalog"><div class="cat-h"><h2 class="big">Каталог</h2></div><main class="grid" id="grid"></main></section></div>
{WHY}
<footer class="foot"><i class="bl f1"></i><i class="bl f2"></i><i class="bl f3"></i><div class="foot-in"><b>Студия брендирования Разгуляев</b><div class="foot-r"><p>Заказы принимаем в WhatsApp. Корзина соберёт выбор в готовое сообщение.</p><div class="foot-b"><a class="btn white" href="https://wa.me/77064230226" target="_blank" rel="noopener">Написать в WhatsApp {ARROW_UR}</a><a class="btn ghost" href="https://instagram.com/raz.brandstudio" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>raz.brandstudio</a></div></div></div></footer>
</div>'''
CARD=r'''let gl3=false;try{const c=document.createElement("canvas");gl3=!!(c.getContext("webgl2")||c.getContext("webgl"))}catch(e){}
function mount3d(){if(window.Eng)window.Eng.mount()}
function th3(m,hex){return window.Eng?window.Eng.thumb(m,hex):m.img}
{const ms=MODELS.filter(m=>!m.custom),cs=colorsOf(ms[0]),av=cs.map((c,i)=>c.n==="Белый"||c.n==="Чёрный"?-1:i).filter(i=>i>=0),FIX={},got={};ms.forEach(m=>{if(m.fix)FIX[m.id]=m.fix});
ms.forEach(m=>{if(FIX[m.id])got[m.id]=cs.findIndex(c=>c.n===FIX[m.id])});
ms.forEach((m,i)=>{if(got[m.id]!==undefined)return;const bad=new Set();for(let d=1;d<=4;d++){[ms[i-d],ms[i+d]].forEach(x=>{if(x&&got[x.id]!==undefined)bad.add(got[x.id])})}const ok=av.filter(c=>!bad.has(c)),p=ok.length?ok:av;got[m.id]=p[Math.floor(Math.random()*p.length)]});
ms.forEach(m=>{sel[m.id]=got[m.id]})}
const TAGS={tykva:["🎃","Хэллоуин"],ghost_hat:["🎃","Хэллоуин"],ghost:["🎃","Хэллоуин"],ghost_scarf:["🎃","Хэллоуин"],ghost_broom:["🎃","Хэллоуин"],heart_knit:["🔥","Хит"],pig:["🐾","Животные"],cat:["🐾","Животные"]};
const tg=m=>{const t=TAGS[m.id];return t?`<span class="tg${t[1]==="Хит"?" hit":""}" role="img" aria-label="${t[1]}" title="${t[1]}"><i aria-hidden="true">${t[0]}</i></span>`:""};
const fixQ=(m,v)=>{const st=stepOf(m);return Math.ceil((parseInt(String(v).replace(/\D/g,""),10)||0)/st)*st};
function addQty(m){return fixQ(m,dget(m))}
let added=null,addedT=0;
function syncDraft(){document.querySelectorAll(".qp").forEach(i=>{if(document.activeElement!==i)i.value=dget(byId(i.dataset.m))});
document.querySelectorAll("button.add[data-m]").forEach(b=>{const m=byId(b.dataset.m),v=addQty(m),l=b.querySelector(".al");if(!l)return;const ok=added===b.dataset.k;b.disabled=!v;b.classList.toggle("ok",ok);const t=ok?"Добавлено ✓":"Добавить";if(l.textContent!==t)l.textContent=t})}
document.addEventListener("click",e=>{const b=e.target.closest("button[data-dq]");if(!b)return;const m=byId(b.dataset.m),st=stepOf(m);{const nv=addQty(m)+(+b.dataset.dq)*st;draft[m.id]=nv>0?nv:""}const i=b.parentNode.querySelector(".qp");if(i)i.value=draft[m.id];syncDraft()});
document.addEventListener("input",e=>{const t=e.target;if(!t.classList||!t.classList.contains("qp"))return;const v=t.value.replace(/\D/g,"").slice(0,5);if(v!==t.value)t.value=v;draft[t.dataset.m]=v;syncDraft()});
document.addEventListener("change",e=>{const t=e.target;if(!t.classList||!t.classList.contains("qp"))return;const m=byId(t.dataset.m),v=addQty(m);draft[m.id]=v?v:"";t.value=draft[m.id];syncDraft()});
document.addEventListener("keydown",e=>{const t=e.target;if(e.key!=="Enter"||!t.classList||!t.classList.contains("qp"))return;e.preventDefault();const b=t.closest(".addrow").querySelector(".add");t.blur();b.click()});
const GC={};
function renderGrid(){const g=$("#grid");MODELS.forEach(m=>{const h=card(m),e=GC[m.id];const mk=()=>{const t=document.createElement("template");t.innerHTML=h;return t.content.firstElementChild};
if(!e){const el=mk();GC[m.id]={h,el};g.append(el)}else if(e.h!==h){const el=mk();e.el.replaceWith(el);e.el=el;e.h=h}})}
const lp={};
function card(m){const s=st(m),t=tiersOf(m);
const txt=m.noPrice?"по запросу":fmt(unit(m,s.T||minOf(m))),chg=lp[m.id]!==undefined&&lp[m.id]!==txt;lp[m.id]=txt;
const tag=`<span class="price${!m.noPrice&&s.T?" on":""}${chg?" pop":""}">${m.noPrice?txt:`${txt}<small>/шт</small>`}</span>`;
const ph=m.custom?`<div class="ph slot" aria-hidden="true"><div class="bls"><i class="bl b1"></i><i class="bl b2"></i><i class="bl b3"></i><i class="bl b4"></i></div><canvas class="spoil"></canvas>${tag}</div>`:`<div class="ph${m.m3&&gl3?" v3":""}"${m.m3&&gl3?` data-v="${m.id}"`:""}>${photo(m)}${m.m3&&gl3?`<button class="b3d" type="button" data-z3="${m.id}" aria-label="Открыть 3D-просмотр"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7"/></svg>3D</button>`:""}${tag}</div>`;
const info=m.custom?`<p class="desc">${customText(m)}</p>`:`<div class="cap">Тираж → цена за шт, ₸</div><div class="tiers" style="--n:${t.length}">${t.map(x=>`<div class="tp${isOn(m,s,x)}"><span>${x.from}+</span><b>${x.price}<i>&nbsp;₸</i></b></div>`).join("")}</div>`;
return `<article class="item"${m.custom?' id="custom"':''}>${ph}<h3>${m.name}</h3>${info}${swatches(m)}<div class="act">${ctrl(m,s)}${noteHTML(m,s)}</div></article>`}
{const w=CONFIG.brand.trim().split(/\s+/),a=document.createElement("span"),b=document.createElement("span"),h=$("#brand");a.className="w1";[...w.shift()].forEach((ch,i)=>{const l=document.createElement("span");l.className="lt";l.style.setProperty("--i",i);l.setAttribute("aria-hidden","true");l.textContent=ch;a.append(l)});b.className="w2";b.textContent=w.join(" ")+" ✨";h.textContent="";h.setAttribute("aria-label",CONFIG.brand);h.append(a,b)}
{const r=$("#barL");let last="";new MutationObserver(()=>{const v=r.textContent;if(v===last)return;last=v;r.classList.remove("pop");void r.offsetWidth;r.classList.add("pop")}).observe(r,{childList:true,characterData:true,subtree:true})}
const SP=(()=>{const P=[];let s=7;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;for(let i=0;i<260;i++)P.push({x:rnd(),y:rnd(),a:rnd()*6.283,v:.01+rnd()*.03,f:.8+rnd()*2.2,p:rnd()*6.283,r:.6+rnd()*1.1});return P})();
const still=matchMedia("(prefers-reduced-motion:reduce)").matches;
function watchVis(){if(!window.IntersectionObserver)return;const io=window.__vio||(window.__vio=new IntersectionObserver(es=>es.forEach(e=>{e.target._vis=e.isIntersecting;if(e.target.classList.contains("bls"))e.target.classList.toggle("off",!e.isIntersecting)}),{rootMargin:"80px"}));document.querySelectorAll("canvas.spoil,.bls").forEach(el=>{if(!el._wv){el._wv=1;io.observe(el)}})}
let spT=0;
function spoil(t){if(t-spT<45)return;spT=t;document.querySelectorAll("canvas.spoil").forEach(c=>{if(c._vis===false)return;const d=Math.min(window.devicePixelRatio||1,1.5),w=c.clientWidth,h=c.clientHeight;if(!w||!h)return;if(c.width!==Math.round(w*d)||c.height!==Math.round(h*d)){c.width=Math.round(w*d);c.height=Math.round(h*d)}
const g=c.getContext("2d"),T=still?0:t/1000;g.setTransform(d,0,0,d,0,0);g.clearRect(0,0,w,h);g.fillStyle="#fff";
for(let i=0;i<SP.length;i+=2){const q=SP[i];let x=(q.x+Math.cos(q.a)*q.v*T)%1,y=(q.y+Math.sin(q.a)*q.v*T)%1;if(x<0)x+=1;if(y<0)y+=1;g.globalAlpha=.12+.88*Math.pow(.5+.5*Math.sin(T*q.f+q.p),2);const s=q.r*1.8;g.fillRect(x*w-s/2,y*h-s/2,s,s)}})}
const EMO={ghost_scarf:"👻",ghost_broom:"🧹",heart_knit:"🧶",tykva:"🎃",ghost_hat:"👻",ghost:"👻",lamb:"🐑",cat:"🐱",pig:"🐷",heart:"❤️",custom:"✨"};
document.addEventListener("click",e=>{const b=e.target.closest("button[data-a=add],button[data-a=inc]");if(!b||still)return;const id=b.dataset.k.split("|")[0],em=EMO[id]||"✨",r=b.getBoundingClientRect(),x0=r.left+r.width/2,y0=r.top+r.height/2;
for(let i=0;i<9;i++){const p=document.createElement("span");p.textContent=em;p.setAttribute("aria-hidden","true");p.style.cssText=`position:fixed;left:${x0}px;top:${y0}px;z-index:95;pointer-events:none;font-size:${20+Math.random()*16}px;line-height:1;will-change:transform,opacity`;document.body.append(p);
const a=-Math.PI/2+(Math.random()-.5)*2.4,d=70+Math.random()*120,dx=Math.cos(a)*d,dy=Math.sin(a)*d,rot=(Math.random()-.5)*80;
p.animate([{transform:"translate(-50%,-50%) scale(.3) rotate(0deg)",opacity:1},{transform:`translate(calc(-50% + ${dx}px),calc(-50% + ${dy}px)) scale(1.1) rotate(${rot}deg)`,opacity:1,offset:.6},{transform:`translate(calc(-50% + ${dx*1.1}px),calc(-50% + ${dy+60}px)) scale(.8) rotate(${rot*1.4}deg)`,opacity:0}],{duration:900+Math.random()*500,delay:i*30,easing:"cubic-bezier(.2,.7,.3,1)",fill:"both"}).onfinish=()=>p.remove()}});
const spLoop=t=>{spoil(t);requestAnimationFrame(spLoop)};requestAnimationFrame(spLoop);
const TPs=MODELS.filter(m=>!m.noPrice),minP=Math.min(...TPs.map(m=>tiersOf(m).slice(-1)[0].price));
$("#advPrice").textContent=`От ${fmt(minP)} за штуку при тираже от 200 шт. Минимальный заказ — ${CONFIG.minQty} шт.`;
function tab(n,after){document.querySelectorAll("[data-page]").forEach(p=>p.hidden=p.dataset.page!==n);document.querySelectorAll("button[data-tab]").forEach(b=>{if(!b.classList.contains("pill"))return;const on=b.dataset.tab===n;b.classList.toggle("on",on);on?b.setAttribute("aria-current","page"):b.removeAttribute("aria-current")});window.scrollTo(0,0);try{history.replaceState(null,"","#"+n)}catch(e){}if(after)requestAnimationFrame(after)}
document.addEventListener("click",e=>{const t=e.target.closest("[data-tab]"),g=e.target.closest("[data-go]");if(t)tab(t.dataset.tab);else if(g)tab("catalog",()=>{const el=document.getElementById(g.dataset.go);el&&el.scrollIntoView({behavior:"smooth"})})});
if(location.hash==="#why")tab("why");'''
BODY=BODY+'<script src="three.min.js" defer></script><script src="engine.js" defer></script>'
import os,shutil,hashlib,base64
PROJ=os.environ.get("PROJ","/home/claude/proj")
OUT=os.environ.get("OUT","/home/claude/site")
os.makedirs(OUT,exist_ok=True)
html=page("raz.toppers",FONTS,CSS,BODY,CARD)
open("D.html","w",encoding="utf-8").write(html)          # фрагмент для артефакта (всё внутри)

# ---------- автономный сайт: настоящий <head>, предзагрузка, внешние картинки ----------
cat=json.load(open(PROJ+"/catalog.json",encoding="utf-8"))
st=html
sm=re.search(r"<style>.*?</style>",st,re.S); style=sm.group(0); st=st.replace(style,"",1)
st=re.sub(r"<title>.*?</title>\n","",st,count=1)
st=re.sub(r'<link rel="preconnect"[^>]*>',"",st)
st=re.sub(r'<link rel="stylesheet" href="https://fonts[^>]*>',"",st)
st=st.replace('<script src="three.min.js" defer></script><script src="engine.js" defer></script>',"")
shutil.rmtree(OUT+"/assets",ignore_errors=True); os.makedirs(OUT+"/assets")
def ext(m):
    b=m.group(2); name="assets/"+hashlib.sha1(b.encode()).hexdigest()[:10]+"."+{"jpeg":"jpg","svg+xml":"svg"}.get(m.group(1),m.group(1))
    open(OUT+"/"+name,"wb").write(base64.b64decode(b)); return name
DU=re.compile(r"data:image/(webp|jpeg|png|svg\+xml);base64,([A-Za-z0-9+/=]{1500,})")
st=DU.sub(ext,st); style=DU.sub(ext,style)
st=st.replace('<figure class="shot"><img src=','<figure class="shot"><img loading="lazy" decoding="async" src=')
boot="""<script>(function(){var h=document.documentElement,d=0,n=2;h.classList.add("boot");
function go(){if(d)return;d=1;requestAnimationFrame(function(){h.classList.remove("boot")})}
window.__go=go;setTimeout(go,1800);
function ok(){if(--n===0)go()}
function fonts(){var f=document.fonts;if(!f||!f.load){ok();return}Promise.all([f.load('800 1em "Inter Tight"'),f.load('600 1em "Inter Tight"'),f.load('400 1em "Inter"')]).then(ok,ok)}
function bind(){var l=document.getElementById("fontcss");if(!l){ok();return}if(l.sheet)fonts();else{l.addEventListener("load",fonts);l.addEventListener("error",ok)}}
function posters(){var im=[].slice.call(document.querySelectorAll(".ph img")).slice(0,4);Promise.all(im.map(function(i){return i.decode?i.decode().catch(function(){}):0})).then(ok,ok)}
window.__boot2=function(){bind();posters()}})();</script>"""
pre="".join('<link rel="preload" as="image" href="posters/%s.webp" fetchpriority="high">'%c["id"] for c in cat[:4])
pre+="".join('<link rel="preload" as="fetch" href="models/%s.bin" crossorigin fetchpriority="low">'%c["id"] for c in cat[:2])
head=('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
 '<title>raz.toppers</title><meta property="og:title" content="raz.toppers"><meta name="theme-color" content="#ffffff">'
 '<meta name="description" content="Топперы для кофейных стаканчиков — студия «Разгуляев»">'
 '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 +boot+style+pre+
 '<link id="fontcss" rel="stylesheet" href="%s" media="print" onload="this.media=\'all\'"><noscript><link rel="stylesheet" href="%s"></noscript>'%(FONTS,FONTS)+
 '<script src="three.min.js" defer></script><script src="engine.js" defer></script></head><body>')
open(OUT+"/index.html","w",encoding="utf-8").write(head+st+'<script>window.__boot2&&__boot2()</script></body></html>')
for f in("three.min.js","engine.js"): shutil.copy(PROJ+"/"+f,OUT+"/"+f)
for d in("models","posters"):
    shutil.rmtree(OUT+"/"+d,ignore_errors=True); os.makedirs(OUT+"/"+d)
    for f in os.listdir(PROJ+"/"+d): shutil.copy("%s/%s/%s"%(PROJ,d,f),"%s/%s/%s"%(OUT,d,f))
print("D33 ok",len(open(OUT+"/index.html",encoding="utf-8").read())//1024,"KB html;",len(os.listdir(OUT+"/assets")),"assets")
