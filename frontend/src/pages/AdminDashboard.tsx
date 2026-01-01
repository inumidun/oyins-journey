import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  Settings, 
  FileText, 
  Award, 
  Code, 
  BarChart3, 
  LogOut,
  User,
  Terminal,
  Sparkles,
  Database,
  Globe
} from 'lucide-react';

export const AdminDashboard: React.FC = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header with gradient background */}
      <header className="relative border-b bg-gradient-to-r from-background via-card to-background">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/5 via-primary/10 to-primary/5"></div>
        <div className="relative container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-primary/20 rounded-xl border border-primary/30 glow-primary">
                <Terminal className="h-8 w-8 text-primary" />
              </div>
              <div>
                <h1 className="text-3xl font-bold gradient-text">Admin Portal</h1>
                <p className="text-muted-foreground mt-1">Manage your portfolio content with style</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3 px-4 py-2 bg-card/50 rounded-lg border border-border/50">
                <div className="p-1.5 bg-primary/20 rounded-full">
                  <User className="h-4 w-4 text-primary" />
                </div>
                <span className="text-sm font-medium">{user?.username || 'Admin'}</span>
              </div>
              <Button variant="outline" size="sm" onClick={handleSignOut} className="hover:bg-destructive/10 hover:text-destructive hover:border-destructive/30">
                <LogOut className="h-4 w-4 mr-2" />
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <Card className="card-hover border-primary/20 bg-gradient-to-br from-card via-card to-primary/5">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <Sparkles className="h-6 w-6 text-primary" />
                <div>
                  <CardTitle className="text-xl">Welcome Back!</CardTitle>
                  <CardDescription className="text-base">
                    Ready to update your portfolio? Everything you need is right here.
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
          </Card>
        </div>

        {/* Management Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {/* Projects Management */}
          <Card className="card-hover group cursor-pointer transition-all duration-300 hover:scale-105">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-500/20 rounded-lg group-hover:bg-blue-500/30 transition-colors">
                    <Code className="h-5 w-5 text-blue-400" />
                  </div>
                  <CardTitle className="text-lg">Projects</CardTitle>
                </div>
                <div className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full font-medium">
                  Coming Soon
                </div>
              </div>
              <CardDescription>
                Showcase your development work
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Add projects with repository links, live demos, and detailed descriptions of your technical achievements.
              </p>
              <Button className="w-full" disabled variant="outline">
                <Code className="h-4 w-4 mr-2" />
                Manage Projects
              </Button>
            </CardContent>
          </Card>

          {/* Certifications Management */}
          <Card className="card-hover group cursor-pointer transition-all duration-300 hover:scale-105">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-green-500/20 rounded-lg group-hover:bg-green-500/30 transition-colors">
                    <Award className="h-5 w-5 text-green-400" />
                  </div>
                  <CardTitle className="text-lg">Certifications</CardTitle>
                </div>
                <div className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full font-medium">
                  Coming Soon
                </div>
              </div>
              <CardDescription>
                Display your professional credentials
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Add certifications with Credly verification links, expiry dates, and badge images.
              </p>
              <Button className="w-full" disabled variant="outline">
                <Award className="h-4 w-4 mr-2" />
                Manage Certifications
              </Button>
            </CardContent>
          </Card>

          {/* Skills Management */}
          <Card className="card-hover group cursor-pointer transition-all duration-300 hover:scale-105">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-purple-500/20 rounded-lg group-hover:bg-purple-500/30 transition-colors">
                    <FileText className="h-5 w-5 text-purple-400" />
                  </div>
                  <CardTitle className="text-lg">Skills</CardTitle>
                </div>
                <div className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full font-medium">
                  Coming Soon
                </div>
              </div>
              <CardDescription>
                Organize your technical expertise
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Categorize skills by proficiency level and add evidence links to demonstrate expertise.
              </p>
              <Button className="w-full" disabled variant="outline">
                <FileText className="h-4 w-4 mr-2" />
                Manage Skills
              </Button>
            </CardContent>
          </Card>

          {/* Site Configuration - Active */}
          <Card className="card-hover group cursor-pointer transition-all duration-300 hover:scale-105 border-primary/30 bg-gradient-to-br from-card to-primary/5">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-primary/30 rounded-lg group-hover:bg-primary/40 transition-colors glow-primary">
                    <Settings className="h-5 w-5 text-primary" />
                  </div>
                  <CardTitle className="text-lg">Site Configuration</CardTitle>
                </div>
                <div className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full font-medium pulse-dot">
                  Active
                </div>
              </div>
              <CardDescription>
                Configure social links and branding
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Update your social media links, personal branding, and site-wide settings.
              </p>
              <Button 
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" 
                onClick={() => navigate('/admin/site-config')}
              >
                <Settings className="h-4 w-4 mr-2" />
                Configure Site
              </Button>
            </CardContent>
          </Card>

          {/* Analytics - Active */}
          <Card className="card-hover group cursor-pointer transition-all duration-300 hover:scale-105 border-primary/30 bg-gradient-to-br from-card to-primary/5">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-primary/30 rounded-lg group-hover:bg-primary/40 transition-colors glow-primary">
                    <BarChart3 className="h-5 w-5 text-primary" />
                  </div>
                  <CardTitle className="text-lg">Analytics</CardTitle>
                </div>
                <div className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full font-medium pulse-dot">
                  Active
                </div>
              </div>
              <CardDescription>
                Track visitor engagement
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Monitor page views, popular sections, and visitor engagement metrics.
              </p>
              <Button 
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground" 
                onClick={() => navigate('/admin/analytics')}
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                View Analytics
              </Button>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card className="card-hover border-border/50 bg-gradient-to-br from-card via-card to-muted/20">
            <CardHeader className="pb-3">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-muted/50 rounded-lg">
                  <Database className="h-5 w-5 text-muted-foreground" />
                </div>
                <CardTitle className="text-lg">Portfolio Stats</CardTitle>
              </div>
              <CardDescription>
                Content overview
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between items-center p-2 bg-muted/30 rounded-lg">
                  <span className="text-sm text-muted-foreground">Projects</span>
                  <span className="font-semibold text-primary">-</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-muted/30 rounded-lg">
                  <span className="text-sm text-muted-foreground">Certifications</span>
                  <span className="font-semibold text-primary">-</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-muted/30 rounded-lg">
                  <span className="text-sm text-muted-foreground">Skills</span>
                  <span className="font-semibold text-primary">-</span>
                </div>
                <div className="flex justify-between items-center p-2 bg-muted/30 rounded-lg">
                  <span className="text-sm text-muted-foreground">Page Views</span>
                  <span className="font-semibold text-primary">-</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Information Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Getting Started */}
          <Card className="card-hover">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <Globe className="h-5 w-5 text-primary" />
                <CardTitle>Getting Started</CardTitle>
              </div>
              <CardDescription>
                Quick guide to managing your portfolio
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 text-sm text-muted-foreground">
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary/20 rounded-full flex items-center justify-center text-xs font-bold text-primary mt-0.5">1</div>
                  <p>Start with <strong className="text-foreground">Site Configuration</strong> to set up your social links and branding</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-primary/20 rounded-full flex items-center justify-center text-xs font-bold text-primary mt-0.5">2</div>
                  <p>Check <strong className="text-foreground">Analytics</strong> to see how visitors interact with your site</p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="w-6 h-6 bg-muted/50 rounded-full flex items-center justify-center text-xs font-bold text-muted-foreground mt-0.5">3</div>
                  <p>Content management features (Projects, Skills, Certifications) are coming soon!</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* System Status */}
          <Card className="card-hover">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <div className="w-2 h-2 bg-green-400 rounded-full pulse-dot"></div>
                <CardTitle>System Status</CardTitle>
              </div>
              <CardDescription>
                All systems operational
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">API Gateway</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                    <span className="text-sm font-medium text-green-400">Online</span>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Database</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                    <span className="text-sm font-medium text-green-400">Connected</span>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Authentication</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                    <span className="text-sm font-medium text-green-400">Active</span>
                  </div>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">CDN</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                    <span className="text-sm font-medium text-green-400">Deployed</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};