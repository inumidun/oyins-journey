import { useState } from 'react';
import { Play, Copy, Check, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import api from '@/services/api';

const apiEndpoints = [
  { method: 'GET', path: '/skills', description: 'List all skills with optional filtering', params: ['category', 'cloud'] },
  { method: 'GET', path: '/projects', description: 'List all projects', params: ['status', 'technology'] },
  { method: 'GET', path: '/certifications', description: 'List all certifications', params: ['provider', 'status'] },
];

const APIExplorer = () => {
  const [selectedEndpoint, setSelectedEndpoint] = useState(apiEndpoints[0]);
  const [copied, setCopied] = useState(false);
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTryIt = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const apiResponse = await api.get(selectedEndpoint.path);
      setResponse(JSON.stringify(apiResponse.data, null, 2));
    } catch (err: any) {
      setError(err.message || 'Failed to fetch data');
      setResponse(JSON.stringify({ error: err.message || 'Failed to fetch data' }, null, 2));
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    const apiUrl = import.meta.env.VITE_API_URL || 'https://api.oyins-journey.dev';
    navigator.clipboard.writeText(`curl -X ${selectedEndpoint.method} ${apiUrl}${selectedEndpoint.path}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getMethodColor = (method: string) => {
    switch (method) {
      case 'GET': return 'text-success';
      case 'POST': return 'text-warning';
      case 'PUT': return 'text-info';
      case 'DELETE': return 'text-destructive';
      default: return 'text-muted-foreground';
    }
  };

  return (
    <section id="api" className="py-24 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-mono mb-4">
            /api/v1
          </span>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Your CV as an <span className="gradient-text">API</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Every skill, project, and decision is exposed via RESTful endpoints. 
            Query my experience like you would any other service.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {/* Endpoints list */}
          <div className="bg-card border border-border rounded-lg overflow-hidden">
            <div className="p-4 border-b border-border bg-secondary/50">
              <h3 className="font-mono text-sm text-muted-foreground">Endpoints</h3>
            </div>
            <div className="divide-y divide-border max-h-[500px] overflow-y-auto">
              {apiEndpoints.map((endpoint) => (
                <button
                  key={endpoint.path}
                  onClick={() => {
                    setSelectedEndpoint(endpoint);
                    setResponse(null);
                    setError(null);
                  }}
                  className={`w-full p-4 text-left hover:bg-secondary/50 transition-colors flex items-center gap-3 ${
                    selectedEndpoint.path === endpoint.path ? 'bg-secondary' : ''
                  }`}
                >
                  <span className={`font-mono text-xs font-bold ${getMethodColor(endpoint.method)}`}>
                    {endpoint.method}
                  </span>
                  <span className="font-mono text-sm text-foreground truncate flex-1">
                    {endpoint.path}
                  </span>
                  <ChevronRight className="w-4 h-4 text-muted-foreground" />
                </button>
              ))}
            </div>
          </div>

          {/* Request/Response panel */}
          <div className="lg:col-span-2 space-y-4">
            {/* Request */}
            <div className="bg-card border border-border rounded-lg overflow-hidden">
              <div className="flex items-center justify-between p-4 border-b border-border bg-secondary/50">
                <h3 className="font-mono text-sm text-muted-foreground">Request</h3>
                <div className="flex items-center gap-2">
                  <Button variant="ghost" size="sm" onClick={handleCopy}>
                    {copied ? <Check className="w-4 h-4 text-success" /> : <Copy className="w-4 h-4" />}
                  </Button>
                  <Button variant="terminal" size="sm" onClick={handleTryIt} disabled={loading}>
                    <Play className="w-4 h-4 mr-1" />
                    {loading ? 'Loading...' : 'Try it'}
                  </Button>
                </div>
              </div>
              <div className="p-4 font-mono text-sm">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`font-bold ${getMethodColor(selectedEndpoint.method)}`}>
                    {selectedEndpoint.method}
                  </span>
                  <span className="text-muted-foreground">{import.meta.env.VITE_API_URL || 'https://api.oyins-journey.dev'}</span>
                  <span className="text-primary">{selectedEndpoint.path}</span>
                </div>
                <p className="mt-3 text-muted-foreground text-sm">
                  {selectedEndpoint.description}
                </p>
                {selectedEndpoint.params.length > 0 && (
                  <div className="mt-4">
                    <p className="text-xs text-muted-foreground mb-2">Query Parameters:</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedEndpoint.params.map((param) => (
                        <span
                          key={param}
                          className="px-2 py-1 rounded bg-secondary text-xs font-mono text-primary"
                        >
                          {param}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Response */}
            <div className="bg-card border border-border rounded-lg overflow-hidden">
              <div className="flex items-center justify-between p-4 border-b border-border bg-secondary/50">
                <h3 className="font-mono text-sm text-muted-foreground">Response</h3>
                {response && !error && (
                  <span className="text-xs font-mono text-success">200 OK</span>
                )}
                {error && (
                  <span className="text-xs font-mono text-destructive">Error</span>
                )}
              </div>
              <div className="p-4 font-mono text-sm max-h-[300px] overflow-y-auto">
                {loading ? (
                  <p className="text-muted-foreground">Making request...</p>
                ) : response ? (
                  <pre className="text-foreground whitespace-pre-wrap">{response}</pre>
                ) : (
                  <p className="text-muted-foreground">Click "Try it" to see the response</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default APIExplorer;