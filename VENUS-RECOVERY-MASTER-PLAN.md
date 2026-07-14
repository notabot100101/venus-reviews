# Venus Website Recovery & Rebuild — Master Plan

**Date:** 2026-07-14
**Status:** Content Recovery in Progress
**Objective:** Restore lost product reviews, convert to durable Hugo format, complete the website

---

## The Problem (Root Cause Identified)

**What happened:**
- Venus had **12 product reviews live** on July 13 (per memory)
- Content existed as **flat HTML pages** (`products/*/index.html`), NOT Hugo markdown
- These flat pages were likely overwritten during a Hostinger sync or rebuild
- Current workspace has Hugo structure but **no product content**

**Why it matters:**
- Flat HTML is fragile — gets wiped on rebuild
- Hugo markdown is durable — survives rebuilds, version controlled
- This pattern affects ALL future websites (Desperados, Trading Bots, etc.)

---

## Recovery Strategy

### Phase 1: Content Archaeology (URGENT — Today)
**Goal:** Recover the lost 12 product reviews

**Sources to check:**
1. ✅ Git history — commits `94be530`, `d72ff26`, `13cf494` (July 9 batches)
2. ⚠️ Live site — fetch current pages (may still have some content)
3. ⚠️ Hostinger server — check if backups exist
4. ⚠️ Workspace search — any `.html`, `.bak`, `.old` files?

**Recovery targets:**
- [ ] lelo-hugo
- [ ] lelo-sona-2  
- [ ] lovehoney-desire
- [ ] lelo-enigma
- [ ] dame-eva-ii
- [ ] we-vibe-chorus
- [ ] we-vibe-sync
- [ ] fun-factory-manta
- [ ] fun-factory-volta
- [ ] lelo-mona
- [ ] womanizer-2-original
- [ ] bvee-original-rabbit

**Deliverable:** `RECOVERED-CONTENT/` directory with all review text

---

### Phase 2: Content Conversion (Day 1-2)
**Goal:** Convert recovered HTML → Hugo markdown

**Process:**
1. Parse review content (text, ratings, categories, affiliate links)
2. Create Hugo frontmatter:
   ```yaml
   ---
   title: "Product Name"
   rating: 4.6
   category: "good-for-beginners"
   price: "$XX"
   affiliate_link: "..."
   tags: ["rabbit", "rechargeable", "waterproof"]
   ---
   ```
3. Write markdown body with practical buying guidance
4. Place in `content/products/product-name.md`

**Categories to preserve:**
- "Good for beginners"
- "Premium/Luxury"  
- "Couples"
- "Discrete/Quiet"
- "Value/Budget"

**Deliverable:** 12 Hugo product markdown files

---

### Phase 3: Visual Restoration (Day 2-4)
**Goal:** Regenerate product images in batches

**Batch 1** (Priority — revenue drivers):
- lelo-mona
- womanizer-2
- bvee-rabbit

**Batch 2-4** (remaining 9 products)

**Per product:** 6-8 images
- Front/main view
- 3 alternate angles  
- Scale/context shot
- Packaging
- Lifestyle (if appropriate)
- Thumbnail

**Tool:** Pixel (ComfyUI local) — no people/faces, product-only

**Deliverable:** WebP images in `static/images/products/`

---

### Phase 4: Site Completion (Day 4-5)
**Goal:** Full featured website

**Homepage:**
- Compelling hero banner (no text, visual only)
- Featured products grid (6 products)
- Category filters (beginners, premium, couples, etc.)
- Trust badges
- CTA buttons

**Product pages:**
- Full review content
- Image gallery (6-8 images)
- Affiliate "Check Price" buttons
- Related products

**Infrastructure:**
- SEO meta tags
- Sitemap
- Mobile responsive
- Performance optimized

---

### Phase 5: Documentation & Template (Day 5)
**Goal:** Make this reusable for future sites

**Create:**
1. `VENUS-PLAYBOOK.md` — step-by-step process
2. `WEBSITE-TEMPLATE.md` — generic structure for any affiliate site
3. `AGENT-WORKFLOW.md` — coordination pattern

**Applies to:**
- Desperados 963ml
- Trading Bots review site
- Any future affiliate/commercial site

---

## Team Assignments

| Phase | Agent | Task |
|-------|-------|------|
| 1 | Architect | Coordinate recovery, git archaeology, source verification |
| 1 | Forge | Search workspace, check for backups, document findings |
| 2 | Forge | Convert HTML → Hugo markdown, create frontmatter |
| 3 | Pixel | Generate product images (ComfyUI) |
| 3 | Forge | Integrate images, update templates |
| 4 | Forge | Homepage, featured grid, trust badges |
| 4 | Architect | Review and verification |
| 5 | Architect | Documentation, template creation |
| All | Sophia | Paul communication, checkpoint reviews |

---

## Review Checkpoints

1. **After Phase 1:** Paul reviews recovered content — is anything still missing?
2. **After Phase 2:** Paul reviews 3 sample product markdown files
3. **After Phase 3:** Paul reviews Batch 1 images before continuing
4. **After Phase 4:** Full site review — approve or request changes
5. **After Phase 5:** Template review — can we reuse this for Desperados?

---

## Success Criteria

- [ ] All 12 product reviews recovered and converted to Hugo
- [ ] 6-8 images per product (72-96 total images)
- [ ] Homepage with hero, featured grid, categories
- [ ] Mobile responsive, fast loading
- [ ] Affiliate links integrated
- [ ] Playbook/template documented for reuse

---

## Immediate Next Action

**Execute Phase 1 NOW:**
1. Check git history for commits `94be530`, `d72ff26`, `13cf494`
2. Fetch live site pages to see what's still there
3. Search workspace for any backup files
4. Compile recovered content

**Start recovery immediately.**
