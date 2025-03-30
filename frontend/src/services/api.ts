import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { getToken } from './auth';
import { 
  Article, 
  ArticleCreate, 
  CategoryInfo, 
  SourceInfo 
} from '../types/article';
import { 
  User, 
  UserCreate, 
  AuthResponse 
} from '../types/user';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to attach the auth token
api.interceptors.request.use(
  (config: AxiosRequestConfig): AxiosRequestConfig => {
    const token = getToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

// API methods for authentication
export const auth = {
  login: (credentials: FormData): Promise<AxiosResponse<AuthResponse>> => 
    api.post('/auth/login', credentials),
  
  register: (userData: UserCreate): Promise<AxiosResponse<User>> => 
    api.post('/auth/register', userData),
  
  getProfile: (): Promise<AxiosResponse<User>> => 
    api.get('/auth/me'),
};

// API methods for articles
export const articles = {
  getAll: (params?: any): Promise<AxiosResponse<Article[]>> => 
    api.get('/articles', { params }),
  
  getLatest: (params?: any): Promise<AxiosResponse<Article[]>> => 
    api.get('/articles/latest', { params }),
  
  getById: (id: string): Promise<AxiosResponse<Article>> => 
    api.get(`/articles/${id}`),
  
  create: (article: ArticleCreate): Promise<AxiosResponse<Article>> => 
    api.post('/articles', article),
  
  getSources: (): Promise<AxiosResponse<SourceInfo[]>> => 
    api.get('/articles/sources/list'),
  
  getCategories: (): Promise<AxiosResponse<CategoryInfo[]>> => 
    api.get('/articles/categories/list'),
};

export default api;