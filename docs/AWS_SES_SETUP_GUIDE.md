# Hướng dẫn Cấu hình AWS SES (Simple Email Service)

AWS SES là dịch vụ gửi email có độ tin cậy cao, giá rẻ và dễ tích hợp vào ứng dụng. Đây là lựa chọn tốt nhất cho production trên AWS.

## 📋 Mục lục

1. [Setup AWS SES Console](#1-setup-aws-ses-console)
2. [Verify Email Addresses](#2-verify-email-addresses)
3. [Request Production Access](#3-request-production-access)
4. [Cấu hình Django](#4-cấu-hình-django)
5. [Cấu hình IAM Permissions](#5-cấu-hình-iam-permissions)
6. [Testing](#6-testing)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Setup AWS SES Console

### Bước 1: Mở AWS SES Console

```bash
# Truy cập AWS Console
https://console.aws.amazon.com/ses/

# Hoặc qua AWS CLI
aws ses verify-email-identity --email-address your-email@example.com --region us-east-1
```

### Bước 2: Chọn Region

⚠️ **Quan trọng**: SES không có sẵn ở tất cả regions. Các regions hỗ trợ:
- `us-east-1` (N. Virginia) - **Khuyến nghị**
- `us-west-2` (Oregon)
- `eu-west-1` (Ireland)
- `ap-southeast-1` (Singapore)
- `ap-southeast-2` (Sydney)

---

## 2. Verify Email Addresses

AWS SES yêu cầu verify email trước khi sử dụng.

### Option 1: Verify Single Email (Development/Testing)

**Trong AWS Console:**

1. Vào **SES Console** → **Verified identities**
2. Click **Create identity**
3. Chọn **Email address**
4. Nhập email của bạn: `your-email@example.com`
5. Click **Create identity**
6. Check email và click link xác nhận

**Qua AWS CLI:**

```bash
# Gửi email verify
aws ses verify-email-identity \
    --email-address your-email@example.com \
    --region us-east-1

# Kiểm tra status
aws ses get-identity-verification-attributes \
    --identities your-email@example.com \
    --region us-east-1
```

### Option 2: Verify Domain (Production - Khuyến nghị)

**Ưu điểm**: Có thể gửi từ bất kỳ email nào trong domain

1. Vào **SES Console** → **Verified identities**
2. Click **Create identity**
3. Chọn **Domain**
4. Nhập domain: `example.com`
5. Chọn **Easy DKIM** (khuyến nghị)
6. Click **Create identity**

**Cấu hình DNS Records:**

AWS sẽ cung cấp các DNS records cần thêm vào domain của bạn:

```
Type: CNAME
Name: _amazonses.example.com
Value: [provided-by-aws]

Type: CNAME (DKIM - có 3 records)
Name: xxxx._domainkey.example.com
Value: [provided-by-aws]
```

**Thêm vào DNS provider** (GoDaddy, Namecheap, Route53, etc.)

Đợi 24-48 giờ để DNS propagate và AWS verify.

---

## 3. Request Production Access

Mặc định, AWS SES ở **Sandbox Mode** với giới hạn:
- ✅ Chỉ gửi tới verified emails
- ✅ Giới hạn 200 emails/ngày
- ✅ 1 email/giây

### Để gửi tới bất kỳ email nào, cần request Production Access:

1. Vào **SES Console** → **Account dashboard**
2. Xem "Sending status" (nếu là Sandbox, cần upgrade)
3. Click **Request production access**
4. Điền form:
   - **Mail type**: Transactional
   - **Website URL**: URL của ứng dụng
   - **Use case description**: 
     ```
     We are building a course registration system for students.
     The system needs to send transactional emails including:
     - Course registration confirmations
     - Course cancellation confirmations
     - User notifications
     
     Expected volume: ~1,000 emails/day
     Users will only receive emails when they take actions in our system.
     We will comply with AWS SES policies and monitor bounce rates.
     ```
   - **Compliance**: Đồng ý tuân thủ chính sách
   - **Bounce handling**: Có process xử lý bounces
   - **Opt-out process**: Có cơ chế unsubscribe (nếu cần)

5. Submit và đợi AWS review (thường 1-2 ngày làm việc)

---

## 4. Cấu hình Django

### Bước 1: Cài đặt package

Cập nhật `backend/requirements.txt`:

```txt
# AWS SES Support
boto3==1.34.0
django-ses==3.5.0
```

Cài đặt:

```bash
cd backend
pip install django-ses boto3
```

### Bước 2: Cấu hình `backend/.env`

```env
# Email Configuration - AWS SES
EMAIL_BACKEND=django_ses.SESBackend
AWS_SES_REGION_NAME=us-east-1
AWS_SES_REGION_ENDPOINT=email.us-east-1.amazonaws.com

# AWS Credentials (Nếu không dùng IAM Role)
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=your-secret-access-key

# Email settings
DEFAULT_FROM_EMAIL=noreply@your-domain.com

# Optional: Configuration set for tracking
# AWS_SES_CONFIGURATION_SET=ses-configuration-set-name
```

### Bước 3: Cập nhật `settings.py`

File `backend/config/settings.py` đã được cấu hình sẵn, chỉ cần thêm:

```python
# AWS SES Configuration (thêm vào cuối file)
if os.getenv('EMAIL_BACKEND') == 'django_ses.SESBackend':
    AWS_SES_REGION_NAME = os.getenv('AWS_SES_REGION_NAME', 'us-east-1')
    AWS_SES_REGION_ENDPOINT = os.getenv('AWS_SES_REGION_ENDPOINT', 'email.us-east-1.amazonaws.com')
    
    # AWS credentials (tốt nhất là dùng IAM Role trên ECS/EC2)
    if os.getenv('AWS_ACCESS_KEY_ID'):
        AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # Optional: Use configuration set
    if os.getenv('AWS_SES_CONFIGURATION_SET'):
        AWS_SES_CONFIGURATION_SET = os.getenv('AWS_SES_CONFIGURATION_SET')
```

---

## 5. Cấu hình IAM Permissions

### Option 1: IAM User với Access Keys (Đơn giản)

**Tạo IAM User:**

1. Vào **IAM Console** → **Users** → **Add user**
2. User name: `ses-sender`
3. Access type: **Programmatic access**
4. Permissions: Attach policy **AmazonSESFullAccess** hoặc custom policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            "Resource": "*"
        }
    ]
}
```

5. Lưu **Access Key ID** và **Secret Access Key**
6. Thêm vào `backend/.env`

### Option 2: IAM Role (Khuyến nghị cho ECS/EC2)

**Tạo IAM Role:**

1. Vào **IAM Console** → **Roles** → **Create role**
2. Trusted entity: **AWS service** → **ECS Task** (hoặc EC2)
3. Attach policy: **AmazonSESFullAccess**
4. Role name: `ECSTaskSESRole`
5. Khi deploy ECS, attach role này vào Task Definition

**Ưu điểm**:
- ✅ Không cần hardcode credentials
- ✅ Tự động rotate credentials
- ✅ An toàn hơn

---

## 6. Testing

### Test 1: Test từ Django Shell

```bash
cd backend
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

# Test gửi email đơn giản
send_mail(
    'Test Email from SES',
    'This is a test email from AWS SES.',
    settings.DEFAULT_FROM_EMAIL,
    ['recipient@example.com'],  # Email đã verify nếu còn trong sandbox
    fail_silently=False,
)

print("Email sent successfully!")
```

### Test 2: Test HTML Email

```python
from django.core.mail import EmailMultiAlternatives

subject = 'Test HTML Email'
text_content = 'This is a plain text version'
html_content = '''
<html>
  <body>
    <h1>Hello from AWS SES!</h1>
    <p>This is a <strong>test</strong> email.</p>
  </body>
</html>
'''

email = EmailMultiAlternatives(
    subject,
    text_content,
    settings.DEFAULT_FROM_EMAIL,
    ['recipient@example.com']
)
email.attach_alternative(html_content, "text/html")
email.send()

print("HTML email sent successfully!")
```

### Test 3: Test qua API

```bash
# Đăng nhập và lấy token
curl -X POST http://localhost:8000/api/login/student_login/ \
  -H "Content-Type: application/json" \
  -d '{"mssv": "SV001", "password": "password123"}'

# Đăng ký môn học (sẽ tự động gửi email)
curl -X POST http://localhost:8000/api/registrations/register/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"course_id": 1}'
```

### Test 4: Monitor trong AWS Console

1. Vào **SES Console** → **Account dashboard**
2. Xem **Sending statistics**:
   - Emails sent
   - Delivery rate
   - Bounce rate
   - Complaint rate

---

## 7. Troubleshooting

### Lỗi: "Email address is not verified"

**Nguyên nhân**: Email chưa được verify hoặc còn trong sandbox mode

**Giải pháp**:
1. Verify email address hoặc domain
2. Request production access nếu muốn gửi tới email chưa verify

### Lỗi: "AccessDeniedException"

**Nguyên nhân**: Thiếu permissions

**Giải pháp**:
```bash
# Kiểm tra credentials
aws sts get-caller-identity

# Kiểm tra permissions
aws ses get-send-quota --region us-east-1
```

### Lỗi: "MessageRejected: Email address not verified"

**Nguyên nhân**: FROM email chưa verify

**Giải pháp**:
- Verify email hoặc domain trong SES Console
- Đảm bảo `DEFAULT_FROM_EMAIL` trong `.env` khớp với email đã verify

### Lỗi: "Daily sending quota exceeded"

**Nguyên nhân**: Vượt quá limit (200/day trong sandbox)

**Giải pháp**:
- Request production access
- Hoặc chờ 24h để quota reset

### Email không gửi được (không có lỗi)

**Debug steps**:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from django.core.mail import send_mail
send_mail(...) # Xem logs chi tiết
```

**Kiểm tra logs**:
```bash
# Django logs
tail -f /path/to/logs/django.log

# CloudWatch logs (nếu trên AWS)
aws logs tail /aws/ecs/course-registration --follow
```

---

## 8. Best Practices

### ✅ Security

1. **Không hardcode credentials** trong code
2. Dùng **IAM Roles** thay vì Access Keys khi có thể
3. Store credentials trong **AWS Secrets Manager** hoặc **Parameter Store**
4. Enable **MFA** cho IAM users có quyền SES

### ✅ Deliverability

1. **Verify domain** thay vì individual emails
2. Setup **SPF, DKIM, DMARC** records đúng cách
3. Monitor **bounce và complaint rates** (< 5%)
4. Xử lý bounces và complaints:

```python
# Thêm vào models.py
class EmailBounce(models.Model):
    email = models.EmailField()
    bounce_type = models.CharField(max_length=20)  # hard, soft
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'email_bounces'
```

5. Implement **unsubscribe mechanism** nếu gửi marketing emails

### ✅ Monitoring

1. Setup **CloudWatch Alarms**:
   - Bounce rate > 5%
   - Complaint rate > 0.1%
   - Sending failures

2. Enable **Event Publishing** cho:
   - Sends
   - Deliveries
   - Bounces
   - Complaints

3. Log tất cả email activities:

```python
# Trong email_service.py
logger.info(f"Sending email to {student.email}, subject: {subject}")
```

### ✅ Cost Optimization

**Pricing** (tính tới February 2026):
- **$0.10** per 1,000 emails
- **Free tier**: 62,000 emails/month khi gửi từ EC2

**Tips**:
- Batch emails khi có thể
- Không gửi email không cần thiết
- Clean email list thường xuyên

---

## 9. Production Checklist

- [ ] Domain verified với DKIM
- [ ] Production access approved
- [ ] IAM Role/User configured đúng
- [ ] `.env` file có đủ config
- [ ] Test gửi email thành công
- [ ] SPF record: `v=spf1 include:amazonses.com ~all`
- [ ] DMARC record configured
- [ ] Bounce/complaint handling implemented
- [ ] CloudWatch monitoring enabled
- [ ] Backup SMTP provider (optional)

---

## 10. Alternative: Gmail SMTP (Development Only)

Nếu chỉ test development, có thể dùng Gmail SMTP:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password  # Không phải password thường!
```

**Tạo App Password**:
1. Vào https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Generate App Password
4. Dùng password này trong EMAIL_HOST_PASSWORD

⚠️ **Không dùng Gmail SMTP cho production**:
- Giới hạn 500 emails/day
- Có thể bị block account
- Không đáng tin cậy

---

## 📚 Resources

- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [Django SES Package](https://github.com/django-ses/django-ses)
- [Email Best Practices](https://docs.aws.amazon.com/ses/latest/dg/best-practices.html)
- [SES Pricing](https://aws.amazon.com/ses/pricing/)

## 🆘 Support

Nếu gặp vấn đề:
1. Check CloudWatch Logs
2. Verify SES Dashboard for errors
3. Test với AWS CLI: `aws ses send-email --help`
4. Contact AWS Support (nếu có support plan)
