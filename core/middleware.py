from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sessions.models import Session
from django.utils import timezone

class AuthenticationMiddleware(MiddlewareMixin):
    """Middleware kiem tra xac thuc va phien"""
    
    EXEMPT_PATHS = [
        '/api/auth/login/',
        '/api/auth/logout/',
        '/api/auth/request-reset/',
        '/api/auth/reset-password/',
        '/admin/',
        '/static/',
    ]
    
    def process_request(self, request):
        # Bo qua cac duong dan khong can xac thuc
        if any(request.path.startswith(path) for path in self.EXEMPT_PATHS):
            return None
        
        # Kiem tra user da dang nhap
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Kiem tra trang thai user
        if hasattr(request.user, 'status') and request.user.status != 'active':
            return JsonResponse({'error': 'Account inactive'}, status=403)
        
        return None

class SessionValidationMiddleware(MiddlewareMixin):
    """Middleware xac thuc phien"""
    
    def process_request(self, request):
        if request.user.is_authenticated:
            session_key = request.session.session_key
            if session_key:
                try:
                    session = Session.objects.get(session_key=session_key)
                    if session.expire_date <= timezone.now():
                        request.session.flush()
                        return JsonResponse({'error': 'Session expired'}, status=401)
                except Session.DoesNotExist:
                    return JsonResponse({'error': 'Invalid session'}, status=401)
        return None

class RolePermissionMiddleware(MiddlewareMixin):
    """Middleware kiem tra phan quyen theo vai tro - CHI KIEM TRA PATH"""
    
    ROLE_PATHS = {
        'admin': ['/api/admin/'],
        'teacher': ['/api/teacher/'],
        'student': ['/api/student/'],
    }
    
    def process_request(self, request):
        if not request.user.is_authenticated:
            return None
        
        user_type = getattr(request.user, 'user_type', None)
        
        for role, paths in self.ROLE_PATHS.items():
            for path in paths:
                if request.path.startswith(path):
                    if user_type != role:
                        return JsonResponse({'error': f'Access denied. {role.title()} role required'}, status=403)
        
        return None
