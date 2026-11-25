/* VA Corporation — retargeting (Meta Pixel + Google tag) with GDPR consent.
   Nothing loads and no banner shows until an ID below is filled in.
   After the visitor clicks "Accept", the Meta Pixel and/or Google tag load; "Decline" keeps the site tracker-free.
   The choice is remembered in localStorage ("va-consent"). */
(function () {
  var CFG = {
    metaPixel: '',      // Meta (Facebook/Instagram) Pixel ID, e.g. '123456789012345'
    googleTag: ''       // Google Ads / GA4 tag ID, e.g. 'AW-123456789' or 'G-XXXXXXX'
  };
  if (!CFG.metaPixel && !CFG.googleTag) return;

  var KEY = 'va-consent';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function load() {
    if (CFG.metaPixel) {
      !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments) };
        if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0;
        t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', CFG.metaPixel); fbq('track', 'PageView');
      document.addEventListener('click', function (ev) {
        var a = ev.target.closest && ev.target.closest('a[href*="wa.me"],a[href*="t.me"]');
        if (a) fbq('track', 'Contact');
      });
    }
    if (CFG.googleTag) {
      var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + CFG.googleTag;
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
      gtag('js', new Date()); gtag('config', CFG.googleTag);
    }
  }

  var c = get();
  if (c === 'yes') { load(); return; }
  if (c === 'no') return;

  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var TX = {
    en: ['We use cookies to show you our offers on other sites (Meta, Google). OK?', 'Accept', 'Decline', 'Privacy'],
    de: ['Wir nutzen Cookies, um Ihnen unsere Angebote auf anderen Seiten (Meta, Google) zu zeigen. Einverstanden?', 'Akzeptieren', 'Ablehnen', 'Datenschutz'],
    ru: ['Мы используем cookie, чтобы показывать вам наши предложения на других сайтах (Meta, Google). Согласны?', 'Принять', 'Отклонить', 'Конфиденциальность']
  }[L] || null;
  if (!TX) TX = ['We use cookies to show you our offers on other sites (Meta, Google). OK?', 'Accept', 'Decline', 'Privacy'];
  var priv = L === 'de' ? '/de/privacy/' : L === 'ru' ? '/ru/privacy/' : '/privacy/';

  var b = document.createElement('div');
  b.setAttribute('role', 'dialog'); b.setAttribute('aria-label', 'Cookies');
  b.style.cssText = 'position:fixed;left:12px;right:12px;bottom:12px;z-index:9999;max-width:560px;margin:auto;background:#0B1033;color:#F2F5FA;border:1px solid rgba(125,211,252,.4);border-radius:16px;padding:14px 16px;font:14px/1.4 Inter,system-ui,sans-serif;box-shadow:0 10px 40px rgba(0,0,0,.4)';
  b.innerHTML = '<div style="margin-bottom:10px"></div><div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center"><button data-a="yes" style="background:#FFC15E;color:#1a1200;border:0;border-radius:10px;padding:9px 16px;font-weight:700;cursor:pointer"></button><button data-a="no" style="background:transparent;color:#F2F5FA;border:1px solid rgba(242,245,250,.4);border-radius:10px;padding:9px 16px;cursor:pointer"></button><a style="color:#7DD3FC;margin-left:auto"></a></div>';
  b.children[0].textContent = TX[0];
  b.querySelector('[data-a="yes"]').textContent = TX[1];
  b.querySelector('[data-a="no"]').textContent = TX[2];
  var a = b.querySelector('a'); a.textContent = TX[3]; a.href = priv;
  b.addEventListener('click', function (ev) {
    var v = ev.target.getAttribute && ev.target.getAttribute('data-a');
    if (!v) return; set(v); b.remove(); if (v === 'yes') load();
  });
  (document.body ? Promise.resolve() : new Promise(function (r) { addEventListener('DOMContentLoaded', r); })).then(function () { document.body.appendChild(b); });
})();
