# Magic Wand Original — SALVAGED, NOT PUBLISHABLE YET

Iconic, category-defining plug-in wand massager known for deep, broad vibration and reliable
AC power. SKU: `magic-wand-original`.

**Status: `draft: true`.** This review was written 2026-09-22 on the `agent/worker` branch,
never merged, and was 404 on the live site for three weeks until the 2026-10-13 repo audit
found it. The 1,820 words of prose are worth keeping; the page is not shippable as-is.

## Why it is still a draft — five gaps, none of them inventable

1. **No product image.** `image:` points at `/images/placeholders/ambient-04.png`, a
   placeholder. Needs a real image through the normal pipeline (local source, vision-verified,
   never generated) — Pixel's call, not something to fabricate.
2. **No working offers.** All four rows (Amazon, Lovehoney, Babeland, Spectrum Boutique) have
   `url: ""`, `price: null`, `available: false`, `checked: ""`. There is nothing for a reader
   to click and nothing for the drift checker to verify.
3. **Price is stale and in the wrong currency.** `price: "74.95"` with
   `price_checked: "2026-09-22"` — three weeks old, and the offer rows say USD while the rest
   of the catalogue prices in EUR.
4. **`schema_product: false`**, unlike every other review. It should only be flipped once a
   real offer with a real price exists, or the schema would describe an offer we do not have.
5. **This README used to claim gallery images existed** at
   `/images/gallery/magic-wand-original/`. They do not — not on `agent/worker`, not in trunk.
   That claim was corrected on 2026-10-13 rather than left to mislead whoever picked this up.

## What is already right

No fabricated testing claims. Zero hits for "verified tester", "we tested", "our testing" or
attributed review quotes, and the frontmatter carries an honest `trust_note` saying the review
is based on manufacturer documentation and that Venus has not tested the product. That is the
required posture and it needs no cleanup.

## To publish

Supply a real image, real offer URLs with checked EUR prices, then set `schema_product: true`
and `draft: false`, run `scripts/check-model-drift.py` against the page, and deploy through the
token-gated process. Paul authorises each Venus production deploy individually.
