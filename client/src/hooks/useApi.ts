import { useState, useCallback } from 'react';
import axios, { AxiosResponse } from 'axios';

const API_BASE_URL = 'http://localhost:3001';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const request = useCallback(async <T>(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    endpoint: string,
    data?: any
  ): Promise<T | null> => {
    try {
      setLoading(true);
      setError(null);
      
      const response: AxiosResponse<T> = await axios({
        method,
        url: `${API_BASE_URL}${endpoint}`,
        data,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'שגיאה לא ידועה';
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    request,
    clearError: () => setError(null),
  };
};
