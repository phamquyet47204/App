import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { BookOpen, CheckCircle, XCircle, AlertTriangle, Clock, Users, MapPin, Calendar } from 'lucide-react';
import { registrationService } from '../services/registrationService';
import { readOnlyService } from '../services/readOnlyService';
import { toast } from 'react-hot-toast';
import { scheduleService } from '../services/scheduleService';
import { AuthStorage } from '../types/user';

const RegistrationPage = () => {
  const [availableCourses, setAvailableCourses] = useState([]);
  const [myRegistrations, setMyRegistrations] = useState([]);
  const [semesterInfo, setSemesterInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [showPrerequisites, setShowPrerequisites] = useState(false);
  const [showScheduleConflict, setShowScheduleConflict] = useState(false);
  const [prerequisitesResult, setPrerequisitesResult] = useState(null);
  const [scheduleConflictResult, setScheduleConflictResult] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Kiểm tra user có đăng nhập không
      const currentUser = AuthStorage.getCurrentUser();
      console.log('🔍 Current user in RegistrationPage:', currentUser);
      console.log('🔍 localStorage sgu_user:', localStorage.getItem('sgu_user'));
      
      if (!currentUser || !currentUser.username) {
        toast.error('Vui lòng đăng nhập để xem môn học');
        setLoading(false);
        return;
      }
      
      const [coursesResult, registrationsResult] = await Promise.all([
        registrationService.getAvailableCourses(),
        scheduleService.getMyRegistrations()
      ]);

      if (coursesResult.success) {
        console.log('📚 Courses result:', coursesResult.data);
        const courses = coursesResult.data.courses || coursesResult.data || [];
        console.log('📚 Parsed courses:', courses);
        console.log('📚 Number of courses:', courses.length);
        setAvailableCourses(courses);
        // Lưu semester info từ response
        if (coursesResult.data.semester) {
          setSemesterInfo(coursesResult.data.semester);
        }
      } else {
        console.error('❌ Failed to load courses:', coursesResult);
        toast.error(coursesResult.message || 'Không thể tải danh sách môn học');
      }

      if (registrationsResult.success) {
        setMyRegistrations(registrationsResult.data);
      }
    } catch (error) {
      console.error('Lỗi tải dữ liệu:', error);
      toast.error('Có lỗi xảy ra khi tải dữ liệu');
    } finally {
      setLoading(false);
    }
  };

  const handleCheckPrerequisites = async (course) => {
    // Hiển thị prerequisites từ course data (đã có trong response)
    if (course.prerequisites && course.prerequisites.length > 0) {
      const prerequisitesInfo = {
        prerequisites: course.prerequisites,
        prerequisitesMet: course.prerequisitesMet,
        canRegister: course.canRegister,
        missingPrerequisites: course.prerequisites.filter(p => !p.met)
      };
      setPrerequisitesResult(prerequisitesInfo);
      setShowPrerequisites(true);
    } else {
      // Nếu không có prerequisites trong course, gọi API
      try {
        const result = await registrationService.checkPrerequisites(course.subject?.subjectId);
        if (result.success) {
          setPrerequisitesResult(result.data);
          setShowPrerequisites(true);
        } else {
          toast.error(result.message);
        }
      } catch (error) {
        console.error('Lỗi kiểm tra môn tiên quyết:', error);
        toast.error('Có lỗi xảy ra khi kiểm tra môn tiên quyết');
      }
    }
  };

  const handleCheckScheduleConflict = async (courseClassId) => {
    try {
      const result = await registrationService.checkScheduleConflict(courseClassId);
      if (result.success) {
        setScheduleConflictResult(result.data);
        setShowScheduleConflict(true);
      } else {
        toast.error(result.message);
      }
    } catch (error) {
      console.error('Lỗi kiểm tra xung đột lịch học:', error);
      toast.error('Có lỗi xảy ra khi kiểm tra xung đột lịch học');
    }
  };

  const handleRegisterCourse = async (course) => {
    if (!course.canRegister) {
      if (!course.prerequisitesMet) {
        toast.error('Chưa đáp ứng môn tiên quyết');
      } else if (!course.registrationPeriod) {
        toast.error('Không trong thời gian đăng ký');
      } else if (course.availableSlots <= 0) {
        toast.error('Môn học đã hết chỗ');
      } else {
        toast.error('Không thể đăng ký môn học này');
      }
      return;
    }

    try {
      const registrationData = {
        courseClassId: course.courseClassId,
        semesterId: course.semester?.semesterId || semesterInfo?.semesterId
      };

      const result = await registrationService.createRegistration(registrationData);
      if (result.success) {
        toast.success('Đăng ký môn học thành công');
        fetchData(); // Refresh data
      } else {
        toast.error(result.message || 'Có lỗi xảy ra khi đăng ký');
      }
    } catch (error) {
      console.error('Lỗi đăng ký môn học:', error);
      toast.error('Có lỗi xảy ra khi đăng ký môn học');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'registered': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'pending': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'cancelled': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'registered': return 'Đã đăng ký';
      case 'pending': return 'Chờ duyệt';
      case 'cancelled': return 'Đã hủy';
      default: return 'Không xác định';
    }
  };

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dữ liệu...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          {/* <h1 className="text-3xl font-bold text-gray-900 dark:text-black">
            Đăng ký môn học
          </h1> */}
          {/* <p className="text-gray-600 dark:text-gray-300 mt-2">
            Đăng ký và quản lý các môn học trong học kỳ
          </p> */}
        </div>
        <Button variant="outline" onClick={fetchData}>
          <BookOpen className="h-4 w-4 mr-2" />
          Làm mới
        </Button>
      </div>

      <Tabs defaultValue="available" className="space-y-4">
        <TabsList>
          <TabsTrigger value="available">Môn học có thể đăng ký</TabsTrigger>
          <TabsTrigger value="registered">Đã đăng ký</TabsTrigger>
        </TabsList>

        <TabsContent value="available" className="space-y-4">
          {semesterInfo && (
            <Card className="mb-4">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-lg">{semesterInfo.semesterName}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {semesterInfo.isRegistrationOpen ? (
                        <span className="text-green-600">✓ Đang mở đăng ký</span>
                      ) : (
                        <span className="text-red-600">✗ Chưa mở đăng ký</span>
                      )}
                    </p>
                  </div>
                  <Badge className={semesterInfo.isRegistrationOpen ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                    {semesterInfo.isRegistrationOpen ? 'Mở' : 'Đóng'}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          )}
          
          {availableCourses.length === 0 ? (
            <Card>
              <CardContent className="pt-6 text-center py-10">
                <p className="text-gray-600 dark:text-gray-400">
                  {semesterInfo && !semesterInfo.isRegistrationOpen 
                    ? 'Chưa đến thời gian đăng ký' 
                    : 'Không có môn học nào có thể đăng ký'}
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {availableCourses.map((course) => (
                <Card 
                  key={course.courseClassId} 
                  className={`hover:shadow-lg transition-shadow ${
                    !course.canRegister ? 'opacity-75' : ''
                  }`}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <div className="space-y-1 flex-1">
                        <CardTitle className="text-lg">{course.courseName}</CardTitle>
                        <CardDescription className="text-sm">
                          {course.courseCode} • {course.subject?.subjectName || course.subject}
                        </CardDescription>
                      </div>
                      <Badge className={`${
                        course.availableSlots > 0 
                          ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
                          : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                      }`}>
                        {course.availableSlots}/{course.maxStudents} chỗ
                      </Badge>
                    </div>
                    {course.prerequisites && course.prerequisites.length > 0 && (
                      <div className="mt-2">
                        {course.prerequisitesMet ? (
                          <Badge className="bg-green-100 text-green-800 text-xs">
                            <CheckCircle className="h-3 w-3 mr-1 inline" />
                            Đã đáp ứng tiên quyết
                          </Badge>
                        ) : (
                          <Badge className="bg-yellow-100 text-yellow-800 text-xs">
                            <AlertTriangle className="h-3 w-3 mr-1 inline" />
                            Chưa đáp ứng tiên quyết
                          </Badge>
                        )}
                      </div>
                    )}
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="space-y-2">
                      <div className="flex items-center text-sm">
                        <Users className="h-4 w-4 mr-2 text-gray-500" />
                        <span className="text-gray-600 dark:text-gray-400">Giảng viên:</span>
                        <span className="ml-2 text-gray-900 dark:text-black">
                          {course.teacher?.name || course.teacher?.fullName || 'TBA'}
                        </span>
                      </div>
                      {(() => {
                        const formatSchedule = (schedule) => {
                          if (!schedule) return null;
                          
                          const dayMap = {
                            'monday': 'Thứ 2',
                            'tuesday': 'Thứ 3',
                            'wednesday': 'Thứ 4',
                            'thursday': 'Thứ 5',
                            'friday': 'Thứ 6',
                            'saturday': 'Thứ 7',
                            'sunday': 'Chủ nhật',
                            'Monday': 'Thứ 2',
                            'Tuesday': 'Thứ 3',
                            'Wednesday': 'Thứ 4',
                            'Thursday': 'Thứ 5',
                            'Friday': 'Thứ 6',
                            'Saturday': 'Thứ 7',
                            'Sunday': 'Chủ nhật'
                          };
                          
                          const dayOfWeek = schedule.dayOfWeekDisplay || schedule.dayOfWeek || '';
                          const dayName = dayMap[dayOfWeek] || dayMap[dayOfWeek?.charAt(0).toUpperCase() + dayOfWeek?.slice(1)] || dayOfWeek;
                          const startTime = schedule.startTime || '';
                          const endTime = schedule.endTime || '';
                          
                          if (dayName && startTime) {
                            return endTime 
                              ? `${dayName}, ${startTime} - ${endTime}`
                              : `${dayName}, ${startTime}`;
                          }
                          
                          return schedule.time || 'Chưa có lịch';
                        };
                        
                        const scheduleText = formatSchedule(course.schedule);
                        
                        return (
                          <div className="flex items-center text-sm">
                            <Calendar className="h-4 w-4 mr-2 text-gray-500" />
                            <span className="text-gray-600 dark:text-gray-400">Lịch học:</span>
                            <span className="ml-2 font-medium text-gray-900 dark:text-black">
                              {scheduleText || 'Chưa có lịch'}
                            </span>
                          </div>
                        );
                      })()}
                      <div className="flex items-center text-sm">
                        <MapPin className="h-4 w-4 mr-2 text-gray-500" />
                        <span className="text-gray-600 dark:text-gray-400">Phòng:</span>
                        <span className="ml-2 text-gray-900 dark:text-black">{course.room}</span>
                      </div>
                      <div className="flex items-center text-sm">
                        <BookOpen className="h-4 w-4 mr-2 text-gray-500" />
                        <span className="text-gray-600 dark:text-gray-400">Tín chỉ:</span>
                        <span className="ml-2 text-gray-900 dark:text-black">
                          {course.subject?.credits || course.credits}
                        </span>
                      </div>
                    </div>
                    
                    <div className="pt-3 border-t border-gray-200 dark:border-gray-700 space-y-2">
                      <div className="flex space-x-2">
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="flex-1"
                          onClick={() => handleCheckPrerequisites(course)}
                        >
                          <CheckCircle className="h-4 w-4 mr-1" />
                          Tiên quyết
                        </Button>
                        <Button 
                          size="sm" 
                          variant="outline" 
                          className="flex-1"
                          onClick={() => handleCheckScheduleConflict(course.courseClassId)}
                        >
                          <Clock className="h-4 w-4 mr-1" />
                          Kiểm tra lịch
                        </Button>
                      </div>
                      <Button 
                        variant={course.canRegister ? "default" : "outline"}
                        className="w-full" 
                        size="sm"
                        onClick={() => handleRegisterCourse(course)}
                        disabled={!course.canRegister}
                      >
                        {course.canRegister ? 'Đăng ký' : 'Không thể đăng ký'}
                      </Button>
                      {!course.canRegister && (
                        <p className="text-xs text-red-600 dark:text-red-400 text-center">
                          {!course.prerequisitesMet && 'Chưa đáp ứng tiên quyết'}
                          {course.prerequisitesMet && !course.registrationPeriod && 'Chưa đến thời gian đăng ký'}
                          {course.prerequisitesMet && course.registrationPeriod && course.availableSlots <= 0 && 'Đã hết chỗ'}
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="registered" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Môn học đã đăng ký</CardTitle>
              <CardDescription>
                Danh sách các môn học bạn đã đăng ký trong học kỳ
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {myRegistrations.map((registration) => (
                  <div key={registration.registrationId} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-black">
                          {registration.courseClass?.courseName}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {registration.courseClass?.courseCode} • {registration.semester?.semesterName}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Ngày đăng ký: {registration.registrationDate}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={getStatusColor(registration.status)}>
                          {getStatusText(registration.status)}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Prerequisites Modal */}
      {showPrerequisites && prerequisitesResult && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Kết quả kiểm tra môn tiên quyết</CardTitle>
                  <CardDescription>
                    Kiểm tra các môn học tiên quyết cần thiết
                  </CardDescription>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setShowPrerequisites(false)}
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                {prerequisitesResult.canRegister ? (
                  <CheckCircle className="h-6 w-6 text-green-500" />
                ) : (
                  <XCircle className="h-6 w-6 text-red-500" />
                )}
                <span className={`font-semibold ${
                  prerequisitesResult.canRegister ? 'text-green-600' : 'text-red-600'
                }`}>
                  {prerequisitesResult.canRegister ? 'Có thể đăng ký' : 'Không thể đăng ký'}
                </span>
              </div>
              
              {prerequisitesResult.prerequisites && prerequisitesResult.prerequisites.length > 0 && (
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-black mb-2">
                    Danh sách môn tiên quyết:
                  </h3>
                  <div className="space-y-2">
                    {prerequisitesResult.prerequisites.map((prereq, index) => (
                      <div key={index} className={`flex items-center space-x-2 p-2 rounded ${
                        prereq.met 
                          ? 'bg-green-50 dark:bg-green-900/20' 
                          : 'bg-red-50 dark:bg-red-900/20'
                      }`}>
                        {prereq.met ? (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        ) : (
                          <XCircle className="h-4 w-4 text-red-500" />
                        )}
                        <span className={`text-sm ${
                          prereq.met 
                            ? 'text-green-600 dark:text-green-400' 
                            : 'text-red-600 dark:text-red-400'
                        }`}>
                          {prereq.subjectName} ({prereq.subjectCode}) - {
                            prereq.met ? 'Đã đáp ứng' : 'Chưa đáp ứng'
                          }
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {prerequisitesResult.missingPrerequisites && prerequisitesResult.missingPrerequisites.length > 0 && (
                <div className="mt-4">
                  <h3 className="font-semibold text-gray-900 dark:text-black mb-2">
                    Môn học tiên quyết còn thiếu:
                  </h3>
                  <div className="space-y-2">
                    {prerequisitesResult.missingPrerequisites.map((prereq, index) => (
                      <div key={index} className="flex items-center space-x-2 p-2 bg-red-50 dark:bg-red-900/20 rounded">
                        <AlertTriangle className="h-4 w-4 text-red-500" />
                        <span className="text-sm text-red-600 dark:text-red-400">
                          {prereq.subjectName} ({prereq.subjectCode})
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Schedule Conflict Modal */}
      {showScheduleConflict && scheduleConflictResult && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Kết quả kiểm tra xung đột lịch học</CardTitle>
                  <CardDescription>
                    Kiểm tra xung đột với các môn học đã đăng ký
                  </CardDescription>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setShowScheduleConflict(false)}
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                {scheduleConflictResult.hasConflict ? (
                  <XCircle className="h-6 w-6 text-red-500" />
                ) : (
                  <CheckCircle className="h-6 w-6 text-green-500" />
                )}
                <span className={`font-semibold ${
                  scheduleConflictResult.hasConflict ? 'text-red-600' : 'text-green-600'
                }`}>
                  {scheduleConflictResult.hasConflict ? 'Có xung đột lịch học' : 'Không có xung đột'}
                </span>
              </div>
              
              {scheduleConflictResult.conflicts && scheduleConflictResult.conflicts.length > 0 && (
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-black mb-2">
                    Các môn học xung đột:
                  </h3>
                  <div className="space-y-2">
                    {scheduleConflictResult.conflicts.map((conflict, index) => (
                      <div key={index} className="flex items-center space-x-2 p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded">
                        <AlertTriangle className="h-4 w-4 text-yellow-500" />
                        <div>
                          <span className="text-sm text-yellow-600 dark:text-yellow-400">
                            {conflict.courseName} ({conflict.courseCode})
                          </span>
                          <p className="text-xs text-yellow-500 dark:text-yellow-400">
                            Lịch học: {conflict.schedule}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default RegistrationPage;
