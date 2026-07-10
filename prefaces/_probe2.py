import sys, urllib.request, ssl, time
sys.stdout.reconfigure(encoding='utf-8')
B="https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/burpref"
hdr={'User-Agent':'Mozilla/5.0'}
def get(url, tries=15):
    last=None
    for t in range(tries):
        for ctx in (ssl.create_default_context(),):
            try:
                req=urllib.request.Request(url, headers=hdr)
                with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                    return r.read().decode('utf-8','replace')
            except Exception as e:
                last=e
        time.sleep(2)
    return f"__FAIL__ {last!r}"
h=get(f"{B}/burpref01.html")
open("_raw01.html","w",encoding="utf-8").write(h)
print("len01", len(h))
print(h[:500] if not h.startswith("__FAIL__") else h)
