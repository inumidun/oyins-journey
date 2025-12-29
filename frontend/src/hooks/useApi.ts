import { useQuery } from '@tanstack/react-query';
import { skillsApi, projectsApi, certificationsApi, systemApi } from '../services/api';

export const useSkills = (filters?: { category?: string; cloud?: string }) => {
  return useQuery({
    queryKey: ['skills', filters],
    queryFn: () => skillsApi.getAll(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useProjects = (filters?: { status?: string; technology?: string }) => {
  return useQuery({
    queryKey: ['projects', filters],
    queryFn: () => projectsApi.getAll(filters),
    staleTime: 5 * 60 * 1000,
  });
};

export const useCertifications = (filters?: { provider?: string; status?: string }) => {
  return useQuery({
    queryKey: ['certifications', filters],
    queryFn: () => certificationsApi.getAll(filters),
    staleTime: 5 * 60 * 1000,
  });
};

export const useSystemHealth = () => {
  return useQuery({
    queryKey: ['system-health'],
    queryFn: systemApi.healthCheck,
    refetchInterval: 30000, // 30 seconds
  });
};