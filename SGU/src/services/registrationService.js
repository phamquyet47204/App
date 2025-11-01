import { apiService } from './apiService';
import { API_ENDPOINTS } from '../config/api';
import { AuthStorage } from '../types/user'; // Thêm dòng này

class RegistrationService {
  getUsername() {
    const user = AuthStorage.getCurrentUser();
    console.log('🔍 getCurrentUser() result:', user);
    console.log('🔍 Username from user:', user?.username);
    console.log('🔍 Is logged in:', AuthStorage.isLoggedIn());
    
    // Try multiple ways to get username
    if (user) {
      return user.username || user.userName || user.user_name || null;
    }
    
    // Fallback: try to get from localStorage directly
    try {
      const userData = localStorage.getItem('sgu_user');
      if (userData) {
        const parsed = JSON.parse(userData);
        console.log('🔍 Parsed userData:', parsed);
        return parsed.username || parsed.userName || parsed.user_name || null;
      }
    } catch (e) {
      console.error('Error parsing userData:', e);
    }
    
    return null;
  }

  async getAvailableCourses() {
    const username = this.getUsername();
    console.log('🔍 Final username:', username);
    
    if (!username) {
      console.error('❌ No username found');
      console.error('❌ LocalStorage sgu_user:', localStorage.getItem('sgu_user'));
      console.error('❌ Please ensure you are logged in');
      return { success: false, message: 'Vui lòng đăng nhập để xem môn học có thể đăng ký', data: { courses: [] } };
    }

    try {
      const endpoint = API_ENDPOINTS.AVAILABLE_COURSES(username);
      console.log('🔗 Calling endpoint:', endpoint);
      const response = await apiService.get(endpoint);
      console.log('✅ API Response:', response);
      
      // Response có thể là { courses: [], semester: {}, total: 0 } hoặc chỉ { courses: [] }
      const result = { 
        success: true, 
        data: response || { courses: [] } 
      };
      console.log('✅ Parsed result:', result);
      return result;
    } catch (error) {
      console.error('❌ Get available courses error:', error);
      console.error('❌ Error details:', error.response || error.message);
      return { success: false, message: error.message || 'Lỗi không xác định', data: { courses: [] } };
    }
  }

  async checkPrerequisites(subjectId) {
    // Backend tự động lấy student từ user hiện tại nếu không gửi studentId
    try {
      const response = await apiService.post(API_ENDPOINTS.CHECK_PREREQUISITES, {
        subjectId
        // Không cần gửi studentId - backend tự lấy từ user hiện tại
      });
      return { success: true, data: response };
    } catch (error) {
      console.error('Check prerequisites error:', error);
      // Xử lý 404
      if (error.response && error.response.status === 404) {
        return { success: false, message: 'Không tìm thấy thông tin. Vui lòng đăng nhập lại.', data: null };
      }
      return { success: false, message: error.message || 'Có lỗi xảy ra khi kiểm tra tiên quyết', data: null };
    }
  }

  async checkScheduleConflict(courseClassId) {
    // Backend tự động lấy student từ user hiện tại nếu không gửi studentId
    try {
      const response = await apiService.post(API_ENDPOINTS.CHECK_SCHEDULE_CONFLICT, {
        courseClassId
        // Không cần gửi studentId - backend tự lấy từ user hiện tại
      });
      return { success: true, data: response };
    } catch (error) {
      console.error('Check schedule conflict error:', error);
      // Xử lý 404
      if (error.response && error.response.status === 404) {
        return { success: false, message: 'Không tìm thấy thông tin. Vui lòng đăng nhập lại.', data: null };
      }
      return { success: false, message: error.message || 'Có lỗi xảy ra khi kiểm tra xung đột lịch học', data: null };
    }
  }

  async createRegistration(registrationData) {
    // Không cần gửi registrationId và studentId - backend tự sinh/tự lấy
    try {
      // Backend sẽ tự lấy student từ user hiện tại
      const response = await apiService.post(API_ENDPOINTS.CREATE_REGISTRATION, {
        courseClassId: registrationData.courseClassId,
        semesterId: registrationData.semesterId
      });
      return { success: true, data: response, message: response.message || 'Đăng ký môn học thành công' };
    } catch (error) {
      console.error('Create registration error:', error);
      // Xử lý error response
      const errorMessage = error.data?.error || error.data?.message || error.message || 'Có lỗi xảy ra khi đăng ký';
      return { success: false, message: errorMessage, data: null };
    }
  }
}

export const registrationService = new RegistrationService();
