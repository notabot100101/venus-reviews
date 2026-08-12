# Venus Website Image Generation Workflow

**Project:** Venus Reviews Website Enhancement  
**Date:** 2026-07-05  
**Agents:** Forge (Worker), Pixel (Image Creator)  
**Status:** In Progress

---

## Current Status: Briefs Prepared

### ✅ Completed

1. **Site Analysis** - Identified visual opportunities on:
   - Homepage (hero banner needs refresh)
   - About page (needs visual interest)
   - Contact page (needs polish)
   - Privacy page (informational)
   - Shipping page (trust signal opportunity)
   - Products page (category headers)

2. **Asset Inventory** - Documented existing:
   - Hero banner: `/images/hero-banner.jpg` (626KB)
   - Product images: 8 JPEG files in `/images/products/`
   - Trust badges: 4 SVG files in `/trust-badges/`

3. **Image Briefs Created** - Comprehensive briefs for 8 image categories:
   - Hero banner (homepage)
   - About section background
   - Privacy section background
   - Shipping section background
   - Contact section background
   - Category header set (4 images)
   - Trust badge icons (PNG alternatives)
   - Feature icon set

### 🔄 In Progress

4. **Briefs Documented**:
   - File: `/venus-site/IMAGE-BRIEFS.md` (8.8KB)
   - Format: Clear purpose, theme, colors, style, dimensions
   - Color palette: Deep purple #6B2C91, Rose gold #B76E79
   - Style: Elegant, sophisticated, premium, discreet

5. **Message to Pixel Prepared**:
   - File: `/venus-site/PAXELS_MESSAGE.md` (2.5KB)
   - Ready to send via AgentMail

### ⏳ Pending

6. **Images to Generate** (Priority Order):
   - Phase 1 (High): Hero banner, About background, Trust icons
   - Phase 2 (Medium): Shipping, Contact backgrounds, Category headers
   - Phase 3 (Lower): Privacy section

7. **Integration Work**:
   - Place images in correct directories
   - Update HTML templates
   - Test locally
   - Commit to git
   - Push to hostinger-deploy branch

---

## Next Steps

### Immediate

1. **Send briefs to Pixel** via AgentMail
   - Use message: `paulpawprints@agentmail.to`
   - Subject: "Venus Website Image Generation Briefs"
   - Attach: IMAGE-BRIEFS.md

2. **Wait for Pixel confirmation** and estimated completion time

### After Pixel Generates

3. **Download & Organize**:
   - Place hero images in `/images/`
   - Place section backgrounds in `/images/sections/`
   - Place icons in `/images/icons/`

4. **Update Templates**:
   - Edit Hugo templates for new images
   - Update page references

5. **Test**:
   - Local Hugo build
   - Check image loading
   - Verify responsive behavior

6. **Deploy**:
   - `git add .`
   - `git commit -m "Add enhanced images for Venus website"`
   - `git push origin hostinger-deploy`

---

## Image Priority Matrix

| Image | Dimensions | File Type | Priority | Purpose |
|-------|-----------|-----------|----------|---------|
| Hero Banner | 1920x600 | JPEG | HIGH | Homepage conversion |
| About BG | 1920x800 | JPEG | HIGH | Brand trust |
| Trust Icons | 100x100 each | PNG | HIGH | Replace/complement SVGs |
| Shipping BG | 1920x800 | JPEG | MEDIUM | Trust signal |
| Contact BG | 1920x800 | JPEG | MEDIUM | Polish |
| Category Headers | 1200x300 | JPEG | MEDIUM | Product pages |
| Privacy BG | 1920x800 | JPEG | LOW | Legal page |

---

## Notes for Pixel

**Color Palette:**
- Deep Purple: #6B2C91 (primary)
- Rose Gold: #B76E79 (accent)

**Style:**
- Elegant and sophisticated
- Discreet and subtle
- Premium quality
- No generic stock imagery
- No faces or explicit content

**File Specs:**
- JPEG: 90-95 quality
- PNG: Transparent backgrounds for icons
- sRGB color space
- No EXIF data

**Variations:**
- 3 options per brief (A/B testing)
- Both orientations where applicable

---

## Checklist

- [x] Site analyzed
- [x] Assets inventoried
- [x] Briefs documented
- [x] Message prepared
- [ ] Send to Pixel
- [ ] Wait for generation
- [ ] Download images
- [ ] Organize by category
- [ ] Update HTML templates
- [ ] Test locally
- [ ] Commit to git
- [ ] Push to deploy branch

---

**Last Updated:** 2026-07-05  
**Agent:** Forge (Worker)  
**Project:** Venus Website Enhancement
