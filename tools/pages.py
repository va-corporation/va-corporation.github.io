"""Service and case-study landing pages (one per language).

Data: pages/data/<id>.json
{
  "id": "ai-agents", "path": "ai-agents/",        # URL path under the language prefix
  "kind": "service" | "case",
  "image": "/assets/kulak-kombat.jpg" (optional), "link": "https://..." (optional external button),
  "i18n": {lang: {"title", "desc", "h1", "lead", "body": [{"h"}, {"p"}...], "faq": [[q, a], ...], "link_label"?}}
}
"""
import json, glob, os, html
import news

e = news.e
BASE = news.BASE

UI = {
 "en": dict(services="Services", cases="Case studies", more="Learn more", faq="Questions & answers", crumbs="Home", ours="Our services", work="Our work"),
 "de": dict(services="Leistungen", cases="Fallstudien", more="Mehr erfahren", faq="Fragen & Antworten", crumbs="Startseite", ours="Unsere Leistungen", work="Unsere Projekte"),
 "es": dict(services="Servicios", cases="Casos", more="Saber más", faq="Preguntas y respuestas", crumbs="Inicio", ours="Nuestros servicios", work="Nuestros proyectos"),
 "it": dict(services="Servizi", cases="Casi studio", more="Scopri di più", faq="Domande e risposte", crumbs="Home", ours="I nostri servizi", work="I nostri progetti"),
 "fr": dict(services="Services", cases="Études de cas", more="En savoir plus", faq="Questions et réponses", crumbs="Accueil", ours="Nos services", work="Nos projets"),
 "pl": dict(services="Usługi", cases="Studia przypadków", more="Dowiedz się więcej", faq="Pytania i odpowiedzi", crumbs="Strona główna", ours="Nasze usługi", work="Nasze projekty"),
 "uk": dict(services="Послуги", cases="Кейси", more="Детальніше", faq="Питання й відповіді", crumbs="Головна", ours="Наші послуги", work="Наші проєкти"),
 "ru": dict(services="Услуги", cases="Кейсы", more="Подробнее", faq="Вопросы и ответы", crumbs="Главная", ours="Наши услуги", work="Наши проекты"),
 "be": dict(services="Паслугі", cases="Кейсы", more="Падрабязней", faq="Пытанні і адказы", crumbs="Галоўная", ours="Нашы паслугі", work="Нашы праекты"),
 "ka": dict(services="სერვისები", cases="ქეისები", more="დაწვრილებით", faq="კითხვები და პასუხები", crumbs="მთავარი", ours="ჩვენი სერვისები", work="ჩვენი პროექტები"),
 "hy": dict(services="Ծառայություններ", cases="Դեպքերի ուսումնասիրություններ", more="Մանրամասն", faq="Հարցեր և պատասխաններ", crumbs="Գլխավոր", ours="Մեր ծառայությունները", work="Մեր նախագծերը"),
}

EXTRA_CSS = """
.hero-img{width:100%;border-radius:22px;border:1px solid var(--line);margin:22px 0 6px;display:block}
.faq details{background:var(--glass);border:1px solid var(--line);border-radius:16px;padding:16px 20px;margin:10px 0}
.faq summary{cursor:pointer;font-weight:700;font-size:17px}.faq details p{color:var(--muted);margin:10px 0 0}
.crumbs{font-size:14px;color:var(--muted);margin-top:30px}.crumbs a{color:var(--muted)}.crumbs a:hover{color:#fff}
.rel{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin:14px 0}
.rel a{display:block;padding:18px 20px;border-radius:18px;background:var(--glass);border:1px solid var(--line);color:var(--text);font-weight:700}
.rel a:hover{border-color:rgba(103,232,249,.55)}.rel a span{display:block;color:var(--gold);font-size:13px;margin-top:6px}
.btn.ghost{background:var(--glass);border:1px solid var(--line);color:#fff}
"""


def load():
    out = []
    for f in sorted(glob.glob("pages/data/*.json")):
        out.append(json.load(open(f, encoding="utf-8")))
    order = {"service": 0, "case": 1}
    out.sort(key=lambda p: (order.get(p["kind"], 2), p.get("order", 9)))
    return out


def url(p, l):
    return BASE + news.prefix(l) + p["path"]


