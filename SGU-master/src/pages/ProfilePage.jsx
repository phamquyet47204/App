import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { User, Lock, Mail, Phone, MapPin, Calendar, Save, Edit, Camera } from 'lucide-react';
import { userService } from '../services/userService';
import { authService } from '../services/authService';
import { AuthStorage } from '../types/user';
import { toast } from 'react-hot-toast';

const ProfilePage = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(true);

  // Lấy thông tin user từ localStorage hoặc API
  const [userInfo, setUserInfo] = useState({
    id: '1',
    studentId: '2021001234',
    fullName: 'Nguyễn Văn A',
    email: 'nguyenvana@sgu.edu.vn',
    phone: '0123456789',
    dateOfBirth: '2003-01-15',
    address: '123 Đường ABC, Quận 1, TP.HCM',
    major: 'Công nghệ thông tin',
    class: 'CNTT01',
    year: '2021',
    avatar: null
  });

  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      setLoading(true);
      const result = await userService.getStudentProfile();
      if (result.success && result.data) {
        const profileData = result.data;
        setUserInfo(prev => ({
          ...prev,
          id: profileData.studentId,
          studentId: profileData.studentCode,
          fullName: profileData.user?.fullName || profileData.fullName,
          email: profileData.user?.email,
          phone: profileData.user?.phone,
          dateOfBirth: profileData.dateOfBirth,
          address: profileData.user?.address,
          major: profileData.studentClass?.major?.majorName,
          class: profileData.studentClass?.className,
          year: profileData.enrollmentYear,
          gpa: profileData.gpa,
          totalCredits: profileData.totalCredits
        }));
      } else {
        // Fallback to localStorage if API fails
        const savedUser = AuthStorage.getCurrentUser();
        if (savedUser) {
          setUserInfo(prev => ({
            ...prev,
            ...savedUser,
            fullName: savedUser.fullName || savedUser.full_name
          }));
        }
      }
    } catch (error) {
      console.error('Lỗi tải profile:', error);
      // Fallback to localStorage
      const savedUser = AuthStorage.getCurrentUser();
      if (savedUser) {
        setUserInfo(prev => ({
          ...prev,
          ...savedUser,
          fullName: savedUser.fullName || savedUser.full_name
        }));
      }
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setUserInfo(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePasswordChange = (field, value) => {
    setPasswordForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSaveProfile = async () => {
    try {
      const result = await userService.updateProfile({
        fullName: userInfo.fullName,
        email: userInfo.email,
        phone: userInfo.phone
      });
      
      if (result.success) {
        toast.success('Cập nhật thông tin thành công');
        setIsEditing(false);
        // Cập nhật localStorage
        AuthStorage.setCurrentUser(userInfo);
      } else {
        toast.error(result.message);
      }
    } catch (error) {
      console.error('Lỗi cập nhật thông tin:', error);
      toast.error('Có lỗi xảy ra khi cập nhật thông tin');
    }
  };

  const handleChangePassword = async () => {
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      toast.error('Mật khẩu mới và xác nhận mật khẩu không khớp');
      return;
    }

    if (passwordForm.newPassword.length < 6) {
      toast.error('Mật khẩu mới phải có ít nhất 6 ký tự');
      return;
    }

    try {
      const result = await authService.changePassword(
        passwordForm.currentPassword,
        passwordForm.newPassword
      );
      
      if (result.success) {
        toast.success('Đổi mật khẩu thành công');
        setPasswordForm({
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        });
      } else {
        toast.error(result.message);
      }
    } catch (error) {
      console.error('Lỗi đổi mật khẩu:', error);
      toast.error('Có lỗi xảy ra khi đổi mật khẩu');
    }
  };

  const getInitials = (name) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải thông tin cá nhân...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          {/* <h1 className="text-2xl font-bold text-gray-900 dark:text-black">
            Thông tin cá nhân
          </h1> */}
          {/* <p className="text-gray-600 dark:text-gray-300 mt-2">
            Quản lý thông tin cá nhân và cài đặt tài khoản
          </p> */}
        </div>
        <div className="flex items-center space-x-2">
          {isEditing ? (
            <>
              <Button variant="outline" onClick={() => setIsEditing(false)}>
                Hủy
              </Button>
              <Button variant="outline" onClick={handleSaveProfile}>
                <Save className="h-4 w-4 mr-2" />
                Lưu thay đổi
              </Button>
            </>
          ) : (
            <Button variant="outline" onClick={() => setIsEditing(true)}>
              <Edit className="h-4 w-4 mr-2" />
              Chỉnh sửa
            </Button>
          )}
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="profile">Thông tin cá nhân</TabsTrigger>
          <TabsTrigger value="password">Đổi mật khẩu</TabsTrigger>
          {/* <TabsTrigger value="settings">Cài đặt</TabsTrigger> */}
        </TabsList>

        <TabsContent value="profile" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Avatar Section */}
            <Card>
              <CardHeader>
                <CardTitle>Ảnh đại diện</CardTitle>
                <CardDescription>
                  Cập nhật ảnh đại diện của bạn
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex flex-col items-center space-y-4">
                  <Avatar className="h-24 w-24">
                    <AvatarImage src={userInfo.avatar} />
                    <AvatarFallback className="text-2xl">
                      {getInitials(userInfo.fullName)}
                    </AvatarFallback>
                  </Avatar>
                  <Button variant="outline" size="sm">
                    <Camera className="h-4 w-4 mr-2" />
                    Thay đổi ảnh
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Personal Information */}
            <div className="lg:col-span-2 space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Thông tin cơ bản</CardTitle>
                  <CardDescription>
                    Thông tin cá nhân cơ bản của bạn
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="fullName">Họ và tên</Label>
                      <Input
                        id="fullName"
                        value={userInfo.fullName}
                        onChange={(e) => handleInputChange('fullName', e.target.value)}
                        disabled={!isEditing}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="studentId">Mã sinh viên</Label>
                      <Input
                        id="studentId"
                        value={userInfo.studentId}
                        disabled
                        className="bg-gray-100 dark:bg-gray-800"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="email">Email</Label>
                      <Input
                        id="email"
                        type="email"
                        value={userInfo.email}
                        onChange={(e) => handleInputChange('email', e.target.value)}
                        disabled={!isEditing}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="phone">Số điện thoại</Label>
                      <Input
                        id="phone"
                        value={userInfo.phone}
                        onChange={(e) => handleInputChange('phone', e.target.value)}
                        disabled={!isEditing}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="dateOfBirth">Ngày sinh</Label>
                      <Input
                        id="dateOfBirth"
                        type="date"
                        value={userInfo.dateOfBirth}
                        onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                        disabled={!isEditing}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="year">Năm nhập học</Label>
                      <Input
                        id="year"
                        value={userInfo.year}
                        disabled
                        className="bg-gray-100 dark:bg-gray-800"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="address">Địa chỉ</Label>
                    <Input
                      id="address"
                      value={userInfo.address}
                      onChange={(e) => handleInputChange('address', e.target.value)}
                      disabled={!isEditing}
                    />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Thông tin học tập</CardTitle>
                  <CardDescription>
                    Thông tin về chương trình học của bạn
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="major">Chuyên ngành</Label>
                      <Input
                        id="major"
                        value={userInfo.major}
                        disabled
                        className="bg-gray-100 dark:bg-gray-800"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="class">Lớp</Label>
                      <Input
                        id="class"
                        value={userInfo.class}
                        disabled
                        className="bg-gray-100 dark:bg-gray-800"
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="password" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Đổi mật khẩu</CardTitle>
              {/* <CardDescription>
                Thay đổi mật khẩu để bảo mật tài khoản của bạn
              </CardDescription> */}
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="currentPassword">Mật khẩu hiện tại</Label>
                <Input
                  id="currentPassword"
                  type="password"
                  value={passwordForm.currentPassword}
                  onChange={(e) => handlePasswordChange('currentPassword', e.target.value)}
                  placeholder="Nhập mật khẩu hiện tại"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="newPassword">Mật khẩu mới</Label>
                <Input
                  id="newPassword"
                  type="password"
                  value={passwordForm.newPassword}
                  onChange={(e) => handlePasswordChange('newPassword', e.target.value)}
                  placeholder="Nhập mật khẩu mới"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Xác nhận mật khẩu mới</Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  value={passwordForm.confirmPassword}
                  onChange={(e) => handlePasswordChange('confirmPassword', e.target.value)}
                  placeholder="Nhập lại mật khẩu mới"
                />
              </div>
              <div className="pt-4">
                <Button variant="outline" onClick={handleChangePassword}>
                  <Lock className="h-4 w-4 mr-2" />
                  Đổi mật khẩu
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* <TabsContent value="settings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Cài đặt tài khoản</CardTitle>
              <CardDescription>
                Quản lý các cài đặt tài khoản của bạn
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-black">
                      Thông báo email
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Nhận thông báo qua email
                    </p>
                  </div>
                  <Button variant="outline" size="sm">
                    Bật
                  </Button>
                </div>
                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-black">
                      Thông báo SMS
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Nhận thông báo qua SMS
                    </p>
                  </div>
                  <Button variant="outline" size="sm">
                    Tắt
                  </Button>
                </div>
                <div className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-black">
                      Chế độ riêng tư
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Ẩn thông tin cá nhân khỏi người khác
                    </p>
                  </div>
                  <Button variant="outline" size="sm">
                    Bật
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent> */}
      </Tabs>
    </div>
  );
};

export default ProfilePage;
