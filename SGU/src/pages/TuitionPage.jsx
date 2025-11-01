import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { DollarSign, Calendar, AlertTriangle, CheckCircle, Clock, Download, CreditCard } from 'lucide-react';
import { tuitionService } from '../services/tuitionService';
import { toast } from 'react-hot-toast';

const TuitionPage = () => {
  const [tuitionFees, setTuitionFees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedFee, setSelectedFee] = useState(null);

  useEffect(() => {
    fetchTuitionFees();
  }, []);

  const fetchTuitionFees = async () => {
    try {
      setLoading(true);
      const result = await tuitionService.getMyTuitionFees();
      if (result.success) {
        setTuitionFees(result.data);
      } else {
        console.error('Lỗi tải học phí:', result.message);
        toast.error('Không thể tải thông tin học phí');
      }
    } catch (error) {
      console.error('Lỗi tải học phí:', error);
      toast.error('Có lỗi xảy ra khi tải học phí');
    } finally {
      setLoading(false);
    }
  };

  const getPaymentStatusColor = (status, remainingAmount) => {
    if (remainingAmount === 0)
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    if (remainingAmount > 0)
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    switch (status) {
      case 'paid': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'pending': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'overdue': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      case 'partial': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const getPaymentStatusText = (status, remainingAmount) => {
    if (remainingAmount === 0) return 'Hoàn thành';
    if (remainingAmount > 0) return 'Chưa hoàn thành';
    switch (status) {
      case 'paid': return 'Đã thanh toán';
      case 'pending': return 'Chờ thanh toán';
      case 'overdue': return 'Quá hạn';
      case 'partial': return 'Thanh toán một phần';
      default: return 'Không xác định';
    }
  };

  const getPaymentStatusIcon = (status) => {
    switch (status) {
      case 'paid': return <CheckCircle className="h-4 w-4" />;
      case 'pending': return <Clock className="h-4 w-4" />;
      case 'overdue': return <AlertTriangle className="h-4 w-4" />;
      case 'partial': return <Clock className="h-4 w-4" />;
      default: return <AlertTriangle className="h-4 w-4" />;
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('vi-VN');
  };

  const calculateTotalAmount = () => {
    return tuitionFees.reduce((total, fee) => total + fee.totalAmount, 0);
  };

  const calculatePaidAmount = () => {
    return tuitionFees.reduce((total, fee) => total + fee.paidAmount, 0);
  };

  const calculateRemainingAmount = () => {
    return tuitionFees.reduce((total, fee) => total + fee.remainingAmount, 0);
  };

  const getOverdueCount = () => {
    return tuitionFees.filter(fee => fee.isOverdue).length;
  };

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải thông tin học phí...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-black">
            Học phí
          </h1>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={fetchTuitionFees}>
            <Calendar className="h-4 w-4 mr-2" />
            Làm mới
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Tổng học phí</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {formatCurrency(calculateTotalAmount())}
                </p>
              </div>
              <DollarSign className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Đã thanh toán</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {formatCurrency(calculatePaidAmount())}
                </p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Còn lại</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {formatCurrency(calculateRemainingAmount())}
                </p>
              </div>
              <Clock className="h-8 w-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Quá hạn</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-black">
                  {getOverdueCount()}
                </p>
              </div>
              <AlertTriangle className="h-8 w-8 text-red-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Banking Information */}
      <Card className="bg-blue-50 border-blue-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-blue-900">
            <CreditCard className="h-5 w-5" />
            Thông tin chuyển khoản
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-white rounded-lg p-4 border border-blue-200">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Ngân hàng:</span>
                <span className="text-sm font-semibold text-gray-900">SGU</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">Số tài khoản:</span>
                <span className="text-sm font-semibold text-blue-600 font-mono">0000000000000000</span>
              </div>
              <div className="pt-2 mt-2 border-t border-gray-200 space-y-2">
                <p className="text-xs text-gray-600">
                  <strong>Lưu ý:</strong> Vui lòng ghi rõ nội dung chuyển khoản: <span className="font-semibold">Học phí - Mã số sinh viên - Học kỳ</span>
                </p>
                <div className="flex items-center gap-2 pt-2">
                  <span className="text-xs font-medium text-gray-700">Hoặc đóng trực tiếp tại:</span>
                  <span className="text-xs font-semibold text-blue-600">Phòng Tài chính A.001</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="all" className="space-y-4">
      {/* <div className="overflow-x-auto scrollbar-hide">
        <TabsList className="flex sm:grid sm:grid-cols-4 bg-gray-50 dark:bg-white-100/30 rounded-lg p-1 gap-0 min-w-max sm:min-w-0">
          <TabsTrigger
            value="all"
            className="
              data-[state=active]:bg-gray-400 data-[state=active]:text-white 
              rounded-md px-4 py-2 whitespace-nowrap transition-all 
              flex-shrink-0 text-sm sm:text-base -ml-1
            "
          >
            Tất cả
          </TabsTrigger>
          <TabsTrigger
            value="pending"
            className="
              data-[state=active]:bg-gray-400 data-[state=active]:text-white 
              rounded-md px-4 py-2 whitespace-nowrap transition-all 
              flex-shrink-0 text-sm sm:text-base -ml-1 -mr-1
            "
          >
            Chờ thanh toán
          </TabsTrigger>
          <TabsTrigger
            value="overdue"
            className="
              data-[state=active]:bg-gray-400 data-[state=active]:text-white 
              rounded-md px-4 py-2 whitespace-nowrap transition-all 
              flex-shrink-0 text-sm sm:text-base -ml-1 -mr-1
            "
          >
            Quá hạn
          </TabsTrigger>
          <TabsTrigger
            value="paid"
            className="
              data-[state=active]:bg-gray-400 data-[state=active]:text-white 
              rounded-md px-4 py-2 whitespace-nowrap transition-all 
              flex-shrink-0 text-sm sm:text-base -ml-1 -mr-1
            "
          >
            Đã thanh toán
          </TabsTrigger>
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
      `}</style> */}

        <TabsContent value="all" className="space-y-4">
          <div className="space-y-4">
            {tuitionFees.map((fee) => (
              <Card 
                key={fee.tuitionFeeId} 
                className="hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => setSelectedFee(fee)}
              >
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-black">
                        Học phí {fee.semester?.semesterName}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {fee.totalCredits} tín chỉ • {formatDate(fee.dueDate)}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge className={getPaymentStatusColor(fee.paymentStatus, fee.remainingAmount)}>
                        <div className="flex items-center space-x-1">
                          {getPaymentStatusIcon(fee.paymentStatus)}
                          <span>{getPaymentStatusText(fee.paymentStatus, fee.remainingAmount)}</span>
                        </div>
                      </Badge>
                      {fee.isOverdue && (
                        <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">
                          Quá hạn
                        </Badge>
                      )}
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">Tổng số tiền</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-black">
                        {formatCurrency(fee.totalAmount)}
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">Đã thanh toán</p>
                      <p className="text-lg font-semibold text-green-600 dark:text-green-400">
                        {formatCurrency(fee.paidAmount)}
                      </p>
                    </div>
                    <div>
                      <p className="text-gray-600 dark:text-gray-400">Còn lại</p>
                      <p className="text-lg font-semibold text-red-600 dark:text-red-400">
                        {formatCurrency(fee.remainingAmount)}
                      </p>
                    </div>
                    {/* <div>
                      <p className="text-gray-600 dark:text-gray-400">Phí/tín chỉ</p>
                      <p className="text-lg font-semibold text-gray-900 dark:text-black">
                        {formatCurrency(fee.feePerCredit)}
                      </p>
                    </div> */}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="pending" className="space-y-4">
          <div className="space-y-4">
            {tuitionFees.filter(fee => fee.paymentStatus === 'pending').map((fee) => (
              <Card 
                key={fee.tuitionFeeId} 
                className="hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => setSelectedFee(fee)}
              >
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-black">
                        Học phí {fee.semester?.semesterName}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Hạn thanh toán: {formatDate(fee.dueDate)}
                      </p>
                    </div>
                    <Badge className={getPaymentStatusColor(fee.paymentStatus, fee.remainingAmount)}>
                      <div className="flex items-center space-x-1">
                        {getPaymentStatusIcon(fee.paymentStatus)}
                        <span>{getPaymentStatusText(fee.paymentStatus, fee.remainingAmount)}</span>
                      </div>
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Số tiền cần thanh toán</p>
                      <p className="text-2xl font-bold text-gray-900 dark:text-black">
                        {formatCurrency(fee.remainingAmount)}
                      </p>
                    </div>
                    <Button>
                      <CreditCard className="h-4 w-4 mr-2" />
                      Thanh toán
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="overdue" className="space-y-4">
          <div className="space-y-4">
            {tuitionFees.filter(fee => fee.isOverdue).map((fee) => (
              <Card 
                key={fee.tuitionFeeId} 
                className="hover:shadow-lg transition-shadow cursor-pointer border-red-200 dark:border-red-800"
                onClick={() => setSelectedFee(fee)}
              >
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-black">
                        Học phí {fee.semester?.semesterName}
                      </h3>
                      <p className="text-sm text-red-600 dark:text-red-400">
                        Quá hạn từ: {formatDate(fee.dueDate)}
                      </p>
                    </div>
                    <Badge className="bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">
                      <div className="flex items-center space-x-1">
                        <AlertTriangle className="h-4 w-4" />
                        <span>Quá hạn</span>
                      </div>
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Số tiền quá hạn</p>
                      <p className="text-2xl font-bold text-red-600 dark:text-red-400">
                        {formatCurrency(fee.remainingAmount)}
                      </p>
                    </div>
                    <Button className="bg-red-600 hover:bg-red-700">
                      <CreditCard className="h-4 w-4 mr-2" />
                      Thanh toán ngay
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="paid" className="space-y-4">
          <div className="space-y-4">
            {tuitionFees.filter(fee => fee.paymentStatus === 'paid').map((fee) => (
              <Card 
                key={fee.tuitionFeeId} 
                className="hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => setSelectedFee(fee)}
              >
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-black">
                        Học phí {fee.semester?.semesterName}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Đã thanh toán: {formatDate(fee.dueDate)}
                      </p>
                    </div>
                    <Badge className={getPaymentStatusColor(fee.paymentStatus, fee.remainingAmount)}>
                      <div className="flex items-center space-x-1">
                        {getPaymentStatusIcon(fee.paymentStatus)}
                        <span>{getPaymentStatusText(fee.paymentStatus, fee.remainingAmount)}</span>
                      </div>
                    </Badge>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">Số tiền đã thanh toán</p>
                      <p className="text-2xl font-bold text-green-600 dark:text-green-400">
                        {formatCurrency(fee.paidAmount)}
                      </p>
                    </div>
                    <Button variant="outline">
                      <Download className="h-4 w-4 mr-2" />
                      Tải hóa đơn
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Fee Detail Modal */}
      {selectedFee && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Chi tiết học phí</CardTitle>
                  <CardDescription>
                    Học phí {selectedFee.semester?.semesterName}
                  </CardDescription>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setSelectedFee(null)}
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Tổng tín chỉ</label>
                  <p className="text-gray-900 dark:text-black">{selectedFee.totalCredits}</p>
                </div>
                {/* <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Phí/tín chỉ</label>
                  <p className="text-gray-900 dark:text-black">{formatCurrency(selectedFee.feePerCredit)}</p>
                </div> */}
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Tổng số tiền</label>
                  <p className="text-gray-900 dark:text-black">{formatCurrency(selectedFee.totalAmount)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Đã thanh toán</label>
                  <p className="text-green-600 dark:text-green-400">{formatCurrency(selectedFee.paidAmount)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Còn lại</label>
                  <p className="text-red-600 dark:text-red-400">{formatCurrency(selectedFee.remainingAmount)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Hạn thanh toán</label>
                  <p className="text-gray-900 dark:text-black">{formatDate(selectedFee.dueDate)}</p>
                </div>
              </div>
              
              {/* <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex space-x-3">
                  {selectedFee.paymentStatus !== 'paid' && (
                    <Button className="flex-1">
                      <CreditCard className="h-4 w-4 mr-2" />
                      Thanh toán
                    </Button>
                  )}
                  <Button variant="outline" className="flex-1">
                    <Download className="h-4 w-4 mr-2" />
                    Tải hóa đơn
                  </Button>
                </div>
              </div> */}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default TuitionPage;
