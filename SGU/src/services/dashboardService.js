import { apiService } from './apiService';
import { API_ENDPOINTS } from '../config/api';

class DashboardService {
  /**
   * Lấy thông tin dashboard của student
   * @returns {Promise<Object>} Thông tin dashboard
   */
  async getStudentDashboard() {
    try {
      const response = await apiService.get(API_ENDPOINTS.STUDENT_DASHBOARD);
      return {
        success: true,
        data: response
      };
    } catch (error) {
      console.error('Get student dashboard error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi tải dashboard'
      };
    }
  }
}

export const dashboardService = new DashboardService();
