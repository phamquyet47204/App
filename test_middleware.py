# -*- coding: utf-8 -*-
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.test import Client
from core.models import User
import json

def test_middleware():
    print("\n" + "="*60)
    print("  TEST MIDDLEWARE XAC THUC")
    print("="*60 + "\n")
    
    client = Client()
    User.objects.filter(username__in=['test_admin', 'test_teacher', 'test_student']).delete()
    
    # Tao users
    admin = User.objects.create_user(
        username='test_admin',
        password='pass123',
        user_type='admin',
        status='active'
    )
    
    teacher = User.objects.create_user(
        username='test_teacher',
        password='pass123',
        user_type='teacher',
        status='active'
    )
    
    student = User.objects.create_user(
        username='test_student',
        password='pass123',
        user_type='student',
        status='inactive'
    )
    
    print("1. Test AuthenticationMiddleware")
    # Truy cap endpoint can xac thuc khi chua dang nhap
    response = client.get('/api/auth/check-session/')
    print(f"   Chua dang nhap -> check-session: {response.status_code} (401) [{'OK' if response.status_code == 401 else 'FAIL'}]")
    
    # Dang nhap thanh cong
    client.login(username='test_admin', password='pass123')
    response = client.get('/api/auth/check-session/')
    print(f"   Da dang nhap -> check-session: {response.status_code} (200) [{'OK' if response.status_code == 200 else 'FAIL'}]")
    
    print("\n2. Test RolePermissionMiddleware")
    # Admin truy cap admin endpoint
    response = client.get('/api/admin/dashboard/')
    print(f"   Admin -> /api/admin/: {response.status_code} (200) [{'OK' if response.status_code == 200 else 'FAIL'}]")
    
    # Admin truy cap teacher endpoint (bi chan)
    response = client.get('/api/teacher/dashboard/')
    print(f"   Admin -> /api/teacher/: {response.status_code} (403) [{'OK' if response.status_code == 403 else 'FAIL'}]")
    
    # Teacher truy cap teacher endpoint
    client.logout()
    client.login(username='test_teacher', password='pass123')
    response = client.get('/api/teacher/dashboard/')
    print(f"   Teacher -> /api/teacher/: {response.status_code} (200) [{'OK' if response.status_code == 200 else 'FAIL'}]")
    
    # Teacher truy cap admin endpoint (bi chan)
    response = client.get('/api/admin/dashboard/')
    print(f"   Teacher -> /api/admin/: {response.status_code} (403) [{'OK' if response.status_code == 403 else 'FAIL'}]")
    
    print("\n3. Test User Status Check")
    # User inactive khong the truy cap
    client.logout()
    client.login(username='test_student', password='pass123')
    response = client.get('/api/student/dashboard/')
    print(f"   Inactive user -> dashboard: {response.status_code} (403) [{'OK' if response.status_code == 403 else 'FAIL'}]")
    
    print("\n4. Test Exempt Paths")
    # Login endpoint khong can xac thuc
    client.logout()
    response = client.post(
        '/api/auth/login/',
        data=json.dumps({'username': 'test_admin', 'password': 'pass123'}),
        content_type='application/json'
    )
    print(f"   Login endpoint (exempt): {response.status_code} (200) [{'OK' if response.status_code == 200 else 'FAIL'}]")
    
    print("\n" + "="*60)
    print("  HOAN THANH TEST MIDDLEWARE")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_middleware()
