"""Генерирует posters/<id>.webp для всех моделей из catalog.json (нейтральная светло-серая глина)."""
import json,base64,subprocess,time,sys,os
from playwright.sync_api import sync_playwright
SITE="/home/claude/site"; PROJ="/home/claude/proj"
cat=json.load(open(PROJ+"/catalog.json",encoding="utf-8"))
only=set(sys.argv[1:])
srv=subprocess.Popen(["python3","-m","http.server","8791","-d",SITE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"]); pg=b.new_page(viewport={"width":1000,"height":900})
        errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
        pg.goto("http://localhost:8791/index.html"); pg.wait_for_function("window.Eng&&window.Eng.ready",timeout=30000)
        for c in cat:
            if only and c["id"] not in only: continue
            d=pg.evaluate("(a)=>window.Eng.poster(a[0],a[1],a[2])",[c["id"],"#ffffff","models/%s.bin"%c["id"]])
            raw=base64.b64decode(d.split(",",1)[1]); open("%s/posters/%s.webp"%(PROJ,c["id"]),"wb").write(raw); print(c["id"],len(raw)//1024,"KB")
        print(errs); b.close()
finally: srv.terminate()
