import { useState, useEffect } from 'react';
import { ExternalLink, Github, Globe, GitBranch, CheckCircle, Clock, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { projectsApi, Project } from '@/services/api';

const ProjectsSection = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const params: any = {};
        if (statusFilter !== 'all') params.status = statusFilter;
        
        const response = await projectsApi.getAll(params);
        setProjects(response.projects || response || []);
      } catch (err) {
        setError('Failed to load projects');
        console.error('Error fetching projects:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, [statusFilter]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4 text-success" />;
      case 'active': return <Clock className="w-4 h-4 text-warning" />;
      case 'planned': return <GitBranch className="w-4 h-4 text-info" />;
      default: return <Clock className="w-4 h-4 text-muted-foreground" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-success/10 text-success border-success/30';
      case 'active': return 'bg-warning/10 text-warning border-warning/30';
      case 'planned': return 'bg-info/10 text-info border-info/30';
      default: return 'bg-muted/10 text-muted-foreground border-muted/30';
    }
  };

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
            Project <span className="gradient-text">Portfolio</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Real projects with live deployments, source code, and architectural decisions. 
            Each project demonstrates specific technical capabilities.
          </p>
        </div>

        {/* Filter */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">Filter by status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:border-primary transition-colors"
            >
              <option value="all">All Projects</option>
              <option value="completed">Completed</option>
              <option value="active">Active</option>
              <option value="planned">Planned</option>
            </select>
          </div>
        </div>

        {/* Projects grid */}
        <div className="max-w-4xl mx-auto space-y-6">
          {projects.map((project) => (
            <div
              key={project.id}
              className="bg-card border border-border rounded-lg p-6 card-hover group"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-semibold text-foreground">{project.name}</h3>
                    <div className={`flex items-center gap-1 px-2 py-1 rounded-full border text-xs ${getStatusColor(project.status)}`}>
                      {getStatusIcon(project.status)}
                      <span className="capitalize">{project.status}</span>
                    </div>
                  </div>
                  <p className="text-muted-foreground mb-4">{project.description}</p>
                </div>
              </div>

              {/* Technologies */}
              {project.technologies && project.technologies.length > 0 && (
                <div className="mb-4">
                  <p className="text-xs text-muted-foreground mb-2">Technologies:</p>
                  <div className="flex flex-wrap gap-2">
                    {project.technologies.map((tech, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 rounded bg-secondary text-xs font-mono text-foreground"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Project details */}
              <div className="grid md:grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-xs text-muted-foreground mb-1">Start Date</p>
                  <p className="font-mono text-sm">{project.start_date}</p>
                </div>
                {project.end_date && (
                  <div>
                    <p className="text-xs text-muted-foreground mb-1">End Date</p>
                    <p className="font-mono text-sm">{project.end_date}</p>
                  </div>
                )}
              </div>

              {/* Links */}
              <div className="flex items-center gap-2 pt-4 border-t border-border">
                {project.repository && (
                  <Button variant="outline" size="sm" asChild>
                    <a href={project.repository} target="_blank" rel="noopener noreferrer">
                      <Github className="w-4 h-4 mr-2" />
                      Source
                    </a>
                  </Button>
                )}
                {project.live_url && (
                  <Button variant="outline" size="sm" asChild>
                    <a href={project.live_url} target="_blank" rel="noopener noreferrer">
                      <Globe className="w-4 h-4 mr-2" />
                      Live Demo
                    </a>
                  </Button>
                )}
                <Button variant="ghost" size="sm">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Details
                </Button>
              </div>
            </div>
          ))}
        </div>

        {projects.length === 0 && (
          <div className="text-center text-muted-foreground">
            <p>No projects found matching your criteria.</p>
          </div>
        )}
      </div>
    </section>
  );
};

export default ProjectsSection;