import { API_ENDPOINTS } from '../config/api';
import { apiService } from './apiService';

class DocumentsService {
  // Lấy danh sách yêu cầu tài liệu
  async getDocumentRequests() {
    try {
      const response = await apiService.get(API_ENDPOINTS.DOCUMENT_REQUESTS);
      return {
        success: true,
        data: response.document_requests || []
      };
    } catch (error) {
      console.error('Get document requests error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách yêu cầu tài liệu',
        data: []
      };
    }
  }

  // Tạo yêu cầu tài liệu mới (Student self-service endpoint)
  async createDocumentRequest(requestData) {
    try {
      // Dùng endpoint /student/my-document-requests/ (POST) - tự sinh requestId, không cần gửi requestId
      const response = await apiService.post(API_ENDPOINTS.MY_DOCUMENT_REQUESTS, requestData);
      
      // Kiểm tra nếu response là "already_requested"
      if (response.message === 'already_requested') {
        return {
          success: false,
          message: 'already_requested',
          data: {
            requestId: response.requestId,
            status: response.status
          }
        };
      }
      
      return {
        success: true,
        message: response.message || 'Tạo yêu cầu tài liệu thành công',
        data: {
          requestId: response.requestId || response.id,
          queuePosition: response.queuePosition,
          status: response.status
        }
      };
    } catch (error) {
      console.error('Create document request error:', error);
      // Xử lý trường hợp đã yêu cầu rồi từ response body
      if (error.response && error.response.data && error.response.data.message === 'already_requested') {
        return {
          success: false,
          message: 'already_requested'
        };
      }
      // Kiểm tra error message
      if (error.message && error.message.includes('already_requested')) {
        return {
          success: false,
          message: 'already_requested'
        };
      }
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi tạo yêu cầu tài liệu'
      };
    }
  }

  // Lấy yêu cầu tài liệu của sinh viên
  async getMyDocumentRequests() {
    try {
      const response = await apiService.get(API_ENDPOINTS.MY_DOCUMENT_REQUESTS);
      return {
        success: true,
        data: response.documentRequests || []
      };
    } catch (error) {
      console.error('Get my document requests error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy yêu cầu tài liệu',
        data: []
      };
    }
  }

  // Lấy danh sách loại tài liệu có thể yêu cầu
  async getDocumentTypes() {
    try {
      const response = await apiService.get(API_ENDPOINTS.DOCUMENT_TYPES);
      return {
        success: true,
        data: response.documentTypes || []
      };
    } catch (error) {
      console.error('Get document types error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách loại tài liệu',
        data: []
      };
    }
  }
}

export const documentsService = new DocumentsService();
