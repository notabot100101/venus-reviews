#!/bin/bash

cd /home/paul/.openclaw/workspaces/assistant/venus-site

echo "======================================"
echo "Theme Picker Rollout - Final Batch Fix"
echo "======================================"
echo

# Get count of HTML files
total=$(find . -name "*.html" -type f ! -path "*/themes/*" ! -path "*/layouts/*" ! -path "*/public/*" ! -name "footer.html" | wc -l)
echo "Total HTML files: $total"
echo

updated=0

for file in $(find . -name "*.html" -type f ! -path "*/themes/*" ! -path "*/layouts/*" ! -path "*/public/*" ! -name "footer.html"); do
    echo "Processing: $file"
    
    # Remove any malformed theme links that appear after </head>
    # This cleans up corrupted structure
    sed -i '/<\/head>/,/</body>/{
        /<link.*theme/d
    }' "$file"
    
    # Add all 7 theme CSS links before </head>
    sed -i '/<\/head>/i\  <link rel="stylesheet" href="/static/css/theme-dark-rose.css">\n  <link rel="stylesheet" href="/static/css/theme-dark-blue.css">\n  <link rel="stylesheet" href="/static/css/theme-dark-green.css">\n  <link rel="stylesheet" href="/static/css/theme-light.css">\n  <link rel="stylesheet" href="/static/css/theme-midnight-gold.css">\n  <link rel="stylesheet" href="/static/css/theme-neon-cyber.css">\n  <link rel="stylesheet" href="/static/css/theme-deep-violet.css">' "$file"
    
    # Add theme-picker.js before </body>
    sed -i '/<\/body>/i\  <script src="/static/css/theme-picker.js"></script>' "$file"
    
    # Fix malformed head section (remove extra links)
    sed -i '/<\/head><link/d' "$file"
    sed -i '/<\/head>\n  <link/d' "$file"
    
    echo "  Done"
    updated=$((updated + 1))
done

echo
echo "======================================"
echo "Complete! Updated $updated files"
echo "======================================"
