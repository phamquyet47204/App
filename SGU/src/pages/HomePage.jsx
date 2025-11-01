import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { BookOpen, Award, FileText, Bell, User, TrendingUp, Calendar } from 'lucide-react';
import { userService } from '../services/userService';
import { notificationsService } from '../services/notificationsService';
import { AuthStorage } from '../types/user';

const HomePage = ({ onPageChange }) => {
  const [userInfo, setUserInfo] = useState(null);
  const [unreadNotifications, setUnreadNotifications] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const [profileResult, notificationsResult] = await Promise.all([
        userService.getStudentProfile(),
        notificationsService.getUnreadNotifications()
      ]);

      if (profileResult.success && profileResult.data) {
        const p = profileResult.data;
        setUserInfo({
          studentId: p.studentCode,
          fullName: p.fullName,
          email: p.email,
          phone: p.phone,
          dateOfBirth: p.dateOfBirth,
          address: p.address,
          gender: p.gender,
          major: p.studentClass?.major?.majorName,
          class: p.studentClass?.className,
          year: p.enrollmentYear,
          gpa: p.gpa,
          totalCredits: p.totalCredits,
        });
      } else {
        const saved = AuthStorage.getCurrentUser();
        if (saved) setUserInfo(saved);
      }

      if (notificationsResult.success) {
        setUnreadNotifications(notificationsResult.data.length);
      }
    } catch (error) {
      console.error('Lỗi tải thông tin:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFeatureClick = (featureId) => {
    if (onPageChange) {
      onPageChange(featureId);
    }
  };

  const features = [
    { id: 'classes', title: 'Xem lớp học', description: 'Xem thông tin lớp học, lịch học và thời khóa biểu', icon: BookOpen, color: 'bg-blue-500' },
    { id: 'registration', title: 'Đăng ký môn học', description: 'Đăng ký và quản lý các môn học trong học kỳ', icon: BookOpen, color: 'bg-indigo-500' },
    { id: 'schedule', title: 'Lịch học', description: 'Xem lịch học và quản lý thời khóa biểu', icon: Calendar, color: 'bg-purple-500' },
    { id: 'documents', title: 'Đăng ký giấy tờ', description: 'Đăng ký các loại giấy tờ cần thiết', icon: FileText, color: 'bg-orange-500' },
    { id: 'tuition', title: 'Học phí', description: 'Xem và quản lý thông tin học phí', icon: TrendingUp, color: 'bg-yellow-500' },
    { id: 'notifications', title: 'Thông báo', description: 'Xem thông báo mới từ trường', icon: Bell, color: 'bg-purple-500' },
    { id: 'profile', title: 'Hồ sơ cá nhân', description: 'Cập nhật thông tin và đổi mật khẩu', icon: User, color: 'bg-pink-500' },
    { id: 'lookup', title: 'Tra cứu thông tin', description: 'Tra cứu khoa, ngành, lớp học và học kỳ', icon: BookOpen, color: 'bg-cyan-500' },
    { id: 'progress', title: 'Tiến độ học', description: 'Xem lớp học đã hoàn thành và tiến độ học tập', icon: TrendingUp, color: 'bg-emerald-500' },
  ];

  const stats = [
    { label: 'Mã sinh viên', value: userInfo?.studentId || 'N/A', icon: User },
    { label: 'GPA', value: userInfo?.gpa ? userInfo.gpa.toFixed(1) : '0.0', icon: Award },
    { label: 'Thông báo chưa đọc', value: unreadNotifications.toString(), icon: Bell },
    { label: 'Tín chỉ', value: userInfo?.totalCredits || '0', icon: FileText },
    { label: 'Lớp học', value: userInfo?.class || 'N/A', icon: BookOpen },
    // { label: 'Năm nhập học', value: userInfo?.year || 'N/A', icon: Calendar },
  ];

  return (
    <div className="p-6 space-y-6">
      {loading ? (
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải thông tin...</p>
        </div>
      ) : (
        <>
          <div className="text-center space-y-4 mb-6">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-black">
              Chào mừng, {userInfo?.fullName || 'Sinh viên'}!
            </h1>
            {/* <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Quản lý học tập và thông tin sinh viên một cách dễ dàng
            </p> */}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                        <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                      </div>
                      <Icon className="h-8 w-8 text-blue-500" />
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>

          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-gray-900">Các chức năng chính</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature) => {
                const Icon = feature.icon;
                return (
                  <Card 
                    key={feature.id} 
                    className="hover:shadow-lg transition-all duration-300 hover:-translate-y-1 cursor-pointer group"
                    onClick={() => handleFeatureClick(feature.id)}
                  >
                    <CardHeader className="pb-3">
                      <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded-lg ${feature.color} text-white`}>
                          <Icon className="h-6 w-6" />
                        </div>
                        <CardTitle className="text-lg group-hover:text-blue-600 transition-colors">
                          {feature.title}
                        </CardTitle>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-sm text-gray-600">
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
