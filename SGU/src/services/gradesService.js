import { API_ENDPOINTS } from '../config/api';
import { apiService } from './apiService';

class GradesService {
  // Lấy danh sách điểm của sinh viên
  async getMyGrades() {
    try {
      console.log('🔍 Calling API:', API_ENDPOINTS.MY_GRADES);
      const response = await apiService.get(API_ENDPOINTS.MY_GRADES);
      console.log('🔍 API Response:', response);
      console.log('🔍 Response type:', typeof response);
      console.log('🔍 Response keys:', Object.keys(response || {}));
      
      // Kiểm tra nếu response có message thay vì grades (endpoint cũ)
      if (response.message && !response.grades) {
        console.error('❌ Wrong endpoint response - got message instead of grades data:', response.message);
        return {
          success: false,
          message: 'API endpoint trả về dữ liệu sai. Vui lòng liên hệ quản trị viên.',
          data: {
            grades: [],
            gpa: 0,
            totalCredits: 0,
            totalPassed: 0,
            totalGrades: 0
          }
        };
      }
      
      console.log('🔍 Grades in response:', response.grades);
      console.log('🔍 Grades count:', response.grades?.length || 0);
      console.log('🔍 GPA in response:', response.gpa);
      
      return {
        success: true,
        data: {
          grades: response.grades || [],
          gpa: response.gpa || 0,
          totalCredits: response.totalCredits || 0,
          totalPassed: response.totalPassed || 0,
          totalGrades: response.totalGrades || 0
        }
      };
    } catch (error) {
      console.error('❌ Get grades error:', error);
      console.error('❌ Error response:', error.response);
      console.error('❌ Error status:', error.status);
      console.error('❌ Error data:', error.data);
      return {
        success: false,
        message: error.message || error.data?.error || 'Có lỗi xảy ra khi lấy danh sách điểm',
        data: {
          grades: [],
          gpa: 0,
          totalCredits: 0,
          totalPassed: 0,
          totalGrades: 0
        }
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
