# Venus Website Phase 3 - Project Template

**Version:** 1.0  
**Created:** 2026-07-03  
**Author:** Architect  
**Status:** Production Ready  

---

## Overview

This template documents the complete Venus Website Phase 3 implementation workflow for affiliate/commercial review sites.

### Reusable For:
- **Desperados 963ml** - Vodka review site
- **Trading Bots** - FinTech review site
- **Any affiliate product site**

---

## Architecture Overview

### Site Structure
```
venus-site/
├── static/
│   ├── css/
│   │   ├── main.css (core styles)
│   │   └── theme-dark-rose.css (branding)
│   └── js/
│       ├── main.js
│       └── deferred.js
├── images/
│   ├── products/ (product images)
│   ├── hero-banner.jpg
│   └── logo.png
├── trust-badges/ (SVG badges)
├── content/
│   ├── about.md
│   ├── privacy.md
│   └── guides/
├── pages/
│   ├── index.html (home)
│   ├── products/
│   ├── about/
│   └── privacy/
└── hugo.toml (configuration)
```

### Deployment
- **Flat deployment** (Hugo static site)
- **Hostinger** (recommended hosting)
- **Git push** (CI/CD integration)

---

## Phase 1: Foundation (Structure)

### Steps:
1. **Initialize Hugo site**
```bash
hugo new site new-site
cd new-site
```

2. **Install dependencies**
```bash
npm install hugo-cli
hugo mod get
```

3. **Flat deployment**
- No Jekyll/liquid templating
- Pure HTML/CSS/JS
- Fast load times

4. **Create core pages**
- Home page
- Products page
- About page
- Privacy policy

### Files Created:
- `pages/` directory
- Basic HTML templates
- CSS framework (Tailwind/Bootstrap)

### Verification:
- ✅ Site loads at 200
- ✅ All pages render
- ✅ No broken links

---

## Phase 2: Content (Hero, Products, Compliance)

### Steps:
1. **Hero Banner**
- High-quality product imagery
- Clear value proposition
- Call-to-action buttons

2. **Products Grid**
- Product cards
- Images (600x600px PNG/WebP)
- Review ratings
- Buy links

3. **Compliance**
- GDPR/CCPA privacy policy
- Affiliate disclosure
- Cookie consent
- Terms of service

### Product Image Workflow:
```
1. Generate via ComfyUI LOCAL
   - NO people/faces allowed
   - 600x600px PNG
   - White/gradient backgrounds

2. Verify quality
   - Check for people/faces
   - Professional product style

3. Optimize
   - Convert to WebP
   - Compress to <500KB
   - Lazy loading enabled

4. Upload
   - Place in images/products/
   - Test on live site
```

### Files Created:
- Product images
- Hero banner
- Privacy policy
- Affiliate disclosure

### Verification:
- ✅ Images load properly
- ✅ Text readable
- ✅ Mobile responsive

---

## Phase 3: Polish (Mobile, Perf, Trust)

### Task 1: Mobile Audit (30 min)
**Owner:** Architect → mobile-auditor

**Steps:**
1. Test on mobile viewport
2. Check touch targets (≥44px)
3. Verify navigation
4. Document issues

**Deliverable:** `mobile-audit-report.md`

**Pass Criteria:**
- No horizontal scrolling
- All buttons touch-friendly
- Navigation accessible

---

### Task 2: Performance Optimization (45 min)
**Owner:** Architect → perf-optimizer

**Steps:**
1. Convert images to WebP
2. Add lazy loading
3. Minify CSS/JS
4. Inline critical CSS

**Deliverable:** `performance-report.md`

**Pass Criteria:**
- Lighthouse score ≥80
- LCP <2.5s
- FID <100ms
- CLS <0.1

---

### Task 3: SEO/Meta (30 min)
**Owner:** Architect → seo-specialist

**Steps:**
1. Add meta descriptions
2. Add Open Graph tags
3. Verify semantic HTML
4. Check title tags
5. Add schema markup

**Deliverable:** `seo-audit-report.md`

**Pass Criteria:**
- Unique meta descriptions
- Open Graph tags present
- Semantic HTML valid
- No duplicate titles

---

### Task 4: Trust Badges (30 min)
**Owner:** Pixel (ComfyUI local) → generate, Forge → integrate

**Steps:**
1. Generate badges (ComfyUI)
   - Discreet shipping
   - Secure checkout
   - 18+ verified
   - Privacy protected
2. Integrate into footer
3. Test mobile rendering

**Deliverable:** SVG badges in `trust-badges/`

**Pass Criteria:**
- All 4 badges present
- Visible on mobile
- No layout breaks

---

### Task 5: Template Documentation (60 min)
**Owner:** Architect

**Steps:**
1. Document workflow (this document)
2. Create checklists
3. Define agent roles
4. Document approval gates
5. Example for Desperados

**Deliverable:** `PROJECT-TEMPLATE.md` (this file)

---

## Agent Roles & Responsibilities

### Architect (Coordinator)
- **Purpose:** Planning, coordination, review
- **Tasks:**
  - Read plans (venus-phase-3-complete.md)
  - Spawn workers sequentially
  - Review deliverables
  - Present to Sophia
- **Model:** Cloud (GPT-5.5)

### Forge (Worker - Local)
- **Purpose:** Content implementation
- **Tasks:**
  - Generate images (ComfyUI)
  - Integrate badges
  - Optimize performance
  - Test mobile
- **Model:** Local (qwen3.5:9b)

### Sophia (Verification)
- **Purpose:** Quality assurance
- **Tasks:**
  - Review all deliverables
  - Verify compliance
  - Present to Paul
