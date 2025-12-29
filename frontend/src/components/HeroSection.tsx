import { useState, useEffect } from 'react';
import { ArrowDown, Terminal, Zap, GitBranch, Database } from 'lucide-react';
import { Button } from '@/components/ui/button';

const HeroSection = () => {
  const [typedText, setTypedText] = useState('');
  const fullText = 'GET /cv/skills?cloud=aws';

  useEffect(() => {
    let index = 0;
    const timer = setInterval(() => {
      if (index <= fullText.length) {
        setTypedText(fullText.slice(0, index));
        index++;
      } else {
        clearInterval(timer);
      }
    }, 80);
    return () => clearInterval(timer);
  }, []);

  return (
    <section className="min-h-screen flex items-center justify-center relative overflow-hidden pt-16">
      {/* Background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,hsl(var(--border))_1px,transparent_1px),linear-gradient(to_bottom,hsl(var(--border))_1px,transparent_1px)] bg-[size:4rem_4rem] opacity-20" />
      
      {/* Gradient orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-float" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-info/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '1s' }} />

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          {/* Status badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-secondary border border-border mb-8 slide-up">
            <div className="w-2 h-2 rounded-full bg-success pulse-dot" />
            <span className="text-sm font-mono text-muted-foreground">
              System Online • Latency 45ms
            </span>
          </div>

          {/* Main headline */}
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 slide-up" style={{ animationDelay: '0.1s' }}>
            <span className="text-foreground">Oyin's</span>{' '}
            <span className="gradient-text">Journey</span>
            <br />
            <span className="text-foreground">CV System</span>
          </h1>

          {/* Tagline */}
          <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto slide-up" style={{ animationDelay: '0.2s' }}>
            My CV isn't a PDF. It's a{' '}
            <span className="text-primary font-semibold">deployed cloud system</span>{' '}
            that proves my skills by existing.
          </p>

          {/* Terminal mockup */}
          <div className="max-w-xl mx-auto mb-10 slide-up" style={{ animationDelay: '0.3s' }}>
            <div className="bg-card border border-border rounded-lg overflow-hidden shadow-2xl">
              <div className="flex items-center gap-2 px-4 py-3 bg-secondary border-b border-border">
                <div className="w-3 h-3 rounded-full bg-destructive/80" />
                <div className="w-3 h-3 rounded-full bg-warning" />
                <div className="w-3 h-3 rounded-full bg-success" />
                <span className="ml-2 text-xs font-mono text-muted-foreground">api.oyins-journey.dev</span>
              </div>
              <div className="p-4 font-mono text-sm">
                <div className="flex items-center gap-2 text-muted-foreground">
                  <span className="text-primary">$</span>
                  <span className="text-foreground">{typedText}</span>
                  <span className="terminal-cursor text-primary">▋</span>
                </div>
              </div>
            </div>
          </div>

          {/* CTA buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12 slide-up" style={{ animationDelay: '0.4s' }}>
            <Button variant="glow" size="xl" className="font-mono">
              <Terminal className="w-5 h-5 mr-2" />
              Explore API
            </Button>
            <Button variant="outline" size="xl">
              View Source Code
            </Button>
          </div>

          {/* Feature pills */}
          <div className="flex flex-wrap items-center justify-center gap-3 slide-up" style={{ animationDelay: '0.5s' }}>
            {[
              { icon: Database, label: 'Queryable Skills' },
              { icon: GitBranch, label: 'Versioned History' },
              { icon: Zap, label: 'Live Endpoints' },
              { icon: Terminal, label: '100% IaC' },
            ].map((feature) => (
              <div
                key={feature.label}
                className="flex items-center gap-2 px-4 py-2 rounded-full bg-secondary/50 border border-border text-sm text-muted-foreground"
              >
                <feature.icon className="w-4 h-4 text-primary" />
                {feature.label}
              </div>
            ))}
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-muted-foreground animate-bounce">
          <span className="text-xs font-mono">scroll to explore</span>
          <ArrowDown className="w-4 h-4" />
        </div>
      </div>
    </section>
  );
};

export default HeroSection;