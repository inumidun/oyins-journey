import { Activity, Clock, AlertCircle, Gauge, Server, RefreshCw } from 'lucide-react';

const HealthDashboard = () => {
  const systemHealth = {
    status: 'healthy',
    uptime: '99.97%',
    lastDeployment: new Date().toISOString(),
    apiLatency: '45ms',
    errorRate: '0.02%',
    version: 'v1.0.0',
  };

  const metrics = [
    {
      icon: Activity,
      label: 'Status',
      value: systemHealth.status,
      status: 'success' as const,
    },
    {
      icon: Gauge,
      label: 'Uptime',
      value: systemHealth.uptime,
      status: 'success' as const,
    },
    {
      icon: Clock,
      label: 'API Latency',
      value: systemHealth.apiLatency,
      status: 'success' as const,
    },
    {
      icon: AlertCircle,
      label: 'Error Rate',
      value: systemHealth.errorRate,
      status: 'success' as const,
    },
  ];

  const statusColors = {
    success: 'text-success',
    warning: 'text-warning',
    error: 'text-destructive',
  };

  return (
    <section className="py-24 bg-secondary/20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-mono mb-4">
            /health
          </span>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            System <span className="gradient-text">Observability</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            My CV exposes its own health. This demonstrates operability, not just buildability.
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Main status card */}
          <div className="bg-card border border-border rounded-xl p-6 mb-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-success/10 flex items-center justify-center">
                  <Server className="w-6 h-6 text-success" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">System Health</h3>
                  <p className="text-sm text-muted-foreground">All systems operational</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-success pulse-dot" />
                <span className="font-mono text-sm text-success uppercase">{systemHealth.status}</span>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {metrics.map((metric) => (
                <div key={metric.label} className="p-4 bg-secondary/50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <metric.icon className={`w-4 h-4 ${statusColors[metric.status]}`} />
                    <span className="text-xs text-muted-foreground">{metric.label}</span>
                  </div>
                  <p className={`text-xl font-mono font-bold ${statusColors[metric.status]}`}>
                    {metric.value}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Deployment info */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-card border border-border rounded-lg p-5">
              <div className="flex items-center gap-3 mb-4">
                <RefreshCw className="w-5 h-5 text-primary" />
                <h3 className="font-semibold text-foreground">Last Deployment</h3>
              </div>
              <p className="font-mono text-sm text-muted-foreground mb-2">
                {new Date(systemHealth.lastDeployment).toLocaleString()}
              </p>
              <div className="flex items-center gap-2">
                <span className="px-2 py-1 rounded text-xs bg-primary/10 text-primary font-mono">
                  {systemHealth.version}
                </span>
                <span className="text-xs text-muted-foreground">via GitHub Actions</span>
              </div>
            </div>

            <div className="bg-card border border-border rounded-lg p-5">
              <div className="flex items-center gap-3 mb-4">
                <Activity className="w-5 h-5 text-primary" />
                <h3 className="font-semibold text-foreground">Infrastructure</h3>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Compute</span>
                  <span className="font-mono text-foreground">AWS Lambda</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Database</span>
                  <span className="font-mono text-foreground">DynamoDB</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">CDN</span>
                  <span className="font-mono text-foreground">CloudFront</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HealthDashboard;