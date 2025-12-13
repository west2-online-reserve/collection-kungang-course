export interface User {
  id?: number;
  username: string;
  role:string
  height?: number | null;
  weight?: number | null;
}

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData extends LoginData {
  confirmPassword: string;
  height?: number | null;
  weight?: number | null;
}

export interface AuthResponse {
  code: number;
  message: string;
  data: {
    token: string;
    user: User;
  };
}

export interface refreshTokenResponse {
  code: number;
  message: string;
  data: {
    token: string;
  }
}

export interface SimpleProfileForm {
  username: string
  height: string
  weight: string
}

export interface FeedbackData {
  content: string;
  email?: string;
}
