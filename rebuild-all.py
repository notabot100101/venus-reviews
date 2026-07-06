#!/usr/bin/env python3
"""
Rebuild all HTML files with proper structure including:
- All 7 theme CSS files in <head>
- theme-picker.js before </body>
"""

import os

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

def extract_body_content(html):
    """Extract everything between <body> and </body> tags."""
    start = html.lower().find('<body>') + 6
    end = html.upper().find('</body>')
    return html[start:end]

def rebuild_html_file(filepath):
    """Rebuild a single HTML file with proper structure."""
    
    print(f"\nProcessing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading: {e}")
        return False
    
    # Build new head section
    # Extract meta info from existing file
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    description_match = re.search(r'<meta name="description" content="(.*?)">', content, re.IGNORECASE)
    keywords_match = re.search(r'<meta name="keywords" content="(.*?)">', content, re.IGNORECASE)
    verification_match = re.search(r"<meta name='[^']*' value='([^']*)">', content)
    
    # Build title
    if title_match:
        title = title_match.group(1)
    else:
        title = "Venus Reviews"
    
    # Build description
    if description_match:
        desc = description_match.group(1)
    else:
        desc = "Venus Reviews content"
    
    # Build keywords
    if keywords_match:
        keywords = keywords_match.group(1)
    else:
        keywords = "pleasure products, reviews"
    
    # Build verification meta if present
    verification_meta = verification_match.group(1) if verification_match else ""
    
    # Build new head
    new_head = f"""<!DOCTYPE html>
<html lang="en">
<head>
	<meta name="generator" content="Hugo">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  
  <link rel="stylesheet" href="/css/main.css">
  <link rel="stylesheet" href="/static/css/theme-dark-rose.css">
  <link rel="stylesheet" href="/static/css/theme-dark-blue.css">
  <link rel="stylesheet" href="/static/css/theme-dark-green.css">
  <link rel="stylesheet" href="/static/css/theme-light.css">
  <link rel="stylesheet" href="/static/css/theme-midnight-gold.css">
  <link rel="stylesheet" href="/static/css/theme-neon-cyber.css">
  <link rel="stylesheet" href="/static/css/theme-deep-violet.css">"""
    
    if verification_meta:
        new_head += f'\n  <meta name=\'impact-site-verification\' value=\'{verification_meta}\'>'
    
    if description_match:
        new_head += f'\n  <meta name="description" content="{desc}">'
    
    if keywords_match:
        new_head += f'\n  <meta name="keywords" content="{keywords}">'
    
    new_head += '\n</head>'
    
    # Extract body content
    body_start = content.upper().find('<body>') + 6
    body_end = content.upper().find('</body>')
    
    if body_start == -1 or body_end == -1:
        print("  WARNING: Could not find body tags")
        return False
    
    body_content = content[body_start:body_end]
    
    # Add theme picker JS to body
    new_body = body_content
    if '<script src="/static/css/theme-picker.js"></script>' not in new_body:
        new_body = new_body + f"\n  <script src=\"{THEME_PICKER_JS}\"></script>"
    
    # Build complete HTML
    new_html = new_head + '\n' + new_body + '\n</html>\n'
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"  Updated")
        return True
    except Exception as e:
        print(f"  ERROR writing: {e}")
        return False

import re

def main():
    """Process all HTML files."""
    
    print("=" * 70)
    print("Rebuild All HTML Files")
    print("=" * 70)
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(VENUSSITE):
        if '/themes/' in root or '/layouts/' in root or '/public/' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    
    html_files = sorted(set(html_files))
    print(f"\nFound {len(html_files)} HTML files")
    
    updated = 0
    for filepath in html_files:
        if rebuild_html_file(filepath):
            updated += 1
    
    print(f"\n{'=' * 70}")
    print(f"Complete! Updated {updated} of {len(html_files)} files")
    print("=" * 70)

if __name__ == "__main__":
    main()
