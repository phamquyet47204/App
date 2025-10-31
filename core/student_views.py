from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import *
from .permissions import require_permission
from django.utils import timezone

# ============ STUDENT PROFILE ============
@require_permission('view_profile')
@csrf_exempt
@require_http_methods(["GET"])
def get_student_profile(request):
    """Xem thông tin cá nhân của student"""
    try:
        student = Student.objects.get(user=request.user)
        
        data = {
            'studentId': student.studentId,
            'studentCode': student.studentCode,
            'fullName': student.user.full_name,
            'email': student.user.email,
            'phone': getattr(student.user, 'phone', ''),
            'address': getattr(student.user, 'address', ''),
            'dateOfBirth': student.dateOfBirth.isoformat() if student.dateOfBirth else None,
            'gender': student.gender,
            'gpa': float(student.gpa) if student.gpa else 0,
            'totalCredits': student.totalCredits,
            'studentClass': {
                'classId': student.studentClass.classId,
                'className': student.studentClass.className,
                'major': {
                    'majorId': student.studentClass.major.majorId,
                    'majorName': student.studentClass.major.majorName,
                    'department': {
                        'departmentId': student.studentClass.major.department.departmentId,
                        'departmentName': student.studentClass.major.department.departmentName
                    }
                }
            } if student.studentClass else None
        }
        
        return JsonResponse(data)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_permission('update_profile')
@csrf_exempt
@require_http_methods(["PUT"])
def update_student_profile(request):
    """Cập nhật thông tin cá nhân của student - chỉ cho phép sửa phone, address, email"""
    try:
        student = Student.objects.get(user=request.user)
        data = json.loads(request.body)
        
        # Chỉ cho phép cập nhật các trường được phép
        allowed_fields = ['phone', 'email']
        updated_fields = []
        
        user = student.user
        
        # Cập nhật phone
        if 'phone' in data and hasattr(user, 'phone'):
            user.phone = data['phone']
            updated_fields.append('phone')
        
        # Cập nhật email
        if 'email' in data:
            user.email = data['email']
            updated_fields.append('email')
        
        # Cập nhật address (nếu model có field này)
        if 'address' in data and hasattr(user, 'address'):
            user.address = data['address']
            updated_fields.append('address')
        
        if updated_fields:
            user.save()
            return JsonResponse({
                'message': 'Profile updated successfully',
                'updated_fields': updated_fields
            })
        else:
            return JsonResponse({
                'message': 'No valid fields to update',
                'allowed_fields': ['phone', 'email', 'address']
            }, status=400)
            
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ============ STUDENT SCHEDULE ============
@require_permission('view_schedule')
@csrf_exempt
@require_http_methods(["GET"])
def get_my_schedule(request):
    """Xem lịch học của student"""
    try:
        student = Student.objects.get(user=request.user)
        
        # Get current semester
        current_semester = Semester.objects.filter(status='active').first()
        if not current_semester:
            return JsonResponse({'schedule': []})
        
        # Get registered courses for current semester
        registrations = CourseRegistration.objects.filter(
            student=student,
            semester=current_semester,
            status='registered'
        ).select_related('courseClass__subject')
        
        schedule = []
        for reg in registrations:
            course_class = reg.courseClass
            schedule.append({
                'courseClassId': course_class.courseClassId,
                'courseCode': course_class.courseCode,
                'courseName': course_class.courseName,
                'subject': course_class.subject.subjectName,
                'credits': course_class.subject.credits,
                'room': course_class.room,
                'schedule': str(course_class.schedule) if course_class.schedule else None,
                'teacher': course_class.teacher.user.full_name if course_class.teacher else None
            })
        
        return JsonResponse({'schedule': schedule})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ============ STUDENT REGISTRATIONS ============
@require_permission('view_registrations')
@csrf_exempt
@require_http_methods(["GET"])
def get_my_registrations(request):
    """Xem danh sách đăng ký của student"""
    try:
        student = Student.objects.get(user=request.user)
        
        registrations = CourseRegistration.objects.filter(
            student=student
        ).select_related('courseClass__subject', 'semester').order_by('-registrationDate')
        
        data = []
        for reg in registrations:
            course_class = reg.courseClass
            data.append({
                'registrationId': reg.registrationId,
                'courseClassId': course_class.courseClassId,
                'courseCode': course_class.courseCode,
                'courseName': course_class.courseName,
                'subject': course_class.subject.subjectName,
                'credits': course_class.subject.credits,
                'semester': reg.semester.semesterName,
                'status': reg.status,
                'registrationDate': reg.registrationDate.isoformat(),
                'grade': reg.grade.letterGrade if hasattr(reg, 'grade') and reg.grade else None
            })
        
        return JsonResponse({'registrations': data})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ============ STUDENT DOCUMENT REQUESTS ============
