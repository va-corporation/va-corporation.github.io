"""News / blog generator for va-corporation.github.io.

Articles live in news/data/*.json:
{
  "date": "2026-11-22",
  "slug": "short-latin-slug",
  "sources": [{"name": "OpenAI", "title": "Introducing ...", "url": "https://..."}],
  "i18n": {
     "en": {"title": "...", "desc": "1-2 sentence summary (<160 chars)",
            "body": [{"h": "Heading"}, {"p": "Paragraph text"}, ...]},
     "de": {...}, ...   # any subset of LANGS; missing languages are simply skipped
  }
}
Text is plain (HTML is escaped). Run tools/build.py — it calls this module.
"""
import json, os, glob, html, datetime

BASE = "https://va-corporation.github.io/"
PATH = {"be": "by", "uk": "ua", "ka": "ge", "hy": "am"}
OG = {"en": "en_US", "de": "de_DE", "es": "es_ES", "it": "it_IT", "fr": "fr_FR", "ru": "ru_RU", "be": "be_BY",
      "uk": "uk_UA", "pl": "pl_PL", "ka": "ka_GE", "hy": "hy_AM"}

UI = {
 "en": dict(news="News", head="AI news & insights", intro="A short daily digest of what matters in artificial intelligence, AI agents and tech — written by our team in plain language, with links to the original sources.", sources="Sources", read="Read", all="All news", home="Home", latest="Latest news", cta_h="Want an AI agent for your business?", cta_p="We build AI agents, games and software. Tell us about your task.", cta="Write to us", mon=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]),
 "de": dict(news="News", head="KI-News & Einblicke", intro="Ein kurzer täglicher Überblick über das Wichtigste aus künstlicher Intelligenz, KI-Agenten und Technologie — verständlich geschrieben von unserem Team, mit Links zu den Originalquellen.", sources="Quellen", read="Lesen", all="Alle News", home="Startseite", latest="Neueste News", cta_h="Ein KI-Agent für Ihr Unternehmen?", cta_p="Wir entwickeln KI-Agenten, Spiele und Software. Erzählen Sie uns von Ihrer Aufgabe.", cta="Schreiben Sie uns"),
 "es": dict(news="Noticias", head="Noticias e ideas sobre IA", intro="Un breve resumen diario de lo más importante en inteligencia artificial, agentes de IA y tecnología, escrito por nuestro equipo en lenguaje claro y con enlaces a las fuentes originales.", sources="Fuentes", read="Leer", all="Todas las noticias", home="Inicio", latest="Últimas noticias", cta_h="¿Un agente de IA para tu negocio?", cta_p="Creamos agentes de IA, juegos y software. Cuéntanos tu proyecto.", cta="Escríbenos"),
 "it": dict(news="Notizie", head="Notizie e approfondimenti sull'IA", intro="Un breve riepilogo quotidiano di ciò che conta nell'intelligenza artificiale, negli agenti IA e nella tecnologia, scritto dal nostro team in modo chiaro e con i link alle fonti originali.", sources="Fonti", read="Leggi", all="Tutte le notizie", home="Home", latest="Ultime notizie", cta_h="Un agente IA per la tua azienda?", cta_p="Creiamo agenti IA, giochi e software. Raccontaci la tua esigenza.", cta="Scrivici"),
 "fr": dict(news="Actualités", head="Actualités et analyses IA", intro="Un bref résumé quotidien de l'essentiel de l'intelligence artificielle, des agents IA et de la tech, rédigé simplement par notre équipe, avec des liens vers les sources originales.", sources="Sources", read="Lire", all="Toutes les actualités", home="Accueil", latest="Dernières actualités", cta_h="Un agent IA pour votre entreprise ?", cta_p="Nous créons des agents IA, des jeux et des logiciels. Parlez-nous de votre projet.", cta="Écrivez-nous"),
 "pl": dict(news="Aktualności", head="Wiadomości i analizy AI", intro="Krótki codzienny przegląd najważniejszych wydarzeń ze świata sztucznej inteligencji, agentów AI i technologii — napisany prostym językiem przez nasz zespół, z linkami do oryginalnych źródeł.", sources="Źródła", read="Czytaj", all="Wszystkie wiadomości", home="Strona główna", latest="Najnowsze wiadomości", cta_h="Agent AI dla Twojej firmy?", cta_p="Tworzymy agentów AI, gry i oprogramowanie. Opowiedz nam o swoim zadaniu.", cta="Napisz do nas"),
 "uk": dict(news="Новини", head="Новини та огляди AI", intro="Короткий щоденний огляд найважливішого у світі штучного інтелекту, AI-агентів і технологій — простою мовою від нашої команди, з посиланнями на першоджерела.", sources="Джерела", read="Читати", all="Усі новини", home="Головна", latest="Останні новини", cta_h="Потрібен AI-агент для бізнесу?", cta_p="Ми створюємо AI-агентів, ігри та софт. Розкажіть про вашу задачу.", cta="Написати нам"),
 "ru": dict(news="Новости", head="Новости и обзоры ИИ", intro="Короткий ежедневный обзор самого важного в мире искусственного интеллекта, ИИ-агентов и технологий — простым языком от нашей команды, со ссылками на первоисточники.", sources="Источники", read="Читать", all="Все новости", home="Главная", latest="Последние новости", cta_h="Нужен ИИ-агент для бизнеса?", cta_p="Мы создаём ИИ-агентов, игры и софт. Расскажите о вашей задаче.", cta="Написать нам"),
 "be": dict(news="Навіны", head="Навіны і агляды ШІ", intro="Кароткі штодзённы агляд самага важнага ў свеце штучнага інтэлекту, AI-агентаў і тэхналогій — простай мовай ад нашай каманды, са спасылкамі на першакрыніцы.", sources="Крыніцы", read="Чытаць", all="Усе навіны", home="Галоўная", latest="Апошнія навіны", cta_h="Патрэбны AI-агент для бізнесу?", cta_p="Мы ствараем AI-агентаў, гульні і софт. Раскажыце пра вашу задачу.", cta="Напісаць нам"),
 "ka": dict(news="სიახლეები", head="AI სიახლეები და მიმოხილვები", intro="მოკლე ყოველდღიური მიმოხილვა ხელოვნური ინტელექტის, AI აგენტებისა და ტექნოლოგიების ყველაზე მნიშვნელოვან ამბებზე — მარტივი ენით, ჩვენი გუნდისგან, პირველწყაროების ბმულებით.", sources="წყაროები", read="წაკითხვა", all="ყველა სიახლე", home="მთავარი", latest="უახლესი სიახლეები", cta_h="გჭირდებათ AI აგენტი ბიზნესისთვის?", cta_p="ვქმნით AI აგენტებს, თამაშებს და პროგრამებს. გვიამბეთ თქვენი ამოცანის შესახებ.", cta="მოგვწერეთ"),
 "hy": dict(news="Նորություններ", head="AI նորություններ և ակնարկներ", intro="Կարճ ամենօրյա ակնարկ արհեստական բանականության, AI գործակալների և տեխնոլոգիաների ամենակարևոր իրադարձությունների մասին՝ պարզ լեզվով, մեր թիմից, սկզբնաղբյուրների հղումներով։", sources="Աղբյուրներ", read="Կարդալ", all="Բոլոր նորությունները", home="Գլխավոր", latest="Վերջին նորություններ", cta_h="AI գործակալ ձեր բիզնեսի համար՞", cta_p="Ստեղծում ենք AI գործակալներ, խաղեր և ծրագրեր։ Պատմեք ձեր խնդրի մասին։", cta="Գրեք մեզ"),
}
LANG_NAME = {"en": "EN", "de": "DE", "es": "ES", "it": "IT", "fr": "FR", "pl": "PL", "uk": "UA", "ru": "RU", "be": "BY", "ka": "GE", "hy": "AM"}

