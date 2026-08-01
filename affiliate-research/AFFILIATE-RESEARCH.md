# Venus Affiliate Program Implementation Research

**Date:** 2026-07-30  
**Researcher:** Subagent Analysis  
**Purpose:** Answer Paul's questions about affiliate program implementation status and next steps

---

## Executive Summary

**Status:** ⚠️ **AFFILIATE LINKS ARE NOT LIVE** - All affiliate links are currently disabled/placeholder. Links will NOT work by default.

**What Paul needs to know:**
1. The links from Hermes' list will NOT work automatically - they require approval, tracking IDs, and implementation
2. There IS an existing implementation framework, but it's in "candidate" mode with all links disabled
3. Current priority order: LELO → Womanizer/We-Vibe (Impact) → SheVibe → Adam & Eve → Amazon (policy risk)

---

## 1. Current Affiliate Configuration State

### State of Configuration Files

| File | Status | Purpose |
|------|--------|---------|
| `/affiliate-config.json` | ✅ Current | Main affiliate program registry with updated statuses |
| `/data/affiliate-config.json` | ⚠️ Outdated | Legacy config from earlier implementation |
| `/AFFILIATE-PROGRAMS.md` | ✅ Current | Application tracker and research notes |
| `/affiliate-setup.md` | ✅ Current | Application status tracking |

### Current Implementation Framework

The Venus site uses a **Hugo partial-based system** for affiliate links:

