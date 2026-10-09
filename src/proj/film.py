"""Раскадровка загрузки через CDP screencast. python3 film.py tag [cpu] [mbps] [lat]"""
import sys,subprocess,time,base64,io
from playwright.sync_api import sync_playwright
from PIL import Image
tag=sys.argv[1]; cpu=float(sys.argv[2]) if len(sys.argv)>2 else 2; mb=float(sys.argv[3]) if len(sys.argv)>3 else 8; lat=int(sys.argv[4]) if len(sys.argv)>4 else 60
srv=subprocess.Popen(["python3","-m","http.server","8803","-d","/home/claude/site"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
frames=[]
try:
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader"])
        ctx=b.new_context(viewport={"width":390,"height":844},device_scale_factor=1,is_mobile=True,has_touch=True)
        pg=ctx.new_page()
        pg.route("**/fonts.googleapis.com/**",lambda r:(time.sleep(0.4),r.fulfill(status=200,content_type="text/css",body="")))
        pg.route("**/fonts.gstatic.com/**",lambda r:r.abort())
        cdp=ctx.new_cdp_session(pg); cdp.send("Network.enable")
        cdp.send("Network.emulateNetworkConditions",{"offline":False,"latency":lat,"downloadThroughput":mb*1024*1024/8,"uploadThroughput":1024*1024/8})
        cdp.send("Emulation.setCPUThrottlingRate",{"rate":cpu})
        t0=[None]
        def on(e):
            ts=e["metadata"]["timestamp"]
            if t0[0] is None: t0[0]=ts
            frames.append((ts-t0[0],base64.b64decode(e["data"]))); cdp.send("Page.screencastFrameAck",{"sessionId":e["sessionId"]})
        cdp.on("Page.screencastFrame",on)
        cdp.send("Page.startScreencast",{"format":"jpeg","quality":50,"maxWidth":390,"maxHeight":844,"everyNthFrame":1})
        pg.goto("http://localhost:8803/index.html",wait_until="commit"); pg.wait_for_timeout(9000)
        cdp.send("Page.stopScreencast"); b.close()
finally: srv.terminate()
print(len(frames),"frames; times:",[round(t,2) for t,_ in frames][:40])
# контактный лист: до 14 кадров, равномерно по времени
if frames:
    ts=[t for t,_ in frames]; pick=[]
    for k in range(14):
        tt=k*0.35
        i=min(range(len(ts)),key=lambda j:abs(ts[j]-tt)); 
        if i not in pick: pick.append(i)
    ims=[Image.open(io.BytesIO(frames[i][1])).convert("RGB").resize((195,422)) for i in pick]
    o=Image.new("RGB",(195*len(ims),422),"white")
    for k,im in enumerate(ims): o.paste(im,(195*k,0))
    o.save(f"/tmp/claude-0/stl/film_{tag}.png"); print("picked t=",[round(ts[i],2) for i in pick])
