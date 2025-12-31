import { useState, useEffect } from 'react';
import { Search, Filter, ExternalLink, Award, Calendar, AlertTriangle, CheckCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { certificationsApi, Certification } from '@/services/api';

const providerColors: Record<string, string> = {
  AWS: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  Azure: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  GCP: 'bg-green-500/20 text-green-400 border-green-500/30',
  Other: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
};

const statusColors: Record<string, string> = {
  active: 'bg-green-500/20 text-green-400 border-green-500/30',
  expired: 'bg-red-500/20 text-red-400 border-red-500/30',
  expiring_soon: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  no_expiry: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
};

const statusIcons: Record<string, React.ElementType> = {
  active: CheckCircle,
  expired: AlertTriangle,
  expiring_soon: AlertTriangle,
  no_expiry: Award,
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
    switch (status) {
      case 'active': return 'Active';
      case 'expired': return 'Expired';
      case 'expiring_soon': return 'Expiring Soon';
      case 'no_expiry': return 'No Expiry';
      default: return status;
    }
  };

  if (loading) {
    return (
      <section id="certifications" className="py-24 bg-secondary/20">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-center">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
            <span className="ml-2 text-muted-foreground">Loading certifications...</span>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="certifications" className="py-24 bg-secondary/20">
        <div className="container mx-auto px-4">
          <div className="text-center text-destructive">
            <p>Error: {error}</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="certifications" className="py-24 bg-secondary/20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-mono mb-4">
            /certifications
          </span>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Verified <span className="gradient-text">Certifications</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Professional certifications with verification links and expiry tracking. Every credential is verifiable and up-to-date.
          </p>
        </div>

        {/* Query Builder */}
        <div className="max-w-4xl mx-auto mb-12">
          <div className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-4 font-mono text-sm text-muted-foreground">
              <Filter className="w-4 h-4 text-primary" />
              <span>Query Builder</span>
            </div>
            
            <div className="grid md:grid-cols-3 gap-4">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search certifications..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:border-primary transition-colors"
                />
              </div>

              {/* Provider filter */}
              <select
                value={providerFilter}
                onChange={(e) => setProviderFilter(e.target.value)}
                className="px-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:border-primary transition-colors"
              >
                {providers.map((provider) => (
                  <option key={provider} value={provider}>
                    {provider === 'all' ? 'All Providers' : provider}
                  </option>
                ))}
              </select>

              {/* Status filter */}
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:border-primary transition-colors"
              >
                {statuses.map((status) => (
                  <option key={status} value={status}>
                    {status === 'all' ? 'All Statuses' : getStatusText(status)}
                  </option>
                ))}
              </select>
            </div>

            {/* Generated query */}
            <div className="mt-4 p-3 bg-background rounded-md font-mono text-xs">
              <span className="text-success">GET</span>
              <span className="text-muted-foreground"> /certifications</span>
              <span className="text-primary">
                ?provider={providerFilter}
                &status={statusFilter}
                {searchQuery && `&search=${searchQuery}`}
              </span>
            </div>
          </div>
        </div>

        {/* Results count */}
        <div className="max-w-4xl mx-auto mb-6">
          <p className="text-sm text-muted-foreground font-mono">
            Found <span className="text-primary">{filteredCertifications.length}</span> certifications matching your query
          </p>
        </div>

        {/* Certifications grid */}
        <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-6">
          {filteredCertifications.map((cert, index) => {
            const StatusIcon = statusIcons[cert.computed_status || 'active'];
            return (
              <div
                key={cert.id}
                className="bg-card border border-border rounded-lg p-6 card-hover group slide-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-md border ${providerColors[cert.provider] || providerColors.Other}`}>
                      <Award className="w-4 h-4" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground">{cert.name}</h3>
                      <p className="text-sm text-muted-foreground">{cert.provider}</p>
                    </div>
                  </div>
                  <Button variant="ghost" size="icon" className="w-6 h-6 opacity-0 group-hover:opacity-100 transition-opacity">
                    <ExternalLink className="w-3 h-3" />
                  </Button>
                </div>

                {/* Status indicator */}
                <div className="flex items-center gap-2 mb-4">
                  <div className={`flex items-center gap-1 px-2 py-1 rounded text-xs border ${statusColors[cert.computed_status || 'active']}`}>
                    <StatusIcon className="w-3 h-3" />
                    <span>{getStatusText(cert.computed_status || 'active')}</span>
                  </div>
                </div>

                {/* Dates */}
                <div className="space-y-2 mb-4">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      Issued
                    </span>
                    <span className="font-mono text-primary">{formatDate(cert.issue_date)}</span>
                  </div>
                  {cert.expiry_date && (
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground flex items-center gap-1">
                        <Calendar className="w-3 h-3" />
                        Expires
                      </span>
                      <span className="font-mono text-primary">{formatDate(cert.expiry_date)}</span>
                    </div>
                  )}
                </div>

                {/* Credential ID */}
                {cert.credential_id && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Credential ID</span>
                      <span className="font-mono text-xs text-primary bg-primary/10 px-2 py-1 rounded">
                        {cert.credential_id}
                      </span>
                    </div>
                  </div>
                )}

                {/* Verification link */}
                <div className="pt-4 border-t border-border">
                  <Button variant="outline" size="sm" className="w-full font-mono text-xs" asChild>
                    <a href="#" target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="w-3 h-3 mr-1" />
                      Verify Credential
                    </a>
                  </Button>
                </div>
              </div>
            );
          })}
        </div>

        {filteredCertifications.length === 0 && !loading && (
          <div className="text-center py-12">
            <Award className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">No certifications found matching your criteria.</p>
          </div>
        )}
      </div>
    </section>
  );
};

export default CertificationsSection;