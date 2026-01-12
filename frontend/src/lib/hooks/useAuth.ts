import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { apiClient } from '../api/client';

interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const token = localStorage.getItem('auth_token');
    if (token) {
      // Verify token and get user info
      fetchUserInfo();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserInfo = async () => {
    try {
      // You would typically have a /me endpoint
      // For now, we'll just set loading to false
      setLoading(false);
    } catch (error) {
      localStorage.removeItem('auth_token');
      apiClient.clearToken();
      setLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    try {
      // Replace with actual login API call
      // const response = await apiClient.post('/api/auth/login', { username, password });
      // const { token, user } = response;

      // Mock login for now
      const mockToken = 'mock_jwt_token';
      const mockUser = { id: 1, username, email: `${username}@example.com` };

      localStorage.setItem('auth_token', mockToken);
      apiClient.setToken(mockToken);
      setUser(mockUser);
    } catch (error) {
      throw new Error('Login failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    apiClient.clearToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}