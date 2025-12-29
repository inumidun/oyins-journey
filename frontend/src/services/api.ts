import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/dev';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

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