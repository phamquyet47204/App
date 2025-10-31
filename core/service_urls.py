from django.urls import path
from . import service_views

app_name = 'services'

urlpatterns = [
    # Grade Service
    path('grades/calculate-gpa/', service_views.calculate_gpa, name='calculate_gpa'),
    path('grades/export-class/<str:class_id>/', service_views.export_class_grades, name='export_class_grades'),
    path('grades/class-statistics/<str:class_id>/', service_views.class_statistics, name='class_statistics'),
    
    # Registration Service
    path('registration/check-prerequisites/', service_views.check_prerequisites, name='check_prerequisites'),
    path('registration/check-schedule-conflict/', service_views.check_schedule_conflict, name='check_schedule_conflict'),
    path('registration/available-courses/<str:student_id>/', service_views.available_courses, name='available_courses'),
    
    # Notification Service
    path('notifications/unread/', service_views.unread_notifications, name='unread_notifications'),
    path('notifications/<str:notification_id>/mark-read/', service_views.mark_notification_read, name='mark_notification_read'),
    
    # Report Service
    path('reports/students/', service_views.student_report, name='student_report'),
    path('reports/grades/', service_views.grade_report, name='grade_report'),
    

]