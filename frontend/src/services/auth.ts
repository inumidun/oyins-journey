import { Amplify } from 'aws-amplify';
import { signIn, signOut, getCurrentUser, fetchAuthSession, SignInInput, AuthUser } from '@aws-amplify/auth';

// Amplify configuration
const authConfig = {
  Auth: {
    Cognito: {
      userPoolId: import.meta.env.VITE_COGNITO_USER_POOL_ID || '',
      userPoolClientId: import.meta.env.VITE_COGNITO_USER_POOL_CLIENT_ID || '',
      loginWith: {
        email: true,
      },
    },
  },
};

// Configure Amplify
Amplify.configure(authConfig);

export interface AuthState {
  isAuthenticated: boolean;
  user: AuthUser | null;
  loading: boolean;
  error: string | null;
}

export interface SignInResult {
  success: boolean;
  error?: string;
  requiresNewPassword?: boolean;
}

export class AuthService {
  private static instance: AuthService;
  private authState: AuthState = {
    isAuthenticated: false,
    user: null,
    loading: true,
    error: null,
  };
  private listeners: ((state: AuthState) => void)[] = [];

  private constructor() {
    this.initializeAuth();
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  private async initializeAuth() {
    try {
      const user = await getCurrentUser();
      const session = await fetchAuthSession();
      
      this.updateAuthState({
        isAuthenticated: !!user && !!session.tokens?.accessToken,
        user,
        loading: false,
        error: null,
      });
    } catch (error) {
      this.updateAuthState({
        isAuthenticated: false,
        user: null,
        loading: false,
        error: null, // Not an error if user is not signed in
      });
    }
  }

  private updateAuthState(newState: Partial<AuthState>) {
    this.authState = { ...this.authState, ...newState };
    this.listeners.forEach(listener => listener(this.authState));
  }

  public subscribe(listener: (state: AuthState) => void): () => void {
    this.listeners.push(listener);
    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  public getAuthState(): AuthState {
    return this.authState;
  }

  public async signIn(email: string, password: string): Promise<SignInResult> {
    try {
      this.updateAuthState({ loading: true, error: null });

      const signInInput: SignInInput = {
        username: email,
        password,
      };

      const result = await signIn(signInInput);

      if (result.isSignedIn) {
        const user = await getCurrentUser();
        this.updateAuthState({
          isAuthenticated: true,
          user,
          loading: false,
          error: null,
        });
        return { success: true };
      } else if (result.nextStep?.signInStep === 'CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED') {
        this.updateAuthState({ loading: false });
        return { 
          success: false, 
          requiresNewPassword: true,
          error: 'New password required' 
        };
      } else {
        this.updateAuthState({ loading: false });
        return { 
          success: false, 
          error: 'Sign in incomplete' 
        };
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Sign in failed';
      this.updateAuthState({
        loading: false,
        error: errorMessage,
      });
      return { success: false, error: errorMessage };
    }
  }

  public async signOut(): Promise<void> {
    try {
      await signOut();
      this.updateAuthState({
        isAuthenticated: false,
        user: null,
        loading: false,
        error: null,
      });
    } catch (error: any) {
      console.error('Sign out error:', error);
      // Force sign out locally even if remote sign out fails
      this.updateAuthState({
        isAuthenticated: false,
        user: null,
        loading: false,
        error: null,
      });
    }
  }

  public async getAccessToken(): Promise<string | null> {
    try {
      const session = await fetchAuthSession();
      return session.tokens?.accessToken?.toString() || null;
    } catch (error) {
      console.error('Failed to get access token:', error);
      return null;
    }
  }

  public async refreshSession(): Promise<void> {
    try {
      const session = await fetchAuthSession({ forceRefresh: true });
      if (session.tokens?.accessToken) {
        const user = await getCurrentUser();
        this.updateAuthState({
          isAuthenticated: true,
          user,
          error: null,
        });
      } else {
        throw new Error('No valid session');
      }
    } catch (error) {
      this.updateAuthState({
        isAuthenticated: false,
        user: null,
        error: 'Session expired',
      });
      throw error;
    }
  }
}

// Export singleton instance
export const authService = AuthService.getInstance();