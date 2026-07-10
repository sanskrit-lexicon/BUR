import sys, os, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__))
IMG="https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/_images"
os.makedirs(os.path.join(HERE,"scans"),exist_ok=True)
rows=[l.strip() for l in open(os.path.join(HERE,"_manifest.txt"),encoding="utf-8") if l.strip()]
for row in rows:
    nn,img=row.split("|")
    if img=="MISSING": print("SKIP",nn); continue
    dest=os.path.join(HERE,"scans",img)
    if os.path.exists(dest) and os.path.getsize(dest)>10000:
        print("have",img,os.path.getsize(dest)); continue
    ok=False
    for t in range(6):
        try:
            urllib.request.urlretrieve(f"{IMG}/{img}",dest)
            if os.path.getsize(dest)>10000: ok=True; break
        except Exception as e: pass
        time.sleep(2)
    print("OK" if ok else "FAIL",img, os.path.getsize(dest) if os.path.exists(dest) else 0, flush=True)
print("ALLDONE",flush=True)
