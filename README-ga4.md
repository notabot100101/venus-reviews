# GA4 + consent banner — PREPARED, NOT INSTALLED

Analytics decision (Paul, 18 Oct 2026): Hostinger server stats now; GA4 prepared dark; Plausible
parked. Design: /mnt/project-files/ads/paid-ads-readiness-2026-10-18.md section 9.

This branch adds the consent-gated Google Analytics 4 loader as a single self-contained file,
`consent.js`. It is **inert**: with no measurement id set it shows no banner, sets no cookie and
makes no network call, so the site keeps its "no cookies, no tracking" promise until it is
deliberately armed. Kept on its own branch, separate from the Brevo signup commits, so the Brevo
merge is not held up.

## What is built
- `consent.js`: a bottom-of-page consent banner (Accept / Decline) that loads GA4 (gtag) ONLY after
  the visitor clicks Accept (TTDSG §25 + GDPR). Decline or ignore loads nothing. The choice is stored
  in localStorage, not a cookie. GA4 is configured with `anonymize_ip` and Google Signals / ad
  personalisation off. The measurement id is a placeholder (`GA4_ID` at the top of the file).

## To activate — only on Paul's explicit word "install GA4"
Do all of these in ONE commit, then merge + deploy:
1. Paul creates the GA4 property for trade.ultramarine963.com, accepts Google's Data Processing
   Terms in his Google account, and gives his measurement id (`G-XXXXXXXXXX`) in the ads thread.
2. Paste that id into `GA4_ID` at the top of `consent.js`.
3. Replace the `[Lex: banner text]` string in `consent.js` with Lex's approved banner wording.
4. Add Lex's GA4 section to `datenschutz.html` (give it `id="analytics"` to match the banner link)
   and reword the footer "No cookies, no tracking." line on every page.
5. Add `<script src="/consent.js" defer></script>` to the `<head>` of every page:
   the home page (the Brevo signup branch renames `index.html` -> `index.php`; add it to whichever
   is current after that branch merges), `results/index.html`, `method.html`, `offer.html`,
   `faq.html`, `datenschutz.html`, `impressum.html`.

Nothing here goes live without Paul's specific word "install GA4".
