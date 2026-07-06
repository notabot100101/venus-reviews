#!/bin/bash

# Batch update all HTML files with theme CSS + theme picker JS
# This script handles all files systematically

VENUSSITE="/home/paul/.openclaw/workspaces/assistant/venus-site"

echo "========================================="
echo "Batch Update - All HTML Files"
echo "========================================="

# Array of files to fix (skip footer.html as it's a template)
files=(
    "about/index.html"
    "affiliate-disclosure/index.html"
    "best-for/beginners/index.html"
    "best-for/couples/index.html"
    "best-for/index.html"
    "best-for/luxury/index.html"
    "best-for/technology/index.html"
    "best-for/travel/index.html"
    "best-for/value/index.html"
    "contact/index.html"
    "guides/index.html"
    "guides/materials/index.html"
    "index.html"
    "privacy/index.html"
    "products/all/index.html"
    "products/bvee-rabbit/index.html"
    "products/compare/index.html"
    "products/dame-eva-ii/index.html"
    "products/fun-factory-manta/index.html"
    "products/fun-factory-volta/index.html"
    "products/h2o-holo-vibe/index.html"
    "products/index.html"
    "products/lelo-enigma/index.html"
    "products/lelo-gigi-2/index.html"
    "products/lelo-hugo/index.html"
    "products/lelo-mona/index.html"
    "products/lelo-sona-2/index.html"
    "products/lovehoney-desire/index.html"
    "products/satisfyer-pro-2/index.html"
    "products/we-vibe-chorus/index.html"
    "products/we-vibe-sync/index.html"
    "products/womanizer-2/index.html"
    "products/womanizer-premium-2/index.html"
    "security/index.html"
    "shipping/index.html"
)

THEME_LINKS='  <link rel="stylesheet" href="/static/css/theme-dark-rose.css">
  <link rel="stylesheet" href="/static/css/theme-dark-blue.css">
  <link rel="stylesheet" href="/static/css/theme-dark-green.css">
  <link rel="stylesheet" href="/static/css/theme-light.css">
  <link rel="stylesheet" href="/static/css/theme-midnight-gold.css">
  <link rel="stylesheet" href="/static/css/theme-neon-cyber.css">
  <link rel="stylesheet" href="/static/css/theme-deep-violet.css">'

PICKER_JS='  <script src="/static/css/theme-picker.js"></script>'

updated=0

for file in "${files[@]}"; do
    filepath="$VENUSSITE/$file"
    
    if [ ! -f "$filepath" ]; then
        echo "SKIP (not found): $file"
        continue
    fi
    
    echo ""
    echo "Processing: $file"
    
    # Read current content
    content=$(cat "$filepath")
    
    # Check if already has all themes
    has_themes=false
    for theme in "theme-dark-rose.css" "theme-dark-blue.css" "theme-dark-green.css" "theme-light.css" "theme-midnight-gold.css" "theme-neon-cyber.css" "theme-deep-violet.css"; do
        if echo "$content" | grep -q "$theme"; then
            has_themes=true
            break
        fi
    done
    
    # Check for theme picker JS
    has_picker=$(echo "$content" | grep -c "theme-picker.js")
    
    if [ "$has_themes" = "false" ] || [ "$has_picker" -eq 0 ]; then
        # Need to fix this file
        
        # Find positions
        head_pos=$(echo "$content" | grep -bo "</head>" | head -1 | cut -d: -f1)
        body_pos=$(echo "$content" | grep -bo "</body>" | head -1 | cut -d: -f1)
        
        # Remove malformed theme links that appear after </head> but before </body>
        # Find the malformed section
        malformed_start=$((head_pos + 6))  # after </head>
        malformed_end=$((body_pos - 2))   # before </body>
        
        # Get the malformed section
        malformed_section=$(echo "$content" | sed -n "${malformed_start},${malformed_end}p")
        
        # Check how many theme links are in malformed section
        malformed_count=$(echo "$malformed_section" | grep -c 'theme-.*\.css')
        
        if [ "$malformed_count" -lt 7 ]; then
            # Need to add missing themes
            echo "    Adding missing theme CSS links..."
            
            # Count existing themes in malformed section
            for theme in "theme-dark-rose.css" "theme-dark-blue.css" "theme-dark-green.css" "theme-light.css" "theme-midnight-gold.css" "theme-neon-cyber.css" "theme-deep-violet.css"; do
                if ! echo "$malformed_section" | grep -q "$theme"; then
                    # Add missing theme link
                    echo "    Adding: $theme"
                fi
            done
        fi
        
        # Now reconstruct the file properly
        # Extract parts before malformed section, the malformed section, and after
        before_malformed=$(echo "$content" | head -n $((malformed_start - 1)))
        after_malformed=$(echo "$content" | tail -n +$((malformed_end + 1)))
        
        # Build proper section between head and body
        proper_section="$THEME_LINKS
$PICKER_JS"
        
        # Reconstruct
        new_content="$before_malformed
$proper_section
$after_malformed"
        
        # Write back
        echo "$new_content" > "$filepath"
        echo "    Fixed: $file"
        updated=$((updated + 1))
    else
        echo "    Already correct"
    fi
done

echo ""
echo "========================================="
echo "Complete! Updated $updated files"
echo "========================================="
