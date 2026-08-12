#!/bin/bash
# Venus Content Recovery Script
exec bash -c '
echo "=== VENUS PRODUCT CONTENT RECOVERY - INVESTIGATION ==="
echo "Date: $(date +\"%Y-%m-%d %H:%M:%S %Z\")"
echo ""

cd /home/paul/.openclaw/workspaces/assistant/venus-site || exit 1

echo ""
echo "=== 1. Git Log Analysis ==="
echo "All commits:"
git log --oneline --all 2>&1 || echo "ERROR: Git not initialized or error"

echo ""
echo "Commits with product content (name-only):"
git log --oneline --all --name-only 2>&1 || echo "ERROR: Git log failed"

echo ""
echo "Differences between hostinger-deploy and main branches:"
git diff hostinger-deploy main --name-only 2>&1 || echo "Branch comparison error"

echo ""
echo "=== 2. File Search ==="
echo "Markdown files:"
find . -name "*.md" -type f 2>&1 | head -50

echo ""
echo "HTML files:"
find . -name "*.html" -type f 2>&1 | head -50

echo ""
echo "Product-related files:"
find . -iname "*product*" -type f 2>&1

echo ""
echo "Review-related files:"
find . -iname "*review*" -type f 2>&1

echo ""
echo "JSON data files:"
find . -name "*.json" -type f 2>&1

echo ""
echo "=== 3. Git Branches ==="
git branch -a 2>&1

echo ""
echo "=== 4. Git Remotes ==="
git remote -v 2>&1

echo ""
echo "=== 5. Git Log with full file names ==="
git log --all --pretty=format:"%H %s" --name-only 2>&1 | head -100

echo ""
echo "=== 6. Backup/Recovery Files ==="
find . -name "*.backup" -o -name "*.old" -o -name "*.recovery" -o -name "*.bak" -o -name "*.tmp" 2>&1 || echo "No backup files found"

echo ""
echo "=== 7. Content Directories ==="
find . -type d -iname "*content*" -o -iname "*product*" -o -iname "*review*" -o -iname "*data*" 2>&1

echo ""
echo "=== 8. tmp directory ==="
find /home/paul/.openclaw/tmp/ -name "*venus*" 2>&1 || echo "No venus files in tmp"
'
