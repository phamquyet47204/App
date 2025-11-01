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
        
        # Tính GPA từ grades hiện tại (đảm bảo luôn đúng)
        from core.models import Grade
        passed_grades = Grade.objects.filter(student=student, isPassed=True)
        if passed_grades.exists():
            total_points = sum(float(g.gradePoint) * g.subject.credits for g in passed_grades)
            total_credits = sum(g.subject.credits for g in passed_grades)
            calculated_gpa = total_points / total_credits if total_credits > 0 else 0
        else:
            calculated_gpa = 0
            total_credits = 0
        
        data = {
            'studentId': student.studentId,
            'studentCode': student.studentCode,
            'fullName': student.user.full_name,
            'email': student.user.email,
            'phone': getattr(student.user, 'phone', ''),
            'address': getattr(student.user, 'address', ''),
            'dateOfBirth': student.dateOfBirth.isoformat() if student.dateOfBirth else None,
            'gender': student.gender,
            'gpa': round(calculated_gpa, 2),  # Sử dụng GPA tính từ grades
            'totalCredits': total_credits,  # Sử dụng credits từ grades đã pass
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
        import traceback
        traceback.print_exc()
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
            
            # Parse schedule nếu có
            schedule_info = None
            if course_class.schedule:
                schedule_dt = course_class.schedule
                days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                day_index = schedule_dt.weekday()  # 0=Monday, 6=Sunday
                day_name = days_of_week[day_index]
                
                start_time = schedule_dt.strftime('%H:%M')
                # Giả sử mỗi lớp học kéo dài 2 giờ
                from datetime import timedelta
                end_time = (schedule_dt + timedelta(hours=2)).strftime('%H:%M')
                
                schedule_info = {
                    'dayOfWeek': day_name,
                    'startTime': start_time,
                    'endTime': end_time,
                    'datetime': schedule_dt.isoformat()
                }
            
            # Đảm bảo luôn có dayOfWeek, startTime, endTime
            day_of_week = schedule_info['dayOfWeek'] if schedule_info else None
            start_time = schedule_info['startTime'] if schedule_info else None
            end_time = schedule_info['endTime'] if schedule_info else None
            
            schedule.append({
                'courseClassId': course_class.courseClassId,
                'courseCode': course_class.courseCode,
                'courseName': course_class.courseName,
                'subject': course_class.subject.subjectName,
                'credits': course_class.subject.credits,
                'room': course_class.room,
                'schedule': schedule_info,
                'schedule_datetime': str(course_class.schedule) if course_class.schedule else None,
                'teacher': course_class.teacher.user.full_name if course_class.teacher else None,
                # Thêm các field để tương thích với frontend - ĐẢM BẢO luôn có giá trị
                'dayOfWeek': day_of_week,
                'startTime': start_time,
                'endTime': end_time,
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

@require_permission('view_grades')
@csrf_exempt
@require_http_methods(["GET"])
def get_my_grades(request):
    """Xem danh sách điểm của student"""
    try:
        student = Student.objects.get(user=request.user)
        
        from core.models import Grade
        grades = Grade.objects.filter(
            student=student
        ).select_related('subject', 'semester', 'courseClass').order_by('-semester__semesterName', 'subject__subjectCode')
        
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"get_my_grades called for student {student.studentId}, found {grades.count()} grades")
        
        data = []
        for grade in grades:
            data.append({
                'gradeId': grade.gradeId,
                'subject': grade.subject.subjectName,
                'subjectCode': grade.subject.subjectCode,
                'credits': grade.subject.credits,
                'semester': grade.semester.semesterName,
                'semesterId': grade.semester.semesterId,
                'assignmentScore': float(grade.assginmentscore) if grade.assginmentscore else None,
                'midtermScore': float(grade.midterm_score) if grade.midterm_score else None,
                'finalScore': float(grade.final_score) if grade.final_score else None,
                'averageScore': float(grade.average_score) if grade.average_score else None,
                'letterGrade': grade.letterGrade,
                'gradePoint': float(grade.gradePoint) if grade.gradePoint else None,
                'isPassed': grade.isPassed,
                'courseCode': grade.courseClass.courseCode if grade.courseClass else None,
                'courseName': grade.courseClass.courseName if grade.courseClass else None,
            })
        
        # Tính GPA từ các môn đã pass
        passed_grades = [g for g in grades if g.isPassed]
        if passed_grades:
            total_points = sum(float(g.gradePoint) * g.subject.credits for g in passed_grades)
            total_credits = sum(g.subject.credits for g in passed_grades)
            gpa = total_points / total_credits if total_credits > 0 else 0
        else:
            gpa = 0
            total_credits = 0
        
        response_data = {
            'grades': data,
            'gpa': round(gpa, 2),
            'totalCredits': total_credits,
            'totalPassed': len(passed_grades),
            'totalGrades': len(data)
        }
        
        logger.info(f"Returning {len(data)} grades, GPA: {gpa}")
        
        return JsonResponse(response_data)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)

@require_permission('view_registrations')
@csrf_exempt
@require_http_methods(["GET"])
def get_my_completed_courses(request):
    """Xem danh sách lớp học đã hoàn thành của student"""
    try:
        student = Student.objects.get(user=request.user)
        
        # Lấy các registrations đã hoàn thành
        completed_registrations = CourseRegistration.objects.filter(
            student=student,
            status='completed'
        ).select_related('courseClass__subject', 'semester', 'courseClass__teacher__user').order_by('-registrationDate')
        
        # Lấy thêm các môn có grade và isPassed=True (có thể chưa set status='completed')
        from core.models import Grade
        passed_grades = Grade.objects.filter(
            student=student,
            isPassed=True
        ).select_related('courseClass__subject', 'semester', 'courseClass__teacher__user', 'courseClass')
        
        data = []
        processed_course_ids = set()
        
        # Thêm các courses từ completed registrations
        for reg in completed_registrations:
            course_class = reg.courseClass
            
            # Lấy grade nếu có
            grade_obj = None
            try:
                grade_obj = Grade.objects.get(
                    student=student,
                    courseClass=course_class,
                    semester=reg.semester
                )
            except Grade.DoesNotExist:
                pass
            
            data.append({
                'registrationId': reg.registrationId,
                'courseClassId': course_class.courseClassId,
                'courseCode': course_class.courseCode,
                'courseName': course_class.courseName,
                'subject': course_class.subject.subjectName,
                'subjectCode': course_class.subject.subjectCode,
                'credits': course_class.subject.credits,
                'semester': reg.semester.semesterName,
                'semesterId': reg.semester.semesterId,
                'status': reg.status,
                'registrationDate': reg.registrationDate.isoformat(),
                'teacher': course_class.teacher.user.full_name if course_class.teacher else None,
                'grade': {
                    'letterGrade': grade_obj.letterGrade if grade_obj else None,
                    'averageScore': float(grade_obj.average_score) if grade_obj and grade_obj.average_score else None,
                    'gradePoint': float(grade_obj.gradePoint) if grade_obj and grade_obj.gradePoint else None,
                    'isPassed': grade_obj.isPassed if grade_obj else None,
                } if grade_obj else None,
                'completedDate': reg.registrationDate.isoformat()  # Using registration date as completed date
            })
            processed_course_ids.add(course_class.courseClassId)
        
        # Thêm các courses từ passed grades (chưa có trong completed registrations)
        for grade in passed_grades:
            course_class = grade.courseClass
            # Skip nếu không có courseClass hoặc đã xử lý
            if not course_class or course_class.courseClassId in processed_course_ids:
                continue
            
            # Tìm registration tương ứng
            reg = CourseRegistration.objects.filter(
                student=student,
                courseClass=course_class,
                semester=grade.semester
            ).first()
            
            data.append({
                'registrationId': reg.registrationId if reg else None,
                'courseClassId': course_class.courseClassId,
                'courseCode': course_class.courseCode,
                'courseName': course_class.courseName,
                'subject': course_class.subject.subjectName,
                'subjectCode': course_class.subject.subjectCode,
                'credits': course_class.subject.credits,
                'semester': grade.semester.semesterName,
                'semesterId': grade.semester.semesterId,
                'status': 'completed',
                'registrationDate': reg.registrationDate.isoformat() if reg else None,
                'teacher': course_class.teacher.user.full_name if course_class.teacher else None,
                'grade': {
                    'letterGrade': grade.letterGrade,
                    'averageScore': float(grade.average_score) if grade.average_score else None,
                    'gradePoint': float(grade.gradePoint),
                    'isPassed': grade.isPassed,
                },
                'completedDate': grade.updatedAt.isoformat() if hasattr(grade, 'updatedAt') else None
            })
            processed_course_ids.add(course_class.courseClassId)
        
        # Sort by completed date (most recent first)
        data.sort(key=lambda x: x.get('completedDate') or x.get('registrationDate') or '', reverse=True)
        
        return JsonResponse({
            'completedCourses': data,
            'total': len(data),
            'totalCredits': sum(c['credits'] for c in data)
        })
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
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
            semester_id = payload.get('semesterId')  # Optional - tự động lấy học kỳ active nếu không có
            purpose = payload.get('purpose')
            if not document_type_id or not purpose:
                return JsonResponse({'error': 'documentTypeId and purpose are required'}, status=400)

            document_type = DocumentType.objects.get(documentTypeId=document_type_id)
            
            # Tự động lấy học kỳ active nếu không có semesterId
            if semester_id:
                semester = Semester.objects.get(semesterId=semester_id)
            else:
                semester = Semester.objects.filter(status='active').first()
                if not semester:
                    return JsonResponse({'error': 'No active semester found'}, status=400)

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