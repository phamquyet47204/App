from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_registration_confirmation(student, course):
        """Gửi email xác nhận đăng ký môn học"""
        try:
            subject = f"Xác nhận đăng ký môn học - {course.code}"
            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Xác nhận đăng ký môn học</h2>
                    <p>Xin chào <strong>{student.full_name}</strong>,</p>
                    <p>Bạn đã đăng ký thành công môn học:</p>
                    <div style="background-color: #f0f0f0; padding: 15px; margin: 20px 0;">
                        <p><strong>Mã môn học:</strong> {course.code}</p>
                        <p><strong>Tên môn học:</strong> {course.name}</p>
                        <p><strong>Số tín chỉ:</strong> {course.credits}</p>
                        <p><strong>Giáo viên:</strong> {course.lecturer}</p>
                        <p><strong>Lịch học:</strong> {course.schedule}</p>
                    </div>
                    <p>Vui lòng kiểm tra hệ thống để cập nhật các thay đổi.</p>
                    <p>Trân trọng,<br/>Phòng Đào tạo</p>
                </body>
            </html>
            """
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [student.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Email đăng ký gửi thành công cho {student.email}")
        except Exception as e:
            logger.error(f"Lỗi gửi email: {str(e)}")

    @staticmethod
    def send_cancellation_confirmation(student, course):
        """Gửi email xác nhận huỷ đăng ký môn học"""
        try:
            subject = f"Xác nhận huỷ đăng ký môn học - {course.code}"
            html_message = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Xác nhận huỷ đăng ký môn học</h2>
                    <p>Xin chào <strong>{student.full_name}</strong>,</p>
                    <p>Bạn đã huỷ đăng ký thành công môn học:</p>
                    <div style="background-color: #f0f0f0; padding: 15px; margin: 20px 0;">
                        <p><strong>Mã môn học:</strong> {course.code}</p>
                        <p><strong>Tên môn học:</strong> {course.name}</p>
                    </div>
                    <p>Vui lòng kiểm tra hệ thống để cập nhật các thay đổi.</p>
                    <p>Trân trọng,<br/>Phòng Đào tạo</p>
                </body>
            </html>
            """
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [student.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Email huỷ đăng ký gửi thành công cho {student.email}")
        except Exception as e:
            logger.error(f"Lỗi gửi email: {str(e)}")
