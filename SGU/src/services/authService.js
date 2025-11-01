import { API_ENDPOINTS } from '../config/api';
import { AuthStorage } from '../types/user';

class AuthService {
  async login(username, password) {
    try {
      console.log('🔐 Attempting login with:', { username, password: '***' });
      console.log('🌐 API Endpoint:', API_ENDPOINTS.LOGIN);
      
      const response = await fetch(API_ENDPOINTS.LOGIN, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password
        })
      });
      
      console.log('📡 Response status:', response.status);
      console.log('📡 Response ok:', response.ok);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Đăng nhập thất bại');
      }

      const data = await response.json();
      console.log('✅ Login successful, data:', data);
      
      // Lưu thông tin user vào localStorage
      if (data.user) {
        AuthStorage.setCurrentUser(data.user);
        console.log('👤 User saved to localStorage');
      }
      
      // Lưu session key thay vì token
      if (data.session_key) {
        localStorage.setItem('sgu_session_key', data.session_key);
        console.log('🔑 Session key saved to localStorage');
      }

      return {
        success: true,
        message: data.message || 'Đăng nhập thành công',
        user: data.user,
        sessionKey: data.session_key
      };
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi đăng nhập'
      };
    }
  }

  async logout() {
    try {
      // Gọi API logout trước khi xóa local storage
      const response = await fetch(API_ENDPOINTS.LOGOUT, {
        method: 'POST',
        headers: this.getAuthHeaders()
      });

      if (!response.ok) {
        console.warn('Logout API call failed, but continuing with local logout');
      }

      // Xóa thông tin user và session key
      AuthStorage.logout();
      localStorage.removeItem('sgu_session_key');
      
      return {
        success: true,
        message: 'Đăng xuất thành công'
      };
    } catch (error) {
      console.error('Logout error:', error);
      // Vẫn xóa local storage ngay cả khi API call thất bại
      AuthStorage.logout();
      localStorage.removeItem('sgu_session_key');
      
      return {
        success: true,
        message: 'Đăng xuất thành công'
      };
    }
  }

  async changePassword(currentPassword, newPassword) {
    try {
      const response = await fetch(API_ENDPOINTS.CHANGE_PASSWORD, {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          currentPassword,
          newPassword
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Đổi mật khẩu thất bại');
      }

      const data = await response.json();
      return {
        success: true,
        message: data.message || 'Đổi mật khẩu thành công'
      };
    } catch (error) {
      console.error('Change password error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi đổi mật khẩu'
      };
    }
  }

  getSessionKey() {
    return localStorage.getItem('sgu_session_key');
  }

  isAuthenticated() {
    return AuthStorage.isLoggedIn() && this.getSessionKey() !== null;
  }

  async checkSession() {
    try {
      const response = await fetch(API_ENDPOINTS.CHECK_SESSION, {
        method: 'GET',
        headers: this.getAuthHeaders()
      });

      if (!response.ok) {
        // Session không hợp lệ, xóa thông tin local
        AuthStorage.logout();
        localStorage.removeItem('sgu_session_key');
        return {
          success: false,
          isValid: false,
          message: 'Session không hợp lệ'
        };
      }

      const data = await response.json();
      return {
        success: true,
        isValid: data.isValid,
        user: data.user,
        message: data.isValid ? 'Session hợp lệ' : 'Session không hợp lệ'
      };
    } catch (error) {
      console.error('Check session error:', error);
      return {
        success: false,
        isValid: false,
        message: 'Có lỗi xảy ra khi kiểm tra session'
      };
    }
  }

  getAuthHeaders() {
    const sessionKey = this.getSessionKey();
    return {
      'Content-Type': 'application/json',
      ...(sessionKey && { 
        'Authorization': `Session ${sessionKey}`,
        'X-Session-Key': sessionKey
      })
    };
  }
}

export const authService = new AuthService();
