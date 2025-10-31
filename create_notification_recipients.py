import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from core.models import *
from datetime import datetime

print("Creating notification recipients...")

# Lấy tất cả notifications và students
notifications = Notification.objects.all()
students = User.objects.filter(user_type='student')

# Tạo NotificationRecipient cho mỗi student với mỗi notification
for notification in notifications:
    for student in students:
        recipient_id = f"NR_{notification.notificationId}_{student.id}"
        recipient, created = NotificationRecipient.objects.get_or_create(
            recipientId=recipient_id,
            defaults={
                'notification': notification,
                'user': student,
                'deliveryStatus': 'delivered',
                'deliveredAt': datetime.now()
            }
        )
        if created:
            print(f"Created recipient: {student.username} -> {notification.title}")

print(f"Total NotificationRecipients: {NotificationRecipient.objects.count()}")