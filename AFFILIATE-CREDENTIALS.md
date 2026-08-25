# Venus Affiliate Credentials — Tracking IDs & Status

**Date created:** 2026-08-06 · **Updated:** 2026-08-25
**Source of truth:** `workspace/main/impact-onboarding-report.md` (2026-08-24)

> ⚠️ **Previous version was stale.** BBoutique was listed as "Not applied" — it has been LIVE since 2026-08-17. Impact partners were listed as "Not applied" — the real blocker is incomplete Impact onboarding, not lack of applications.
>
> **Security note:** This doc lives in the deploy branch root, masked only by `.htaccess`. Consider moving planning docs out of the deployed tree (follow-up from 2026-08-25 JSON-exposure fix).

---

## Impact (Womanizer · We-Vibe · SheVibe)

| Partner | Status | Tracking ID / Deep Link | Notes |
|---------|--------|------------------------|-------|
| Womanizer | ⏳ Not applied | `_________________` | App via Impact — BLOCKED by incomplete onboarding |
| We-Vibe | ⏳ Not applied | `_________________` | App via Impact — BLOCKED by incomplete onboarding |
| SheVibe | ⏳ Not applied | `_________________` | App via Impact — BLOCKED by incomplete onboarding |

### Impact Account Credentials
> **Login:** `https://app.impact.com`
> **Email used:** _________________
> **Password (manager):** Stored securely per policy

---

## Direct Programs

| Partner | Status | Tracking ID | URL |
|---------|--------|-------------|-----|
| LELO | ❌ Rejected (Aug 20) | `_________________` | http://lip.hasoffers.com/signup — "missing information or misalignment with our brand" |
| Adam & Eve | ⏳ Pending | `_________________` | https://www.pepperjamnetwork.com/affiliate/registration.php?refid=107783 — Submitted Aug 5, awaiting review |
| Bellesa/BBoutique | ✅ LIVE | `3022209` | https://ui.awin.com/merchant-profile/15527 (Awin) — Active on all product pages since 2026-08-17 |

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