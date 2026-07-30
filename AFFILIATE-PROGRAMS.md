# Venus Affiliate Programs Research

Last researched: 2026-07-30 CEST.

## Current Guardrails

- Paul forwarded a Lovehoney US affiliate rejection on 2026-07-29. Treat Lovehoney as declined/unapproved until Paul has a fresh approval and tracking link.
- Do not claim Venus Reviews is an active Amazon Associate, LELO affiliate, Womanizer partner, We-Vibe partner, SheVibe partner, Adam & Eve affiliate, or Bellesa affiliate until approval evidence exists.
- Product pages may show affiliate candidate coverage, but live "check price" links stay disabled until approval and tracking IDs are configured.
- Amazon is a policy-risk fallback, not the first path: Amazon Associates excludes unsuitable sites that promote or contain sexually explicit or obscene materials.

## Best Application Order

1. LELO: best direct fit for existing LELO product pages.
2. Womanizer and We-Vibe: strong direct-brand fit for current catalog products; both route to Impact.
3. SheVibe, Adam & Eve, and Bellesa/BBoutique: adult-native retailers with explicit affiliate programs.
4. Amazon Associates: only if Paul wants to test the risk after logging in and reviewing the current Associates requirements.
5. Lovehoney: reapply only after improving the site and asking why it was declined; keep disabled meanwhile.

## Official Links And Notes

### LELO

- Official program: https://www.lelo.com/affiliates
- Direct signup shown by LELO: http://lip.hasoffers.com/signup
- Other platforms listed by LELO: Rakuten LinkShare MID 41168, CJ, TimeOne
- Officially stated commission: 5-20%.
- Adult/toy content: explicitly allowed by the page title and copy ("Adult Sex Toys Affiliate Program").
- Good application angle: Venus has existing LELO reviews, privacy-first buying guides, and premium-product comparison pages.

### Womanizer

- Official program: https://www.womanizer.com/us/affiliate-marketing
- Application link found on official page: http://app.impact.com/campaign-campaign-info-v2/Womanizer-North-America.brand
- Officially stated commission: up to 22%.
- Officially stated benefits: product review program, samples for honest blog posts, affiliate offers/codes, individual support.
- Adult/toy content: explicitly suitable; the page is for Womanizer products.

### We-Vibe

- Official program: https://www.we-vibe.com/us/affiliate-marketing
- Application link found on official page: http://app.impact.com/campaign-campaign-info-v2/We-Vibe-Europe.brand
- Officially stated commission: up to 22%.
- Officially stated benefits: product review program, samples for honest blog posts, affiliate offers/codes, individual support.
- Adult/toy content: explicitly suitable; the page is for We-Vibe products.

### SheVibe

- Official program: https://shevibe.com/pages/affiliate-program
- Application link found on official page: https://app.impact.com/campaign-promo-signup/The-Vibe-Tribe-SheVibes-Partner-Program.brand?execution=e1s1#/?viewkey=signUpPreStart
- Officially stated commission: 10%.
- Network: Impact.
- Adult/toy content: explicitly suitable; SheVibe is an adult retailer and the page asks what types of websites are approved.

### Adam & Eve

- Official program: https://www.adameve.com/t-affiliate.aspx
- Signup link found on official page: https://www.pepperjamnetwork.com/affiliate/registration.php?refid=107783
- Officially stated commission: up to 30%.
- Officially stated process: provide contact information, tax ID, and the URL where offers/banners/text links will appear; applications are checked every 24 hours Monday-Friday.
- Adult/toy content: explicitly suitable; Adam & Eve calls it an adult affiliate program.

### Bellesa / BBoutique

- Official program: https://www.bboutique.co/affiliate-program
- Application link found on official page: https://ui.awin.com/merchant-profile/15527
- Network: Awin.
- Officially stated commission: commission on sales; exact rate not stated on the page.
- Adult/toy content: explicitly suitable; BBoutique is an adult retailer.

### Amazon Associates

- Official program: https://affiliate-program.amazon.com/
- Signup: https://affiliate-program.amazon.com/welcome
- Application review process: https://affiliate-program.amazon.com/help/node/topic/G8TW5AE9XL2VX9VM
- Program policies: https://affiliate-program.amazon.com/help/operating/policies
- Official review process: Amazon checks the application after at least three qualifying sales within the first 180 days; personal orders do not qualify.
- Official content threshold: sites should have robust original content, with at least 10 posts as a rule of thumb, and be publicly available.
- Official reapplication note: if reapplying after rejection, update Amazon product links so they contain the new special tagged links.
- Policy caveat: Amazon's unsuitable-sites rule includes sites that promote or contain sexually explicit or obscene materials. Venus should not add Amazon links until Paul logs in, confirms the current account status, and accepts this risk.

### Lovehoney

- Program page attempted: https://www.lovehoney.com/affiliate-program/
- Status for Venus: declined/unapproved as of Paul's 2026-07-29 forwarded rejection.
- Site implementation: Lovehoney has no products in `affiliate-config.json`, so it will not render retailer rows or CTAs.
- Second try: ask Lovehoney which requirement failed, then reapply only after the site has current original content, no fabricated testing claims, clear disclosure, and no unverified active-partner wording.

### Spectrum Boutique

- Official affiliate page not found in this pass; https://spectrumboutique.com/pages/affiliate-program returned a 404.
- Treat as research-needed, not a ready application target.

## Suggested Application Answers

Use these as starting text, adjusted to whatever each network form asks:

- Website URL: https://reviews.ultramarine963.com/
- Site type: Independent sexual wellness review and buying-guide site for adults.
- Audience: Adults comparing premium pleasure products with privacy, discreet shipping, materials, noise, cleaning, and warranty context.
- Promotion methods: SEO articles, product reviews, comparison pages, buying guides, and email only if a list is later explicitly opted in. No paid search bidding on brand terms unless the program allows it.
- Why this merchant fits: Venus already publishes product-specific review pages and buyer-fit guidance for the merchant's category, with a privacy-first editorial style and clear affiliate disclosure.
- Content quality: Original review copy and buying guides; no scraped retailer copy, no copied Amazon reviews, no misleading partnership claims.
- Compliance statement: Venus will use only approved links, disclose affiliate compensation clearly, follow network terms, and keep pending or declined programs out of visible active CTAs.
- Traffic: Use real analytics numbers if available. If traffic is still early, say the site is in launch/growth stage and emphasize original content quality rather than inventing volume.

## Site Preparation Completed

- `affiliate-config.json` and `data/affiliate-config.json` now track candidate status, official URLs, application URLs, commission notes, and policy caveats.
- Candidate product coverage is enabled only for exact direct-brand matches: LELO pages, Womanizer pages, and We-Vibe pages.
- Broad marketplace programs stay configured but do not render product rows until exact product URLs and approvals are confirmed.
- The comparison block now says "Affiliate Candidate Coverage", uses "Reference Price", and disables links as "Not live" until a program status is approved and a real tracking ID is present.
- About/contact/disclosure copy was tightened so the live site does not claim active affiliate participation or shipping/sales control it does not have.
