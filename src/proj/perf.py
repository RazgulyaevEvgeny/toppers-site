"""Замер загрузки на «телефоне»: filmstrip + long tasks. python3 perf.py tag"""
import sys,subprocess,time,json
from playwright.sync_api import sync_playwright
tag=sys.argv[1] if len(sys.argv)>1 else "a"
SITE=sys.argv[2] if len(sys.argv)>2 else "/home/claude/site"
srv=subprocess.Popen(["python3","-m","http.server","8801","-d",SITE],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
        ctx=b.new_context(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True,has_touch=True)
        pg=ctx.new_page()
        def fonts(route):
            time.sleep(0.5); route.fulfill(status=200,content_type="text/css",body="")
        pg.route("**/fonts.googleapis.com/**",fonts); pg.route("**/fonts.gstatic.com/**",lambda r:r.abort())
        cdp=ctx.new_cdp_session(pg)
        cdp.send("Network.enable"); cdp.send("Network.emulateNetworkConditions",{"offline":False,"latency":120,"downloadThroughput":1.6*1024*1024/8,"uploadThroughput":750*1024/8})
        cdp.send("Emulation.setCPUThrottlingRate",{"rate":4})
        pg.add_init_script("""window.__lt=[];try{new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lt.push([Math.round(e.startTime),Math.round(e.duration)])}).observe({entryTypes:['longtask']})}catch(e){}""")
        t0=time.time(); pg.goto("http://localhost:8801/index.html",wait_until="commit")
        shots=[]
        for i in range(24):
            t=time.time()-t0
            try: pg.screenshot(path=f"/tmp/claude-0/stl/perf_{tag}_{i:02d}.png",scale="css")
            except Exception as e: pass
            shots.append(round(t,2)); time.sleep(0.35)
        m=pg.evaluate("""()=>({fcp:(performance.getEntriesByName('first-contentful-paint')[0]||{}).startTime,lt:window.__lt,ready:document.querySelectorAll('.ph.ready').length,items:document.querySelectorAll('.item').length,res:performance.getEntriesByType('resource').map(r=>[r.name.split('/').slice(-2).join('/'),Math.round(r.startTime),Math.round(r.responseEnd),r.transferSize])})""")
        print("shots at",shots[:8],"...")
        print("FCP",m['fcp'],"ready cards",m['ready'],"/",m['items'])
        print("longtasks",m['lt'])
        for r in m['res']:
            if not r[0].endswith('.webp') or True: print(r)
        b.close()
finally: srv.terminate()
