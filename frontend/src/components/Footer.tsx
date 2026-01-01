import { Terminal, Linkedin, Github, Mail } from 'lucide-react';
import { useSiteConfig } from '@/hooks/useSiteConfig';

const Footer = () => {
  const { config } = useSiteConfig();
  
  // Use config or fallback to hardcoded values
  const socialLinks = config?.socialLinks || {
    linkedin: 'https://linkedin.com/in/oyindamola-oladipo',
    github: 'https://github.com/oyindamola-oladipo',
    email: 'mailto:hello@oyins-journey.dev'
  };

  return (
    <footer className="py-12 border-t border-border">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center gap-6">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <Terminal className="w-5 h-5 text-primary" />
            <span className="font-mono font-bold">oyin.journey</span>
          </div>

          {/* Social Links */}
          <div className="flex items-center gap-4">
            {socialLinks.linkedin && (
              <a 
                href={socialLinks.linkedin} 
                target="_blank" 
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-secondary/50 border border-border hover:border-primary/50 hover:bg-primary/10 transition-all"
                aria-label="LinkedIn Profile"
              >
                <Linkedin className="w-4 h-4 text-muted-foreground hover:text-primary" />
              </a>
            )}
            {socialLinks.github && (
              <a 
                href={socialLinks.github} 
                target="_blank" 
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-secondary/50 border border-border hover:border-primary/50 hover:bg-primary/10 transition-all"
                aria-label="GitHub Profile"
              >
                <Github className="w-4 h-4 text-muted-foreground hover:text-primary" />
              </a>
            )}
            {socialLinks.email && (
              <a 
                href={socialLinks.email}
                className="p-2 rounded-full bg-secondary/50 border border-border hover:border-primary/50 hover:bg-primary/10 transition-all"
                aria-label="Email Me"
              >
                <Mail className="w-4 h-4 text-muted-foreground hover:text-primary" />
              </a>
            )}
          </div>

          {/* Description */}
          <p className="text-sm text-muted-foreground text-center max-w-md">
            A living, breathing cloud architecture that demonstrates real-world engineering skills.
          </p>

          {/* Tech Stack */}
          <div className="flex flex-wrap items-center justify-center gap-2 text-xs text-muted-foreground">
            <span>Built with</span>
            <span className="px-2 py-1 rounded bg-secondary/50 text-primary font-mono">AWS</span>
            <span className="px-2 py-1 rounded bg-secondary/50 text-primary font-mono">Terraform</span>
            <span className="px-2 py-1 rounded bg-secondary/50 text-primary font-mono">React</span>
            <span className="px-2 py-1 rounded bg-secondary/50 text-primary font-mono">TypeScript</span>
          </div>

          {/* Copyright */}
          <p className="text-xs text-muted-foreground">
            © {new Date().getFullYear()} Oyin's Journey. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;