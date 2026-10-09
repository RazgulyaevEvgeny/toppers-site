import subprocess,time
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(["python3","-m","http.server","8796","-d","/home/claude/site"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
  with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); errs=[]
    for W,H in((1280,900),(360,740)):
      pg=b.new_page(viewport={"width":W,"height":H}); pg.on("pageerror",lambda e:errs.append(str(e)))
      pg.on("console",lambda m:errs.append(m.text[:160]) if m.type=="error" and "fonts" not in m.text and "Failed to load resource" not in m.text else None)
      pg.goto("http://localhost:8796/index.html"); pg.wait_for_timeout(2500)
      it=pg.locator(".item").nth(1); it.scroll_into_view_if_needed(); pg.wait_for_timeout(800)
      lab=lambda: it.locator(".add .al").inner_text()
      cnt=lambda: pg.evaluate("document.querySelector('#barL').textContent")
      print(W,"label0:",lab(),"cart:",repr(cnt()))
      it.locator("button[data-dq='1']").click(); it.locator("button[data-dq='1']").click(); print("after ++:",lab(),"input:",it.locator(".qp").input_value(),"cart:",repr(cnt()))
      it.locator("button[data-dq='-1']").click(); print("after -:",lab(),"cart:",repr(cnt()))
      it.locator(".qp").fill(""); it.locator(".qp").type("120"); print("typed 120:",lab(),"cart:",repr(cnt()))
      it.locator(".qp").fill("125"); print("typed 125 label:",lab())
      it.locator(".add").click(); pg.wait_for_timeout(400)
      it=pg.locator(".item").nth(1)
      print("after add: cart",repr(cnt()),"note:",it.locator(".sub").inner_text(),"| btn:",it.locator(".add .al").inner_text())
      it.locator(".qp").fill(""); print("empty -> disabled:",it.locator(".add").is_disabled(),it.locator(".add .al").inner_text())
      it.locator(".qp").fill("30"); it.locator(".qp").press("Enter"); pg.wait_for_timeout(300); print("enter adds 30 -> cart",repr(cnt()))
      pg.screenshot(path=f"/home/claude/v/AU_card_{W}.png")
      # modal
      pg.evaluate("document.querySelectorAll('.b3d')[3].click()"); pg.wait_for_timeout(1800)
      print("modal q:",pg.evaluate("document.querySelector('#m3q').innerText.replace(/\\n/g,' | ')"))
      pg.locator("#m3 .dot").nth(2).click(); pg.wait_for_timeout(600)
      pg.locator("#m3q .qp").fill("70"); pg.locator("#m3q .add").click(); pg.wait_for_timeout(500)
      print("modal add 70 -> cart",repr(cnt()),"| m3q:",pg.evaluate("document.querySelector('#m3q').innerText.replace(/\\n/g,' | ')"))
      pg.screenshot(path=f"/home/claude/v/AU_modal_{W}.png")
      pg.wait_for_timeout(1500); print("btn reset:",pg.locator("#m3q .add .al").inner_text())
      pg.keyboard.press("Escape")
      pg.evaluate("document.querySelector('#openCart').click()"); pg.wait_for_timeout(500)
      print("cart rows:",pg.evaluate("[...document.querySelectorAll('#list .row')].map(r=>r.innerText.replace(/\\n/g,' ')).join(' ## ')"))
      pg.close()
    print(errs); b.close()
finally: srv.terminate()
