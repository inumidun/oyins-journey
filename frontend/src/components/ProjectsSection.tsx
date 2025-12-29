import { useState } from 'react';
import { useProjects } from '../hooks/useApi';
import { Loader2, ExternalLink, Github } from 'lucide-react';

const ProjectsSection = () => {
  const [filters, setFilters] = useState<{ status?: string }>({});
  const { data, isLoading, error } = useProjects(filters);

  const statuses = ['active', 'completed', 'planned'];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500/20 text-green-400';
      case 'completed': return 'bg-blue-500/20 text-blue-400';
      case 'planned': return 'bg-yellow-500/20 text-yellow-400';
      default: return 'bg-gray-500/20 text-gray-400';
    }
  };

  return (
    <section id="projects" className="py-24">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Projects</span> & Experience
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Live project data with real deployment status and technology stacks.
          </p>
        </div>

        {/* Filters */}
        <div className="flex justify-center mb-12">
          <select
            value={filters.status || ''}
            onChange={(e) => setFilters({ status: e.target.value || undefined })}
            className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white"
          >
            <option value="">All Projects</option>
            {statuses.map(status => (
              <option key={status} value={status}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {/* Projects Grid */}
        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {isLoading ? (
            <div className="col-span-full flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-cyan-500" />
              <span className="ml-2 text-gray-400">Loading projects...</span>
            </div>
          ) : error ? (
            <div className="col-span-full text-center py-12">
              <p className="text-red-400">Failed to load projects</p>
            </div>
          ) : (
            data?.projects?.map((project) => (
              <div key={project.id} className="bg-gray-800 border border-gray-700 rounded-lg p-6 hover:border-cyan-500/50 transition-all duration-300">
                <div className="flex items-start justify-between mb-3">
                  <h3 className="font-semibold text-white text-lg">{project.name}</h3>
                  <span className={`text-xs px-2 py-1 rounded font-mono ${getStatusColor(project.status)}`}>
                    {project.status}
                  </span>
                </div>
                
                <p className="text-gray-400 text-sm mb-4 leading-relaxed">
                  {project.description}
                </p>
                
                <div className="flex flex-wrap gap-2 mb-4">
                  {project.technologies?.map((tech, i) => (
                    <span key={i} className="text-xs px-2 py-1 rounded bg-gray-700 text-gray-300">
                      {tech}
                    </span>
                  ))}
                </div>
                
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>
                    {project.start_date} - {project.end_date || 'Present'}
                  </span>
                  
                  <div className="flex items-center gap-2">
                    {project.repository && (
                      <a 
                        href={project.repository}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-400 hover:text-white transition-colors"
                      >
                        <Github className="w-4 h-4" />
                      </a>
                    )}
                    {project.live_url && (
                      <a 
                        href={project.live_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-gray-400 hover:text-white transition-colors"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {data?.count !== undefined && (
          <div className="text-center mt-8">
            <p className="text-gray-400 font-mono text-sm">
              Showing {data.count} projects
            </p>
          </div>
        )}
      </div>
    </section>
  );
};

export default ProjectsSection;