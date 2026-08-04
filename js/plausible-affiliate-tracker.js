/**
 * Plausible Analytics Affiliate Link Tracker
 * Tracks outbound affiliate clicks as custom events
 * Privacy-friendly: no cookies, no personal data collection
 */

(function() {
  'use strict';

  // Wait for Plausible to be available
  function trackAffiliateClick(event) {
    var link = event.currentTarget;
    var href = link.getAttribute('href') || '';
    var product = link.getAttribute('data-product') || 'unknown';
    var merchant = link.getAttribute('data-merchant') || extractMerchant(href);
    var location = link.getAttribute('data-location') || 'body';

    // Track with Plausible if available
    if (window.plausible) {
      plausible('Affiliate Click', {
        props: {
          product: product,
          merchant: merchant,
          location: location
        }
      });
    }
  }

  // Extract merchant domain from URL
  function extractMerchant(url) {
    try {
      var urlObj = new URL(url);
      var hostname = urlObj.hostname.replace(/^www\./, '');
      // Map common affiliate domains
      var merchants = {
        'lelo.com': 'Lelo',
        'dameproducts.com': 'Dame',
        'we-vibe.com': 'We-Vibe',
        'lovehoney.com': 'Lovehoney',
        'funfactory.com': 'Fun Factory',
        'womanizer.com': 'Womanizer',
        'shevibe.com': 'SheVibe',
        'spectrumboutique.com': 'Spectrum Boutique',
        'unboundbabes.com': 'Unbound',
        'goodvibes.com': 'Good Vibes',
        'amazon.com': 'Amazon',
        'amzn.to': 'Amazon'
      };
      return merchants[hostname] || hostname;
    } catch (e) {
      return 'unknown';
    }
  }

  // Initialize tracking on DOM ready
  function init() {
    // Track links with data-affiliate attribute
    var affiliateLinks = document.querySelectorAll('a[data-affiliate="true"]');
    affiliateLinks.forEach(function(link) {
      link.addEventListener('click', trackAffiliateClick);
    });

    // Also track any link going to known merchant domains
    var allLinks = document.querySelectorAll('a[href^="http"]');
    allLinks.forEach(function(link) {
      var href = link.getAttribute('href') || '';
      if (isAffiliateLink(href) && !link.hasAttribute('data-affiliate')) {
        link.setAttribute('data-affiliate', 'auto');
        link.addEventListener('click', trackAffiliateClick);
      }
    });
  }

  // Check if URL is an affiliate/merchant link
  function isAffiliateLink(url) {
    var merchants = [
      'lelo.com', 'dameproducts.com', 'we-vibe.com', 'lovehoney.com',
      'funfactory.com', 'womanizer.com', 'shevibe.com', 'amazon.com',
      'amzn.to', 'prf.hn', 'click.linksynergy.com', 'partnershop.link'
    ];
    return merchants.some(function(m) { return url.indexOf(m) !== -1; });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
