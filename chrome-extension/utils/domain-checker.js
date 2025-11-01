// Domain Reputation Checker
// Uses the same 45+ domain database as backend

const DOMAIN_CHECKER = {
  // Known fake/misinformation domains (from backend)
  FAKE_DOMAINS: [
    'naturalnews.com',
    'infowars.com',
    'beforeitsnews.com',
    'worldtruth.tv',
    'yournewswire.com',
    'neonnettle.com',
    'realfarmacy.com',
    'thelastamericanvagabond.com',
    'collective-evolution.com',
    'activistpost.com',
    'themindunleashed.com',
    'davidicke.com',
    'newspunch.com',
    'bigleaguepolitics.com',
    'thegatewaypundit.com',
    'breitbart.com',
    'dailycaller.com',
    'conservativetribune.com',
    'thefederalistpapers.org',
    'dcclothesline.com'
  ],

  // Trusted domains (from backend)
  TRUSTED_DOMAINS: [
    'cdc.gov',
    'nih.gov',
    'who.int',
    'fda.gov',
    'nasa.gov',
    'bbc.com',
    'bbc.co.uk',
    'reuters.com',
    'apnews.com',
    'nytimes.com',
    'washingtonpost.com',
    'theguardian.com',
    'cnn.com',
    'npr.org',
    'pbs.org',
    'economist.com',
    'nature.com',
    'science.org',
    'sciencemag.org',
    'wikipedia.org',
    'snopes.com',
    'factcheck.org',
    'politifact.com',
    'fullfact.org',
    'mediabiasfactcheck.com'
  ],

  /**
   * Check if a domain is known to be fake/misinformation
   * @param {string} url - Full URL or domain
   * @returns {Object} - { isFake: boolean, isTrusted: boolean, confidence: number }
   */
  checkDomain(url) {
    try {
      const domain = this.extractDomain(url);
      
      // Check if it's a known fake domain
      const isFake = this.FAKE_DOMAINS.some(fakeDomain => 
        domain.includes(fakeDomain) || fakeDomain.includes(domain)
      );
      
      // Check if it's a trusted domain
      const isTrusted = this.TRUSTED_DOMAINS.some(trustedDomain => 
        domain.includes(trustedDomain) || trustedDomain.includes(domain)
      );
      
      return {
        domain: domain,
        isFake: isFake,
        isTrusted: isTrusted,
        confidence: isFake ? 0.92 : (isTrusted ? 0.93 : 0.5),
        source: isFake ? 'blacklist' : (isTrusted ? 'whitelist' : 'unknown')
      };
    } catch (error) {
      console.error('Domain check error:', error);
      return {
        domain: url,
        isFake: false,
        isTrusted: false,
        confidence: 0.5,
        source: 'error'
      };
    }
  },

  /**
   * Extract domain from URL
   * @param {string} url - Full URL
   * @returns {string} - Domain name
   */
  extractDomain(url) {
    try {
      // If it's already just a domain, return it
      if (!url.includes('/') && !url.includes(':')) {
        return url.toLowerCase();
      }
      
      // Parse as URL
      const urlObj = new URL(url.startsWith('http') ? url : `https://${url}`);
      return urlObj.hostname.toLowerCase();
    } catch (error) {
      // Fallback: extract domain manually
      return url.replace(/^https?:\/\//, '')
                .replace(/^www\./, '')
                .split('/')[0]
                .toLowerCase();
    }
  },

  /**
   * Get warning message for a domain
   * @param {string} url - URL to check
   * @returns {Object|null} - Warning object or null if no warning
   */
  getWarning(url) {
    const check = this.checkDomain(url);
    
    if (check.isFake) {
      return {
        type: 'fake',
        level: 'critical',
        icon: '⚠️',
        title: 'Warning: Misinformation Source',
        message: `This site (${check.domain}) is known for spreading fake news and misinformation.`,
        confidence: check.confidence,
        color: '#ff4757'
      };
    } else if (check.isTrusted) {
      return {
        type: 'trusted',
        level: 'info',
        icon: '✅',
        title: 'Verified Source',
        message: `This site (${check.domain}) is a trusted and reliable news source.`,
        confidence: check.confidence,
        color: '#2ed573'
      };
    }
    
    return null;
  },

  /**
   * Check if current page domain should trigger warning
   * @returns {Object|null} - Warning object or null
   */
  checkCurrentPage() {
    return this.getWarning(window.location.href);
  },

  /**
   * Extract all URLs from a webpage
   * @param {number} limit - Maximum number of URLs to extract
   * @returns {Array<string>} - Array of URLs
   */
  extractUrlsFromPage(limit = 20) {
    const urls = new Set();
    
    // Get all links
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.href;
      if (href && href.startsWith('http') && urls.size < limit) {
        urls.add(href);
      }
    });
    
    return Array.from(urls);
  }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DOMAIN_CHECKER;
}
