import os

# Kiểm tra và tạo file .env nếu chưa có
env_file = os.path.join(os.path.dirname(__file__), '.env')
if not os.path.exists(env_file):
    with open(env_file, 'w') as f:
        with open(os.path.join(os.path.dirname(__file__), '.env.example'), 'r') as example:
            f.write(example.read())
    print(f"File .env đã được tạo. Vui lòng chỉnh sửa file để cấu hình.")
