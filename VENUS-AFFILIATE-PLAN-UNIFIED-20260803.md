# Venus Affiliate Program — Unified Action Plan

**Date:** 2026-08-03  
**Status:** Framework ready, awaiting applications  
**Document Purpose:** Complete, actionable affiliate implementation guide for Venus Reviews

---

## 1. Executive Summary

### Current State
- **Framework:** Technical implementation complete (Hugo partials + config)
- **Disclosure:** FTC-compliant affiliate disclosure page already exists
- **Links:** All affiliate links currently **DISABLED** (placeholders only)
- **Priority:** Smaller/direct brand partners first, **Amazon LAST**

### Lovehoney Status — DECLINED ⚠️
- **Rejection Date:** 2026-07-29
- **Action:** Do NOT reapply immediately; wait for traffic/content growth
- **Note:** Revisit in 2-3 months with improved metrics

### Technical Framework (Already Built)
| Component | Status | Location |
|-----------|--------|----------|
| Price comparison partial | ✅ Ready | `layouts/partials/comparison-block.html` |
| Best offer display | ✅ Ready | `layouts/partials/best-offer-display.html` |
| Affiliate config | ✅ Ready | `affiliate-config.json` |
| FTC disclosure | ✅ Ready | `/affiliate-disclosure/index.html` |
| Product offers array | ✅ Ready | Each product's front matter |

### How Links Work
Links render ONLY when both conditions are true:
1. `url` field is non-empty in product front matter
2. `available: true` flag is set

---

## 2. Per-Partner Application Table

Apply in this exact order (smaller partners first):

