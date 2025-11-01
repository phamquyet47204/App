import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Bell, CheckCircle, AlertCircle, Info, XCircle, Filter, Search } from 'lucide-react';
import { notificationsService } from '../services/notificationsService';
import { toast } from 'react-hot-toast';

const NotificationsPage = () => {
  const [selectedNotification, setSelectedNotification] = useState(null);
  const [filter, setFilter] = useState('all');
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const result = await notificationsService.getMyNotifications();
      if (result.success) {
        setNotifications(result.data);
      } else {
        console.error('Lỗi tải thông báo:', result.message);
        toast.error('Không thể tải danh sách thông báo');
      }
    } catch (error) {
      console.error('Lỗi tải thông báo:', error);
      toast.error('Có lỗi xảy ra khi tải thông báo');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (notificationId) => {
    try {
      const result = await notificationsService.markNotificationAsRead(notificationId);
      if (result.success) {
        toast.success('Đánh dấu thông báo đã đọc');
        // Update local state
        setNotifications(prev => 
          prev.map(notif => 
            notif.notificationId === notificationId || notif.id === notificationId
              ? { ...notif, isRead: true }
              : notif
          )
        );
      } else {
        toast.error(result.message);
      }
    } catch (error) {
      console.error('Lỗi đánh dấu đã đọc:', error);
      toast.error('Có lỗi xảy ra khi đánh dấu đã đọc');
    }
  };

  const categories = [
    { id: 'all', label: 'Tất cả', count: notifications.length },
    { id: 'exam', label: 'Thi cử', count: notifications.filter(n => n.category === 'exam').length },
    { id: 'grade', label: 'Điểm số', count: notifications.filter(n => n.category === 'grade').length },
    { id: 'schedule', label: 'Lịch học', count: notifications.filter(n => n.category === 'schedule').length },
    { id: 'document', label: 'Giấy tờ', count: notifications.filter(n => n.category === 'document').length },
    { id: 'payment', label: 'Thanh toán', count: notifications.filter(n => n.category === 'payment').length }
  ];

  const getTypeIcon = (type) => {
    switch (type) {
      case 'success': return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'warning': return <AlertCircle className="h-5 w-5 text-yellow-500" />;
      case 'error': return <XCircle className="h-5 w-5 text-red-500" />;
      case 'info': return <Info className="h-5 w-5 text-blue-500" />;
      default: return <Bell className="h-5 w-5 text-gray-500" />;
    }
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'success': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'warning': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      case 'info': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const getTypeText = (type) => {
    switch (type) {
      case 'success': return 'Thành công';
      case 'warning': return 'Cảnh báo';
      case 'error': return 'Lỗi';
      case 'info': return 'Thông tin';
      default: return 'Khác';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Vừa xong';
    if (diffInHours < 24) return `${diffInHours} giờ trước`;
    if (diffInHours < 48) return 'Hôm qua';
    return date.toLocaleDateString('vi-VN');
  };

  const filteredNotifications = filter === 'all' 
    ? notifications 
    : notifications.filter(n => n.category === filter);

  const unreadCount = notifications.filter(n => !n.isRead).length;

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải thông báo...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Button variant="outline" size="sm">
            <Filter className="h-4 w-4 mr-2" />
            Lọc
          </Button>
          <Button variant="outline" size="sm">
            <Search className="h-4 w-4 mr-2" />
            Tìm kiếm
          </Button>
        </div>
      </div>

      {/* Stats */}
      <Tabs defaultValue="all" className="space-y-4">
        <div className="overflow-x-auto scrollbar-hide">
          <TabsList className="flex sm:grid sm:grid-cols-6 bg-gray-50 dark:bg-white-100/30 rounded-lg p-1 gap-1 min-w-max sm:min-w-0">
            {categories.map(cat => (
              <TabsTrigger
                key={cat.id}
                value={cat.id}
                onClick={() => setFilter(cat.id)}
                className="
                  data-[state=active]:bg-gray-400 data-[state=active]:text-white 
                  rounded-md px-4 py-2 whitespace-nowrap transition-all 
                  flex-shrink-0 text-sm sm:text-base
                "
              >
                {cat.label} ({cat.count})
              </TabsTrigger>
            ))}
          </TabsList>
        </div>
        <style jsx>{`
          .scrollbar-hide::-webkit-scrollbar {
            display: none;
          }
          .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
          }
        `}</style>

        <TabsContent value={filter} className="space-y-4">
          <div className="space-y-4">
            {filteredNotifications.map((notification) => (
              <Card 
                key={notification.notificationId || notification.id} 
                className={`hover:shadow-lg transition-shadow cursor-pointer ${
                  !notification.isRead ? 'border-l-4 border-l-blue-500 bg-blue-50/50 dark:bg-blue-950/20' : ''
                }`}
                onClick={() => setSelectedNotification(notification)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      {getTypeIcon(notification.notificationType || notification.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className={`font-semibold ${
                          !notification.isRead ? 'text-gray-900 dark:text-black' : 'text-black-100 dark:text-black-300'
                        }`}>
                          {notification.title}
                        </h3>
                        <div className="flex items-center space-x-2">
                          {notification.priority === 'high' && (
                            <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">
                              Quan trọng
                            </Badge>
                          )}
                          <Badge className={getTypeColor(notification.notificationType || notification.type)}>
                            {getTypeText(notification.notificationType || notification.type)}
                          </Badge>
                        </div>
                      </div>
                      <p className={`text-sm mb-2 ${
                        !notification.isRead ? '' : 'text-black-600 dark:text-black-400'
                      }`}>
                        {notification.content || notification.message}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          {formatDate(notification.deliveredAt || notification.scheduledAt || notification.createdAt)}
                        </span>
                        {!notification.isRead && (
                          <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Notification Detail Modal */}
      {selectedNotification && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {getTypeIcon(selectedNotification.type)}
                  <div>
                    <CardTitle>{selectedNotification.title}</CardTitle>
                    <CardDescription>
                      {formatDate(selectedNotification.createdAt)}
                    </CardDescription>
                  </div>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setSelectedNotification(null)}
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                <Badge className={getTypeColor(selectedNotification.type)}>
                  {getTypeText(selectedNotification.type)}
                </Badge>
                {selectedNotification.isImportant && (
                  <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">
                    Quan trọng
                  </Badge>
                )}
                {!selectedNotification.isRead && (
                  <Badge className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                    Chưa đọc
                  </Badge>
                )}
              </div>
              
              <div className="prose dark:prose-invert max-w-none">
                <p className="text-gray-700 dark:text-gray-300">
                  {selectedNotification.message}
                </p>
              </div>
              
              <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex flex-col space-y-3">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    ID thông báo: #{selectedNotification.id}
                  </div>
                  <div className="flex space-x-2">
                    {!selectedNotification.isRead && (
                      <Button 
                        size="sm" 
                        variant="outline"
                        onClick={() => handleMarkAsRead(selectedNotification.notificationId || selectedNotification.id)}
                      >
                        Đánh dấu đã đọc
                      </Button>
                    )}
                    {/* <Button size="sm">
                      Thực hiện hành động
                    </Button> */}
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

export default NotificationsPage;
