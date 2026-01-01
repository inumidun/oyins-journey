import { useState, useEffect } from 'react';
import { Search, Filter, ExternalLink, Database, Cloud, Code, Layout, Settings, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { skillsApi, Skill } from '@/services/api';

const categoryIcons: Record<string, React.ElementType> = {
  cloud: Cloud,
  devops: Settings,
  backend: Code,
  frontend: Layout,
  database: Database,
};

const categoryColors: Record<string, string> = {
  cloud: 'bg-primary/20 text-primary border-primary/30',
  devops: 'bg-warning/20 text-warning border-warning/30',
  backend: 'bg-info/20 text-info border-info/30',
  frontend: 'bg-success/20 text-success border-success/30',
  database: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
};

const proficiencyWidth: Record<string, string> = {
  beginner: 'w-1/4',
  intermediate: 'w-2/4',
  advanced: 'w-3/4',
  expert: 'w-full',
};

const SkillsSection = () => {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [cloudFilter, setCloudFilter] = useState<string>('all');

  useEffect(() => {
    const fetchSkills = async () => {
      try {
        setLoading(true);
        const params: any = {};
        if (categoryFilter !== 'all') params.category = categoryFilter;
        if (cloudFilter !== 'all') params.cloud = cloudFilter;
        
        const response = await skillsApi.getAll(params);
        setSkills(response.skills || response || []);
      } catch (err) {
        console.error('Error fetching skills:', err);
        // Use fallback data when API is unavailable
        const fallbackSkills: Skill[] = [
          { id: 'aws-lambda', name: 'AWS Lambda', category: 'cloud', technologies: ['Python', 'Node.js'], usage_count: 12, proficiency: 'advanced', years_experience: 3 },
          { id: 'dynamodb', name: 'DynamoDB', category: 'database', technologies: ['NoSQL', 'AWS'], usage_count: 8, proficiency: 'advanced', years_experience: 2 },
          { id: 'api-gateway', name: 'API Gateway', category: 'cloud', technologies: ['REST', 'AWS'], usage_count: 10, proficiency: 'advanced', years_experience: 3 },
          { id: 'terraform', name: 'Terraform', category: 'devops', technologies: ['IaC', 'HCL'], usage_count: 6, proficiency: 'intermediate', years_experience: 2 },
          { id: 'github-actions', name: 'GitHub Actions', category: 'devops', technologies: ['CI/CD', 'YAML'], usage_count: 15, proficiency: 'advanced', years_experience: 3 },
          { id: 'cloudwatch', name: 'CloudWatch', category: 'cloud', technologies: ['Monitoring', 'AWS'], usage_count: 9, proficiency: 'intermediate', years_experience: 2 },
          { id: 's3', name: 'S3', category: 'cloud', technologies: ['Storage', 'AWS'], usage_count: 14, proficiency: 'expert', years_experience: 4 },
          { id: 'cloudfront', name: 'CloudFront', category: 'cloud', technologies: ['CDN', 'AWS'], usage_count: 4, proficiency: 'intermediate', years_experience: 2 },
          { id: 'typescript', name: 'TypeScript', category: 'backend', technologies: ['JavaScript', 'Node.js'], usage_count: 20, proficiency: 'advanced', years_experience: 3 },
          { id: 'react', name: 'React', category: 'frontend', technologies: ['JavaScript', 'UI'], usage_count: 18, proficiency: 'advanced', years_experience: 3 },
          { id: 'python', name: 'Python', category: 'backend', technologies: ['Scripting', 'API'], usage_count: 16, proficiency: 'advanced', years_experience: 4 },
          { id: 'docker', name: 'Docker', category: 'devops', technologies: ['Containers', 'DevOps'], usage_count: 7, proficiency: 'intermediate', years_experience: 2 }
        ];
        
        // Apply filters to fallback data
        let filtered = fallbackSkills;
        if (categoryFilter !== 'all') {
          filtered = filtered.filter(s => s.category === categoryFilter);
        }
        if (cloudFilter !== 'all' && cloudFilter === 'aws') {
          filtered = filtered.filter(s => s.technologies.some(t => t.toLowerCase().includes('aws')) || s.category === 'cloud');
        }
        setSkills(filtered);
      } finally {
        setLoading(false);
      }
    };

    fetchSkills();
  }, [categoryFilter, cloudFilter]);

  const filteredSkills = skills.filter((skill) => {
    const matchesSearch = skill.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSearch;
  });

  const categories = ['all', 'cloud', 'devops', 'backend', 'frontend', 'database'];

  if (loading) {
    return (
      <section id="skills" className="py-24 bg-secondary/20">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-center">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
            <span className="ml-2 text-muted-foreground">Loading skills...</span>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="skills" className="py-24 bg-secondary/20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-mono mb-4">
            /skills
          </span>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Queryable <span className="gradient-text">Skills</span> Intelligence
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Skills are structured data, not bullet points. Filter and query my experience just like you would a database.
          </p>
        </div>

        {/* Query Builder */}
        <div className="max-w-4xl mx-auto mb-12">
          <div className="bg-card border border-border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-4 font-mono text-sm text-muted-foreground">
              <Filter className="w-4 h-4 text-primary" />
              <span>Query Builder</span>
            </div>
            
            <div className="grid md:grid-cols-3 gap-4">
              {/* Search */}
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search skills..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:border-primary transition-colors"
                />
              </div>

              {/* Category filter */}
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="px-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:border-primary transition-colors"
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat === 'all' ? 'All Categories' : cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </option>
                ))}
              </select>

              {/* Cloud filter */}
              <select
                value={cloudFilter}
                onChange={(e) => setCloudFilter(e.target.value)}
                className="px-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:border-primary transition-colors"
              >
                <option value="all">All Clouds</option>
                <option value="aws">AWS Only</option>
              </select>
            </div>

            {/* Generated query */}
            <div className="mt-4 p-3 bg-background rounded-md font-mono text-xs">
              <span className="text-success">GET</span>
              <span className="text-muted-foreground"> /skills</span>
              <span className="text-primary">
                ?category={categoryFilter}
                &cloud={cloudFilter}
                {searchQuery && `&search=${searchQuery}`}
              </span>
            </div>
          </div>
        </div>

        {/* Results count */}
        <div className="max-w-4xl mx-auto mb-6">
          <p className="text-sm text-muted-foreground font-mono">
            Found <span className="text-primary">{filteredSkills.length}</span> skills matching your query
          </p>
        </div>

        {/* Skills grid */}
        <div className="max-w-4xl mx-auto grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredSkills.map((skill) => {
            const Icon = categoryIcons[skill.category] || Database;
            return (
              <div
                key={skill.id}
                className="bg-card border border-border rounded-lg p-4 card-hover group"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <div className={`p-2 rounded-md border ${categoryColors[skill.category] || 'bg-muted/20 text-muted-foreground border-muted/30'}`}>
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground">{skill.name}</h3>
                      <p className="text-xs text-muted-foreground capitalize">{skill.category}</p>
                    </div>
                  </div>
                  <Button variant="ghost" size="icon" className="w-6 h-6 opacity-0 group-hover:opacity-100 transition-opacity">
                    <ExternalLink className="w-3 h-3" />
                  </Button>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Proficiency</span>
                    <span className="text-primary capitalize">{skill.proficiency}</span>
                  </div>
                  <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
                    <div className={`h-full bg-primary rounded-full ${proficiencyWidth[skill.proficiency] || 'w-2/4'}`} />
                  </div>
                </div>

                <div className="flex items-center justify-between mt-3 pt-3 border-t border-border">
                  <span className="text-xs text-muted-foreground">Years Experience</span>
                  <span className="font-mono text-sm text-primary">{skill.years_experience || 0}</span>
                </div>

                {skill.technologies && skill.technologies.length > 0 && (
                  <div className="mt-2">
                    <div className="flex flex-wrap gap-1">
                      {skill.technologies.slice(0, 3).map((tech, index) => (
                        <span key={index} className="inline-block px-2 py-0.5 rounded text-xs bg-primary/10 text-primary font-mono">
                          {tech}
                        </span>
                      ))}
                      {skill.technologies.length > 3 && (
                        <span className="text-xs text-muted-foreground">+{skill.technologies.length - 3} more</span>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default SkillsSection;