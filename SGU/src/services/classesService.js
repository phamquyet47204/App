import { API_ENDPOINTS } from '../config/api';
import { apiService } from './apiService';

class ClassesService {
  // Lấy danh sách lớp học
  async getClasses() {
    try {
      console.log('📚 Fetching classes from:', API_ENDPOINTS.CLASSES);
      const response = await apiService.get(API_ENDPOINTS.CLASSES);
      console.log('📚 Classes response:', response);
      return {
        success: true,
        data: response.course_classes || []
      };
    } catch (error) {
      console.error('❌ Get classes error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách lớp học',
        data: []
      };
    }
  }
}

export const classesService = new ClassesService();
