import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Building, BookOpen, GraduationCap, Calendar, Search, Users, Clock } from 'lucide-react';
import { readOnlyService } from '../services/readOnlyService';
import { toast } from 'react-hot-toast';

const LookupPage = () => {
  const [departments, setDepartments] = useState([]);
  const [majors, setMajors] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [courseClasses, setCourseClasses] = useState([]);
  const [semesters, setSemesters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState('departments');

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const [departmentsResult, majorsResult, subjectsResult, courseClassesResult, semestersResult] = await Promise.all([
        readOnlyService.getDepartments(),
        readOnlyService.getMajors(),
        readOnlyService.getSubjects(),
        readOnlyService.getCourseClasses(),
        readOnlyService.getSemesters()
      ]);

      if (departmentsResult.success) {
        setDepartments(departmentsResult.data);
      }

      if (majorsResult.success) {
        setMajors(majorsResult.data);
      }

      if (subjectsResult.success) {
        setSubjects(subjectsResult.data);
      }

      if (courseClassesResult.success) {
        setCourseClasses(courseClassesResult.data);
      }

      if (semestersResult.success) {
        setSemesters(semestersResult.data);
      }
    } catch (error) {
      console.error('Lỗi tải dữ liệu:', error);
      toast.error('Có lỗi xảy ra khi tải dữ liệu');
    } finally {
      setLoading(false);
    }
  };

  const filterData = (data, fields) => {
    if (!searchQuery) return data;
    
    const query = searchQuery.toLowerCase();
    return data.filter(item =>
      fields.some(field => {
        const value = item[field];
        return value && value.toString().toLowerCase().includes(query);
      })
    );
  };

  const getStatusColor = (status) => {
    if (status === 'active' || status === 'available') {
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    }
    return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
  };

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dữ liệu tra cứu...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-black">
            Tra cứu thông tin
          </h1>
          {/* <p className="text-gray-600 dark:text-gray-300 mt-2">
            Tra cứu thông tin về khoa, ngành, môn học, lớp học và học kỳ
          </p> */}
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={fetchAllData}>
            <Search className="h-4 w-4 mr-2" />
            Làm mới
          </Button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
        <Input
          type="text"
          placeholder="Tìm kiếm..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10 w-full"
        />
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="departments">Khoa</TabsTrigger>
          <TabsTrigger value="majors">Ngành</TabsTrigger>
          <TabsTrigger value="subjects">Môn học</TabsTrigger>
          <TabsTrigger value="course-classes">Lớp học</TabsTrigger>
          <TabsTrigger value="semesters">Học kỳ</TabsTrigger>
        </TabsList>

        <TabsContent value="departments" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Building className="h-5 w-5 mr-2" />
                Danh sách khoa
              </CardTitle>
              <CardDescription>
                Thông tin các khoa trong trường
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filterData(departments, ['departmentName', 'departmentCode']).map((dept) => (
                  <Card key={dept.departmentId} className="hover:shadow-lg transition-shadow">
                    <CardContent className="p-4">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900 dark:text-black">
                            {dept.departmentName}
                          </h3>
                          <Badge className={getStatusColor(dept.status)}>
                            {dept.status}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Mã khoa: {dept.departmentCode}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="majors" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <GraduationCap className="h-5 w-5 mr-2" />
                Danh sách ngành
              </CardTitle>
              <CardDescription>
                Thông tin các ngành học trong trường
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filterData(majors, ['majorName', 'majorCode']).map((major) => (
                  <Card key={major.majorId} className="hover:shadow-lg transition-shadow">
                    <CardContent className="p-4">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900 dark:text-black">
                            {major.majorName}
                          </h3>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Mã ngành: {major.majorCode}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Khoa: {major.department}
                        </p>
                        <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                          <span>
                            <Clock className="h-4 w-4 inline mr-1" />
                            {major.durationYears} năm
                          </span>
                          <span>
                            <BookOpen className="h-4 w-4 inline mr-1" />
                            {major.totalCredits} tín chỉ
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="subjects" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <BookOpen className="h-5 w-5 mr-2" />
                Danh sách môn học
              </CardTitle>
              <CardDescription>
                Thông tin các môn học trong chương trình
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {filterData(subjects, ['subjectName', 'subjectCode']).map((subject) => (
                  <div key={subject.subjectId} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-black">
                          {subject.subjectName}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {subject.subjectCode}
                        </p>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Khoa</p>
                        <p className="text-gray-900 dark:text-black">{subject.department}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Tín chỉ</p>
                        <p className="text-gray-900 dark:text-black">{subject.credits}</p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Lý thuyết</p>
                        <p className="text-gray-900 dark:text-black">{subject.theoryHours}h</p>
                      </div>
                      <div>
                        <p className="text-gray-600 dark:text-gray-400">Thực hành</p>
                        <p className="text-gray-900 dark:text-black">{subject.practiceHours}h</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="course-classes" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Users className="h-5 w-5 mr-2" />
                Danh sách lớp học phần
              </CardTitle>
              <CardDescription>
                Thông tin các lớp học phần
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filterData(courseClasses, ['courseName', 'courseCode']).map((courseClass) => (
                  <Card key={courseClass.courseClassId} className="hover:shadow-lg transition-shadow">
                    <CardContent className="p-4">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900 dark:text-black">
                            {courseClass.courseName}
                          </h3>
                          <Badge className={courseClass.currentStudents >= courseClass.maxStudents 
                            ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
                            : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
                          }>
                            {courseClass.currentStudents}/{courseClass.maxStudents}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Mã lớp: {courseClass.courseCode}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Môn học: {courseClass.subject}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Giảng viên: {courseClass.teacher}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Học kỳ: {courseClass.semester}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Phòng: {courseClass.room}
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="semesters" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Calendar className="h-5 w-5 mr-2" />
                Danh sách học kỳ
              </CardTitle>
              <CardDescription>
                Thông tin các học kỳ trong hệ thống
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {filterData(semesters, ['semesterName', 'semesterCode', 'academicYear']).map((semester) => (
                  <Card key={semester.semesterId} className="hover:shadow-lg transition-shadow">
                    <CardContent className="p-4">
                      <div className="space-y-2">
                        <h3 className="font-semibold text-gray-900 dark:text-black">
                          {semester.semesterName}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Mã học kỳ: {semester.semesterCode}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Năm học: {semester.academicYear}
                        </p>
                        <div className="flex items-center space-x-2 text-xs text-gray-600 dark:text-gray-400">
                          <span>Từ: {semester.startDate ? new Date(semester.startDate).toLocaleDateString('vi-VN') : 'N/A'}</span>
                          <span>•</span>
                          <span>Đến: {semester.endDate ? new Date(semester.endDate).toLocaleDateString('vi-VN') : 'N/A'}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default LookupPage;
