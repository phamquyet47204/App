// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  TIMEOUT: 10000
};

// API Endpoints
export const API_ENDPOINTS = {
  // Authentication APIs
  LOGIN: `${API_CONFIG.BASE_URL}/auth/student/login/`,
  LOGOUT: `${API_CONFIG.BASE_URL}/auth/logout/`,
  CHANGE_PASSWORD: `${API_CONFIG.BASE_URL}/auth/change-password/`,
  CHECK_SESSION: `${API_CONFIG.BASE_URL}/auth/check-session/`,
  
  // Dashboard API
  STUDENT_DASHBOARD: `${API_CONFIG.BASE_URL}/student/dashboard/`,
  
  // Grades APIs
  MY_GRADES: `${API_CONFIG.BASE_URL}/student/my-grades/`,
  CALCULATE_GPA: `${API_CONFIG.BASE_URL}/services/grades/calculate-gpa/`,
  
  // Course Registration APIs
  AVAILABLE_COURSES: (username) => `${API_CONFIG.BASE_URL}/services/registration/available-courses/${username}/`,
  CHECK_PREREQUISITES: `${API_CONFIG.BASE_URL}/services/registration/check-prerequisites/`,
  CHECK_SCHEDULE_CONFLICT: `${API_CONFIG.BASE_URL}/services/registration/check-schedule-conflict/`,
  CREATE_REGISTRATION: `${API_CONFIG.BASE_URL}/crud/registrations/create/`,
  
  // Schedule APIs
  MY_SCHEDULE: `${API_CONFIG.BASE_URL}/student/my-schedule/`,
  MY_REGISTRATIONS: `${API_CONFIG.BASE_URL}/student/my-registrations/`,
  
  // Document Request APIs
  DOCUMENT_REQUESTS: `${API_CONFIG.BASE_URL}/crud/document-requests/`,
  CREATE_DOCUMENT_REQUEST: `${API_CONFIG.BASE_URL}/crud/document-requests/create/`,
  MY_DOCUMENT_REQUESTS: `${API_CONFIG.BASE_URL}/student/my-document-requests/`,
  DOCUMENT_TYPES: `${API_CONFIG.BASE_URL}/crud/document-types/`,
  
  // Tuition Fees APIs
  MY_TUITION_FEES: `${API_CONFIG.BASE_URL}/student/my-tuition-fees/`,
  
  // Notification APIs
  UNREAD_NOTIFICATIONS: `${API_CONFIG.BASE_URL}/services/notifications/unread/`,
  MARK_NOTIFICATION_READ: (notificationId) => `${API_CONFIG.BASE_URL}/services/notifications/${notificationId}/mark-read/`,
  MY_NOTIFICATIONS: `${API_CONFIG.BASE_URL}/student/my-notifications/`,
  
  // Profile Management APIs
  STUDENT_PROFILE: `${API_CONFIG.BASE_URL}/student/profile/`,
  UPDATE_PROFILE: `${API_CONFIG.BASE_URL}/student/profile/update/`,
  
  // Read-only Information APIs
  DEPARTMENTS: `${API_CONFIG.BASE_URL}/crud/departments/`,
  MAJORS: `${API_CONFIG.BASE_URL}/crud/majors/`,
  SUBJECTS: `${API_CONFIG.BASE_URL}/crud/subjects/`,
  COURSE_CLASSES: `${API_CONFIG.BASE_URL}/crud/course-classes/`,
  SEMESTERS: `${API_CONFIG.BASE_URL}/crud/semesters/`,
  
  // Legacy endpoints (keeping for backward compatibility)
  CLASSES: `${API_CONFIG.BASE_URL}/crud/course-classes/`,
  UPDATE_USER: (userId) => `${API_CONFIG.BASE_URL}/crud/users/${userId}/update/`,
  TUITION_FEES: `${API_CONFIG.BASE_URL}/crud/tuition-fees/`
};
