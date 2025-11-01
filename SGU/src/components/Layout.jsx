import React, { useEffect, useState } from 'react';
import { Sidebar } from './Sidebar';
import { Button } from './ui/button';
import { Menu } from 'lucide-react';
import { AuthStorage } from '../types/user';
import { toast } from 'react-hot-toast';

const Layout = ({
  children,
  onBack,
  onRefresh,
  showBack = false,
  showRefresh = false,
  page,
  onPageChange,
  title,
  onLogout,
}) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const loggedInUser = AuthStorage.isLoggedIn();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleLogout = async () => {
    try {
      if (onLogout) {
        await onLogout();
      } else {
        AuthStorage.logout();
        toast.success("Đăng xuất thành công");
        window.location.reload();
      }
    } catch (error) {
      toast.error("Có lỗi xảy ra khi đăng xuất");
    }
  };

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
    }
  }, []);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
    if (!isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden hidden md:block">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-50 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-50 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-pink-50 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"></div>
      </div>

      <div className="relative z-10 flex w-full">
        {/* Sidebar */}
        <Sidebar
          onBack={onBack}
          onRefresh={onRefresh}
          showBack={showBack}
          showRefresh={showRefresh}
          page={page}
          onPageChange={onPageChange}
          title={title}
          onThemeToggle={toggleTheme}
          isDark={isDarkMode}
          isOpen={sidebarOpen}
          isAuth={loggedInUser}
          onLogout={handleLogout}
          onToggle={toggleSidebar}
        />

        {/* Main Content */}
        <div className="flex-1 w-full min-w-0 lg:ml-0">
          {/* Mobile Header */}
          <div className="lg:hidden sticky top-0 z-40 bg-white/95 backdrop-blur-sm border-b border-gray-200">
            <div className="flex items-center justify-between p-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleSidebar}
                className="p-2"
              >
                <Menu className="h-5 w-5" />
              </Button>
              <h1 className="text-lg font-semibold text-gray-900 truncate">
                {title}
              </h1>
              <div className="w-10" /> {/* Spacer for centering */}
            </div>
          </div>

          {/* Content */}
          <main className="relative w-full min-w-0">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
};

export { Layout };
