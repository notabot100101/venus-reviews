# GA4 + consent banner — ARMED, NOT YET MERGED

Analytics decision (Paul, 18 Oct 2026): Hostinger server stats now; GA4 prepared then installed on
his word; Plausible parked. Design: /mnt/project-files/ads/paid-ads-readiness-2026-10-18.md section 9.

`consent.js` is a single self-contained, consent-gated Google Analytics 4 loader. On 18 Oct Paul said
"install GA4" and gave the measurement id **G-XG7R0ZNQ4R**, so it is now armed. It is still DARK because
this branch is UNMERGED; merge + deploy is the only go-live action, and it waits for Lex's text. Kept
separate from the Brevo signup commits so the Brevo merge is not held up.

## What is built and armed
- `consent.js`: a bottom-of-page Accept / Decline banner that loads GA4 (gtag) ONLY after the visitor
  clicks Accept (TTDSG §25 + GDPR). Decline or ignore loads nothing. The choice is stored in
  localStorage, not a cookie. GA4 is configured with `anonymize_ip` and Google Signals / ad
  personalisation off. `GA4_ID` is set to G-XG7R0ZNQ4R (emptying it makes the file inert again).
- Include `<script src="/consent.js" defer></script>` and the footer line "No tracking without your
  consent." added to: `method.html`, `faq.html`, `offer.html`, `impressum.html`, `results/index.html`.

## Still to do before merge (board task #362; Lex via the ads thread)
1. Replace the `[Lex: banner text]` string in `consent.js` with Lex's approved banner wording.
2. Add Lex's GA4 section to `datenschutz.html` with `id="analytics"` (matches the banner link).
3. Add the `consent.js` include + footer reword to the two pages deferred here because the Brevo
   signup branch also changes them: the home page (which that branch renames `index.html` ->
   `index.php`; add it to whichever is current after Brevo merges) and `datenschutz.html`.
4. Reconcile with the Brevo branch at merge time (home page is the overlapping file).

Merge + deploy only after 1-3 are done. Nothing here went live on Paul's "install GA4" alone; the word
armed the id, the merge is the install.
