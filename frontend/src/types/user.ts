export interface UserBase {
    email: string;
    name: string;
  }
  
  export interface User extends UserBase {
    id: string;
    created_at: string | Date;
    updated_at: string | Date;
    saved_articles: string[];
    recent_tabs: string[];
  }
  
  export interface UserCreate extends UserBase {
    password: string;
  }
  
  export interface UserUpdate {
    email?: string;
    name?: string;
    password?: string;
  }
  
  export interface LoginCredentials {
    username: string;
    password: string;
  }
  
  export interface AuthResponse {
    access_token: string;
    token_type: string;
  }
  
  export interface TokenPayload {
    sub: string;
    exp: number;
  }