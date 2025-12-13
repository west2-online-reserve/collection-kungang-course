import type { LoginData, RegisterData, AuthResponse, User, refreshTokenResponse ,SimpleProfileForm,FeedbackData} from '@/types/auth';


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const authAPI = {
  async login(loginData: LoginData): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginData),
    });


    if (response.status !== 200 && response.status !== 401 && response.status !== 400) {
      throw new Error('登录请求失败');
    }

    return await response.json();
  },

  async register(registerData: Omit<RegisterData, 'confirmPassword'>): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(registerData),
    });

    if (!response.ok) {
      throw new Error('注册请求失败');
    }

    return await response.json();
  },

  async verifyToken(token: string): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/auth/profile`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Token验证失败');
    }

    const data = await response.json();
    return data.data;
  },

  async refreshToken(Token: string): Promise<refreshTokenResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${Token}`,
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error('刷新Token失败');
    }
    const data = await response.json();
    return data;

  },
  async update_simple_profile(token: string, userData: SimpleProfileForm): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/auth/update_simple_profile`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    if (!response.ok) {
      throw new Error('更新用户资料失败');
    }
    return 'success';
  },
  async changePassword(token: string, newPassword: string): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/auth/change_password`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ password: newPassword }),
    });
    if (!response.ok) {
      throw new Error('修改密码失败');
    }
    return 'success';
  },
  async feedback(token: string, content: FeedbackData): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/api/feedback`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(content),
    });
    if (!response.ok) {
      throw new Error('提交反馈失败');
    }
    return 'success';
  }
};

