import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  Building2,
  GraduationCap,
  BookOpen,
  Users,
  UserCheck,
  ClipboardList,
  Calendar,
  Bell,
  LogOut
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('session_key');
    navigate('/login');
  };

  const menuItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/departments', icon: Building2, label: 'Khoa' },
    { path: '/majors', icon: GraduationCap, label: 'Ngành học' },
    { path: '/subjects', icon: BookOpen, label: 'Môn học' },
    { path: '/students', icon: Users, label: 'Sinh viên' },
    { path: '/teachers', icon: UserCheck, label: 'Giảng viên' },
    { path: '/course-classes', icon: Calendar, label: 'Lớp học' },
    { path: '/grades', icon: ClipboardList, label: 'Điểm số' },
    { path: '/notifications', icon: Bell, label: 'Thông báo' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Admin Dashboard</h2>
        <p>Quản lý trường đại học</p>
      </div>
      
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => 
              `nav-item ${isActive ? 'active' : ''}`
            }
            end={item.path === '/'}
          >
            <item.icon />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      
      <div style={{ padding: '1rem', borderTop: '1px solid #334155', marginTop: 'auto' }}>
        <button 
          onClick={handleLogout}
          className="nav-item"
          style={{ 
            width: '100%', 
            background: 'none', 
            border: 'none', 
            color: '#cbd5e1',
            cursor: 'pointer',
            padding: '0.75rem 0'
          }}
        >
          <LogOut />
          <span>Đăng xuất</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;