| Priority | Name | Network | Commission | Signup URL | Dashboard URL | Approval Status | Next Action |
|----------|------|---------|------------|------------|---------------|-----------------|-------------|
| 1 | **LELO** | Direct/HasOffers | 5–20% | [lip.hasoffers.com/signup](http://lip.hasoffers.com/signup) | HasOffers dashboard after signup | 🟡 Candidate — Not yet applied | **Apply first** — provides product images |
| 2 | **Womanizer** | Impact | Up to 22% | [Impact signup](https://app.impact.com/campaign-promo-signup/Womanizer-North-America.brand) | app.impact.com after approval | 🟡 Candidate — Not yet applied | Apply after LELO |
| 3 | **We-Vibe** | Impact | Up to 22% | [Impact signup](https://app.impact.com/campaign-promo-signup/We-Vibe-Europe.brand) | app.impact.com after approval | 🟡 Candidate — Not yet applied | Apply (same network as Womanizer) |
| 4 | **SheVibe** | Impact | 10% | [Impact signup](https://app.impact.com/campaign-promo-signup/The-Vibe-Tribe-SheVibes-Partner-Program.brand) | app.impact.com after approval | 🟡 Candidate — Not yet applied | Apply (same Impact network) |
| 5 | **Adam & Eve** | Pepperjam | Up to 30% | [Pepperjam signup](https://www.pepperjamnetwork.com/affiliate/registration.php?refid=107783) | Pepperjam dashboard after approval | 🟡 Candidate — Not yet applied | Apply (US market focus) |
| 6 | **Bellesa/BBoutique** | Awin | Not specified | [Awin merchant page](https://ui.awin.com/merchant-profile/15527) | Awin dashboard after approval | 🟡 Candidate — Not yet applied | Optional — apply if Awin preferred |
| 7 | **Amazon Associates** | Amazon | 1–3% | [Amazon Associates](https://affiliate-program.amazon.com/) | affiliate-program.amazon.com | 🟡 Needs policy review | **LAST** — high policy risk |

### Alternative Networks for LELO (if direct fails)
- Rakuten LinkShare: https://cli.linksynergy.com/
- CJ Affiliate: https://members.cj.com/
- TimeOne: https://www.timeone.io/

### Lovehoney (Declined — Reapply Later)
| Name | Status | Note |
|------|--------|------|
| Lovehoney | 🔴 Declined 2026-07-29 | Wait 2-3 months, grow traffic, then reapply |

---

## 3. Ordered Rollout Plan

### Phase 1: LELO Direct (Week 1)
- [ ] Apply at http://lip.hasoffers.com/signup
- [ ] Use application template (see Section 6)
- [ ] Wait for approval email (typically 3-7 days)
- [ ] Upon approval: obtain tracking ID from dashboard

### Phase 2: Impact Network Trio (Week 1-2)
Apply to all three (same network = single dashboard):
- [ ] Womanizer via Impact
- [ ] We-Vibe via Impact  
- [ ] SheVibe via Impact

### Phase 3: Adam & Eve (Week 2-3)
- [ ] Apply via Pepperjam
- [ ] Note: US-market focus, highest commission (up to 30%)

### Phase 4: Optional/Additional (Week 3-4)
- [ ] Bellesa via Awin (if desired)
- [ ] Research Spectrum Boutique (pending)

### Phase 5: Amazon LAST (Week 6-8, if at all)
- [ ] Review Amazon's "Unsuitable Sites" policy thoroughly
- [ ] Adult content policy risk — may reject adult toy review sites
- [ ] Consider only for non-adult accessories if approved
- [ ] **Only apply after other programs established**

---

## 4. Implementation Steps (Post-Approval)

### Step 1: Obtain Tracking ID
After each approval, login to the respective dashboard and locate your:
- **Tracking ID** (sometimes called "Affiliate ID" or "Publisher ID")
- **Base URL format** for creating product links

### Step 2: Update Configuration File
Edit `affiliate-config.json` in site root:

```json
{
  "trackingPrefixes": {
    "lelo": "YOUR_ACTUAL_LELO_ID",
    "womanizer": "YOUR_ACTUAL_WOMANIZER_ID",
    "wevibe": "YOUR_ACTUAL_WEVIBE_ID",
    "shevibe": "YOUR_ACTUAL_SHEVIBE_ID",
    "adameve": "YOUR_ACTUAL_ADAMEVE_ID",
    "amazon": "YOUR_ACTUAL_AMAZON_TAG"
  }
}
```

Replace `AFFILIATE_ID_*` placeholders with real tracking IDs.

### Step 3: Update Product Front Matter
For each product, edit its `index.md` offers array:

```yaml
offers:
  - retailer: "LELO"
    url: "https://www.lelo.com/sona-2?aff=YOUR_LELO_ID"
    price: 179.99
    currency: "USD"
    checked: "2026-08-03"
    available: true          # ← Set to true to enable link
  - retailer: "Amazon"
    url: "https://amazon.com/dp/XXXX?tag=YOUR_AMAZON_TAG"
    price: 179.99
    currency: "USD"
    checked: "2026-08-03"
    available: true
```

**Key fields:**
- `url`: Full affiliate URL with tracking parameter
- `available: true`: Enables the link button
- `checked`: Date of price verification

### Step 4: Redeploy
After all changes:
```bash
./deploy.sh
```

This rebuilds the Hugo site and syncs to hosting.

### Step 5: Verify Live
- Check product pages show affiliate buttons
- Click-test links (use incognito to avoid cookie issues)
- Verify disclosure banner appears

---

## 5. Dashboard Explanation

### What the Dashboard Shows You

After signing up for any program, you may see:
- **Status:** "Pending Approval" or "Application Received"
- **Site:** `reviews.ultramarine963.com` (Venus domain)

### What This Means
If your dashboard shows `reviews.ultramarine963.com` as a registered site:
1. ✅ Your site is **registered/approved** in the network
2. 🔄 **Next steps:** Obtain your tracking ID
3. 🔄 **Then:** Add ID to `affiliate-config.json`
4. 🔄 **Then:** Update product URLs + `available: true`
5. 🔄 **Then:** Run `deploy.sh` to go live

### How to Find Your Tracking ID
| Network | Where to Find Tracking ID |
|---------|---------------------------|
| HasOffers (LELO) | Dashboard → Account Settings → API/Tracking |
| Impact | Dashboard → Account → Publisher ID |
| Pepperjam | Dashboard → Account Info → PID |
| Awin | Dashboard → Account → Publisher ID |
| Amazon Associates | Account Settings → Tracking ID |

---

## 6. Application Template

Use these answers when applying to affiliate programs:

| Field | Suggested Answer |
|-------|------------------|
| **Website URL** | https://reviews.ultramarine963.com/ |
| **Site Type** | Independent sexual wellness review and buying-guide site for adults |
| **Audience** | Adults comparing premium pleasure products with privacy, materials, noise, cleaning, and warranty context |
| **Promotion Methods** | SEO articles, product reviews, comparison pages, buying guides. No paid search bidding on brand terms. |
| **Why This Merchant** | Venus publishes product-specific reviews with privacy-first editorial style and clear affiliate disclosure |
| **Content Quality** | Original review copy and buying guides; no scraped retailer copy, no copied Amazon reviews, no misleading partnership claims |
| **Compliance Statement** | Venus uses only approved links, discloses affiliate compensation clearly, follows network terms |

---

## 7. Risk Summary

| Program | Risk Level | Notes |
|---------|------------|-------|
| Amazon Associates | 🔴 HIGH | "Unsuitable Sites" policy excludes adult content; apply LAST only |
| Lovehoney | 🟡 MEDIUM | Already declined once; reapply later with more traffic |
| All others | 🟢 LOW | Adult-native programs, well-established, no policy conflicts |

---

## 8. Key Files Reference

| File | Purpose |
|------|---------|
| `affiliate-config.json` | Master affiliate registry + tracking IDs |
| `layouts/partials/comparison-block.html` | Price comparison table template |
| `layouts/partials/best-offer-display.html` | Best price display template |
| `content/products/*/index.md` | Product pages with offers array |
| `/affiliate-disclosure/index.html` | FTC disclosure page |

---

## 9. Quick Checklist for Paul

### Immediate (This Week)
- [ ] Apply to LELO: http://lip.hasoffers.com/signup
- [ ] Apply to Womanizer via Impact
- [ ] Apply to We-Vibe via Impact

### Short-term (Next 2 Weeks)
- [ ] Receive approvals and tracking IDs
- [ ] Update `affiliate-config.json`
- [ ] Implement links on top 5 products
- [ ] Run `deploy.sh` and verify

### Medium-term (Next Month)
- [ ] Apply to Adam & Eve (Pepperjam)
- [ ] Apply to SheVibe (Impact)
- [ ] Full product catalog coverage
- [ ] Consider Amazon (policy review first)

---

*Document consolidated from: AFFILIATE-RESEARCH.md, VENUS-IMAGERY-AND-GROWTH-PLAN-20260803.md, affiliate-config.json*  
*Priority order verified: LELO → Womanizer → We-Vibe → SheVibe → Adam & Eve → Bellesa → Amazon LAST*  
*Lovehoney: DECLINED 2026-07-29 — reapply later*
