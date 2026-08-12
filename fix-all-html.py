#!/usr/bin/env python3
"""
Fix and update all HTML files with theme picker
"""

import os
import re

VENUSSITE = "/home/paul/.openclaw/workspaces/assistant/venus-site"

THEME_CSS_FILES = [
    "theme-dark-rose.css",
    "theme-dark-blue.css",
    "theme-dark-green.css",
    "theme-light.css",
    "theme-midnight-gold.css",
    "theme-neon-cyber.css",
    "theme-deep-violet.css"
]

THEME_PICKER_JS = "/static/css/theme-picker.js"

def fix_html_file(filepath):
    """Fix a single HTML file and add theme CSS + picker JS."""
    
    print(f"\nProcessing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading: {e}")
        return False
    
    # Check if file is corrupted (no </head> or malformed)
    if content.count('<head>') > 1 or content.count('</head>') != content.count('<head>'):
        print(f"  WARNING: Malformed head section")
    
    # Find </head> position (handle malformed HTML)
    # Look for </head> case-insensitively
    head_end = -1
    for pattern in ['</head>', '<\/head>', '</ HEAD >']:
        pos = content.upper().find(pattern.upper())
        if pos != -1:
            head_end = pos
            break
    
    # If </head> not found, find after <head> meta tags
    if head_end == -1:
        # Find end of head section based on meta/link tags
        head_end = content.upper().find('</head>')
        if head_end == -1:
            # No </head> found - find after the last link/meta before body
            last_link = content.rfind('<link')
            last_meta = content.rfind('<meta')
            last_style = content.rfind('<style')
            
            # Find position after these tags and before </body>
            max_pos = max([
                content.rfind('\n', 0, last_link) if last_link != -1 else 0,
                content.rfind('\n', 0, last_meta) if last_meta != -1 else 0,
                content.rfind('\n', 0, last_style) if last_style != -1 else 0,
                0
            ])
            head_end = max_pos
            if head_end > 0:
                head_end += 1  # Move past the newline
    
    # Build theme CSS links
    theme_css_links = "\n  ".join([
        f'<link rel="stylesheet" href="/static/css/{theme}.css">'
        for theme in THEME_CSS_FILES
    ])
    
    # Find </body> position
    body_end = content.upper().find('</body>')
    
    # Check if theme picker JS already exists
    has_picker_js = '<script src="/static/css/theme-picker.js"></script>' in content
    
    # Build the insertion string
    insertion = f"\n  <script src=\"{THEME_PICKER_JS}\"></script>\n"
    
    # Check for existing theme links (normalize paths for comparison)
    existing_themes = set()
    for theme in THEME_CSS_FILES:
        # Check various patterns
        if f'/static/css/{theme}.css"' in content:
            existing_themes.add(theme)
        elif f'href="/static/css/{theme}.css"' in content:
            existing_themes.add(theme)
        elif f"href='/static/css/{theme}.css'" in content:
            existing_themes.add(theme)
    
    # Build new theme links for missing themes
    missing_themes = [t for t in THEME_CSS_FILES if t not in existing_themes]
    
    if missing_themes:
        # Build links for missing themes only
        new_theme_links = "\n  ".join([
            f'<link rel="stylesheet" href="/static/css/{theme}.css">'
            for theme in missing_themes
        ])
    else:
        # All themes exist, just use empty string
        new_theme_links = ""
    
    # Apply fixes
    new_content = content
    
    # 1. Insert theme CSS links before </head>
    if head_end != -1 and new_theme_links:
        insert_pos = content.rfind('\n', 0, head_end)
        new_content = new_content[:insert_pos] + "\n  " + new_theme_links + "\n" + new_content[insert_pos:]
    
    # 2. Insert theme picker JS before </body>
    if body_end != -1 and not has_picker_js:
        insert_pos = content.rfind('\n', 0, body_end)
        new_content = new_content[:insert_pos] + insertion + new_content[insert_pos:]
    
    # 3. Fix malformed head section (remove duplicate theme links outside </head>)
    # Pattern: </head><link or </head> followed by link tags
    malformed_pattern = r'</head>(?<!/\*)(?:\n|\s*)<(?:link|meta|style|script)[^>]*'
    
    # Find and remove theme links that appear after </head> but before </body>
    # These are the malformed ones
    malformed_match = re.search(r'</head>[\s\n]*(?:<(?:link|meta|style|script)[^>]*\s*/?>)*', new_content)
    
    if malformed_match:
        # This is the malformed section - find where it ends (next </body>)
        malformed_section = new_content[malformed_match.end():body_end]
        
        # Count existing theme links in this malformed section
        existing_in_malformed = sum(1 for theme in THEME_CSS_FILES if theme in malformed_section)
        
        if existing_in_malformed < len(THEME_CSS_FILES):
            # Need to add missing themes before </body> but keep structure
            # Remove the malformed section and rebuild properly
            new_content = new_content[:malformed_match.end()] + "\n  " + new_theme_links + "\n" + new_content[body_end:]
            new_content = new_content[:new_content.rfind('\n</body>')] + insertion + new_content[new_content.rfind('\n</body>'):]
    
    # Write if changed
    if new_content != content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Fixed and updated")
            return True
        except Exception as e:
            print(f"  ERROR writing: {e}")
            return False
    
    print(f"  Already correct")
    return True

def main():
    """Process all HTML files."""
    
    print("=" * 70)
    print("Venus Theme Picker Rollout - Fix All Files")
    print("=" * 70)
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(VENUSSITE):
        if '/themes/' in root or '/layouts/' in root or '/public/' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                html_files.append(filepath)
    
    html_files = sorted(set(html_files))
    print(f"\nFound {len(html_files)} HTML files")
    
    # Process each
    updated = 0
    for filepath in html_files:
        if fix_html_file(filepath):
            updated += 1
    
    print(f"\n{'=' * 70}")
    print(f"Complete! Updated {updated} files")
    print("=" * 70)

if __name__ == "__main__":
    main()
