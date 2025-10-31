import React, { useState, useEffect } from 'react';
import { Bell, Plus, Search } from 'lucide-react';
import api from '../services/api';

interface Notification {
  notificationId: string;
  title: string;
  content: string;
  targetAudience: string;
  notificationType: string;
  priority: number;
  createdBy: string;
}

const Notifications: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const [formData, setFormData] = useState({
    notificationId: '',
    title: '',
    content: '',
    targetAudience: 'all',
    notificationType: 'general',
    priority: 'medium'
  });

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await api.get('/crud/notifications/');
      setNotifications(response.data.notifications || []);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const priorityMap: { [key: string]: number } = {
        'low': 1,
        'medium': 2,
        'high': 3
      };
      
      const payload = {
        ...formData,
        priority: priorityMap[formData.priority]
      };
      
      await api.post('/crud/notifications/create/', payload);
      fetchNotifications();
      setShowModal(false);
      resetForm();
    } catch (error) {
      console.error('Error creating notification:', error);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa thông báo này?')) {
      try {
        await api.delete(`/crud/notifications/${id}/delete/`);
        fetchNotifications();
      } catch (error) {
        console.error('Error deleting notification:', error);
        alert('Có lỗi xảy ra khi xóa thông báo');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      notificationId: '',
      title: '',
      content: '',
      targetAudience: 'all',
      notificationType: 'general',
      priority: 'medium'
    });
  };

  const getTypeConfig = (type: string) => {
    switch (type) {
      case 'urgent': return { color: 'bg-red-500', label: 'Khẩn cấp' };
      case 'announcement': return { color: 'bg-blue-500', label: 'Thông báo' };
      case 'reminder': return { color: 'bg-orange-500', label: 'Nhắc nhở' };
      default: return { color: 'bg-gray-500', label: 'Chung' };
    }
  };

  const getAudienceConfig = (audience: string) => {
    switch (audience) {
      case 'students': return { label: 'Sinh viên', color: 'text-blue-600' };
      case 'teachers': return { label: 'Giảng viên', color: 'text-green-600' };
      case 'staff': return { label: 'Nhân viên', color: 'text-purple-600' };
      default: return { label: 'Tất cả', color: 'text-gray-600' };
    }
  };

  const filteredNotifications = notifications.filter(notification =>
    notification.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    notification.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
    notification.targetAudience.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <div className="page-header">
        <h1>Quản lý Thông báo</h1>
        <p>Danh sách và quản lý thông báo</p>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h3>Danh sách Thông báo ({filteredNotifications.length})</h3>
          <button 
            className="btn btn-primary" 
            onClick={() => setShowModal(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}
          >
            <Plus size={16} />
            Thêm Thông báo
          </button>
        </div>

        <div style={{ marginBottom: '1rem', position: 'relative' }}>
          <Search size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#64748b' }} />
          <input
            type="text"
            placeholder="Tìm kiếm thông báo..."
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

        {filteredNotifications.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Tiêu đề</th>
                <th>Nội dung</th>
                <th>Đối tượng</th>
                <th>Loại</th>
                <th>Ưu tiên</th>
                <th>Người tạo</th>
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {filteredNotifications.map((notification) => {
                const audienceConfig = getAudienceConfig(notification.targetAudience);
                const typeConfig = getTypeConfig(notification.notificationType);
                
                return (
                  <tr key={notification.notificationId}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Bell size={16} color="#64748b" />
                        {notification.title}
                      </div>
                    </td>
                    <td>{notification.content}</td>
                    <td>{audienceConfig.label}</td>
                    <td>{typeConfig.label}</td>
                    <td>
                      <span style={{
                        padding: '0.25rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.875rem',
                        backgroundColor: notification.priority === 3 ? '#fee2e2' : notification.priority === 2 ? '#fef3c7' : '#d1fae5',
                        color: notification.priority === 3 ? '#991b1b' : notification.priority === 2 ? '#92400e' : '#065f46'
                      }}>
                        {notification.priority === 3 ? 'Cao' : notification.priority === 2 ? 'Trung bình' : 'Thấp'}
                      </span>
                    </td>
                    <td>{notification.createdBy || 'Hệ thống'}</td>
                    <td>
                      <button 
                        onClick={() => handleDelete(notification.notificationId)}
                        style={{ 
                          padding: '0.25rem 0.5rem', 
                          fontSize: '0.875rem', 
                          color: '#dc2626',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.25rem'
                        }}
                      >
                        Xóa
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
            <Bell size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            <p>Chưa có thông báo nào trong hệ thống</p>
            <p>Nhấn "Thêm Thông báo" để tạo thông báo mới</p>
          </div>
        )}
      </div>

      {showModal && (
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
            <h3 style={{ marginBottom: '1.5rem' }}>Tạo thông báo mới</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Mã thông báo *</label>
                <input
                  type="text"
                  value={formData.notificationId}
                  onChange={(e) => setFormData({...formData, notificationId: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Tiêu đề *</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Nội dung *</label>
                <textarea
                  value={formData.content}
                  onChange={(e) => setFormData({...formData, content: e.target.value})}
                  rows={3}
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Đối tượng *</label>
                <select
                  value={formData.targetAudience}
                  onChange={(e) => setFormData({...formData, targetAudience: e.target.value})}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  <option value="all">Tất cả người dùng</option>
                  <option value="students">Sinh viên</option>
                  <option value="teachers">Giảng viên</option>
                  <option value="staff">Nhân viên</option>
                </select>
              </div>
              
              <div className="form-group">
                <label>Loại thông báo *</label>
                <select
                  value={formData.notificationType}
                  onChange={(e) => setFormData({...formData, notificationType: e.target.value})}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  <option value="general">Chung</option>
                  <option value="announcement">Thông báo</option>
                  <option value="reminder">Nhắc nhở</option>
                  <option value="urgent">Khẩn cấp</option>
                </select>
              </div>
              
              <div className="form-group">
                <label>Mức độ ưu tiên *</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({...formData, priority: e.target.value})}
                  required
                  style={{ width: '100%', padding: '0.75rem', border: '1px solid #d1d5db', borderRadius: '6px' }}
                >
                  <option value="low">Thấp</option>
                  <option value="medium">Trung bình</option>
                  <option value="high">Cao</option>
                </select>
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                  Thêm mới
                </button>
                <button 
                  type="button" 
                  onClick={() => {setShowModal(false); resetForm();}}
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

export default Notifications;