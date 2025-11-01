from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
import json
import csv
from decimal import Decimal
from .models import *
from .permissions import require_permission
from django.db.models import Avg, Count, Q, F
from django.db import models

# ============ GRADE SERVICE ============
@require_permission('input_grades')
@csrf_exempt
@require_http_methods(["POST"])
def calculate_gpa(request):
    try:
        data = json.loads(request.body)
        student = Student.objects.get(studentId=data['studentId'])
        
        grades = Grade.objects.filter(student=student, isPassed=True)
        if not grades.exists():
            return JsonResponse({'gpa': 0.0})
        
        total_points = sum(float(g.gradePoint) * g.subject.credits for g in grades)
        total_credits = sum(g.subject.credits for g in grades)
        gpa = total_points / total_credits if total_credits > 0 else 0
        
        # Update student GPA
        student.gpa = round(gpa, 2)
        student.totalCredits = total_credits
        student.save()
        
        return JsonResponse({'gpa': round(gpa, 2), 'totalCredits': total_credits})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('export_grades')
@require_http_methods(["GET"])
def export_class_grades(request, class_id):
    try:
        course_class = CourseClass.objects.get(courseClassId=class_id)
        grades = Grade.objects.filter(courseClass=course_class).select_related(
            'student__user', 'subject'
        )
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="grades_{course_class.courseCode}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student Code', 'Student Name', 'Subject', 'Assignment', 'Midterm', 'Final', 'Average', 'Letter Grade', 'Passed'])
        
        for grade in grades:
            writer.writerow([
                grade.student.studentCode,
                grade.student.user.full_name,
                grade.subject.subjectName,
                grade.assginmentscore or 0,
                grade.midterm_score or 0,
                grade.final_score or 0,
                grade.average_score or 0,
                grade.letterGrade,
                'Yes' if grade.isPassed else 'No'
            ])
        
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('view_students')
@require_http_methods(["GET"])
def class_statistics(request, class_id):
    try:
        course_class = CourseClass.objects.get(courseClassId=class_id)
        grades = Grade.objects.filter(courseClass=course_class)
        
        stats = {
            'totalStudents': grades.count(),
            'passedStudents': grades.filter(isPassed=True).count(),
            'failedStudents': grades.filter(isPassed=False).count(),
            'averageScore': grades.aggregate(avg=Avg('average_score'))['avg'] or 0,
            'gradeDistribution': {}
        }
        
        # Grade distribution
        for grade in ['A', 'B', 'C', 'D', 'F']:
            count = grades.filter(letterGrade=grade).count()
            stats['gradeDistribution'][grade] = count
        
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# ============ REGISTRATION SERVICE ============
@require_permission('register_course')
@csrf_exempt
@require_http_methods(["POST"])
def check_prerequisites(request):
    """
    Kiểm tra prerequisites - studentId có thể là studentId hoặc username
    Nếu không có studentId, tự động lấy từ user hiện tại
    """
    try:
        data = json.loads(request.body)
        subject_id = data.get('subjectId')
        if not subject_id:
            return JsonResponse({'error': 'subjectId is required'}, status=400)
        
        # Lấy student - ưu tiên từ user hiện tại, nếu không thì từ studentId/username trong payload
        student = None
        student_id = data.get('studentId')
        
        if not student_id:
            # Tự động lấy từ user hiện tại
            try:
                student = Student.objects.get(user=request.user)
            except Student.DoesNotExist:
                return JsonResponse({'error': 'Student profile not found. Please provide studentId or ensure you are logged in as a student.'}, status=404)
        else:
            # Thử tìm theo studentId hoặc username
            try:
                student = Student.objects.get(studentId=student_id)
            except Student.DoesNotExist:
                try:
                    user = User.objects.get(username=student_id)
                    student = Student.objects.get(user=user)
                except (User.DoesNotExist, Student.DoesNotExist):
                    return JsonResponse({'error': 'Student not found'}, status=404)
        
        try:
            subject = Subject.objects.get(subjectId=subject_id)
        except Subject.DoesNotExist:
            return JsonResponse({'error': 'Subject not found'}, status=404)

        # Check if student has completed prerequisites
        prerequisites = subject.prerequisites.all()
        missing_prerequisites = []

        for prereq in prerequisites:
            passed_grade = Grade.objects.filter(
                student=student,
                subject=prereq,
                isPassed=True
            ).exists()

            if not passed_grade:
                missing_prerequisites.append({
                    'subjectCode': prereq.subjectCode,
                    'subjectName': prereq.subjectName
                })

        can_register = len(missing_prerequisites) == 0

        return JsonResponse({
            'canRegister': can_register,
            'missingPrerequisites': missing_prerequisites
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('register_course')
@csrf_exempt
@require_http_methods(["POST"])
def check_schedule_conflict(request):
    """
    Kiểm tra schedule conflict - studentId có thể là studentId hoặc username
    Nếu không có studentId, tự động lấy từ user hiện tại
    """
    try:
        data = json.loads(request.body)
        course_class_id = data.get('courseClassId')
        if not course_class_id:
            return JsonResponse({'error': 'courseClassId is required'}, status=400)
        
        # Lấy student - ưu tiên từ user hiện tại, nếu không thì từ studentId/username trong payload
        student = None
        student_id = data.get('studentId')
        
        if not student_id:
            # Tự động lấy từ user hiện tại
            try:
                student = Student.objects.get(user=request.user)
            except Student.DoesNotExist:
                return JsonResponse({'error': 'Student profile not found. Please provide studentId or ensure you are logged in as a student.'}, status=404)
        else:
            # Thử tìm theo studentId hoặc username
            try:
                student = Student.objects.get(studentId=student_id)
            except Student.DoesNotExist:
                try:
                    user = User.objects.get(username=student_id)
                    student = Student.objects.get(user=user)
                except (User.DoesNotExist, Student.DoesNotExist):
                    return JsonResponse({'error': 'Student not found'}, status=404)
        
        try:
            course_class = CourseClass.objects.get(courseClassId=course_class_id)
        except CourseClass.DoesNotExist:
            return JsonResponse({'error': 'Course class not found'}, status=404)

        # Get student's current registrations for the semester
        current_registrations = CourseRegistration.objects.filter(
            student=student,
            semester=course_class.semester,
            status='registered'
        ).select_related('courseClass')

        conflicts = []
        for reg in current_registrations:
            if reg.courseClass.schedule == course_class.schedule:
                conflicts.append({
                    'courseCode': reg.courseClass.courseCode,
                    'courseName': reg.courseClass.courseName,
                    'schedule': str(reg.courseClass.schedule)
                })

        has_conflict = len(conflicts) > 0

        return JsonResponse({
            'hasConflict': has_conflict,
            'conflicts': conflicts
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
@csrf_exempt
def available_courses(request, student_id):
    """
    Lấy danh sách môn học có thể đăng ký cho student
    - Chỉ lấy courses của semester active
    - Loại bỏ courses đã đăng ký
    - Chỉ lấy courses còn chỗ (currentStudents < maxStudents)
    - Kiểm tra registration period
    
    student_id có thể là studentId hoặc username
    """
    try:
        # Lấy student - thử tìm theo studentId trước, sau đó theo username
        try:
            student = Student.objects.get(studentId=student_id)
        except Student.DoesNotExist:
            try:
                # Nếu không tìm thấy theo studentId, thử tìm theo username
                user = User.objects.get(username=student_id)
                student = Student.objects.get(user=user)
            except (User.DoesNotExist, Student.DoesNotExist):
                return JsonResponse({'error': 'Student not found'}, status=404)
        
        # Lấy semester active
        active_semester = Semester.objects.filter(status='active').first()
        if not active_semester:
            return JsonResponse({'courses': [], 'message': 'No active semester'})
        
        # Kiểm tra registration period
        now = timezone.now()
        
        # Nếu không có registration period được set, coi như luôn mở
        if not active_semester.registrationStart or not active_semester.registrationEnd:
            is_in_registration_period = True
        else:
            # Kiểm tra xem có trong period không
            is_in_registration_period = (
                active_semester.registrationStart <= now <= active_semester.registrationEnd
            )
            
            # Nếu period ở quá xa trong tương lai (> 1 năm), coi như lỗi data và mở luôn
            if active_semester.registrationStart > now + timedelta(days=365):
                print(f"WARNING: Registration period seems to be in the far future, treating as open")
                is_in_registration_period = True
        
        print(f"DEBUG: Registration period check:")
        print(f"  - Now: {now}")
        print(f"  - Start: {active_semester.registrationStart}")
        print(f"  - End: {active_semester.registrationEnd}")
        print(f"  - Is open: {is_in_registration_period}")
        
        # Debug: In ra thông tin
        print(f"DEBUG: Student: {student.studentId}, Semester: {active_semester.semesterId}")
        
        # Lấy courses của semester active, còn chỗ, chưa đăng ký
        registered_course_ids = CourseRegistration.objects.filter(
            student=student,
            semester=active_semester,
            status__in=['registered', 'pending']
        ).values_list('courseClass__courseClassId', flat=True)
        
        print(f"DEBUG: Registered courses: {list(registered_course_ids)}")
        
        # Kiểm tra tất cả courses trong semester
        all_courses_in_semester = CourseClass.objects.filter(semester=active_semester)
        print(f"DEBUG: Total courses in semester: {all_courses_in_semester.count()}")
        for c in all_courses_in_semester:
            print(f"  - {c.courseClassId}: status={c.status} (type: {type(c.status)}), current={c.currentStudents}, max={c.maxStudents}")
        
        # Filter courses - status là BooleanField với default=True
        # Chỉ filter status=True nếu có, nếu không thì lấy tất cả
        available_courses = CourseClass.objects.filter(
            semester=active_semester,
            status=True  # BooleanField
        ).exclude(
            courseClassId__in=registered_course_ids
        ).filter(
            currentStudents__lt=F('maxStudents')
        ).select_related('subject', 'teacher__user', 'semester')
        
        print(f"DEBUG: Available courses after filter: {available_courses.count()}")
        for c in available_courses:
            print(f"  - Available: {c.courseClassId} ({c.courseCode})")
        
        # Build response data
        data = []
        for course in available_courses:
            # Kiểm tra prerequisites
            prerequisites = course.subject.prerequisites.all()
            prerequisites_met = True
            prerequisites_info = []
            
            if prerequisites.exists():
                # Kiểm tra student đã pass prerequisites chưa
                for prereq in prerequisites:
                    prereq_grade = Grade.objects.filter(
                        student=student,
                        subject=prereq,
                        isPassed=True
                    ).exists()
                    prerequisites_info.append({
                        'subjectCode': prereq.subjectCode,
                        'subjectName': prereq.subjectName,
                        'met': prereq_grade
                    })
                    if not prereq_grade:
                        prerequisites_met = False
            
            # Tính số chỗ còn lại
            available_slots = course.maxStudents - course.currentStudents
            
            course_data = {
                'courseClassId': course.courseClassId,
                'courseCode': course.courseCode,
                'courseName': course.courseName,
                'subject': {
                    'subjectId': course.subject.subjectId,
                    'subjectCode': course.subject.subjectCode,
                    'subjectName': course.subject.subjectName,
                    'credits': course.subject.credits
                },
                'teacher': {
                    'teacherId': course.teacher.teacherId if course.teacher else None,
                    'teacherCode': course.teacher.teacherCode if course.teacher else None,
                    'name': course.teacher.user.full_name if course.teacher else 'TBA'
                },
                'semester': {
                    'semesterId': course.semester.semesterId,
                    'semesterName': course.semester.semesterName
                },
                'room': course.room,
                'maxStudents': course.maxStudents,
                'currentStudents': course.currentStudents,
                'availableSlots': available_slots,
                'prerequisites': prerequisites_info,
                'prerequisitesMet': prerequisites_met,
                'canRegister': prerequisites_met and is_in_registration_period and available_slots > 0,
                'registrationPeriod': is_in_registration_period,
                'registrationStart': active_semester.registrationStart.isoformat() if active_semester.registrationStart else None,
                'registrationEnd': active_semester.registrationEnd.isoformat() if active_semester.registrationEnd else None
            }
            
            # Thêm schedule info nếu có (parse từ DateTimeField)
            if course.schedule:
                # Parse datetime thành day of week và time
                schedule_dt = course.schedule
                # Lấy tên thứ trong tuần
                days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_index = schedule_dt.weekday()  # 0=Monday, 6=Sunday
                day_name = days_of_week[day_index]
                
                # Format thời gian
                start_time = schedule_dt.strftime('%H:%M')
                # Giả sử mỗi lớp học kéo dài 2 giờ (có thể điều chỉnh)
                end_time = (schedule_dt + timedelta(hours=2)).strftime('%H:%M')
                
                course_data['schedule'] = {
                    'dayOfWeek': day_name.lower(),  # monday, tuesday, ...
                    'dayOfWeekDisplay': day_name,  # Monday, Tuesday, ...
                    'startTime': start_time,
                    'endTime': end_time,
                    'datetime': schedule_dt.isoformat(),
                    'date': schedule_dt.strftime('%Y-%m-%d'),
                    'time': start_time + ' - ' + end_time
                }
            
            data.append(course_data)
        
        return JsonResponse({
            'courses': data,
            'semester': {
                'semesterId': active_semester.semesterId,
                'semesterName': active_semester.semesterName,
                'isRegistrationOpen': is_in_registration_period
            },
            'total': len(data)
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=400)

# ============ NOTIFICATION SERVICE ============
@require_http_methods(["GET"])
def unread_notifications(request):
    try:
        unread = NotificationRecipient.objects.filter(
            user=request.user,
            readAt__isnull=True
        ).select_related('notification').order_by('-notification__scheduledAt')
        
        data = [{
            'notificationId': nr.notification.notificationId,
            'title': nr.notification.title,
            'content': nr.notification.content,
            'notificationType': nr.notification.notificationType,
            'priority': nr.notification.priority,
            'deliveredAt': nr.deliveredAt.isoformat() if nr.deliveredAt else None
        } for nr in unread]
        
        return JsonResponse({'notifications': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id):
    try:
        from django.utils import timezone
        
        recipient = NotificationRecipient.objects.get(
            notification__notificationId=notification_id,
            user=request.user
        )
        recipient.readAt = timezone.now()
        recipient.save()
        
        return JsonResponse({'message': 'Notification marked as read'})
    except NotificationRecipient.DoesNotExist:
        return JsonResponse({'error': 'Notification not found'}, status=404)

# ============ REPORT SERVICE ============
@require_permission('generate_reports')
@require_http_methods(["GET"])
def student_report(request):
    try:
        # Get query parameters
        department_id = request.GET.get('department')
        major_id = request.GET.get('major')
        class_id = request.GET.get('class')
        
        students = Student.objects.select_related('user', 'studentClass__major__department')
        
        if department_id:
            students = students.filter(studentClass__major__department__departmentId=department_id)
        if major_id:
            students = students.filter(studentClass__major__majorId=major_id)
        if class_id:
            students = students.filter(studentClass__classId=class_id)
        
        data = [{
            'studentId': s.studentId,
            'studentCode': s.studentCode,
            'fullName': s.user.full_name,
            'email': s.user.email,
            'class': s.studentClass.className if s.studentClass else None,
            'major': s.studentClass.major.majorName if s.studentClass else None,
            'department': s.studentClass.major.department.departmentName if s.studentClass else None,
            'gpa': float(s.gpa) if s.gpa else 0,
            'totalCredits': s.totalCredits,
            'status': s.user.status
        } for s in students]
        
        return JsonResponse({'students': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('generate_reports')
@require_http_methods(["GET"])
def grade_report(request):
    try:
        semester_id = request.GET.get('semester')
        subject_id = request.GET.get('subject')
        
        grades = Grade.objects.select_related(
            'student__user', 'subject', 'semester', 'courseClass'
        )
        
        if semester_id:
            grades = grades.filter(semester__semesterId=semester_id)
        if subject_id:
            grades = grades.filter(subject__subjectId=subject_id)
        
        data = [{
            'gradeId': g.gradeId,
            'student': g.student.user.full_name,
            'studentCode': g.student.studentCode,
            'subject': g.subject.subjectName,
            'courseClass': g.courseClass.courseName,
            'semester': g.semester.semesterName,
            'averageScore': float(g.average_score) if g.average_score else 0,
            'letterGrade': g.letterGrade,
            'gradePoint': float(g.gradePoint),
            'isPassed': g.isPassed
        } for g in grades]
        
        return JsonResponse({'grades': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

