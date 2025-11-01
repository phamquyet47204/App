import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { TrendingUp, Award, BookOpen, Calendar, Target, BarChart3, CheckCircle, Eye } from 'lucide-react';
import { progressService } from '../services/progressService';
import { gradesService } from '../services/gradesService';
import { toast } from 'react-hot-toast';

const ProgressPage = () => {
  const [loading, setLoading] = useState(true);
  const [progressData, setProgressData] = useState({
    current: {
      gpa: 0,
      creditsCompleted: 0,
      creditsTotal: 120,
      subjectsCompleted: 0,
      subjectsTotal: 40,
      attendanceRate: 0,
      averageGrade: 0
    },
    overall: {
      gpa: 0,
      creditsCompleted: 0,
      creditsTotal: 120,
      subjectsCompleted: 0,
      subjectsTotal: 40,
      attendanceRate: 0,
      averageGrade: 0
    }
  });
  const [availableCourses, setAvailableCourses] = useState([]);
  const [tuitionFees, setTuitionFees] = useState([]);
  const [completedCourses, setCompletedCourses] = useState([]);
  const [grades, setGrades] = useState([]);
  const [selectedGrade, setSelectedGrade] = useState(null);
  const [goals, setGoals] = useState([
    {
      id: 1,
      title: 'Hoàn thành 100% tín chỉ (data for FE test)',
      description: 'Đăng ký và hoàn thành toàn bộ tín chỉ theo kế hoạch học tập (data for FE test)',
      progress: 75,
      target: 100,
      status: 'in_progress',
      deadline: '2025-06-30',
    },
    {
      id: 2,
      title: 'Đạt GPA 8.5+',
      description: 'Duy trì điểm trung bình tích lũy trên 8.5',
      progress: 80,
      target: 100,
      status: 'in_progress',
      deadline: '2025-12-31',
    },
  ]);
  

  useEffect(() => {
    fetchProgressData();
  }, []);

  const fetchProgressData = async () => {
    try {
      setLoading(true);
      
      // Lấy điểm số để tính GPA
      const gradesResult = await gradesService.getMyGrades();
      console.log('📊 ProgressPage - Grades result:', gradesResult);
      
      if (gradesResult.success) {
        const gradesData = gradesResult.data.grades || [];
        console.log('📊 ProgressPage - Grades data:', gradesData);
        console.log('📊 ProgressPage - Grades count:', gradesData.length);
        console.log('📊 ProgressPage - GPA from API:', gradesResult.data.gpa);
        
        setGrades(gradesData); // Lưu grades để hiển thị
        
        // Sử dụng GPA từ backend (đã tính đúng với credits thực tế)
        const currentGPA = gradesResult.data.gpa || 0;
        // Tính credits từ grades thực tế
        const completedCredits = gradesResult.data.totalCredits || gradesData
          .filter(g => g.isPassed)
          .reduce((sum, g) => sum + (g.credits || 3), 0);
        const averageGrade = gradesData.length > 0 
          ? gradesData.reduce((sum, g) => sum + (g.averageScore || 0), 0) / gradesData.length 
          : 0;
        
        console.log('📊 ProgressPage - Setting GPA:', currentGPA);
        console.log('📊 ProgressPage - Setting credits:', completedCredits);
        
        setProgressData(prev => ({
          current: {
            ...prev.current,
            gpa: currentGPA,
            creditsCompleted: completedCredits,
            subjectsCompleted: gradesData.length,
            averageGrade: averageGrade || 0
          },
          overall: {
            ...prev.overall,
            gpa: currentGPA,
            creditsCompleted: completedCredits,
            subjectsCompleted: gradesData.length,
            averageGrade: averageGrade || 0
          }
        }));
      } else {
        console.error('❌ ProgressPage - Failed to fetch grades:', gradesResult.message);
      }

      // Lấy khóa học có thể đăng ký
      const coursesResult = await progressService.getAvailableCourses('S001'); // Giả sử student ID
      if (coursesResult.success) {
        setAvailableCourses(coursesResult.data);
      }

      // Lấy thông tin học phí
      const tuitionResult = await progressService.getTuitionFees();
      if (tuitionResult.success) {
        setTuitionFees(tuitionResult.data);
      }

      // Lấy danh sách lớp học đã hoàn thành
      const completedResult = await progressService.getCompletedCourses();
      if (completedResult.success) {
        setCompletedCourses(completedResult.data);
        // Cập nhật credits từ completed courses
        setProgressData(prev => ({
          ...prev,
          current: {
            ...prev.current,
            creditsCompleted: completedResult.totalCredits || prev.current.creditsCompleted,
            subjectsCompleted: completedResult.total || prev.current.subjectsCompleted
          },
          overall: {
            ...prev.overall,
            creditsCompleted: completedResult.totalCredits || prev.overall.creditsCompleted,
            subjectsCompleted: completedResult.total || prev.overall.subjectsCompleted
          }
        }));
      }

    } catch (error) {
      console.error('Lỗi tải dữ liệu tiến độ:', error);
      toast.error('Có lỗi xảy ra khi tải dữ liệu tiến độ');
    } finally {
      setLoading(false);
    }
  };

  const calculateGPA = (grades) => {
    if (!grades || grades.length === 0) return 0;
    
    // Chỉ tính GPA từ các môn đã pass
    const passedGrades = grades.filter(g => g.isPassed);
    if (passedGrades.length === 0) return 0;
    
    // Lấy credits từ subject, nếu không có thì dùng 3 làm mặc định
    const totalPoints = passedGrades.reduce((sum, grade) => {
      const credits = grade.credits || grade.subject?.credits || 3;
      const gradePoint = grade.gradePoint || 0;
      return sum + (gradePoint * credits);
    }, 0);
    
    const totalCredits = passedGrades.reduce((sum, grade) => {
      return sum + (grade.credits || grade.subject?.credits || 3);
    }, 0);
    
    return totalCredits > 0 ? totalPoints / totalCredits : 0;
  };

  // Helper functions for grades
  const getGradeColor = (grade) => {
    if (!grade) return 'text-gray-600 dark:text-gray-400';
    if (grade >= 9) return 'text-green-600 dark:text-green-400';
    if (grade >= 8) return 'text-blue-600 dark:text-blue-400';
    if (grade >= 7) return 'text-yellow-600 dark:text-yellow-400';
    if (grade >= 6) return 'text-orange-600 dark:text-orange-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getGradeBadgeColor = (letterGrade) => {
    switch (letterGrade) {
      case 'A': case 'A+': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'B': case 'B+': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      case 'C': case 'C+': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'D': case 'D+': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300';
      case 'F': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const semesterProgress = [
    {
      semester: 'HK1 2021-2022',
      gpa: 8.0,
      credits: 15,
      subjects: 5,
      status: 'completed'
    },
    {
      semester: 'HK2 2021-2022',
      gpa: 8.2,
      credits: 15,
      subjects: 5,
      status: 'completed'
    },
    {
      semester: 'HK1 2022-2023',
      gpa: 8.5,
      credits: 15,
      subjects: 5,
      status: 'completed'
    },
    {
      semester: 'HK2 2022-2023',
      gpa: 8.3,
      credits: 15,
      subjects: 5,
      status: 'completed'
    },
    {
      semester: 'HK1 2023-2024',
      gpa: 8.7,
      credits: 15,
      subjects: 5,
      status: 'completed'
    },
    {
      semester: 'HK2 2023-2024',
      gpa: 8.4,
      credits: 15,
      subjects: 5,
      status: 'completed'
    },
    {
      semester: 'HK1 2024-2025',
      gpa: 8.5,
      credits: 15,
      subjects: 5,
      status: 'current'
    }
  ];

  const achievements = [
    {
      id: 1,
      title: 'Học sinh giỏi test',
      description: 'Đạt danh hiệu học sinh giỏi học kỳ 1 năm 2024-2025 (data for FE test)',
      date: '2024-10-15 (data for FE test)',
      type: 'academic (data for FE test)',
      status: 'earned'
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'current': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      case 'earned': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'pending': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'in_progress': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed': return 'Hoàn thành';
      case 'current': return 'Hiện tại';
      case 'earned': return 'Đã đạt';
      case 'pending': return 'Chờ đạt';
      case 'in_progress': return 'Đang thực hiện';
      default: return 'Chưa xác định';
    }
  };

  const getAchievementIcon = (type) => {
    switch (type) {
      case 'academic': return <Award className="h-5 w-5 text-yellow-500" />;
      case 'attendance': return <Calendar className="h-5 w-5 text-blue-500" />;
      case 'grade': return <TrendingUp className="h-5 w-5 text-green-500" />;
      case 'graduation': return <BookOpen className="h-5 w-5 text-purple-500" />;
      default: return <Award className="h-5 w-5 text-gray-500" />;
    }
  };

  const currentData = progressData.overall;

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dữ liệu tiến độ...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-black">
          Theo dõi tiến độ học
        </h1>
        <p className="text-gray-600 dark:text-gray-300 mt-2">
          Theo dõi tiến độ học tập và thành tích của bạn
        </p>
      </div>


      {/* Progress Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">GPA</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {currentData.gpa && currentData.gpa > 0 ? currentData.gpa.toFixed(2) : '0.00'}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Tín chỉ</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {currentData.creditsCompleted}/{currentData.creditsTotal}
                </p>
              </div>
              <BookOpen className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="completed" className="space-y-4">
        <TabsList>
          <TabsTrigger value="completed">Lớp học đã hoàn thành</TabsTrigger>
          <TabsTrigger value="semester">Theo học kỳ</TabsTrigger>
          <TabsTrigger value="achievements">Thành tích</TabsTrigger>
          <TabsTrigger value="goals">Mục tiêu</TabsTrigger>
        </TabsList>

        {/* Grades Section - Direct display without tab */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Award className="h-5 w-5 text-blue-600" />
              Điểm số và kết quả học tập
            </CardTitle>
            <CardDescription>
              Danh sách điểm số của tất cả các môn học đã có điểm
            </CardDescription>
          </CardHeader>
          <CardContent>
            {grades.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Award className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-black mb-2">
                  Chưa có điểm số
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Bạn chưa có điểm số nào. Vui lòng liên hệ với giáo viên để biết thêm chi tiết.
                </p>
              </div>
            ) : (
              <div className="overflow-x-auto pb-2 -mx-2 px-2">
                <div className="flex gap-4 min-w-max">
                  {grades.map((grade) => (
                    <Card
                      key={grade.gradeId}
                      className="hover:shadow-lg transition-all cursor-pointer flex-shrink-0 w-72 border border-gray-200 hover:border-blue-300"
                      onClick={() => setSelectedGrade(grade)}
                    >
                      <CardHeader className="pb-3 bg-gradient-to-br from-blue-50 to-indigo-50 border-b border-blue-100">
                        <div className="flex items-start justify-between">
                          <div className="space-y-1 flex-1 min-w-0">
                            <CardTitle className="text-base font-semibold text-gray-900 truncate" title={grade.subject}>
                              {grade.subject}
                            </CardTitle>
                            <CardDescription className="text-xs text-gray-600 truncate">
                              {grade.courseName || grade.courseCode} • {grade.semester}
                            </CardDescription>
                          </div>
                          <Badge className={getGradeBadgeColor(grade.letterGrade)}>
                            {grade.letterGrade}
                          </Badge>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-2.5 pt-3">
                        <div className="flex items-center justify-between bg-gray-50 rounded-lg p-2">
                          <span className="text-xs font-medium text-gray-600">Điểm tổng kết</span>
                          <span className={`text-xl font-bold ${getGradeColor(grade.averageScore)}`}>
                            {grade.averageScore?.toFixed(1) || 'N/A'}
                          </span>
                        </div>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div className="bg-gray-50 rounded p-2">
                            <div className="text-gray-500 mb-0.5">Tín chỉ</div>
                            <div className="text-gray-900 font-semibold">{grade.credits}</div>
                          </div>
                          <div className="bg-blue-50 rounded p-2">
                            <div className="text-gray-500 mb-0.5">Điểm hệ 4</div>
                            <div className="text-blue-600 font-semibold">{grade.gradePoint?.toFixed(1) || 'N/A'}</div>
                          </div>
                        </div>
                        <div className="flex items-center justify-between pt-2 border-t border-gray-200 text-xs text-blue-600 hover:text-blue-700">
                          <span className="font-medium">Xem chi tiết</span>
                          <Eye className="h-3.5 w-3.5" />
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <TabsContent value="completed" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5 text-green-600" />
                Lớp học đã hoàn thành
              </CardTitle>
              <CardDescription>
                Danh sách các lớp học bạn đã hoàn thành ({completedCourses.length} lớp, {completedCourses.reduce((sum, c) => sum + (c.credits || 0), 0)} tín chỉ)
              </CardDescription>
            </CardHeader>
            <CardContent>
              {completedCourses.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <BookOpen className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                  <p>Chưa có lớp học nào đã hoàn thành</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {completedCourses.map((course, index) => (
                    <div
                      key={course.courseClassId || index}
                      className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <h4 className="font-semibold text-gray-900 dark:text-black">
                              {course.courseName}
                            </h4>
                            <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                              Đã hoàn thành
                            </Badge>
                          </div>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                            {course.courseCode} • {course.subject}
                          </p>
                          <div className="flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400">
                            <span>Học kỳ: {course.semester}</span>
                            <span>•</span>
                            <span>{course.credits} tín chỉ</span>
                            {course.teacher && (
                              <>
                                <span>•</span>
                                <span>GV: {course.teacher}</span>
                              </>
                            )}
                          </div>
                          {course.grade && (
                            <div className="mt-2 flex items-center gap-3">
                              {course.grade.letterGrade && (
                                <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                                  Điểm chữ: {course.grade.letterGrade}
                                </Badge>
                              )}
                              {course.grade.averageScore !== null && course.grade.averageScore !== undefined && (
                                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                  Điểm TB: {course.grade.averageScore.toFixed(1)}
                                </span>
                              )}
                              {course.grade.gradePoint !== null && course.grade.gradePoint !== undefined && (
                                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                  Điểm hệ 4: {course.grade.gradePoint.toFixed(1)}
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="semester" className="space-y-4">
          {/* Tiến độ theo học kỳ */}
          <Card>
            <CardHeader>
              <CardTitle>Tiến độ theo học kỳ</CardTitle>
              <CardDescription>
                Xem tiến độ học tập qua các học kỳ
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Group completed courses by semester */}
                {(() => {
                  const coursesBySemester = {};
                  completedCourses.forEach(course => {
                    const semester = course.semester || 'Không xác định';
                    if (!coursesBySemester[semester]) {
                      coursesBySemester[semester] = [];
                    }
                    coursesBySemester[semester].push(course);
                  });
                  
                  return Object.keys(coursesBySemester).length === 0 ? (
                    <div className="text-center py-4 text-gray-500">
                      <p>Chưa có dữ liệu theo học kỳ</p>
                    </div>
                  ) : (
                    Object.entries(coursesBySemester).map(([semester, courses]) => {
                      const totalCredits = courses.reduce((sum, c) => sum + (c.credits || 0), 0);
                      const avgGrade = courses
                        .filter(c => c.grade && c.grade.gradePoint !== null && c.grade.gradePoint !== undefined)
                        .reduce((sum, c, idx, arr) => {
                          const gpa = sum + (c.grade.gradePoint * c.credits);
                          return idx === arr.length - 1 ? gpa / totalCredits : gpa;
                        }, 0);
                      
                      return (
                        <div key={semester} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                          <div className="flex items-center justify-between mb-3">
                            <div>
                              <h3 className="font-semibold text-gray-900 dark:text-black">
                                {semester}
                              </h3>
                              <p className="text-sm text-gray-600 dark:text-gray-400">
                                {totalCredits} tín chỉ • {courses.length} môn học
                              </p>
                            </div>
                            <div className="flex items-center space-x-2">
                              <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                                Hoàn thành
                              </Badge>
                              {!isNaN(avgGrade) && avgGrade > 0 && (
                                <span className="text-lg font-bold text-gray-900 dark:text-black">
                                  GPA: {avgGrade.toFixed(2)}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      );
                    })
                  );
                })()}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="achievements" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Thành tích</CardTitle>
              <CardDescription>
                Các thành tích và danh hiệu đã đạt được
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {achievements.map((achievement) => (
                  <div key={achievement.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0">
                        {getAchievementIcon(achievement.type)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold text-gray-900 dark:text-black">
                            {achievement.title}
                          </h3>
                          <Badge className={getStatusColor(achievement.status)}>
                            {getStatusText(achievement.status)}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                          {achievement.description}
                        </p>
                        {achievement.date && (
                          <p className="text-xs text-gray-500 dark:text-gray-400">
                            {achievement.date}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="goals" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Mục tiêu học tập</CardTitle>
              <CardDescription>
                Theo dõi tiến độ thực hiện các mục tiêu học tập
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {goals.map((goal) => (
                  <div key={goal.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-black">
                          {goal.title}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {goal.description}
                        </p>
                      </div>
                      <Badge className={getStatusColor(goal.status)}>
                        {getStatusText(goal.status)}
                      </Badge>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Tiến độ</span>
                        <span className="text-gray-900 dark:text-black">
                          {goal.progress}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${goal.progress}%` }}
                        ></div>
                      </div>
                      <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                        <span>Hạn: {goal.deadline}</span>
                        <span>Mục tiêu: {goal.target}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Grade Detail Modal */}
      {selectedGrade && (
        <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center p-4 z-50" onClick={() => setSelectedGrade(null)}>
          <Card className="w-full max-w-2xl bg-white shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-200">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-gray-900">{selectedGrade.subject}</CardTitle>
                  <CardDescription className="text-gray-600">{selectedGrade.subjectCode} • {selectedGrade.semester}</CardDescription>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setSelectedGrade(null)}
                  className="text-gray-500 hover:text-gray-900"
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4 bg-white">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-600">Tín chỉ</label>
                  <p className="text-gray-900 text-lg font-semibold">{selectedGrade.credits}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600">Điểm tổng kết</label>
                  <p className={`text-2xl font-bold ${getGradeColor(selectedGrade.averageScore)}`}>
                    {selectedGrade.averageScore?.toFixed(1) || 'N/A'}
                  </p>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700 mb-3 block">Chi tiết điểm</label>
                <div className="mt-2 space-y-2">
                  {selectedGrade.assignmentScore !== null && selectedGrade.assignmentScore !== undefined && (
                    <div className="flex items-center justify-between py-3 px-4 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors">
                      <span className="text-sm font-medium text-gray-700">Điểm bài tập</span>
                      <span className={`font-semibold text-lg ${getGradeColor(selectedGrade.assignmentScore)}`}>
                        {selectedGrade.assignmentScore?.toFixed(1) || 'N/A'}
                      </span>
                    </div>
                  )}
                  {selectedGrade.midtermScore !== null && selectedGrade.midtermScore !== undefined && (
                    <div className="flex items-center justify-between py-3 px-4 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors">
                      <span className="text-sm font-medium text-gray-700">Điểm giữa kỳ</span>
                      <span className={`font-semibold text-lg ${getGradeColor(selectedGrade.midtermScore)}`}>
                        {selectedGrade.midtermScore?.toFixed(1) || 'N/A'}
                      </span>
                    </div>
                  )}
                  {selectedGrade.finalScore !== null && selectedGrade.finalScore !== undefined && (
                    <div className="flex items-center justify-between py-3 px-4 bg-gray-50 hover:bg-gray-100 rounded-lg border border-gray-200 transition-colors">
                      <span className="text-sm font-medium text-gray-700">Điểm cuối kỳ</span>
                      <span className={`font-semibold text-lg ${getGradeColor(selectedGrade.finalScore)}`}>
                        {selectedGrade.finalScore?.toFixed(1) || 'N/A'}
                      </span>
                    </div>
                  )}
                  <div className="flex items-center justify-between py-3 px-4 bg-blue-50 hover:bg-blue-100 rounded-lg border border-blue-200 transition-colors">
                    <span className="text-sm font-medium text-gray-700">Điểm trung bình</span>
                    <span className={`font-semibold text-xl ${getGradeColor(selectedGrade.averageScore)}`}>
                      {selectedGrade.averageScore?.toFixed(1) || 'N/A'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-3 px-4 bg-indigo-50 hover:bg-indigo-100 rounded-lg border border-indigo-200 transition-colors">
                    <span className="text-sm font-medium text-gray-700">Điểm hệ 4</span>
                    <span className="font-semibold text-lg text-blue-600">
                      {selectedGrade.gradePoint?.toFixed(1) || 'N/A'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-3 px-4 bg-purple-50 hover:bg-purple-100 rounded-lg border border-purple-200 transition-colors">
                    <span className="text-sm font-medium text-gray-700">Xếp loại</span>
                    <Badge className={getGradeBadgeColor(selectedGrade.letterGrade)}>
                      {selectedGrade.letterGrade}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between py-3 px-4 bg-green-50 hover:bg-green-100 rounded-lg border border-green-200 transition-colors">
                    <span className="text-sm font-medium text-gray-700">Trạng thái</span>
                    <Badge className={selectedGrade.isPassed ? 'bg-green-500 text-white hover:bg-green-600' : 'bg-red-500 text-white hover:bg-red-600'}>
                      {selectedGrade.isPassed ? 'Đạt' : 'Không đạt'}
                    </Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ProgressPage;
