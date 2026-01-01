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
  User
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
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Settings className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">Admin Portal</h1>
              <p className="text-muted-foreground">Manage your portfolio content</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm">
              <User className="h-4 w-4" />
              <span>{user?.username || 'Admin'}</span>
            </div>
            <Button variant="outline" size="sm" onClick={handleSignOut}>
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Projects Management */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <div className="flex items-center space-x-2">
                <Code className="h-5 w-5 text-primary" />
                <CardTitle>Projects</CardTitle>
              </div>
              <CardDescription>
                Manage your project portfolio
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Add, edit, and organize your projects with repository links and live demos.
              </p>
              <Button className="w-full" disabled>
                Manage Projects
                <span className="ml-2 text-xs">(Coming Soon)</span>
              </Button>
            </CardContent>
          </Card>

          {/* Certifications Management */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <div className="flex items-center space-x-2">
                <Award className="h-5 w-5 text-primary" />
                <CardTitle>Certifications</CardTitle>
              </div>
              <CardDescription>
                Manage your professional certifications
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Add certifications with Credly verification links and badge images.
              </p>
              <Button className="w-full" disabled>
                Manage Certifications
                <span className="ml-2 text-xs">(Coming Soon)</span>
              </Button>
            </CardContent>
          </Card>

          {/* Skills Management */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <div className="flex items-center space-x-2">
                <FileText className="h-5 w-5 text-primary" />
                <CardTitle>Skills</CardTitle>
              </div>
              <CardDescription>
                Manage your technical skills
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Organize your skills by category and proficiency level.
              </p>
              <Button className="w-full" disabled>
                Manage Skills
                <span className="ml-2 text-xs">(Coming Soon)</span>
              </Button>
            </CardContent>
          </Card>

          {/* Site Configuration */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <div className="flex items-center space-x-2">
                <Settings className="h-5 w-5 text-primary" />
                <CardTitle>Site Configuration</CardTitle>
              </div>
              <CardDescription>
                Configure social links and branding
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Update your social media links, branding, and site settings.
              </p>
              <Button 
                className="w-full" 
                onClick={() => navigate('/admin/site-config')}
              >
                Configure Site
              </Button>
            </CardContent>
          </Card>

          {/* Analytics */}
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <div className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-primary" />
                <CardTitle>Analytics</CardTitle>
              </div>
              <CardDescription>
                View visitor statistics
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                Track page views, popular sections, and visitor engagement.
              </p>
              <Button 
                className="w-full" 
                onClick={() => navigate('/admin/analytics')}
              >
                View Analytics
              </Button>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card className="md:col-span-2 lg:col-span-1">
            <CardHeader>
              <CardTitle>Quick Stats</CardTitle>
              <CardDescription>
                Portfolio overview
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Projects</span>
                  <span className="font-semibold">-</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Certifications</span>
                  <span className="font-semibold">-</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Skills</span>
                  <span className="font-semibold">-</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-muted-foreground">Page Views</span>
                  <span className="font-semibold">-</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Welcome Message */}
        <div className="mt-8">
          <Card>
            <CardHeader>
              <CardTitle>Welcome to Your Admin Portal</CardTitle>
              <CardDescription>
                This is your central hub for managing all portfolio content
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="prose prose-sm max-w-none text-muted-foreground">
                <p>
                  From here, you can manage all aspects of your portfolio website:
                </p>
                <ul className="list-disc list-inside space-y-1 mt-2">
                  <li>Add and update your projects with repository and demo links</li>
                  <li>Manage your professional certifications with Credly verification</li>
                  <li>Organize your technical skills by category and proficiency</li>
                  <li>Configure social media links and site branding</li>
                  <li>View visitor analytics and engagement metrics</li>
                </ul>
                <p className="mt-4">
                  Content management features are currently being developed and will be available soon.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};