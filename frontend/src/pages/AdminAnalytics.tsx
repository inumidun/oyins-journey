import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  ArrowLeft, 
  BarChart3, 
  Users, 
  Eye, 
  TrendingUp,
  RefreshCw,
  Info,
  Trash2
} from 'lucide-react';
import { useAnalytics, VisitorAnalytics } from '@/services/analytics';

export const AdminAnalytics: React.FC = () => {
  const navigate = useNavigate();
  const { getAnalytics, clearAnalytics, getPrivacyInfo } = useAnalytics();
  const [analytics, setAnalytics] = useState<VisitorAnalytics | null>(null);
  const [timeRange, setTimeRange] = useState('7d');
  const [showPrivacyInfo, setShowPrivacyInfo] = useState(false);

  const loadAnalytics = () => {
    const data = getAnalytics(timeRange);
    setAnalytics(data);
  };

  useEffect(() => {
    loadAnalytics();
  }, [timeRange]);

  const handleClearAnalytics = () => {
    if (confirm('Are you sure you want to clear all analytics data? This action cannot be undone.')) {
      clearAnalytics();
      loadAnalytics();
    }
  };

  const timeRangeOptions = [
    { value: '24h', label: 'Last 24 Hours' },
    { value: '7d', label: 'Last 7 Days' },
    { value: '30d', label: 'Last 30 Days' },
    { value: '90d', label: 'Last 90 Days' }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="sm" onClick={() => navigate('/admin')}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
            <div>
              <h1 className="text-2xl font-bold">Analytics Dashboard</h1>
              <p className="text-muted-foreground">Visitor statistics and engagement metrics</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button variant="outline" size="sm" onClick={loadAnalytics}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              onClick={() => setShowPrivacyInfo(!showPrivacyInfo)}
            >
              <Info className="h-4 w-4 mr-2" />
              Privacy
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Privacy Information */}
        {showPrivacyInfo && (
          <Alert className="mb-6">
            <Info className="h-4 w-4" />
            <AlertDescription>
              {getPrivacyInfo()}
            </AlertDescription>
          </Alert>
        )}

        {/* Time Range Selector */}
        <div className="mb-6">
          <Tabs value={timeRange} onValueChange={setTimeRange}>
            <TabsList>
              {timeRangeOptions.map(option => (
                <TabsTrigger key={option.value} value={option.value}>
                  {option.label}
                </TabsTrigger>
              ))}
            </TabsList>
          </Tabs>
        </div>

        {analytics && (
          <>
            {/* Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Page Views</CardTitle>
                  <Eye className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{analytics.pageViews.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    {timeRange === '24h' ? 'in the last 24 hours' : `in the last ${timeRange}`}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Unique Visitors</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{analytics.uniqueVisitors.toLocaleString()}</div>
                  <p className="text-xs text-muted-foreground">
                    Unique sessions tracked
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Avg. Views per Visitor</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {analytics.uniqueVisitors > 0 
                      ? (analytics.pageViews / analytics.uniqueVisitors).toFixed(1)
                      : '0'
                    }
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Pages per session
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Popular Sections */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <BarChart3 className="h-5 w-5" />
                  <span>Popular Sections</span>
                </CardTitle>
                <CardDescription>
                  Most visited sections of your portfolio
                </CardDescription>
              </CardHeader>
              <CardContent>
                {analytics.popularSections.length > 0 ? (
                  <div className="space-y-4">
                    {analytics.popularSections.map((section, index) => (
                      <div key={section.section} className="flex items-center space-x-4">
                        <div className="flex-shrink-0 w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center text-sm font-medium">
                          {index + 1}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-medium capitalize">
                              {section.section.replace(/([A-Z])/g, ' $1').trim()}
                            </span>
                            <span className="text-sm text-muted-foreground">
                              {section.views} views ({section.percentage}%)
                            </span>
                          </div>
                          <div className="w-full bg-secondary rounded-full h-2">
                            <div 
                              className="bg-primary h-2 rounded-full transition-all duration-300"
                              style={{ width: `${section.percentage}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <BarChart3 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No data available for the selected time range.</p>
                    <p className="text-sm">Visit your portfolio to start collecting analytics.</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Data Management */}
            <Card>
              <CardHeader>
                <CardTitle>Data Management</CardTitle>
                <CardDescription>
                  Manage your analytics data and privacy settings
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h4 className="font-medium">Clear Analytics Data</h4>
                      <p className="text-sm text-muted-foreground">
                        Remove all stored analytics data from local storage
                      </p>
                    </div>
                    <Button 
                      variant="destructive" 
                      size="sm"
                      onClick={handleClearAnalytics}
                    >
                      <Trash2 className="h-4 w-4 mr-2" />
                      Clear Data
                    </Button>
                  </div>
                  
                  <div className="p-4 bg-muted/50 rounded-lg">
                    <h4 className="font-medium mb-2">Privacy Notice</h4>
                    <p className="text-sm text-muted-foreground">
                      This analytics system is privacy-first and GDPR compliant:
                    </p>
                    <ul className="text-sm text-muted-foreground mt-2 space-y-1">
                      <li>• No personal information is collected</li>
                      <li>• No IP addresses are stored</li>
                      <li>• Data is stored locally in your browser</li>
                      <li>• Only page sections and anonymous session IDs are tracked</li>
                      <li>• You can clear all data at any time</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </main>
    </div>
  );
};