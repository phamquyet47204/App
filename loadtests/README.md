# K6 load test

Script: `loadtests/k6-api-load.js`

Frontend burst script: `loadtests/k6-fe-burst.js`

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

## 5) Gia lap tang tai cho frontend

Chay mac dinh (burst):

```bash
cd App
BASE_URL=http://localhost k6 run loadtests/k6-fe-burst.js
```

Chay voi profile tuy bien:

```bash
cd App
BASE_URL=http://localhost \
RAMP_UP_1=20s RAMP_UP_1_TARGET=80 \
RAMP_UP_2=60s RAMP_UP_2_TARGET=200 \
HOLD=120s RAMP_DOWN=40s \
k6 run loadtests/k6-fe-burst.js
```

Bien moi truong cho frontend burst:

- `BASE_URL`: URL frontend, vi du `http://localhost` hoac domain CloudFront/ALB
- `RAMP_UP_1`, `RAMP_UP_1_TARGET`: pha tang tai 1
- `RAMP_UP_2`, `RAMP_UP_2_TARGET`: pha tang tai 2
- `HOLD`: giu tai dinh
- `RAMP_DOWN`: ha tai

Metric can theo doi:

- `http_req_failed`: ty le loi request
- `http_req_duration p95`: do tre p95
- `checks`: ty le pass check `status=200` va `content-type=text/html`

## 6) Chay k6 tren he thong ECS (khong phai local)

Ban can target vao URL production/staging dang chay tren AWS:

- Uu tien: domain CloudFront, vi du `https://app.yourdomain.com`
- Hoac: ALB DNS name, vi du `http://course-registration-alb-xxxx.us-east-1.elb.amazonaws.com`

### 6.1 Lay ALB DNS bang AWS CLI (neu can)

```bash
AWS_REGION=us-east-1
aws elbv2 describe-load-balancers \
	--region $AWS_REGION \
	--query 'LoadBalancers[].{name:LoadBalancerName,dns:DNSName}' \
	--output table
```

### 6.2 Chay burst test vao frontend tren ECS

```bash
cd App
BASE_URL=https://app.yourdomain.com \
RAMP_UP_1=30s RAMP_UP_1_TARGET=80 \
RAMP_UP_2=90s RAMP_UP_2_TARGET=250 \
HOLD=180s RAMP_DOWN=60s \
k6 run loadtests/k6-fe-burst.js
```

Neu chay truc tiep qua ALB (khong SSL):

```bash
cd App
BASE_URL=http://<alb-dns-name> k6 run loadtests/k6-fe-burst.js
```

### 6.3 Theo doi scale frontend trong luc test

- `ECS -> Cluster -> Service frontend -> Tasks`: so task tang theo policy
- `CloudWatch -> Metrics -> ECS/ServiceName`: `CPUUtilization`
- `EC2 -> Target Groups -> frontend TG -> Targets`: target van `healthy`
