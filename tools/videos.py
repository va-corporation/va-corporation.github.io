"""Video gallery: videos/data.json (newest first) -> home reels block + /<lang>/videos/ pages with VideoObject schema.

Entry: {"id", "date": "YYYY-MM-DD", "lang", "title", "description", "video": mp4 URL, "cover": jpg URL or "", "duration": seconds}
The reel task prepends a new entry after each published reel and runs tools/build.py.
"""
import json, os
import news

e = news.e
BASE = news.BASE
UI = {
 "en": ("AI videos", "Every reel here was scripted, animated and scored by our AI video agent — new ones appear after each publication.", "All videos"),
 "de": ("KI-Videos", "Jedes Reel hier wurde von unserem KI-Video-Agenten geschrieben, animiert und vertont — neue erscheinen nach jeder Veröffentlichung.", "Alle Videos"),
 "es": ("Vídeos de IA", "Cada reel de esta página lo guionizó, animó y musicalizó nuestro agente de vídeo con IA; los nuevos aparecen tras cada publicación.", "Todos los vídeos"),
 "it": ("Video IA", "Ogni reel qui è stato scritto, animato e musicato dal nostro agente video IA: i nuovi compaiono dopo ogni pubblicazione.", "Tutti i video"),
 "fr": ("Vidéos IA", "Chaque reel ici a été écrit, animé et mis en musique par notre agent vidéo IA ; les nouveaux apparaissent après chaque publication.", "Toutes les vidéos"),
 "pl": ("Wideo AI", "Każdą rolkę tutaj napisał, zanimował i udźwiękowił nasz agent wideo AI — nowe pojawiają się po każdej publikacji.", "Wszystkie filmy"),
 "uk": ("AI-відео", "Кожен рілс тут написав, анімував і озвучив наш AI-відеоагент — нові з'являються після кожної публікації.", "Усі відео"),
 "ru": ("ИИ-видео", "Каждый рилс здесь написал, анимировал и озвучил наш ИИ-видеоагент — новые появляются после каждой публикации.", "Все видео"),
 "be": ("AI-відэа", "Кожны рылс тут напісаў, аніміраваў і агучыў наш AI-відэаагент — новыя з'яўляюцца пасля кожнай публікацыі.", "Усе відэа"),
 "ka": ("AI ვიდეოები", "აქ ყველა რილსი ჩვენმა AI ვიდეო-აგენტმა დაწერა, გააცოცხლა და გაახმოვანა — ახლები ყოველი გამოქვეყნების შემდეგ ჩნდება.", "ყველა ვიდეო"),
 "hy": ("AI վիդեոներ", "Այստեղ յուրաքանչյուր ռիլս գրել, անիմացրել և հնչյունավորել է մեր AI վիդեո գործակալը․ նորերը հայտնվում են յուրաքանչյուր հրապարակումից հետո։", "Բոլոր վիդեոները"),
}
CSS = """
.vgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:18px;margin:26px 0}
.vcard{background:var(--glass);border:1px solid var(--line);border-radius:20px;overflow:hidden}
.vcard video{width:100%;aspect-ratio:9/16;object-fit:cover;display:block;background:#0B1033}
.vcard div{padding:12px 14px}.vcard h2{font-size:15px;margin:0 0 4px;line-height:1.3}.vcard time{color:var(--cyan2);font-size:12px;font-weight:600}
"""


def load():
    try:
        d = json.load(open("videos/data.json", encoding="utf-8"))
    except FileNotFoundError:
        return []
    d.sort(key=lambda v: v["date"], reverse=True)  # stable: same-date order kept as in file
    return d


def ld_video(v, page):
    o = {"@type": "VideoObject", "name": v["title"], "description": v["description"], "uploadDate": v["date"] + "T12:00:00+01:00",
         "contentUrl": v["video"], "embedUrl": page, "duration": f'PT{int(v.get("duration", 12))}S', "inLanguage": v.get("lang", "en"),
         "thumbnailUrl": v["cover"] or BASE + "assets/og.jpg",
         "publisher": {"@type": "Organization", "name": "VA Corporation", "logo": {"@type": "ImageObject", "url": BASE + "assets/logo.png"}}}
    return o


def tag(v, autoplay):
    poster = f' poster="{e(v["cover"])}"' if v.get("cover") else ""
    if autoplay:
        return f'<video src="{e(v["video"])}"{poster} muted loop playsinline autoplay preload="metadata" aria-label="{e(v["title"])}"></video>'
    return f'<video src="{e(v["video"])}"{poster} controls playsinline preload="none" aria-label="{e(v["title"])}"></video>'


def home_block(vids, l):
    if not vids:
        return ""
    t = UI[l]
    return ('<div class="reels">' + "".join(tag(v, True) for v in vids[:3]) + '</div>'
            f'<p style="margin-top:22px"><a class="btn ghost" href="/{news.prefix(l)}videos/">{e(t[2])} →</a></p>')


def build_all(langs):
    vids = load()
    if not vids:
        return []
    alts = [(l, BASE + news.prefix(l) + "videos/") for l in langs]
    entries = []
    for l in langs:
        t = UI[l]
        canon = BASE + news.prefix(l) + "videos/"
        cards = "".join(f'<article class="vcard">{tag(v, False)}<div><h2>{e(v["title"])}</h2><time datetime="{v["date"]}">{news.fmt_date(v["date"], l)}</time></div></article>' for v in vids)
        body = (f'<p class="kicker">VA Corporation</p><h1>{e(t[0])}</h1><p class="lead">{e(t[1])}</p><div class="vgrid">{cards}</div>{news.cta(l)}')
        ld = {"@context": "https://schema.org", "@graph": [ld_video(v, canon) for v in vids[:50]]}
        h = news.page(l, f"{t[0]} — VA Corporation", t[1][:158], canon, alts, body, ld)
        h = h.replace("</style>", CSS + "</style>", 1).replace(f'<a href="{news.index_url(l)}" aria-current="page">', f'<a href="{news.index_url(l)}">', 1)
        out = news.prefix(l) + "videos/index.html"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(h)
        entries.append((canon, vids[0]["date"], alts))
    return entries
