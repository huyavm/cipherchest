import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import api from '../api';

type AuthContextType = {
  user: any;
  token: string | null;
  csrf: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (fullName: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'));
  const [refreshToken, setRefreshToken] = useState<string | null>(() => localStorage.getItem('refresh_token'));
  const [csrf, setCsrf] = useState<string | null>(() => localStorage.getItem('csrf_token'));
  const [user, setUser] = useState<any>(() => {
    const raw = localStorage.getItem('user');
    return raw ? JSON.parse(raw) : null;
  });

  useEffect(() => {
    const interceptor = api.interceptors.request.use((config) => {
      if (token) {
        config.headers = config.headers ?? {};
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      if (csrf && config.method && ['post', 'put', 'patch', 'delete'].includes(config.method)) {
        config.headers = config.headers ?? {};
        config.headers['csrf-token'] = csrf;
      }
      return config;
    });
    return () => api.interceptors.request.eject(interceptor);
  }, [token, csrf]);

  const persist = (payload: any) => {
    setToken(payload.access_token);
    setRefreshToken(payload.refresh_token);
    setCsrf(payload.csrf_token);
    setUser(payload.user);
    localStorage.setItem('access_token', payload.access_token);
    localStorage.setItem('refresh_token', payload.refresh_token);
    localStorage.setItem('csrf_token', payload.csrf_token);
    localStorage.setItem('user', JSON.stringify(payload.user));
  };

  const login = async (email: string, password: string) => {
    const { data } = await api.post('/auth/login', { email, password });
    persist(data);
  };

  const register = async (fullName: string, email: string, password: string) => {
    await api.post('/auth/register', { full_name: fullName, email, password });
    await login(email, password);
  };

  const logout = async () => {
    if (refreshToken) {
      await api.post('/auth/logout', { refresh_token: refreshToken });
    }
    setToken(null);
    setRefreshToken(null);
    setCsrf(null);
    setUser(null);
    localStorage.clear();
  };

  const value = useMemo(() => ({ token, csrf, user, login, register, logout }), [token, csrf, user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('AuthContext missing');
  return ctx;
};
