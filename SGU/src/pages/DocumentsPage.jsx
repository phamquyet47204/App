import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { FileText, Download, Upload, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { documentsService } from '../services/documentsService';
import { toast } from 'react-hot-toast';

const DocumentsPage = () => {
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [myRequests, setMyRequests] = useState([]);
  const [documentTypes, setDocumentTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [createForm, setCreateForm] = useState({
    documentTypeId: '',
    purpose: ''
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [requestsResult, typesResult] = await Promise.all([
        documentsService.getMyDocumentRequests(),
        documentsService.getDocumentTypes()
      ]);

      if (requestsResult.success) {
        setMyRequests(requestsResult.data);
      }

      if (typesResult.success) {
        setDocumentTypes(typesResult.data);
      }
    } catch (error) {
      console.error('Lỗi tải dữ liệu:', error);
      toast.error('Có lỗi xảy ra khi tải dữ liệu');
    } finally {
      setLoading(false);
    }
  };

  // Tạo yêu cầu nhanh từ card (không cần form)
  const handleQuickCreateRequest = async (documentTypeId, purpose = 'Yêu cầu tài liệu') => {
    try {
      const payload = {
        documentTypeId: documentTypeId,
        purpose: purpose
      };
      
      const result = await documentsService.createDocumentRequest(payload);
      if (result.success) {
        toast.success('Đã đăng ký thành công');
        fetchData(); // Refresh danh sách
      } else {
        // Xử lý trường hợp đã đăng ký rồi
        if (result.message && result.message.includes('already_requested') || 
            result.message && result.message.includes('đã tạo')) {
          toast.error('Đã đăng ký loại giấy này rồi');
        } else {
          toast.error(result.message || 'Có lỗi xảy ra khi đăng ký');
        }
      }
    } catch (error) {
      console.error('Lỗi đăng ký:', error);
      // Kiểm tra nếu là lỗi đã đăng ký rồi
      if (error.message && error.message.includes('already_requested')) {
        toast.error('Đã đăng ký loại giấy này rồi');
      } else {
        toast.error('Có lỗi xảy ra khi đăng ký');
      }
    }
  };

  // Tạo yêu cầu từ form (với mục đích tùy chỉnh)
  const handleCreateRequest = async () => {
    // Validation - bỏ semesterId, backend tự lấy học kỳ active
    if (!createForm.documentTypeId || !createForm.purpose) {
      toast.error('Vui lòng điền đầy đủ thông tin (Loại tài liệu và Mục đích)');
      return;
    }

    try {
      // Không gửi requestId và semesterId - backend tự sinh/tự lấy
      const payload = {
        documentTypeId: createForm.documentTypeId,
        purpose: createForm.purpose
      };
      
      const result = await documentsService.createDocumentRequest(payload);
      if (result.success) {
        toast.success('Tạo yêu cầu tài liệu thành công');
        setShowCreateForm(false);
        setCreateForm({
          documentTypeId: '',
          purpose: ''
        });
        fetchData(); // Refresh danh sách
      } else {
        // Xử lý trường hợp đã đăng ký rồi
        if (result.message && result.message.includes('already_requested') || 
            result.message && result.message.includes('đã tạo')) {
          toast.error('Đã đăng ký loại giấy này rồi');
        } else {
          toast.error(result.message || 'Có lỗi xảy ra khi tạo yêu cầu');
        }
      }
    } catch (error) {
      console.error('Lỗi tạo yêu cầu:', error);
      if (error.message && error.message.includes('already_requested')) {
        toast.error('Đã đăng ký loại giấy này rồi');
      } else {
        toast.error('Có lỗi xảy ra khi tạo yêu cầu');
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'available': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'pending': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'processing': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'approved': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'rejected': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'approved': return <CheckCircle className="h-4 w-4" />;
      case 'pending': return <Clock className="h-4 w-4" />;
      case 'processing': return <Clock className="h-4 w-4" />;
      case 'completed': return <CheckCircle className="h-4 w-4" />;
      case 'rejected': return <XCircle className="h-4 w-4" />;
      default: return <AlertCircle className="h-4 w-4" />;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'approved': return 'Đã duyệt';
      case 'pending': return 'Đang xử lý';
      case 'processing': return 'Đang xử lý';
      case 'completed': return 'Hoàn thành';
      case 'rejected': return 'Từ chối';
      default: return 'Chưa xác định';
    }
  };

  if (loading) {
    return (
      <div className="p-6 space-y-6">
        <div className="text-center py-10">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Đang tải dữ liệu...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-black">
            Đăng ký giấy tờ
          </h1>
          {/* <p className="text-gray-600 dark:text-gray-300 mt-2">
            Đăng ký và theo dõi các loại giấy tờ cần thiết
          </p> */}
        </div>
        <Button variant="outline" onClick={() => setShowCreateForm(true)}>
          <FileText className="h-4 w-4 mr-2" />
          Đăng ký mới
        </Button>
      </div>

      <Tabs defaultValue="types" className="space-y-4">
        <TabsList>
          <TabsTrigger value="types">Loại giấy tờ</TabsTrigger>
          <TabsTrigger value="requests">Yêu cầu của tôi</TabsTrigger>
        </TabsList>

        <TabsContent value="types" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {documentTypes.map((docType) => (
              <Card 
                key={docType.typeId || docType.documentTypeId || docType.id} 
                className="hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => setSelectedDocument(docType)}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <CardTitle className="text-lg">{docType.typeName || docType.name}</CardTitle>
                      <CardDescription className="text-sm">
                        {docType.description || 'Không có mô tả'}
                      </CardDescription>
                    </div>
                    <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">
                      Có sẵn
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">Thời gian xử lý:</span>
                    <span className="text-gray-900 dark:text-black">
                      {docType.processingTime || docType.processingDays || 'N/A'} ngày
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">Số lượng tối đa:</span>
                    <span className="text-gray-900 dark:text-black">
                      {docType.maxRequestsPerSemester || 'Không giới hạn'}
                    </span>
                  </div>
                  <div className="pt-2 border-t border-gray-200 dark:border-gray-700">
                    <Button 
                      variant="outline" 
                      className="w-full" 
                      size="sm" 
                      onClick={(e) => {
                        e.stopPropagation(); // Prevent card onClick
                        const typeId = docType.typeId || docType.documentTypeId;
                        handleQuickCreateRequest(typeId, `Yêu cầu ${docType.typeName || docType.name}`);
                      }}
                    >
                      Đăng ký
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="requests" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Yêu cầu của tôi</CardTitle>
              <CardDescription>
                Theo dõi trạng thái các yêu cầu giấy tờ đã gửi
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {myRequests.map((request) => (
                  <div key={request.requestId || request.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-black">
                          {request.documentType?.typeName || 'Không xác định'}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Ngày yêu cầu: {request.requestDate}
                        </p>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          Mục đích: {request.purpose}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={getStatusColor(request.status)}>
                          <div className="flex items-center space-x-1">
                            {getStatusIcon(request.status)}
                            <span>{getStatusText(request.status)}</span>
                          </div>
                        </Badge>
                      </div>
                    </div>
                    
                    {request.approvedDate && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                        Ngày duyệt: {request.approvedDate}
                      </p>
                    )}
                    
                    {request.completedDate && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                        Ngày hoàn thành: {request.completedDate}
                      </p>
                    )}
                    
                    <div className="flex items-center justify-between">
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        ID yêu cầu: #{request.requestId || request.id}
                      </div>
                      {request.status === 'completed' && (
                        <Button size="sm" variant="outline">
                          <Download className="h-4 w-4 mr-2" />
                          Tải xuống
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Document Detail Modal */}
      {selectedDocument && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>{selectedDocument.typeName || selectedDocument.name}</CardTitle>
                  <CardDescription>{selectedDocument.description || 'Không có mô tả'}</CardDescription>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setSelectedDocument(null)}
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Thời gian xử lý</label>
                  <p className="text-gray-900 dark:text-black">
                    {selectedDocument.processingTime || selectedDocument.processingDays || 'N/A'} ngày
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Phí</label>
                  <p className="text-gray-900 dark:text-black">
                    {selectedDocument.fee === 0
                      ? 'Miễn phí'
                      : selectedDocument.fee
                      ? `${selectedDocument.fee.toLocaleString()} VNĐ`
                      : 'Không có thông tin'}
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Trạng thái</label>
                  <Badge className={getStatusColor(selectedDocument.status)}>
                    {selectedDocument.status === 'available' ? 'Có sẵn' : selectedDocument.status}
                  </Badge>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500 dark:text-gray-400">Bắt buộc</label>
                  <p className="text-gray-900 dark:text-black">
                    {selectedDocument.required ? 'Có' : 'Không'}
                  </p>
                </div>
              </div>
              
              {/* <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <h3 className="font-semibold text-gray-900 dark:text-black mb-2">
                  Hướng dẫn đăng ký:
                </h3>
                <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400">
                  <li>Điền đầy đủ thông tin yêu cầu</li>
                  <li>Kiểm tra lại thông tin trước khi gửi</li>
                  <li>Chờ xử lý và thông báo kết quả</li>
                  <li>Tải xuống giấy tờ khi được duyệt</li>
                </ol>
              </div>
              
              <div className="flex space-x-3 pt-4">
                <Button variant="outline" className="flex-1">
                  Đăng ký ngay
                </Button>
                <Button variant="outline" onClick={() => setSelectedDocument(null)}>
                  Hủy
                </Button>
              </div> */}
            </CardContent>
          </Card>
        </div>
      )}

      {/* Create Request Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Tạo yêu cầu tài liệu mới</CardTitle>
                  <CardDescription>Điền thông tin để tạo yêu cầu tài liệu</CardDescription>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => setShowCreateForm(false)}
                >
                  ×
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700">Loại tài liệu *</label>
                  <select
                    value={createForm.documentTypeId}
                    onChange={(e) => setCreateForm(prev => ({ ...prev, documentTypeId: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Chọn loại tài liệu</option>
                    {documentTypes.map(type => (
                      <option key={type.typeId || type.documentTypeId} value={type.typeId || type.documentTypeId}>
                        {type.typeName || type.name}
                      </option>
                    ))}
                  </select>
                  {documentTypes.length === 0 && (
                    <p className="text-xs text-gray-500">Đang tải danh sách loại tài liệu...</p>
                  )}
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700">Mục đích *</label>
                  <textarea
                    value={createForm.purpose}
                    onChange={(e) => setCreateForm(prev => ({ ...prev, purpose: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Nhập mục đích sử dụng"
                    rows={3}
                  />
                </div>
              </div>
              <div className="flex space-x-3 pt-4">
                <Button onClick={handleCreateRequest} className="flex-1">
                  Tạo yêu cầu
                </Button>
                <Button variant="outline" onClick={() => setShowCreateForm(false)}>
                  Hủy
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default DocumentsPage;
