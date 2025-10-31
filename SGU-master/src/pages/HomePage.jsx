import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { BookOpen, Award, FileText, Bell, User, TrendingUp, Calendar, Clock } from 'lucide-react';
import { dashboardService } from '../services/dashboardService';
import { notificationsService } from '../services/notificationsService';

const HomePage = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [unreadNotifications, setUnreadNotifications] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [dashboardResult, notificationsResult] = await Promise.all([
        dashboardService.getStudentDashboard(),
        notificationsService.getUnreadNotifications()
      ]);

      if (dashboardResult.success) {
        setDashboardData(dashboardResult.data);
      }

      if (notificationsResult.success) {
        setUnreadNotifications(notificationsResult.data.length);
      }
    } catch (error) {
      console.error('Lỗi tải dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const features = [
    {
      id: 'classes',
      title: 'Xem lớp học',
      description: 'Xem thông tin lớp học, lịch học và thời khóa biểu',
      icon: BookOpen,
      color: 'bg-blue-500',
      href: '/classes'
    },
    {
      id: 'registration',
      title: 'Đăng ký môn học',
      description: 'Đăng ký và quản lý các môn học trong học kỳ',
      icon: BookOpen,
      color: 'bg-indigo-500',
      href: '/registration'
    },
    {
      id: 'schedule',
      title: 'Lịch học',
      description: 'Xem lịch học và quản lý thời khóa biểu',
      icon: Calendar,
      color: 'bg-purple-500',
      href: '/schedule'
    },
    {
      id: 'grades',
      title: 'Xem điểm và kết quả học tập',
      description: 'Theo dõi điểm số, kết quả học tập và bảng điểm',
      icon: Award,
      color: 'bg-green-500',
      href: '/grades'
    },
    {
      id: 'documents',
      title: 'Đăng ký giấy',
      description: 'Đăng ký các loại giấy tờ cần thiết cho sinh viên',
      icon: FileText,
      color: 'bg-orange-500',
      href: '/documents'
    },
    {
      id: 'tuition',
      title: 'Học phí',
      description: 'Xem và quản lý thông tin học phí',
      icon: TrendingUp,
      color: 'bg-yellow-500',
      href: '/tuition'
    },
    {
      id: 'notifications',
      title: 'Nhận thông báo',
      description: 'Xem thông báo mới và cập nhật từ trường',
      icon: Bell,
      color: 'bg-purple-500',
      href: '/notifications'
    },
    {
      id: 'profile',
      title: 'Cập nhật thông tin cá nhân',
      description: 'Quản lý thông tin cá nhân và đổi mật khẩu',
      icon: User,
      color: 'bg-pink-500',
      href: '/profile'
    },
    // {
    //   id: 'progress',
    //   title: 'Theo dõi tiến độ học',
    //   description: 'Theo dõi tiến độ học tập và thành tích cá nhân',
    //   icon: TrendingUp,
    //   color: 'bg-indigo-500',
    //   href: '/progress'
    // },
    {
      id: 'lookup',
      title: 'Tra cứu thông tin',
      description: 'Tra cứu khoa, ngành, môn học, lớp học và học kỳ',
      icon: BookOpen,
      color: 'bg-cyan-500',
      href: '/lookup'
    }
  ];

  const stats = [
    { 
      label: 'Mã sinh viên', 
      value: dashboardData?.student?.studentCode || 'N/A', 
      icon: User 
    },
    { 
      label: 'GPA', 
      value: dashboardData?.student?.gpa?.toFixed(2) || '0.00', 
      icon: Award 
    },
    { 
      label: 'Thông báo chưa đọc', 
      value: dashboardData?.unreadNotifications?.toString() || unreadNotifications.toString(), 
      icon: Bell 
    },
    { 
      label: 'Tín chỉ', 
      value: dashboardData?.student?.totalCredits || '0', 
      icon: FileText 
    },
    { 
      label: 'Lớp học đã đăng ký', 
      value: dashboardData?.registeredCourses || '0', 
      icon: BookOpen 
    },
    { 
      label: 'Năm nhập học', 
      value: dashboardData?.student?.enrollmentYear || 'N/A', 
      icon: Calendar 
    }
  ];

  return (
    <div className="p-6 space-y-6">
      {loading ? (
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dashboard...</p>
        </div>
      ) : (
        <>
          {/* Welcome Section */}
          <div className="text-center space-y-4 mb-6">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-black">
              Chào mừng, {dashboardData?.student?.fullName || 'Sinh viên'}!
            </h1>
            {/* <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Quản lý học tập và thông tin sinh viên một cách dễ dàng và hiệu quả
            </p> */}
            {dashboardData?.currentSemester && (
              <div className="inline-flex items-center px-4 py-2 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-sm font-medium">
                <Calendar className="h-4 w-4 mr-2" />
                Học kỳ hiện tại: {dashboardData.currentSemester.semesterName}
              </div>
            )}
          </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      {stat.label}
                    </p>
                <p className="text-2xl font-bold text-gray-900">
                  {stat.value}
                </p>
                  </div>
                  <Icon className="h-8 w-8 text-blue-500" />
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Features Grid */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-gray-900">
          Các chức năng chính
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Card key={feature.id} className="hover:shadow-lg transition-all duration-300 hover:-translate-y-1 cursor-pointer group">
                <CardHeader className="pb-3">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${feature.color} text-white`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    <CardTitle className="text-lg group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                      {feature.title}
                    </CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-sm text-gray-600 dark:text-gray-400">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

        </>
      )}
    </div>
  );
};

export default HomePage;
