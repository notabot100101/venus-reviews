#!/usr/bin/env python3
"""Quick script to rebuild all HTML files with theme picker."""

import os

VENUSSITE = "/home/paul/.openclaw/workspaces/assistant/venus-site"

HEADING = '''<!DOCTYPE html>
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

FOOTER = '''

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
</footer>

  <script src="/static/css/theme-switcher.js"></script>
  <script src="/static/css/theme-picker.js"></script>
</body>
</html>
'''

def rebuild(filepath):
    """Rebuild single HTML file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find title
    title_start = content.upper().find('<TITLE>') + 7 if '<TITLE>' in content.upper() else 0
    title_end = content.upper().find('</TITLE>')
    title = content[title_start:title_end].strip() if title_end > title_start else content[content.upper().find('<TITLE>') + 6:content.upper().find('</TITLE>')].strip()
    
    # Find description meta
    desc_start = content.upper().find('<META NAME="DESCRIPTION"')
    desc_end = content.upper().find('"', desc_start) + 1
    description = content[desc_start+19:desc_end].strip() if desc_start != -1 else ""
    
    # Find keywords meta
    kw_start = content.upper().find('<META NAME="KEYWORDS"')
    kw_end = content.upper().find('"', kw_start) + 1
    keywords = content[kw_start+20:kw_end].strip() if kw_start != -1 else ""
    
    # Find verification meta
    verify_match = '<META NAME=\'IMPACT-SITE-VERIFICATION\' VALUE=\'' in content.upper()
    if verify_match:
        ver_start = content.upper().find('<META NAME=\'IMPACT-SITE-VERIFICATION\' VALUE=\'') + 47
        ver_end = content[ver_start:].find('\'')
        verification = content[ver_start:ver_start+ver_end]
    else:
        verification = ""
    
    # Find body start/end
    body_start = content.upper().find('<BODY>') + 6
    body_end = content.upper().find('</BODY>')
    
    if body_start == -1 or body_end == -1:
        # No body tags found, use template
        body_content = ''
    else:
        body_content = content[body_start:body_end]
    
    # Build new HTML
    new_head = HEADING.format(title=title.strip() if title.strip() else "Venus Reviews")
    
    if body_content:
        new_html = new_head + '\n' + body_content + FOOTER
    else:
        new_html = new_head
    
    with open(filepath, 'w') as f:
        f.write(new_html)
    
    return True

if __name__ == '__main__':
    print("Finding HTML files...")
    files = []
    for root, dirs, files in os.walk(VENUSSITE):
        if '/themes/' in root or '/layouts/' in root or '/public/' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                files.append(os.path.join(root, f))
    
    files = sorted(set(files))
    print(f"Found {len(files)} files")
    
    for f in files:
        print(f"Processing {f}")
        rebuild(f)
    
    print(f"Done! Updated {len(files)} files")
