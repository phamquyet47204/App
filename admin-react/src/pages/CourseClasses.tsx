import React, { useState, useEffect } from 'react';
import { Calendar, Plus, Search, Pencil, Trash2 } from 'lucide-react';
import api from '../services/api';

interface CourseClass {
  courseClassId: string;
  courseCode: string;
  courseName: string;
  subject: string;
  subjectId?: string;
  teacher: string;
  teacherId?: string;
  semester: string;
  semesterId?: string;
  room: string;
  maxStudents: number;
  currentStudents: number;
}

interface Subject {
  subjectId: string;
  subjectName: string;
}

interface Teacher {
  id: number;
  teacherId: string;
  full_name: string;
}

interface Semester {
  semesterId: string;
  semesterName: string;
}

const CourseClasses: React.FC = () => {
  const [courseClasses, setCourseClasses] = useState<CourseClass[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [semesters, setSemesters] = useState<Semester[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingClass, setEditingClass] = useState<CourseClass | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [formData, setFormData] = useState({
    courseClassId: '',
    courseCode: '',
    courseName: '',
    subjectId: '',
    teacherId: '',
    semesterId: '',
    room: '',
    maxStudents: 30
  });

  useEffect(() => {
    const loadData = async () => {
      await Promise.all([fetchSubjects(), fetchTeachers(), fetchSemesters()]);
      await fetchCourseClasses();
    };
    loadData();
  }, []);

  const fetchCourseClasses = async () => {
    try {
      const response = await api.get('/crud/course-classes/');
      const classes = response.data.course_classes || [];
      
      const enrichedClasses = classes.map((cls: any) => {
        const subject = subjects.find(s => s.subjectName === cls.subject);
        const teacher = teachers.find(t => t.full_name === cls.teacher);
        const semester = semesters.find(s => s.semesterName === cls.semester);
        
        return {
          ...cls,
          subjectId: subject?.subjectId,
          teacherId: teacher?.teacherId,
          semesterId: semester?.semesterId
        };
      });
      
      setCourseClasses(enrichedClasses);
    } catch (error) {
      console.error('Error fetching course classes:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSubjects = async () => {
    try {
      const response = await api.get('/crud/subjects/');
      setSubjects(response.data.subjects || []);
    } catch (error) {
      console.error('Error fetching subjects:', error);
    }
  };

  const fetchTeachers = async () => {
    try {
      const response = await api.get('/crud/teachers/');
      const teachersData = (response.data.teachers || []).map((teacher: any) => ({
        id: teacher.teacherId,
        teacherId: teacher.teacherId,
        full_name: teacher.full_name
      }));
      setTeachers(teachersData);
    } catch (error) {
      console.error('Error fetching teachers:', error);
    }
  };

  const fetchSemesters = async () => {
    try {
      const response = await api.get('/crud/semesters/');
      setSemesters(response.data.semesters || []);
    } catch (error) {
      console.error('Error fetching semesters:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload: any = {
        courseClassId: formData.courseClassId,
        courseCode: formData.courseCode,
        courseName: formData.courseName,
        subjectId: formData.subjectId,
        semesterId: formData.semesterId,
        room: formData.room,
        maxStudents: formData.maxStudents
      };
      
      if (formData.teacherId && formData.teacherId.trim() !== '') {
        payload.teacherId = formData.teacherId;
      }
      
      console.log('Payload being sent:', payload);
      
      if (editingClass) {
        await api.put(`/crud/course-classes/${editingClass.courseClassId}/update/`, payload);
      } else {
        await api.post('/crud/course-classes/create/', payload);
      }
      fetchCourseClasses();
      resetForm();
    } catch (error) {
      console.error('Error saving course class:', error);
      alert('Có lỗi xảy ra khi lưu thông tin lớp học');
    }
  };

  const handleEdit = (courseClass: CourseClass) => {
    setEditingClass(courseClass);
    
    const subject = subjects.find(s => s.subjectName === courseClass.subject);
    const teacher = teachers.find(t => t.full_name === courseClass.teacher);
    const semester = semesters.find(s => s.semesterName === courseClass.semester);
    
    setFormData({
      courseClassId: courseClass.courseClassId,
      courseCode: courseClass.courseCode,
      courseName: courseClass.courseName,
      subjectId: subject?.subjectId || '',
      teacherId: teacher?.teacherId || '',
      semesterId: semester?.semesterId || '',
      room: courseClass.room,
      maxStudents: courseClass.maxStudents
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa lớp học này?')) {
      try {
        await api.delete(`/crud/course-classes/${id}/delete/`);
        fetchCourseClasses();
      } catch (error) {
        console.error('Error deleting course class:', error);
        alert('Có lỗi xảy ra khi xóa lớp học');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      courseClassId: '',
      courseCode: '',
      courseName: '',
      subjectId: '',
      teacherId: '',
      semesterId: '',
      room: '',
      maxStudents: 30
    });
    setEditingClass(null);
    setShowForm(false);
  };

  const filteredClasses = courseClasses.filter(cls =>
    cls.courseName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cls.courseCode.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cls.subject.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <div className="page-header">
        <h1>Quản lý Lớp Học</h1>
        <p>Danh sách và thông tin lớp học</p>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3>Danh sách Lớp Học ({filteredClasses.length})</h3>
          <button 
            className="btn btn-primary" 
            onClick={() => setShowForm(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Plus size={16} />
            Thêm Lớp Học
          </button>
        </div>

        <div style={{ marginBottom: '1rem', position: 'relative' }}>
          <Search size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#64748b' }} />
          <input
            type="text"
            placeholder="Tìm kiếm lớp học..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              padding: '0.75rem 0.75rem 0.75rem 2.5rem',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '1rem'
            }}
          />
        </div>

        {filteredClasses.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Mã lớp</th>
                <th>Tên lớp</th>
                <th>Môn học</th>
                <th>Giảng viên</th>
                <th>Học kỳ</th>
                <th>Phòng</th>
                <th>Sinh viên</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {filteredClasses.map((cls) => (
                <tr key={cls.courseClassId}>
                  <td>{cls.courseCode}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Calendar size={16} color="#64748b" />
                      {cls.courseName}
                    </div>
                  </td>
                  <td>{cls.subject}</td>
                  <td>{cls.teacher || 'Chưa phân công'}</td>
                  <td>{cls.semester}</td>
                  <td>{cls.room}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                      <span style={{ fontWeight: 'bold', color: '#2563eb' }}>{cls.currentStudents}</span>
                      <span style={{ color: '#9ca3af' }}>/</span>
                      <span style={{ color: '#6b7280' }}>{cls.maxStudents}</span>
                    </div>
                  </td>
                  <td>
                    <button 
                      onClick={() => handleEdit(cls)}
                      style={{ 
                        marginRight: '0.5rem', 
                        padding: '0.25rem 0.5rem', 
                        fontSize: '0.875rem',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.25rem'
                      }}
                    >
                      <Pencil size={14} />
                      Sửa
                    </button>
                    <button 
                      onClick={() => handleDelete(cls.courseClassId)}
                      style={{ 
                        padding: '0.25rem 0.5rem', 
                        fontSize: '0.875rem', 
                        color: '#dc2626',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.25rem'
                      }}
                    >
                      <Trash2 size={14} />
                      Xóa
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
            <Calendar size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            <p>Chưa có lớp học nào trong hệ thống</p>
            <p>Nhấn "Thêm Lớp Học" để tạo lớp học mới</p>
          </div>
        )}
      </div>

      {showForm && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '8px',
            padding: '2rem',
            width: '100%',
            maxWidth: '500px',
            maxHeight: '90vh',
            overflow: 'auto'
          }}>
            <h3 style={{ marginBottom: '1.5rem' }}>
              {editingClass ? 'Sửa thông tin lớp học' : 'Thêm lớp học mới'}
            </h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Mã lớp học *</label>
                <input
                  type="text"
                  value={formData.courseClassId}
                  onChange={(e) => setFormData({...formData, courseClassId: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  disabled={!!editingClass}
                />
              </div>
              
              <div className="form-group">
                <label>Mã khóa học *</label>
                <input
                  type="text"
                  value={formData.courseCode}
                  onChange={(e) => setFormData({...formData, courseCode: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Tên khóa học *</label>
                <input
                  type="text"
                  value={formData.courseName}
                  onChange={(e) => setFormData({...formData, courseName: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Môn học *</label>
                <select
                  value={formData.subjectId}
                  onChange={(e) => setFormData({...formData, subjectId: e.target.value})}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  <option value="">Chọn môn học</option>
                  {subjects.map(subject => (
                    <option key={subject.subjectId} value={subject.subjectId}>{subject.subjectName}</option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label>Giảng viên</label>
                <select
                  value={formData.teacherId}
                  onChange={(e) => setFormData({...formData, teacherId: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  <option value="">Chọn giảng viên</option>
                  {teachers.map(teacher => (
                    <option key={teacher.id} value={teacher.teacherId}>{teacher.full_name}</option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label>Học kỳ *</label>
                <select
                  value={formData.semesterId}
                  onChange={(e) => setFormData({...formData, semesterId: e.target.value})}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  <option value="">Chọn học kỳ</option>
                  {semesters.map(semester => (
                    <option key={semester.semesterId} value={semester.semesterId}>{semester.semesterName}</option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label>Phòng học *</label>
                <input
                  type="text"
                  value={formData.room}
                  onChange={(e) => setFormData({...formData, room: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Số sinh viên tối đa *</label>
                <input
                  type="number"
                  value={formData.maxStudents}
                  onChange={(e) => setFormData({...formData, maxStudents: parseInt(e.target.value)})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                  {editingClass ? 'Cập nhật' : 'Thêm mới'}
                </button>
                <button 
                  type="button" 
                  onClick={resetForm}
                  style={{ 
                    flex: 1, 
                    padding: '0.75rem', 
                    border: '1px solid #d1d5db', 
                    borderRadius: '6px',
                    background: 'white',
                    cursor: 'pointer'
                  }}
                >
                  Hủy
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default CourseClasses;