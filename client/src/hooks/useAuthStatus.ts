import { useEffect } from 'react';
import { useAppStore } from '../store/appStore';
import { useApi } from './useApi';

export const useAuthStatus = () => {
  const { facebookStatus, setFacebookStatus, setLastVerifiedAt } = useAppStore();
  const { request } = useApi();

  const checkAuthStatus = async () => {
    const response = await request<{
      status: 'connected' | 'needs_reauth' | 'disconnected';
      lastVerifiedAt: string | null;
    }>('GET', '/auth/facebook/status');
    
    if (response) {
      setFacebookStatus(response.status);
      setLastVerifiedAt(response.lastVerifiedAt);
    }
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  return {
    facebookStatus,
    checkAuthStatus,
  };
};