1. **Template:** `layouts/partials/comparison-block.html` - Renders price comparison tables
2. **Template:** `layouts/partials/best-offer-display.html` - Shows best available price
3. **Data Source:** Product front matter (`offers` array in each product's `index.md`)

### How Affiliate Links Currently Work

**Product Front Matter Structure (in each product's index.md):**
```yaml
offers:
  - retailer: "Amazon"
    url: ""                              # ← Empty = disabled
    price: null                          # ← No price shown
    currency: "EUR"
    checked: ""                          # ← Empty = stale/hidden
    available: false                     # ← False = disabled button
  - retailer: "Lovehoney"
    url: ""
    price: null
    currency: "EUR"
    checked: ""
    available: false
  # ... more retailers
```

**Rendering Logic:**
- Links only render when `url != ""` AND `available == true`
- Prices only show when `price` exists AND `checked` date exists AND price is <7 days old
- Button text shows "Coming soon" / "Affiliate link pending" when disabled

### Current Program Status Summary

| Program | Status | Has Tracking ID | Links Live |
|---------|--------|-----------------|------------|
| **Lovehoney** | ❌ Declined (2026-07-29) | No | No |
| **LELO** | 🟡 Candidate - Apply | No | No |
| **Womanizer** | 🟡 Candidate - Apply | No | No |
| **We-Vibe** | 🟡 Candidate - Apply | No | No |
| **SheVibe** | 🟡 Candidate - Apply | No | No |
| **Adam & Eve** | 🟡 Candidate - Apply | No | No |
| **Bellesa/BBoutique** | 🟡 Candidate - Apply | No | No |
| **Amazon Associates** | 🟡 Needs Policy Review | No | No |
| **Spectrum Boutique** | 🔴 Research Needed | No | No |

---

## 2. Answer to Paul's Questions

### Q1: Will those links work by default automatically on the Venus site?

**NO** ❌

**Explanation:**
- The links are currently **placeholders with empty URLs** (`""`)
- No affiliate tracking IDs are configured
- Lovehoney (the only one previously applied) was **declined** on 2026-07-29
- The system requires:
  1. ✅ Approval from each affiliate program
  2. ✅ Real tracking IDs assigned
  3. ✅ URLs populated in product front matter
  4. ✅ `available: true` flag set
  5. ✅ Real-time price scraping (optional)

### Q2: What do we need to do to implement them?

**Implementation Steps:**

#### Phase 1: Apply to Programs (Paul's Action Required)
1. **LELO** - Apply at http://lip.hasoffers.com/signup (5-20% commission)
2. **Womanizer** - Apply via Impact at http://app.impact.com/... (up to 22% commission)
3. **We-Vibe** - Apply via Impact at http://app.impact.com/... (up to 22% commission)
4. **SheVibe** - Apply via Impact at https://app.impact.com/...signup (10% commission)
5. **Adam & Eve** - Apply via Pepperjam (up to 30% commission)
6. **Amazon Associates** - Review policy risk first (policy restrictions on adult content)

#### Phase 2: Configure Tracking IDs (Technical)
1. Once approved, insert real affiliate IDs into `affiliate-config.json`
2. Update `trackingPrefixes` section with actual IDs (not placeholders)

#### Phase 3: Update Product Links (Content)
1. For each product, populate the `offers` array in front matter:
   ```yaml
   offers:
     - retailer: "LELO"
       url: "https://www.lelo.com/sona-2?AFF_ID=venus123"
       price: 179.99
       currency: "USD"
       checked: "2026-07-30"
       available: true
   ```

#### Phase 4: Enable Links (Testing)
1. Test all links render correctly
2. Verify disclosure is visible
3. Check FTC compliance

---

## 3. Affiliate Program Comparison

### Paul's Programs from Hermes + Amazon

| Program | Network | Commission | Cookie | Adult Safe? | Approval Difficulty | Best For |
|---------|---------|------------|--------|-------------|---------------------|----------|
| **LELO** | Direct/HasOffers | 5-20% | Not stated | ✅ Yes | Medium | Direct brand reviews |
| **Womanizer** | Impact | Up to 22% | Impact terms | ✅ Yes | Medium | Direct brand reviews |
| **We-Vibe** | Impact | Up to 22% | Impact terms | ✅ Yes | Medium | Direct brand reviews |
| **SheVibe** | Impact | 10% | Impact terms | ✅ Yes | Medium | Multi-brand retailer |
| **Adam & Eve** | Pepperjam | Up to 30% | 30-90 days | ✅ Yes | Medium | US-market broad |
| **Amazon Associates** | Amazon | 1-3% | 24 hours | ⚠️ Risk | Hard | Last resort only |

### Additional Recommended Programs

| Program | Network | Commission | Cookie | Adult Safe? | Why Consider |
|---------|---------|------------|--------|-------------|--------------|
| **Bellesa/BBoutique** | Awin | Not specified | Awin terms | ✅ Yes | Women-focused, high brand recognition |
| **Spectrum Boutique** | Unknown | Unknown | Unknown | ✅ Probably | UK/EU focused |
| **Lovehoney (reapply)** | Previous network | Unknown | Unknown | ✅ Yes | Previously declined - reapply later |

---

## 4. Detailed Program Analysis

### LELO Affiliate Program
- **URL:** https://www.lelo.com/affiliates
- **Signup:** http://lip.hasoffers.com/signup
- **Also on:** Rakuten LinkShare, CJ, TimeOne
- **Commission:** 5-20%
- **Best For:** Venus has multiple LELO product reviews (Sona 2, Mona 2, Enigma, Hugo)
- **Pros:** Direct brand match, high commission, premium products
- **Cons:** Need separate applications for different regions

### Womanizer Affiliate Program
- **URL:** https://www.womanizer.com/us/affiliate-marketing
- **Signup:** Impact platform
- **Commission:** Up to 22%
- **Benefits:** Product review program, sample program, dedicated support
- **Best For:** Womanizer product pages
- **Cons:** Single brand focus

### We-Vibe Affiliate Program
- **URL:** https://www.we-vibe.com/us/affiliate-marketing
- **Signup:** Impact platform
- **Commission:** Up to 22%
- **Benefits:** Same as Womanizer (both owned by same company)
- **Best For:** We-Vibe Chorus, Sync products

### SheVibe Affiliate Program
- **URL:** https://shevibe.com/pages/affiliate-program
- **Signup:** Impact platform
- **Commission:** 10%
- **Best For:** Broad product catalog coverage
- **Pros:** Adult-native retailer, extensive catalog, 10% commission is solid
- **Cons:** Lower commission than direct brands

### Adam & Eve Affiliate Program
- **URL:** https://www.adameve.com/t-affiliate.aspx
- **Signup:** Pepperjam network
- **Commission:** Up to 30%
- **Best For:** US market broad coverage
- **Pros:** Highest commission rate, established brand
- **Cons:** US-only, Pepperjam network learning curve

### Amazon Associates - Policy Warning ⚠️
- **URL:** https://affiliate-program.amazon.com/
- **Commission:** 1-3% (product category dependent)
- **Cookie:** 24 hours
- **Policy Risk:** Amazon's "Unsuitable Sites" policy excludes sites with "sexually explicit or obscene materials"
- **Current Status:** Venus Reviews content MAY trigger rejection
- **Recommendation:** Apply ONLY after other programs are established, with full awareness of policy risk
- **Alternative:** Consider only for non-adult accessories (chargers, storage cases, cleaning products)

---

## 5. Implementation Requirements

### Technical Requirements

1. **Tracking ID Storage**
   - File: `affiliate-config.json` (root level)
   - Section: `trackingPrefixes` → replace `AFFILIATE_ID_*` placeholders with real IDs

2. **Product URL Generation**
   - Each product needs exact URLs with tracking parameters
   - Example: `https://www.lelo.com/sona-2?aff=PAUL_TRACKING_ID`
   - Store in product front matter under `offers[].url`

3. **Price Scraping (Optional but Recommended)**
   - Current: Manual entry in front matter
   - Automated: Would require scraper for each retailer
   - Recommendation: Start manual, automate later

4. **Disclosure Requirements**
   - Current disclosure page: `/affiliate-disclosure/index.html`
   - Inline banners already implemented (see `comparison-block.html`)
   - FTC compliance: ✅ Already in place

### Content Updates Needed

For each of the ~12 products currently on site:

```yaml
# Example: content/products/lelo-sona-2/index.md
offers:
  - retailer: "LELO"
    url: "https://www.lelo.com/sona-2?aff=PAUL_TRACKING_ID"
    price: 179.99
    currency: "USD"
    checked: "2026-07-30"
    available: true
  - retailer: "Amazon"
    url: "https://www.amazon.com/lelo-sona-2?tag=PAUL_AMAZON_TAG"
    price: 179.99
    currency: "USD"
    checked: "2026-07-30"
    available: true
  # ... other retailers
```

---

## 6. Implementation Roadmap

### Immediate (This Week)
- [ ] Paul applies to LELO affiliate program
- [ ] Paul applies to Womanizer via Impact
- [ ] Paul applies to SheVibe via Impact

### Short-term (Next 2 Weeks)
- [ ] Receive approvals and tracking IDs
- [ ] Update `affiliate-config.json` with real tracking IDs
- [ ] Implement affiliate links on top 5 product pages
- [ ] Test link rendering and click-through

### Medium-term (Next Month)
- [ ] Apply to Adam & Eve (Pepperjam)
- [ ] Apply to We-Vibe (Impact)
- [ ] Implement links on all product pages
- [ ] Consider Amazon Associates (after policy review)

### Ongoing
- [ ] Weekly price updates (manual or automated)
- [ ] Monitor affiliate dashboard for performance
- [ ] Track click-through rates
- [ ] Consider additional programs if earning/p>
n
---

## 7. Risk Assessment

### Amazon Associates Risk
**Level:** HIGH ⚠️
- Amazon explicitly excludes "sexually explicit or obscene materials"
- Adult toy review sites have been rejected/terminated
- **Mitigation:** Get other programs approved first, use Amazon only for non-adult accessories

### Lovehoney Rejection Risk
**Level:** MEDIUM
- Already declined once (2026-07-29)
- **Mitigation:** Wait until site has more content/traffic, then reapply

### Network Consolidation Risk
**Level:** LOW
- Womanizer, We-Vibe, SheVibe all use Impact
- Single dashboard for 3 programs
- **Benefit:** Easier management

### Commission Rate Risk
**Level:** LOW
- Adult affiliate programs are well-established
- Rates are competitive (5-30%)
- **Benefit:** Higher than Amazon's 1-3%

---

## 8. Application Quick-Start Guide

### Suggested Application Answers (Use as Template)

**Website URL:** https://reviews.ultramarine963.com/

**Site Type:** Independent sexual wellness review and buying-guide site for adults

**Audience:** Adults comparing premium pleasure products with privacy, materials, noise, cleaning, and warranty context

**Promotion Methods:** SEO articles, product reviews, comparison pages, buying guides. No paid search bidding on brand terms.

**Why This Merchant:** Venus already publishes product-specific reviews with privacy-first editorial style and clear affiliate disclosure

**Content Quality:** Original review copy and buying guides; no scraped retailer copy, no copied Amazon reviews, no misleading partnership claims

**Compliance Statement:** Venus will use only approved links, disclose affiliate compensation clearly, follow network terms

---

## 9. Summary & Recommendations

### Will Links Work Automatically?
**NO.** All are currently disabled placeholders. Paul needs to:
1. Apply to programs
2. Get approved
3. Add tracking IDs
4. Update product URLs

### Implementation Complexity
**MEDIUM.**
- Framework exists ✅
- Templates are ready ✅
- Disclosure is compliant ✅
- Need approvals and data entry

### Recommended Priority
1. **LELO** - Direct brand match for existing reviews
2. **Womanizer + SheVibe** (same Impact network)
3. **We-Vibe** (Impact network)
4. **Adam & Eve** (highest commission, Pepjham
5. **Amazon** - Last, after policy review

### Expected Timeline
- **To first live affiliate link:** 1-2 weeks (LELO direct usually fast)
- **To full program coverage:** 4-6 weeks (Impact network approvals)
- **To Amazon (if attempted):** 6-8 weeks (plus risk assessment)

---

## Files Referenced

- `/home/paul/.openclaw/workspaces/worker/venus-site/affiliate-config.json` - Master configuration
- `/home/paul/.openclaw/workspaces/worker/venus-site/AFFILIATE-PROGRAMS.md` - Application tracker
- `/home/paul/.openclaw/workspaces/worker/venus-site/layouts/partials/comparison-block.html` - Price table template
- `/home/paul/.openclaw/workspaces/worker/venus-site/layouts/partials/best-offer-display.html` - Best price template
- `/home/paul/.openclaw/workspaces/worker/venus-site/content/products/*/index.md` - Product pages with offer data

---

*End of Research Report - Ready for Paul's Review*