import { Terminal } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="py-12 border-t border-border">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center gap-4">
          <div className="flex items-center gap-2">
            <Terminal className="w-5 h-5 text-primary" />
            <span className="font-mono font-bold">oyin.journey</span>
          </div>
          <p className="text-sm text-muted-foreground text-center">
            A living, breathing cloud architecture that demonstrates real-world engineering skills.
          </p>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>Built with</span>
            <span className="text-primary">AWS</span>
            <span>•</span>
            <span className="text-primary">Terraform</span>
            <span>•</span>
            <span className="text-primary">React</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;