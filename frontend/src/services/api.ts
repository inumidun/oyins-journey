import axios from 'axios';
import { authService } from './auth';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/dev';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor for admin requests
api.interceptors.request.use(async (config) => {
  // Add auth header for admin endpoints
  if (config.url?.includes('/admin/')) {
    const token = await authService.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Try to refresh the session
      try {
        await authService.refreshSession();
        // Retry the original request
        const token = await authService.getAccessToken();
        if (token) {
          error.config.headers.Authorization = `Bearer ${token}`;
          return api.request(error.config);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        window.location.href = '/admin/login';
      }
    }
    return Promise.reject(error);
  }
);

export interface Skill {
  id: string;
  name: string;
  category: string;
  technologies: string[];
  usage_count: number;
  proficiency: string;
  years_experience: number;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'completed' | 'planned';
  technologies: string[];
  start_date: string;
  end_date?: string;
  repository?: string;
  live_url?: string;
}

export interface Certification {
  id: string;
  name: string;
  provider: string;
  issue_date: string;
  expiry_date?: string;
  credential_id?: string;
  computed_status?: 'active' | 'expired' | 'expiring_soon' | 'no_expiry';
  credly_url?: string;
  badge_url?: string;
}

export interface SiteConfig {
  socialLinks: {
    linkedin?: string;
    github?: string;
    email?: string;
    twitter?: string;
    website?: string;
  };
  branding: {
    name: string;
    tagline: string;
  };
  sourceRepoUrl: string;
  liveApiUrl: string;
}

export const skillsApi = {
  getAll: async (params?: { category?: string; cloud?: string }) => {
    const response = await api.get('/skills', { params });
    return response.data;
  },
};

export const projectsApi = {
  getAll: async (params?: { status?: string; technology?: string }) => {
    const response = await api.get('/projects', { params });
    return response.data;
  },
};

export const certificationsApi = {
  getAll: async (params?: { provider?: string; status?: string }) => {
    const response = await api.get('/certifications', { params });
    return response.data;
  },
};

export const siteConfigApi = {
  get: async (): Promise<SiteConfig> => {
    try {
      const response = await api.get('/config');
      return response.data;
    } catch (error) {
      // Return default config if API fails
      return {
        socialLinks: {
          linkedin: 'https://linkedin.com/in/your-linkedin-username',
          github: 'https://github.com/your-github-username',
          email: 'mailto:hello@your-domain.com'
        },
        branding: {
          name: 'Your Name',
          tagline: 'Your Professional Title'
        },
        sourceRepoUrl: 'https://github.com/your-github-username/your-repo-name',
        liveApiUrl: 'https://api.your-domain.com'
      };
    }
  },
  
  update: async (config: Partial<SiteConfig>): Promise<SiteConfig> => {
    const response = await api.put('/admin/config', config);
    return response.data;
  }
};

export const systemApi = {
  healthCheck: async () => {
    try {
      const start = Date.now();
      await api.get('/skills');
      const latency = Date.now() - start;
      return { status: 'online', latency: `${latency}ms` };
    } catch {
      return { status: 'offline', latency: 'N/A' };
    }
  },
};

export default api;