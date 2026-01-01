import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSiteConfig } from '@/hooks/useSiteConfig';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { ArrowLeft, Save, Loader2, ExternalLink, CheckCircle } from 'lucide-react';

interface FormData {
  socialLinks: {
    linkedin?: string;
    github?: string;
    email?: string;
    twitter?: string;
    website?: string;
  };
  branding: {
    name: string;
    tagline: string;
  };
  sourceRepoUrl: string;
  liveApiUrl: string;
}

export const AdminSiteConfig: React.FC = () => {
  const navigate = useNavigate();
  const { config, loading, updateConfig } = useSiteConfig();
  const [formData, setFormData] = useState<FormData>({
    socialLinks: {},
    branding: { name: '', tagline: '' },
    sourceRepoUrl: '',
    liveApiUrl: ''
  });
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (config) {
      setFormData({
        socialLinks: config.socialLinks || {},
        branding: config.branding || { name: '', tagline: '' },
        sourceRepoUrl: config.sourceRepoUrl || '',
        liveApiUrl: config.liveApiUrl || ''
      });
    }
  }, [config]);

  const validateUrl = (url: string): boolean => {
    if (!url) return true; // Empty URLs are valid (optional)
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSocialLinkChange = (platform: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      socialLinks: {
        ...prev.socialLinks,
        [platform]: value || undefined
      }
    }));
  };

  const handleBrandingChange = (field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      branding: {
        ...prev.branding,
        [field]: value
      }
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSaveSuccess(false);

    // Validate URLs
    const urlFields = [
      { name: 'LinkedIn', value: formData.socialLinks.linkedin },
      { name: 'GitHub', value: formData.socialLinks.github },
      { name: 'Twitter', value: formData.socialLinks.twitter },
      { name: 'Website', value: formData.socialLinks.website },
      { name: 'Source Repository', value: formData.sourceRepoUrl },
      { name: 'Live API', value: formData.liveApiUrl }
    ];

    for (const field of urlFields) {
      if (field.value && !validateUrl(field.value)) {
        setError(`Invalid URL format for ${field.name}`);
        return;
      }
    }

    // Validate email
    if (formData.socialLinks.email && !formData.socialLinks.email.includes('@')) {
      setError('Invalid email format');
      return;
    }

    setIsSaving(true);

    try {
      await updateConfig(formData);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err: any) {
      setError(err.message || 'Failed to save configuration');
    } finally {
      setIsSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-muted-foreground">Loading configuration...</p>
        </div>
      </div>
    );
  }

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
              <h1 className="text-2xl font-bold">Site Configuration</h1>
              <p className="text-muted-foreground">Manage your portfolio settings</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Social Links */}
          <Card>
            <CardHeader>
              <CardTitle>Social Links</CardTitle>
              <CardDescription>
                Configure your social media profiles. Leave empty to hide from the site.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="linkedin">LinkedIn Profile</Label>
                  <Input
                    id="linkedin"
                    type="url"
                    placeholder="https://linkedin.com/in/your-profile"
                    value={formData.socialLinks.linkedin || ''}
                    onChange={(e) => handleSocialLinkChange('linkedin', e.target.value)}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="github">GitHub Profile</Label>
                  <Input
                    id="github"
                    type="url"
                    placeholder="https://github.com/your-username"
                    value={formData.socialLinks.github || ''}
                    onChange={(e) => handleSocialLinkChange('github', e.target.value)}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="email">Email Address</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="your.email@example.com"
                    value={formData.socialLinks.email || ''}
                    onChange={(e) => handleSocialLinkChange('email', e.target.value)}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="twitter">Twitter Profile</Label>
                  <Input
                    id="twitter"
                    type="url"
                    placeholder="https://twitter.com/your-handle"
                    value={formData.socialLinks.twitter || ''}
                    onChange={(e) => handleSocialLinkChange('twitter', e.target.value)}
                  />
                </div>
                
                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="website">Personal Website</Label>
                  <Input
                    id="website"
                    type="url"
                    placeholder="https://your-website.com"
                    value={formData.socialLinks.website || ''}
                    onChange={(e) => handleSocialLinkChange('website', e.target.value)}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Branding */}
          <Card>
            <CardHeader>
              <CardTitle>Branding</CardTitle>
              <CardDescription>
                Configure your personal branding and tagline.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Display Name</Label>
                  <Input
                    id="name"
                    type="text"
                    placeholder="Your Name"
                    value={formData.branding.name}
                    onChange={(e) => handleBrandingChange('name', e.target.value)}
                    required
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="tagline">Professional Tagline</Label>
                  <Input
                    id="tagline"
                    type="text"
                    placeholder="Cloud Engineer & Solutions Architect"
                    value={formData.branding.tagline}
                    onChange={(e) => handleBrandingChange('tagline', e.target.value)}
                    required
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Site URLs */}
          <Card>
            <CardHeader>
              <CardTitle>Site URLs</CardTitle>
              <CardDescription>
                Configure the source repository and API documentation links.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="sourceRepo">Source Repository URL</Label>
                  <div className="flex space-x-2">
                    <Input
                      id="sourceRepo"
                      type="url"
                      placeholder="https://github.com/your-username/your-repo"
                      value={formData.sourceRepoUrl}
                      onChange={(e) => setFormData(prev => ({ ...prev, sourceRepoUrl: e.target.value }))}
                      required
                    />
                    {formData.sourceRepoUrl && (
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => window.open(formData.sourceRepoUrl, '_blank')}
                      >
                        <ExternalLink className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="liveApi">Live API URL</Label>
                  <div className="flex space-x-2">
                    <Input
                      id="liveApi"
                      type="url"
                      placeholder="https://api.your-domain.com"
                      value={formData.liveApiUrl}
                      onChange={(e) => setFormData(prev => ({ ...prev, liveApiUrl: e.target.value }))}
                      required
                    />
                    {formData.liveApiUrl && (
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => window.open(formData.liveApiUrl, '_blank')}
                      >
                        <ExternalLink className="h-4 w-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Error/Success Messages */}
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {saveSuccess && (
            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertDescription>Configuration saved successfully!</AlertDescription>
            </Alert>
          )}

          {/* Save Button */}
          <div className="flex justify-end">
            <Button type="submit" disabled={isSaving}>
              {isSaving ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="mr-2 h-4 w-4" />
                  Save Configuration
                </>
              )}
            </Button>
          </div>
        </form>
      </main>
    </div>
  );
};