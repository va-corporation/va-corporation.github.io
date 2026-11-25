"""Build one static page per language from src/site.html.

Run from the repo root:  python3 tools/build.py
Output: index.html (English, x-default) and <lang>/index.html for every other language,
plus sitemap.xml with hreflang alternates.
"""
import news, pages, videos, extra, legal, re, datetime, os, html as _html

BASE = "https://va-corporation.github.io/"
LANGS = ["en", "de", "es", "it", "fr", "pl", "uk", "ru", "be", "ka", "hy"]
OG = {"en": "en_US", "de": "de_DE", "es": "es_ES", "it": "it_IT", "fr": "fr_FR", "ru": "ru_RU", "be": "be_BY", "uk": "uk_UA", "pl": "pl_PL", "ka": "ka_GE", "hy": "hy_AM"}
META = {
    "en": ("AI Agent Development & Game Studio — VA Corporation",
           "Custom AI agents and AI chatbots for business, Telegram bots, websites and game development. Prices from €190 + VAT. Free consultation."),
    "de": ("KI-Agenten erstellen lassen & Spieleentwicklung — VA Corporation",
           "KI-Agenten und KI-Chatbots für Unternehmen, Telegram-Bots, Websites und Spiele entwickeln lassen. Preise ab 190 € zzgl. MwSt. Kostenlose Beratung."),
    "es": ("VA Corporation — agentes de IA, juegos y software",
           "VA Corporation crea agentes de IA, juegos y software: asistentes de IA para empresas, agentes de vídeo con IA, automatización, webs y bots."),
    "it": ("VA Corporation — agenti IA, giochi e software",
           "VA Corporation crea agenti IA, giochi e software: assistenti IA per le aziende, agenti video IA, automazione, siti web e bot."),
    "fr": ("VA Corporation — agents IA, jeux et logiciels",
           "VA Corporation crée des agents IA, des jeux et des logiciels : assistants IA pour les entreprises, agents vidéo IA, automatisation, sites web et bots."),
    "ru": ("Разработка ИИ-агентов и игр на заказ — VA Corporation",
           "ИИ-агенты и чат-боты для бизнеса, Telegram-боты, сайты и разработка игр на заказ. Цены от 190 € + НДС. Бесплатная консультация."),
    "be": ("VA Corporation — AI-агенты, гульні і софт",
           "VA Corporation стварае AI-агентаў, гульні і софт: AI-асістэнты для бізнесу, AI-відэаагенты, аўтаматызацыя, сайты і боты."),
    "uk": ("VA Corporation — AI-агенти, ігри та софт",
           "VA Corporation створює AI-агентів, ігри та софт: AI-асистенти для бізнесу, AI-відеоагенти, автоматизація, сайти й боти."),
    "pl": ("VA Corporation — agenci AI, gry i oprogramowanie",
           "VA Corporation tworzy agentów AI, gry i oprogramowanie: asystentów AI dla firm, agentów wideo AI, automatyzację, strony i boty."),
    "ka": ("VA Corporation — AI აგენტები, თამაშები და პროგრამები",
           "VA Corporation ქმნის AI აგენტებს, თამაშებს და პროგრამებს: AI ასისტენტები ბიზნესისთვის, AI ვიდეო-აგენტები, ავტომატიზაცია, საიტები და ბოტები."),
    "hy": ("VA Corporation — AI գործակալներ, խաղեր և ծրագրեր",
           "VA Corporation-ը ստեղծում է AI գործակալներ, խաղեր և ծրագրեր՝ AI օգնականներ բիզնեսի համար, AI վիդեո գործակալներ, ավտոմատացում, կայքեր և բոտեր։"),
}

PATH = {"be": "by", "uk": "ua", "ka": "ge", "hy": "am"}

EXTRA = extra.load()
CORE = list(LANGS)
for _c, _d in EXTRA.items():
    LANGS.append(_c)
    OG[_c] = _d["og"]
    META[_c] = tuple(_d["meta"])
    news.OG[_c] = _d["og"]
    news.LANG_NAME[_c] = _d["name"].split(" ")[0]
    news.UI[_c] = dict(news.UI["en"], **_d.get("news", {}))
    pages.UI[_c] = dict(pages.UI["en"], **_d.get("pages", {}))
    videos.UI[_c] = tuple(_d.get("videos", videos.UI["en"]))


def url(l):
    return BASE if l == "en" else f"{BASE}{PATH.get(l, l)}/"

# a data-l span: inner content may contain one level of nested <span>…</span>
SPAN = re.compile(r'<span data-l="(\w+)">((?:[^<]|<span[^>]*>[^<]*</span>|<(?!/?span\b)[^>]*>)*?)</span>')

