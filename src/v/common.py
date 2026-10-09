import re
SRC=open("/home/claude/final.html",encoding="utf-8").read()
LOGO=re.search(r'data:image/svg\+xml;base64,[A-Za-z0-9+/=]+',SRC).group(0)
SCRIPT=SRC[SRC.index("<script>")+8:SRC.rindex("</script>")]
a=SCRIPT.index("function card(m){"); z=SCRIPT.index("function msg()")
CORE_PRE=SCRIPT[:a]; CORE_POST=SCRIPT[z:]
CORE_POST=CORE_POST.replace('if(c)s+=`\\nКофейня: ${c}`;','const wh=$("#who").value.trim();if(wh)s+=`\\nИмя: ${wh}`;if(c)s+=`\\nКофейня: ${c}`;').replace('$("#cafe").oninput=$("#note").oninput=render;','$("#who").oninput=$("#cafe").oninput=$("#note").oninput=render;')
HELPERS=r'''
const PLUS='<svg viewBox="0 0 48 48" width="44" height="44" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M24 8v32M8 24h32"/></svg>';
const st=m=>{const k=key(m.id,sel[m.id]),q=cart[k]||0,T=total(m.id),mn=minOf(m);return{k,q,T,mn,addQ:Math.max(stepOf(m),mn-T),ok:!T||T>=mn}};
const swatches=m=>{if(m.custom)return"";const cs=colorsOf(m);return `<div class="sw" role="group" aria-label="Цвет">${cs.map((c,i)=>`<button class="dot${i===sel[m.id]?" on":""}" style="--c:${c.c}" data-a="col" data-id="${m.id}" data-i="${i}" aria-label="${c.n}" aria-pressed="${i===sel[m.id]}" title="${c.n}"></button>`).join("")}</div><div class="cn">Цвет: ${cs[sel[m.id]].n}</div>`};
const ctrl=(m,s)=>s.q?`<div class="qty"><button data-a="dec" data-k="${s.k}" aria-label="Меньше">−</button><span>${s.q} шт</span><button data-a="inc" data-k="${s.k}" aria-label="Больше">+</button></div>`:`<button class="add" data-a="add" data-k="${s.k}">Добавить ${s.addQ} шт</button>`;
const noteHTML=(m,s)=>{const n=!s.T?"":!s.ok?`Минимум ${s.mn} шт, добавьте ещё ${s.mn-s.T}`:m.custom?`В заказе ${s.T} шт, цену назовём после макета`:`В заказе ${s.T} шт · ${fmt(unit(m,s.T))}/шт`;return n?`<div class="sub${s.ok?"":" warn"}">${n}</div>`:""};
const customText=m=>`Принесите логотип или персонажа, напечатаем по вашему макету. От ${minOf(m)} шт, шаг ${stepOf(m)} шт.`;
const isOn=(m,s,x)=>s.T&&pick(tiersOf(m),s.T)===x?" on":"";
const photo=m=>`<img src="${m.img}" alt="${m.name}, топпер на крышке стакана">`;
'''
def build(css, markup, card_js, title_fonts=""):
    js=CORE_PRE+HELPERS+card_js+"\n"+CORE_POST
    return css, markup, js
CART_MARKUP='''<div class="bar" id="bar"><button id="openCart"><span id="barL"></span><span id="barR"></span></button></div>
<div class="ov" id="ov"><div class="sheet" role="dialog" aria-label="Корзина">
<h2>Ваш заказ <button class="x" id="close" aria-label="Закрыть">✕</button></h2>
<div id="list"></div>
<div class="leads" id="leads"></div>
<div class="tot"><span>Итого</span><span id="total"></span></div>
<label for="who">Как мы можем к вам обращаться</label><input id="who" autocomplete="name" placeholder="Имя">
<label for="cafe">Название кофейни</label><input id="cafe" autocomplete="organization">
<label for="note">Комментарий (для своей модели опишите, что напечатать)</label><textarea id="note" rows="2"></textarea>
<div id="warn"></div>
<a class="wa" id="wa" target="_blank" rel="noopener">Отправить заказ в WhatsApp</a>
<p class="hint">Откроется WhatsApp с готовым текстом заказа, останется нажать «Отправить».</p>
</div></div>'''
FOOT='<footer><b>Студия брендирования Разгуляев</b><br>Заказы принимаем в <a href="https://wa.me/77064230226" target="_blank" rel="noopener">WhatsApp</a></footer>'
def page(title,fonts,css,body_top,card_js):
    js=CORE_PRE+HELPERS+card_js+"\n"+CORE_POST
    return f'''<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<style>
{css}
</style>
{body_top}
{CART_MARKUP}
<script>
{js}
</script>
'''
CORE_POST=CORE_POST.replace(" (срок ${lead(m,T)})","").replace("(цена и срок после согласования макета)","(цену назовём после согласования макета)")
CORE_POST=re.sub(r'\$\("#leads"\)\.innerHTML=.*?;\n\$\("#total"\)',lambda m:'$("#leads").innerHTML=L.length?"<b>Срок изготовления:</b> менеджер уточнит в WhatsApp после отправки заказа."+(ls.some(x=>x.np)?"<br>Цену своей модели назовём после согласования макета.":""):"";\n$("#total")',CORE_POST,flags=re.S)
