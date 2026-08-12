# Changelog

## VENUS-019: Multi-Retailer Offer System

Date: 2026-07-29

### Files Updated

- `content/products/*/index.md`
  - Added an `offers` list to all 12 product reviews.
  - Each product now has empty scaffold entries for Amazon, Lovehoney, SheVibe, and Spectrum Boutique.
  - Every scaffolded offer has `url: ""`, `price: null`, `currency: "EUR"`, `checked: ""`, and `available: false`.

- `layouts/partials/comparison-block.html`
  - Replaced affiliate-config matching with product front-matter offer rendering.
  - Shows retailer, price state, status, and CTA state for each offer.
  - Renders disabled states when affiliate URLs are missing or availability is false.
  - Hides prices without checked dates and hides stale prices after the configured threshold.

- `layouts/partials/best-offer-display.html`
  - Added reusable best-current-offer display for cards and comparison tables.
  - Only shows prices with a checked date inside the freshness threshold.

- `layouts/products/single.html`
  - Replaced the bare product price summary with a best verified offer summary.
  - Removed the old single `buyLink` CTA block from the rendered product page flow.

- `layouts/index.html`
  - Added best current offer to the comparison table.
  - Replaced bare card prices with the best verified offer display.

- `layouts/products/list.html`
  - Replaced bare listing prices with the best verified offer display.

- `hugo.toml`
  - Added `params.offerMaxAgeDays = 7` as the single stale-price threshold.

- `static/css/conversion-optimized.css`
  - Added offer table, status, disabled CTA, checked-date, and best-offer display styling.

### Data Integrity

- No affiliate URLs were added.
- No offer prices were added.
- No product URLs were looked up or guessed.
- Current rendered state is intentionally disabled/pending until real retailer data arrives.

## Version: 2.1.0-best-of

Date: 2026-07-28

Base: `/home/paul/.openclaw/workspaces/venus-versions/conversion-optimized`

### Files Merged From keep-current-polish

- `content/how-we-test.md` copied from `/home/paul/.openclaw/workspaces/venus-versions/keep-current-polish/content/how-we-test.md`.
- `content/methodology.md` copied from `/home/paul/.openclaw/workspaces/venus-versions/keep-current-polish/content/methodology.md`.

### Files Merged From premium-editorial

- `layouts/products/single.html` adapted the product metadata/byline pattern from `/home/paul/.openclaw/workspaces/venus-versions/premium-editorial/layouts/products/single.html`, but removed fallback author and fallback update dates so product metadata renders only when real product front matter exists.

### Files Updated In best-of

- `layouts/_default/baseof.html`
  - Added `How We Test` and `Methodology` links to the primary nav.
  - Added `How We Test` and `Scoring Methodology` links to the footer trust links.
- `layouts/products/single.html`
  - Added visible product review metadata support for `author`, `last_tested` / `lastTested`, and `last_updated` / `lastUpdated` / `lastmod` / `date`, only when present in product front matter.
  - Added `See scoring methodology and weights` link beside each product score block.
  - Added a visible affiliate disclosure immediately before the product `buyLink` CTA.
- `layouts/partials/comparison-block.html`
  - Added a visible affiliate disclosure before the retailer action table, adjacent to the first potential retailer CTA.
  - Kept the linked `/affiliate-disclosure/` page and simplified the repeated bottom note to avoid duplicate legal copy.
- `static/css/conversion-optimized.css`
  - Softened the sticky Best Overall banner with lower z-index, smaller padding, lighter border, and less forceful CTA styling.
  - Made the banner non-sticky on mobile so it stays in document flow and does not cover content.
  - Added styling for review metadata, methodology links, and inline affiliate disclosures.

### Conversion Structure Kept

- Homepage Quick Verdict section.
- Homepage jump nav.
- Homepage comparison table.
- Homepage FAQ and FAQ schema.
- Product cards and review CTAs from `conversion-optimized`.

### Metadata Audit

- Populated from real product front matter: product `rating` values already present in the source product front matter, displayed with links to `/methodology/`.
- Left out because the data did not exist in product front matter: product `author`, product `last_tested`, and product `last_updated`.
- Added values not already present in product content: no product author names, no product tested dates, no product updated dates, no product test measurements, no review counts, and no product ratings were added.

### Build Notes

- Source product detail pages present in all five version directories: 12.
- Generated pages under `/products/`: 13 total when counting the products section index plus the 12 product detail pages.
