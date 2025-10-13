from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .authentication import AuthenticationService
from .permissions import require_permission

# ============ AUTH ENDPOINTS (Middleware tu dong kiem tra) ============

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """API dang nhap chung"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)
        
        user = AuthenticationService.authenticate_user(username, password)
        if user:
            session_key = AuthenticationService.create_session(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'session_key': session_key,
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'user_type': user.user_type
                }
            })
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def admin_login(request):
    """API dang nhap danh cho Admin"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)
        
        user = AuthenticationService.authenticate_user(username, password)
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        if user.user_type != 'admin':
            return JsonResponse({'error': 'Access denied. Admin only'}, status=403)
        
        session_key = AuthenticationService.create_session(request, user)
        return JsonResponse({
            'message': 'Admin login successful',
            'session_key': session_key,
            'user': {
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'user_type': user.user_type
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def teacher_login(request):
    """API dang nhap danh cho Teacher"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)
        
        user = AuthenticationService.authenticate_user(username, password)
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        if user.user_type != 'teacher':
            return JsonResponse({'error': 'Access denied. Teacher only'}, status=403)
        
        session_key = AuthenticationService.create_session(request, user)
        return JsonResponse({
            'message': 'Teacher login successful',
            'session_key': session_key,
            'user': {
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'user_type': user.user_type
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def student_login(request):
    """API dang nhap danh cho Student"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password required'}, status=400)
        
        user = AuthenticationService.authenticate_user(username, password)
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        if user.user_type != 'student':
            return JsonResponse({'error': 'Access denied. Student only'}, status=403)
        
        session_key = AuthenticationService.create_session(request, user)
        return JsonResponse({
            'message': 'Student login successful',
            'session_key': session_key,
            'user': {
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'user_type': user.user_type
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """API dang xuat"""
    try:
        if request.user.is_authenticated:
            AuthenticationService.logout_user(request)
        return JsonResponse({'message': 'Logout successful'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def change_password_view(request):
    """API doi mat khau - Middleware kiem tra auth"""
    try:
        data = json.loads(request.body)
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return JsonResponse({'error': 'Old and new password required'}, status=400)
        
        success = AuthenticationService.change_password(request.user, old_password, new_password)
        if success:
            return JsonResponse({'message': 'Password changed successfully'})
        return JsonResponse({'error': 'Invalid old password'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def request_password_reset(request):
    """API yeu cau dat lai mat khau"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)
        
        token = AuthenticationService.reset_password(email)
        if token:
            return JsonResponse({
                'message': 'Reset token created',
                'token': token.token
            })
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def reset_password_view(request):
    """API dat lai mat khau voi token"""
    try:
        data = json.loads(request.body)
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return JsonResponse({'error': 'Token and new password required'}, status=400)
        
        success = AuthenticationService.set_new_password(token, new_password)
        if success:
            return JsonResponse({'message': 'Password reset successfully'})
        return JsonResponse({'error': 'Invalid or expired token'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def check_session(request):
    """API kiem tra phien dang nhap - Middleware kiem tra auth"""
    return JsonResponse({
        'authenticated': True,
        'user': {
            'username': request.user.username,
            'user_type': request.user.user_type,
            'status': request.user.status
        }
    })

# ============ ROLE-BASED DASHBOARDS (Middleware kiem tra role theo path) ============

@require_http_methods(["GET"])
def admin_dashboard(request):
    """Dashboard admin - Middleware kiem tra role"""
    return JsonResponse({'message': 'Welcome to admin dashboard'})

@require_http_methods(["GET"])
def teacher_dashboard(request):
    """Dashboard teacher - Middleware kiem tra role"""
    return JsonResponse({'message': 'Welcome to teacher dashboard'})

@require_http_methods(["GET"])
def student_dashboard(request):
    """Dashboard student - Middleware kiem tra role"""
    return JsonResponse({'message': 'Welcome to student dashboard'})

# ============ PERMISSION-BASED ENDPOINTS (Decorator kiem tra permission cu the) ============

@require_permission('manage_users')
@require_http_methods(["GET"])
def manage_users(request):
    """Quan ly users - Decorator kiem tra permission 'manage_users'"""
    from .models import User
    users = User.objects.all().values('username', 'email', 'user_type', 'status')
    return JsonResponse({'users': list(users)})

@require_permission('input_grades')
@require_http_methods(["POST"])
def input_grades(request):
    """Nhap diem - Decorator kiem tra permission 'input_grades'"""
    return JsonResponse({'message': 'Grade input functionality'})

@require_permission('approve_documents')
@require_http_methods(["POST"])
def approve_document(request):
    """Duyet tai lieu - Decorator kiem tra permission 'approve_documents'"""
    return JsonResponse({'message': 'Document approval functionality'})

@require_permission('view_grades')
@require_http_methods(["GET"])
def view_my_grades(request):
    """Xem diem cua minh - Decorator kiem tra permission 'view_grades'"""
    return JsonResponse({'message': 'Student grades view'})
