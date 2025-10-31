import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { BookOpen, Clock, MapPin, User, Calendar } from 'lucide-react';
import { classesService } from '../services/classesService';

const ClassesPage = () => {
  const [classes, setClasses] = useState([]);
  const [selectedClass, setSelectedClass] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        setLoading(true);
        const result = await classesService.getClasses();
        if (result.success) {
          setClasses(result.data);
        } else {
          console.error("Lỗi tải lớp học:", result.message);
        }
      } catch (error) {
        console.error("Lỗi tải lớp học:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchClasses();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  if (loading) return <div className="text-center py-10">Đang tải lớp học...</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Lớp học của tôi</h1>
          {/* <p className="text-gray-500">Theo dõi danh sách lớp bạn đang học</p> */}
        </div>
        <Button variant="outline"><BookOpen className="h-4 w-4 mr-2" /> Thêm lớp học</Button>
      </div>

      <Tabs defaultValue="list" className="space-y-4">
        <TabsList>
          <TabsTrigger value="list">Danh sách lớp</TabsTrigger>
        </TabsList>

        <TabsContent value="list">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {classes.map((c) => (
              <Card key={c.courseClassId} onClick={() => setSelectedClass(c)} className="hover:shadow-lg cursor-pointer">
                <CardHeader>
                  <CardTitle>{c.courseName}</CardTitle>
                  <CardDescription>{c.courseCode} • {c.subject}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex items-center text-sm text-gray-600"><User className="h-4 w-4 mr-2" /> {c.teacher}</div>
                  <div className="flex items-center text-sm text-gray-600"><MapPin className="h-4 w-4 mr-2" /> {c.room}</div>
                  <div className="pt-2 border-t text-xs text-gray-500">{c.semester} • {c.currentStudents}/{c.maxStudents} SV</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {selectedClass && (
        <div className="fixed inset-0 bg-black/40 flex justify-center items-center">
          <Card className="max-w-lg w-full">
            <CardHeader>
              <div className="flex justify-between">
                <div>
                  <CardTitle>{selectedClass.courseName}</CardTitle>
                  <CardDescription>{selectedClass.courseCode}</CardDescription>
                </div>
                <Button variant="ghost" size="sm" onClick={() => setSelectedClass(null)}>×</Button>
              </div>
            </CardHeader>
            <CardContent>
              <p><strong>Giảng viên:</strong> {selectedClass.teacher}</p>
              <p><strong>Phòng học:</strong> {selectedClass.room}</p>
              <p><strong>Sinh viên:</strong> {selectedClass.currentStudents}/{selectedClass.maxStudents}</p>
              <p><strong>Học kỳ:</strong> {selectedClass.semester}</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default ClassesPage;
