# K6 load test

Script: `loadtests/k6-api-load.js`

## 1) Cài k6

Ubuntu/Debian:

```bash
sudo gpg -k
sudo apt-get update
sudo apt-get install -y gnupg ca-certificates
curl -fsSL https://dl.k6.io/key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/k6-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install -y k6
```

## 2) Chạy nhanh

```bash
cd App
BASE_URL=http://localhost:8000 IDENTIFIER=sv001 PASSWORD='Password123!' VUS=30 DURATION=2m k6 run loadtests/k6-api-load.js
```

## 3) Tùy chỉnh

- `BASE_URL`: URL backend, ví dụ `http://localhost:8000`
- `IDENTIFIER`: mssv/email/username để login
- `PASSWORD`: mật khẩu tài khoản test
- `VUS`: mức tải đỉnh (default: `30`)
- `DURATION`: thời gian giữ tải ở mức `VUS` (default: `2m`)
- `THINK_TIME`: pause giữa iteration, giây (default: `0.3`)

## 4) Kết quả cần nhìn

- `http_req_failed`: tỷ lệ lỗi request
- `http_req_duration` p95: độ trễ ở phân vị 95%
- `checks`: tỷ lệ pass check logic

Nếu backend chạy trong Docker Compose, đảm bảo service backend đã up trước khi chạy k6.
