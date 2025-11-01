import { apiService } from './apiService';
import { API_ENDPOINTS } from '../config/api';

class ScheduleService {
  /**
   * Lấy lịch học của sinh viên
   * @returns {Promise<Object>} Lịch học của sinh viên
   */
  async getMySchedule() {
    try {
      const response = await apiService.get(API_ENDPOINTS.MY_SCHEDULE);
      const rawData = response.schedule || [];

      // Chuẩn hóa dữ liệu để tương thích với SchedulePage.jsx
      const normalizedData = rawData.map((item, index) => {
        // ƯU TIÊN: Lấy trực tiếp từ backend (đã parse sẵn)
        let dayOfWeek = item.dayOfWeek;
        let startTime = item.startTime;
        let endTime = item.endTime;
        
        // Nếu có schedule object, lấy từ đó
        if (!dayOfWeek && item.schedule && typeof item.schedule === 'object') {
          dayOfWeek = item.schedule.dayOfWeek;
          startTime = item.schedule.startTime || startTime;
          endTime = item.schedule.endTime || endTime;
        }
        
        // CHỈ parse từ datetime nếu CHƯA có dayOfWeek từ backend
        if (!dayOfWeek && (item.schedule_datetime || (typeof item.schedule === 'string' && item.schedule))) {
          try {
            const scheduleStr = item.schedule_datetime || item.schedule;
            const scheduleDate = new Date(scheduleStr);
            const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
            dayOfWeek = days[scheduleDate.getDay()];
            
            if (!startTime) {
              const hours = scheduleDate.getHours().toString().padStart(2, '0');
              const minutes = scheduleDate.getMinutes().toString().padStart(2, '0');
              startTime = `${hours}:${minutes}`;
            }
            
            if (!endTime) {
              const endDate = new Date(scheduleDate);
              endDate.setHours(endDate.getHours() + 2);
              const endHours = endDate.getHours().toString().padStart(2, '0');
              const endMinutes = endDate.getMinutes().toString().padStart(2, '0');
              endTime = `${endHours}:${endMinutes}`;
            }
          } catch (e) {
            console.warn('[ScheduleService] Error parsing schedule:', e);
          }
        }
        
        return {
          courseClassId: item.courseClassId || `UNKNOWN-${index}`,
          courseCode: item.courseCode || 'N/A',
          courseName: item.courseName || 'Chưa rõ tên môn học',
          subject: item.subject || 'Chưa rõ môn học',
          credits: item.credits ?? 0,
          room: item.room || 'Chưa có phòng',
          teacher: item.teacher || 'Chưa có giảng viên',
          dayOfWeek: dayOfWeek,
          startTime: startTime,
          endTime: endTime,
        };
      });

      return {
        success: true,
        data: normalizedData,
      };
    } catch (error) {
      console.error('Get my schedule error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy lịch học',
        data: [],
      };
    }
  }

  /**
   * Lấy danh sách đăng ký của sinh viên
   */
  /**
 * Lấy danh sách đăng ký của sinh viên
 */
  async getMyRegistrations() {
    try {
      const response = await apiService.get(API_ENDPOINTS.MY_REGISTRATIONS);
      const rawData = response.registrations || [];

      // 🔹 Chuẩn hóa dữ liệu để tương thích với SchedulePage.jsx
      const normalizedData = rawData.map((item, index) => ({
        registrationId: item.registrationId || `REG-${index}`,
        status: item.status || 'registered',
        registrationDate: item.registrationDate || 'N/A',
        grade: item.grade ?? null,

        // Mô phỏng lại cấu trúc mà UI đang mong đợi
        courseClass: {
          courseClassId: item.courseClassId || 'UNKNOWN',
          courseCode: item.courseCode || 'N/A',
          courseName: item.courseName || 'Chưa rõ tên môn học',
          subject: item.subject || 'Chưa rõ môn học',
          credits: item.credits ?? 0,
        },
        semester: {
          semesterName: item.semester || 'Chưa rõ học kỳ',
        },
      }));

      return {
        success: true,
        data: normalizedData,
      };
    } catch (error) {
      console.error('Get my registrations error:', error);
      return {
        success: false,
        message: error.message || 'Có lỗi xảy ra khi lấy danh sách đăng ký',
        data: [],
      };
    }
  }
}

export const scheduleService = new ScheduleService();

