#!/usr/bin/env python3
"""
Comprehensive fix: Rebuild ALL HTML files with proper structure
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

THEME_PICKER_JS = "/static/css/theme-picker.js"

def extract_content_between(start_tag, end_tag, content):
    """Extract content between opening and closing tags (case insensitive)."""
    start = content.lower().find(start_tag)
    end = content.upper().find(end_tag)
    
    if start == -1 or end == -1 or end <= start:
        return None, None, None
    
    return content[start:end], start + len(start_tag), end

def fix_file(filepath):
    """Comprehensive fix for single HTML file."""
    
    print(f"\nProcessing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading: {e}")
        return False
    
    # Extract sections
    head_content, head_start, head_end = extract_content_between('<head>', '</head>', content)
    body_content, body_start, body_end = extract_content_between('<body>', '</body>', content)
    
    # Extract metadata
    title = ""
    description = ""
    keywords = ""
    verification = ""
    
    if head_content is not None:
        # Get title
        title_match = re.search(r'<title>(.+?)</title>', head_content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        
        # Get description
        desc_match = re.search(r'<meta name="description" content="([^"]*)">', head_content, re.IGNORECASE)
        if desc_match:
            description = desc_match.group(1).strip()
        
        # Get keywords
        kw_match = re.search(r'<meta name="keywords" content="([^"]*)">', head_content, re.IGNORECASE)
        if kw_match:
            keywords = kw_match.group(1).strip()
        
        # Get verification meta
        verify_match = re.search(r"<meta[^>]*value=['\"]([^'\"]*)['\"]>", head_content)
        if verify_match:
            verification = verify_match.group(1).strip()
    
    # Extract nav section if exists
    nav_match = re.search(r'<nav[^>]*>(.+?)</nav>', content, re.IGNORECASE | re.DOTALL)
    nav_html = nav_match.group(1).strip() if nav_match else ""
    
    # Extract main content if exists
    main_match = re.search(r'<main[^>]*>(.+?)</main>', content, re.IGNORECASE | re.DOTALL)
    main_html = main_match.group(1).strip() if main_match else ""
    
    # Extract hero section if exists (for pages with hero)
    hero_match = re.search(r'<section class="hero">(.*?)</section>', content, re.IGNORECASE | re.DOTALL)
    hero_html = hero_match.group(1).strip() if hero_match else ""
    
    # Extract newsletter section if exists
    newsletter_match = re.search(r'<section class="section newsletter-section">(.*?)</section>', content, re.IGNORECASE | re.DOTALL)
    newsletter_html = newsletter_match.group(1).strip() if newsletter_match else ""
    
    # Extract testimonials section
    testimonials_match = re.search(r'<section class="section testimonials-section">(.*?)</section>', content, re.IGNORECASE | re.DOTALL)
    testimonials_html = testimonials_match.group(1).strip() if testimonials_match else ""
    
    # Extract review section (for product pages)
    review_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.IGNORECASE | re.DOTALL)
    
    # Rebuild head section with all theme CSS
    head_new = f'''<!DOCTYPE html>
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
  <link rel="stylesheet" href="/static/css/theme-deep-violet.css">
'''
    
    if verification:
        head_new += f'  <meta name=\'impact-site-verification\' value=\'{verification}\'>\n'
    
    if description:
        head_new += f'  <meta name="description" content="{description}">\n'
    
    if keywords:
        head_new += f'  <meta name="keywords" content="{keywords}">\n'
    
    head_new += '\n</head>\n'
    
    # Rebuild body with proper sections
    body_new = ""
    
    # Add nav if exists
    if nav_html:
        body_new += f'  {nav_html}\n\n'
    else:
        # Add default nav
        body_new += '''  <nav class="nav">
  <div class="nav-content">
    <a href="/" class="nav-brand">Venus<span>Reviews</span></a>
    <ul class="nav-links">
      <li><a href="/">Home</a></li>
      <li><a href="/products/">Reviews</a></li>
      <li><a href="/guides/">Buying Guides</a></li>
      <li><a href="/best-for/">Best For</a></li>
      <li><a href="/about/">About</a></li>
    </ul>
  </div>
</nav>\n\n'''
    
    # Add hero if exists
    if hero_html:
        body_new += f'  {hero_html}\n\n'
    
    # Add main content if exists (without </main>)
    if main_html:
        main_text = main_html.rsplit('</main>', 1)[0]
        body_new += f'  {main_text}\n\n'
    
    # Add newsletter if exists
    if newsletter_html:
        body_new += f'  {newsletter_html}\n\n'
    
    # Add testimonials if exists
    if testimonials_html:
        body_new += f'  {testimonials_html}\n\n'
    
    # Add footer
    body_new += '''  <footer class="footer">
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
</footer>\n\n'''
    
    # Add scripts
    body_new += '  <script src="/static/css/theme-switcher.js"></script>\n'
    
    # Always add theme picker JS
    body_new += f'  <script src="{THEME_PICKER_JS}"></script>\n'
    
    # Combine
    new_html = head_new + body_new + '</html>\n'
    
    # Write back if changed
    if new_html != content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"  Updated!")
            return True
        except Exception as e:
            print(f"  ERROR writing: {e}")
            return False
    
    print(f"  No changes needed")
    return True

def main():
    print("=" * 70)
    print("COMPREHENSIVE FIX - All HTML Files")
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
        if fix_file(filepath):
            updated += 1
    
    print(f"\n{'=' * 70}")
    print(f"COMPLETE! Updated {updated} of {len(html_files)} files")
    print("=" * 70)

if __name__ == "__main__":
    main()
