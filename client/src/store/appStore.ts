import { create } from 'zustand';

interface AppState {
  // Auth status
  facebookStatus: 'connected' | 'needs_reauth' | 'disconnected';
  lastVerifiedAt: string | null;
  
  // UI state
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setFacebookStatus: (status: 'connected' | 'needs_reauth' | 'disconnected') => void;
  setLastVerifiedAt: (date: string | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Initial state
  facebookStatus: 'disconnected',
  lastVerifiedAt: null,
  isLoading: false,
  error: null,
  
  // Actions
  setFacebookStatus: (status) => set({ facebookStatus: status }),
  setLastVerifiedAt: (date) => set({ lastVerifiedAt: date }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
}));
