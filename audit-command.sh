#!/bin/bash

echo "=== HUGO BUILD OUTPUT ==="
cd /home/paul/.openclaw/workspaces/assistant/venus-site
hugo

echo ""
echo "=== CONTENT DIRECTORY LISTING (recursive) ==="
find content/ -type f -o -type d | sort

echo ""
echo "=== STATIC/IMAGES/PRODUCTS LISTING ==="
find static/images/products/ -type f -o -type d 2>/dev/null | sort || echo "static/images/products/ does not exist"

echo ""
echo "=== PRODUCT INVENTORY ==="
# Count products with content
echo "Products with content:"
find content/products/ -name "*.md" -type f 2>/dev/null | while read file; do
    filename=$(basename "$file")
    if [ -f "static/images/products/$filename" ]; then
        image_count=$(find "static/images/products/$filename" -type f -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" | wc -l)
        echo "$filename | Y | $image_count"
    else
        echo "$filename | Y | 0"
    fi
done

echo ""
echo "Products without images:"
find content/products/ -name "*.md" -type f 2>/dev/null | while read file; do
    filename=$(basename "$file")
    if [ ! -f "static/images/products/$filename" ] || [ -z "$(find "static/images/products/$filename" -type f -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" 2>/dev/null)" ]; then
        echo "$filename | N/A (no images)"
    fi
done

echo ""
echo "=== PRODUCT SUBDIRECTORY CHECK ==="
ls -la content/products/ 2>/dev/null || echo "content/products/ does not exist"
ls -la static/images/products/ 2>/dev/null || echo "static/images/products/ does not exist"

echo ""
echo "=== WHAT'S BROKEN/MISSING ==="
echo "Checking for missing images for content pages..."
# For each content page, check if image exists
for imgdir in static/images/products/*.png static/images/products/*.jpg static/images/products/*.jpeg static/images/products/*.webp; do
    if [ -f "$imgdir" ]; then
        basename="${imgdir##*/}"
        echo "Image exists: $basename"
    fi
done
