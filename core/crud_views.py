from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
import json
from .models import *
from .permissions import require_permission, require_role
from datetime import datetime, date
from decimal import Decimal
from django.utils import timezone

# ============ DEPARTMENT CRUD ============
@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["POST"])
def create_department(request):
    try:
        data = json.loads(request.body)
        department = Department.objects.create(
            departmentId=data['departmentId'],
            departmentCode=data['departmentCode'],
            departmentName=data['departmentName'],
            status=data.get('status', 'active')
        )
        return JsonResponse({'message': 'Department created', 'id': department.departmentId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def list_departments(request):
    """Xem danh sách khoa - Tất cả user đã đăng nhập đều có thể xem"""
    try:
        # Kiểm tra user đã đăng nhập
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        departments = Department.objects.filter(status='active').values(
            'departmentId', 'departmentCode', 'departmentName', 'status'
        )
        return JsonResponse({'departments': list(departments)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_permission('manage_departments')
@require_http_methods(["GET"])
def get_department(request, dept_id):
    try:
        dept = Department.objects.get(departmentId=dept_id)
        return JsonResponse({
            'departmentId': dept.departmentId,
            'departmentCode': dept.departmentCode,
            'departmentName': dept.departmentName,
            'status': dept.status
        })
    except Department.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)

@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["PUT"])
def update_department(request, dept_id):
    try:
        data = json.loads(request.body)
        dept = Department.objects.get(departmentId=dept_id)
        for key, value in data.items():
            setattr(dept, key, value)
        dept.save()
        return JsonResponse({'message': 'Department updated'})
    except Department.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)

@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_department(request, dept_id):
    try:
        dept = Department.objects.get(departmentId=dept_id)
        dept.delete()
        return JsonResponse({'message': 'Department deleted'})
    except Department.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)

