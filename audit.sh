#!/bin/bash
set -o xtrace

cd /home/paul/.openclaw/workspaces/assistant/venus-site

echo "======= HUGO BUILD ======="
hugo 2>&1 || echo "Hugo build completed with exit code: $?"

echo ""
echo "======= CONTENT DIRECTORY ======="
find content/ -type f -o -type d 2>/dev/null | sort

echo ""
echo "======= STATIC/IMAGES/PRODUCTS ======="
if [ -d "static/images/products" ]; then
    find static/images/products/ -type f -o -type d 2>/dev/null | sort
else
    echo "static/images/products/ does not exist"
fi

echo ""
echo "======= PRODUCT INVENTORY ======="
echo "File | Content | Image"
echo "------|---------|------"

# Check for all product markdown files
find content/ -name "*.md" -type f 2>/dev/null | sort | while read file; do
    filename=$(basename "$file")
    echo "$filename | Y | "
done

echo ""
echo "======= IMAGES LISTING ======="
if [ -d "static/images/products" ]; then
    ls -la static/images/products/ 2>/dev/null || echo "No images or directory empty"
else
    echo "static/images/products/ does not exist"
fi

echo ""
echo "======= ALL PRODUCTS ======="
echo "All product directories/files in content/products:"
ls -laR content/products/ 2>/dev/null || echo "content/products/ does not exist"
