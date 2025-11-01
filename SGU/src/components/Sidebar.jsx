import React, { useState } from 'react';
import { Button } from './ui/button';
import { 
  X, Home, Calendar, Sun, Moon, GraduationCap, RefreshCw,
  ArrowLeft, ChevronRight, ChevronDown, LogOut, BookOpen,
  Award, FileText, Bell, User, Search, DollarSign, TrendingUp
} from 'lucide-react';
import { cn } from '../lib/utils';

const Sidebar = ({
  onBack,
  onRefresh,
  showBack = false,
  showRefresh = false,
  title = "Student",
  page = "home",
  onPageChange,
  onThemeToggle,
  isDark = false,
  isOpen = false,
  isAuth = false,
  onLogout,
  onToggle
}) => {
  const [expandedItems, setExpandedItems] = useState(['navigation']);

  const toggleExpanded = (item) => {
    setExpandedItems(prev =>
      prev.includes(item)
        ? prev.filter(i => i !== item)
        : [...prev, item]
    );
  };

  const navigationItems = [
    { id: 'home', label: 'Trang chủ', icon: Home, description: 'Trang chính của ứng dụng' },
    { id: 'registration', label: 'Đăng ký môn học', icon: BookOpen, description: 'Đăng ký và quản lý các môn học' },
    { id: 'schedule', label: 'Lịch học', icon: Calendar, description: 'Xem lịch học trong tuần' },
    { id: 'classes', label: 'Xem lớp học', icon: BookOpen, description: 'Xem thông tin lớp học và lịch học' },
    { id: 'progress', label: 'Tiến độ học', icon: TrendingUp, description: 'Xem lớp học đã hoàn thành và tiến độ học tập' },
    { id: 'documents', label: 'Đăng ký giấy', icon: FileText, description: 'Đăng ký các loại giấy tờ cần thiết' },
    { id: 'notifications', label: 'Nhận thông báo', icon: Bell, description: 'Xem thông báo và cập nhật mới' },
    { id: 'profile', label: 'Cập nhật thông tin cá nhân', icon: User, description: 'Thông tin cá nhân và đổi mật khẩu' },
    { id: 'lookup', label: 'Tra cứu', icon: Search, description: 'Tra cứu thông tin khoa, ngành, môn học' },
    { id: 'tuition', label: 'Học phí', icon: DollarSign, description: 'Xem và thanh toán học phí' }
  ];

  const actionItems = [
    ...(showBack && onBack ? [{ id: 'back', label: 'Quay lại', icon: ArrowLeft, action: onBack, description: 'Quay về trang trước' }] : []),
    ...(showRefresh && onRefresh ? [{ id: 'refresh', label: 'Làm mới', icon: RefreshCw, action: onRefresh, description: 'Tải lại dữ liệu' }] : []),
    ...(onThemeToggle ? [{ id: 'theme', label: isDark ? 'Chế độ sáng' : 'Chế độ tối', icon: isDark ? Sun : Moon, action: onThemeToggle, description: 'Chuyển đổi chế độ sáng/tối (tạm thời ko hoạt động)' }] : []),
    ...(isAuth && onLogout ? [{ id: 'logout', label: "Đăng xuất", icon: LogOut, action: onLogout, description: "Đăng xuất khỏi hệ thống" }] : [])
  ];

  return (
    <>
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 lg:hidden"
          onClick={onToggle}
        />
      )}

      <aside className={cn(
        "fixed top-0 left-0 z-50 h-full w-80 bg-gradient-to-b from-sky-50 to-teal-50 border-r border-teal-200 transform transition-transform duration-300 ease-in-out shadow-md lg:sticky lg:top-0 lg:translate-x-0",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-teal-200 bg-gradient-to-r from-sky-200 to-teal-100">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 bg-gradient-to-r from-teal-400 to-sky-500 rounded-xl flex items-center justify-center shadow-md">
                <GraduationCap className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-teal-700">
                  Student
                </h1>
                <p className="text-xs text-teal-600">{title}</p>
              </div>
            </div>
            <Button variant="ghost" size="sm" onClick={onToggle} className="lg:hidden p-2">
              <X className="h-5 w-5 text-teal-700" />
            </Button>
          </div>

          {/* Navigation */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            <div className="space-y-1">
              <button
                onClick={() => toggleExpanded('navigation')}
                className="flex items-center justify-between w-full p-2 text-sm font-semibold text-teal-800 hover:bg-teal-100 rounded-lg transition"
              >
                <span>Điều hướng</span>
                {expandedItems.includes('navigation') ? (
                  <ChevronDown className="h-4 w-4" />
                ) : (
                  <ChevronRight className="h-4 w-4" />
                )}
              </button>

              {expandedItems.includes('navigation') && (
                <div className="ml-3 space-y-1">
                  {navigationItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = page === item.id;
                    return (
                      <button
                        key={item.id}
                        onClick={() => {
                          onPageChange?.(item.id);
                          if (window.innerWidth < 1024) onToggle?.();
                        }}
                        className={cn(
                          "flex items-center gap-3 w-full p-3 rounded-lg transition-all group shadow-sm",
                          isActive
                            ? "bg-gradient-to-r from-teal-400 to-sky-500 text-white shadow-lg"
                            : "text-teal-800 hover:bg-teal-100"
                        )}
                      >
                        <Icon className={cn("h-5 w-5 flex-shrink-0", isActive ? "text-white" : "text-teal-500")} />
                        <div className="flex-1 text-left">
                          <div className="font-medium">{item.label}</div>
                          <div className="text-xs opacity-70">{item.description}</div>
                        </div>
                        {isActive && (
                          <div className="w-2 h-2 bg-white rounded-full" />
                        )}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Actions */}
            {actionItems.length > 0 && (
              <div className="space-y-1 pt-4 border-t border-teal-200">
                <button
                  onClick={() => toggleExpanded('actions')}
                  className="flex items-center justify-between w-full p-2 text-sm font-semibold text-teal-800 hover:bg-teal-100 rounded-lg transition"
                >
                  <span>Hành động</span>
                  {expandedItems.includes('actions') ? (
                    <ChevronDown className="h-4 w-4" />
                  ) : (
                    <ChevronRight className="h-4 w-4" />
                  )}
                </button>

                {expandedItems.includes('actions') && (
                  <div className="ml-3 space-y-1">
                    {actionItems.map((item) => {
                      const Icon = item.icon;
                      return (
                        <button
                          key={item.id}
                          onClick={() => {
                            item.action?.();
                            if (window.innerWidth < 1024) onToggle?.();
                          }}
                          className="flex items-center gap-3 w-full p-3 rounded-lg text-teal-800 hover:bg-teal-100 transition group"
                        >
                          <Icon className="h-5 w-5 text-teal-500" />
                          <div className="flex-1 text-left">
                            <div className="font-medium">{item.label}</div>
                            <div className="text-xs opacity-70">{item.description}</div>
                          </div>
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </aside>
    </>
  );
};

export { Sidebar };
