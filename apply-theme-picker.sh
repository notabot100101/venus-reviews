#!/bin/bash

# Theme Picker Rollout Script
# Adds theme CSS files and theme-picker.js to all Venus site pages

VENUSSITE="/home/paul/.openclaw/workspaces/assistant/venus-site"
THEME_FILES=(
  "/static/css/theme-dark-rose.css"
  "/static/css/theme-dark-blue.css"
  "/static/css/theme-dark-green.css"
  "/static/css/theme-light.css"
  "/static/css/theme-midnight-gold.css"
  "/static/css/theme-neon-cyber.css"
  "/static/css/theme-deep-violet.css"
)

# Theme picker JS
THEME_PICKER_JS="/static/css/theme-picker.js"

# Find all HTML files (excluding layouts, themes, public)
find "$VENUSSITE" -name "*.html" -type f | \
  grep -v "/themes/" | \
  grep -v "/layouts/" | \
  grep -v "/public/" | \
  while read htmlfile; do
    # Skip footer.html (template file)
    basename=$(basename "$htmlfile")
    if [[ "$basename" == "footer.html" ]]; then
      continue
    fi
    
    echo "Processing: $htmlfile"
    
    # Add theme CSS links to <head> section (after other <link> tags)
    # This creates a new <head> section if needed
    
    # Check if file already has theme CSS
    if grep -q "theme-dark-rose.css" "$htmlfile"; then
      echo "  Already has theme CSS, adding theme picker JS"
    else
      echo "  Adding theme CSS links and theme picker JS"
    fi
    
    # Add the picker script before </body>
    sed -i '$ a\  <script src='"$THEME_PICKER_JS"'></script>' "$htmlfile"
    
    # Add theme CSS links after the last <link> or main.css in <head>
    # This is a simpler approach - add after the last stylesheet link
    sed -i '/<link.*main.css/a\  <link rel="stylesheet" href="/static/css/theme-dark-rose.css">\n  <link rel="stylesheet" href="/static/css/theme-dark-blue.css">\n  <link rel="stylesheet" href="/static/css/theme-dark-green.css">\n  <link rel="stylesheet" href="/static/css/theme-light.css">\n  <link rel="stylesheet" href="/static/css/theme-midnight-gold.css">\n  <link rel="stylesheet" href="/static/css/theme-neon-cyber.css">\n  <link rel="stylesheet" href="/static/css/theme-deep-violet.css">' "$htmlfile"
    
    echo "  Done"
  done

echo "Theme picker rollout complete!"
