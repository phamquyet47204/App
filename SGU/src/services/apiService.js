import { API_CONFIG } from '../config/api';
import { authService } from './authService';

class ApiService {
  async request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_CONFIG.BASE_URL}${endpoint}`;
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...authService.getAuthHeaders(),
        ...options.headers
      },
      ...options
    };

    console.log('🚀 Making API request to:', url);
    console.log('🔧 Request options:', defaultOptions);

    try {
      const response = await fetch(url, defaultOptions);
      console.log('📡 Response status:', response.status);
      console.log('📡 Response ok:', response.ok);

      // 🧩 Parse JSON nếu có thể
      let data = null;
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        data = await response.json().catch(() => null);
      } else {
        data = await response.text().catch(() => null);
      }

      // ⚠️ Kiểm tra lỗi Authentication
      if (
        (data && data.error === 'Authentication required') ||
        response.status === 401 ||
        response.status === 403
      ) {
        console.warn('⚠️ Session expired or unauthorized. Auto logout triggered.');
        await authService.logout();

        // 👉 Chuyển hướng về trang login
        window.location.href = '/';
        return Promise.reject(new Error('Authentication required - auto logout'));
      }

      // ❌ Nếu không ok thì ném lỗi khác
      if (!response.ok) {
        console.error('❌ API Error:', data);
        const error = new Error(
          (data && (data.error || data.message)) || `HTTP error! status: ${response.status}`
        );
        error.response = response;
        error.status = response.status;
        error.data = data;
        throw error;
      }

      console.log('✅ API Response data:', data);
      return data;
    } catch (error) {
      console.error('❌ API request error:', error);
      throw error;
    }
  }

  // GET
  async get(endpoint, options = {}) {
    return this.request(endpoint, {
      method: 'GET',
      ...options
    });
  }

  // POST
  async post(endpoint, data = null, options = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
      ...options
    });
  }

  // PUT
  async put(endpoint, data = null, options = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
      ...options
    });
  }

  // DELETE
  async delete(endpoint, options = {}) {
    return this.request(endpoint, {
      method: 'DELETE',
      ...options
    });
  }
}

export const apiService = new ApiService();
