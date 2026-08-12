#!/bin/bash
exec bash -c '
cd /home/paul/.openclaw/workspaces/assistant/venus-site
echo "=== ALL GIT COMMITS ==="
git log --oneline --all 2>&1 | head -40
echo ""
echo "=== COMMITS WITH FILE CHANGES ==="
git log --oneline --all --name-status 2>&1 | head -100
echo ""
echo "=== FINDING ALL FILES ==="
find . -type f \( -name "*.md" -o -name "*.html" -o -name "*.webp" \) 2>&1 | head -80
echo ""
echo "=== BRANCHES ==="
git branch -a 2>&1
'
