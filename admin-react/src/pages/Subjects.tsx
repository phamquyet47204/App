import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BookOpen, Edit, Trash2, Plus, Search } from 'lucide-react';

interface Subject {
  subjectId: string;
  subjectCode: string;
  subjectName: string;
  department: string;
  credits: number;
  theoryHours: number;
  practiceHours: number;
}

interface Department {
  departmentId: string;
  departmentName: string;
}

const Subjects: React.FC = () => {
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingSubject, setEditingSubject] = useState<Subject | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    subjectId: '',
    subjectCode: '',
    subjectName: '',
    departmentId: '',
    credits: 3,
    theoryHours: 30,
    practiceHours: 15
  });

  useEffect(() => {
    fetchSubjects();
    fetchDepartments();
  }, []);

  const fetchSubjects = async () => {
    try {
      const sessionKey = localStorage.getItem('session_key');
      const response = await axios.get('http://127.0.0.1:8000/api/crud/subjects/', {
        headers: {
          'Authorization': `Session ${sessionKey}`,
          'X-Session-Key': sessionKey
        }
      });
      const data = response.data.subjects || response.data;
      setSubjects(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching subjects:', error);
      setSubjects([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchDepartments = async () => {
    try {
      const sessionKey = localStorage.getItem('session_key');
      const response = await axios.get('http://127.0.0.1:8000/api/crud/departments/', {
        headers: {
          'Authorization': `Session ${sessionKey}`,
          'X-Session-Key': sessionKey
        }
      });
      const data = response.data.departments || response.data;
      setDepartments(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching departments:', error);
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

      if (editingSubject) {
        await axios.put(`http://127.0.0.1:8000/api/crud/subjects/${editingSubject.subjectId}/update/`, formData, config);
      } else {
        await axios.post('http://127.0.0.1:8000/api/crud/subjects/create/', formData, config);
      }
      
      fetchSubjects();
      resetForm();
    } catch (error) {
      console.error('Error saving subject:', error);
      alert('Có lỗi xảy ra khi lưu thông tin môn học');
    }
  };

  const handleEdit = (subject: Subject) => {
    setEditingSubject(subject);
    const dept = departments.find(d => d.departmentName === subject.department);
    setFormData({
      subjectId: subject.subjectId,
      subjectCode: subject.subjectCode,
      subjectName: subject.subjectName,
      departmentId: dept?.departmentId || '',
      credits: subject.credits,
      theoryHours: subject.theoryHours,
      practiceHours: subject.practiceHours
    });
    setShowForm(true);
  };

  const handleDelete = async (subjectId: string) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa môn học này?')) {
      try {
        const sessionKey = localStorage.getItem('session_key');
        await axios.delete(`http://127.0.0.1:8000/api/crud/subjects/${subjectId}/delete/`, {
          headers: {
            'Authorization': `Session ${sessionKey}`,
            'X-Session-Key': sessionKey
          }
        });
        fetchSubjects();
      } catch (error) {
        console.error('Error deleting subject:', error);
        alert('Có lỗi xảy ra khi xóa môn học');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      subjectId: '',
      subjectCode: '',
      subjectName: '',
      departmentId: '',
      credits: 3,
      theoryHours: 30,
      practiceHours: 15
    });
    setEditingSubject(null);
    setShowForm(false);
  };

  const filteredSubjects = subjects.filter(subject =>
    subject.subjectName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    subject.subjectCode.toLowerCase().includes(searchTerm.toLowerCase()) ||
    subject.department.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div>Đang tải...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Quản lý Môn học</h1>
        <p>Danh sách các môn học trong trường</p>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3>Danh sách Môn học ({filteredSubjects.length})</h3>
          <button 
            className="btn btn-primary" 
            onClick={() => setShowForm(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Plus size={16} />
            Thêm Môn học
          </button>
        </div>

        <div style={{ marginBottom: '1rem', position: 'relative' }}>
          <Search size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#64748b' }} />
          <input
            type="text"
            placeholder="Tìm kiếm môn học..."
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

        {filteredSubjects.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Mã Môn</th>
                <th>Tên Môn học</th>
                <th>Mã Code</th>
                <th>Thuộc Khoa</th>
                <th>Tín chỉ</th>
                <th>Lý thuyết</th>
                <th>Thực hành</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {filteredSubjects.map((subject) => (
                <tr key={subject.subjectId}>
                  <td>{subject.subjectId}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <BookOpen size={16} color="#64748b" />
                      {subject.subjectName}
                    </div>
                  </td>
                  <td>{subject.subjectCode}</td>
                  <td>{subject.department}</td>
                  <td>{subject.credits}</td>
                  <td>{subject.theoryHours}h</td>
                  <td>{subject.practiceHours}h</td>
                  <td>
                    <button 
                      onClick={() => handleEdit(subject)}
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
                      onClick={() => handleDelete(subject.subjectId)}
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
            <BookOpen size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            <p>Chưa có môn học nào trong hệ thống</p>
            <p>Nhấn "Thêm Môn học" để tạo môn học mới</p>
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
              {editingSubject ? 'Sửa thông tin môn học' : 'Thêm môn học mới'}
            </h3>
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Mã môn học *</label>
                <input
                  type="text"
                  value={formData.subjectId}
                  onChange={(e) => setFormData({...formData, subjectId: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  disabled={!!editingSubject}
                />
              </div>
              
              <div className="form-group">
                <label>Mã code *</label>
                <input
                  type="text"
                  value={formData.subjectCode}
                  onChange={(e) => setFormData({...formData, subjectCode: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Tên môn học *</label>
                <input
                  type="text"
                  value={formData.subjectName}
                  onChange={(e) => setFormData({...formData, subjectName: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Thuộc khoa *</label>
                <select
                  value={formData.departmentId}
                  onChange={(e) => setFormData({...formData, departmentId: e.target.value})}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  <option value="">Chọn khoa</option>
                  {departments.map(dept => (
                    <option key={dept.departmentId} value={dept.departmentId}>
                      {dept.departmentName}
                    </option>
                  ))}
                </select>
              </div>
              
              <div className="form-group">
                <label>Số tín chỉ *</label>
                <input
                  type="number"
                  value={formData.credits}
                  onChange={(e) => setFormData({...formData, credits: parseInt(e.target.value)})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  min="1"
                  max="10"
                />
              </div>
              
              <div className="form-group">
                <label>Số tiết lý thuyết *</label>
                <input
                  type="number"
                  value={formData.theoryHours}
                  onChange={(e) => setFormData({...formData, theoryHours: parseInt(e.target.value)})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  min="0"
                />
              </div>
              
              <div className="form-group">
                <label>Số tiết thực hành *</label>
                <input
                  type="number"
                  value={formData.practiceHours}
                  onChange={(e) => setFormData({...formData, practiceHours: parseInt(e.target.value)})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  min="0"
                />
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                  {editingSubject ? 'Cập nhật' : 'Thêm mới'}
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

export default Subjects;