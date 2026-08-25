# Venus Affiliate Credentials — Drop Tracking IDs Here

**Date created:** 2026-08-06 · **Updated:** 2026-08-25
**Source of truth:** `impact-onboarding-report.md` (2026-08-24)

> ⚠️ **DEPLOYMENT NOTE:** This planning doc lives in the deploy branch root. Post-2026-08-25 JSON-exposure fix, planning docs should be moved OUT of the deployed tree.

**Target:** Paul drops real tracking IDs here as approvals land.

---

## Impact (Womanizer · We-Vibe · SheVibe)

| Partner | Status | Tracking ID / Deep Link | Notes |
|---------|--------|------------------------|-------|
| Womanizer | ⏳ Not applied — onboarding blocked | `_________________` | URL: http://app.impact.com/campaign-campaign-info-v2/Womanizer-North-America.brand |
| We-Vibe | ⏳ Not applied — onboarding blocked | `_________________` | URL: http://app.impact.com/campaign-campaign-info-v2/We-Vibe-Europe.brand |
| SheVibe | ⏳ Not applied — onboarding blocked | `_________________` | URL: https://app.impact.com/campaign-promo-signup/The-Vibe-Tribe-SheVibes-Partner-Program.brand |

### Impact Account Credentials
> **Login:** `https://app.impact.com`
> **Username:** `paulpawprints`
> **Account ID:** `7454049`
> **Password (manager):** Stored securely per policy
> **Blocker:** Partner Program Agreement checkbox must be checked manually to complete onboarding

---

## Direct Programs

| Partner | Status | Tracking ID | URL |
|---------|--------|-------------|-----|
| LELO | ❌ **REJECTED** Aug 20, 2026 | N/A — account rejected | http://lip.hasoffers.com/signup |
| Adam & Eve | ⏳ **Pending** — submitted Aug 5 | `_________________` | https://www.pepperjamnetwork.com/affiliate/registration.php?refid=107783 |
| Bellesa/BBoutique | ✅ **LIVE since 2026-08-17** | **Awin Publisher ID: 3022209** | https://ui.awin.com/merchant-profile/15527 (Awin) |

---

## Blocked / Future / Rejected

| Partner | Status | Notes |
|---------|--------|-------|
| Lovehoney | ❌ Declined 2026-07-29 | Reason: "Brand alignment mismatch". Reapply once traffic/content grows. |
| LELO | ❌ Rejected Aug 20, 2026 | LIP/HasOffers account rejected. Email `affiliates@lelo.com` for specifics before reapplying. |
| Amazon Associates | ⚠️ High policy risk | Only for non-adult accessories, last resort |
| Spectrum Boutique | ❓ Needs research | Affiliate program not verified |

## LELO Reapplication Strategy

**Option A: Reapply with improved positioning**
1. Wait until Venus site has 10+ product reviews with substantial content
2. Ensure BBoutique/Awin links showing live traffic
3. Reapply via LIP with updated positioning

**Option B: Contact LELO directly**
1. Email `affiliates@lelo.com` for specific feedback on rejection
2. Ask what "missing information" or "brand alignment" issues existed

**Recommendation:** Start with Option B (email for specifics).

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