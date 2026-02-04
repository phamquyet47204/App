import jwt
import os
from datetime import datetime, timedelta
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Student

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None

        try:
            payload = jwt.decode(
                token,
                os.getenv('SECRET_KEY', 'django-insecure-your-secret-key'),
                algorithms=['HS256']
            )
            student_id = payload.get('student_id')
            
            try:
                student = Student.objects.get(id=student_id)
            except Student.DoesNotExist:
                raise AuthenticationFailed('Người dùng không tồn tại')

            return (student, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token đã hết hạn')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token không hợp lệ')

class JWTGenerator:
    @staticmethod
    def generate_token(student):
        payload = {
            'student_id': student.id,
            'mssv': student.mssv,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(
            payload,
            os.getenv('SECRET_KEY', 'django-insecure-your-secret-key'),
            algorithm='HS256'
        )
        return token
