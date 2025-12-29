import { useState, useEffect } from 'react';
import { ArrowDown, Terminal, Zap, GitBranch, Database } from 'lucide-react';

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
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgb(55_65_81_/_0.3)_1px,transparent_1px),linear-gradient(to_bottom,rgb(55_65_81_/_0.3)_1px,transparent_1px)] bg-[size:4rem_4rem]" />
      
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gray-800 border border-gray-700 mb-8 animate-slide-up">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse-glow" />
            <span className="text-sm font-mono text-gray-400">System Online • Latency 45ms</span>
          </div>

          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 animate-slide-up">
            <span className="text-white">Living</span>{' '}
            <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Architecture</span>
            <br />
            <span className="text-white">Resume</span>
          </h1>

          <p className="text-xl md:text-2xl text-gray-400 mb-8 max-w-2xl mx-auto animate-slide-up">
            My CV isn't a PDF. It's a{' '}
            <span className="text-cyan-400 font-semibold">deployed cloud system</span>{' '}
            that proves my skills by existing.
          </p>

          <div className="max-w-xl mx-auto mb-10 animate-slide-up">
            <div className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden shadow-2xl">
              <div className="flex items-center gap-2 px-4 py-3 bg-gray-700 border-b border-gray-600">
                <div className="w-3 h-3 rounded-full bg-red-500" />
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <div className="w-3 h-3 rounded-full bg-green-500" />
                <span className="ml-2 text-xs font-mono text-gray-400">api.oyintech.dev</span>
              </div>
              <div className="p-4 font-mono text-sm">
                <div className="flex items-center gap-2 text-gray-400">
                  <span className="text-cyan-400">$</span>
                  <span className="text-white">{typedText}</span>
                  <span className="animate-pulse text-cyan-400">▋</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12 animate-slide-up">
            <button className="px-6 py-3 bg-cyan-500 hover:bg-cyan-400 text-black font-mono font-semibold rounded-lg shadow-[0_0_20px_rgba(6,182,212,0.3)] transition-all duration-300 flex items-center gap-2">
              <Terminal className="w-5 h-5" />
              Explore API
            </button>
            <button className="px-6 py-3 border border-gray-600 hover:border-gray-500 text-white rounded-lg transition-all duration-300">
              View Source Code
            </button>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3 animate-slide-up">
            {[
              { icon: Database, label: 'Queryable Skills' },
              { icon: GitBranch, label: 'Versioned History' },
              { icon: Zap, label: 'Live Endpoints' },
              { icon: Terminal, label: '100% IaC' },
            ].map((feature) => (
              <div
                key={feature.label}
                className="flex items-center gap-2 px-4 py-2 rounded-full bg-gray-800/50 border border-gray-700 text-sm text-gray-400"
              >
                <feature.icon className="w-4 h-4 text-cyan-400" />
                {feature.label}
              </div>
            ))}
          </div>
        </div>

        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-gray-400 animate-bounce">
          <span className="text-xs font-mono">scroll to explore</span>
          <ArrowDown className="w-4 h-4" />
        </div>
      </div>
    </section>
  );
};

export default HeroSection;