- **Model:** Cloud (GPT-5.5)

### Pixel (Image Generation)
- **Purpose:** Visual content
- **Tasks:**
  - Generate product images (ComfyUI)
  - Create trust badges
  - Ensure no people/faces
- **Model:** ComfyUI LOCAL

### Hermes (Email - AgentMail)
- **Purpose:** Email handling
- **Tasks:**
  - Process inbound emails
  - Generate replies
- **Model:** Local/Cloud (as configured)

---

## Workflow Example: New Product Site (Desperados)

### Pre-flight Checklist

**Before starting:**
- [ ] Read this template
- [ ] Understand agent roles
- [ ] Verify ComfyUI LOCAL running
- [ ] Check cloud API rate limits
- [ ] Prepare workspace directory

**Execute:**
1. Spawn Forge for image generation
2. Spawn SEO agent for meta
3. Spawn perf agent for optimization
4. Wait for completion events

**Review:**
1. Read Sophia's verification
2. Present to Paul
3. Get approval

**Deploy:**
1. Push to Hostinger
2. Verify live site
3. Monitor analytics

---

## Compliance Requirements

### Always Required:
- [x] GDPR/CCPA compliant
- [x] 18+ age verification (if needed)
- [x] Affiliate disclosure visible
- [x] No people/faces in images
- [x] ComfyUI LOCAL for images

### Site-Specific:
- **Adult sites:** 18+ verification mandatory
- **Health claims:** Disclaimers required
- **Financial:** Regulatory compliance
- **International:** Local laws

---

## Approval Gates

### Gate 1: Plan Review
**Who:** Sophia
**Action:** Verify plan completeness
**Output:** Approval or feedback

### Gate 2: Deliverable Review
**Who:** Sophia
**Action:** Check each deliverable
**Output:** Pass or request changes

### Gate 3: Paul Approval
**Who:** Paul (user)
**Action:** Final approval
**Output:** Go to production or reject

---

## Common Issues & Solutions

### Issue: Cloud API Rate-Limited
**Solution:** Use ComfyUI LOCAL only
**Reference:** Policy forbids cloud APIs when rate-limited

### Issue: Images Contain People
**Solution:** Regenerate with stricter prompts
**Prompts:** Emphasize "device only", "isolated", "no human elements"

### Issue: Mobile Layout Breaks
**Solution:** Test on all device sizes
**Viewport:** 375px-414px minimum

### Issue: Images Too Large
**Solution:** Compress to <500KB
**Target:** 300-500KB per image

---

## Quick Reference

### Command Cheat Sheet

```bash
# Spawn Forge worker
sessions_spawn({ agentId: "worker", task: "Generate Womanizer image", taskName: "womanizer-gen" })

# Wait for completion
sessions_yield()

# Read results
sessions_history({ sessionKey: "agent:worker", includeTools: true })

# Deploy to Hostinger - use the deploy script, nothing else
cd /home/paul/.openclaw/workspaces/assistant/venus-site
./deploy.sh "what changed"
```

**Why `deploy.sh` (corrected 2026-07-16):** Hostinger auto-deploys the ROOT of the
`hostinger-deploy` branch via its Git integration (hPanel). There is no ssh/git-pull
step (the `ssh root@venus-hostinger` command previously documented here was never the
real mechanism), and pushing `main` deploys nothing. Crucially, Hugo builds into
`public/` but Hostinger serves the branch ROOT - the build output must be synced to
the root before pushing, which is exactly what `deploy.sh` does. Skipping that sync
caused task 616's "pushed successfully but live site unchanged" failure. After a
deploy, wait 5-10 minutes for propagation, then verify with a real fetch:
`curl -s https://reviews.ultramarine963.com/products/<any-product>/ | grep comparison`

---

## Contact & Support

**Issues:** Report to #sophia Discord channel  
**Urgent:** Contact Paul directly  
**Documentation:** See README files in workspace

---

## Appendix

### A. Image Generation Prompts

**Womanizer 2:**
```
Product photography of Womanizer 2 pleasure device on pure white background. Device ONLY. NO HANDS NO PEOPLE NO FACES no human elements, product isolated on background, studio lighting, commercial product shot, white/gold colors
```

**Negative Prompt:**
```
people, faces, hands, body parts, humans, hands arms legs feet skin, blurry, low quality
```

**Bvee Rabbit:**
```
Product photography of purple silicone rabbit vibe on soft gradient background. Device ONLY. NO HANDS NO PEOPLE NO FACES no human elements, isolated product, studio lighting, commercial photography, purple colors, luxury aesthetic
```

**Lelo Mona:**
```
Product photography of sleek black silicone device, minimalist curved design, white background, premium adult wellness product, high-end commercial photography
```

### B. SEO Meta Tags Template

```html
<meta name="description" content="[Unique description, 150-160 chars]" />
<meta property="og:title" content="[Page Title]" />
<meta property="og:description" content="[Short description]" />
<meta property="og:image" content="[Hero image URL]" />
<meta property="og:url" content="[Current URL]" />
<meta property="og:type" content="website" />
<meta property="og:locale" content="en_US" />
```

### C. Trust Badge Colors

| Badge | Hex | Usage |
|-------|-----|-----|
| Discreet Shipping | `#2c3e50` | Gray, professional |
| Secure Checkout | `#27ae60` | Green, safe |
| 18+ Verified | `#8e44ad` | Purple, premium |
| Privacy Protected | `#3498db` | Blue, secure |

---

**Template Version:** 1.0  
**Last Updated:** 2026-07-03  
**Status:** Production Ready

---

*End of Project Template for Venus Website Phase 3*
