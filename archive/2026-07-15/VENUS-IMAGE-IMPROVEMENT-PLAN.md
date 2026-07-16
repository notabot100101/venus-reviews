# Venus Reviews - Image Improvement Plan

**Date:** 2026-07-08  
**Project:** Continuous product visual improvement for all 15 products  
**Team:** Architect (coordination), Pixel (asset creation), Forge (integration/optimization), Sophia (communication)

---

## Current State Audit

### Product Inventory
- **Total Products:** 15 (from PRODUCT-CATALOG.md)
- **Active Product Folders:** 17 in `products/` directory
- **Existing Images:** 69 files in `images/products/`
- **Current Layout:** Single-angle product shots with badges

### Image Requirements Per Product
Each product needs:
1. **Front/Main** - Primary product image (current state)
2. **Alternate Angles** - 3-4 views (top, side, angled, detail)
3. **Scale/Context** - Size reference shot
4. **Packaging** - Retail box shot (if available)
5. **Lifestyle** - Contextual scene (bath, bedroom, storage)
6. **Thumbnail** - Compressed web-optimized version

**Total Per Product:** 6-8 images (front + 3 angles + scale + packaging + lifestyle + thumb)

---

## Quality Gates

### Visual Fit
- Accurate representation (no misleading scale)
- Consistent lighting/style across all products
- No overlapping/occluded elements

### Mobile/Desktop Layout
- No horizontal overflow on mobile
- Responsive srcset implementation
- Blur-up loading for better performance

### Alt Text
- Descriptive and accurate
- Non-misleading affiliate-safe language
- Keywords: product name, key features, colors

### Affiliate Safety
- All disclosure links present
- No misleading claims about pricing
- No fake scarcity or urgency

---

## File Naming Convention

```
product-{slug}-front.webp       # Main hero image
product-{slug}-angle-01.webp    # Top/overhead view
product-{slug}-angle-02.webp    # Side profile view
product-{slug}-angle-03.webp    # Angled 3-quarter view
product-{slug}-angle-04.webp    # Detail/close-up view (optional)
product-{slug}-scale.webp       # Size context shot
product-{slug}-packaging.webp   # Retail packaging
product-{slug}-lifestyle.webp   # Contextual scene
product-{slug}-thumb.webp       # Thumbnail version
```

---

## Batch Structure

### Batch Size: 2-3 Products Per Cycle
**Rationale:** Small bounded batches for verification; sequential Pixel→Forge flow.

### Batch Assignment
- **Batch 1:** lelo-mona, womanizer-2 (Premium tier, highest revenue)
- **Batch 2:** lelo-enigma, dame-eva-ii (Premium, diverse tech)
- **Batch 3:** we-vibe-chorus, we-vibe-sync (Couples wearables)
- **Batch 4:** fun-factory-manta, fun-factory-volta (Value tier)
- **Batch 5:** lelo-hugo, lelo-sona-2 (App-controlled)
- **Batch 6:** lovehoney-desire, satisfyer-pro-2 (Mid-range)
- **Batch 7:** h2o-holo-vibe, bvee-rabbit (Innovation tier)
- **Batch 8:** lelo-gigi-2 (Completes catalog)

---

## First Batch: lelo-mona & womanizer-2

### Tasks for Pixel (Sequential)
1. Generate lelo-mona:
   - Front view (existing may suffice with optimization)
   - 3 alternate angles (top, side, angled)
   - Scale shot with object reference
   - Lifestyle scene (bathroom counter)
   - Thumbnail version

2. Generate womanizer-2:
   - Front view
   - 3 alternate angles
   - Scale shot
   - Lifestyle scene
   - Thumbnail version

### Output Location
- `images/products/lelo-mona/{slug}-front.webp`
- `images/products/lelo-mona/{slug}-angle-01.webp`
- ...etc
- `images/products/womanizer-2/` (similar structure)

### Output Volume
- **2 products × 6 images = 12 new images**
- **Formats:** PNG → WebP conversion
- **Sizes:** Hero (2048px), Scale (1920px), Thumb (400px)

---

## Tasks for Forge (After Pixel Completion)

### Integration Steps
1. Update Hugo layout for multi-image galleries (if needed)
2. Optimize WebP conversion (existing images already converted)
3. Add srcset for responsive loading
4. Verify alt text accuracy
5. Rebuild HTML for affected pages

### Verification
1. Visual inspection: no artifacts, correct aspect ratios
2. Mobile test: no horizontal scroll required
3. Speed test: LCP under 2.5s target
4. Alt text audit: accurate descriptions
5. Affiliate links: all disclosure present

---

## Workflow Timeline

```
[Day 1] Pixel generates Batch 1 images → Forge integrates Batch 1 → Verification → Paul review
[Day 2] Pixel generates Batch 2 images → Forge integrates Batch 2 → Verification → Paul review
[Day 3] Continue batching...
```

**Daily Cadence:**
- Morning: Pixel work queued
- Midday: Forge integration
- Afternoon: Verification
- Evening: Sophia reports to Paul

---

## Quality Checklist

### Before Pixel Generation
- [ ] Product research complete
- [ ] Angle/shot composition planned
- [ ] Lighting/style guidelines defined
- [ ] Naming convention mapped

### After Pixel Generation
- [ ] Images visually accurate
- [ ] No misleading representations
- [ ] Consistent style across angles
- [ ] File sizes reasonable

### After Forge Integration
- [ ] All images displayed correctly
- [ ] Responsive loading works
- [ ] Alt text accurate
- [ ] Affiliate disclosures present
- [ ] No layout breaks

### After Verification
- [ ] Mobile test passed
- [ ] Desktop test passed
- [ ] Page speed acceptable
- [ ] Accessibility compliant
- [ ] No horizontal overflow

---

## Next Steps

1. **Approve this plan**
2. **Pixel receives prompt** for Batch 1 (lelo-mona, womanizer-2)
3. **Forge prepares** Hugo layout updates
4. **Sequential execution** (Pixel → Forge)
5. **Verification** before Paul review

---

## Communication

**Sophia will report to Paul:**
- Batch completion status
- Image count generated
- Any issues encountered
- Progress against timeline

**Pixel & Forge:**
- No direct communication
- Sequential handoff via file completion
- Issues escalated to Architect (you)

---

## Risk Mitigation

- **Image generation failures:** Have backups/existing images ready
- **Layout breaks:** Forge tests on multiple devices
- **Speed regressions:** Forge monitors Core Web Vitals
- **Affiliate violations:** Pre-approved alt text templates
