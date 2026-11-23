/* VA Corporation — service worker for the installable app (PWA).
   Pages: network first and revalidated with the server (no 10-minute HTTP cache), so the app always shows the latest version;
   the cached copy is used only when there is no connection.
   Same-origin static files (fonts, images, icons): served from cache, refreshed in the background.
   Other sites (videos, Telegram, Instagram) and non-GET requests are not touched. */
const VERSION = 'va-v2';
const PAGES = VERSION + '-pages';
const STATIC = VERSION + '-static';
const OFFLINE = '/offline.html';
const PRECACHE = ['/', OFFLINE, '/assets/app/icon-192.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(STATIC).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || req.headers.has('range')) return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req, { cache: 'no-cache' })
        .then((res) => {
          if (res.ok) { const copy = res.clone(); caches.open(PAGES).then((c) => c.put(req, copy)); }
          return res;
        })
        .catch(() => caches.match(req).then((hit) => hit || caches.match(OFFLINE)))
    );
    return;
  }

  // Only cache static files; data and feeds (json, xml) always come from the network.
  if (!/\.(png|jpe?g|webp|gif|svg|ico|woff2?|css|js)$/i.test(url.pathname) || url.pathname === '/sw.js') return;
  e.respondWith(
    caches.open(STATIC).then((c) =>
      c.match(req).then((hit) => {
        const net = fetch(req)
          .then((res) => { if (res.ok) c.put(req, res.clone()); return res; })
          .catch(() => hit);
        return hit || net;
      })
    )
  );
});
