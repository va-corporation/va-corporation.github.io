# VA Corporation

Website: https://va-corporation.github.io

AI agents · Games · Software

## News / blog (`/news/`)
- One JSON file per article in `news/data/YYYY-MM-DD-<slug>.json` (format documented at the top of `tools/news.py`).
- Text is plain and must be **original writing** (own summary + analysis) with links to the original sources — never copy articles.
- `python3 tools/build.py` regenerates article pages for every language present in `i18n`, the `/news/` index pages, RSS feeds (`<lang>/news/feed.xml`), the "Latest news" block on the home pages and `sitemap.xml`.

## Videos (`/videos/`)
- `videos/data.json` — newest first; format at the top of `tools/videos.py`. The daily reel task prepends each published reel (media hosted in benzogamesltd-ops/va-media via GitHub Pages) and runs `tools/build.py`.
- The home page shows the 3 newest reels; `/<lang>/videos/` lists all with VideoObject schema.

## App (PWA)
- The site installs as a phone app: `manifest.webmanifest`, `sw.js`, `offline.html`, icons in `assets/app/`.
- The manifest link and service-worker registration live in `src/site.html` and `tools/news.py` (`page()`), so `tools/build.py` keeps them on every page.
- `sw.js` loads pages network-first (visitors always get the latest site) and only falls back to cache offline. Bump `VERSION` in `sw.js` to clear old caches.
