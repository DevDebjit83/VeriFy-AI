// Statistics Tracker
// Tracks all scans, detections, and performance metrics

const STATS_TRACKER = {
  /**
   * Record a completed scan
   * @param {Object} scanData - Scan data object
   */
  async recordScan(scanData) {
    const stats = await this.getStats();
    
    // Update statistics
    stats.totalScans++;
    stats.lastScan = Date.now();
    
    // Count fake items by type
    if (scanData.results && Array.isArray(scanData.results)) {
      scanData.results.forEach(result => {
        if (result.is_fake) {
          stats.totalFakeDetected++;
          
          const type = result.type || 'unknown';
          stats.byType[type] = (stats.byType[type] || 0) + 1;
        }
      });
    }
    
    // Add to scan history
    if (!stats.scanHistory) {
      stats.scanHistory = [];
    }
    
    stats.scanHistory.unshift({
      id: Date.now().toString(),
      url: scanData.url || window.location?.href || 'unknown',
      timestamp: Date.now(),
      totalItems: scanData.results?.length || 0,
      fakeCount: scanData.results?.filter(r => r.is_fake).length || 0,
      duration: scanData.duration || 0,
      results: scanData.results || []
    });
    
    // Keep only last 100 scans
    if (stats.scanHistory.length > 100) {
      stats.scanHistory = stats.scanHistory.slice(0, 100);
    }
    
    // Save statistics
    await chrome.storage.local.set({ statistics: stats });
    
    return stats;
  },

  /**
   * Get current statistics
   * @returns {Promise<Object>} - Statistics object
   */
  async getStats() {
    try {
      const { statistics } = await chrome.storage.local.get('statistics');
      
      return statistics || {
        totalScans: 0,
        totalFakeDetected: 0,
        byType: {
          text: 0,
          image: 0,
          video: 0,
          url: 0,
          voice: 0
        },
        scanHistory: [],
        lastScan: 0,
        firstScan: Date.now()
      };
    } catch (error) {
      console.error('Error getting statistics:', error);
      return this.getDefaultStats();
    }
  },

  /**
   * Get default statistics object
   * @returns {Object} - Default statistics
   */
  getDefaultStats() {
    return {
      totalScans: 0,
      totalFakeDetected: 0,
      byType: {
        text: 0,
        image: 0,
        video: 0,
        url: 0,
        voice: 0
      },
      scanHistory: [],
      lastScan: 0,
      firstScan: Date.now()
    };
  },

  /**
   * Reset all statistics
   */
  async resetStats() {
    await chrome.storage.local.set({ statistics: this.getDefaultStats() });
  },

  /**
   * Get scan history
   * @param {number} limit - Maximum number of scans to return
   * @returns {Promise<Array>} - Array of scan history objects
   */
  async getScanHistory(limit = 10) {
    const stats = await this.getStats();
    return stats.scanHistory.slice(0, limit);
  },

  /**
   * Get statistics summary for display
   * @returns {Promise<Object>} - Formatted statistics summary
   */
  async getSummary() {
    const stats = await this.getStats();
    
    // Calculate detection rate
    const detectionRate = stats.totalScans > 0 
      ? (stats.totalFakeDetected / stats.totalScans) * 100 
      : 0;
    
    // Find most common fake type
    let mostCommonType = 'none';
    let maxCount = 0;
    Object.entries(stats.byType).forEach(([type, count]) => {
      if (count > maxCount) {
        maxCount = count;
        mostCommonType = type;
      }
    });
    
    // Calculate days since first scan
    const daysSinceFirst = stats.firstScan 
      ? Math.floor((Date.now() - stats.firstScan) / (1000 * 60 * 60 * 24))
      : 0;
    
    return {
      totalScans: stats.totalScans,
      totalFakeDetected: stats.totalFakeDetected,
      detectionRate: detectionRate.toFixed(1),
      byType: stats.byType,
      mostCommonType: mostCommonType,
      lastScan: stats.lastScan,
      daysSinceFirst: daysSinceFirst,
      scansPerDay: daysSinceFirst > 0 ? (stats.totalScans / daysSinceFirst).toFixed(1) : 0
    };
  },

  /**
   * Export statistics as JSON
   * @returns {Promise<string>} - JSON string of statistics
   */
  async exportStats() {
    const stats = await this.getStats();
    const summary = await this.getSummary();
    
    return JSON.stringify({
      summary: summary,
      fullStats: stats,
      exportDate: new Date().toISOString()
    }, null, 2);
  },

  /**
   * Get statistics for a specific time period
   * @param {number} days - Number of days to look back
   * @returns {Promise<Object>} - Statistics for time period
   */
  async getStatsForPeriod(days = 7) {
    const stats = await this.getStats();
    const cutoffTime = Date.now() - (days * 24 * 60 * 60 * 1000);
    
    // Filter scan history for period
    const periodScans = stats.scanHistory.filter(scan => 
      scan.timestamp >= cutoffTime
    );
    
    // Calculate period statistics
    const periodFakeCount = periodScans.reduce((sum, scan) => 
      sum + scan.fakeCount, 0
    );
    
    return {
      days: days,
      scans: periodScans.length,
      fakeDetected: periodFakeCount,
      avgFakePerScan: periodScans.length > 0 
        ? (periodFakeCount / periodScans.length).toFixed(2) 
        : 0
    };
  }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = STATS_TRACKER;
}