e = lambda s: html.escape(str(s), quote=True)


def prefix(l):
    return "" if l == "en" else PATH.get(l, l) + "/"


def home_url(l):
    return BASE + prefix(l)


def index_url(l):
    return BASE + prefix(l) + "news/"


def art_path(a, l):
    return f"{prefix(l)}news/{a['date']}-{a['slug']}/"


def fmt_date(d, l):
    y, m, dd = d.split("-")
    if l == "en":
        return f"{UI['en']['mon'][int(m) - 1]} {int(dd)}, {y}"
    return f"{dd}.{m}.{y}"


def load():
    arts = []
    for f in glob.glob("news/data/*.json"):
        a = json.load(open(f, encoding="utf-8"))
        arts.append(a)
    arts.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    return arts


CSS = """@font-face{font-family:Montserrat;src:url(/assets/fonts/montserrat-var.woff) format("woff");font-weight:100 900;font-display:swap}
@font-face{font-family:Inter;src:url(/assets/fonts/inter-regular.woff) format("woff");font-weight:400;font-display:swap}
@font-face{font-family:Inter;src:url(/assets/fonts/inter-semibold.woff) format("woff");font-weight:600;font-display:swap}
@font-face{font-family:Inter;src:url(/assets/fonts/inter-bold.woff) format("woff");font-weight:700;font-display:swap}
:root{--bg:#070A22;--cyan:#22D3EE;--cyan2:#67E8F9;--gold:#FACC15;--amber:#FFC15E;--text:#F2F5FA;--muted:#AAB4D4;--glass:rgba(255,255,255,.06);--line:rgba(255,255,255,.14)}
*{box-sizing:border-box}html,body{margin:0}
body{font-family:Inter,"Noto Sans Georgian","Noto Sans Armenian",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--text);line-height:1.65;background:radial-gradient(1200px 700px at 85% -10%,rgba(34,211,238,.16),transparent 60%),radial-gradient(900px 600px at -10% 30%,rgba(30,42,120,.55),transparent 60%),radial-gradient(800px 500px at 50% 120%,rgba(255,193,94,.10),transparent 60%),var(--bg);min-height:100vh}
a{color:var(--cyan2);text-decoration:none}a:hover{color:#fff}
.wrap{max-width:860px;margin:0 auto;padding:0 22px}
header{border-bottom:1px solid var(--line);background:rgba(7,10,34,.7);backdrop-filter:blur(10px);position:sticky;top:0;z-index:5}
.nav{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:68px;flex-wrap:wrap}
.logo{display:flex;align-items:center;gap:12px;color:#fff;font:800 18px Montserrat,Inter,sans-serif}
.sun{width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 42% 35%,#FFF7DE 0%,#FFC15E 48%,#F07A1A 100%);box-shadow:0 0 22px 5px rgba(255,190,90,.4);display:flex;align-items:center;justify-content:center;color:#3A1A00;font-weight:800;font-size:13px}
.links{display:flex;gap:18px;font-weight:600;font-size:15px}.links a{color:var(--muted)}.links a:hover,.links a[aria-current]{color:#fff}
h1,h2,h3{font-family:Montserrat,Inter,"Noto Sans Georgian","Noto Sans Armenian",sans-serif;line-height:1.2}
h1{font-size:clamp(30px,5vw,46px);margin:46px 0 14px}
.kicker{color:var(--cyan);font:700 13px Montserrat,Inter,sans-serif;letter-spacing:.18em;text-transform:uppercase;margin-top:42px}
.lead{color:var(--muted);font-size:18px;max-width:720px}
.card{display:block;background:var(--glass);border:1px solid var(--line);border-radius:20px;padding:24px 26px;margin:18px 0;color:var(--text);transition:transform .25s,border-color .25s}
.card:hover{transform:translateY(-3px);border-color:rgba(103,232,249,.55);color:var(--text)}
.card time{color:var(--cyan2);font-size:14px;font-weight:600}.card h2{font-size:22px;margin:6px 0 8px}.card p{color:var(--muted);margin:0}
.more{display:inline-block;margin-top:12px;color:var(--gold);font-weight:700}
article{padding-bottom:20px}article time{color:var(--cyan2);font-weight:600}
article h2{font-size:24px;margin:34px 0 10px}article p{font-size:17.5px;margin:0 0 16px}
.src{margin-top:34px;padding:20px 24px;border:1px solid var(--line);border-radius:18px;background:var(--glass)}
.src h2{font-size:18px;margin:0 0 10px}.src ul{margin:0;padding-left:18px}.src li{margin:6px 0}
.cta{margin:40px 0;padding:30px;border-radius:24px;background:linear-gradient(135deg,rgba(34,211,238,.14),rgba(250,204,21,.12));border:1px solid rgba(250,204,21,.35)}
.cta h2{margin:0 0 8px;font-size:24px}.cta p{color:var(--muted);margin:0 0 18px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:14px 24px;border-radius:999px;font-weight:800;background:linear-gradient(90deg,var(--gold),var(--amber));color:#0B1033;min-height:48px}.btn:hover{color:#0B1033;filter:brightness(1.08)}
.langs{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0 0}.langs a{padding:6px 12px;border:1px solid var(--line);border-radius:999px;font-size:13px;font-weight:700;color:var(--muted)}.langs a[aria-current]{background:var(--cyan);color:#06122B;border-color:var(--cyan)}
footer{border-top:1px solid var(--line);margin-top:50px;padding:26px 0;color:var(--muted);font-size:14px}footer .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:10px}
@media(max-width:600px){.links{gap:14px;font-size:14px}.logo{font-size:16px}article p{font-size:17px}}
"""


