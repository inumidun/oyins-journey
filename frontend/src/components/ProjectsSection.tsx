import { useState, useEffect } from 'react';
import { ExternalLink, Github, Play, BarChart3, CheckCircle2, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { projectsApi, Project } from '@/services/api';

const ProjectsSection = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const response = await projectsApi.getAll();
        setProjects(response.projects || response || []);
      } catch (err) {
        setError('Failed to load projects');
        console.error('Error fetching projects:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  if (loading) {
    return (
      <section id="projects" className="py-24">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-center">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
            <span className="ml-2 text-muted-foreground">Loading projects...</span>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="projects" className="py-24">
        <div className="container mx-auto px-4">
          <div className="text-center text-destructive">
            <p>Error: {error}</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="projects" className="py-24">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-mono mb-4">
            /projects
          </span>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Proof by <span className="gradient-text">Link</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            No screenshots, no claims. Every project links to live proof — repos, demos, pipelines, and dashboards.
          </p>
        </div>

        <div className="max-w-5xl mx-auto space-y-6">
          {projects.map((project, index) => (
            <div
              key={project.id}
              className="bg-card border border-border rounded-xl overflow-hidden card-hover slide-up"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="p-6 md:p-8">
                <div className="flex flex-col md:flex-row md:items-start gap-6">
                  {/* Main content */}
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <h3 className="text-xl font-bold text-foreground">{project.name}</h3>
                      <span className="text-xs font-mono text-muted-foreground">{project.start_date}</span>
                    </div>
                    <p className="text-muted-foreground mb-4">{project.description}</p>

                    {/* Tech stack */}
                    {project.technologies && project.technologies.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-4">
                        {project.technologies.map((tech) => (
                          <span
                            key={tech}
                            className="px-2 py-1 rounded text-xs bg-secondary text-secondary-foreground font-mono"
                          >
                            {tech}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Status */}
                    <div className="flex flex-wrap gap-2">
                      <span className="px-2 py-1 rounded text-xs bg-primary/10 text-primary font-mono capitalize">
                        {project.status}
                      </span>
                    </div>
                  </div>

                  {/* Badges and links */}
                  <div className="flex flex-col gap-4">
                    {/* Evidence links */}
                    <div className="flex flex-wrap gap-2">
                      {project.repository && (
                        <Button variant="outline" size="sm" className="font-mono text-xs" asChild>
                          <a href={project.repository} target="_blank" rel="noopener noreferrer">
                            <Github className="w-3 h-3 mr-1" />
                            Repo
                          </a>
                        </Button>
                      )}
                      {project.live_url && (
                        <Button variant="outline" size="sm" className="font-mono text-xs" asChild>
                          <a href={project.live_url} target="_blank" rel="noopener noreferrer">
                            <ExternalLink className="w-3 h-3 mr-1" />
                            Demo
                          </a>
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ProjectsSection;