import { useState, useEffect } from 'react';
import { Search, Filter, ExternalLink, Award, Calendar, AlertTriangle, CheckCircle, Loader2, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { certificationsApi, Certification } from '@/services/api';

const providerLogos: Record<string, string> = {
  AWS: '🟠',
  Azure: '🔵', 
  GCP: '🟢',
  Other: '🟣',
};

const providerColors: Record<string, string> = {
  AWS: 'from-orange-500/20 to-orange-600/10 border-orange-500/30',
  Azure: 'from-blue-500/20 to-blue-600/10 border-blue-500/30',
  GCP: 'from-green-500/20 to-green-600/10 border-green-500/30',
  Other: 'from-purple-500/20 to-purple-600/10 border-purple-500/30',
};

const statusConfig: Record<string, { color: string; icon: React.ElementType; label: string }> = {
  active: { color: 'text-green-400', icon: CheckCircle, label: 'Active' },
  expired: { color: 'text-red-400', icon: AlertTriangle, label: 'Expired' },
  expiring_soon: { color: 'text-yellow-400', icon: AlertTriangle, label: 'Expiring Soon' },
  no_expiry: { color: 'text-blue-400', icon: Award, label: 'No Expiry' },
};

const CertificationsSection = () => {
  const [certifications, setCertifications] = useState<Certification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [providerFilter, setProviderFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    const fetchCertifications = async () => {
      try {
        setLoading(true);
        const params: any = {};
        if (providerFilter !== 'all') params.provider = providerFilter;
        if (statusFilter !== 'all') params.status = statusFilter;
        
        const response = await certificationsApi.getAll(params);
        setCertifications(response.certifications || response || []);
      } catch (err) {
        setError('Failed to load certifications');
        console.error('Error fetching certifications:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCertifications();
  }, [providerFilter, statusFilter]);

  const filteredCertifications = certifications.filter((cert) => {
    const matchesSearch = cert.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSearch;
  });

  const providers = ['all', 'AWS', 'Azure', 'GCP', 'Other'];
  const statuses = ['all', 'active', 'expired', 'expiring_soon', 'no_expiry'];

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getStatusText = (status: string) => {
    return statusConfig[status]?.label || status;
  };

  if (loading) {
    return (
      <section id="certifications" className="py-24 bg-gradient-to-br from-background via-secondary/5 to-background">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-center min-h-[400px]">
            <div className="text-center">
              <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto mb-4" />
              <p className="text-muted-foreground font-mono">Loading certifications...</p>
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="certifications" className="py-24 bg-gradient-to-br from-background via-secondary/5 to-background">
        <div className="container mx-auto px-4">
          <div className="text-center min-h-[400px] flex items-center justify-center">
            <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-8">
              <AlertTriangle className="w-12 h-12 text-destructive mx-auto mb-4" />
              <p className="text-destructive font-mono">Error: {error}</p>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="certifications" className="py-24 bg-gradient-to-br from-background via-secondary/5 to-background relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-grid-white/[0.02] bg-[size:50px_50px]" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/5 rounded-full blur-3xl" />
      
      <div className="container mx-auto px-4 relative">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6">
            <Shield className="w-4 h-4 text-primary" />
            <span className="text-primary font-mono text-sm">/certifications</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Professional <span className="gradient-text">Certifications</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto leading-relaxed">
            Verified credentials from leading cloud providers. Each certification represents 
            hands-on expertise and commitment to continuous learning.
          </p>
        </div>

        {/* Interactive Filters */}
        <div className="max-w-4xl mx-auto mb-12">
          <div className="bg-card/50 backdrop-blur-sm border border-border/50 rounded-xl p-6 shadow-lg">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-primary/10">
                <Filter className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h3 className="font-semibold text-foreground">Filter Certifications</h3>
                <p className="text-sm text-muted-foreground">Find specific credentials by provider or status</p>
              </div>
            </div>
            
            <div className="grid md:grid-cols-3 gap-4">
              {/* Search */}
              <div className="relative group">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
                <input
                  type="text"
                  placeholder="Search certifications..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 bg-background/50 border border-border rounded-lg text-sm focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
                />
              </div>

              {/* Provider filter */}
              <select
                value={providerFilter}
                onChange={(e) => setProviderFilter(e.target.value)}
                className="px-4 py-3 bg-background/50 border border-border rounded-lg text-sm focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
              >
                <option value="all">All Providers</option>
                {providers.slice(1).map((provider) => (
                  <option key={provider} value={provider}>
                    {`${providerLogos[provider] || '🔹'} ${provider}`}
                  </option>
                ))}
              </select>

              {/* Status filter */}
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-3 bg-background/50 border border-border rounded-lg text-sm focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
              >
                <option value="all">All Statuses</option>
                {statuses.slice(1).map((status) => (
                  <option key={status} value={status}>
                    {getStatusText(status)}
                  </option>
                ))}
              </select>
            </div>

            {/* API Query Display */}
            <div className="mt-6 p-4 bg-background/80 rounded-lg border border-border/50">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-xs font-mono text-muted-foreground">LIVE API QUERY</span>
              </div>
              <div className="font-mono text-sm">
                <span className="text-green-400 font-semibold">GET</span>
                <span className="text-muted-foreground"> /api/v1</span>
                <span className="text-primary">/certifications</span>
                <span className="text-yellow-400">
                  ?provider={providerFilter}&status={statusFilter}
                  {searchQuery && `&search=${encodeURIComponent(searchQuery)}`}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Results Summary */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="flex items-center justify-between">
            <p className="text-muted-foreground font-mono text-sm">
              <span className="text-primary font-semibold">{filteredCertifications.length}</span> certifications matching your query
            </p>
            {filteredCertifications.length > 0 && (
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>All credentials verified</span>
              </div>
            )}
          </div>
        </div>

        {/* Certifications Grid */}
        <div className="max-w-6xl mx-auto">
          {filteredCertifications.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCertifications.map((cert, index) => {
                const status = statusConfig[cert.computed_status || 'active'];
                const StatusIcon = status.icon;
                const providerGradient = providerColors[cert.provider] || providerColors.Other;
                
                return (
                  <div
                    key={cert.id}
                    className="group relative bg-gradient-to-br from-card/80 to-card/40 backdrop-blur-sm border border-border/50 rounded-xl p-6 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:shadow-primary/10 slide-up"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    {/* Provider Badge */}
                    <div className={`absolute -top-3 -right-3 w-12 h-12 bg-gradient-to-br ${providerGradient} rounded-full border flex items-center justify-center text-lg font-bold shadow-lg`}>
                      {providerLogos[cert.provider] || '🔹'}
                    </div>

                    {/* Status Indicator */}
                    <div className="flex items-center justify-between mb-4">
                      <div className={`flex items-center gap-2 px-3 py-1 rounded-full bg-background/50 border ${status.color} border-current/20`}>
                        <StatusIcon className="w-3 h-3" />
                        <span className="text-xs font-medium">{status.label}</span>
                      </div>
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        className="w-8 h-8 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-primary/10"
                        asChild
                      >
                        <a href="#" target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="w-4 h-4" />
                        </a>
                      </Button>
                    </div>

                    {/* Certification Info */}
                    <div className="mb-4">
                      <h3 className="font-bold text-lg text-foreground mb-2 leading-tight">
                        {cert.name}
                      </h3>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <Shield className="w-4 h-4" />
                        <span className="font-medium">{cert.provider}</span>
                      </div>
                    </div>

                    {/* Dates */}
                    <div className="space-y-3 mb-4">
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Calendar className="w-4 h-4" />
                          <span>Issued</span>
                        </div>
                        <span className="font-mono text-primary bg-primary/10 px-2 py-1 rounded text-xs">
                          {formatDate(cert.issue_date)}
                        </span>
                      </div>
                      {cert.expiry_date && (
                        <div className="flex items-center justify-between text-sm">
                          <div className="flex items-center gap-2 text-muted-foreground">
                            <Calendar className="w-4 h-4" />
                            <span>Expires</span>
                          </div>
                          <span className="font-mono text-primary bg-primary/10 px-2 py-1 rounded text-xs">
                            {formatDate(cert.expiry_date)}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Credential ID */}
                    {cert.credential_id && (
                      <div className="mb-4 p-3 bg-background/50 rounded-lg border border-border/50">
                        <div className="flex items-center justify-between">
                          <span className="text-xs text-muted-foreground">Credential ID</span>
                          <span className="font-mono text-xs text-foreground bg-secondary/50 px-2 py-1 rounded">
                            {cert.credential_id}
                          </span>
                        </div>
                      </div>
                    )}

                    {/* Verification Button */}
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="w-full font-mono text-xs hover:bg-primary/10 hover:border-primary/50 transition-all group-hover:shadow-md" 
                      asChild
                    >
                      <a href="#" target="_blank" rel="noopener noreferrer">
                        <Shield className="w-3 h-3 mr-2" />
                        Verify Credential
                        <ExternalLink className="w-3 h-3 ml-2" />
                      </a>
                    </Button>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-16">
              <div className="bg-card/50 backdrop-blur-sm border border-border/50 rounded-xl p-12 max-w-md mx-auto">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Award className="w-8 h-8 text-primary" />
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">No certifications found matching your criteria.</h3>
                <p className="text-muted-foreground text-sm">
                  Try adjusting your filters or search terms to find the certifications you're looking for.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default CertificationsSection;