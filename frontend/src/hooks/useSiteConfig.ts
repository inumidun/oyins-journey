import { useState, useEffect } from 'react';
import { siteConfigApi, SiteConfig } from '@/services/api';

export const useSiteConfig = () => {
  const [config, setConfig] = useState<SiteConfig | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchConfig = async () => {
    try {
      setLoading(true);
      setError(null);
      const siteConfig = await siteConfigApi.get();
      setConfig(siteConfig);
    } catch (err) {
      console.error('Failed to fetch site config:', err);
      setError('Failed to load site configuration');
      // The API already provides fallback data, so we should still have config
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConfig();
  }, []);

  const updateConfig = async (updates: Partial<SiteConfig>) => {
    try {
      const updatedConfig = await siteConfigApi.update(updates);
      setConfig(updatedConfig);
      return updatedConfig;
    } catch (err) {
      console.error('Failed to update site config:', err);
      throw err;
    }
  };

  return {
    config,
    loading,
    error,
    refetch: fetchConfig,
    updateConfig
  };
};