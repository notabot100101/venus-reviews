#!/usr/bin/env python3
"""Optimize Venus product images to WebP format"""

import os
from PIL import Image

PRODUCTS_DIR = "images/products"
OUTPUT_QUALITY = 80  # 80% quality for good balance

def optimize_image(input_path, output_path):
    """Convert PNG to optimized WebP"""
    try:
        img = Image.open(input_path)
        # Convert to RGB if needed (WebP doesn't support alpha for most use cases)
        if img.mode in ('RGBA', 'LA', 'La'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            img = background
        
        # Save as WebP
        img.save(
            output_path,
            'WebP',
            quality=OUTPUT_QUALITY,
            optimize=True,
            strip=True
        )
        print(f"✓ {os.path.basename(input_path)} → {os.path.basename(output_path)}")
        
        # Get sizes
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        reduction = ((input_size - output_size) / input_size) * 100
        
        print(f"  Size: {input_size:,}B → {output_size:,}B ({reduction:.1f}% reduction)")
        
        return True
    except Exception as e:
        print(f"✗ Failed {input_path}: {e}")
        return False

def main():
    """Process all PNG files in products directory"""
    if not os.path.exists(PRODUCTS_DIR):
        print(f"Directory not found: {PRODUCTS_DIR}")
        return
    
    optimized = 0
    skipped = 0
    
    # Process each PNG file
    for filename in os.listdir(PRODUCTS_DIR):
        if filename.endswith('.png'):
            input_path = os.path.join(PRODUCTS_DIR, filename)
            output_path = os.path.join(PRODUCTS_DIR, f"{filename}.webp")
            
            # Skip if WebP already exists
            if os.path.exists(output_path):
                print(f"⊘ Skipping {filename} (WebP exists)")
                skipped += 1
                continue
            
            # Optimize
            if optimize_image(input_path, output_path):
                optimized += 1
                
                # Optional: delete original PNG (commented out for safety)
                # os.remove(input_path)
    
    print(f"\n{'='*50}")
    print(f"Summary: {optimized} images optimized, {skipped} skipped")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