# ============ MAJOR CRUD ============
@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["POST"])
def create_major(request):
    try:
        data = json.loads(request.body)
        department = Department.objects.get(departmentId=data['departmentId'])
        major = Major.objects.create(
            majorId=data['majorId'],
            majorCode=data['majorCode'],
            majorName=data['majorName'],
            department=department,
            durationYears=data['durationYears'],
            totalCredits=data['totalCredits']
        )
        return JsonResponse({'message': 'Major created', 'id': major.majorId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_majors(request):
    majors = Major.objects.select_related('department').all()
    data = [{
        'majorId': m.majorId,
        'majorCode': m.majorCode,
        'majorName': m.majorName,
        'department': m.department.departmentName,
        'durationYears': m.durationYears,
        'totalCredits': m.totalCredits
    } for m in majors]
    return JsonResponse({'majors': data})

@require_http_methods(["GET"])
def get_major(request, major_id):
    try:
        major = Major.objects.select_related('department').get(majorId=major_id)
        return JsonResponse({
            'majorId': major.majorId,
            'majorCode': major.majorCode,
            'majorName': major.majorName,
            'department': major.department.departmentName,
            'durationYears': major.durationYears,
            'totalCredits': major.totalCredits
        })
    except Major.DoesNotExist:
        return JsonResponse({'error': 'Major not found'}, status=404)

@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["PUT"])
def update_major(request, major_id):
    try:
        data = json.loads(request.body)
        major = Major.objects.get(majorId=major_id)
        if 'departmentId' in data:
            major.department = Department.objects.get(departmentId=data['departmentId'])
        for key, value in data.items():
            if key != 'departmentId':
                setattr(major, key, value)
        major.save()
        return JsonResponse({'message': 'Major updated'})
    except Major.DoesNotExist:
        return JsonResponse({'error': 'Major not found'}, status=404)

@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_major(request, major_id):
    try:
        major = Major.objects.get(majorId=major_id)
        major.delete()
        return JsonResponse({'message': 'Major deleted'})
    except Major.DoesNotExist:
        return JsonResponse({'error': 'Major not found'}, status=404)

# ============ SUBJECT CRUD ============
@require_permission('manage_subjects')
@csrf_exempt
@require_http_methods(["POST"])
def create_subject(request):
    try:
        data = json.loads(request.body)
        department = Department.objects.get(departmentId=data['departmentId'])
        subject = Subject.objects.create(
            subjectId=data['subjectId'],
            subjectCode=data['subjectCode'],
            subjectName=data['subjectName'],
            department=department,
            credits=data['credits'],
            theoryHours=data['theoryHours'],
            practiceHours=data['practiceHours']
        )
        return JsonResponse({'message': 'Subject created', 'id': subject.subjectId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_subjects(request):
    subjects = Subject.objects.select_related('department').all()
    data = [{
        'subjectId': s.subjectId,
        'subjectCode': s.subjectCode,
        'subjectName': s.subjectName,
        'department': s.department.departmentName,
        'credits': s.credits,
        'theoryHours': s.theoryHours,
        'practiceHours': s.practiceHours
    } for s in subjects]
    return JsonResponse({'subjects': data})

@require_http_methods(["GET"])
def get_subject(request, subject_id):
    try:
        subject = Subject.objects.select_related('department').get(subjectId=subject_id)
        return JsonResponse({
            'subjectId': subject.subjectId,
            'subjectCode': subject.subjectCode,
            'subjectName': subject.subjectName,
            'department': subject.department.departmentName,
            'credits': subject.credits,
            'theoryHours': subject.theoryHours,
            'practiceHours': subject.practiceHours
        })
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)

@require_permission('manage_subjects')
@csrf_exempt
@require_http_methods(["PUT"])
def update_subject(request, subject_id):
    try:
        data = json.loads(request.body)
        subject = Subject.objects.get(subjectId=subject_id)
        if 'departmentId' in data:
            subject.department = Department.objects.get(departmentId=data['departmentId'])
        for key, value in data.items():
            if key != 'departmentId':
                setattr(subject, key, value)
        subject.save()
        return JsonResponse({'message': 'Subject updated'})
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)

@require_permission('manage_subjects')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_subject(request, subject_id):
    try:
        subject = Subject.objects.get(subjectId=subject_id)
        subject.delete()
        return JsonResponse({'message': 'Subject deleted'})
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Subject not found'}, status=404)

# ============ STUDENT CLASS CRUD ============
@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["POST"])
def create_student_class(request):
    try:
        data = json.loads(request.body)
        major = Major.objects.get(majorId=data['majorId'])
        student_class = StudentClass.objects.create(
            classId=data['classId'],
            classCode=data['classCode'],
            className=data['className'],
            major=major,
            academicYear=data['academicYear'],
            maxStudents=data['maxStudents']
        )
        return JsonResponse({'message': 'Student class created', 'id': student_class.classId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_student_classes(request):
    classes = StudentClass.objects.select_related('major').all()
    data = [{
        'classId': c.classId,
        'classCode': c.classCode,
        'className': c.className,
        'major': c.major.majorName,
        'academicYear': c.academicYear,
        'maxStudents': c.maxStudents,
        'currentStudents': c.currentStudents
    } for c in classes]
    return JsonResponse({'classes': data})

# ============ ACADEMIC YEAR CRUD ============
@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["POST"])
def create_academic_year(request):
    try:
        data = json.loads(request.body)
        academic_year = AcademicYear.objects.create(
            yearId=data['yearId'],
            yearCode=data['yearCode'],
            yearName=data['yearName'],
            startDate=datetime.strptime(data['startDate'], '%Y-%m-%d').date(),
            endDate=datetime.strptime(data['endDate'], '%Y-%m-%d').date()
        )
        return JsonResponse({'message': 'Academic year created', 'id': academic_year.yearId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_academic_years(request):
    years = AcademicYear.objects.all().values()
    return JsonResponse({'academic_years': list(years)})

# ============ SEMESTER CRUD ============
@require_permission('manage_departments')
@csrf_exempt
@require_http_methods(["POST"])
def create_semester(request):
    try:
        data = json.loads(request.body)
        academic_year = AcademicYear.objects.get(yearId=data['academicYearId'])
        semester = Semester.objects.create(
            semesterId=data['semesterId'],
            semesterCode=data['semesterCode'],
            semesterName=data['semesterName'],
            academicYear=academic_year,
            startDate=datetime.strptime(data['startDate'], '%Y-%m-%d').date(),
            endDate=datetime.strptime(data['endDate'], '%Y-%m-%d').date(),
            registrationStart=datetime.strptime(data['registrationStart'], '%Y-%m-%d %H:%M:%S'),
            registrationEnd=datetime.strptime(data['registrationEnd'], '%Y-%m-%d %H:%M:%S')
        )
        return JsonResponse({'message': 'Semester created', 'id': semester.semesterId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_semesters(request):
    semesters = Semester.objects.select_related('academicYear').all()
    data = [{
        'semesterId': s.semesterId,
        'semesterCode': s.semesterCode,
        'semesterName': s.semesterName,
        'academicYear': s.academicYear.yearName,
        'startDate': s.startDate.isoformat(),
        'endDate': s.endDate.isoformat()
    } for s in semesters]
    return JsonResponse({'semesters': data})

# ============ COURSE CLASS CRUD ============
@require_permission('manage_subjects')
@csrf_exempt
@require_http_methods(["POST"])
def create_course_class(request):
    try:
        data = json.loads(request.body)
        subject = Subject.objects.get(subjectId=data['subjectId'])
        semester = Semester.objects.get(semesterId=data['semesterId'])
        
        teacher = None
        if data.get('teacherId'):
            try:
                teacher = Teacher.objects.get(teacherId=data['teacherId'])
            except Teacher.DoesNotExist:
                pass
        
        course_class = CourseClass.objects.create(
            courseClassId=data['courseClassId'],
            courseCode=data['courseCode'],
            courseName=data['courseName'],
            subject=subject,
            teacher=teacher,
            semester=semester,
            room=data['room'],
            maxStudents=data['maxStudents']
        )
        return JsonResponse({'message': 'Course class created', 'id': course_class.courseClassId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_course_classes(request):
    classes = CourseClass.objects.select_related('subject', 'teacher__user', 'semester').all()
    data = [{
        'courseClassId': c.courseClassId,
        'courseCode': c.courseCode,
        'courseName': c.courseName,
        'subject': c.subject.subjectName,
        'teacher': c.teacher.user.full_name if c.teacher else None,
        'semester': c.semester.semesterName,
        'room': c.room,
        'maxStudents': c.maxStudents,
        'currentStudents': c.currentStudents
    } for c in classes]
    return JsonResponse({'course_classes': data})

@require_permission('manage_subjects')
@csrf_exempt
@require_http_methods(["PUT"])
def update_course_class(request, class_id):
    try:
        data = json.loads(request.body)
        course_class = CourseClass.objects.get(courseClassId=class_id)
        
        if 'subjectId' in data:
            course_class.subject = Subject.objects.get(subjectId=data['subjectId'])
        if 'semesterId' in data:
            course_class.semester = Semester.objects.get(semesterId=data['semesterId'])
        if 'teacherId' in data:
            try:
                course_class.teacher = Teacher.objects.get(teacherId=data['teacherId'])
            except Teacher.DoesNotExist:
                course_class.teacher = None
        
        for key, value in data.items():
            if key not in ['subjectId', 'semesterId', 'teacherId'] and hasattr(course_class, key):
                setattr(course_class, key, value)
        
        course_class.save()
        return JsonResponse({'message': 'Course class updated'})
    except CourseClass.DoesNotExist:
        return JsonResponse({'error': 'Course class not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('manage_subjects')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_course_class(request, class_id):
    try:
        course_class = CourseClass.objects.get(courseClassId=class_id)
        course_class.delete()
        return JsonResponse({'message': 'Course class deleted'})
    except CourseClass.DoesNotExist:
        return JsonResponse({'error': 'Course class not found'}, status=404)

# ============ COURSE REGISTRATION CRUD ============
@require_permission('register_course')
@csrf_exempt
@require_http_methods(["POST"])
def register_course(request):
    try:
        data = json.loads(request.body)
        student = Student.objects.get(studentId=data['studentId'])
        course_class = CourseClass.objects.get(courseClassId=data['courseClassId'])
        semester = Semester.objects.get(semesterId=data['semesterId'])
        
        registration = CourseRegistration.objects.create(
            registrationId=data['registrationId'],
            student=student,
            courseClass=course_class,
            semester=semester,
            registrationDate=datetime.now().date()
        )
        return JsonResponse({'message': 'Course registered', 'id': registration.registrationId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('view_students')
@require_http_methods(["GET"])
def list_registrations(request):
    registrations = CourseRegistration.objects.select_related(
        'student__user', 'courseClass', 'semester'
    ).all()
    data = [{
        'registrationId': r.registrationId,
        'student': r.student.user.full_name,
        'courseClass': r.courseClass.courseName,
        'semester': r.semester.semesterName,
        'registrationDate': r.registrationDate.isoformat(),
        'status': r.status
    } for r in registrations]
    return JsonResponse({'registrations': data})

# ============ GRADE CRUD ============
@require_permission('input_grades')
@csrf_exempt
@require_http_methods(["POST"])
def create_grade(request):
    try:
        data = json.loads(request.body)
        student = Student.objects.get(studentId=data['studentId'])
        subject = Subject.objects.get(subjectId=data['subjectId'])
        teacher = Teacher.objects.get(teacherId=data['teacherId'])
        course_class = CourseClass.objects.get(courseClassId=data['courseClassId'])
        semester = Semester.objects.get(semesterId=data['semesterId'])
        
        grade = Grade.objects.create(
            gradeId=data['gradeId'],
            student=student,
            subject=subject,
            teacher=teacher,
            courseClass=course_class,
            semester=semester,
            assginmentscore=data.get('assignmentScore'),
            midterm_score=data.get('midtermScore'),
            final_score=data.get('finalScore'),
            average_score=data.get('averageScore'),
            letterGrade=data['letterGrade'],
            gradePoint=data['gradePoint'],
            isPassed=data['isPassed']
        )
        return JsonResponse({'message': 'Grade created', 'id': grade.gradeId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_grades(request):
    grades = Grade.objects.select_related(
        'student__user', 'subject', 'teacher__user', 'semester'
    ).all()
    data = [{
        'gradeId': g.gradeId,
        'student': g.student.user.full_name,
        'subject': g.subject.subjectName,
        'teacher': g.teacher.user.full_name,
        'semester': g.semester.semesterName,
        'assignmentScore': float(g.assginmentscore) if g.assginmentscore else None,
        'midtermScore': float(g.midterm_score) if g.midterm_score else None,
        'finalScore': float(g.final_score) if g.final_score else None,
        'averageScore': float(g.average_score) if g.average_score else None,
        'letterGrade': g.letterGrade,
        'gradePoint': float(g.gradePoint),
        'isPassed': g.isPassed
    } for g in grades]
    return JsonResponse({'grades': data})

# ============ TUITION FEE CRUD ============
@require_permission('manage_tuition')
@csrf_exempt
@require_http_methods(["POST"])
def create_tuition_fee(request):
    try:
        data = json.loads(request.body)
        student = Student.objects.get(studentId=data['studentId'])
        semester = Semester.objects.get(semesterId=data['semesterId'])
        
        tuition = TuitionFee.objects.create(
            tuitionFee=data['tuitionFeeId'],
            student=student,
            semester=semester,
            totalCredit=data['totalCredits'],
            feePerCredit=Decimal(data['feePerCredit']),
            totalAmount=Decimal(data['totalAmount']),
            paidAmount=Decimal(data.get('paidAmount', 0)),
            dueDate=datetime.strptime(data['dueDate'], '%Y-%m-%d').date()
        )
        return JsonResponse({'message': 'Tuition fee created', 'id': tuition.tuitionFee})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('view_tuition')
@require_http_methods(["GET"])
def list_tuition_fees(request):
    tuitions = TuitionFee.objects.select_related('student__user', 'semester').all()
    data = [{
        'tuitionFeeId': t.tuitionFee,
        'student': t.student.user.full_name,
        'semester': t.semester.semesterName,
        'totalCredits': t.totalCredit,
        'feePerCredit': float(t.feePerCredit),
        'totalAmount': float(t.totalAmount),
        'paidAmount': float(t.paidAmount),
        'paymentStatus': t.paymentStatus,
        'dueDate': t.dueDate.isoformat()
    } for t in tuitions]
    return JsonResponse({'tuition_fees': data})

# ============ DOCUMENT REQUEST CRUD ============
@require_permission('request_document')
@csrf_exempt
@require_http_methods(["POST"])
def create_document_request(request):
    try:
        data = json.loads(request.body)
        document_type = DocumentType.objects.get(documentTypeId=data['documentTypeId'])
        semester = Semester.objects.get(semesterId=data['semesterId'])
        
        doc_request = DocumentRequest.objects.create(
            requestId=data['requestId'],
            documentType=document_type,
            semester=semester,
            requestDate=datetime.now(),
            purpose=data['purpose']
        )
        
        # Add students to the request
        student_ids = data.get('studentIds', [])
        for student_id in student_ids:
            student = Student.objects.get(studentId=student_id)
            doc_request.student.add(student)
        
        return JsonResponse({'message': 'Document request created', 'id': doc_request.requestId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('approve_documents')
@require_http_methods(["GET"])
def list_document_requests(request):
    requests = DocumentRequest.objects.select_related('documentType', 'semester').all()
    data = [{
        'requestId': r.requestId,
        'documentType': r.documentType.name,
        'semester': r.semester.semesterName,
        'requestDate': r.requestDate.isoformat(),
        'purpose': r.purpose,
        'status': r.status
    } for r in requests]
    return JsonResponse({'document_requests': data})

# ============ NOTIFICATION CRUD ============
@require_permission('manage_users')
@csrf_exempt
@require_http_methods(["POST"])
def create_notification(request):
    try:
        data = json.loads(request.body)
        notification = Notification.objects.create(
            notificationId=data['notificationId'],
            createdBy=request.user,
            title=data['title'],
            content=data['content'],
            targetAudience=data['targetAudience'],
            notificationType=data['notificationType'],
            priority=data['priority']
        )
        notification.set_target_ids(data.get('targetIds', []))
        notification.save()
        return JsonResponse({'message': 'Notification created', 'id': notification.notificationId})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["GET"])
def list_notifications(request):
    notifications = Notification.objects.select_related('createdBy').all()
    data = [{
        'notificationId': n.notificationId,
        'title': n.title,
        'content': n.content,
        'targetAudience': n.targetAudience,
        'notificationType': n.notificationType,
        'priority': n.priority,
        'createdBy': n.createdBy.full_name if n.createdBy else None
    } for n in notifications]
    return JsonResponse({'notifications': data})

@require_permission('manage_users')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(notificationId=notification_id)
        notification.delete()
        return JsonResponse({'message': 'Notification deleted'})
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Notification not found'}, status=404)

# ============ USER CRUD (Students/Teachers) ============
@require_permission('manage_users')
@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'full_name', 'user_type']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            full_name=data['full_name'],
            user_type=data['user_type']
        )
        
        # Set optional fields if they exist in model
        if hasattr(user, 'phone'):
            user.phone = data.get('phone', '')
        if hasattr(user, 'address'):
            user.address = data.get('address', '')
        user.save()
        
        # Create Student or Teacher profile
        if data['user_type'] == 'student':
            student = Student.objects.create(
                studentId=data['username'],
                user=user,
                enrollmentYear=data.get('enrollmentYear', str(timezone.now().year))
            )
        elif data['user_type'] == 'teacher':
            Teacher.objects.create(
                teacherId=data['username'],
                user=user
            )
        
        return JsonResponse({'message': f'{data["user_type"].title()} created', 'id': user.id})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('manage_users')
@require_http_methods(["GET"])
def list_users(request):
    user_type = request.GET.get('user_type')
    users = User.objects.all()
    if user_type:
        users = users.filter(user_type=user_type)
    
    data = []
    for u in users:
        user_data = {
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'full_name': u.full_name,
            'user_type': u.user_type,
            'phone': getattr(u, 'phone', ''),
            'address': getattr(u, 'address', ''),
            'status': u.status,
            'created_at': u.created_at.isoformat()
        }
        
        # Add enrollmentYear for students
        if u.user_type == 'student':
            try:
                student = Student.objects.get(user=u)
                user_data['enrollmentYear'] = getattr(student, 'enrollmentYear', '')
            except Student.DoesNotExist:
                user_data['enrollmentYear'] = ''
        
        data.append(user_data)
    
    return JsonResponse({'users': data})

@require_permission('manage_users')
@require_http_methods(["GET"])
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'user_type': user.user_type,
            'phone': getattr(user, 'phone', ''),
            'address': getattr(user, 'address', ''),
            'status': user.status,
            'created_at': user.created_at.isoformat()
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@require_permission('manage_users')
@csrf_exempt
@require_http_methods(["PUT"])
def update_user(request, user_id):
    try:
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)
        
        # Update user fields
        for key, value in data.items():
            if key != 'password' and hasattr(user, key):
                setattr(user, key, value)
        
        # Update password if provided
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        user.save()
        return JsonResponse({'message': 'User updated'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_permission('manage_users')
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


# ============ TEACHER LIST ============
@require_http_methods(["GET"])
def list_teachers(request):
    teachers = Teacher.objects.select_related('user').all()
    data = [{
        'teacherId': t.teacherId,
        'teacherCode': t.teacherCode,
        'full_name': t.user.full_name,
        'position': t.position
    } for t in teachers]
    return JsonResponse({'teachers': data})

# ============ DOCUMENT TYPE CRUD ============
@csrf_exempt
@require_http_methods(["GET"])
def list_document_types(request):
    """Xem loại tài liệu có thể yêu cầu"""
    try:
        document_types = DocumentType.objects.all()
        data = [{
            'typeId': dt.documentTypeId,
            'typeName': dt.name,
            'description': dt.description,
            'processingTime': dt.processingDays,
            'maxRequestsPerSemester': dt.maxRequestsPerSemester
        } for dt in document_types]
        
        return JsonResponse({'documentTypes': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
