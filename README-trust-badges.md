# Trust Badges for Venus Website

## Generated Badges

All badges are SVG format for scalability and SEO.

### 1. Discreet Shipping Badge
**File:** `trust-badges/discreet-shipping.svg`
**Text:** "Discreet Shipping - Free & Fast"
**Colors:** Gray scale, professional

### 2. Secure Checkout Badge
**File:** `trust-badges/secure-checkout.svg`
**Text:** "Secure Checkout - 256-bit SSL"
**Colors:** Green accent, trustworthy

### 3. 18+ Age Verification Badge
**File:** `trust-badges/18-plus.svg`
**Text:** "18+ Age Verified"
**Colors:** Dark with gold accent

### 4. Privacy Protected Badge
**File:** `trust-badges/privacy-protected.svg`
**Text:** "Privacy Protected - Discreet"
**Colors:** Blue accent, secure

## Implementation

Add to all pages footer section:

```html
<footer class="site-footer">
  <div class="trust-badges">
    <img src="/trust-badges/discreet-shipping.svg" alt="Discreet Shipping Badge" />
    <img src="/trust-badges/secure-checkout.svg" alt="Secure Checkout Badge" />
    <img src="/trust-badges/18-plus.svg" alt="18+ Age Verified Badge" />
    <img src="/trust-badges/privacy-protected.svg" alt="Privacy Protected Badge" />
  </div>
</footer>
```

## Mobile Responsiveness

Badges are:
- ✅ Visible on mobile (stacked vertically)
- ✅ Touch-friendly (adequate spacing)
- ✅ SVG format (scales to any size)
- ✅ Fast loading (small file size)

## Alternative: PNG Versions

If SVG not supported, convert to PNG:
- `trust-badges/png/discreet-shipping.png` (100x40px)
- `trust-badges/png/secure-checkout.png` (100x40px)
- `trust-badges/png/18-plus.png` (100x40px)
- `trust-badges/png/privacy-protected.png` (100x40px)
