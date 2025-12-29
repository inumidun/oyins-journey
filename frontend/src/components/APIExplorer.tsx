import { useState } from 'react';
import { Play, Copy, Check, ChevronRight } from 'lucide-react';
import api from '../services/api';

interface Endpoint {
  method: string;
  path: string;
  description: string;
  params: string[];
}

const APIExplorer = () => {
  const [selectedEndpoint, setSelectedEndpoint] = useState<Endpoint>({
    method: 'GET',
    path: '/skills',
    description: 'Get all technical skills and expertise',
    params: ['category', 'cloud']
  });
  const [copied, setCopied] = useState(false);
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const endpoints: Endpoint[] = [
    { method: 'GET', path: '/skills', description: 'Get all technical skills and expertise', params: ['category', 'cloud'] },
    { method: 'GET', path: '/projects', description: 'List projects and experience', params: ['status', 'technology'] },
    { method: 'GET', path: '/certifications', description: 'View professional certifications', params: ['provider', 'status'] },
  ];

  const handleTryIt = async () => {
    setLoading(true);
    try {
      const result = await api.get(selectedEndpoint.path);
      setResponse(JSON.stringify(result.data, null, 2));
    } catch (error: any) {
      setResponse(JSON.stringify({ error: error.message }, null, 2));
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(`curl -X ${selectedEndpoint.method} ${api.defaults.baseURL}${selectedEndpoint.path}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getMethodColor = (method: string) => {
    switch (method) {
      case 'GET': return 'text-green-400';
      case 'POST': return 'text-yellow-400';
      case 'PUT': return 'text-blue-400';
      case 'DELETE': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <section id="api" className="py-24 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 text-sm font-mono mb-4">
            /api/v1
          </span>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Your CV as an <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">API</span>
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Every skill, project, and decision is exposed via RESTful endpoints. 
            Query my experience like you would any other service.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {/* Endpoints list */}
          <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
            <div className="p-4 border-b border-gray-700 bg-gray-700/50">
              <h3 className="font-mono text-sm text-gray-400">Endpoints</h3>
            </div>
            <div className="divide-y divide-gray-700 max-h-[500px] overflow-y-auto">
              {endpoints.map((endpoint) => (
                <button
                  key={endpoint.path}
                  onClick={() => {
                    setSelectedEndpoint(endpoint);
                    setResponse(null);
                  }}
                  className={`w-full p-4 text-left hover:bg-gray-700 transition-colors flex items-center gap-3 ${
                    selectedEndpoint.path === endpoint.path ? 'bg-gray-700' : ''
                  }`}
                >
                  <span className={`font-mono text-xs font-bold ${getMethodColor(endpoint.method)}`}>
                    {endpoint.method}
                  </span>
                  <span className="font-mono text-sm text-white truncate flex-1">
                    {endpoint.path}
                  </span>
                  <ChevronRight className="w-4 h-4 text-gray-400" />
                </button>
              ))}
            </div>
          </div>

          {/* Request/Response panel */}
          <div className="lg:col-span-2 space-y-4">
            {/* Request */}
            <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
              <div className="flex items-center justify-between p-4 border-b border-gray-700 bg-gray-700/50">
                <h3 className="font-mono text-sm text-gray-400">Request</h3>
                <div className="flex items-center gap-2">
                  <button onClick={handleCopy} className="p-2 hover:bg-gray-600 rounded">
                    {copied ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                  <button 
                    onClick={handleTryIt}
                    disabled={loading}
                    className="px-3 py-1 bg-cyan-500 hover:bg-cyan-400 text-black text-sm font-mono rounded flex items-center gap-1 disabled:opacity-50"
                  >
                    <Play className="w-4 h-4" />
                    {loading ? 'Testing...' : 'Try it'}
                  </button>
                </div>
              </div>
              <div className="p-4 font-mono text-sm">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className={`font-bold ${getMethodColor(selectedEndpoint.method)}`}>
                    {selectedEndpoint.method}
                  </span>
                  <span className="text-gray-400">{api.defaults.baseURL}</span>
                  <span className="text-cyan-400">{selectedEndpoint.path}</span>
                </div>
                <p className="mt-3 text-gray-400 text-sm">
                  {selectedEndpoint.description}
                </p>
                {selectedEndpoint.params.length > 0 && (
                  <div className="mt-4">
                    <p className="text-xs text-gray-400 mb-2">Query Parameters:</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedEndpoint.params.map((param) => (
                        <span
                          key={param}
                          className="px-2 py-1 rounded bg-gray-700 text-xs font-mono text-cyan-400"
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
            <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden">
              <div className="flex items-center justify-between p-4 border-b border-gray-700 bg-gray-700/50">
                <h3 className="font-mono text-sm text-gray-400">Response</h3>
                {response && (
                  <span className="text-xs font-mono text-green-400">200 OK</span>
                )}
              </div>
              <div className="p-4 font-mono text-sm max-h-[300px] overflow-y-auto">
                {loading ? (
                  <p className="text-gray-400">Loading...</p>
                ) : response ? (
                  <pre className="text-white whitespace-pre-wrap">{response}</pre>
                ) : (
                  <p className="text-gray-400">Click "Try it" to see the response</p>
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