import { API_ENDPOINTS } from '../config/api';
import { apiService } from './apiService';

// 💡 Các hàm tiện ích đặt ngoài class
function mapNotificationType(type) {
  switch (type) {
    case 'success':
    case 'info':
    case 'warning':
    case 'error':
      return type;
    case 'administrative':
      return 'warning';
    case 'general':
      return 'info';
    default:
      return 'info';
  }
}

function mapCategory(type) {
  switch (type) {
    case 'exam':
    case 'grade':
    case 'schedule':
    case 'document':
    case 'payment':
      return type;
    case 'administrative':
      return 'document';
    case 'general':
      return 'info';
    default:
      return 'other';
  }
}

function normalizePriority(priority) {
  if (!priority) return 'normal';
  if (priority <= 1) return 'low';
  if (priority === 2) return 'normal';
  if (priority >= 3) return 'high';
  return 'normal';
}

class NotificationsService {
  // Lấy danh sách thông báo chưa đọc
  async getUnreadNotifications() {
    try {
      const response = await apiService.get(API_ENDPOINTS.UNREAD_NOTIFICATIONS);
      return {
        success: true,
        data: response.notifications || []
      };
    } catch (error) {
      console.error('Get unread notifications error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách thông báo',
        data: []
      };
    }
  }

  // Đánh dấu thông báo đã đọc
  async markNotificationAsRead(notificationId) {
    try {
      const response = await apiService.post(API_ENDPOINTS.MARK_NOTIFICATION_READ(notificationId));
      return {
        success: true,
        message: response.message || 'Đánh dấu thông báo đã đọc thành công'
      };
    } catch (error) {
      console.error('Mark notification as read error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi đánh dấu thông báo đã đọc'
      };
    }
  }

  // Lấy tất cả thông báo của sinh viên
  async getMyNotifications() {
    try {
      const response = await apiService.get(API_ENDPOINTS.MY_NOTIFICATIONS);
      const rawList = response?.notifications || [];

      const normalized = rawList.map((item) => ({
        id: item.notificationId || item.id || null,
        title: item.title || 'Không có tiêu đề',
        message: item.content || item.message || '',
        type: mapNotificationType(item.notificationType),
        category: mapCategory(item.notificationType),
        priority: normalizePriority(item.priority),
        isRead: item.isRead || !!item.readAt,
        createdAt: item.createdAt || item.deliveredAt || item.scheduledAt || null,
        deliveredAt: item.deliveredAt || null,
        raw: item
      }));

      return {
        success: true,
        data: normalized
      };
    } catch (error) {
      console.error('Get my notifications error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách thông báo',
        data: []
      };
    }
  }
}

export const notificationsService = new NotificationsService();
