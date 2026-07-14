#!/bin/bash
exec bash -c '
echo "=== VENUS PRODUCT CONTENT RECOVERY ==="
echo "Date: $(date +\"%Y-%m-%d %H:%M:%S %Z\")"
cd /home/paul/.openclaw/workspaces/assistant/venus-site

echo ""
echo "=== GIT LOG ==="
git log --oneline --all 2>&1 | head -30

echo ""
echo "=== GIT LOG NAME-ONLY ==="
git log --oneline --all --name-only 2>&1 | head -80

echo ""
echo "=== DIFF BETWEEN BRANCHES ==="
git diff hostinger-deploy main --name-only 2>&1

echo ""
echo "=== FIND MD FILES ==="
find . -name "*.md" -type f 2>&1 | head -30

echo ""
echo "=== FIND HTML FILES ==="
find . -name "*.html" -type f 2>&1

echo ""
echo "=== BRANCHES ==="
git branch -a 2>&1

echo ""
echo "=== REMOTES ==="
git remote -v 2>&1
'
