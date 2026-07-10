import sys, urllib.request, ssl
sys.stdout.reconfigure(encoding='utf-8')
ctx=ssl.create_default_context()
B="https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/burpref"
for nn in ["01","06"]:
    try:
        with urllib.request.urlopen(f"{B}/burpref{nn}.html", timeout=60, context=ctx) as r:
            html=r.read().decode('utf-8','replace')
        print(f"=== {nn} len={len(html)} ===")
        import re
        for m in re.finditer(r'<img[^>]*>', html, re.I):
            print("IMG:", m.group(0)[:300])
        # also any token ending in .png
        for m in re.finditer(r'[\w./-]+\.png', html, re.I):
            print("PNG:", m.group(0))
    except Exception as e:
        print(nn, "ERR", repr(e))