def build(tpl, lang):
    s = SPAN.sub(lambda m: m.group(0) if m.group(1) == lang else "", tpl)
    s = s.replace('<html lang="en" translate="no">', f'<html lang="{lang}">', 1)
    title, desc = META[lang]
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', s, count=1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', s, count=1)
    s = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url(lang)}">', s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url(lang)}">', s, count=1)
    # og:locale = this language, alternates = the others
    s = re.sub(r'<meta property="og:locale"[^>]*>(<meta property="og:locale:alternate"[^>]*>)*', "", s)
    alts = "".join(f'<meta property="og:locale:alternate" content="{OG[o]}">' for o in LANGS if o != lang)
    hreflang = "".join(f'\n<link rel="alternate" hreflang="{o}" href="{url(o)}">' for o in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{BASE}">'
    s = re.sub(r'\n?<link rel="alternate" hreflang="[^"]*" href="[^"]*">', "", s)
    s = s.replace(f'<link rel="canonical" href="{url(lang)}">',
                  f'<link rel="canonical" href="{url(lang)}">{hreflang}\n<meta property="og:locale" content="{OG[lang]}">{alts}', 1)
    # selected option
    s = s.replace(f'<option value="{lang}">', f'<option value="{lang}" selected>', 1)
    # root-relative assets so sub-folders work
    s = s.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    return s

def latest_extra(arts, l, n=3):
    u = news.UI[l]
    mine = [a for a in arts if "en" in a["i18n"]][:n]
    if not mine:
        return ""
    e = news.e
    cards = "".join(
        f'<a class="ncard" href="/{news.art_path(a, "en")}" hreflang="en"><time datetime="{a["date"]}">{news.fmt_date(a["date"], l)}</time>'
        f'<h3>{e(a["i18n"]["en"]["title"])}</h3><p>{e(a["i18n"]["en"]["desc"])}</p><span>{e(u["read"])} (EN) →</span></a>' for a in mine)
    return (f'<section id="news"><div class="wrap"><div class="kicker">{e(u["news"])}</div><h2>{e(u["latest"])}</h2>'
            f'<div class="ngrid">{cards}</div><p style="margin-top:22px"><a class="btn ghost" href="/news/">{e(u["all"])} →</a></p></div></section>')


def home(tpl, l, arts, pgs):
    h = build(tpl, l).replace("<!--NEWS-->", latest_extra(arts, l) if l in EXTRA else news.latest_block(arts, l))
    if l in EXTRA:
        h = h.replace('href="news/"', 'href="/news/"')
        h = h.replace("</head>", f'<style>[data-l="{l}"]{{display:revert}}</style>\n</head>', 1)
        h = h.replace("OK={en:", "OK={" + l + ":" + repr(EXTRA[l].get("ok", "Copied!")) + ",en:", 1)
    svc, case = pages.home_links(pgs, l)
    h = h.replace("<!--SVCLINKS-->", svc).replace("<!--CASELINKS-->", case)
    foot = '<nav class="footlinks">' + "".join(
        f'<a href="/{news.prefix(l)}{p["path"]}">{news.e(p["i18n"][l]["h1"])}</a>' for p in pgs if l in p["i18n"]) + \
        f'<a href="/{"" if l in EXTRA else news.prefix(l)}news/">{news.e(news.UI[l]["news"])}</a><a href="/{news.prefix(l)}videos/">{news.e(videos.UI[l][0])}</a>' + legal.links(l) + '</nav>'
    h = h.replace("<!--FOOTLINKS-->", foot)
    h = h.replace("</head>", pages.faq_ld(h, l) + "\n</head>", 1)
    return h

def main():
    tpl = open("src/site.html", encoding="utf-8").read()
    opts = "".join(f'<option value="{c}">{_html.escape(d["name"])}</option>' for c, d in EXTRA.items())
    tpl = tpl.replace('<option value="hy">AM · Հայերեն</option>', '<option value="hy">AM · Հայերեն</option>' + opts, 1) if opts else tpl
    tpl = tpl.replace("var SUP=['en','de','es','it','fr','ru','be','uk','pl','ka','hy'];",
                      "var SUP=" + repr(CORE + list(EXTRA)).replace(" ", "") + ";", 1)
    for c, d in EXTRA.items():
        tpl = extra.inject(tpl, c, d)
    nentries, arts = news.build_all(CORE)
    pentries, pgs = pages.build_all(LANGS)
    nentries = pentries + nentries + videos.build_all(LANGS) + legal.build_all()
    vids = videos.load()
    for l in LANGS:
        out = "index.html" if l == "en" else f"{PATH.get(l, l)}/index.html"
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        open(out, "w", encoding="utf-8").write(home(tpl, l, arts, pgs).replace("<!--REELS-->", videos.home_block(vids, l)))
    for l in LANGS:  # short, hashtag-free links for social posts: /<lang>/prices/ -> /<lang>/#prices
        t = "/" if l == "en" else f"/{PATH.get(l, l)}/"
        d = "prices" if l == "en" else f"{PATH.get(l, l)}/prices"
        os.makedirs(d, exist_ok=True)
        open(f"{d}/index.html", "w", encoding="utf-8").write(
            f'<!DOCTYPE html><html lang="{l}" translate="no"><head><meta charset="utf-8"><meta name="google" content="notranslate"><title>VA Corporation — Prices</title>'
            f'<meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE[:-1]}{t}#prices">'
            f'<meta http-equiv="refresh" content="0; url={t}#prices"><script>location.replace("{t}#prices")</script></head>'
            f'<body><a href="{t}#prices">VA Corporation — Prices</a></body></html>')
    today = datetime.date.today().isoformat()
    links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{o}" href="{url(o)}"/>' for o in LANGS) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>'
    urls = "".join(f"\n  <url>\n    <loc>{url(l)}</loc>\n    <lastmod>{today}</lastmod>{links}\n  </url>" for l in LANGS)
    for loc, mod, alts in nentries:
        al = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{o}" href="{h}"/>' for o, h in alts)
        urls += f"\n  <url>\n    <loc>{loc}</loc>\n    <lastmod>{mod}</lastmod>{al}\n  </url>"
    open("sitemap.xml", "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}\n</urlset>\n')
    print("built", LANGS, "news pages:", len(nentries))

if __name__ == "__main__":
    main()
