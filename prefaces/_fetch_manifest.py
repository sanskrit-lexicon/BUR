import sys, re, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')
B="https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/burpref"
pat=re.compile(r'bur_Page_\d+_Image_\d+\.png', re.I)
rows=[]
for n in range(1,29):
    nn=f"{n:02d}"; img=None
    for t in range(8):
        try:
            with urllib.request.urlopen(f"{B}/burpref{nn}.html", timeout=30) as r:
                html=r.read().decode('utf-8','replace')
            m=pat.search(html)
            if m: img=m.group(0); break
        except Exception as e:
            pass
        time.sleep(1.5)
    rows.append(f"{nn}|{img or 'MISSING'}")
    print(rows[-1], flush=True)
open(r"C:\Users\user\Documents\GitHub\BUR\prefaces\_manifest.txt","w",encoding="utf-8").write("\n".join(rows)+"\n")
print("DONE", flush=True)
