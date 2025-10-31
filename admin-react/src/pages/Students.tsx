import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { User, Edit, Trash2, Plus, Search } from 'lucide-react';

interface Student {
  id: string;
  username: string;
  email: string;
  full_name: string;
  phone?: string;
  address?: string;
  enrollmentYear?: string;
  status: string;
  created_at: string;
}

const Students: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingStudent, setEditingStudent] = useState<Student | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    full_name: '',
    phone: '',
    address: '',
    enrollmentYear: new Date().getFullYear().toString(),
    password: ''
  });

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const sessionKey = localStorage.getItem('session_key');
      const response = await axios.get('http://127.0.0.1:8000/api/crud/users/', {
        headers: {
          'Authorization': `Session ${sessionKey}`,
          'X-Session-Key': sessionKey
        }
      });
      const data = response.data.users || response.data;
      const studentData = Array.isArray(data) ? data.filter(user => user.user_type === 'student') : [];
      setStudents(studentData);
    } catch (error) {
      console.error('Error fetching students:', error);
      setStudents([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const sessionKey = localStorage.getItem('session_key');
      const config = {
        headers: {
          'Authorization': `Session ${sessionKey}`,
          'X-Session-Key': sessionKey
        }
      };

      if (editingStudent) {
        await axios.put(`http://127.0.0.1:8000/api/crud/users/${editingStudent.id}/update/`, {
          ...formData,
          user_type: 'student'
        }, config);
      } else {
        await axios.post('http://127.0.0.1:8000/api/crud/users/create/', {
          ...formData,
          user_type: 'student'
        }, config);
      }
      
      fetchStudents();
      resetForm();
    } catch (error) {
      console.error('Error saving student:', error);
      alert('Có lỗi xảy ra khi lưu thông tin sinh viên');
    }
  };

  const handleEdit = (student: Student) => {
    setEditingStudent(student);
    setFormData({
      username: student.username,
      email: student.email,
      full_name: student.full_name,
      phone: student.phone || '',
      address: student.address || '',
      enrollmentYear: student.enrollmentYear || new Date().getFullYear().toString(),
      password: ''
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa sinh viên này?')) {
      try {
        const sessionKey = localStorage.getItem('session_key');
        await axios.delete(`http://127.0.0.1:8000/api/crud/users/${id}/delete/`, {
          headers: {
            'Authorization': `Session ${sessionKey}`,
            'X-Session-Key': sessionKey
          }
        });
        fetchStudents();
      } catch (error) {
        console.error('Error deleting student:', error);
        alert('Có lỗi xảy ra khi xóa sinh viên');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      username: '',
      email: '',
      full_name: '',
      phone: '',
      address: '',
      enrollmentYear: new Date().getFullYear().toString(),
      password: ''
    });
    setEditingStudent(null);
    setShowForm(false);
  };

  const filteredStudents = students.filter(student =>
    student.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div>Đang tải...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Quản lý Sinh viên</h1>
        <p>Danh sách và thông tin sinh viên</p>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3>Danh sách Sinh viên ({filteredStudents.length})</h3>
          <button 
            className="btn btn-primary" 
            onClick={() => setShowForm(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Plus size={16} />
            Thêm Sinh viên
          </button>
        </div>

        <div style={{ marginBottom: '1rem', position: 'relative' }}>
          <Search size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#64748b' }} />
          <input
            type="text"
            placeholder="Tìm kiếm sinh viên..."
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

        {filteredStudents.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Mã SV</th>
                <th>Họ tên</th>
                <th>Email</th>
                <th>Điện thoại</th>
                <th>Năm nhập học</th>
                <th>Trạng thái</th>
                <th>Ngày tạo</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {filteredStudents.map((student) => (
                <tr key={student.id}>
                  <td>{student.username}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <User size={16} color="#64748b" />
                      {student.full_name}
                    </div>
                  </td>
                  <td>{student.email}</td>
                  <td>{student.phone || 'Chưa có'}</td>
                  <td>{student.enrollmentYear || 'Chưa có'}</td>
                  <td>
                    <span style={{
                      padding: '0.25rem 0.5rem',
                      borderRadius: '4px',
                      fontSize: '0.875rem',
                      backgroundColor: student.status === 'active' ? '#d1fae5' : '#fee2e2',
                      color: student.status === 'active' ? '#065f46' : '#991b1b'
                    }}>
                      {student.status === 'active' ? 'Hoạt động' : 'Không hoạt động'}
                    </span>
                  </td>
                  <td>{new Date(student.created_at).toLocaleDateString('vi-VN')}</td>
                  <td>
                    <button 
                      onClick={() => handleEdit(student)}
                      style={{ 
                        marginRight: '0.5rem', 
                        padding: '0.25rem 0.5rem', 
                        fontSize: '0.875rem',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '0.25rem'
                      }}
                    >
                      <Edit size={14} />
                      Sửa
                    </button>
                    <button 
                      onClick={() => handleDelete(student.id)}
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
            <User size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            <p>Chưa có sinh viên nào trong hệ thống</p>
            <p>Nhấn "Thêm Sinh viên" để tạo sinh viên mới</p>
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
              {editingStudent ? 'Sửa thông tin sinh viên' : 'Thêm sinh viên mới'}
            </h3>
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Mã sinh viên *</label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({...formData, username: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  disabled={!!editingStudent}
                />
              </div>
              
              <div className="form-group">
                <label>Họ tên *</label>
                <input
                  type="text"
                  value={formData.full_name}
                  onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Email *</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Điện thoại</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                />
              </div>
              
              <div className="form-group">
                <label>Địa chỉ</label>
                <textarea
                  value={formData.address}
                  onChange={(e) => setFormData({...formData, address: e.target.value})}
                  rows={3}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                />
              </div>
              
              <div className="form-group">
                <label>Năm nhập học *</label>
                <select
                  value={formData.enrollmentYear}
                  onChange={(e) => setFormData({...formData, enrollmentYear: e.target.value})}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  {Array.from({ length: 10 }, (_, i) => {
                    const year = new Date().getFullYear() - i;
                    return (
                      <option key={year} value={year.toString()}>
                        {year}
                      </option>
                    );
                  })}
                </select>
              </div>
              
              {!editingStudent && (
                <div className="form-group">
                  <label>Mật khẩu *</label>
                  <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                    required={!editingStudent}
                  />
                </div>
              )}
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                  {editingStudent ? 'Cập nhật' : 'Thêm mới'}
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

export default Students;