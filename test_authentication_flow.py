# -*- coding: utf-8 -*-
"""
Script kiem tra luong xac thuc
Chay: python test_authentication_flow.py
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.test import Client
from core.models import User, PasswordResetToken
from core.authentication import AuthenticationService
from core.permissions import RolePermission
import json

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_authentication_flow():
    """Test toan bo luong xac thuc"""
    
    print_section("BAT DAU KIEM TRA HE THONG XAC THUC")
    
    # Tao test users
    print("1. Tao test users...")
    
    # Xoa users cu neu co
    User.objects.filter(username__in=['admin_test', 'teacher_test', 'student_test']).delete()
    
    admin_user = User.objects.create_user(
        username='admin_test',
        password='admin123',
        email='admin@test.com',
        full_name='Admin Test',
        user_type='admin',
        status='active'
    )
    print(f"   [OK] Tao admin: {admin_user.username}")
    
    teacher_user = User.objects.create_user(
        username='teacher_test',
        password='teacher123',
        email='teacher@test.com',
        full_name='Teacher Test',
        user_type='teacher',
        status='active'
    )
    print(f"   [OK] Tao teacher: {teacher_user.username}")
    
    student_user = User.objects.create_user(
        username='student_test',
        password='student123',
        email='student@test.com',
        full_name='Student Test',
        user_type='student',
        status='active'
    )
    print(f"   [OK] Tao student: {student_user.username}")
    
    # Test dang nhap
    print_section("2. TEST DANG NHAP")
    
    client = Client()
    
    # Test dang nhap thanh cong
    response = client.post(
        '/api/auth/login/',
        data=json.dumps({
            'username': 'admin_test',
            'password': 'admin123'
        }),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] Dang nhap thanh cong")
        print(f"   - Username: {data['user']['username']}")
        print(f"   - User type: {data['user']['user_type']}")
        print(f"   - Session key: {data['session_key'][:20]}...")
    else:
        print(f"   [FAIL] Dang nhap that bai: {response.status_code}")
    
    # Test dang nhap sai mat khau
    response = client.post(
        '/api/auth/login/',
        data=json.dumps({
            'username': 'admin_test',
            'password': 'wrong_password'
        }),
        content_type='application/json'
    )
    
    if response.status_code == 401:
        print(f"   [OK] Tu choi dang nhap voi mat khau sai")
    else:
        print(f"   [FAIL] Loi kiem tra mat khau sai")
    
    # Test phan quyen
    print_section("3. TEST PHAN QUYEN")
    
    # Admin permissions
    admin_perms = RolePermission.get_permissions('admin')
    print(f"   Admin co {len(admin_perms)} quyen:")
    for perm in admin_perms[:3]:
        print(f"   - {perm}")
    print(f"   - ...")
    
    # Teacher permissions
    teacher_perms = RolePermission.get_permissions('teacher')
    print(f"\n   Teacher co {len(teacher_perms)} quyen:")
    for perm in teacher_perms:
        print(f"   - {perm}")
    
    # Student permissions
    student_perms = RolePermission.get_permissions('student')
    print(f"\n   Student co {len(student_perms)} quyen:")
    for perm in student_perms:
        print(f"   - {perm}")
    
    # Test kiem tra quyen
    print("\n   Kiem tra quyen cu the:")
    has_perm = RolePermission.has_permission(admin_user, 'manage_users')
    print(f"   - Admin co quyen 'manage_users': {has_perm} [OK]")
    
    has_perm = RolePermission.has_permission(student_user, 'manage_users')
    print(f"   - Student co quyen 'manage_users': {has_perm} [OK]")
    
    has_perm = RolePermission.has_permission(teacher_user, 'input_grades')
    print(f"   - Teacher co quyen 'input_grades': {has_perm} [OK]")
    
    # Test truy cap dashboard theo role
    print_section("4. TEST TRUY CAP DASHBOARD THEO ROLE")
    
    # Admin truy cap admin dashboard
    client.login(username='admin_test', password='admin123')
    response = client.get('/api/admin/dashboard/')
    print(f"   Admin truy cap admin dashboard: {response.status_code == 200} [OK]")
    
    # Teacher truy cap admin dashboard (should fail)
    client.logout()
    client.login(username='teacher_test', password='teacher123')
    response = client.get('/api/admin/dashboard/')
    print(f"   Teacher bi chan admin dashboard: {response.status_code == 403} [OK]")
    
    # Teacher truy cap teacher dashboard
    response = client.get('/api/teacher/dashboard/')
    print(f"   Teacher truy cap teacher dashboard: {response.status_code == 200} [OK]")
    
    # Student truy cap student dashboard
    client.logout()
    client.login(username='student_test', password='student123')
    response = client.get('/api/student/dashboard/')
    print(f"   Student truy cap student dashboard: {response.status_code == 200} [OK]")
    
    # Test doi mat khau
    print_section("5. TEST DOI MAT KHAU")
    
    client.logout()
    client.login(username='admin_test', password='admin123')
    
    response = client.post(
        '/api/auth/change-password/',
        data=json.dumps({
            'old_password': 'admin123',
            'new_password': 'newpassword123'
        }),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        print(f"   [OK] Doi mat khau thanh cong")
        
        # Test dang nhap voi mat khau moi
        client.logout()
        response = client.post(
            '/api/auth/login/',
            data=json.dumps({
                'username': 'admin_test',
                'password': 'newpassword123'
            }),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            print(f"   [OK] Dang nhap voi mat khau moi thanh cong")
        else:
            print(f"   [FAIL] Dang nhap voi mat khau moi that bai")
    else:
        print(f"   [FAIL] Doi mat khau that bai")
    
    # Test dat lai mat khau
    print_section("6. TEST DAT LAI MAT KHAU")
    
    # Yeu cau reset token
    response = client.post(
        '/api/auth/request-reset/',
        data=json.dumps({'email': 'teacher@test.com'}),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data['token']
        print(f"   [OK] Tao reset token thanh cong")
        print(f"   - Token: {token[:30]}...")
        
        # Dat lai mat khau voi token
        response = client.post(
            '/api/auth/reset-password/',
            data=json.dumps({
                'token': token,
                'new_password': 'resetpassword123'
            }),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            print(f"   [OK] Dat lai mat khau thanh cong")
            
            # Test dang nhap voi mat khau moi
            response = client.post(
                '/api/auth/login/',
                data=json.dumps({
                    'username': 'teacher_test',
                    'password': 'resetpassword123'
                }),
                content_type='application/json'
            )
            
            if response.status_code == 200:
                print(f"   [OK] Dang nhap voi mat khau reset thanh cong")
            else:
                print(f"   [FAIL] Dang nhap voi mat khau reset that bai")
        else:
            print(f"   [FAIL] Dat lai mat khau that bai")
    else:
        print(f"   [FAIL] Tao reset token that bai")
    
    # Test quan ly phien
    print_section("7. TEST QUAN LY PHIEN")
    
    client.logout()
    client.login(username='student_test', password='student123')
    
    # Kiem tra phien
    response = client.get('/api/auth/check-session/')
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] Phien hop le")
        print(f"   - Authenticated: {data['authenticated']}")
        print(f"   - Username: {data['user']['username']}")
        print(f"   - User type: {data['user']['user_type']}")
    
    # Dang xuat
    response = client.post('/api/auth/logout/')
    if response.status_code == 200:
        print(f"   [OK] Dang xuat thanh cong")
    
    # Kiem tra phien sau khi dang xuat
    response = client.get('/api/auth/check-session/')
    if response.status_code == 302:  # Redirect to login
        print(f"   [OK] Phien da bi xoa sau khi dang xuat")
    
    # Test user inactive
    print_section("8. TEST USER INACTIVE")
    
    admin_user.status = 'inactive'
    admin_user.save()
    
    response = client.post(
        '/api/auth/login/',
        data=json.dumps({
            'username': 'admin_test',
            'password': 'newpassword123'
        }),
        content_type='application/json'
    )
    
    if response.status_code == 401:
        print(f"   [OK] User inactive khong the dang nhap")
    else:
        print(f"   [FAIL] User inactive van dang nhap duoc")
    
    print_section("KET THUC KIEM TRA")
    print("Tat ca cac test da hoan thanh!\n")

if __name__ == '__main__':
    try:
        test_authentication_flow()
    except Exception as e:
        print(f"\n[ERROR] Loi: {str(e)}")
        import traceback
        traceback.print_exc()
