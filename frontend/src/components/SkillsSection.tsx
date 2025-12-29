import { useState } from 'react';
import { useSkills } from '../hooks/useApi';
import { Loader2 } from 'lucide-react';

const SkillsSection = () => {
  const [filters, setFilters] = useState<{ category?: string; cloud?: string }>({});
  const { data, isLoading, error } = useSkills(filters);

  const categories = ['cloud', 'programming', 'devops', 'database'];
  const cloudProviders = ['aws', 'azure', 'gcp'];

  return (
    <section id="skills" className="py-24 bg-gray-800/30">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">Skills</span> & Technologies
          </h2>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Real-time data from my skills database, queryable by category and cloud provider.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-4 justify-center mb-12">
          <select
            value={filters.category || ''}
            onChange={(e) => setFilters(prev => ({ ...prev, category: e.target.value || undefined }))}
            className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white"
          >
            <option value="">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat.charAt(0).toUpperCase() + cat.slice(1)}</option>
            ))}
          </select>
          
          <select
            value={filters.cloud || ''}
            onChange={(e) => setFilters(prev => ({ ...prev, cloud: e.target.value || undefined }))}
            className="px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white"
          >
            <option value="">All Providers</option>
            {cloudProviders.map(cloud => (
              <option key={cloud} value={cloud}>{cloud.toUpperCase()}</option>
            ))}
          </select>
        </div>

        {/* Skills Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {isLoading ? (
            <div className="col-span-full flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-cyan-500" />
              <span className="ml-2 text-gray-400">Loading skills...</span>
            </div>
          ) : error ? (
            <div className="col-span-full text-center py-12">
              <p className="text-red-400">Failed to load skills</p>
            </div>
          ) : (
            data?.skills?.map((skill) => (
              <div key={skill.id} className="bg-gray-800 border border-gray-700 rounded-lg p-6 hover:border-cyan-500/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-white">{skill.name}</h3>
                  <span className="text-xs px-2 py-1 rounded bg-cyan-500/20 text-cyan-400 font-mono">
                    {skill.category}
                  </span>
                </div>
                <div className="text-sm text-gray-400 mb-2">
                  Proficiency: {skill.proficiency}
                </div>
                <div className="text-xs text-gray-500 mb-3">
                  Used in {skill.usage_count} projects
                </div>
                {skill.technologies && (
                  <div className="flex flex-wrap gap-1">
                    {skill.technologies.slice(0, 3).map((tech, i) => (
                      <span key={i} className="text-xs px-2 py-1 rounded bg-gray-700 text-gray-300">
                        {tech}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {data?.count !== undefined && (
          <div className="text-center mt-8">
            <p className="text-gray-400 font-mono text-sm">
              Showing {data.count} skills
            </p>
          </div>
        )}
      </div>
    </section>
  );
};

export default SkillsSection;