# VA Corporation

Website: https://va-corporation.github.io

AI agents · Games · Software

## News / blog (`/news/`)
- One JSON file per article in `news/data/YYYY-MM-DD-<slug>.json` (format documented at the top of `tools/news.py`).
- Text is plain and must be **original writing** (own summary + analysis) with links to the original sources — never copy articles.
- `python3 tools/build.py` regenerates article pages for every language present in `i18n`, the `/news/` index pages, RSS feeds (`<lang>/news/feed.xml`), the "Latest news" block on the home pages and `sitemap.xml`.
