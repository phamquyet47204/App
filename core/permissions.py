from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class RolePermission:
    """Quản lý quyền dựa trên vai trò"""
    
    ADMIN_PERMISSIONS = [
        'manage_users',
        'manage_departments',
        'manage_subjects',
        'generate_reports',
        'backup_system',
        'configure_system',
        'approve_documents',
        'manage_tuition'
    ]
    
    TEACHER_PERMISSIONS = [
        'view_assigned_classes',
        'input_grades',
        'export_grades',
        'take_attendance',
        'view_students'
    ]
    
    STUDENT_PERMISSIONS = [
        'view_grades',
        'register_course',
        'drop_course',
        'view_schedule',
        'request_document',
        'view_tuition'
    ]

    @staticmethod
    def get_permissions(user_type):
        """Lấy danh sách quyền theo vai trò"""
        permissions_map = {
            'admin': RolePermission.ADMIN_PERMISSIONS,
            'teacher': RolePermission.TEACHER_PERMISSIONS,
            'student': RolePermission.STUDENT_PERMISSIONS
        }
        return permissions_map.get(user_type, [])

    @staticmethod
    def has_permission(user, permission):
        """Kiểm tra người dùng có quyền không"""
        if not user.is_authenticated or user.status != 'active':
            return False
        user_permissions = RolePermission.get_permissions(user.user_type)
        return permission in user_permissions

def require_role(*roles):
    """Decorator kiểm tra vai trò"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.user_type not in roles:
                return JsonResponse({'error': 'Permission denied'}, status=403)
            if request.user.status != 'active':
                return JsonResponse({'error': 'Account inactive'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_permission(permission):
    """Decorator kiểm tra quyền cụ thể"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if not RolePermission.has_permission(request.user, permission):
                return JsonResponse({'error': 'Permission denied'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
