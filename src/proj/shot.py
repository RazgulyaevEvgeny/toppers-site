import subprocess,time,sys
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(["python3","-m","http.server","8792","-d","/home/claude/site"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); errs=[]
        for w,h in((1280,800),(390,844)):
            pg=b.new_page(viewport={"width":w,"height":h}); pg.on("pageerror",lambda e:errs.append(str(e)))
            reqs=[]; pg.on("request",lambda r:reqs.append(r.url.split("/")[-1]) if "localhost" in r.url else None)
            pg.on("response",lambda r:errs.append("HTTP %d %s"%(r.status,r.url)) if "localhost" in r.url and r.status>=400 else None)
            pg.goto("http://localhost:8792/index.html"); pg.wait_for_timeout(600)
            pg.evaluate("document.querySelector('#grid').scrollIntoView()"); pg.wait_for_timeout(3500)
            print(w,"ready cards",pg.evaluate("document.querySelectorAll('.ph.ready').length"),"loaded",pg.evaluate("Object.values(Eng.V).filter(v=>v.st==='ready').length"),"over-x",pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"))
            pg.screenshot(path=f"/home/claude/v/AS_{w}.png"); print(reqs[:30]); pg.close()
        print(errs); b.close()
finally: srv.terminate()
