from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.db import transaction

from .models import Student, Course, Registration, RegistrationPeriod, AuditLog
from .serializers import (
    StudentSerializer, LoginSerializer, CourseSerializer,
    RegistrationSerializer, RegistrationCreateSerializer,
    RegistrationPeriodSerializer, RegistrationPeriodUpdateSerializer,
    AdminLoginSerializer, CourseCreateUpdateSerializer
)
from .authentication import JWTGenerator
from .email_service import EmailService

class LoginViewSet(viewsets.ViewSet):
    """API để đăng nhập sinh viên"""
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def student_login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.validated_data['student']
            token = JWTGenerator.generate_token(student)
            
            # Ghi log hoạt động
            AuditLog.objects.create(
                student=student,
                action='login'
            )
            
            return Response({
                'token': token,
                'student': StudentSerializer(student).data,
                'message': 'Đăng nhập thành công'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def admin_login(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.validated_data['student']
            token = JWTGenerator.generate_token(student)
            
            # Ghi log hoạt động
            AuditLog.objects.create(
                student=student,
                action='login'
            )
            
            return Response({
                'token': token,
                'student': StudentSerializer(student).data,
                'message': 'Đăng nhập admin thành công'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseViewSet(viewsets.ModelViewSet):
    """API để quản lý môn học"""
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def create(self, request, *args, **kwargs):
        """Chỉ admin mới có thể tạo môn học"""
        if not request.user.is_admin:
            return Response(
                {'error': 'Chỉ admin mới có quyền tạo môn học'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Chỉ admin mới có thể cập nhật môn học"""
        if not request.user.is_admin:
            return Response(
                {'error': 'Chỉ admin mới có quyền cập nhật môn học'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Chỉ admin mới có thể xóa môn học"""
        if not request.user.is_admin:
            return Response(
                {'error': 'Chỉ admin mới có quyền xóa môn học'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

class RegistrationViewSet(viewsets.ViewSet):
    """API để quản lý đăng ký môn học"""
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """Lấy danh sách môn học đã đăng ký của sinh viên"""
        registrations = Registration.objects.filter(
            student=request.user,
            status='registered'
        ).select_related('course')
        
        serializer = RegistrationSerializer(
            registrations,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Đăng ký môn học"""
        # Kiểm tra xem kỳ đăng ký có đang mở không
        if not RegistrationPeriod.is_registration_open():
            return Response(
                {'error': 'Kỳ đăng ký chưa mở hoặc đã đóng'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RegistrationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        course_id = serializer.validated_data['course_id']
        
        try:
            course = Course.objects.get(id=course_id, is_active=True)
        except Course.DoesNotExist:
            return Response(
                {'error': 'Môn học không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Kiểm tra xem sinh viên đã đăng ký môn này chưa
        existing = Registration.objects.filter(
            student=request.user,
            course=course
        ).first()

        if existing:
            if existing.status == 'registered':
                return Response(
                    {'error': 'Bạn đã đăng ký môn học này'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Nếu đã huỷ, cho phép đăng ký lại
            existing.status = 'registered'
            existing.cancelled_at = None
            existing.save()
        else:
            # Kiểm tra sức chứa
            if course.get_available_spots() <= 0:
                return Response(
                    {'error': 'Môn học đã đầy'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Tạo đăng ký mới
            registration = Registration.objects.create(
                student=request.user,
                course=course,
                status='registered'
            )

        # Ghi log hoạt động
        AuditLog.objects.create(
            student=request.user,
            action='register',
            course=course
        )

        # Gửi email xác nhận
        EmailService.send_registration_confirmation(request.user, course)

        return Response(
            {'message': 'Đăng ký môn học thành công'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def cancel(self, request):
        """Huỷ đăng ký môn học"""
        # Kiểm tra xem kỳ đăng ký có đang mở không
        if not RegistrationPeriod.is_registration_open():
            return Response(
                {'error': 'Kỳ đăng ký đã đóng, không thể huỷ đăng ký'},
                status=status.HTTP_403_FORBIDDEN
            )

        course_id = request.data.get('course_id')
        if not course_id:
            return Response(
                {'error': 'course_id là bắt buộc'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            registration = Registration.objects.get(
                student=request.user,
                course_id=course_id,
                status='registered'
            )
        except Registration.DoesNotExist:
            return Response(
                {'error': 'Không tìm thấy đăng ký môn học'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Huỷ đăng ký
        registration.status = 'cancelled'
        registration.cancelled_at = timezone.now()
        registration.save()

        # Ghi log hoạt động
        AuditLog.objects.create(
            student=request.user,
            action='cancel',
            course=registration.course
        )

        # Gửi email xác nhận
        EmailService.send_cancellation_confirmation(request.user, registration.course)

        return Response(
            {'message': 'Huỷ đăng ký môn học thành công'},
            status=status.HTTP_200_OK
        )

class RegistrationPeriodViewSet(viewsets.ViewSet):
    """API để quản lý kỳ đăng ký"""
    
    def get_permissions(self):
        # active_period có thể truy cập không cần đăng nhập
        if self.action == 'active_period':
            return [AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def active_period(self, request):
        """Lấy thông tin kỳ đăng ký đang hoạt động - Không cần đăng nhập"""
        now = timezone.now()
        period = RegistrationPeriod.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()
        
        if not period:
            return Response(
                {
                    'is_open': False,
                    'message': 'Kỳ đăng ký chưa mở hoặc đã đóng'
                },
                status=status.HTTP_200_OK
            )
        
        serializer = RegistrationPeriodSerializer(period)
        return Response({
            'is_open': True,
            'period': serializer.data
        })

    @action(detail=False, methods=['get'])
    def list_periods(self, request):
        """Lấy danh sách các kỳ đăng ký"""
        if not request.user.is_admin:
            return Response(
                {'error': 'Chỉ admin mới có quyền'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        periods = RegistrationPeriod.objects.all().order_by('-created_at')
        serializer = RegistrationPeriodSerializer(periods, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_period(self, request):
        """Tạo kỳ đăng ký mới"""
        if not request.user.is_admin:
            return Response(
                {'error': 'Chỉ admin mới có quyền'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = RegistrationPeriodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def update_period(self, request):
        """Cập nhật kỳ đăng ký"""
        if not request.user.is_admin:
            return Response(
                {'error': 'Chỉ admin mới có quyền'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        period_id = request.data.get('id')
        if not period_id:
            return Response(
                {'error': 'period id là bắt buộc'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            period = RegistrationPeriod.objects.get(id=period_id)
        except RegistrationPeriod.DoesNotExist:
            return Response(
                {'error': 'Kỳ đăng ký không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RegistrationPeriodUpdateSerializer(
            period,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentViewSet(viewsets.ViewSet):
    """API để quản lý sinh viên"""

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Lấy thông tin tài khoản"""
        serializer = StudentSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Thay đổi mật khẩu"""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {'error': 'old_password và new_password là bắt buộc'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not request.user.check_password(old_password):
            return Response(
                {'error': 'Mật khẩu cũ không chính xác'},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.set_password(new_password)
        request.user.save()

        return Response({'message': 'Thay đổi mật khẩu thành công'})
