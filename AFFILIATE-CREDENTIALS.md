# Venus Affiliate Credentials — Drop Tracking IDs Here

**Date created:** 2026-08-06
**Target:** Paul drops real tracking IDs here as approvals land.

---

## Impact (Womanizer · We-Vibe · SheVibe)

| Partner | Status | Tracking ID / Deep Link | Notes |
|---------|--------|------------------------|-------|
| Womanizer | ❌ Not applied | `_________________` | App via Impact — URL: http://app.impact.com/campaign-campaign-info-v2/Womanizer-North-America.brand |
| We-Vibe | ❌ Not applied | `_________________` | App via Impact — URL: http://app.impact.com/campaign-campaign-info-v2/We-Vibe-Europe.brand |
| SheVibe | ❌ Not applied | `_________________` | App via Impact — URL: https://app.impact.com/campaign-promo-signup/The-Vibe-Tribe-SheVibes-Partner-Program.brand?execution=e1s1#/?viewkey=signUpPreStart |

### Impact Account Credentials
> **Login:** `https://app.impact.com`
> **Email used:** _________________
> **Password (manager):** Stored securely per policy

---

## Direct Programs

| Partner | Status | Tracking ID | URL |
|---------|--------|-------------|-----|
| LELO | ❌ Not applied | `_________________` | http://lip.hasoffers.com/signup |
| Adam & Eve | ❌ Not applied | `_________________` | https://www.pepperjamnetwork.com/affiliate/registration.php?refid=107783 |
| Bellesa/BBoutique | ❌ Not applied | `_________________` | https://ui.awin.com/merchant-profile/15527 (Awin) |

---

## Blocked / Future

| Partner | Status | Notes |
|---------|--------|-------|
| Lovehoney | ❌ Declined 2026-07-29 | Reapply once traffic grows |
| Amazon Associates | ⚠️ High policy risk | Only for non-adult accessories, last resort |
| Spectrum Boutique | ❓ Needs research | Affiliate program not verified |

---

## How to Activate a Partner

Once you have a real tracking ID:

1. **Update `affiliate-config.json`** — paste ID into `trackingPrefixes.{partner}`
2. **Update product front matter** — for each relevant product's `index.md`, fill:
   ```yaml
   offers:
     - retailer: "PARTNER_NAME"
       url: "https://partner.com/product?aff=YOUR_TRACKING_ID"
       price: 99.99
       currency: "USD"
       checked: "2026-08-06"
       available: true
   ```
3. **Deploy:**
   ```bash
   cd /home/paul/.openclaw/workspaces/assistant/venus-worktree
   ./deploy.sh
   ```
4. **Verify** — visit the product page, confirm the affiliate button renders and click-through works.