# Venus Unified Affiliate Plan
**Date:** 2026-08-04 · **Status:** updated 2026-08-25 · **Source of truth:** `workspace/main/impact-onboarding-report.md` (2026-08-24)

> ⚠️ **This document was stale.** Previous versions listed LELO and Lovehoney as not-applied candidates and BBoutique as not applied. The real state is below. Always check the dated report in `workspace/main/` for current truth.
> 
> **Security note:** These planning docs live in the deploy branch root, currently masked from the public only by `.htaccess`. Consider moving them out of the deployed tree entirely (follow-up from 2026-08-25 JSON-exposure fix).

---

## 1. TL;DR for Paul

**Some links ARE live.** BBoutique/Awin links (publisher 3022209) have been active on all product pages since 2026-08-17. Impact partners are blocked by incomplete onboarding. To activate remaining partners:
1. Complete Impact onboarding (Partner Program Agreement + verification).
2. Apply to each programme → get approved → receive a tracking ID.
3. Drop that ID into `affiliate-config.json` + the product's `offers[].url`.
4. Run `./deploy.sh` to rebuild and push.

**If a dashboard already shows `reviews.ultramarine963.com`** — that only means the site URL is registered in that network/account. It does **not** mean the programme is approved or that links are active. You still need to:
- Complete the merchant-specific application inside that network.
- Wait for merchant approval.
- Grab the real tracking link/ID from the dashboard.
- Insert it into the config and redeploy.

---

## 2. Per-Partner Rollout Table (smaller partners first, Amazon LAST)

| # | Partner | Network | Commission | Sign-up URL | Dashboard / Login | Approval Status | Next Action |
|---|---------|---------|------------|-------------|-------------------|-----------------|-------------|
| 1 | **BBoutique / Bellesa** | Awin | unstated | <https://ui.awin.com/merchant-profile/15527> | <https://ui.awin.com> | ✅ **LIVE** — Publisher 3022209 since 2026-08-17 | Links active on all product pages. |
| 2 | **Adam & Eve** | Pepperjam | **Up to 30%** | <https://www.pepperjamnetwork.com/affiliate/registration.php?refid=107783> | <http://www.pepperjamnetwork.com/> | ⏳ **PENDING** — Submitted Aug 5, awaiting review | Awaiting Pepperjam review. |
| 3 | **Womanizer** | Impact | **Up to 22%** | Search inside Impact dashboard | <https://app.impact.com> | ⏳ **NOT APPLIED** — Onboarding incomplete | Complete Impact onboarding first. |
| 4 | **We-Vibe** | Impact | **Up to 22%** | Search inside Impact dashboard | <https://app.impact.com> | ⏳ **NOT APPLIED** — Onboarding incomplete | Complete Impact onboarding first. |
| 5 | **SheVibe** | Impact | **10%** | <https://app.impact.com/campaign-promo-signup/The-Vibe-Tribe-SheVibes-Partner-Program.brand?execution=e1s1#/?viewkey=signUpPreStart> | <https://app.impact.com> | ⏳ **NOT APPLIED** — Onboarding incomplete | Complete Impact onboarding first. |
| — | **LELO** | LIP/HasOffers | 5–20% | <http://lip.hasoffers.com/signup> | <https://lip.hasoffers.com/> | ❌ **REJECTED** (Aug 20) — "missing information or misalignment with our brand" | Email `affiliates@lelo.com` for specifics, or reapply later with stronger site metrics. |
| — | **Lovehoney** | — | — | — | — | ❌ **DECLINED** (Jul 29) — "Brand alignment mismatch" | Do not apply now. Reapply once traffic/content grows. |
| — | **Amazon Associates** | Amazon | 1–3% | <https://affiliate-program.amazon.com/welcome> | <https://affiliate-program.amazon.com/> | Needs Paul's login + policy review | **LAST.** High policy risk. Only for non-adult accessories after other programmes are live. |

### Network consolidation tip
Womanizer + We-Vibe + SheVibe all live on **Impact**. Create ONE Impact account and apply to all three merchants from inside it.

---

## 3. What "Dashboard Shows reviews.ultramarine963.com" Means

Paul asked: *"My affiliate-program dashboards show `reviews.ultramarine963.com` registered — is this correct, how do I proceed?"*

**Answer:**
- **Yes, the domain is correct** — that is Venus's live URL.
- **"Registered" ≠ "Approved"**. It means the network knows about the site, but each merchant (LELO, Womanizer, etc.) must still individually approve your application.
- **Exact next steps per programme:**
  1. Log into the network dashboard (Impact / Pepperjam / HasOffers / Awin / Amazon).
  2. Find the merchant's application page inside that network.
  3. Submit / complete the application if not already done.
  4. Wait for merchant approval email.
  5. Once approved, the dashboard will show a **tracking ID** and/or **deep-link generator**.
  6. Copy that tracking ID into `affiliate-config.json` under `trackingPrefixes.{partner}`.
  7. Generate or construct the real product URLs and paste them into each product's front matter (`content/products/{product}/index.md`) inside the `offers[]` array.
  8. Set `available: true` for that offer.
  9. Rebuild + redeploy.

---

## 4. Where the IDs Go (Concrete Implementation)

### 4a. Global config: `affiliate-config.json` (root of repo)

Replace the placeholder values under `trackingPrefixes` with real IDs as you receive them:

```json
{
  "trackingPrefixes": {
    "lelo": "YOUR_LELO_TRACKING_ID",
    "womanizer": "YOUR_IMPACT_ID",
    "wevibe": "YOUR_IMPACT_ID",
    "shevibe": "YOUR_IMPACT_ID",
    "adameve": "YOUR_PEPPERJAM_ID",
    "bellesa": "YOUR_AWIN_ID",
    "amazon": "YOUR_AMAZON_TAG"
  }
}
```

