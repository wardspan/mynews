'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { useToast } from '@chakra-ui/react';
import { User, UserCreate } from '../types/user';
import { auth as authApi } from '../services/api';
import { setToken, getToken, removeToken, isLoggedIn } from '../services/auth';

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (userData: UserCreate) => Promise<boolean>;
  logout: () => void;
  loading: boolean;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps): JSX.Element => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();
  const toast = useToast();

  useEffect(() => {
    // Check if user is logged in on initial load
    const initAuth = async (): Promise<void> => {
      if (isLoggedIn()) {
        try {
          const response = await authApi.getProfile();
          setUser(response.data);
        } catch (error) {
          console.error('Failed to fetch user profile', error);
          removeToken();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      const response = await authApi.login(formData);
      setToken(response.data.access_token);
      
      // Fetch user profile after successful login
      const userResponse = await authApi.getProfile();
      setUser(userResponse.data);
      
      toast({
        title: 'Login successful',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
      return true;
    } catch (error: any) {
      console.error('Login failed', error);
      const errorMessage = error.response?.data?.detail || 'Login failed. Please try again.';
      
      toast({
        title: 'Login failed',
        description: errorMessage,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      
      return false;
    }
  };

  const register = async (userData: UserCreate): Promise<boolean> => {
    try {
      const response = await authApi.register(userData);
      toast({
        title: 'Registration successful',
        description: 'You can now log in with your credentials',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      return true;
    } catch (error: any) {
      console.error('Registration failed', error);
      const errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.';
      
      toast({
        title: 'Registration failed',
        description: errorMessage,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      
      return false;
    }
  };

  const logout = (): void => {
    removeToken();
    setUser(null);
    router.push('/login');
    
    toast({
      title: 'Logged out successfully',
      status: 'info',
      duration: 3000,
      isClosable: true,
    });
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      login, 
      register, 
      logout, 
      loading, 
      isAuthenticated: !!user 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};