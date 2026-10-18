/*
 * Cookie-consent banner + Google Analytics 4 loader for the Grid Bot trade site.
 *
 * ARMED 2026-10-18 on Paul's "install GA4" with measurement id G-XG7R0ZNQ4R (a GA4
 * measurement id is public in page source). Still DARK because this branch is UNMERGED:
 * it goes live only when the branch is merged + deployed, which waits for Lex's banner
 * text and the Datenschutz GA4 section (board task #362). If GA4_ID is emptied, this file
 * does NOTHING: no banner, no cookie, no network call.
 *
 * Compliance (TTDSG section 25 + GDPR): GA4 sets cookies, so it loads ONLY after the visitor
 * clicks Accept. Declining (or ignoring) the banner loads nothing. The choice is stored in
 * localStorage (strictly necessary, not a cookie) so the banner is not shown again.
 *
 * STILL TO DO before this branch is merged (do NOT invent these -- see README-ga4.md):
 *   - Add Lex's GA4 section to datenschutz.html (anchor id="analytics"), add the
 *     <script src="/consent.js" defer></script> include to the home page (index.php after the
 *     Brevo branch merges) and datenschutz.html, and reword their footer line, in the same merge.
 */
(function () {
  'use strict';

  // Public GA4 measurement id. Armed on "install GA4". Empty = inert.
  var GA4_ID = 'G-XG7R0ZNQ4R';

  // Do nothing at all unless a real measurement id is present.
  if (!/^G-[A-Z0-9]{6,}$/.test(GA4_ID)) { return; }

  var STORE_KEY = 'ga_consent'; // 'granted' | 'denied'

  function readConsent() {
    try { return localStorage.getItem(STORE_KEY); } catch (e) { return null; }
  }
  function writeConsent(v) {
    try { localStorage.setItem(STORE_KEY, v); } catch (e) {}
  }

  function loadGA4() {
    if (window.__ga4_loaded) { return; }
    window.__ga4_loaded = true;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA4_ID);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    // GA4 anonymises IP by default; keep Google Signals and ad personalisation off.
    gtag('config', GA4_ID, {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
  }

  function removeBanner(b) { if (b && b.parentNode) { b.parentNode.removeChild(b); } }

  function showBanner() {
    var style = document.createElement('style');
    style.textContent =
      '.cc-banner{position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#111;color:#fff;' +
      'padding:16px;font:14px/1.5 system-ui,-apple-system,sans-serif;display:flex;flex-wrap:wrap;' +
      'gap:12px;align-items:center;justify-content:center}' +
      '.cc-banner p{margin:0;max-width:60ch}' +
      '.cc-banner button{border:0;border-radius:6px;padding:8px 16px;font:inherit;cursor:pointer}' +
      '.cc-accept{background:#4ade80;color:#063}.cc-decline{background:#333;color:#fff}' +
      '.cc-banner a{color:#9cf}';
    document.head.appendChild(style);

    var b = document.createElement('div');
    b.className = 'cc-banner';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', 'Cookie consent');
    // Banner wording: Lex, Agora #362, 2026-10-18 (EN first because the site is English; DE below).
    var p = document.createElement('p');
    p.innerHTML = '<strong>Cookie notice \u2014 Analytics (Google Analytics)</strong><br>' +
      'This website uses Google Analytics (GA4) to understand how visitors use our site. With your consent, ' +
      'information (cookies) is stored on and read from your device, and your data is processed into anonymised ' +
      'usage statistics. Legal bases: Art. 6 (1)(a) GDPR and \u00a7 25 (1) TTDSG. You can withdraw your consent at any ' +
      'time with effect for the future, e.g. via this banner. ' +
      '<a href="/datenschutz.html#analytics">Learn more in the privacy notice</a>.<br>' +
      '<span lang="de"><strong>Cookie-Hinweis \u2014 Analyse (Google Analytics)</strong><br>' +
      'Diese Website verwendet Google Analytics (GA4), um zu verstehen, wie Besucherinnen und Besucher unsere Website ' +
      'nutzen. Mit Ihrer Einwilligung werden Informationen (Cookies) auf Ihrem Ger\u00e4t gespeichert und ausgelesen und ' +
      'Ihre Daten zu anonymisierten Nutzungsstatistiken verarbeitet. Rechtsgrundlagen sind Art. 6 Abs. 1 lit. a DSGVO ' +
      'und \u00a7 25 Abs. 1 TTDSG. Sie k\u00f6nnen Ihre Einwilligung jederzeit mit Wirkung f\u00fcr die Zukunft widerrufen, ' +
      'z.\u00a0B. \u00fcber dieses Banner. <a href="/datenschutz.html#analytics">Mehr erfahren in der Datenschutzerkl\u00e4rung</a>.</span>';
    b.appendChild(p);

    var accept = document.createElement('button');
    accept.className = 'cc-accept'; accept.type = 'button'; accept.textContent = 'Accept / Zustimmen';
    accept.addEventListener('click', function () { writeConsent('granted'); removeBanner(b); loadGA4(); });

    var decline = document.createElement('button');
    decline.className = 'cc-decline'; decline.type = 'button'; decline.textContent = 'Decline / Ablehnen';
    decline.addEventListener('click', function () { writeConsent('denied'); removeBanner(b); });

    b.appendChild(accept);
    b.appendChild(decline);
    document.body.appendChild(b);
  }

  // Re-open link in the footer, so consent can be changed on every page (Lex wiring note, #362).
  function addReopenLink() {
    var f = document.querySelector('footer .wrap p:last-child') || document.querySelector('footer');
    if (!f || document.getElementById('cc-reopen')) { return; }
    var a = document.createElement('a');
    a.id = 'cc-reopen'; a.href = '#'; a.textContent = 'Cookie settings / Cookie-Einstellungen';
    a.addEventListener('click', function (ev) { ev.preventDefault(); if (!document.querySelector('.cc-banner')) { showBanner(); } });
    f.appendChild(document.createTextNode(' \u00b7 ')); f.appendChild(a);
  }
  if (document.body) { addReopenLink(); } else { document.addEventListener('DOMContentLoaded', addReopenLink); }

  var prior = readConsent();
  if (prior === 'granted') {
    loadGA4();
  } else if (prior === 'denied') {
    // respect the refusal; load nothing
  } else if (document.body) {
    showBanner();
  } else {
    document.addEventListener('DOMContentLoaded', showBanner);
  }
})();
