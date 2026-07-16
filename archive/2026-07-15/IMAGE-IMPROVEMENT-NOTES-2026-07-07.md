# Venus Image Improvement Notes - 2026-07-07

## Current Active Image Health

- Active HTML references 32 images.
- All active image references exist and open successfully.
- Known people/face/body variants are no longer referenced.
- Invalid placeholder files with image extensions were removed to prevent accidental reuse.

## Good / Keep

- `images/products/womanizer-clean_00001_.png`
- `images/products/bvee-clean_00001_.png`
- `images/products/lelo-product_00001_.png`

These are the verified product-only assets from the Pixel/Forge cleanup: no people, faces, hands, or body parts.

## Improve Next

Regenerate these as product-only, consistent e-commerce shots with no people, faces, hands, body parts, text, or lifestyle use:

- `product-fun-factory-manta.jpg` / `product-funfactory-manta.png`
- `product-lelo-hugo.jpg`
- `product-lelo-sona-2.jpg`
- `product-womanizer-premium-2.jpg`
- `product-lovehoney-desire.png`
- `product-funfactory-volta.png`

These are acceptable for now, but style and framing are inconsistent with the clean final trio.

## Hero / Category Improvement

- `hero-banner.jpg` has baked-in marketing text. Prefer a text-free background image so page HTML handles copy responsively.
- `category-luxury-toys---4c701df9-7c50-422c-890b-777a960dc57f.jpg` is very abstract and weak as a category card. Replace with a discreet product-only arrangement or premium flat lay.
- `social-header.png` includes brand text in the image. Fine for social usage, but avoid using text-heavy images inside responsive page layouts.

## Pixel Prompt Guardrails

Use strict negative prompts:

`person, people, human, face, hands, body, skin, model, portrait, holding, using, lifestyle scene, nudity, anatomy`

Use positive framing:

`clean product-only ecommerce photography, isolated device, premium studio lighting, no human presence, elegant neutral background, consistent 4:3 or 1:1 crop`
