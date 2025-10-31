import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Calendar, Clock, MapPin, Users, BookOpen, Download } from 'lucide-react';
import { scheduleService } from '../services/scheduleService';
import { toast } from 'react-hot-toast';

const SchedulePage = () => {
  const [mySchedule, setMySchedule] = useState([]);
  // const [myRegistrations, setMyRegistrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDay, setSelectedDay] = useState('all');

  const daysOfWeek = [
    { id: 'all', label: 'Tất cả', value: 'all' },
    { id: 'monday', label: 'Thứ 2', value: 'monday' },
    { id: 'tuesday', label: 'Thứ 3', value: 'tuesday' },
    { id: 'wednesday', label: 'Thứ 4', value: 'wednesday' },
    { id: 'thursday', label: 'Thứ 5', value: 'thursday' },
    { id: 'friday', label: 'Thứ 6', value: 'friday' },
    { id: 'saturday', label: 'Thứ 7', value: 'saturday' },
    { id: 'sunday', label: 'Chủ nhật', value: 'sunday' }
  ];

  useEffect(() => {
    fetchScheduleData();
  }, []);

  const fetchScheduleData = async () => {
    try {
      setLoading(true);
      const [scheduleResult] = await Promise.all([
        scheduleService.getMySchedule()
        // scheduleService.getMyRegistrations()
      ]);

      if (scheduleResult.success) {
        setMySchedule(scheduleResult.data);
      }

      // if (registrationsResult.success) {
      //   setMyRegistrations(registrationsResult.data);
      // }
    } catch (error) {
      console.error('Lỗi tải lịch học:', error);
      toast.error('Có lỗi xảy ra khi tải lịch học');
    } finally {
      setLoading(false);
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

  const getDayColor = (dayOfWeek) => {
    const colors = {
      'monday': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
      'tuesday': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
      'wednesday': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
      'thursday': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
      'friday': 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300',
      'saturday': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300',
      'sunday': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
    };
    return colors[dayOfWeek] || 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
  };

  const getDayLabel = (dayOfWeek) => {
    const labels = {
      'monday': 'Thứ 2',
      'tuesday': 'Thứ 3',
      'wednesday': 'Thứ 4',
      'thursday': 'Thứ 5',
      'friday': 'Thứ 6',
      'saturday': 'Thứ 7',
      'sunday': 'Chủ nhật'
    };
    return labels[dayOfWeek] || dayOfWeek;
  };

  const filteredSchedule = selectedDay === 'all' 
    ? mySchedule 
    : mySchedule.filter(course => course.dayOfWeek === selectedDay);

  const scheduleByDay = daysOfWeek.slice(1).map(day => ({
    ...day,
    courses: mySchedule.filter(course => course.dayOfWeek === day.value)
  }));

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải lịch học...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-black">
            Lịch học
          </h1>
          {/* <p className="text-gray-600 dark:text-gray-300 mt-2">
            Xem lịch học và quản lý các môn học đã đăng ký
          </p> */}
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={fetchScheduleData}>
            <Calendar className="h-4 w-4 mr-2" />
            Làm mới
          </Button>
          {/* <Button>
            <Download className="h-4 w-4 mr-2" />
            Xuất lịch
          </Button> */}
        </div>
      </div>

      <Tabs defaultValue="weekly" className="space-y-4">
        {/* <TabsList>
          <TabsTrigger value="weekly">Lịch tuần</TabsTrigger>
          <TabsTrigger value="list">Danh sách lịch học</TabsTrigger>
          <TabsTrigger value="registrations">Danh sách đăng ký</TabsTrigger>
        </TabsList> */}

        <TabsContent value="weekly" className="space-y-4">
          {/* Day Filter */}
          <div className="flex flex-wrap gap-2">
            {daysOfWeek.map((day) => (
              <Button
                key={day.id}
                variant={selectedDay === day.value ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedDay(day.value)}
              >
                {day.label}
              </Button>
            ))}
          </div>

          {/* Weekly Schedule Grid */}
          <div className="grid grid-cols-1 md:grid-cols-7 gap-4">
            {scheduleByDay.map((day) => (
              <Card key={day.id} className="min-h-[400px]">
                <CardHeader className="pb-3">
                  <CardTitle className="text-center">
                    <Badge className={getDayColor(day.value)}>
                      {day.label}
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  {day.courses.length > 0 ? (
                    day.courses.map((course, index) => (
                      <div key={index} className="p-3 bg-gray-50 dark:bg-gray-100 rounded-lg">
                        <div className="space-y-1">
                          <h4 className="font-semibold text-sm text-gray-900 dark:text-black">
                            {course.courseName}
                          </h4>
                          <p className="text-xs text-gray-600 dark:text-gray-800">
                            {course.courseCode}
                          </p>
                          <div className="flex items-center text-xs text-gray-500 dark:text-gray-800">
                            <Clock className="h-3 w-3 mr-1" />
                            {course.startTime} - {course.endTime}
                          </div>
                          <div className="flex items-center text-xs text-gray-500 dark:text-gray-800">
                            <MapPin className="h-3 w-3 mr-1" />
                            {course.room}
                          </div>
                          <div className="flex items-center text-xs text-gray-500 dark:text-gray-800">
                            <Users className="h-3 w-3 mr-1" />
                            {course.teacher}
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center text-gray-500 dark:text-gray-400 text-sm py-8">
                      Không có lịch học
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* <TabsContent value="list" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Danh sách lịch học</CardTitle>
              <CardDescription>
                Tất cả các môn học trong lịch học của bạn
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filteredSchedule.map((course, index) => (
                  <div key={index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-black">
                          {course.courseName}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {course.courseCode}
                        </p>
                      </div>
                      <Badge className={getDayColor(course.dayOfWeek)}>
                        {getDayLabel(course.dayOfWeek)}
                      </Badge>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div className="flex items-center">
                        <Clock className="h-4 w-4 mr-2 text-gray-500" />
                        <div>
                          <p className="text-gray-600 dark:text-gray-400">Thời gian</p>
                          <p className="text-gray-900 dark:text-black">
                            {course.startTime} - {course.endTime}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-2 text-gray-500" />
                        <div>
                          <p className="text-gray-600 dark:text-gray-400">Phòng</p>
                          <p className="text-gray-900 dark:text-black">{course.room}</p>
                        </div>
                      </div>
                      <div className="flex items-center">
                        <Users className="h-4 w-4 mr-2 text-gray-500" />
                        <div>
                          <p className="text-gray-600 dark:text-gray-400">Giảng viên</p>
                          <p className="text-gray-900 dark:text-black">{course.teacher}</p>
                        </div>
                      </div>
                      <div className="flex items-center">
                        <BookOpen className="h-4 w-4 mr-2 text-gray-500" />
                        <div>
                          <p className="text-gray-600 dark:text-gray-400">Mã lớp</p>
                          <p className="text-gray-900 dark:text-black">{course.courseClassId}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent> */}

        {/* <TabsContent value="registrations" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Danh sách đăng ký</CardTitle>
              <CardDescription>
                Theo dõi trạng thái đăng ký các môn học
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
        </TabsContent> */}
      </Tabs>
    </div>
  );
};

export default SchedulePage;
