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
    """
    Đăng ký môn học cho student
    - Tự động lấy student từ user hiện tại
    - Tự sinh registrationId nếu không có
    - Validate các điều kiện (đã đăng ký, hết chỗ, prerequisites, schedule conflict, registration period)
    """
    try:
        data = json.loads(request.body)
        
        # Lấy student từ user hiện tại (student chỉ có thể đăng ký cho mình)
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student profile not found. Please ensure you are logged in as a student.'}, status=404)
        
        # Validate required fields
        course_class_id = data.get('courseClassId')
        if not course_class_id:
            return JsonResponse({'error': 'courseClassId is required'}, status=400)
        
        try:
            course_class = CourseClass.objects.get(courseClassId=course_class_id)
        except CourseClass.DoesNotExist:
            return JsonResponse({'error': 'Course class not found'}, status=404)
        
        # Derive semester from payload or course_class
        semester_id = data.get('semesterId')
        if semester_id:
            try:
                semester = Semester.objects.get(semesterId=semester_id)
            except Semester.DoesNotExist:
                return JsonResponse({'error': 'Semester not found'}, status=404)
        else:
            semester = course_class.semester
        
        # Kiểm tra đã đăng ký chưa
        existing = CourseRegistration.objects.filter(
            student=student,
            courseClass=course_class,
            semester=semester,
            status__in=['registered', 'pending']
        ).first()
        if existing:
            return JsonResponse({
                'error': 'Bạn đã đăng ký môn học này rồi',
                'registrationId': existing.registrationId
            }, status=400)
        
        # Kiểm tra còn chỗ không
        if course_class.currentStudents >= course_class.maxStudents:
            return JsonResponse({'error': 'Lớp học đã đầy'}, status=400)
        
        # Kiểm tra prerequisites
        prerequisites = course_class.subject.prerequisites.all()
        if prerequisites.exists():
            for prereq in prerequisites:
                passed_grade = Grade.objects.filter(
                    student=student,
                    subject=prereq,
                    isPassed=True
                ).exists()
                if not passed_grade:
                    return JsonResponse({
                        'error': f'Chưa đáp ứng môn tiên quyết: {prereq.subjectName} ({prereq.subjectCode})',
                        'missingPrerequisite': {
                            'subjectCode': prereq.subjectCode,
                            'subjectName': prereq.subjectName
                        }
                    }, status=400)
        
        # Kiểm tra schedule conflict với các môn đã đăng ký
        current_registrations = CourseRegistration.objects.filter(
            student=student,
            semester=semester,
            status='registered'
        ).select_related('courseClass')
        
        conflicts = []
        for reg in current_registrations:
            registered_class = reg.courseClass
            
            # Kiểm tra conflict bằng cách so sánh schedule DateTimeField
            if course_class.schedule and registered_class.schedule:
                # So sánh datetime - nếu cùng ngày giờ thì conflict
                if course_class.schedule == registered_class.schedule:
                    conflicts.append({
                        'courseCode': registered_class.courseCode,
                        'courseName': registered_class.courseName,
                        'schedule': str(registered_class.schedule),
                        'reason': 'Cùng lịch học (schedule)'
                    })
            
            # Nếu không có schedule, kiểm tra conflict dựa trên phòng học
            # Nếu cùng phòng, có thể cùng thời gian -> conflict
            elif course_class.room and registered_class.room:
                if course_class.room == registered_class.room:
                    # Cảnh báo nếu cùng phòng (có thể conflict)
                    # Nhưng chỉ chặn nếu có thông tin schedule hoặc có rule rõ ràng
                    # Tạm thời chỉ cảnh báo, không chặn nếu không có schedule
                    pass
        
        if conflicts:
            conflict_details = ', '.join([f"{c['courseCode']}" for c in conflicts])
            return JsonResponse({
                'error': f'Xung đột lịch học với môn đã đăng ký: {conflict_details}',
                'conflicts': conflicts
            }, status=400)
        
        # Kiểm tra registration period
        if semester.registrationStart and semester.registrationEnd:
            now = timezone.now()
            if not (semester.registrationStart <= now <= semester.registrationEnd):
                return JsonResponse({
                    'error': 'Không trong thời gian đăng ký',
                    'registrationStart': semester.registrationStart.isoformat() if semester.registrationStart else None,
                    'registrationEnd': semester.registrationEnd.isoformat() if semester.registrationEnd else None
                }, status=400)
        
        # Auto-generate registrationId nếu không có
        registration_id = data.get('registrationId')
        if not registration_id:
            base_prefix = 'REG'
            next_num = CourseRegistration.objects.count() + 1
            while True:
                candidate_id = f"{base_prefix}{next_num:06d}"
                if not CourseRegistration.objects.filter(registrationId=candidate_id).exists():
                    registration_id = candidate_id
                    break
                next_num += 1
        
        # Tạo registration
        registration = CourseRegistration.objects.create(
            registrationId=registration_id,
            student=student,
            courseClass=course_class,
            semester=semester,
            registrationDate=timezone.now().date(),
            status='registered'
        )
        
        # Update currentStudents count
        course_class.currentStudents += 1
        course_class.save()
        
        return JsonResponse({
            'message': 'Course registered successfully',
            'registrationId': registration.registrationId,
            'status': registration.status
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        import traceback
        traceback.print_exc()
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
def calculate_grade_from_score(average_score):
    """
    Tính letterGrade và gradePoint từ average_score (thang điểm 10)
    Quy tắc:
    - 9.0-10.0: A (4.0)
    - 8.5-8.9: B+ (3.5)
    - 8.0-8.4: B (3.0)
    - 7.5-7.9: C+ (2.5)
    - 7.0-7.4: C (2.0)
    - 6.5-6.9: D+ (1.5)
    - 6.0-6.4: D (1.0)
    - < 6.0: F (0.0)
    """
    if average_score is None:
        return None, None, None
    
    score = float(average_score)
    
    if score >= 9.0:
        return 'A', 4.0, True
    elif score >= 8.5:
        return 'B+', 3.5, True
    elif score >= 8.0:
        return 'B', 3.0, True
    elif score >= 7.5:
        return 'C+', 2.5, True
    elif score >= 7.0:
        return 'C', 2.0, True
    elif score >= 6.5:
        return 'D+', 1.5, True
    elif score >= 6.0:
        return 'D', 1.0, True
    else:
        return 'F', 0.0, False

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
        
        # Tính letterGrade và gradePoint từ average_score nếu có
        average_score = data.get('averageScore')
        letter_grade = data.get('letterGrade')
        grade_point = data.get('gradePoint')
        is_passed = data.get('isPassed')
        
        # Nếu có average_score và chưa có letterGrade/gradePoint, tự động tính
        if average_score is not None:
            calculated_letter, calculated_point, calculated_passed = calculate_grade_from_score(average_score)
            if calculated_letter:
                # Ưu tiên dùng giá trị đã tính từ average_score
                letter_grade = calculated_letter
                grade_point = calculated_point
                is_passed = calculated_passed
        
        # Validate required fields
        if not letter_grade or grade_point is None or is_passed is None:
            return JsonResponse({'error': 'letterGrade, gradePoint, and isPassed are required'}, status=400)
        
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
            average_score=average_score,
            letterGrade=letter_grade,
            gradePoint=grade_point,
            isPassed=is_passed
        )
        return JsonResponse({'message': 'Grade created', 'id': grade.gradeId})
    except Exception as e:
        import traceback
        traceback.print_exc()
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

        # Resolve student: students can ONLY create for themselves; admin/teacher may specify studentId
        student_obj = None
        student_id = data.get('studentId')
        if getattr(request.user, 'user_type', None) == 'student':
            # If student tries to submit for another student, reject
            try:
                self_student = Student.objects.get(user=request.user)
            except Student.DoesNotExist:
                return JsonResponse({'error': 'Student profile not found'}, status=404)
            if student_id and student_id != self_student.studentId:
                return JsonResponse({'error': 'Students cannot create requests for other students'}, status=403)
            student_obj = self_student
        else:
            # Admin/teacher must specify target studentId
            if not student_id:
                return JsonResponse({'error': 'studentId is required for this operation'}, status=400)
            student_obj = Student.objects.get(studentId=student_id)

        document_type = DocumentType.objects.get(documentTypeId=data['documentTypeId'])
        
        # Tự động lấy học kỳ active nếu không có semesterId
        semester_id = data.get('semesterId')
        if semester_id:
            semester = Semester.objects.get(semesterId=semester_id)
        else:
            semester = Semester.objects.filter(status='active').first()
            if not semester:
                return JsonResponse({'error': 'No active semester found'}, status=400)

        # Nếu đã có yêu cầu tương tự (đang chờ/đã duyệt/đã hoàn tất), trả về bản ghi hiện có
        existing = DocumentRequest.objects.filter(
            student=student_obj,
            documentType=document_type,
            semester=semester,
            status__in=['pending', 'approved', 'completed']
        ).order_by('-requestDate').first()
        if existing:
            return JsonResponse({
                'message': 'already_requested',
                'id': existing.requestId,
                'status': existing.status
            }, status=200)

        # Generate requestId if not provided
        request_id = data.get('requestId')
        if not request_id:
            base_prefix = 'DR'
            next_num = DocumentRequest.objects.count() + 1
            while True:
                candidate_id = f"{base_prefix}{next_num:06d}"
                if not DocumentRequest.objects.filter(requestId=candidate_id).exists():
                    request_id = candidate_id
                    break
                next_num += 1

        doc_request = DocumentRequest.objects.create(
            requestId=request_id,
            student=student_obj,
            documentType=document_type,
            semester=semester,
            requestDate=datetime.now(),
            purpose=data['purpose']
        )

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
    """Xem loại tài liệu có thể yêu cầu - chỉ trả về các loại đang active"""
    try:
        # Chỉ lấy các loại tài liệu đang active
        document_types = DocumentType.objects.filter(status='active')
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
