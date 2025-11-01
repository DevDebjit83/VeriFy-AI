// Domain Warning System - Enhanced Content Script Features
// This extends content.js with domain reputation checking

// Known fake domains (from backend reputation system)
const FAKE_DOMAINS = [
  'naturalnews.com', 'infowars.com', 'beforeitsnews.com',
  'worldtruth.tv', 'yournewswire.com', 'neonnettle.com',
  'realfarmacy.com', 'thelastamericanvagabond.com',
  'collective-evolution.com', 'activistpost.com',
  'themindunleashed.com', 'davidicke.com', 'newspunch.com',
  'bigleaguepolitics.com', 'thegatewaypundit.com'
];

// Trusted domains (from backend reputation system)
const TRUSTED_DOMAINS = [
  'cdc.gov', 'nih.gov', 'who.int', 'fda.gov', 'nasa.gov',
  'bbc.com', 'bbc.co.uk', 'reuters.com', 'apnews.com',
  'nytimes.com', 'washingtonpost.com', 'theguardian.com',
  'cnn.com', 'npr.org', 'pbs.org', 'wikipedia.org',
  'snopes.com', 'factcheck.org', 'politifact.com'
];

/**
 * Check if current domain is known fake/trusted
 */
function checkDomainReputation() {
  const domain = window.location.hostname.toLowerCase();
  
  // Check if it's a known fake domain
  const isFake = FAKE_DOMAINS.some(fakeDomain => 
    domain.includes(fakeDomain) || fakeDomain.includes(domain)
  );
  
  // Check if it's a trusted domain
  const isTrusted = TRUSTED_DOMAINS.some(trustedDomain => 
    domain.includes(trustedDomain) || trustedDomain.includes(domain)
  );
  
  if (isFake) {
    showDomainWarning({
      type: 'fake',
      icon: '⚠️',
      message: `WARNING: This site (${domain}) is known for spreading misinformation and fake news. Content should be verified from trusted sources.`,
      confidence: 92
    });
  } else if (isTrusted) {
    showDomainWarning({
      type: 'trusted',
      icon: '✅',
      message: `This site (${domain}) is a verified trusted source.`,
      confidence: 93
    });
  }
}

/**
 * Show domain warning banner at top of page
 */
function showDomainWarning(warning) {
  // Check if warning already exists
  if (document.querySelector('.verify-domain-warning')) {
    return;
  }
  
  // Create warning banner
  const banner = document.createElement('div');
  banner.className = `verify-domain-warning verify-domain-${warning.type}`;
  banner.innerHTML = `
    <div class="verify-warning-content">
      <span class="verify-warning-icon">${warning.icon}</span>
      <span class="verify-warning-text">${warning.message}</span>
      <button class="verify-warning-close" aria-label="Close warning">✕</button>
    </div>
  `;
  
  // Add to page (at the very beginning)
  document.body.insertBefore(banner, document.body.firstChild);
  
  // Add close handler
  const closeBtn = banner.querySelector('.verify-warning-close');
  closeBtn.addEventListener('click', () => {
    banner.style.animation = 'verify-slide-up 0.3s ease-in forwards';
    setTimeout(() => banner.remove(), 300);
  });
  
  // Auto-dismiss trusted warnings after 5 seconds
  if (warning.type === 'trusted') {
    setTimeout(() => {
      if (banner.parentNode) {
        banner.style.animation = 'verify-slide-up 0.3s ease-in forwards';
        setTimeout(() => banner.remove(), 300);
      }
    }, 5000);
  }
  
  console.log(`✅ Domain warning shown: ${warning.type} (${warning.confidence}% confident)`);
}

/**
 * Extract all URLs from page for analysis
 */
function extractUrlsFromPage(limit = 20) {
  const urls = new Set();
  
  // Get all links
  document.querySelectorAll('a[href]').forEach(link => {
    const href = link.href;
    if (href && href.startsWith('http') && urls.size < limit) {
      // Skip internal links and anchors
      if (new URL(href).hostname !== window.location.hostname) {
        urls.add(href);
      }
    }
  });
  
  return Array.from(urls);
}

/**
 * Initialize domain checker
 */
function initializeDomainChecker() {
  // Check domain on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkDomainReputation);
  } else {
    checkDomainReputation();
  }
  
  console.log('✅ Domain checker initialized');
}

// Initialize immediately
initializeDomainChecker();

// Add CSS animation for slide up
const style = document.createElement('style');
style.textContent = `
  @keyframes verify-slide-up {
    from {
      transform: translateY(0);
      opacity: 1;
    }
    to {
      transform: translateY(-100%);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);

// Make functions available globally for other scripts
window.VERIFY_DOMAIN = {
  checkDomainReputation,
  showDomainWarning,
  extractUrlsFromPage,
  FAKE_DOMAINS,
  TRUSTED_DOMAINS
};
