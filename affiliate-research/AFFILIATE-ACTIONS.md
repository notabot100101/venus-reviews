# Affiliate Program Implementation - Action Checklist

**Status:** All links currently DISABLED | **Goal:** Get first live affiliate link within 2 weeks

---

## Immediate Actions (Week 1)

### ☐ Step 1: Apply to LELO (Direct Brand Match)
- [ ] Visit: http://lip.hasoffers.com/signup
- [ ] Or: https://www.lelo.com/affiliates
- [ ] Expected commission: 5-20%
- [ ] Expected approval: 3-7 days
- [ ] Note your tracking ID once approved

### ☐ Step 2: Create Impact Account (3 programs in one)
- [ ] Visit: https://app.impact.com/signup
- [ ] This one signup covers: Womanizer, We-Vibe, SheVibe
- [ ] Apply to all three programs once account is created

### ☐ Step 3: Apply via Impact
- [ ] Womanizer: http://app.impact.com/campaign-campaign-info-v2/Womanizer-North-America.brand
- [ ] We-Vibe: http://app.impact.com/campaign-campaign-info-v2/We-Vibe-Europe.brand  
- [ ] SheVibe: https://app.impact.com/campaign-promo-signup/The-Vibe-Tribe-SheVibes-Partner-Program.brand?execution=e1s1
- [ ] Expected commission: up to 22% (Womanizer/We-Vibe), 10% (SheVibe)

---

## Short-Term Actions (Week 2-3)

### ☐ Step 4: Update Tracking IDs
Once approved, update `/affiliate-config.json`:

```json
{
  "trackingPrefixes": {
    "lelo": "YOUR_ACTUAL_LELO_ID",
    "womanizer": "YOUR_IMPACT_ID",
    "wevibe": "YOUR_IMPACT_ID", 
    "shevibe": "YOUR_IMPACT_ID"
  }
}
```

### ☐ Step 5: Activate Links on Priority Products
Start with these products (best traffic potential):
- [ ] content/products/lelo-sona-2/index.md
- [ ] content/products/lelo-mona/index.md
- [ ] content/products/womanizer-2-original/index.md
- [ ] content/products/we-vibe-chorus/index.md

For each product, update the `offers` array:
```yaml
offers:
  - retailer: "LELO"
    url: "https://www.lelo.com/sona-2?aff=YOUR_TRACKING_ID"
    price: 179.99
    currency: "USD"
    checked: "2026-07-30"
    available: true
```

### ☐ Step 6: Test Links
- [ ] Build site: `hugo --gc --minify`
- [ ] Check HTML output for correct hrefs
- [ ] Verify tracking parameter is included
- [ ] Click test links (don't buy through them yet)

---

## Medium-Term Actions (Month 2)

### ☐ Step 7: Apply to Adam & Eve
- [ ] Visit: https://www.pepperjamnetwork.com/affiliate/registration.php?refid=107783
- [ ] Or: https://www.adameve.com/t-affiliate.aspx
- [ ] Commission: up to 30%
- [ ] Network: Pepperjam

### ☐ Step 8: Consider Bellesa/BBoutique
- [ ] Via Awin: https://ui.awin.com/merchant-profile/15527
- [ ] Commission: not specified publicly

### ☐ Step 9: Amazon Associates Decision
- [ ] Review policy risk in full research document
- [ ] Make go/no-go decision
- [ ] If go: apply at https://affiliate-program.amazon.com/signup
- [ ] Be prepared for possible rejection due to adult content policy

---

## Administrative

### ☐ Step 10: Document Your IDs
Create a private file (NOT in git) with:
- LELO tracking ID
- Impact account details
- Pepperjam credentials
- Any other network logins

### ☐ Step 11: Set Calendar Reminder
- [ ] Check affiliate dashboards monthly
- [ ] Update prices weekly (or set up automation)
- [ ] Review top-performing links quarterly

---

## Expected Results

| Program | Expected Commission | Min Cookie | Time to First $ |  
|---------|---------------------|------------|-----------------|
| LELO | 5-20% | Unknown | 2-4 weeks |
| Womanizer/We-Vibe | up to 22% | Impact std | 4-6 weeks |
| SheVibe | 10% | Impact std | 4-6 weeks |
| Adam & Eve | up to 30% | 30-90 days | 6-8 weeks |

---

## Questions?

See full research document: `AFFILIATE-RESEARCH.md`

**Blockers?** Check the troubleshooting section in the full report.
