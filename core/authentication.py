from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from datetime import timedelta

class AuthenticationService:
    @staticmethod
    def authenticate_user(username, password):
        """Xác thực người dùng"""
        user = authenticate(username=username, password=password)
        if user and user.status == 'active':
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            return user
        return None

    @staticmethod
    def create_session(request, user):
        """Tạo phiên đăng nhập"""
        login(request, user)
        request.session.set_expiry(3600)  # 1 giờ
        # Force save session
        if not request.session.session_key:
            request.session.save()
        return request.session.session_key

    @staticmethod
    def validate_session(session_key):
        """Kiểm tra phiên hợp lệ"""
        try:
            session = Session.objects.get(session_key=session_key)
            if session.expire_date > timezone.now():
                return True
        except Session.DoesNotExist:
            pass
        return False

    @staticmethod
    def logout_user(request):
        """Đăng xuất người dùng"""
        logout(request)

    @staticmethod
    def change_password(user, old_password, new_password):
        """Đổi mật khẩu"""
        if check_password(old_password, user.password):
            user.password = make_password(new_password)
            user.save(update_fields=['password'])
            return True
        return False

    @staticmethod
    def reset_password(email):
        """Đặt lại mật khẩu - tạo token"""
        from .models import PasswordResetToken
        try:
            user = User.objects.get(email=email, status='active')
            token = PasswordResetToken.create_token(user)
            return token
        except User.DoesNotExist:
            return None

    @staticmethod
    def verify_reset_token(token):
        """Xác minh token đặt lại mật khẩu"""
        from .models import PasswordResetToken
        return PasswordResetToken.verify_token(token)

    @staticmethod
    def set_new_password(token, new_password):
        """Đặt mật khẩu mới"""
        from .models import PasswordResetToken
        reset_token = PasswordResetToken.verify_token(token)
        if reset_token:
            user = reset_token.user
            user.password = make_password(new_password)
            user.save(update_fields=['password'])
            reset_token.is_used = True
            reset_token.save()
            return True
        return False
