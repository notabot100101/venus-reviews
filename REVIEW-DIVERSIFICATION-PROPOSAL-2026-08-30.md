# Venus Reviews — Review Diversification Proposal (draft for Paul's approval)

Date: 2026-08-30 (Claw/main live-evidence pass)
Status: PROPOSAL ONLY — no content/production changes made. Awaiting Paul's approval of direction.

## 1. What I inspected (evidence)

- Live site: https://reviews.ultramarine963.com/ — sitemap shows **17 published product reviews**.
- Source of truth repo: `/home/paul/.openclaw/workspaces/worker/venus-site`
  - Branch: `hostinger-deploy` | origin: `github.com/notabot100101/venus-reviews`
  - HEAD: `66f04a57 integration: rebuild site output from merged SEO/schema source (ORA 3, JSON-LD, title/meta fixes)`
  - `content/products/` = 38 product dirs; **17 published** (`draft: false`), 21 drafts. Live sitemap = exactly the 17.
- Template reality check — `layouts/products/single.html` lines 167-169:
  > "No Review.rating in the schema (2026-08-07): the old ratingValue was an invented editorial score for products the site itself says were never physically tested. Product reviews are represented without ratings."
  → **The live site intentionally renders NO numeric star ratings.** Ratings were removed 2026-08-07 as an integrity fix because products were never physically tested.
- How tone is expressed today: a `badge` label per product (all POSITIVE-sounding):
  Advanced Pick (lelo-enigma), Compact Pick (dame-eva-ii), Flexible Shape (fun-factory-manta), Precision Pick (fun-factory-volta), Premium Wellness (lelo-hugo), Sonic Wave (lelo-sona-2), Mid-Range Bestseller (lovehoney-desire), Couples Pick (we-vibe-chorus), Adjustable Fit (we-vibe-sync). No badge on ~8 others. **No mixed/critical labels exist.**
- Templates already support `pros` / `cons` params — but no published product currently populates a structured Cons block.
- Honest downside content ALREADY exists in the prose (not surfaced as verdicts):
  - satisfyer-pro-2: "runtime is modest, charging is slow, and the build and interface are plainly less refined than Womanizer's Premium line"
  - lelo-ora-3: "fit-dependent, position-sensitive", "shorter runtime than some simple vibrators"
  - we-vibe-sync: "appears out of stock on the live manufacturer page"
  - fun-factory-volta / manta: several specs "not documented by the manufacturer" (dimensions, battery, runtime, noise, warranty)
  - lovehoney-desire: "exact manufacturer page was not reachable… specs are not documented by the manufacturer here"

## 2. The core tension (must decide before drafting)

