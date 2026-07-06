#!/usr/bin/env python3
"""
Final Fix: Rebuild all HTML files with proper theme picker structure
"""

import os
import re

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

def fix_html_file(filepath):
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading: {e}")
        return False
    
    # Extract title
    title_match = re.search(r'<title>(.+?)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else ""
    
    # Extract description meta
    desc_match = re.search(r'<meta name="description" content="([^"]*)"', content, re.IGNORECASE)
    description = desc_match.group(1) if desc_match else ""
    
    # Extract keywords meta
    kw_match = re.search(r'<meta name="keywords" content="([^"]*)"', content, re.IGNORECASE)
    keywords = kw_match.group(1) if kw_match else ""
    
    # Extract verification meta - try different patterns
    verification = ""
    verify_patterns = [
        r"<meta name='[^']*' value='([^']*)'>",
        r"<meta name=\"[^"]*\" value=\"([^\"]*)\"",
        r"<meta name=['\"]impact-site-verification['\"] value=['\"]([^'\"]*)['\"]>"
    ]
    for pattern in verify_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            verification = match.group(1)
            break
    
    # Extract body content
    body_start = content.lower().find('<body>')
    body_end = content.upper().find('</body>')
    
    if body_start != -1 and body_end != -1 and body_end > body_start:
        body_content = content[body_start + 6:body_end]
    else:
        body_content = ""
    
    # Extract nav if present
    nav_match = re.search(r'<nav class="nav">(.*?)</nav>', content, re.IGNORECASE | re.DOTALL)
    nav_content = nav_match.group(1) if nav_match else ""
    
    # Build footer
    footer_content = '''

  <footer class="footer">
  <div class="container">
    <div class="footer-content">
      <div class="footer-section">
        <h3>Venus Reviews</h3>
        <p style="color: rgba(255, 255, 255, 0.7); line-height: 1.7;">
          Expert reviews and discreet analysis of premium pleasure products for US and global customers. Honest, privacy-focused reviews with US shipping.
        </p>
      </div>
      
      <div class="footer-section">
        <h3>Quick Links</h3>
        <a href="/products/">Product Reviews</a>
        <a href="/guides/">Buying Guides</a>
        <a href="/best-for/">Best For</a>
        <a href="/about/">About Us</a>
      </div>
      
      <div class="footer-section">
        <h3>Our Promise</h3>
        <a href="/privacy/">Privacy Compliant</a>
        <a href="/shipping/">Discreet Shipping</a>
        <a href="/security/">Secure Transactions</a>
        <a href="/contact/">Contact Support</a>
      </div>
      
      <div class="footer-section">
        <h3>Newsletter</h3>
        <p style="color: rgba(255, 255, 255, 0.7);">Subscribe for exclusive reviews and buying guides.</p>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; 2026 Venus Reviews. All rights reserved. | 18&#43;+ Content | Privacy Compliant</p>
      <p style="font-size: 0.8rem; margin-top: var(--space-xs);">Discreet US shipping available &bull; Secure payment processing &bull; 24/7 customer support</p>
    </div>
  </div>
</footer>'''
    
    # Check for theme picker JS
    has_picker_js = '<script src="/static/css/theme-picker.js"></script>' in body_content
    
    # Build theme CSS links
    theme_css_links = "\n  ".join([f'<link rel="stylesheet" href="{t}">' for t in THEME_CSS])
    
    # Build head
    if verification:
        head = f'''<!DOCTYPE html>
<html lang="en">
<head>
	<meta name="generator" content="Hugo">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  
  <link rel="stylesheet" href="/css/main.css">
  {theme_css_links}
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name='impact-site-verification' value='{verification}'>
</head>'''
    else:
        head = f'''<!DOCTYPE html>
<html lang="en">
<head>
	<meta name="generator" content="Hugo">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  
  <link rel="stylesheet" href="/css/main.css">
  {theme_css_links}
</head>'''
    
    # Build body
    if nav_content:
        new_body = nav_content + "\n" + body_content
    else:
        new_body = body_content
    
    # Add theme picker JS if needed
    if not has_picker_js:
        new_body = new_body + '\n  <script src="/static/css/theme-picker.js"></script>'
    
    # Combine
    new_html = head + "\n" + new_body + footer_content + "\n</html>\n"
    
    # Write if changed
    if new_html != content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"  Fixed!")
            return True
        except Exception as e:
            print(f"  ERROR writing: {e}")
            return False
    
    print(f"  Already correct")
    return True

def main():
    print("=" * 70)
    print("FINAL FIX - Theme Picker Rollout")
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
    print(f"\nFound {len(html_files)} HTML files to process")
    
    # Process each
    updated = 0
    for filepath in html_files:
        if fix_html_file(filepath):
            updated += 1
    
    print(f"\n{'=' * 70}")
    print(f"COMPLETE! Updated {updated} of {len(html_files)} files")
    print("=" * 70)

if __name__ == "__main__":
    main()
