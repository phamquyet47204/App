from django.urls import path
from . import crud_views

app_name = 'crud'

urlpatterns = [
    # Department CRUD
    path('departments/', crud_views.list_departments, name='list_departments'),
    path('departments/create/', crud_views.create_department, name='create_department'),
    path('departments/<str:dept_id>/', crud_views.get_department, name='get_department'),
    path('departments/<str:dept_id>/update/', crud_views.update_department, name='update_department'),
    path('departments/<str:dept_id>/delete/', crud_views.delete_department, name='delete_department'),
    
    # Major CRUD
    path('majors/', crud_views.list_majors, name='list_majors'),
    path('majors/create/', crud_views.create_major, name='create_major'),
    path('majors/<str:major_id>/', crud_views.get_major, name='get_major'),
    path('majors/<str:major_id>/update/', crud_views.update_major, name='update_major'),
    path('majors/<str:major_id>/delete/', crud_views.delete_major, name='delete_major'),
    
    # Subject CRUD
    path('subjects/', crud_views.list_subjects, name='list_subjects'),
    path('subjects/create/', crud_views.create_subject, name='create_subject'),
    path('subjects/<str:subject_id>/', crud_views.get_subject, name='get_subject'),
    path('subjects/<str:subject_id>/update/', crud_views.update_subject, name='update_subject'),
    path('subjects/<str:subject_id>/delete/', crud_views.delete_subject, name='delete_subject'),
    
    # Student Class CRUD
    path('student-classes/', crud_views.list_student_classes, name='list_student_classes'),
    path('student-classes/create/', crud_views.create_student_class, name='create_student_class'),
    
    # Academic Year CRUD
    path('academic-years/', crud_views.list_academic_years, name='list_academic_years'),
    path('academic-years/create/', crud_views.create_academic_year, name='create_academic_year'),
    
    # Semester CRUD
    path('semesters/', crud_views.list_semesters, name='list_semesters'),
    path('semesters/create/', crud_views.create_semester, name='create_semester'),
    
    # Course Class CRUD
    path('course-classes/', crud_views.list_course_classes, name='list_course_classes'),
    path('course-classes/create/', crud_views.create_course_class, name='create_course_class'),
    path('course-classes/<str:class_id>/update/', crud_views.update_course_class, name='update_course_class'),
    path('course-classes/<str:class_id>/delete/', crud_views.delete_course_class, name='delete_course_class'),
    
    # Course Registration CRUD
    path('registrations/', crud_views.list_registrations, name='list_registrations'),
    path('registrations/create/', crud_views.register_course, name='register_course'),
    
    # Grade CRUD
    path('grades/', crud_views.list_grades, name='list_grades'),
    path('grades/create/', crud_views.create_grade, name='create_grade'),
    
    # Tuition Fee CRUD
    path('tuition-fees/', crud_views.list_tuition_fees, name='list_tuition_fees'),
    path('tuition-fees/create/', crud_views.create_tuition_fee, name='create_tuition_fee'),
    
    # Document Request CRUD
    path('document-requests/', crud_views.list_document_requests, name='list_document_requests'),
    path('document-requests/create/', crud_views.create_document_request, name='create_document_request'),
    
    # Document Type CRUD
    path('document-types/', crud_views.list_document_types, name='list_document_types'),
    
    # Notification CRUD
    path('notifications/', crud_views.list_notifications, name='list_notifications'),
    path('notifications/create/', crud_views.create_notification, name='create_notification'),
    path('notifications/<str:notification_id>/delete/', crud_views.delete_notification, name='delete_notification'),
    
    # User CRUD (Students/Teachers)
    path('users/', crud_views.list_users, name='list_users'),
    path('users/create/', crud_views.create_user, name='create_user'),
    path('users/<str:user_id>/', crud_views.get_user, name='get_user'),
    path('users/<str:user_id>/update/', crud_views.update_user, name='update_user'),
    path('users/<str:user_id>/delete/', crud_views.delete_user, name='delete_user'),
    
    # Teacher List
    path('teachers/', crud_views.list_teachers, name='list_teachers'),
]