#!/bin/bash

cd /home/paul/.openclaw/workspaces/assistant/venus-site

echo "=========================================="
echo "HUGO BUILD OUTPUT"
echo "=========================================="
hugo 2>&1 || true

echo ""
echo "=========================================="
echo "CONTENT DIRECTORY (recursive)"
echo "=========================================="
find content/ -type f -o -type d 2>/dev/null | sort || echo "content/ directory does not exist"

echo ""
echo "=========================================="
echo "STATIC/IMAGES/PRODUCTS DIRECTORY"
echo "=========================================="
if [ -d "static/images/products" ]; then
    find static/images/products/ -type f -o -type d 2>/dev/null | sort
else
    echo "static/images/products/ does not exist"
fi

echo ""
echo "=========================================="
echo "PRODUCT INVENTORY TABLE"
echo "=========================================="
echo "Product Name | Has Content | Image Count"
echo "-------------|-------------|------------"

# Get all markdown files in content/products
if [ -d "content/products" ]; then
    for md in content/products/*.md; do
        if [ -f "$md" ]; then
            filename=$(basename "$md")
            imagecount=0
            for ext in png jpg jpeg webp; do
                if [ -f "static/images/products/${filename}.${ext}" ]; then
                    imagecount=$((imagecount + 1))
                fi
            done
            echo "$filename | Y | $imagecount"
        fi
    done
    
    # Check for directories with content but no .md files
    for dir in content/products/*/; do
        dir=${dir%/}
        page=""
        for md in "$dir"/*.md "$dir"/*.json; do
            if [ -f "$md" ]; then
                page=$(basename "$md")
                break
            fi
        done
        if [ -z "$page" ]; then
            echo "$dir | N | 0"
        fi
    done
else
    echo "content/products/ does not exist"
fi

echo ""
echo "=========================================="
echo "WHAT'S BROKEN/MISSING"
echo "=========================================="
echo "1. Hugo build errors (if any):"
echo "   - Check above output for errors"

echo ""
echo "2. Missing images for product pages:"
# List all product pages
if [ -d "content/products" ]; then
    for md in content/products/*.md; do
        if [ -f "$md" ]; then
            filename=$(basename "$md")
            hasimage="YES"
            for ext in png jpg jpeg webp; do
                if [ ! -f "static/images/products/${filename}.${ext}" ]; then
                    hasimage="NO"
                    break
                fi
            done
            if [ "$hasimage" = "NO" ]; then
                echo "   - $filename (no image found)"
            fi
        fi
    done
fi

echo ""
echo "3. Directory structure verification:"
if [ -d "content/products" ]; then
    echo "   - content/products/ exists: $(ls content/products/ | wc -l) subdirectories"
    ls content/products/ 2>/dev/null || echo "   - No subdirectories"
else
    echo "   - content/products/ does not exist"
fi

if [ -d "static/images/products" ]; then
    echo "   - static/images/products/ exists: $(ls static/images/products/ 2>/dev/null | wc -l) images"
    ls static/images/products/ 2>/dev/null || echo "   - No images"
else
    echo "   - static/images/products/ does not exist"
fi
