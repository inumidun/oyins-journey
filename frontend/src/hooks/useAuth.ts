import { useState, useEffect } from 'react';
import { authService, AuthState, SignInResult } from '@/services/auth';

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>(authService.getAuthState());

  useEffect(() => {
    const unsubscribe = authService.subscribe(setAuthState);
    return unsubscribe;
  }, []);

  const signIn = async (email: string, password: string): Promise<SignInResult> => {
    return authService.signIn(email, password);
  };

  const signOut = async (): Promise<void> => {
    return authService.signOut();
  };

  const getAccessToken = async (): Promise<string | null> => {
    return authService.getAccessToken();
  };

  const refreshSession = async (): Promise<void> => {
    return authService.refreshSession();
  };

  return {
    ...authState,
    signIn,
    signOut,
    getAccessToken,
    refreshSession,
  };
};