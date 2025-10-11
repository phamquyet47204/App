# -*- coding: utf-8 -*-
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from django.test import Client
from core.models import User
import json

def test_decorator_vs_middleware():
    print("\n" + "="*70)
    print("  TEST: MIDDLEWARE vs DECORATORS")
    print("="*70 + "\n")
    
    client = Client()
    User.objects.filter(username__in=['admin1', 'teacher1', 'student1']).delete()
    
    # Tao users
    admin = User.objects.create_user(
        username='admin1',
        password='pass123',
        user_type='admin',
        status='active'
    )
    
    teacher = User.objects.create_user(
        username='teacher1',
        password='pass123',
        user_type='teacher',
        status='active'
    )
    
    student = User.objects.create_user(
        username='student1',
        password='pass123',
        user_type='student',
        status='active'
    )
    
    print("="*70)
    print("MIDDLEWARE: Kiem tra ROLE theo PATH")
    print("="*70)
    
    # Admin truy cap /api/admin/*
    client.login(username='admin1', password='pass123')
    response = client.get('/api/admin/dashboard/')
    print(f"1. Admin -> /api/admin/dashboard/")
    print(f"   Middleware kiem tra path '/api/admin/*' -> role 'admin'")
    print(f"   Result: {response.status_code} [{'PASS' if response.status_code == 200 else 'FAIL'}]\n")
    
    # Teacher truy cap /api/admin/* (FAIL)
    client.logout()
    client.login(username='teacher1', password='pass123')
    response = client.get('/api/admin/dashboard/')
    print(f"2. Teacher -> /api/admin/dashboard/")
    print(f"   Middleware kiem tra path '/api/admin/*' -> role 'admin'")
    print(f"   Teacher khong phai admin -> BI CHAN")
    print(f"   Result: {response.status_code} [{'PASS' if response.status_code == 403 else 'FAIL'}]\n")
    
    print("="*70)
    print("DECORATORS: Kiem tra PERMISSION cu the")
    print("="*70)
    
    # Admin co permission 'manage_users'
    client.logout()
    client.login(username='admin1', password='pass123')
    response = client.get('/api/admin/manage-users/')
    print(f"3. Admin -> /api/admin/manage-users/")
    print(f"   Middleware: PASS (path /api/admin/* + role admin)")
    print(f"   Decorator: Kiem tra permission 'manage_users'")
    print(f"   Admin co permission 'manage_users' -> PASS")
    print(f"   Result: {response.status_code} [{'PASS' if response.status_code == 200 else 'FAIL'}]\n")
    
    # Teacher khong co permission 'manage_users'
    client.logout()
    client.login(username='teacher1', password='pass123')
    response = client.get('/api/admin/manage-users/')
    print(f"4. Teacher -> /api/admin/manage-users/")
    print(f"   Middleware: FAIL (path /api/admin/* nhung role teacher)")
    print(f"   Decorator: Khong chay vi middleware da chan")
    print(f"   Result: {response.status_code} [{'PASS' if response.status_code == 403 else 'FAIL'}]\n")
    
    # Teacher co permission 'input_grades'
    response = client.post('/api/teacher/input-grades/')
    print(f"5. Teacher -> /api/teacher/input-grades/")
    print(f"   Middleware: PASS (path /api/teacher/* + role teacher)")
    print(f"   Decorator: Kiem tra permission 'input_grades'")
    print(f"   Teacher co permission 'input_grades' -> PASS")
    print(f"   Result: {response.status_code} [{'PASS' if response.status_code == 200 else 'FAIL'}]\n")
    
    # Student khong co permission 'input_grades'
    client.logout()
    client.login(username='student1', password='pass123')
    response = client.post('/api/teacher/input-grades/')
    print(f"6. Student -> /api/teacher/input-grades/")
    print(f"   Middleware: FAIL (path /api/teacher/* nhung role student)")
    print(f"   Decorator: Khong chay vi middleware da chan")
    print(f"   Result: {response.status_code} [{'PASS' if response.status_code == 403 else 'FAIL'}]\n")
    
    # Student co permission 'view_grades'
    response = client.get('/api/student/my-grades/')
    print(f"7. Student -> /api/student/my-grades/")
    print(f"   Middleware: PASS (path /api/student/* + role student)")
    print(f"   Decorator: Kiem tra permission 'view_grades'")
    print(f"   Student co permission 'view_grades' -> PASS")
    print(f"   Result: {response.status_code} [{'PASS' if response.status_code == 200 else 'FAIL'}]\n")
    
    print("="*70)
    print("KET LUAN")
    print("="*70)
    print("""
MIDDLEWARE:
- Kiem tra CHUNG cho tat ca requests theo PATH PATTERN
- Vi du: /api/admin/* -> chi admin moi vao duoc
- Chay TRUOC, chan som neu sai role

DECORATORS:
- Kiem tra CHI TIET cho TUNG view theo PERMISSION
- Vi du: @require_permission('manage_users')
- Chay SAU middleware, kiem tra quyen cu the

=> KET HOP CA HAI:
   1. Middleware: Loc theo role (admin/teacher/student)
   2. Decorator: Kiem tra permission cu the trong role do
    """)

if __name__ == '__main__':
    test_decorator_vs_middleware()
