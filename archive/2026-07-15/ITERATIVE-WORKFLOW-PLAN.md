# Venus Image Generation Workflow — Iterative Approach

## Model Configuration
- **Pixel:** ollama/qwen3:30b (upgraded from qwen3.5:9b)
- **Image Generation:** ComfyUI LOCAL only
- **Method:** One image at a time, verify, iterate until great

## Image 1: bvee-original-rabbit/front.webp

### Generation Parameters
- **Product:** BVibe Original Rabbit Vibrator
- **File:** front.webp
- **Path:** `/home/paul/.openclaw/workspaces/image-creator/venus-images/bvee-original-rabbit/front.webp`
- **Dimensions:** 800x800 pixels
- **Format:** WebP
- **Style:** Professional product photography

### Prompt Template
"Professional product photography of luxury rabbit vibrator, sleek silicone design with dual stimulation curves, clean gradient background deep purple #6B2C91 to black, soft studio lighting, commercial product shot, no people, no hands, isolated product, high-end commercial photography, 800x800 square format, luxury aesthetic"

### Verification Checklist
- [ ] File exists at specified path
- [ ] File size > 50KB (indicates valid image)
- [ ] Dimensions confirmed 800x800
- [ ] No people/faces/hands visible
- [ ] Clean professional appearance
- [ ] Gradient background present

### Rating Criteria
- **GREAT:** File exists, proper dimensions, professional quality, ready for production
- **GOOD:** Minor issues (slight blur, color off) — acceptable if time-constrained
- **NEEDS IMPROVEMENT:** Major issues (wrong product, wrong dimensions, artifacts) — regenerate with feedback

### Improvement Feedback Template
If rating is "needs improvement":
"Image issue: [specific problem]. Regenerate with: [specific fix instruction]"

---

## Image 2: dame-eva-ii/front.webp
(same structure, different product)

### Generation Parameters
- **Product:** Dame Eva II Hands-Free Vibrator
- **File:** front.webp
- **Path:** `/home/paul/.openclaw/workspaces/image-creator/venus-images/dame-eva-ii/front.webp`

### Prompt Template
"Professional product photography of compact hands-free couples vibrator, minimalist white design, clean gradient background deep purple #6B2C91 to black, soft studio lighting, commercial product shot, no people, no hands, isolated product, high-end commercial photography, 800x800 square format, luxury aesthetic"
