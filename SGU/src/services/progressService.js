import { API_ENDPOINTS } from '../config/api';
import { apiService } from './apiService';
import { AuthStorage } from '../types/user'; // 👈 Thêm dòng này

class ProgressService {
  // Lấy username từ localStorage
  getUsername() {
    const user = AuthStorage.getCurrentUser();
    return user?.username || null;
  }

  // ✅ Lấy danh sách khóa học có thể đăng ký
  async getAvailableCourses() {
    const username = this.getUsername(); // 👈 Tự động lấy username
    if (!username) {
      return { success: false, message: 'Không tìm thấy username trong localStorage', data: [] };
    }

    try {
      const response = await apiService.get(API_ENDPOINTS.AVAILABLE_COURSES(username));
      return {
        success: true,
        data: response.courses || []
      };
    } catch (error) {
      console.error('Get available courses error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách khóa học',
        data: []
      };
    }
  }

  // ✅ Kiểm tra điều kiện tiên quyết
  // async checkPrerequisites(subjectId) {
  //   const username = this.getUsername();
  //   if (!username) {
  //     return { success: false, message: 'Không tìm thấy username trong localStorage', data: null };
  //   }

  //   try {
  //     const response = await apiService.post(API_ENDPOINTS.CHECK_PREREQUISITES, {
  //       studentId: username,
  //       subjectId
  //     });
  //     return {
  //       success: true,
  //       data: {
  //         canRegister: response.canRegister,
  //         missingPrerequisites: response.missingPrerequisites || []
  //       }
  //     };
  //   } catch (error) {
  //     console.error('Check prerequisites error:', error);
  //     return {
  //       success: false,
  //       message: error.message || 'Có lỗi xảy ra khi kiểm tra điều kiện tiên quyết',
  //       data: null
  //     };
  //   }
  // }

  // ✅ Lấy thông tin học phí
  async getTuitionFees() {
    try {
      const response = await apiService.get(API_ENDPOINTS.TUITION_FEES);
      return {
        success: true,
        data: response.tuition_fees || []
      };
    } catch (error) {
      console.error('Get tuition fees error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy thông tin học phí',
        data: []
      };
    }
  }

  // ✅ Lấy danh sách lớp học đã hoàn thành
  async getCompletedCourses() {
    try {
      const response = await apiService.get(API_ENDPOINTS.MY_COMPLETED_COURSES);
      return {
        success: true,
        data: response.completedCourses || [],
        total: response.total || 0,
        totalCredits: response.totalCredits || 0
      };
    } catch (error) {
      console.error('Get completed courses error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách lớp học đã hoàn thành',
        data: [],
        total: 0,
        totalCredits: 0
      };
    }
  }
}

export const progressService = new ProgressService();