Paul asked for "some that have downsides and lower star ratings."
- The site has **no star ratings** by deliberate integrity policy (2026-08-07), because every review states "Venus has not physically tested this product."
- Reintroducing numeric stars as editorial scores would be exactly what the team removed as "invented" — unless the stars are **sourced** (e.g., a documented aggregate rating, like lelo-sila's "LELO aggregate rating: 4.4/5 (89 reviews)").

So there are two honest paths:
- **Path A (recommended): diversify VERDICT TONE, no invented stars.** Add explicit mixed/critical verdict framing + a structured "Cons / Who it's NOT for" block per selected product, and add lower-key badges (e.g., "Entry / Value Pick", "Specialist Only", "Mixed Feedback", "Check Availability"). This satisfies "not all just good products, some with downsides" without fabricating ratings, and it's what the site can defend under its own "How We Evaluate" page.
- **Path B (only if Paul explicitly wants stars back): sourced aggregate ratings only.** Re-add a star display ONLY where a documented source exists (manufacturer aggregate, e.g., LELO's 4.4/5), shown as "source aggregate, not Venus editorial." Where documentation is weak (lovehoney-desire, fun-factory-volta/manta), stars stay absent or read "insufficient public data to rate."

## 3. Concrete diversification proposal (Path A default)

**A. New verdict/badge vocabulary** (pick per product, replaces/augments the all-positive badges):
- Positive tier: Advanced / Best Overall / Top Value / Best for X (keep for: lelo-enigma, lelo-sona-2, we-vibe-chorus, dame-eva-ii, lelo-hugo, womanizer-premium-2)
- Mixed tier ("good but with real caveats"): **satisfyer-pro-2** (value pick, modest runtime/slow charge/less refined), **lelo-ora-3** (specialist, position-sensitive, shorter runtime), **fun-factory-manta** (flexible shape, spec gaps), **fun-factory-volta** (precision, spec gaps)
- Critical/documentation tier: **lovehoney-desire** (manufacturer page unreachable → cannot verify key specs; honest verdict should say so and rate it "unverifiable — verify before buying"), **we-vibe-sync** (availability concern; out-of-stock on manufacturer page)
- Leave truly neutral (no rating, no badge): any product where neither badge nor caveat is supportable

**B. Structured Cons block (template already has `.Params.cons`)** — add a visible "Trade-offs & Cons" + "Who it's not for" section on the ~6 mixed/critical products, reusing the honest caveat language already in the prose. This is the single highest-value change and requires zero invented facts.

**C. Lower star ratings (Path B) only where sourced** — lelo-sila already cites a documented aggregate (4.4/5, 89 reviews). If Paul wants stars displayed, that's the only safe pattern: sourced aggregates labeled as such, never Venus editorial stars.

## 4. Suggested target state

| Product | Current badge | Proposed verdict | Basis (all from existing copy/docs) |
|---|---|---|---|
| lelo-enigma | Advanced Pick | Positive — keep | strong docs, waterproof, 2yr/10yr warranty |
| lelo-sona-2 | Sonic Wave | Positive — keep | premium sonic, 12 modes, waterproof |
| we-vibe-chorus | Couples Pick | Positive — keep | richest app/remote feature set |
| dame-eva-ii | Compact Pick | Positive — keep | hands-free, quiet, documented |
| lelo-hugo | Premium Wellness | Positive — keep | prostate pick, strong docs |
| womanizer-premium-2 | (none) | Positive | premium air-pulse, 5yr warranty |
| satisfyer-pro-2 | (none) | **Mixed — Value Pick** | "runtime modest, charging slow, less refined" |
| lelo-ora-3 | (none) | **Mixed — Specialist** | "position-sensitive", shorter runtime |
| fun-factory-manta | Flexible Shape | **Mixed** | spec gaps documented |
| fun-factory-volta | Precision Pick | **Mixed** | spec gaps documented |
| lovehoney-desire | Mid-Range Bestseller | **Critical — Unverifiable specs** | manufacturer page unreachable |
| we-vibe-sync | Adjustable Fit | **Mixed — Check availability** | out-of-stock on manufacturer page |
| (lelo-gigi-2, lelo-mona, lelo-sila, we-vibe-tango-x, fun-factory-vim) | (none) | Verify docs before labeling | — |

## 5. What needs Paul's approval

1. **Path A vs Path B** — diversify tone only (recommended) vs also reintroduce sourced numeric stars.
2. **The 6 mixed/critical assignments above** — confirm the target list before drafting.
3. **Draft location**: on a non-production branch of `worker/venus-site` (e.g., `review-diversification-2026-08-30`), content + a Cons block template tweak; nothing merged/pushed until Paul reviews the rendered preview.
4. No invented factual/testing claims — every con reuses language already in the reviews or documented manufacturer/availability facts.

## 6. Files touched (after approval, not now)
- `content/products/{satisfyer-pro-2,lelo-ora-3,fun-factory-manta,fun-factory-volta,lovehoney-desire,we-vibe-sync}/index.md` — verdict, badge, cons block
- `layouts/products/single.html` — render `.Params.cons` (if not already handled)
- New branch; no changes to public/ or live deploy
