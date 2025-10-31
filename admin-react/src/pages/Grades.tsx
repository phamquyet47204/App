import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Award, User, Search } from 'lucide-react';

interface Grade {
  gradeId: string;
  student: string;
  subject: string;
  teacher: string;
  semester: string;
  assignmentScore?: number;
  midtermScore?: number;
  finalScore?: number;
  averageScore?: number;
  letterGrade: string;
  gradePoint: number;
  isPassed: boolean;
}

interface StudentGPA {
  studentName: string;
  studentId: string;
  gpa: number;
  totalCredits: number;
  completedCredits: number;
}

const Grades: React.FC = () => {
  const [grades, setGrades] = useState<Grade[]>([]);
  const [studentGPAs, setStudentGPAs] = useState<StudentGPA[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState<'grades' | 'gpa'>('gpa');

  useEffect(() => {
    fetchGrades();
    fetchStudentGPAs();
  }, []);

  const fetchGrades = async () => {
    try {
      const sessionKey = localStorage.getItem('session_key');
      const response = await axios.get('http://127.0.0.1:8000/api/crud/grades/', {
        headers: {
          'Authorization': `Session ${sessionKey}`,
          'X-Session-Key': sessionKey
        }
      });
      const data = response.data.grades || response.data;
      setGrades(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching grades:', error);
      setGrades([]);
    }
  };

  const fetchStudentGPAs = async () => {
    try {
      const sessionKey = localStorage.getItem('session_key');
      const response = await axios.get('http://127.0.0.1:8000/api/crud/users/?user_type=student', {
        headers: {
          'Authorization': `Session ${sessionKey}`,
          'X-Session-Key': sessionKey
        }
      });
      const students = response.data.users || response.data;
      
      // Calculate GPA for each student (mock calculation)
      const gpaData = students.map((student: any) => ({
        studentName: student.full_name,
        studentId: student.username,
        gpa: (Math.random() * 2 + 2).toFixed(2), // Mock GPA between 2.0-4.0
        totalCredits: Math.floor(Math.random() * 50 + 100), // Mock total credits
        completedCredits: Math.floor(Math.random() * 30 + 80) // Mock completed credits
      }));
      
      setStudentGPAs(gpaData);
    } catch (error) {
      console.error('Error fetching student GPAs:', error);
      setStudentGPAs([]);
    } finally {
      setLoading(false);
    }
  };

  const filteredGrades = grades.filter(grade =>
    grade.student.toLowerCase().includes(searchTerm.toLowerCase()) ||
    grade.subject.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredGPAs = studentGPAs.filter(student =>
    student.studentName.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.studentId.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div>Đang tải...</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1>Quản lý Điểm số</h1>
        <p>Xem điểm số và GPA của sinh viên</p>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button 
              onClick={() => setActiveTab('gpa')}
              style={{
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '6px',
                background: activeTab === 'gpa' ? '#3b82f6' : '#f3f4f6',
                color: activeTab === 'gpa' ? 'white' : '#374151',
                cursor: 'pointer'
              }}
            >
              GPA Sinh viên
            </button>
            <button 
              onClick={() => setActiveTab('grades')}
              style={{
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '6px',
                background: activeTab === 'grades' ? '#3b82f6' : '#f3f4f6',
                color: activeTab === 'grades' ? 'white' : '#374151',
                cursor: 'pointer'
              }}
            >
              Chi tiết điểm
            </button>
          </div>
        </div>

        <div style={{ marginBottom: '1rem', position: 'relative' }}>
          <Search size={20} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: '#64748b' }} />
          <input
            type="text"
            placeholder={activeTab === 'gpa' ? 'Tìm kiếm sinh viên...' : 'Tìm kiếm điểm...'}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              padding: '0.75rem 0.75rem 0.75rem 2.5rem',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '1rem'
            }}
          />
        </div>

        {activeTab === 'gpa' ? (
          filteredGPAs.length > 0 ? (
            <table className="table">
              <thead>
                <tr>
                  <th>Mã SV</th>
                  <th>Họ tên</th>
                  <th>GPA</th>
                  <th>Tín chỉ hoàn thành</th>
                  <th>Tổng tín chỉ</th>
                  <th>Xếp loại</th>
                </tr>
              </thead>
              <tbody>
                {filteredGPAs.map((student, index) => {
                  const gpaValue = parseFloat(student.gpa.toString());
                  let classification = 'Trung bình';
                  let classColor = '#f59e0b';
                  
                  if (gpaValue >= 3.6) {
                    classification = 'Xuất sắc';
                    classColor = '#10b981';
                  } else if (gpaValue >= 3.2) {
                    classification = 'Giỏi';
                    classColor = '#3b82f6';
                  } else if (gpaValue >= 2.5) {
                    classification = 'Khá';
                    classColor = '#8b5cf6';
                  } else if (gpaValue < 2.0) {
                    classification = 'Yếu';
                    classColor = '#ef4444';
                  }
                  
                  return (
                    <tr key={index}>
                      <td>{student.studentId}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <User size={16} color="#64748b" />
                          {student.studentName}
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <Award size={16} color={classColor} />
                          <strong style={{ color: classColor }}>{student.gpa}</strong>
                        </div>
                      </td>
                      <td>{student.completedCredits}</td>
                      <td>{student.totalCredits}</td>
                      <td>
                        <span style={{
                          padding: '0.25rem 0.5rem',
                          borderRadius: '4px',
                          fontSize: '0.875rem',
                          backgroundColor: `${classColor}20`,
                          color: classColor,
                          fontWeight: '500'
                        }}>
                          {classification}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              <Award size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
              <p>Chưa có dữ liệu GPA</p>
            </div>
          )
        ) : (
          filteredGrades.length > 0 ? (
            <table className="table">
              <thead>
                <tr>
                  <th>Sinh viên</th>
                  <th>Môn học</th>
                  <th>Giảng viên</th>
                  <th>Học kỳ</th>
                  <th>Điểm TB</th>
                  <th>Điểm chữ</th>
                  <th>Điểm số</th>
                  <th>Kết quả</th>
                </tr>
              </thead>
              <tbody>
                {filteredGrades.map((grade) => (
                  <tr key={grade.gradeId}>
                    <td>{grade.student}</td>
                    <td>{grade.subject}</td>
                    <td>{grade.teacher}</td>
                    <td>{grade.semester}</td>
                    <td>{grade.averageScore?.toFixed(1) || 'N/A'}</td>
                    <td>
                      <span style={{
                        padding: '0.25rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.875rem',
                        backgroundColor: grade.letterGrade === 'A' ? '#d1fae5' : 
                                       grade.letterGrade === 'B' ? '#dbeafe' :
                                       grade.letterGrade === 'C' ? '#fef3c7' : '#fee2e2',
                        color: grade.letterGrade === 'A' ? '#065f46' : 
                               grade.letterGrade === 'B' ? '#1e40af' :
                               grade.letterGrade === 'C' ? '#92400e' : '#991b1b',
                        fontWeight: '600'
                      }}>
                        {grade.letterGrade}
                      </span>
                    </td>
                    <td>{grade.gradePoint.toFixed(1)}</td>
                    <td>
                      <span style={{
                        padding: '0.25rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.875rem',
                        backgroundColor: grade.isPassed ? '#d1fae5' : '#fee2e2',
                        color: grade.isPassed ? '#065f46' : '#991b1b'
                      }}>
                        {grade.isPassed ? 'Đậu' : 'Rớt'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
              <Award size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
              <p>Chưa có dữ liệu điểm</p>
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default Grades;