import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Building2, Edit, Trash2, Plus, Search } from 'lucide-react';

interface Department {
  departmentId: string;
  departmentCode: string;
  departmentName: string;
  status: string;
}

const Departments: React.FC = () => {
  const [departments, setDepartments] = useState<Department[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingDepartment, setEditingDepartment] = useState<Department | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    departmentId: '',
    departmentCode: '',
    departmentName: '',
    status: 'active'
  });

  useEffect(() => {
    fetchDepartments();
  }, []);

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
      setDepartments([]);
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

      if (editingDepartment) {
        await axios.put(`http://127.0.0.1:8000/api/crud/departments/${editingDepartment.departmentId}/update/`, formData, config);
      } else {
        await axios.post('http://127.0.0.1:8000/api/crud/departments/create/', formData, config);
      }
      
      fetchDepartments();
      resetForm();
    } catch (error) {
      console.error('Error saving department:', error);
      alert('Có lỗi xảy ra khi lưu thông tin khoa');
    }
  };

  const handleEdit = (department: Department) => {
    setEditingDepartment(department);
    setFormData({
      departmentId: department.departmentId,
      departmentCode: department.departmentCode,
      departmentName: department.departmentName,
      status: department.status
    });
    setShowForm(true);
  };

  const handleDelete = async (departmentId: string) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa khoa này?')) {
      try {
        const sessionKey = localStorage.getItem('session_key');
        await axios.delete(`http://127.0.0.1:8000/api/crud/departments/${departmentId}/delete/`, {
          headers: {
            'Authorization': `Session ${sessionKey}`,
            'X-Session-Key': sessionKey
          }
        });
        fetchDepartments();
      } catch (error) {
        console.error('Error deleting department:', error);
        alert('Có lỗi xảy ra khi xóa khoa');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      departmentId: '',
      departmentCode: '',
      departmentName: '',
      status: 'active'
    });
    setEditingDepartment(null);
    setShowForm(false);
  };

  const filteredDepartments = departments.filter(dept =>
    dept.departmentName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    dept.departmentCode.toLowerCase().includes(searchTerm.toLowerCase()) ||
    dept.departmentId.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div>Đang tải...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Quản lý Khoa</h1>
        <p>Danh sách các khoa trong trường</p>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3>Danh sách Khoa ({filteredDepartments.length})</h3>
          <button 
            className="btn btn-primary" 
            onClick={() => setShowForm(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Plus size={16} />
            Thêm Khoa
          </button>
        </div>

        <div style={{ marginBottom: '1rem', position: 'relative' }}>
          <Search size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#64748b' }} />
          <input
            type="text"
            placeholder="Tìm kiếm khoa..."
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

        {filteredDepartments.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Mã Khoa</th>
                <th>Tên Khoa</th>
                <th>Mã Code</th>
                <th>Trạng thái</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {filteredDepartments.map((dept) => (
                <tr key={dept.departmentId}>
                  <td>{dept.departmentId}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <Building2 size={16} color="#64748b" />
                      {dept.departmentName}
                    </div>
                  </td>
                  <td>{dept.departmentCode}</td>
                  <td>
                    <span style={{ 
                      padding: '0.25rem 0.5rem', 
                      borderRadius: '4px', 
                      fontSize: '0.875rem',
                      backgroundColor: dept.status === 'active' ? '#d1fae5' : '#fee2e2',
                      color: dept.status === 'active' ? '#065f46' : '#991b1b'
                    }}>
                      {dept.status === 'active' ? 'Hoạt động' : 'Không hoạt động'}
                    </span>
                  </td>
                  <td>
                    <button 
                      onClick={() => handleEdit(dept)}
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
                      onClick={() => handleDelete(dept.departmentId)}
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
            <Building2 size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            <p>Chưa có khoa nào trong hệ thống</p>
            <p>Nhấn "Thêm Khoa" để tạo khoa mới</p>
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
              {editingDepartment ? 'Sửa thông tin khoa' : 'Thêm khoa mới'}
            </h3>
            
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Mã khoa *</label>
                <input
                  type="text"
                  value={formData.departmentId}
                  onChange={(e) => setFormData({...formData, departmentId: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                  disabled={!!editingDepartment}
                />
              </div>
              
              <div className="form-group">
                <label>Mã code *</label>
                <input
                  type="text"
                  value={formData.departmentCode}
                  onChange={(e) => setFormData({...formData, departmentCode: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Tên khoa *</label>
                <input
                  type="text"
                  value={formData.departmentName}
                  onChange={(e) => setFormData({...formData, departmentName: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Trạng thái *</label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({...formData, status: e.target.value})}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  <option value="active">Hoạt động</option>
                  <option value="inactive">Không hoạt động</option>
                </select>
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                  {editingDepartment ? 'Cập nhật' : 'Thêm mới'}
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

export default Departments;