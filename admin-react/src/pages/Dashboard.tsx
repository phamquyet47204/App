import React, { useEffect, useState } from 'react';
import { Users, Building2, BookOpen, GraduationCap } from 'lucide-react';
import axios from 'axios';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    students: 0,
    teachers: 0,
    departments: 0,
    subjects: 0
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const sessionKey = localStorage.getItem('session_key');
      const config = {
        headers: {
          'Authorization': `Session ${sessionKey}`,
          'X-Session-Key': sessionKey
        }
      };

      // Fetch actual data from each endpoint
      const [deptResponse, subjectResponse] = await Promise.all([
        axios.get('http://127.0.0.1:8000/api/crud/departments/', config),
        axios.get('http://127.0.0.1:8000/api/crud/subjects/', config)
      ]);

      // Try to get dashboard stats, fallback to counting from CRUD endpoints
      try {
        const dashResponse = await axios.get('http://127.0.0.1:8000/api/admin/dashboard/', config);
        setStats(dashResponse.data);
      } catch {
        setStats({
          students: 0,
          teachers: 0,
          departments: deptResponse.data.length || 0,
          subjects: subjectResponse.data.length || 0
        });
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const statCards = [
    {
      title: 'Sinh viên',
      value: stats.students,
      icon: Users,
      color: '#3b82f6',
      bgColor: '#dbeafe'
    },
    {
      title: 'Giảng viên',
      value: stats.teachers,
      icon: GraduationCap,
      color: '#10b981',
      bgColor: '#d1fae5'
    },
    {
      title: 'Khoa',
      value: stats.departments,
      icon: Building2,
      color: '#f59e0b',
      bgColor: '#fef3c7'
    },
    {
      title: 'Môn học',
      value: stats.subjects,
      icon: BookOpen,
      color: '#ef4444',
      bgColor: '#fee2e2'
    }
  ];

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Tổng quan hệ thống quản lý trường đại học</p>
      </div>

      <div className="stats-grid">
        {statCards.map((stat, index) => (
          <div key={index} className="stat-card">
            <div 
              className="stat-icon"
              style={{ backgroundColor: stat.bgColor, color: stat.color }}
            >
              <stat.icon size={24} />
            </div>
            <div className="stat-content">
              <h3>{stat.value}</h3>
              <p>{stat.title}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', fontWeight: '700' }}>Hoạt động gần đây</h3>
        <div style={{ color: '#64748b' }}>
          <p>• Hệ thống đang hoạt động bình thường</p>
          <p>• Có {stats.students} sinh viên đang học</p>
          <p>• Có {stats.teachers} giảng viên đang giảng dạy</p>
          <p>• Quản lý {stats.departments} khoa và {stats.subjects} môn học</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
