import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Award, TrendingUp, BookOpen, Calendar, Download, Eye } from 'lucide-react';
import { gradesService } from '../services/gradesService';

const GradesPage = () => {
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [overallStats, setOverallStats] = useState({
    gpa: 0,
    totalCredits: 0,
    completedCredits: 0,
    averageGrade: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGrades = async () => {
      try {
        setLoading(true);
        const result = await gradesService.getMyGrades();
        if (result.success) {
          setSubjects(result.data);
          // Tính toán thống kê tổng quan
          const stats = calculateOverallStats(result.data);
          setOverallStats(stats);
        } else {
          console.error('Lỗi tải điểm:', result.message);
        }
      } catch (error) {
        console.error('Lỗi tải điểm:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchGrades();
  }, []);

  const calculateOverallStats = (grades) => {
    if (!grades || grades.length === 0) {
      return { gpa: 0, totalCredits: 0, completedCredits: 0, averageGrade: 0 };
    }

    const totalCredits = grades.reduce((sum, grade) => sum + (grade.subject?.credits || 0), 0);
    const completedCredits = grades.filter(grade => grade.isPassed).reduce((sum, grade) => sum + (grade.subject?.credits || 0), 0);
    const averageGrade = grades.reduce((sum, grade) => sum + (grade.totalScore || 0), 0) / grades.length;
    
    // Tính GPA từ gradePoints
    const gpa = grades.reduce((sum, grade) => {
      const gradePoint = grade.gradePoints || 0;
      const credits = grade.subject?.credits || 0;
      return sum + (gradePoint * credits);
    }, 0) / totalCredits;

    return {
      gpa: gpa || 0,
      totalCredits,
      completedCredits,
      averageGrade: averageGrade || 0
    };
  };

  const getGradeColor = (grade) => {
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

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải điểm số...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          {/* <h1 className="text-3xl font-bold text-gray-900 dark:text-black">
            Điểm và kết quả học tập
          </h1> */}
          {/* <p className="text-gray-600 dark:text-gray-300 mt-2">
            Theo dõi điểm số và kết quả học tập của bạn
          </p> */}
        </div>
        <Button variant="outline">
          <Download className="h-4 w-4 mr-2" />
          Xuất bảng điểm
        </Button>
      </div>

      {/* Overall Stats */}
      {/* <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">GPA</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {overallStats.gpa}
                </p>
              </div>
              <Award className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Tín chỉ đã hoàn thành</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {overallStats.completedCredits}/{overallStats.totalCredits}
                </p>
              </div>
              <BookOpen className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Điểm trung bình</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {overallStats.averageGrade}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Môn học</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {subjects.length}
                </p>
              </div>
              <Calendar className="h-8 w-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>
      </div> */}

      <Tabs defaultValue="subjects" className="space-y-4">
        <TabsList>
          <TabsTrigger value="subjects">Môn học</TabsTrigger>
          <TabsTrigger value="detailed">Chi tiết điểm</TabsTrigger>
          <TabsTrigger value="transcript">Bảng điểm</TabsTrigger>
        </TabsList>

        <TabsContent value="subjects" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {subjects.map((subject) => (
              <Card 
                key={subject.gradeId || subject.id} 
                className="hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => setSelectedSubject(subject)}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <CardTitle className="text-lg">{subject.subject?.subjectName || subject.subjectName}</CardTitle>
                      <CardDescription className="text-sm">
                        {subject.courseClass?.courseName || subject.courseClass} • {subject.semester?.semesterName || subject.semester}
                      </CardDescription>
                    </div>
                    <Badge className={getGradeBadgeColor(subject.letterGrade)}>
                      {subject.letterGrade}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Điểm tổng kết</span>
                    <span className={`text-2xl font-bold ${getGradeColor(subject.totalScore)}`}>
                      {subject.totalScore?.toFixed(1) || 'N/A'}
                    </span>
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {subject.semester?.semesterName || subject.semester}
                  </div>
                  <div className="flex items-center justify-between pt-2 border-t border-gray-200 dark:border-gray-700">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Xem chi tiết</span>
                    <Eye className="h-4 w-4 text-gray-400" />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="detailed" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Chi tiết điểm số</CardTitle>
              <CardDescription>
                Xem chi tiết điểm số của từng môn học
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {subjects.map((subject) => (
                  <div key={subject.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-black">
                          {subject.subject?.subjectName || subject.subjectName} ({subject.subject?.subjectCode || subject.subjectCode})
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {subject.semester?.semesterName || subject.semester}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className={`text-2xl font-bold ${getGradeColor(subject.totalScore)}`}>
                          {subject.totalScore?.toFixed(1) || 'N/A'}
                        </div>
                        <Badge className={getGradeBadgeColor(subject.letterGrade)}>
                          {subject.letterGrade}
                        </Badge>
                      </div>
                    </div>
                    <div className="space-y-2">
                    {Array.isArray(subject.grades) && subject.grades.map((grade, index) => (
                        <div key={index} className="flex items-center justify-between py-2 px-3 bg-gray-50 dark:bg-gray-800 rounded">
                          <div className="flex items-center space-x-3">
                            <span className="text-sm font-medium text-gray-900 dark:text-black">
                              {grade.type}
                            </span>
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              ({grade.weight}%)
                            </span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className={`font-semibold ${getGradeColor(grade.score)}`}>
                              {grade.score}/{grade.maxScore}
                            </span>
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {grade.date}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="transcript" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Bảng điểm</CardTitle>
              <CardDescription>
                Bảng điểm tổng hợp tất cả các môn học
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200 dark:border-gray-700">
                      <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-black">Môn học</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-black">Mã môn</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-black">Tín chỉ</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-black">Điểm</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-black">Xếp loại</th>
                    </tr>
                  </thead>
                  <tbody>
                    {subjects.map((subject) => (
                      <tr key={subject.gradeId || subject.id} className="border-b border-gray-200 dark:border-gray-700">
                        <td className="py-3 px-4 text-gray-900 dark:text-black">{subject.subject?.subjectName || subject.subjectName}</td>
                        <td className="py-3 px-4 text-gray-600 dark:text-gray-400">{subject.subject?.subjectCode || subject.subjectCode}</td>
                        <td className="py-3 px-4 text-gray-600 dark:text-gray-400">{subject.subject?.credits || subject.credits}</td>
                        <td className={`py-3 px-4 font-semibold ${getGradeColor(subject.totalScore)}`}>
                          {subject.totalScore?.toFixed(1) || 'N/A'}
                        </td>
                        <td className="py-3 px-4">
                          <Badge className={getGradeBadgeColor(subject.letterGrade)}>
                            {subject.letterGrade}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Subject Detail Modal */}
      {selectedSubject && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>{selectedSubject.subject?.subjectName || selectedSubject.subjectName}</CardTitle>
                  <CardDescription>{selectedSubject.subject?.subjectCode || selectedSubject.subjectCode} • {selectedSubject.semester?.semesterName || selectedSubject.semester}</CardDescription>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setSelectedSubject(null)}
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Tín chỉ</label>
                  <p className="text-gray-900 dark:text-black">{selectedSubject.subject?.credits || selectedSubject.credits}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Điểm tổng kết</label>
                  <p className={`text-2xl font-bold ${getGradeColor(selectedSubject.totalScore)}`}>
                    {selectedSubject.totalScore?.toFixed(1) || 'N/A'}
                  </p>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Chi tiết điểm</label>
                <div className="mt-2 space-y-2">
                  <div className="flex items-center justify-between py-2 px-3 bg-gray-50 dark:bg-gray-800 rounded">
                    <span className="text-sm font-medium text-gray-900 dark:text-black">Điểm chuyên cần</span>
                    <span className={`font-semibold ${getGradeColor(selectedSubject.attendanceScore)}`}>
                      {selectedSubject.attendanceScore?.toFixed(1) || 'N/A'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-2 px-3 bg-gray-50 dark:bg-gray-800 rounded">
                    <span className="text-sm font-medium text-gray-900 dark:text-black">Điểm bài tập</span>
                    <span className={`font-semibold ${getGradeColor(selectedSubject.assignmentScore)}`}>
                      {selectedSubject.assignmentScore?.toFixed(1) || 'N/A'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-2 px-3 bg-gray-50 dark:bg-gray-800 rounded">
                    <span className="text-sm font-medium text-gray-900 dark:text-black">Điểm giữa kỳ</span>
                    <span className={`font-semibold ${getGradeColor(selectedSubject.midtermScore)}`}>
                      {selectedSubject.midtermScore?.toFixed(1) || 'N/A'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-2 px-3 bg-gray-50 dark:bg-gray-800 rounded">
                    <span className="text-sm font-medium text-gray-900 dark:text-black">Điểm cuối kỳ</span>
                    <span className={`font-semibold ${getGradeColor(selectedSubject.finalScore)}`}>
                      {selectedSubject.finalScore?.toFixed(1) || 'N/A'}
                    </span>
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

export default GradesPage;
