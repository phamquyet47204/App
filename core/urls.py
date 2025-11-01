from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.login_view, name='login'),
    path('auth/admin/login/', views.admin_login, name='admin_login'),
    path('auth/teacher/login/', views.teacher_login, name='teacher_login'),
    path('auth/student/login/', views.student_login, name='student_login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/change-password/', views.change_password_view, name='change_password'),
    path('auth/request-reset/', views.request_password_reset, name='request_reset'),
    path('auth/reset-password/', views.reset_password_view, name='reset_password'),
    path('auth/check-session/', views.check_session, name='check_session'),
    
    # Role-based dashboards (Middleware kiem tra theo path)
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # Permission-based endpoints (Decorator kiem tra permission cu the)
    path('admin/manage-users/', views.manage_users, name='manage_users'),
    path('admin/approve-document/', views.approve_document, name='approve_document'),
    path('teacher/input-grades/', views.input_grades, name='input_grades'),
    
    # CRUD endpoints
    path('crud/', include('core.crud_urls')),
    
    # Service endpoints
    path('services/', include('core.service_urls')),
    
    # Student endpoints
    path('student/', include('core.student_urls')),
]
