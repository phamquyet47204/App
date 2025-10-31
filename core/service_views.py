from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
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
    try:
        data = json.loads(request.body)
        student_id = data.get('studentId')
        subject_id = data.get('subjectId')
        if not student_id or not subject_id:
            return JsonResponse({'error': 'studentId and subjectId are required'}, status=400)

        try:
            student = Student.objects.get(studentId=student_id)
        except Student.DoesNotExist:
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
    try:
        data = json.loads(request.body)
        student_id = data.get('studentId')
        course_class_id = data.get('courseClassId')
        if not student_id or not course_class_id:
            return JsonResponse({'error': 'studentId and courseClassId are required'}, status=400)

        try:
            student = Student.objects.get(studentId=student_id)
        except Student.DoesNotExist:
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
    try:
        # Đơn giản hóa - chỉ trả về tất cả course classes
        all_courses = CourseClass.objects.filter(status=True).select_related('subject')
        
        data = [{
            'courseClassId': c.courseClassId,
            'courseCode': c.courseCode,
            'courseName': c.courseName,
            'subject': c.subject.subjectName,
            'credits': c.subject.credits,
            'room': c.room
        } for c in all_courses]
        
        return JsonResponse({'courses': data})
    except Exception as e:
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

