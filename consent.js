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
 *   - Replace the [Lex] banner text below with Lex's approved wording.
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
    // [Lex] Replace this text with Lex's approved banner wording before go-live.
    var p = document.createElement('p');
    p.innerHTML = '[Lex: banner text] We would like to use Google Analytics to measure how this ' +
      'site is used. It sets cookies and loads only if you accept. See the ' +
      '<a href="/datenschutz.html#analytics">privacy notice</a>.';
    b.appendChild(p);

    var accept = document.createElement('button');
    accept.className = 'cc-accept'; accept.type = 'button'; accept.textContent = 'Accept';
    accept.addEventListener('click', function () { writeConsent('granted'); removeBanner(b); loadGA4(); });

    var decline = document.createElement('button');
    decline.className = 'cc-decline'; decline.type = 'button'; decline.textContent = 'Decline';
    decline.addEventListener('click', function () { writeConsent('denied'); removeBanner(b); });

    b.appendChild(accept);
    b.appendChild(decline);
    document.body.appendChild(b);
  }

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
