import { apiService } from './apiService';
import { API_ENDPOINTS } from '../config/api';

class TuitionService {
  /**
   * Lấy thông tin học phí của sinh viên
   * @returns {Promise<Object>} Thông tin học phí
   */
  async getMyTuitionFees() {
    try {
      const response = await apiService.get(API_ENDPOINTS.MY_TUITION_FEES);
      return {
        success: true,
        data: response.tuitionFees || []
      };
    } catch (error) {
      console.error('Get my tuition fees error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy thông tin học phí',
        data: []
      };
    }
  }
}

export const tuitionService = new TuitionService();
