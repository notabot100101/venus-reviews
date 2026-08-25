# Venus Unified Affiliate Plan
**Date:** 2026-08-04 · **Updated:** 2026-08-25 · **Status:** REFRESHED — see `impact-onboarding-report.md` (2026-08-24) for dated source of truth

> ⚠️ **IMPORTANT:** This planning doc lives in the deploy branch root (masked by .htaccess). Post-2026-08-25 JSON-exposure fix, these planning docs should be moved OUT of the deployed tree.

**Reconciles:** AFFILIATE-RESEARCH.md (Jul 30) + VENUS-IMAGERY-AND-GROWTH-PLAN-20260803.md

---

## 1. TL;DR for Paul

**BBoutique/Awin links ARE live since 2026-08-17** (Publisher ID: 3022209). Impact partners remain blocked by incomplete onboarding.
1. Apply to each programme → get approved → receive a tracking ID.
2. Drop that ID into `affiliate-config.json` + the product's `offers[].url`.
3. Run `./deploy.sh` to rebuild and push.

**If a dashboard already shows `reviews.ultramarine963.com`** — that only means the site URL is registered in that network/account. It does **not** mean the programme is approved or that links are active. You still need to:
- Complete the merchant-specific application inside that network.
- Wait for merchant approval.
- Grab the real tracking link/ID from the dashboard.
- Insert it into the config and redeploy.

---

## 2. Per-Partner Rollout Table (smaller partners first, Amazon LAST)

| # | Partner | Network | Commission | Sign-up URL | Dashboard / Login | Approval Status | Next Action |
|---|---------|---------|------------|-------------|-------------------|-----------------|-------------|
| 1 | **LELO** | Direct (HasOffers) + alternates | **5–20%** (web-verified 2026-08-04) | <http://lip.hasoffers.com/signup> | <https://lip.hasoffers.com/> | ❌ **REJECTED** Aug 20, 2026 | Account rejected. Reapply once site has stronger traffic/content. See AFFILIATE-CREDENTIALS.md for reapplication strategy. |
| 2 | **Womanizer** | Impact | **Up to 22%** | <http://app.impact.com/campaign-campaign-info-v2/Womanizer-North-America.brand> | <https://app.impact.com> | ⏳ **Not applied** — onboarding blocked | Account exists (paulpawprints, ID: 7454049). Partner Program Agreement checkbox must be checked to proceed. |
| 3 | **We-Vibe** | Impact | **Up to 22%** | <http://app.impact.com/campaign-campaign-info-v2/We-Vibe-Europe.brand> | <https://app.impact.com> | ⏳ **Not applied** — onboarding blocked | Same Impact account. Application blocked until onboarding complete. |
| 4 | **SheVibe** | Impact | **10%** (web-verified) | <https://app.impact.com/campaign-promo-signup/The-Vibe-Tribe-SheVibes-Partner-Program.brand> | <https://app.impact.com> | ⏳ **Not applied** — onboarding blocked | Same Impact account. Application blocked until onboarding complete. |
| 5 | **Adam & Eve** | Pepperjam (eBay Enterprise) | **Up to 30%** (web-verified) | <https://www.pepperjamnetwork.com/affiliate/registration.php?refid=107783> | <http://www.pepperjamnetwork.com/> | ⏳ **Pending** — submitted Aug 5 | 24-48h review period. US-only. Highest commission. |
| 6 | **Bellesa / BBoutique** | Awin | unstated | <https://ui.awin.com/merchant-profile/15527> | <https://ui.awin.com> | ✅ **LIVE since 2026-08-17** | Publisher ID: 3022209. Links active on all product pages. Awin links are the ONLY live affiliate revenue source currently. |
| — | **Lovehoney** | — | — | — | — | **DECLINED 2026-07-29** | Do not apply now. Reapply once traffic/content grows. |
| 7 | **Amazon Associates** | Amazon | 1–3% | <https://affiliate-program.amazon.com/welcome> | <https://affiliate-program.amazon.com/> | Needs Paul's login + policy review | **LAST.** High policy risk — Amazon excludes "sexually explicit" sites. Only consider for non-adult accessories (chargers, cases, cleaners) after other programmes are live. |

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

### Phase 1 — This Week (LELO + Impact account)
- [ ] Apply to **LELO** direct: <http://lip.hasoffers.com/signup>
- [ ] Create **Impact** account: <https://app.impact.com>
- [ ] Apply to **Womanizer** inside Impact
- [ ] Apply to **We-Vibe** inside Impact
- [ ] Apply to **SheVibe** inside Impact

### Phase 2 — Next 1–2 Weeks (Approval + IDs)
- [ ] Receive approval emails + tracking IDs
- [ ] Update `affiliate-config.json` with real IDs
- [ ] Populate `offers[].url` + `available: true` for top 5 products
- [ ] Run `./deploy.sh`
- [ ] Test that buttons render and click-throughs work

### Phase 3 — Weeks 2–4 (Expand coverage)
- [ ] Apply to **Adam & Eve** via Pepperjam
- [ ] Fill affiliate links for all remaining products
- [ ] Optional: apply to Bellesa/BBoutique via Awin

### Phase 4 — Last (Amazon, only if you accept the risk)
- [ ] Review Amazon Associates policy: <https://affiliate-program.amazon.com/help/operating/policies>
- [ ] Decide whether adult toy review content is worth the risk
- [ ] If yes, apply; if no, skip entirely
- [ ] If approved, only use for accessories (chargers, cases, cleaners)

### Phase 5 — Later (Lovehoney reapplication)
- [ ] Once traffic/content has grown, reapply to Lovehoney
- [ ] Previous decline was 2026-07-29 — wait for stronger metrics before reapplying

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
