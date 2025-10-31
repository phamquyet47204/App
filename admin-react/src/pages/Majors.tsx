import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { GraduationCap, Edit, Trash2, Plus, Search } from 'lucide-react';

interface Major {
  majorId: string;
  majorCode: string;
  majorName: string;
  department: string;
  durationYears: number;
  totalCredits: number;
}

interface Department {
  departmentId: string;
  departmentName: string;
}

const Majors: React.FC = () => {
  const [majors, setMajors] = useState<Major[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingMajor, setEditingMajor] = useState<Major | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    majorId: '',
    majorCode: '',
    majorName: '',
    departmentId: '',
    durationYears: 4,
    totalCredits: 140
  });

  useEffect(() => {
    fetchMajors();
    fetchDepartments();
  }, []);

  const fetchMajors = async () => {
    try {
      const sessionKey = localStorage.getItem('session_key');
      const response = await axios.get('http://127.0.0.1:8000/api/crud/majors/', {
        headers: {
          'Authorization': `Session ${sessionKey}`,
          'X-Session-Key': sessionKey
        }
      });
      const data = response.data.majors || response.data;
      setMajors(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching majors:', error);
      setMajors([]);
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

      if (editingMajor) {
        await axios.put(`http://127.0.0.1:8000/api/crud/majors/${editingMajor.majorId}/update/`, formData, config);
      } else {
        await axios.post('http://127.0.0.1:8000/api/crud/majors/create/', formData, config);
      }
      
      fetchMajors();
      resetForm();
    } catch (error) {
      console.error('Error saving major:', error);
      alert('Có lỗi xảy ra khi lưu thông tin ngành học');
    }
  };

  const handleEdit = (major: Major) => {
    setEditingMajor(major);
    const dept = departments.find(d => d.departmentName === major.department);
    setFormData({
      majorId: major.majorId,
      majorCode: major.majorCode,
      majorName: major.majorName,
      departmentId: dept?.departmentId || '',
      durationYears: major.durationYears,
      totalCredits: major.totalCredits
    });
    setShowForm(true);
  };

  const handleDelete = async (majorId: string) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa ngành học này?')) {
      try {
        const sessionKey = localStorage.getItem('session_key');
        await axios.delete(`http://127.0.0.1:8000/api/crud/majors/${majorId}/delete/`, {
          headers: {
            'Authorization': `Session ${sessionKey}`,
            'X-Session-Key': sessionKey
          }
        });
        fetchMajors();
      } catch (error) {
        console.error('Error deleting major:', error);
        alert('Có lỗi xảy ra khi xóa ngành học');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      majorId: '',
      majorCode: '',
      majorName: '',
      departmentId: '',
      durationYears: 4,
      totalCredits: 140
    });
    setEditingMajor(null);
    setShowForm(false);
  };

  const filteredMajors = majors.filter(major =>
    major.majorName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    major.majorCode.toLowerCase().includes(searchTerm.toLowerCase()) ||
    major.department.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div>Đang tải...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Quản lý Ngành học</h1>
        <p>Danh sách các ngành học trong trường</p>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3>Danh sách Ngành học ({filteredMajors.length})</h3>
          <button 
            className="btn btn-primary" 
            onClick={() => setShowForm(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Plus size={16} />
            Thêm Ngành học
          </button>
        </div>

        <div style={{ marginBottom: '1rem', position: 'relative' }}>
          <Search size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#64748b' }} />
          <input
            type="text"
            placeholder="Tìm kiếm ngành học..."
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

        {filteredMajors.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Mã Ngành</th>
                <th>Tên Ngành</th>
                <th>Mã Code</th>
                <th>Thuộc Khoa</th>
                <th>Thời gian</th>
                <th>Tín chỉ</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {filteredMajors.map((major) => (
                <tr key={major.majorId}>
                  <td>{major.majorId}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <GraduationCap size={16} color="#64748b" />
                      {major.majorName}
                    </div>
                  </td>
                  <td>{major.majorCode}</td>
                  <td>{major.department}</td>
                  <td>{major.durationYears} năm</td>
                  <td>{major.totalCredits} tín chỉ</td>
                  <td>
                    <button 
                      onClick={() => handleEdit(major)}
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
                      onClick={() => handleDelete(major.majorId)}
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
            <GraduationCap size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            <p>Chưa có ngành học nào trong hệ thống</p>
            <p>Nhấn "Thêm Ngành học" để tạo ngành mới</p>
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
              {editingMajor ? 'Sửa thông tin ngành học' : 'Thêm ngành học mới'}
            </h3>
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Mã ngành *</label>
                <input
                  type="text"
                  value={formData.majorId}
                  onChange={(e) => setFormData({...formData, majorId: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  disabled={!!editingMajor}
                />
              </div>
              
              <div className="form-group">
                <label>Mã code *</label>
                <input
                  type="text"
                  value={formData.majorCode}
                  onChange={(e) => setFormData({...formData, majorCode: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Tên ngành *</label>
                <input
                  type="text"
                  value={formData.majorName}
                  onChange={(e) => setFormData({...formData, majorName: e.target.value})}
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
                <label>Thời gian đào tạo (năm) *</label>
                <input
                  type="number"
                  value={formData.durationYears}
                  onChange={(e) => setFormData({...formData, durationYears: parseInt(e.target.value)})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  min="1"
                  max="10"
                />
              </div>
              
              <div className="form-group">
                <label>Tổng tín chỉ *</label>
                <input
                  type="number"
                  value={formData.totalCredits}
                  onChange={(e) => setFormData({...formData, totalCredits: parseInt(e.target.value)})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  min="1"
                />
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                  {editingMajor ? 'Cập nhật' : 'Thêm mới'}
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

export default Majors;