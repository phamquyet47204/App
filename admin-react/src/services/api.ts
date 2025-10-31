import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include session key
api.interceptors.request.use((config) => {
  const sessionKey = localStorage.getItem('session_key');
  if (sessionKey) {
    config.headers['Authorization'] = `Session ${sessionKey}`;
    config.headers['X-Session-Key'] = sessionKey;
  }
  return config;
});

// Auth API
export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/auth/admin/login/', { username, password }),
  logout: () => api.post('/auth/logout/'),
};

// CRUD APIs
export const crudAPI = {
  // Departments
  getDepartments: () => api.get('/crud/departments/'),
  createDepartment: (data: any) => api.post('/crud/departments/create/', data),
  updateDepartment: (id: string, data: any) => api.put(`/crud/departments/${id}/update/`, data),
  deleteDepartment: (id: string) => api.delete(`/crud/departments/${id}/delete/`),

  // Majors
  getMajors: () => api.get('/crud/majors/'),
  createMajor: (data: any) => api.post('/crud/majors/create/', data),
  updateMajor: (id: string, data: any) => api.put(`/crud/majors/${id}/update/`, data),
  deleteMajor: (id: string) => api.delete(`/crud/majors/${id}/delete/`),

  // Subjects
  getSubjects: () => api.get('/crud/subjects/'),
  createSubject: (data: any) => api.post('/crud/subjects/create/', data),
  updateSubject: (id: string, data: any) => api.put(`/crud/subjects/${id}/update/`, data),
  deleteSubject: (id: string) => api.delete(`/crud/subjects/${id}/delete/`),
};

// Dashboard API
export const dashboardAPI = {
  getStats: () => api.get('/admin/dashboard/'),
};

// Service APIs
export const serviceAPI = {
  // Grades
  calculateGPA: (studentId: string) => 
    api.post('/services/grades/calculate-gpa/', { studentId }),
  getClassStatistics: (classId: string) => 
    api.get(`/services/grades/class-statistics/${classId}/`),

  // Reports
  getStudentReport: (params?: any) => 
    api.get('/services/reports/students/', { params }),
  getGradeReport: (params?: any) => 
    api.get('/services/reports/grades/', { params }),
};

export default api;