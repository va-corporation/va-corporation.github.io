"""Compile i18n/src/<lang>.json (index-keyed drafts) into i18n/<lang>.json (English-string-keyed)."""
import json, glob, os, sys, re
EN = json.load(open("i18n/_en.json", encoding="utf-8"))
PRICE = re.compile(r'^(from )?([\d ]+) €(/mo)?$')
NK = ['news','head','intro','sources','read','all','home','latest','cta_h','cta_p','cta']
PK = ['services','cases','more','faq','crumbs','ours','work']
for f in sorted(glob.glob("i18n/src/*.json")):
    code = os.path.basename(f)[:-5]
    d = json.load(open(f, encoding="utf-8"))
    t = {}
    for i, en in enumerate(EN):
        m = PRICE.match(en)
        if m:
            num = m.group(2).replace(" ", d.get("thou", " "))
            v = d["price"].replace("{}", num + " €") if m.group(1) else num + " €"
            if m.group(3): v += d["mo"]
            if not m.group(1) and m.group(3): v = num + " €" + d["mo"]
            t[en] = v
        elif str(i) in d["t"]:
            t[en] = d["t"][str(i)]
    miss = [i for i, en in enumerate(EN) if en not in t]
    out = {"name": d["name"], "og": d["og"], "meta": d["meta"], "t": t,
           "news": dict(zip(NK, d["news"])), "pages": dict(zip(PK, d["pages"])), "videos": d["videos"], "ok": d["ok"]}
    json.dump(out, open(f"i18n/{code}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(code, "missing:", miss)
