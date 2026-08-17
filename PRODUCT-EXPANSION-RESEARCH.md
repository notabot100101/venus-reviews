# Venus Product Expansion Research
**Created:** 2026-08-05  
**For:** Ascend (Pepperjam) + Impact + LELO affiliate programs  
**Current product count:** 12 live pages, 15 in catalog

---

## Research Approach

These recommendations are organized by **which approved affiliate program can earn commission for each product**, so Paul can prioritize applying to programs that unlock the most new content.

---

## Priority 1: LELO Products (Direct Affiliate, 5-20%)

LELO is the strongest first target: Venus already has 4 LELO reviews, LELO explicitly allows adult content, and the commission is solid. Adding more LELO products strengthens the brand cluster.

| Product | Price | Category | Why Add |
|---------|-------|----------|---------|
| **LELO Sila** | $119 | Air pulse (Sonic) | Competitor to Womanizer in the air-pulse space; gives Venus an alternate recommendation angle |
| **LELO Ora 3** | $129 | Oral-simulation | Unique category — no other product on Venus does this. Great for variety |
| **LELO Tiani 3** | $119 | Couple's wearable | Competes with We-Vibe Chorus; gives readers a premium alternative to compare |
| **LELO Tor 3** | $79 | Vibrating ring | Currently no male-focused product on Venus; fills a gap |
| **LELO F1S V2** | $129 | Male-focused (stroker) | Only male-focused pleasure device; fills the biggest gender gap on the site |
| **LELO Ida** | $159 | App-controlled couple's | Premium app-controlled; rounds out the LELO ecosystem |

**Commission from LELO:** 5-20%. Adding 6 new LELO products = 10 total LELO reviews. Strong cluster for SEO.

---

## Priority 2: Womanizer Products (Impact, Up to 22%)

Womanizer only has 1 product on Venus. Their affiliate program offers up to 22% + product samples for reviews.

| Product | Price | Category | Why Add |
|---------|-------|----------|---------|
| **Womanizer Premium 2** | $179 | Premium air pulse | Already in catalog as "Womanizer 2" but no dedicated review page. This IS the 2nd-gen model |
| **Womanizer Liberty** | $89 | Compact air pulse | Budget-friendly entry to the brand; attracts price-sensitive shoppers |
| **Womanizer DUO 2** | $179 | Dual stimulation | Internal + clitoral — unique dual-stim product for the premium tier |
| **Womanizer Next** | $159 | Newest model | Latest generation; future-proofs the site |
| **Womanizer Starlet 3** | $59 | Budget air pulse | Entry-level; competes with Satisfyer Pro 2 |

**Commission:** Up to 22%. Adding 5 Womanizer products = 5-6 total. Strongest per-product commission.

---

## Priority 3: We-Vibe Products (Impact, Up to 22%)

Currently 2 We-Vibe products. The brand cluster can grow to cover more couple's and wearable options.

| Product | Price | Category | Why Add |
|---------|-------|----------|---------|
| **We-Vibe Melt** | $149 | Air pulse (clitoral) | Womanizer competitor under same parent; comparison content opportunity |
| **We-Vibe Nova 2** | $119 | Rabbit vibrator | Replaces/heals the lovehoney-desire gap (no approved program for LH) |
| **We-Vibe Match** | $99 | Budget couple's wearable | Entry-level couple's option |
| **We-Vibe Vector** | $99 | Prostate massager | Male-focused; fills gap, same Impact dashboard |
| **We-Vibe Jive** | $99 | Wearable remote | Discreet wearable; good for "gift" / "starter" content |

**Commission:** Up to 22%. Adding 5 We-Vibe products = 7 total. Best ROI since single Impact dashboard manages all.

---

## Priority 4: Broad Catalog (SheVibe — Impact, 10%)

SheVibe carries many brands. Use these for products without a direct-brand program, or when you want a second retailer link for price comparison.

| Product | Price | Brand/Why | Affiliate Via |
|---------|-------|-----------|--------------|
| **Satisfyer Pro 3** | $59 | Satisfyer — update/replace Pro 2 | SheVibe (Impact, 10%) |
| **Satisfyer Curvy 1+** | $55 | App-controlled air pulse | SheVibe |
| **Fun Factory Stronic G** | $149 | Pulsator (unique tech category) | SheVibe |
| **Fun Factory Bi Stronic** | $149 | Couple's pulsator | SheVibe |
| **B-Vibe Rimming Plug** | $89-129 | Anal educator (unique content) | SheVibe |
| **B-Vibe Snug Plug 2-4** | $40-60 | Weighted plug set (great "best of" content) | SheVibe |
| **Dame Pillo** | $125 | Innovative shape, quality brand | SheVibe |
| **Dame Kip** | $85 | Ergonomic vibe | SheVibe |

**Commission:** 10%. Good for non-LELO/Womanizer/We-Vibe products. Broad catalog means one affiliate link per product instead of per-brand.

---

## Priority 5: Adam & Eve (Pepperjam/Ascend, Up to 30%)

Your Ascend registration is being reviewed. Adam & Eve's up to 30% is the highest commission, but it's US-only and they're a broad retailer rather than a brand. Best use: add links to existing products rather than creating new product pages.

---

## Product Expansion Summary

| Priority | Program | New Products | Est. Commission | Products After |
|----------|---------|-------------|-----------------|----------------|
| 1 | LELO (direct) | 6 | 5-20% | 4 → 10 LELO |
| 2 | Womanizer (Impact) | 5 | up to 22% | 1 → 6 Womanizer |
| 3 | We-Vibe (Impact) | 5 | up to 22% | 2 → 7 We-Vibe |
| 4 | SheVibe (Impact) | 8 | 10% | 0 → 8 (broad catalog) |

**Total potential growth:** 24 new products → 36 total
**First-phase target (most impactful):** 8-12 products from LELO + Womanizer + We-Vibe

---

## Site Pre-Configuration Status

- ✅ `affiliate-link-setup.sh` — one-step script to drop in tracking IDs
- ✅ `affiliate-link-setup.py` — updates config JSON + product front matter
- ✅ `.env.affiliate.example` — env file template (keep IDs out of git)
- ✅ `affiliate-config.json` — tracking prefix placeholders ready
- ✅ All 12 product pages have `offers` arrays with empty URLs + `available: false`
- ❌ No tracking IDs yet (waiting on approvals)

**Getting links live when approved takes 3 commands:**
```bash
./affiliate-link-setup.sh --lelo=REAL_ID
git diff          # verify
./deploy.sh "activate LELO affiliate links"
```