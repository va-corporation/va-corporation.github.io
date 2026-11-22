"""Build one static page per language from src/site.html.

Run from the repo root:  python3 tools/build.py
Output: index.html (English, x-default) and <lang>/index.html for every other language,
plus sitemap.xml with hreflang alternates.
"""
import news, pages, videos, re, datetime, os

BASE = "https://va-corporation.github.io/"
LANGS = ["en", "de", "es", "it", "fr", "pl", "uk", "ru", "be", "ka", "hy"]
OG = {"en": "en_US", "de": "de_DE", "es": "es_ES", "it": "it_IT", "fr": "fr_FR", "ru": "ru_RU", "be": "be_BY", "uk": "uk_UA", "pl": "pl_PL", "ka": "ka_GE", "hy": "hy_AM"}
META = {
    "en": ("VA Corporation — AI agents, games & software",
           "VA Corporation builds AI agents, games and software: AI assistants for business, AI video agents, automation, websites and bots."),
    "de": ("VA Corporation — KI-Agenten, Spiele & Software",
           "VA Corporation entwickelt KI-Agenten, Spiele und Software: KI-Assistenten für Unternehmen, KI-Video-Agenten, Automatisierung, Websites und Bots."),
    "es": ("VA Corporation — agentes de IA, juegos y software",
           "VA Corporation crea agentes de IA, juegos y software: asistentes de IA para empresas, agentes de vídeo con IA, automatización, webs y bots."),
    "it": ("VA Corporation — agenti IA, giochi e software",
           "VA Corporation crea agenti IA, giochi e software: assistenti IA per le aziende, agenti video IA, automazione, siti web e bot."),
    "fr": ("VA Corporation — agents IA, jeux et logiciels",
           "VA Corporation crée des agents IA, des jeux et des logiciels : assistants IA pour les entreprises, agents vidéo IA, automatisation, sites web et bots."),
    "ru": ("VA Corporation — AI-агенты, игры и софт",
           "VA Corporation создаёт AI-агентов, игры и софт: AI-ассистенты для бизнеса, AI-видеоагенты, автоматизация, сайты и боты."),
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

def url(l):
    return BASE if l == "en" else f"{BASE}{PATH.get(l, l)}/"

# a data-l span: inner content may contain one level of nested <span>…</span>
SPAN = re.compile(r'<span data-l="(\w+)">((?:[^<]|<span[^>]*>[^<]*</span>|<(?!/?span\b)[^>]*>)*?)</span>')

def build(tpl, lang):
    s = SPAN.sub(lambda m: m.group(0) if m.group(1) == lang else "", tpl)
    s = s.replace('<html lang="en">', f'<html lang="{lang}">', 1)
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

def home(tpl, l, arts, pgs):
    h = build(tpl, l).replace("<!--NEWS-->", news.latest_block(arts, l))
    svc, case = pages.home_links(pgs, l)
    h = h.replace("<!--SVCLINKS-->", svc).replace("<!--CASELINKS-->", case)
    foot = '<nav class="footlinks">' + "".join(
        f'<a href="/{news.prefix(l)}{p["path"]}">{news.e(p["i18n"][l]["h1"])}</a>' for p in pgs if l in p["i18n"]) + \
        f'<a href="/{news.prefix(l)}news/">{news.e(news.UI[l]["news"])}</a><a href="/{news.prefix(l)}videos/">{news.e(videos.UI[l][0])}</a></nav>'
    h = h.replace("<!--FOOTLINKS-->", foot)
    h = h.replace("</head>", pages.faq_ld(h, l) + "\n</head>", 1)
    return h

def main():
    tpl = open("src/site.html", encoding="utf-8").read()
    nentries, arts = news.build_all(LANGS)
    pentries, pgs = pages.build_all(LANGS)
    nentries = pentries + nentries + videos.build_all(LANGS)
    vids = videos.load()
    for l in LANGS:
        out = "index.html" if l == "en" else f"{PATH.get(l, l)}/index.html"
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        open(out, "w", encoding="utf-8").write(home(tpl, l, arts, pgs).replace("<!--REELS-->", videos.home_block(vids, l)))
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