@require_permission('view_documents')
@csrf_exempt
@require_http_methods(["GET", "POST"])
def get_my_document_requests(request):
    """GET: Xem yêu cầu tài liệu của student; POST: Tạo yêu cầu mới và xếp hàng chờ"""
    try:
        student = Student.objects.get(user=request.user)

        if request.method == 'POST':
            # Chỉ cho phép nếu có quyền request_document
            from .permissions import RolePermission
            if not RolePermission.has_permission(request.user, 'request_document'):
                return JsonResponse({'error': 'Permission denied'}, status=403)

            payload = json.loads(request.body)
            document_type_id = payload.get('documentTypeId')
            semester_id = payload.get('semesterId')
            purpose = payload.get('purpose')
            if not document_type_id or not semester_id or not purpose:
                return JsonResponse({'error': 'documentTypeId, semesterId, purpose are required'}, status=400)

            document_type = DocumentType.objects.get(documentTypeId=document_type_id)
            semester = Semester.objects.get(semesterId=semester_id)

            # Nếu đã có yêu cầu cho cùng loại tài liệu trong cùng học kỳ thì trả về thông tin hiện có
            existing = DocumentRequest.objects.filter(
                student=student,
                documentType=document_type,
                semester=semester,
                status__in=['pending', 'approved', 'completed']
            ).order_by('-requestDate').first()
            if existing:
                return JsonResponse({
                    'message': 'already_requested',
                    'requestId': existing.requestId,
                    'status': existing.status
                }, status=200)

            # Tạo requestId tự tăng dựa theo số lượng hiện có, đảm bảo không trùng
            base_prefix = 'DR'
            next_num = DocumentRequest.objects.count() + 1
            while True:
                candidate_id = f"{base_prefix}{next_num:06d}"
                if not DocumentRequest.objects.filter(requestId=candidate_id).exists():
                    break
                next_num += 1

            # Tính vị trí hàng chờ hiện tại (pending)
            queue_position = DocumentRequest.objects.filter(status='pending').count() + 1

            created = DocumentRequest.objects.create(
                requestId=candidate_id,
                student=student,
                documentType=document_type,
                semester=semester,
                requestDate=timezone.now(),
                purpose=purpose,
                status='pending'
            )

            return JsonResponse({
                'message': 'Document request created',
                'requestId': created.requestId,
                'queuePosition': queue_position,
                'status': created.status
            }, status=201)

        # GET: Danh sách yêu cầu của sinh viên
        document_requests = DocumentRequest.objects.filter(
            student=student
        ).select_related('documentType').order_by('-requestDate')

        data = []
        for req in document_requests:
            data.append({
                'requestId': req.requestId,
                'documentType': {
                    'typeId': req.documentType.documentTypeId,
                    'typeName': req.documentType.name,
                    'description': req.documentType.description
                },
                'purpose': req.purpose,
                'status': req.status,
                'requestDate': req.requestDate.isoformat(),
                'approvedDate': req.approvedDate.isoformat() if req.approvedDate else None,
                'rejectedReason': getattr(req, 'rejectionReason', '')
            })

        return JsonResponse({'documentRequests': data})
    except DocumentType.DoesNotExist:
        return JsonResponse({'error': 'Document type not found'}, status=404)
    except Semester.DoesNotExist:
        return JsonResponse({'error': 'Semester not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ============ STUDENT NOTIFICATIONS ============
@require_permission('view_notifications')
@csrf_exempt
@require_http_methods(["GET"])
def get_my_notifications(request):
    """Xem thông báo của student"""
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
            
        notifications = NotificationRecipient.objects.filter(
            user=request.user
        ).select_related('notification').order_by('-notification__scheduledAt')
        
        data = []
        for nr in notifications:
            notification = nr.notification
            if notification:  # Kiểm tra notification tồn tại
                data.append({
                    'notificationId': notification.notificationId,
                    'title': notification.title,
                    'content': notification.content,
                    'notificationType': notification.notificationType,
                    'priority': notification.priority,
                    'scheduledAt': notification.scheduledAt.isoformat() if notification.scheduledAt else None,
                    'deliveredAt': nr.deliveredAt.isoformat() if nr.deliveredAt else None,
                    'readAt': nr.readAt.isoformat() if nr.readAt else None,
                    'isRead': nr.readAt is not None,
                    'deliveryStatus': nr.deliveryStatus
                })
        
        return JsonResponse({'notifications': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ============ STUDENT TUITION FEES ============
@require_permission('view_tuition')
@csrf_exempt
@require_http_methods(["GET"])
def get_my_tuition_fees(request):
    """Xem học phí của student"""
    try:
        student = Student.objects.get(user=request.user)
        
        tuition_fees = TuitionFee.objects.filter(
            student=student
        ).select_related('semester').order_by('-semester__startDate')
        
        data = []
        for fee in tuition_fees:
            data.append({
                'feeId': fee.tuitionFee,
                'semester': fee.semester.semesterName,
                'totalAmount': float(fee.totalAmount),
                'paidAmount': float(fee.paidAmount),
                'remainingAmount': float(fee.totalAmount - fee.paidAmount),
                'dueDate': fee.dueDate.isoformat(),
                'status': fee.paymentStatus,
                'paymentDate': fee.paymentDate.isoformat() if fee.paymentDate else None
            })
        
        return JsonResponse({'tuitionFees': data})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)