def fit(text, n):
    """Cut text to at most n characters at a word boundary (SEO snippet length)."""
    if len(text) <= n:
        return text
    cut = text[:n - 1].rsplit(" ", 1)[0].rstrip(" ,.;:—-")
    return cut + "…"


def page(lang, title, desc, canon, alternates, body, ld, ogtype="website"):
    u = UI[lang]
    for suf in (" — VA Corporation", " | VA Corporation"):  # drop the brand suffix when the title is too long
        if len(title) > 65 and title.endswith(suf):
            title = title[: -len(suf)]
    desc = fit(desc, 160)
    alt = "".join(f'\n<link rel="alternate" hreflang="{l}" href="{h}">' for l, h in alternates)
    if alternates:
        alt += f'\n<link rel="alternate" hreflang="x-default" href="{dict(alternates).get("en", alternates[0][1])}">'
    feed = f'{index_url(lang)}feed.xml'
    return f"""<!DOCTYPE html>
<html lang="{lang}" translate="no">
<head>
<meta charset="utf-8"><meta name="google" content="notranslate">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">{alt}
<link rel="alternate" type="application/rss+xml" title="VA Corporation — {e(u['news'])}" href="{feed}">
<meta property="og:type" content="{ogtype}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}assets/og.jpg">
<meta property="og:locale" content="{OG[lang]}">
<meta property="og:site_name" content="VA Corporation">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#070A22">
<link rel="icon" href="/assets/logo.png">
<link rel="apple-touch-icon" href="/assets/logo.png">
<link rel="manifest" href="/manifest.webmanifest">
<script>if('serviceWorker' in navigator)addEventListener('load',function(){{navigator.serviceWorker.register('/sw.js').catch(function(){{}})}})</script>
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header><div class="wrap nav">
 <a class="logo notranslate" translate="no" href="{home_url(lang)}"><span class="sun notranslate" translate="no">VA</span>VA Corporation</a>
 <nav class="links"><a href="{home_url(lang)}">{e(u['home'])}</a><a href="{index_url(lang)}" aria-current="page">{e(u['news'])}</a><a href="{home_url(lang)}#contact">{e(u['cta'])}</a></nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap"><span>© {datetime.date.today().year} VA Corporation</span><span>AI agents · Games · Software</span><span><a href="/{"" if lang == "en" else (prefix(lang) if lang in ("de", "ru") else "")}terms/">Terms</a> · <a href="/{"" if lang == "en" else (prefix(lang) if lang in ("de", "ru") else "")}privacy/">Privacy</a></span></div></footer>
<script src="/track.js?v=2" defer></script></body>
</html>
"""


