#!/usr/bin/env python3
"""
Theme Picker Rollout Script for Venus Website
Clean implementation that properly adds all 7 theme CSS files and theme-picker.js
"""

import os
import re

VENUSSITE = "/home/paul/.openclaw/workspaces/assistant/venus-site"

THEME_CSS = [
    "theme-dark-rose.css",
    "theme-dark-blue.css",
    "theme-dark-green.css",
    "theme-light.css",
    "theme-midnight-gold.css",
    "theme-neon-cyber.css",
    "theme-deep-violet.css"
]

THEME_PICKER_JS = "/static/css/theme-picker.js"

def normalize_path(path):
    """Normalize CSS path for comparison."""
    return f'/static/css/{os.path.basename(path)}'

def has_theme_css(content):
    """Check if content already has a theme CSS."""
    for theme in THEME_CSS:
        if f'/static/css/{theme}' in content or f'/static/css/{theme}' in content:
            return True
    return False

def add_theme_css_links(head_content):
    """Add all 7 theme CSS links to head section."""
    
    # Build theme links HTML
    theme_links = "\n  ".join([
        f'<link rel="stylesheet" href="/static/css/{theme}.css">'
        for theme in THEME_CSS
    ])
    
    # Find insertion point - after </head> or after existing theme links
    # Strategy: Find </head> and insert before it, or after existing theme links
    
    # First check if </head> exists
    if '</head>' in head_content:
        head_pos = head_content.upper().find('</head>')
        # Insert before </head>
        # Find the newline before </head> if exists
        newline_pos = head_content.rfind('\n', 0, head_pos)
        insert_pos = newline_pos if newline_pos != -1 else head_pos
        return head_content[:insert_pos] + "\n  " + theme_links + head_content[insert_pos:]
    
    return head_content

def ensure_theme_picker_js(body_content):
    """Ensure theme-picker.js is added before </body>."""
    
    # Check if already present
    if '<script src="/static/css/theme-picker.js"></script>' in body_content:
        return body_content
    
    # Find </body> and insert before
    body_pos = body_content.upper().find('</body>')
    if body_pos != -1:
        insert_pos = body_content.rfind('\n', 0, body_pos)
        return body_content[:insert_pos] + "\n  <script src="/static/css/theme-picker.js"></script>\n" + body_content[insert_pos:]
    
    return body_content

def process_html_file(filepath):
    """Process a single HTML file."""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
        return False
    
    original = content
    
    # Add theme CSS if needed
    if not has_theme_css(content):
        content = add_theme_css_links(content)
        print(f"    Added theme CSS links")
    
    # Ensure theme-picker.js is present
    content = ensure_theme_picker_js(content)
    
    # Only write if content changed
    if content != original:
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
