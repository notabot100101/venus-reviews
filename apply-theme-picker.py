#!/usr/bin/env python3
"""
Theme Picker Rollout Script for Venus Website
Adds all 7 theme CSS files and theme-picker.js to every page.
"""

import os
import re
import sys

VENUSSITE = "/home/paul/.openclaw/workspaces/assistant/venus-site"

THEME_CSS = [
    "/static/css/theme-dark-rose.css",
    "/static/css/theme-dark-blue.css",
    "/static/css/theme-dark-green.css",
    "/static/css/theme-light.css",
    "/static/css/theme-midnight-gold.css",
    "/static/css/theme-neon-cyber.css",
    "/static/css/theme-deep-violet.css"
]

THEME_PICKER_JS = "/static/css/theme-picker.js"

def add_theme_css(head_content):
    """Add all theme CSS links after the main.css link in the head section."""
    
    # Check if theme CSS already exists (avoid duplicates)
    existing_themes = [
        t for t in THEME_CSS 
        if 'href="{t}"' in head_content or "href='{t}'" in head_content or 'href="/static/css/' + os.path.basename(t) + '"' in head_content
    ]
    
    if len(existing_themes) >= len(THEME_CSS):
        return head_content  # All themes already present
    
    # Find position after the last theme link or after main.css
    theme_pattern = r'</head>|<link.*?theme-(?:dark-rose|dark-blue|dark-green|light|midnight-gold|neon-cyber|deep-violet)\.css'
    
    match = re.search(theme_pattern, head_content, re.IGNORECASE)
    if match:
        insert_pos = match.end()
        existing_links = set(existing_themes)
        missing_links = [t for t in THEME_CSS if t not in existing_links]
        
        if missing_links:
            theme_css_links = "\n  ".join(['<link rel="stylesheet" href="' + t + '">' for t in missing_links])
            # Check if there's a newline at insert_pos
            if insert_pos < len(head_content) and head_content[insert_pos:insert_pos+1].isspace():
                return head_content[:insert_pos] + theme_css_links + head_content[insert_pos:]
            else:
                return head_content[:insert_pos] + "\n" + theme_css_links + head_content[insert_pos:]
    
    # Fallback: find </head> and add before it
    head_end = head_content.upper().find('</head>')
    if head_end != -1:
        theme_css_links = "\n  ".join(['<link rel="stylesheet" href="' + t + '">' for t in THEME_CSS])
        return head_content[:head_end] + "\n" + theme_css_links + head_content[head_end:]
    
    return head_content

def add_theme_picker_js(body_content):
    """Add theme-picker.js script before </body> tag if not present."""
    if '<script src="/static/css/theme-picker.js"></script>' in body_content:
        return body_content  # Already present
    
    # Find </body> and insert before
    body_end = body_content.upper().find('</body>')
    if body_end != -1:
        picker_script = '\n  <script src="/static/css/theme-picker.js"></script>\n'
        return body_content[:body_end] + picker_script + body_content[body_end:]
    
    return body_content

def process_html_file(filepath):
    """Process a single HTML file, adding theme CSS and picker JS."""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
        return False
    
    original = content
    theme_added = False
    picker_added = False
    
    # Add theme CSS to head
    content = add_theme_css(content)
    if content != original:
        theme_added = True
        original = content
    
    # Add theme picker JS to body
    content = add_theme_picker_js(content)
    if content != original:
        picker_added = True
    
    # Only write if content changed
    if theme_added or picker_added:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated: {filepath}")
            return True
        except Exception as e:
            print(f"  ERROR writing {filepath}: {e}")
            return False
    
    return False

def main():
    """Main function to find and process all HTML files."""
    
    print("=" * 70)
    print("Venus Theme Picker Rollout")
    print("=" * 70)
    print()
    
    # Find all HTML files (excluding templates)
    html_files = []
    for root, dirs, files in os.walk(VENUSSITE):
        # Skip template directories
        if '/themes/' in root or '/layouts/' in root or '/public/' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                filepath = os.path.join(root, f)
                html_files.append(filepath)
    
    # Remove duplicates and sort
    html_files = sorted(set(html_files))
    
    print(f"Found {len(html_files)} HTML files to process")
    print()
    
    # Process each file
    updated = 0
    for filepath in html_files:
        print(f"Processing: {filepath}")
        if process_html_file(filepath):
            updated += 1
    
    print()
    print("=" * 70)
    print(f"Complete! Updated {updated} of {len(html_files)} files")
    print("=" * 70)

if __name__ == "__main__":
    main()
