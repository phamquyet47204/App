from django.test import TestCase, Client
from django.urls import reverse
from .models import User, PasswordResetToken
from .authentication import AuthenticationService
from .permissions import RolePermission
import json

class AuthenticationTestCase(TestCase):
    def setUp(self):
        """Thiết lập dữ liệu test"""
        self.client = Client()
        
        # Tạo user test
        self.admin_user = User.objects.create_user(
            username='admin_test',
            password='admin123',
            email='admin@test.com',
            full_name='Admin Test',
            user_type='admin',
            status='active'
        )
        
        self.teacher_user = User.objects.create_user(
            username='teacher_test',
            password='teacher123',
            email='teacher@test.com',
            full_name='Teacher Test',
            user_type='teacher',
            status='active'
        )
        
        self.student_user = User.objects.create_user(
            username='student_test',
            password='student123',
            email='student@test.com',
            full_name='Student Test',
            user_type='student',
            status='active'
        )

    def test_login_success(self):
        """Test đăng nhập thành công"""
        response = self.client.post(
            reverse('core:login'),
            data=json.dumps({
                'username': 'admin_test',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('session_key', data)
        self.assertEqual(data['user']['username'], 'admin_test')

    def test_login_invalid_credentials(self):
        """Test đăng nhập với thông tin sai"""
        response = self.client.post(
            reverse('core:login'),
            data=json.dumps({
                'username': 'admin_test',
                'password': 'wrong_password'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)

    def test_admin_login_success(self):
        """Test admin login thành công"""
        response = self.client.post(
            reverse('core:admin_login'),
            data=json.dumps({
                'username': 'admin_test',
                'password': 'admin123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_admin_login_wrong_user_type(self):
        """Test teacher không thể dùng admin login"""
        response = self.client.post(
            reverse('core:admin_login'),
            data=json.dumps({
                'username': 'teacher_test',
                'password': 'teacher123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_teacher_login_success(self):
        """Test teacher login thành công"""
        response = self.client.post(
            reverse('core:teacher_login'),
            data=json.dumps({
                'username': 'teacher_test',
                'password': 'teacher123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_student_login_success(self):
        """Test student login thành công"""
        response = self.client.post(
            reverse('core:student_login'),
            data=json.dumps({
                'username': 'student_test',
                'password': 'student123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test đăng xuất"""
        self.client.login(username='admin_test', password='admin123')
        response = self.client.post(reverse('core:logout'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_success(self):
        """Test đổi mật khẩu thành công"""
        self.client.login(username='admin_test', password='admin123')
        response = self.client.post(
            reverse('core:change_password'),
            data=json.dumps({
                'old_password': 'admin123',
                'new_password': 'newpassword123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_change_password_wrong_old_password(self):
        """Test đổi mật khẩu với mật khẩu cũ sai"""
        self.client.login(username='admin_test', password='admin123')
        response = self.client.post(
            reverse('core:change_password'),
            data=json.dumps({
                'old_password': 'wrong_password',
                'new_password': 'newpassword123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_request_password_reset(self):
        """Test yêu cầu đặt lại mật khẩu"""
        response = self.client.post(
            reverse('core:request_reset'),
            data=json.dumps({'email': 'admin@test.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('token', data)

    def test_reset_password_with_valid_token(self):
        """Test đặt lại mật khẩu với token hợp lệ"""
        token = PasswordResetToken.create_token(self.admin_user)
        response = self.client.post(
            reverse('core:reset_password'),
            data=json.dumps({
                'token': token.token,
                'new_password': 'newpassword123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_reset_password_with_invalid_token(self):
        """Test đặt lại mật khẩu với token không hợp lệ"""
        response = self.client.post(
            reverse('core:reset_password'),
            data=json.dumps({
                'token': 'invalid_token',
                'new_password': 'newpassword123'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_check_session_authenticated(self):
        """Test kiểm tra phiên khi đã đăng nhập"""
        self.client.login(username='admin_test', password='admin123')
        response = self.client.get(reverse('core:check_session'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['authenticated'])

    def test_check_session_unauthenticated(self):
        """Test kiểm tra phiên khi chưa đăng nhập"""
        response = self.client.get(reverse('core:check_session'))
        self.assertEqual(response.status_code, 401)  # Middleware returns 401

class RolePermissionTestCase(TestCase):
    def setUp(self):
        """Thiết lập dữ liệu test"""
        self.client = Client()
        
        self.admin_user = User.objects.create_user(
            username='admin_test',
            password='admin123',
            user_type='admin',
            status='active'
        )
        
        self.teacher_user = User.objects.create_user(
            username='teacher_test',
            password='teacher123',
            user_type='teacher',
            status='active'
        )
        
        self.student_user = User.objects.create_user(
            username='student_test',
            password='student123',
            user_type='student',
            status='active'
        )

    def test_admin_access_admin_dashboard(self):
        """Test admin truy cập dashboard admin"""
        self.client.login(username='admin_test', password='admin123')
        response = self.client.get(reverse('core:admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_access_admin_dashboard(self):
        """Test teacher không thể truy cập dashboard admin"""
        self.client.login(username='teacher_test', password='teacher123')
        response = self.client.get(reverse('core:admin_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_student_access_student_dashboard(self):
        """Test student truy cập dashboard student"""
        self.client.login(username='student_test', password='student123')
        response = self.client.get(reverse('core:student_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_has_manage_users_permission(self):
        """Test admin có quyền manage_users"""
        has_perm = RolePermission.has_permission(self.admin_user, 'manage_users')
        self.assertTrue(has_perm)

    def test_student_no_manage_users_permission(self):
        """Test student không có quyền manage_users"""
        has_perm = RolePermission.has_permission(self.student_user, 'manage_users')
        self.assertFalse(has_perm)

    def test_teacher_has_input_grades_permission(self):
        """Test teacher có quyền input_grades"""
        has_perm = RolePermission.has_permission(self.teacher_user, 'input_grades')
        self.assertTrue(has_perm)

    def test_inactive_user_no_permission(self):
        """Test user inactive không có quyền"""
        self.admin_user.status = 'inactive'
        self.admin_user.save()
        has_perm = RolePermission.has_permission(self.admin_user, 'manage_users')
        self.assertFalse(has_perm)

class SessionManagementTestCase(TestCase):
    def setUp(self):
        """Thiết lập dữ liệu test"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            password='test123',
            status='active'
        )

    def test_session_creation(self):
        """Test tạo phiên đăng nhập"""
        self.client.login(username='test_user', password='test123')
        self.assertIn('_auth_user_id', self.client.session)

    def test_session_validation(self):
        """Test xác thực phiên"""
        self.client.login(username='test_user', password='test123')
        session_key = self.client.session.session_key
        is_valid = AuthenticationService.validate_session(session_key)
        self.assertTrue(is_valid)

    def test_session_expiry(self):
        """Test phiên hết hạn"""
        self.client.login(username='test_user', password='test123')
        # Session được set expiry 3600 giây trong AuthenticationService
        self.assertIsNotNone(self.client.session.get_expiry_age())
