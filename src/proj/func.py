import subprocess,time,base64
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(["python3","-m","http.server","8795","-d","/home/claude/site"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); errs=[]
    pg=b.new_page(viewport={"width":1280,"height":900}); pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.on("console",lambda m:errs.append(m.text[:160]) if m.type=="error" and "fonts" not in m.text and "Failed to load resource" not in m.text else None)
    pg.goto("http://localhost:8795/index.html"); pg.wait_for_timeout(2500)
    pg.evaluate("document.querySelector('#grid').scrollIntoView()"); pg.wait_for_timeout(2000)
    # rotation changes over time in LIVE card?
    r1=pg.evaluate("[document.querySelector('canvas.live').parentNode.dataset.v,Object.values(Eng.V).map(v=>+v.rot.toFixed(2))]"); pg.wait_for_timeout(700)
    r2=pg.evaluate("[document.querySelector('canvas.live').parentNode.dataset.v,Object.values(Eng.V).map(v=>+v.rot.toFixed(2))]"); print("live",r1[0],"->",r2[0],"rot moves:",r1[1]!=r2[1])
    # hover card 3 -> becomes live
    box=pg.evaluate("(()=>{const r=document.querySelectorAll('.ph')[2].getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()"); pg.mouse.move(*box); pg.wait_for_timeout(500)
    print("hover live ->",pg.evaluate("document.querySelector('canvas.live').parentNode.dataset.v"))
    # drag rotates
    rot0=pg.evaluate("Eng.V.ghost_scarf.rot"); pg.mouse.down(); pg.mouse.move(box[0]+80,box[1],steps=6); pg.mouse.up(); pg.wait_for_timeout(200); print("drag dRot",round(pg.evaluate("Eng.V.ghost_scarf.rot")-rot0,2))
    # change colour by clicking a swatch in card 2 (pig)
    pg.evaluate("document.querySelectorAll('.item')[1].querySelectorAll('.dot')[1].click()"); pg.wait_for_timeout(900)
    print("pig colour:",pg.evaluate("document.querySelectorAll('.item')[1].querySelector('.cn').textContent"),"still has canvas:",pg.evaluate("!!document.querySelectorAll('.item')[1].querySelector('canvas.cv3')"))
    # add to cart 2 items, set qty
    pg.evaluate("document.querySelectorAll('.item')[1].querySelector('.add').click()"); pg.wait_for_timeout(300)
    pg.evaluate("(()=>{const q=document.querySelectorAll('.item')[1].querySelector('.qp');q.value='60';q.dispatchEvent(new Event('change',{bubbles:true}))})()"); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelector('#openCart').click()"); pg.wait_for_timeout(700)
    src=pg.evaluate("document.querySelector('#list .rp img').src.slice(0,30)"); print("cart thumb:",src)
    pg.screenshot(path="/home/claude/v/AT_cart.png")
    pg.evaluate("document.querySelector('#close').click()"); pg.wait_for_timeout(300)
    # modal
    pg.evaluate("document.querySelectorAll('.b3d')[3].click()"); pg.wait_for_timeout(1800)
    print("modal open:",pg.evaluate("!document.querySelector('#m3').hidden"))
    pg.screenshot(path="/home/claude/v/AT_modal.png")
    pg.evaluate("document.querySelector('#m3 .dot').click()"); pg.wait_for_timeout(800)
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300); print("modal closed:",pg.evaluate("document.querySelector('#m3').hidden"))
    print(errs); b.close()
finally: srv.terminate()
