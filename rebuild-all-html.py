#!/usr/bin/env python3
"""
Rebuild All HTML Files with Proper Theme Picker Structure
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

# Body content templates for different page types
BODY_TEMPLATES = {
    "default": '''  <nav class="nav">
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
</nav>

  <main>
    <div class="page-header">
      <h1>Page Title</h1>
      <p class="page-header-meta">Page description.</p>
    </div>

    <section class="section">
      <div class="container">
        <h2>Section Title</h2>
        <p>Content goes here.</p>
      </div>
    </section>
  </main>
  
  <footer class="footer">
  <div class="container">
    <div class="footer-content">
      <div class="footer-section">
        <h3>Venus Reviews</h3>
        <p style="color: rgba(255, 255, 255, 0.7); line-height: 1.7;">
          Expert reviews and discreet analysis of premium pleasure products.
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
        <p style="color: rgba(255, 255, 255, 0.7);">Subscribe for exclusive content.</p>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; 2026 Venus Reviews. All rights reserved. | 18&#43;+ Content | Privacy Compliant</p>
      <p style="font-size: 0.8rem; margin-top: var(--space-xs);">Discreet US shipping available &bull; Secure payment processing &bull; 24/7 customer support</p>
    </div>
  </div>
</footer>

  <script src="/static/css/theme-switcher.js"></script>
  <script src="/static/css/theme-picker.js"></script>''',
    
    "newsletter": '''  <nav class="nav">
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
</nav>

  <section class="section newsletter-section">
    <h2 class="section-title">Stay Updated</h2>
    <p class="section-header p">Subscribe to our newsletter for exclusive reviews, buying guides, and early access to new content.</p>
    
    <div class="newsletter">
      <div class="newsletter-content">
        <h2>Subscribe to Our Newsletter</h2>
        <p>Get the latest reviews, buying guides, and special offers delivered to your inbox. We respect your privacy and won't share your email.</p>
        
        <form class="newsletter-form" action="https://formspree.io/f/xpqgkwaj" method="POST">
          <input type="email" name="email" class="newsletter-input" placeholder="Enter your email address" required />
          <button type="submit" class="btn btn-primary">Subscribe</button>
          <div class="newsletter-privacy">
            <input type="checkbox" id="privacy-check" required />
            <label for="privacy-check" style="display: inline;">I agree to receive emails and accept our <a href="/privacy/">Privacy Policy</a></label>
          </div>
        </form>
        
        <div class="newsletter-success" style="display: none; color: #4CAF50; margin-top: 1rem;">
          Thank you for subscribing! Check your email for a confirmation message.
        </div>
      </div>
    </div>
  </section>

  <!-- Trust Section -->
  <section class="section trust-section">
    <div class="container">
      <h2 class="section-title">Why Trust Venus Reviews?</h2>
      <div class="privacy-grid">
        <div class="privacy-item">
          <h5>Independent Testing</h5>
          <p>All products are thoroughly tested by our expert team before review</p>
        </div>
        <div class="privacy-item">
          <h5>Honest Pros & Cons</h5>
          <p>We share both the strengths and weaknesses of every product</p>
        </div>
        <div class="privacy-item">
          <h5>Transparency</h5>
          <p>We disclose affiliate relationships and maintain editorial independence</p>
        </div>
        <div class="privacy-item">
          <h5>Privacy-Focused</h5>
          <p>Your data is protected. We use discreet packaging and secure practices</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
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

  <script>
    function validateNewsletterForm(event) {
      const email = event.target.email.value;
      const privacyCheck = event.target.privacyCheck.checked;
      
      if (!email || !email.includes('@')) {
        alert('Please enter a valid email address.');
        return false;
      }
      
      if (!privacyCheck) {
        alert('You must agree to receive emails and accept our Privacy Policy.');
        return false;
      }
      
      // Simulate subscription
      event.target.style.display = 'none';
      document.querySelector('.newsletter-success').style.display = 'block';
      
      return true;
    }
  </script>''',
}

def build_head(title, description, keywords, verification=""):
    """Build the head section for an HTML file."""
    head = f'''<!DOCTYPE html>
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
        head += f'  <meta name=\'impact-site-verification\' value=\'{verification}\'>\n'
    
    if description:
        head += f'  <meta name="description" content="{description}">\n'
    
    if keywords:
        head += f'  <meta name="keywords" content="{keywords}">\n'
    
    head += '\n</head>\n'
    
    return head

def extract_metadata(content):
    """Extract metadata from existing content."""
    title_match = re.search(r'<title>(.+?)</title>', content, re.IGNORECASE)
    desc_match = re.search(r'<meta name="description" content="(.+?)">', content, re.IGNORECASE)
    kw_match = re.search(r'<meta name="keywords" content="(.+?)">', content, re.IGNORECASE)
    verify_match = re.search(r"<meta name='[^']*' value='([^']*)'>", content)
    
    return {
        'title': title_match.group(1).strip() if title_match else '',
        'description': desc_match.group(1).strip() if desc_match else '',
        'keywords': kw_match.group(1).strip() if kw_match else '',
        'verification': verify_match.group(1) if verify_match else ''
    }

def extract_body(content):
    """Extract body content between <body> and </body> tags."""
    body_start = content.upper().find('<body>') + 6
    body_end = content.upper().find('</body>')
    
    if body_start == -1 or body_end == -1:
        return ""
    
    return content[body_start:body_end]

def rebuild_file(filepath):
    """Rebuild a single HTML file."""
    
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading: {e}")
        return False
    
    # Extract metadata
    metadata = extract_metadata(content)
    
    # Extract existing body content
    existing_body = extract_body(content)
    
    # Determine which body template to use based on existing body content
    if 'newsletter-form' in existing_body.lower() or 'newsletter-section' in existing_body.lower():
        body_template = BODY_TEMPLATES["newsletter"]
    else:
        body_template = BODY_TEMPLATES["default"]
    
    # Build new HTML
    new_head = build_head(
        metadata['title'],
        metadata['description'],
        metadata['keywords'],
        metadata['verification']
    )
    
    # Use existing body content if it's substantial (not just placeholder)
    if len(existing_body) > 100:
        # Use existing body but ensure it has theme-picker.js
        new_body = existing_body
        if '<script src="/static/css/theme-picker.js"></script>' not in new_body:
            new_body = new_body + '\n  <script src="/static/css/theme-picker.js"></script>'
    else:
        # Use template body
        new_body = body_template
    
    # Build complete HTML
    new_html = new_head + '\n' + new_body + '\n</html>\n'
    
    # Write back
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"  Fixed and updated")
        return True
    except Exception as e:
        print(f"  ERROR writing: {e}")
        return False

def main():
    """Process all HTML files."""
    
    print("=" * 70)
    print("Rebuild All HTML Files with Theme Picker")
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
    
    updated = 0
    for filepath in html_files:
        if rebuild_file(filepath):
            updated += 1
    
    print(f"\n{'=' * 70}")
    print(f"Complete! Updated {updated} of {len(html_files)} files")
    print("=" * 70)

if __name__ == "__main__":
    main()
