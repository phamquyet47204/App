import { apiService } from './apiService';
import { API_ENDPOINTS } from '../config/api';

class ReadOnlyService {
  /**
   * Lấy danh sách khoa
   * @returns {Promise<Object>} Danh sách khoa
   */
  async getDepartments() {
    try {
      const response = await apiService.get(API_ENDPOINTS.DEPARTMENTS);
      return {
        success: true,
        data: response.departments || []
      };
    } catch (error) {
      console.error('Get departments error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách khoa',
        data: []
      };
    }
  }

  /**
   * Lấy danh sách ngành
   * @returns {Promise<Object>} Danh sách ngành
   */
  async getMajors() {
    try {
      const response = await apiService.get(API_ENDPOINTS.MAJORS);
      return {
        success: true,
        data: response.majors || []
      };
    } catch (error) {
      console.error('Get majors error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách ngành',
        data: []
      };
    }
  }

  /**
   * Lấy danh sách môn học
   * @returns {Promise<Object>} Danh sách môn học
   */
  async getSubjects() {
    try {
      const response = await apiService.get(API_ENDPOINTS.SUBJECTS);
      return {
        success: true,
        data: response.subjects || []
      };
    } catch (error) {
      console.error('Get subjects error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách môn học',
        data: []
      };
    }
  }

  /**
   * Lấy danh sách lớp học phần
   * @returns {Promise<Object>} Danh sách lớp học phần
   */
  async getCourseClasses() {
    try {
      const response = await apiService.get(API_ENDPOINTS.COURSE_CLASSES);
      return {
        success: true,
        data: response.course_classes || []
      };
    } catch (error) {
      console.error('Get course classes error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách lớp học phần',
        data: []
      };
    }
  }

  /**
   * Lấy danh sách học kỳ
   * @returns {Promise<Object>} Danh sách học kỳ
   */
  async getSemesters() {
    try {
      const response = await apiService.get(API_ENDPOINTS.SEMESTERS);
      return {
        success: true,
        data: response.semesters || []
      };
    } catch (error) {
      console.error('Get semesters error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách học kỳ',
        data: []
      };
    }
  }
}

export const readOnlyService = new ReadOnlyService();