def build_all(langs):
    pages = load()
    entries = []
    for p in pages:
        have = [l for l in langs if l in p["i18n"]]
        alts = [(l, url(p, l)) for l in have]
        for l in have:
            t, u = p["i18n"][l], UI[l]
            blocks = "".join(f"<h2>{e(b['h'])}</h2>" if "h" in b else f"<p>{e(b['p'])}</p>" for b in t["body"])
            img = f'<img class="hero-img" src="{p["image"]}" alt="{e(t["h1"])}" loading="lazy">' if p.get("image") else ""
            ext = f'<p><a class="btn" href="{e(p["link"])}" target="_blank" rel="noopener">{e(t.get("link_label", "Open"))} →</a></p>' if p.get("link") else ""
            faq = ""
            if t.get("faq"):
                faq = f'<h2>{e(u["faq"])}</h2><div class="faq">' + "".join(
                    f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in t["faq"]) + "</div>"
            others = [o for o in pages if o is not p and l in o["i18n"]]
            rel = ('<h2>' + e(u["ours"]) + '</h2><nav class="rel">' + "".join(
                f'<a href="/{news.prefix(l)}{o["path"]}">{e(o["i18n"][l]["h1"])}<span>{e(u["more"])} →</span></a>' for o in others) + "</nav>") if others else ""
            switch = '<nav class="langs" aria-label="Language">' + "".join(
                f'<a href="/{news.prefix(o)}{p["path"]}" hreflang="{o}"{" aria-current=\"true\"" if o == l else ""}>{news.LANG_NAME[o]}</a>' for o in have) + "</nav>"
            section = u["services"] if p["kind"] == "service" else u["cases"]
            body = (f'<p class="crumbs"><a href="{news.home_url(l)}">{e(u["crumbs"])}</a> › {e(section)}</p>'
                    f'<h1 style="margin-top:14px">{e(t["h1"])}</h1><p class="lead">{e(t["lead"])}</p>{img}{ext}{blocks}{faq}'
                    f'{news.cta(l)}{rel}{switch}')
            canon = url(p, l)
            graph = [{"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": u["crumbs"], "item": news.home_url(l)},
                {"@type": "ListItem", "position": 2, "name": t["h1"], "item": canon}]}]
            if p["kind"] == "service":
                graph.append({"@type": "Service", "name": t["h1"], "description": t["desc"], "url": canon, "inLanguage": l,
                              "provider": {"@type": "Organization", "name": "VA Corporation", "url": BASE}, "areaServed": "Worldwide"})
            else:
                graph.append({"@type": "CreativeWork", "name": t["h1"], "description": t["desc"], "url": canon, "inLanguage": l,
                              "creator": {"@type": "Organization", "name": "VA Corporation", "url": BASE}})
            if t.get("faq"):
                graph.append({"@type": "FAQPage", "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]})
            ld = {"@context": "https://schema.org", "@graph": graph}
            h = news.page(l, t["title"], t["desc"], canon, alts, body, ld)
            h = h.replace("</style>", EXTRA_CSS + "</style>", 1)
            h = h.replace(f'<a href="{news.index_url(l)}" aria-current="page">', f'<a href="{news.index_url(l)}">', 1)
            out = news.prefix(l) + p["path"] + "index.html"
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "w", encoding="utf-8").write(h)
            entries.append((canon, p.get("updated", "2026-11-22"), alts))
    return entries, pages


def home_links(pages, l):
    """Links block for the home page services section."""
    u = UI[l]
    svc = [p for p in pages if p["kind"] == "service" and l in p["i18n"]]
    case = [p for p in pages if p["kind"] == "case" and l in p["i18n"]]
    def row(items):
        return "".join(f'<a href="/{news.prefix(l)}{p["path"]}">{e(p["i18n"][l]["h1"])}<span>{e(u["more"])} →</span></a>' for p in items)
    out = ""
    if svc:
        out += f'<nav class="svc-links" aria-label="{e(u["ours"])}">{row(svc)}</nav>'
    return out, (f'<nav class="svc-links" aria-label="{e(u["cases"])}">{row(case)}</nav>' if case else "")


def faq_ld(html_page, lang):
    """FAQPage JSON-LD from the <details> FAQ on a built home page."""
    import re
    m = re.search(r'<div class="faq">(.*?)</div>', html_page, flags=re.S)
    if not m:
        return ""
    qa = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", m.group(1), flags=re.S)
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    items = [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qa if strip(q)]
    if not items:
        return ""
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang, "mainEntity": items}, ensure_ascii=False) + "</script>"
