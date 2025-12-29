import { useState, useEffect } from 'react';
import { Terminal, Activity, Github, Linkedin, Mail } from 'lucide-react';
import { useSystemHealth } from '../hooks/useApi';

const Header = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const { data: health } = useSystemHealth();

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-gray-700 bg-gray-900/80 backdrop-blur-xl">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-primary-500">
            <Terminal className="w-5 h-5" />
            <span className="font-mono font-bold text-lg">LAR</span>
          </div>
          <div className="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full bg-gray-800 border border-gray-700">
            <div className={`w-2 h-2 rounded-full ${health?.status === 'online' ? 'bg-green-500 animate-pulse-glow' : 'bg-red-500'}`} />
            <span className="text-xs font-mono text-gray-400">
              {health?.status || 'checking'} • {health?.latency || 'N/A'}
            </span>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-6">
          <a href="#api" className="text-sm text-gray-400 hover:text-white transition-colors">API</a>
          <a href="#skills" className="text-sm text-gray-400 hover:text-white transition-colors">Skills</a>
          <a href="#projects" className="text-sm text-gray-400 hover:text-white transition-colors">Projects</a>
        </nav>

        <div className="flex items-center gap-3">
          <div className="hidden lg:flex items-center gap-2 text-xs font-mono text-gray-400">
            <Activity className="w-3 h-3 text-green-500" />
            <span>{currentTime.toLocaleTimeString()}</span>
          </div>
          <div className="flex items-center gap-1">
            <button className="w-8 h-8 flex items-center justify-center hover:bg-gray-800 rounded">
              <Github className="w-4 h-4" />
            </button>
            <button className="w-8 h-8 flex items-center justify-center hover:bg-gray-800 rounded">
              <Linkedin className="w-4 h-4" />
            </button>
            <button className="w-8 h-8 flex items-center justify-center hover:bg-gray-800 rounded">
              <Mail className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;