# 🚀 Quick Start Guide

Hướng dẫn nhanh để chạy FastAPI backend.

## ⚡ Bắt đầu trong 3 bước

### Bước 1: Cài đặt dependencies

```bash
# Tạo virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Cài đặt packages
pip install -r requirements.txt
```

### Bước 2: Khởi tạo database

```bash
python init_db.py
```

### Bước 3: Chạy server

```bash
python main.py
```

🎉 Xong! API của bạn đã chạy tại http://localhost:8000

## 📖 Truy cập Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🌱 (Optional) Thêm dữ liệu mẫu

```bash
python seed_data.py
```

## 🧪 Test API

### Test với curl

```bash
# Health check
curl http://localhost:8000/health

# Lấy danh sách devices
curl http://localhost:8000/api/v1/devices

# Tạo device mới
curl -X POST http://localhost:8000/api/v1/devices \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Sensor",
    "device_type": "sensor",
    "location": "Living Room"
  }'
```

### Test với Python

```python
import requests

# Get all devices
response = requests.get("http://localhost:8000/api/v1/devices")
print(response.json())

# Create new device
new_device = {
    "name": "Temperature Sensor",
    "device_type": "sensor",
    "location": "Kitchen"
}
response = requests.post(
    "http://localhost:8000/api/v1/devices",
    json=new_device
)
print(response.json())
```

## 📝 Các lệnh hữu ích

```bash
# Chạy với auto-reload (development)
uvicorn main:app --reload

# Chạy trên port khác
uvicorn main:app --port 8080

# Chạy với workers (production)
uvicorn main:app --workers 4

# Xem logs chi tiết
uvicorn main:app --log-level debug
```

## 🔧 Cấu hình (Optional)

Tạo file `.env` từ template:

```bash
cp env.example .env
```

Sau đó chỉnh sửa các biến môi trường trong `.env` theo nhu cầu.

## ❓ Troubleshooting

### Lỗi: ModuleNotFoundError

```bash
# Đảm bảo đã activate virtual environment
source venv/bin/activate

# Cài lại dependencies
pip install -r requirements.txt
```

### Lỗi: Port already in use

```bash
# Chạy trên port khác
uvicorn main:app --port 8001
```

### Lỗi: Database locked

```bash
# Xóa database và tạo lại
rm iot_dashboard.db
python init_db.py
```

## 🎯 Endpoints chính

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/api/v1/devices` | Lấy danh sách devices |
| POST | `/api/v1/devices` | Tạo device mới |
| GET | `/api/v1/sensors` | Lấy dữ liệu sensors |
| POST | `/api/v1/sensors` | Gửi dữ liệu sensor |
| GET | `/api/v1/alerts` | Lấy danh sách alerts |
| POST | `/api/v1/alerts` | Tạo alert mới |

Xem đầy đủ tại: http://localhost:8000/docs

