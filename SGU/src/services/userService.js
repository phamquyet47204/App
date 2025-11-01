import { API_ENDPOINTS } from '../config/api';
import { apiService } from './apiService';

class UserService {
  // Lấy thông tin profile của sinh viên
  async getStudentProfile() {
    try {
      const response = await apiService.get(API_ENDPOINTS.STUDENT_PROFILE);
      const studentData = response.student || response || null;
      return {
        success: !!studentData,
        data: studentData
      };
    } catch (error) {
      console.error('Get student profile error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy thông tin profile',
        data: null
      };
    }
  }

  // Cập nhật thông tin profile của sinh viên
  async updateProfile(profileData) {
    try {
      const response = await apiService.put(API_ENDPOINTS.UPDATE_PROFILE, profileData);
      return {
        success: true,
        message: response.message || 'Cập nhật thông tin thành công'
      };
    } catch (error) {
      console.error('Update profile error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi cập nhật thông tin'
      };
    }
  }

  // Cập nhật thông tin người dùng (legacy method)
  async updateUser(userId, userData) {
    try {
      const response = await apiService.put(API_ENDPOINTS.UPDATE_USER(userId), userData);
      return {
        success: true,
        message: response.message || 'Cập nhật thông tin thành công'
      };
    } catch (error) {
      console.error('Update user error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi cập nhật thông tin'
      };
    }
  }
}

export const userService = new UserService();
