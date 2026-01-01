import { useState } from 'react';
import { Play, Copy, Check, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import api from '@/services/api';

interface APIEndpoint {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  description: string;
  params: string[];
}

const apiEndpoints: APIEndpoint[] = [
  { method: 'GET', path: '/skills', description: 'List all skills with optional filtering', params: ['category', 'cloud'] },
  { method: 'GET', path: '/projects', description: 'List all projects', params: ['status', 'technology'] },
  { method: 'GET', path: '/certifications', description: 'List all certifications', params: ['provider', 'status'] },
  { method: 'GET', path: '/adrs', description: 'List all architectural decision records', params: [] },
  { method: 'GET', path: '/health', description: 'System health status', params: [] },
];

const APIExplorer = () => {
  const [selectedEndpoint, setSelectedEndpoint] = useState<APIEndpoint>(apiEndpoints[0]);
  const [copied, setCopied] = useState(false);
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [statusCode, setStatusCode] = useState<number | null>(null);
  const [parameters, setParameters] = useState<Record<string, string>>({});

  const handleTryIt = async () => {
    try {
      setLoading(true);
      setError(null);
      setStatusCode(null);
      
      // Build query string from parameters
      const queryParams = new URLSearchParams();
      Object.entries(parameters).forEach(([key, value]) => {
        if (value.trim()) {
          queryParams.append(key, value);
        }
      });
      
      const pathWithParams = queryParams.toString() 
        ? `${selectedEndpoint.path}?${queryParams.toString()}`
        : selectedEndpoint.path;
      
      const apiResponse = await api.get(pathWithParams);
      setResponse(JSON.stringify(apiResponse.data, null, 2));
      setStatusCode(200);
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'Failed to fetch data';
      const errorStatus = err.response?.status || 500;
      
      setError(errorMessage);
      setStatusCode(errorStatus);
      setResponse(JSON.stringify({ 
        error: errorMessage,
        status: errorStatus,
        timestamp: new Date().toISOString()
      }, null, 2));
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    const apiUrl = import.meta.env.VITE_API_URL || 'https://api.oyins-journey.dev';
    const queryParams = new URLSearchParams();
    Object.entries(parameters).forEach(([key, value]) => {
      if (value.trim()) {
        queryParams.append(key, value);
      }
    });
    
    const pathWithParams = queryParams.toString() 
      ? `${selectedEndpoint.path}?${queryParams.toString()}`
      : selectedEndpoint.path;
    
    navigator.clipboard.writeText(`curl -X ${selectedEndpoint.method} ${apiUrl}${pathWithParams}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleParameterChange = (param: string, value: string) => {
    setParameters(prev => ({
      ...prev,
      [param]: value
    }));
  };

  const handleEndpointSelect = (endpoint: APIEndpoint) => {
    setSelectedEndpoint(endpoint);
    setResponse(null);
    setError(null);
    setStatusCode(null);
    setParameters({});
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

  const getStatusColor = (status: number) => {
    if (status >= 200 && status < 300) return 'text-success';
    if (status >= 400 && status < 500) return 'text-warning';
    if (status >= 500) return 'text-destructive';
    return 'text-muted-foreground';
  };

  return (
    <section id="api" className="py-24 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-mono mb-4">
            /api/v1
          </span>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            My CV as an <span className="gradient-text">API</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            My skills, projects, and certifications are exposed via RESTful endpoints. 
            Query my experience programmatically.
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
                  onClick={() => handleEndpointSelect(endpoint)}
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
                  {Object.keys(parameters).some(key => parameters[key].trim()) && (
                    <span className="text-muted-foreground">
                      ?{Object.entries(parameters)
                        .filter(([, value]) => value.trim())
                        .map(([key, value]) => `${key}=${value}`)
                        .join('&')}
                    </span>
                  )}
                </div>
                <div className="mt-3">
                  <p className="text-muted-foreground text-sm">
                    {selectedEndpoint.description}
                  </p>
                  <div className="mt-2 text-xs text-muted-foreground">
                    <span className="font-semibold">Documentation:</span> This endpoint provides {selectedEndpoint.description.toLowerCase()}
                  </div>
                </div>
                {selectedEndpoint.params.length > 0 ? (
                  <div className="mt-4">
                    <p className="text-xs text-muted-foreground mb-2">Query Parameters:</p>
                    <div className="space-y-2">
                      {selectedEndpoint.params.map((param) => (
                        <div key={param} className="flex items-center gap-2">
                          <span className="px-2 py-1 rounded bg-secondary text-xs font-mono text-primary min-w-[80px]">
                            {param}
                          </span>
                          <input
                            type="text"
                            placeholder={`Enter ${param} value`}
                            value={parameters[param] || ''}
                            onChange={(e) => handleParameterChange(param, e.target.value)}
                            className="flex-1 px-2 py-1 text-xs bg-background border border-border rounded focus:outline-none focus:ring-1 focus:ring-primary"
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="mt-4">
                    <p className="text-xs text-muted-foreground">No parameters required</p>
                  </div>
                )}
              </div>
            </div>

            {/* Response */}
            <div className="bg-card border border-border rounded-lg overflow-hidden">
              <div className="flex items-center justify-between p-4 border-b border-border bg-secondary/50">
                <h3 className="font-mono text-sm text-muted-foreground">Response</h3>
                {statusCode && (
                  <span className={`text-xs font-mono ${getStatusColor(statusCode)}`}>
                    {statusCode} {statusCode === 200 ? 'OK' : error ? 'Error' : 'Unknown'}
                  </span>
                )}
              </div>
              <div className="p-4 font-mono text-sm max-h-[300px] overflow-y-auto">
                {loading ? (
                  <div>
                    <p className="text-muted-foreground">Making request...</p>
                    <p className="text-xs text-muted-foreground mt-1">Request data will appear here</p>
                  </div>
                ) : error ? (
                  <div role="alert">
                    <p className="text-destructive mb-2">Error: {error}</p>
                    <pre className="text-foreground whitespace-pre-wrap">{response}</pre>
                    <p className="text-xs text-muted-foreground mt-2">Response data shows error details</p>
                  </div>
                ) : response ? (
                  <div>
                    <pre className="text-foreground whitespace-pre-wrap">{response}</pre>
                    <p className="text-xs text-muted-foreground mt-2">Response data received successfully</p>
                  </div>
                ) : (
                  <div>
                    <p className="text-muted-foreground">Click "Try it" to see the response</p>
                    <p className="text-xs text-muted-foreground mt-1">Request and response data will appear here</p>
                  </div>
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