Do **not** edit `data/affiliate-config.json` — that is legacy/outdated.

### 4b. Per-product front matter: `content/products/{product}/index.md`

Example for `lelo-sona-2`:

```yaml
offers:
  - retailer: "LELO"
    url: "https://www.lelo.com/sona-2?aff=YOUR_LELO_TRACKING_ID"
    price: 179.99
    currency: "USD"
    checked: "2026-08-04"
    available: true
  - retailer: "Amazon"
    url: ""
    price: null
    currency: "EUR"
    checked: ""
    available: false
```

**Rules:**
- Links render **only** when `url != ""` AND `available: true`.
- If either is missing, the button shows "Coming soon" / "Affiliate link pending".
- Keep `available: false` until you have a real, approved tracking URL.

### 4c. Redeploy step (required)

After any change to `affiliate-config.json` or product front matter:

```bash
./deploy.sh
```

This rebuilds the Hugo site and rsyncs it to the live host. **Links will not appear on the live site until you redeploy.**

---

## 5. Ordered Rollout Plan

### Phase 1 — Complete Impact Onboarding (Blocks Everything)
- [ ] Log into **Impact**: <https://app.impact.com> (credentials: `paulpawprints`)
- [ ] Check the **Partner Program Agreement** checkbox
- [ ] Click **Continue** to complete onboarding wizard
- [ ] Handle any Cloudflare verification challenge manually
- [ ] Once onboarding is complete, notify agent to proceed with applications

### Phase 1b — LELO Reapplication (Optional)
- [ ] Email `affiliates@lelo.com` for specific rejection feedback, OR
- [ ] Wait until site has stronger metrics, then reapply via <http://lip.hasoffers.com/signup>

### Phase 2 — Apply Inside Impact (After Onboarding)
- [ ] Apply to **Womanizer** inside Impact
- [ ] Apply to **We-Vibe** inside Impact
- [ ] Apply to **SheVibe** inside Impact
- [ ] Await approval emails + tracking IDs
- [ ] Update `affiliate-config.json` with real IDs
- [ ] Populate `offers[].url` + `available: true` for relevant products
- [ ] Run `./deploy.sh`
- [ ] Test that buttons render and click-throughs work

### Phase 3 — Expand Coverage
- [ ] Confirm **Adam & Eve** Pepperjam status (submitted Aug 5, awaiting review)
- [ ] Fill affiliate links for all remaining products
- [ ] Optional: apply to additional Awin merchants beyond BBoutique

### Phase 4 — Amazon (Last Resort, High Risk)
- [ ] Review Amazon Associates policy: <https://affiliate-program.amazon.com/help/operating/policies>
- [ ] Decide whether adult toy review content is worth the risk
- [ ] If yes, apply; if no, skip entirely
- [ ] If approved, only use for accessories (chargers, cases, cleaners)

### Phase 5 — Later (Lovehoney + LELO Reapplication)
- [ ] Once traffic/content has grown, reapply to **Lovehoney** (declined 2026-07-29)
- [ ] Reapply to **LELO** with stronger site metrics and specific feedback addressed

---

## 6. Application Quick-Start Answers

Use these answers when applying:

| Field | Suggested answer |
|-------|------------------|
| **Website URL** | `https://reviews.ultramarine963.com/` |
| **Site type** | Independent sexual wellness review and buying-guide site for adults |
| **Audience** | Adults comparing premium pleasure products with privacy, materials, noise, cleaning, and warranty context |
| **Promotion methods** | SEO articles, product reviews, comparison pages, buying guides. No paid search bidding on brand terms. |
| **Why this merchant** | Venus already publishes product-specific reviews with privacy-first editorial style and clear affiliate disclosure |
| **Content quality** | Original review copy and buying guides; no scraped retailer copy, no copied Amazon reviews, no misleading partnership claims |
| **Compliance** | Venus uses only approved links, discloses affiliate compensation clearly, follows network terms |

---

## 7. Risk Summary

| Risk | Level | Mitigation |
|------|-------|------------|
| Amazon Associates rejection/termination | **HIGH** | Apply last; only for non-adult accessories; have backups live first |
| Lovehoney re-decline | MEDIUM | Wait for more traffic/content before reapplying |
| Impact network (3 merchants) | LOW | Single dashboard makes management easy |
| Commission rate drops | LOW | Adult affiliate rates are stable (5–30%) |

---

## 8. Files You Need to Touch

| File | What to do |
|------|------------|
| `affiliate-config.json` | Replace `AFFILIATE_ID_*` placeholders with real tracking IDs |
| `content/products/*/index.md` | Fill `offers[].url` and set `available: true` per approved partner |
| `./deploy.sh` | Run after any change to make links live |

---

## 9. Evidence & Sources

- LELO affiliate terms: web-verified 2026-08-04 at <https://www.lelo.com/affiliates> — 5–20% commission, banners/images provided.
- SheVibe affiliate terms: web-verified 2026-08-04 at <https://shevibe.com/pages/affiliate-program> — 10% commission, Impact platform.
- Adam & Eve affiliate terms: web-verified 2026-08-04 at <https://www.adameve.com/t-affiliate.aspx> — up to 30% commission, Pepperjam platform.
- Womanizer / We-Vibe: existing research (AFFILIATE-RESEARCH.md, Jul 30) cites Impact, up to 22%; exact deep links inside Impact change — search merchant name after account creation.
- Lovehoney decline: Paul-forwarded rejection email dated 2026-07-29.
- Technical framework: Hugo `offers` array + `affiliate-config.json` + FTC-compliant disclosure page — already implemented, only data entry remains.

---

*Plan built by consolidating existing research. Do not overwrite this file without reading it first — it is the single source of truth for Venus affiliate rollout.*
