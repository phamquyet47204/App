import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { Layout } from './components/Layout';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import ClassesPage from './pages/ClassesPage';
import GradesPage from './pages/GradesPage';
import DocumentsPage from './pages/DocumentsPage';
import NotificationsPage from './pages/NotificationsPage';
import ProfilePage from './pages/ProfilePage';
// import ProgressPage from './pages/ProgressPage';
import RegistrationPage from './pages/RegistrationPage';
import LookupPage from './pages/LookupPage';
import SchedulePage from './pages/SchedulePage';
import TuitionPage from './pages/TuitionPage';
import { authService } from './services/authService';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Kiểm tra trạng thái đăng nhập khi app khởi động
    const checkAuth = () => {
      const authenticated = authService.isAuthenticated();
      setIsAuthenticated(authenticated);
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const handleLoginSuccess = (user) => {
    setIsAuthenticated(true);
    setCurrentPage('home');
  };

  const handleLogout = async () => {
    const result = await authService.logout();
    if (result.success) {
      setIsAuthenticated(false);
      setCurrentPage('home');
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage />;
      case 'classes':
        return <ClassesPage />;
      case 'grades':
        return <GradesPage />;
      case 'documents':
        return <DocumentsPage />;
      case 'notifications':
        return <NotificationsPage />;
      case 'profile':
        return <ProfilePage />;
      // case 'progress':
      //   return <ProgressPage />;
      case 'registration':
        return <RegistrationPage />;
      case 'lookup':
        return <LookupPage />;
      case 'schedule':
        return <SchedulePage />;
      case 'tuition':
        return <TuitionPage />;
      default:
        return <HomePage />;
    }
  };

  const getPageTitle = () => {
    switch (currentPage) {
      case 'home':
        return 'Trang chủ';
      case 'classes':
        return 'Lớp học';
      case 'grades':
        return 'Điểm số';
      case 'documents':
        return 'Giấy tờ';
      case 'notifications':
        return 'Thông báo';
      case 'profile':
        return 'Thông tin cá nhân';
      case 'progress':
        return 'Tiến độ học';
      case 'registration':
        return 'Đăng ký môn học';
      case 'lookup':
        return 'Tra cứu';
      case 'schedule':
        return 'Lịch học';
      case 'tuition':
        return 'Học phí';
      default:
        return 'Student';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="App">
        <LoginPage onLoginSuccess={handleLoginSuccess} />
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#4ade80',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    );
  }

  return (
    <div className="App">
      <Layout
        page={currentPage}
        onPageChange={setCurrentPage}
        title={getPageTitle()}
        onLogout={handleLogout}
      >
        {renderPage()}
      </Layout>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#4ade80',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  );
}

export default App;