def cta(lang):
    u = UI[lang]
    return f'<section class="cta"><h2>{e(u["cta_h"])}</h2><p>{e(u["cta_p"])}</p><a class="btn" href="https://wa.me/34641387122" rel="noopener" style="background:#1FA855;color:#fff">WhatsApp →</a> &nbsp; <a href="https://t.me/vladimiramelchenko33" rel="noopener">Telegram</a> &nbsp;·&nbsp; <a href="{home_url(lang)}#contact">{e(u["cta"])}</a></section>'


def build_all(langs):
    """Writes all news pages; returns sitemap entries [(loc, lastmod, [(hreflang, href)])]."""
    arts = load()
    entries = []
    # article pages
    for a in arts:
        have = [l for l in langs if l in a["i18n"]]
        alts = [(l, BASE + art_path(a, l)) for l in have]
        for l in have:
            t = a["i18n"][l]
            blocks = "".join(f"<h2>{e(b['h'])}</h2>" if "h" in b else f"<p>{e(b['p'])}</p>" for b in t["body"])
            src = "".join(f'<li><a href="{e(s["url"])}" rel="noopener nofollow" target="_blank">{e(s.get("title") or s["name"])}</a> — {e(s["name"])}</li>' for s in a.get("sources", []))
            switch = '<nav class="langs" aria-label="Language">' + "".join(
                f'<a href="/{art_path(a, o)}" hreflang="{o}"{" aria-current=\"true\"" if o == l else ""}>{LANG_NAME[o]}</a>' for o in have) + "</nav>"
            body = (f'<article><p class="kicker"><a href="{index_url(l)}">{e(UI[l]["news"])}</a></p>'
                    f'<h1>{e(t["title"])}</h1><time datetime="{a["date"]}">{fmt_date(a["date"], l)}</time>'
                    f'<p class="lead" style="margin-top:14px">{e(t["desc"])}</p>{blocks}'
                    + (f'<section class="src"><h2>{e(UI[l]["sources"])}</h2><ul>{src}</ul></section>' if src else "")
                    + f'{switch}</article>{cta(l)}')
            canon = BASE + art_path(a, l)
            ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": t["title"][:110], "description": t["desc"],
                  "datePublished": a["date"], "dateModified": a.get("updated", a["date"]), "inLanguage": l, "url": canon,
                  "mainEntityOfPage": canon, "image": BASE + "assets/og.jpg",
                  "author": {"@type": "Organization", "name": "VA Corporation", "url": BASE},
                  "publisher": {"@type": "Organization", "name": "VA Corporation", "logo": {"@type": "ImageObject", "url": BASE + "assets/logo.png"}}}
            out = art_path(a, l) + "index.html"
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "w", encoding="utf-8").write(page(l, f'{t["title"]} — VA Corporation', t["desc"], canon, alts, body, ld, "article"))
            entries.append((canon, a.get("updated", a["date"]), alts))
    # index pages + RSS
    today = datetime.date.today().isoformat()
    ialts = [(l, index_url(l)) for l in langs]
    for l in langs:
        u = UI[l]
        mine = [a for a in arts if l in a["i18n"]]
        cards = "".join(
            f'<a class="card" href="/{art_path(a, l)}"><time datetime="{a["date"]}">{fmt_date(a["date"], l)}</time>'
            f'<h2>{e(a["i18n"][l]["title"])}</h2><p>{e(a["i18n"][l]["desc"])}</p><span class="more">{e(u["read"])} →</span></a>' for a in mine)
        body = f'<p class="kicker">VA Corporation · {e(u["news"])}</p><h1>{e(u["head"])}</h1><p class="lead">{e(u["intro"])}</p>{cards}{cta(l)}'
        ld = {"@context": "https://schema.org", "@type": "Blog", "name": f'VA Corporation — {u["head"]}', "url": index_url(l), "inLanguage": l,
              "blogPost": [{"@type": "BlogPosting", "headline": a["i18n"][l]["title"][:110], "url": BASE + art_path(a, l), "datePublished": a["date"]} for a in mine[:20]]}
        out = prefix(l) + "news/index.html"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(page(l, f'{u["head"]} — VA Corporation', u["intro"][:158], index_url(l), ialts, body, ld))
        entries.append((index_url(l), mine[0]["date"] if mine else today, ialts))
        items = "".join(
            f'<item><title>{e(a["i18n"][l]["title"])}</title><link>{BASE + art_path(a, l)}</link><guid>{BASE + art_path(a, l)}</guid>'
            f'<pubDate>{datetime.datetime.strptime(a["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 08:00:00 +0000")}</pubDate>'
            f'<description>{e(a["i18n"][l]["desc"])}</description></item>' for a in mine[:30])
        open(prefix(l) + "news/feed.xml", "w", encoding="utf-8").write(
            f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>VA Corporation — {e(u["head"])}</title>'
            f'<link>{index_url(l)}</link><description>{e(u["intro"])}</description><language>{l}</language>{items}</channel></rss>\n')
    return entries, arts


def latest_block(arts, lang, n=3):
    """HTML for the 'Latest news' section on the home page."""
    u = UI[lang]
    mine = [a for a in arts if lang in a["i18n"]][:n]
    if not mine:
        return ""
    cards = "".join(
        f'<a class="ncard" href="/{art_path(a, lang)}"><time datetime="{a["date"]}">{fmt_date(a["date"], lang)}</time>'
        f'<h3>{e(a["i18n"][lang]["title"])}</h3><p>{e(a["i18n"][lang]["desc"])}</p><span>{e(u["read"])} →</span></a>' for a in mine)
    return (f'<section id="news"><div class="wrap"><div class="kicker">{e(u["news"])}</div><h2>{e(u["latest"])}</h2>'
            f'<div class="ngrid">{cards}</div><p style="margin-top:22px"><a class="btn ghost" href="/{prefix(lang)}news/">{e(u["all"])} →</a></p></div></section>')
