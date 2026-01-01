import { Terminal, Github, ExternalLink } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useSiteConfig } from '@/hooks/useSiteConfig';

const Header = () => {
  const { config } = useSiteConfig();
  
  // Use config or fallback to hardcoded values
  const sourceRepoUrl = config?.sourceRepoUrl || 'https://github.com/your-github-username/your-repo-name';
  const liveApiUrl = config?.liveApiUrl || 'https://api.your-domain.com';

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <Terminal className="w-6 h-6 text-primary" />
            <span className="font-mono font-bold text-lg">oyin.journey</span>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <a href="#api" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              API
            </a>
            <a href="#skills" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Skills
            </a>
            <a href="#projects" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Projects
            </a>
            <a href="#certifications" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Certifications
            </a>
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" asChild>
              <a href={sourceRepoUrl} target="_blank" rel="noopener noreferrer">
                <Github className="w-4 h-4 mr-2" />
                Source
              </a>
            </Button>
            <Button variant="outline" size="sm" asChild>
              <a href={liveApiUrl} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="w-4 h-4 mr-2" />
                Live API
              </a>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;