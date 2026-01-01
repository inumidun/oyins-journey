export interface AnalyticsEvent {
  section: string;
  timestamp: number;
  sessionId: string;
}

export interface VisitorAnalytics {
  pageViews: number;
  uniqueVisitors: number;
  popularSections: SectionStats[];
  timeRange: string;
}

export interface SectionStats {
  section: string;
  views: number;
  percentage: number;
}

class AnalyticsService {
  private static instance: AnalyticsService;
  private sessionId: string;
  private events: AnalyticsEvent[] = [];

  private constructor() {
    this.sessionId = this.generateSessionId();
    this.loadStoredEvents();
  }

  public static getInstance(): AnalyticsService {
    if (!AnalyticsService.instance) {
      AnalyticsService.instance = new AnalyticsService();
    }
    return AnalyticsService.instance;
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private loadStoredEvents(): void {
    try {
      const stored = localStorage.getItem('portfolio_analytics');
      if (stored) {
        this.events = JSON.parse(stored);
      }
    } catch (error) {
      console.warn('Failed to load stored analytics events:', error);
      this.events = [];
    }
  }

  private saveEvents(): void {
    try {
      // Keep only last 1000 events to prevent storage bloat
      const eventsToStore = this.events.slice(-1000);
      localStorage.setItem('portfolio_analytics', JSON.stringify(eventsToStore));
    } catch (error) {
      console.warn('Failed to save analytics events:', error);
    }
  }

  public recordPageView(section: string): void {
    const event: AnalyticsEvent = {
      section,
      timestamp: Date.now(),
      sessionId: this.sessionId
    };

    this.events.push(event);
    this.saveEvents();

    // In a real implementation, you would also send this to your backend
    // For now, we'll just store it locally for the admin dashboard
    console.debug('Analytics: Page view recorded', { section, sessionId: this.sessionId });
  }

  public getAnalytics(timeRange: string = '7d'): VisitorAnalytics {
    const now = Date.now();
    const timeRangeMs = this.parseTimeRange(timeRange);
    const cutoffTime = now - timeRangeMs;

    // Filter events within time range
    const recentEvents = this.events.filter(event => event.timestamp >= cutoffTime);

    // Calculate unique visitors (unique session IDs)
    const uniqueSessions = new Set(recentEvents.map(event => event.sessionId));
    const uniqueVisitors = uniqueSessions.size;

    // Calculate total page views
    const pageViews = recentEvents.length;

    // Calculate popular sections
    const sectionCounts = new Map<string, number>();
    recentEvents.forEach(event => {
      sectionCounts.set(event.section, (sectionCounts.get(event.section) || 0) + 1);
    });

    const popularSections: SectionStats[] = Array.from(sectionCounts.entries())
      .map(([section, views]) => ({
        section,
        views,
        percentage: pageViews > 0 ? Math.round((views / pageViews) * 100) : 0
      }))
      .sort((a, b) => b.views - a.views)
      .slice(0, 10); // Top 10 sections

    return {
      pageViews,
      uniqueVisitors,
      popularSections,
      timeRange
    };
  }

  private parseTimeRange(timeRange: string): number {
    const unit = timeRange.slice(-1);
    const value = parseInt(timeRange.slice(0, -1));

    switch (unit) {
      case 'h': return value * 60 * 60 * 1000; // hours
      case 'd': return value * 24 * 60 * 60 * 1000; // days
      case 'w': return value * 7 * 24 * 60 * 60 * 1000; // weeks
      case 'm': return value * 30 * 24 * 60 * 60 * 1000; // months (approximate)
      default: return 7 * 24 * 60 * 60 * 1000; // default to 7 days
    }
  }

  public clearAnalytics(): void {
    this.events = [];
    localStorage.removeItem('portfolio_analytics');
  }

  // Privacy-compliant method - no PII collection
  public getPrivacyInfo(): string {
    return 'Analytics data is stored locally in your browser and contains no personally identifiable information. Only page sections visited and anonymous session IDs are tracked.';
  }
}

// Export singleton instance
export const analyticsService = AnalyticsService.getInstance();

// React hook for analytics
export const useAnalytics = () => {
  const recordPageView = (section: string) => {
    analyticsService.recordPageView(section);
  };

  const getAnalytics = (timeRange?: string) => {
    return analyticsService.getAnalytics(timeRange);
  };

  const clearAnalytics = () => {
    analyticsService.clearAnalytics();
  };

  const getPrivacyInfo = () => {
    return analyticsService.getPrivacyInfo();
  };

  return {
    recordPageView,
    getAnalytics,
    clearAnalytics,
    getPrivacyInfo
  };
};