import { API_ENDPOINTS } from '../config/api';
import { apiService } from './apiService';

class GradesService {
  // Lấy danh sách điểm của sinh viên
  async getMyGrades() {
    try {
      const response = await apiService.get(API_ENDPOINTS.MY_GRADES);
      return {
        success: true,
        data: response.grades || []
      };
    } catch (error) {
      console.error('Get grades error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách điểm',
        data: []
      };
    }
  }

  // Tính toán GPA
  async calculateGPA(studentId) {
    try {
      const response = await apiService.post(API_ENDPOINTS.CALCULATE_GPA, {
        studentId
      });
      return {
        success: true,
        data: {
          gpa: response.gpa,
          totalCredits: response.totalCredits
        }
      };
    } catch (error) {
      console.error('Calculate GPA error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi tính toán GPA',
        data: null
      };
    }
  }
}

export const gradesService = new GradesService();
