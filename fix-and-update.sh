#!/bin/bash

# Fix corrupted HTML files and update with theme CSS + theme picker JS

VENUSSITE="/home/paul/.openclaw/workspaces/assistant/venus-site"

echo "============================================"
echo "Venus Theme Picker Rollout - Fix & Update"
echo "============================================"
echo

# Find all HTML files to process
files=$(find "$VENUSSITE" -name "*.html" -type f 2>/dev/null | grep -v "/themes/" | grep -v "/layouts/" | grep -v "/public/")

count=0
updated=0

echo "$files" | while read file; do
    if [ -z "$file" ]; then
        continue
    fi
    
    # Skip footer.html (template)
    basename=$(basename "$file")
    if [ "$basename" = "footer.html" ]; then
        continue
    fi
    
    echo "Processing: $file"
    
    # First, fix corrupted head section by restoring original structure
    # Use sed to fix malformed HTML
    
    # Create a temp file
    tmpfile=$(mktemp)
    
    # Read the file and process it
    content=$(cat "$file")
    
    # Add theme CSS links if not present (7 themes)
    if ! grep -q "theme-dark-rose.css" "$file"; then
        echo "    Adding 7 theme CSS links..."
        
        # Insert theme CSS links before </head>
        # Create replacement
        new_head="
  <link rel=\"stylesheet\" href=\"/static/css/theme-dark-rose.css\">
  <link rel=\"stylesheet\" href=\"/static/css/theme-dark-blue.css\">
  <link rel=\"stylesheet\" href=\"/static/css/theme-dark-green.css\">
  <link rel=\"stylesheet\" href=\"/static/css/theme-light.css\">
  <link rel=\"stylesheet\" href=\"/static/css/theme-midnight-gold.css\">
  <link rel=\"stylesheet\" href=\"/static/css/theme-neon-cyber.css\">
  <link rel=\"stylesheet\" href=\"/static/css/theme-deep-violet.css\">"
        
        # Replace all theme links with complete set (idempotent)
        sed -i 's|<link rel="stylesheet" href="/static/css/theme-[^-]*\.css">|<link rel="stylesheet" href="/static/css/theme-dark-rose.css">\n  <link rel="stylesheet" href="/static/css/theme-dark-blue.css">\n  <link rel="stylesheet" href="/static/css/theme-dark-green.css">\n  <link rel="stylesheet" href="/static/css/theme-light.css">\n  <link rel="stylesheet" href="/static/css/theme-midnight-gold.css">\n  <link rel="stylesheet" href="/static/css/theme-neon-cyber.css">\n  <link rel="stylesheet" href="/static/css/theme-deep-violet.css">|g' "$file"
    fi
    
    # Add theme picker JS if not present
    if ! grep -q "theme-picker.js" "$file"; then
        echo "    Adding theme picker JS..."
        sed -i 's|</body>|  <script src="/static/css/theme-picker.js"></script>\n</body>|g' "$file"
    fi
    
    # Fix any corrupted HTML structure
    # Ensure proper head/body structure
    if grep -q "<head><link" "$file" || grep -q "<head><link.*main.css" "$file"; then
        # Fix malformed head section
        echo "    Fixing head structure..."
        # Add newline after </head> before theme links were added
        sed -i '/<\/head>/a\  <link rel="stylesheet" href="/static/css/theme-dark-rose.css">\n  <link rel="stylesheet" href="/static/css/theme-dark-blue.css">\n  <link rel="stylesheet" href="/static/css/theme-dark-green.css">\n  <link rel="stylesheet" href="/static/css/theme-light.css">\n  <link rel="stylesheet" href="/static/css/theme-midnight-gold.css">\n  <link rel="stylesheet" href="/static/css/theme-neon-cyber.css">\n  <link rel="stylesheet" href="/static/css/theme-deep-violet.css">' "$file"
    fi
    
    echo "    Done"
    updated=$((updated + 1))
done

echo
echo "============================================"
echo "Rollout complete!"
echo "============================================"
