# IoT Dashboard Backend API

Backend API cho IoT Dashboard được xây dựng bằng FastAPI.

## 📋 Tính năng

- ✅ **Device Management**: Quản lý các thiết bị IoT
- ✅ **Sensor Data**: Lưu trữ và truy vấn dữ liệu từ các cảm biến
- ✅ **Alerts System**: Hệ thống cảnh báo và thông báo
- ✅ **RESTful API**: API tuân thủ chuẩn REST
- ✅ **Auto Documentation**: Swagger UI và ReDoc tự động
- ✅ **Database Support**: SQLite (mặc định), PostgreSQL, MySQL
- ✅ **CORS Enabled**: Hỗ trợ Cross-Origin Resource Sharing

## 🚀 Cài đặt

### 1. Tạo môi trường ảo

```bash
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
# hoặc
venv\Scripts\activate  # Trên Windows
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình môi trường

```bash
cp .env.example .env
# Sau đó chỉnh sửa file .env theo nhu cầu
```

### 4. Khởi tạo database

```python
# Chạy trong Python shell hoặc tạo file init_db.py
from app.database import engine, Base
from app.models import Device, SensorData, Alert

Base.metadata.create_all(bind=engine)
```

## 🏃 Chạy server

### Development mode (với auto-reload)

```bash
python main.py
```

hoặc

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Server sẽ chạy tại: `http://localhost:8000`

## 📚 API Documentation

Sau khi khởi động server, bạn có thể truy cập:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Devices

- `GET /api/v1/devices` - Lấy danh sách thiết bị
- `GET /api/v1/devices/{device_id}` - Lấy thông tin thiết bị
- `POST /api/v1/devices` - Tạo thiết bị mới
- `PUT /api/v1/devices/{device_id}` - Cập nhật thiết bị
- `DELETE /api/v1/devices/{device_id}` - Xóa thiết bị
- `GET /api/v1/devices/status/online` - Lấy danh sách thiết bị online

### Sensors

- `GET /api/v1/sensors` - Lấy dữ liệu cảm biến (có filter)
- `GET /api/v1/sensors/{sensor_data_id}` - Lấy dữ liệu cảm biến cụ thể
- `POST /api/v1/sensors` - Tạo dữ liệu cảm biến mới
- `GET /api/v1/sensors/device/{device_id}/latest` - Lấy dữ liệu mới nhất
- `GET /api/v1/sensors/device/{device_id}/stats` - Thống kê dữ liệu cảm biến

### Alerts

- `GET /api/v1/alerts` - Lấy danh sách cảnh báo (có filter)
- `GET /api/v1/alerts/{alert_id}` - Lấy thông tin cảnh báo
- `POST /api/v1/alerts` - Tạo cảnh báo mới
- `PATCH /api/v1/alerts/{alert_id}` - Cập nhật cảnh báo
- `DELETE /api/v1/alerts/{alert_id}` - Xóa cảnh báo
- `GET /api/v1/alerts/unread/count` - Đếm cảnh báo chưa đọc
- `POST /api/v1/alerts/mark-all-read` - Đánh dấu tất cả đã đọc

## 🗂️ Cấu trúc project

```
BE/
├── app/
│   ├── __init__.py
│   ├── config.py          # Cấu hình ứng dụng
│   ├── database.py        # Database connection
│   ├── models/            # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── device.py
│   │   ├── sensor.py
│   │   └── alert.py
│   ├── schemas/           # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── device.py
│   │   ├── sensor.py
│   │   └── alert.py
│   └── routers/           # API endpoints
│       ├── __init__.py
│       ├── devices.py
│       ├── sensors.py
│       └── alerts.py
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables example
├── .gitignore
└── README.md
```

## 🔧 Sử dụng

### Ví dụ: Tạo thiết bị mới

```bash
curl -X POST "http://localhost:8000/api/v1/devices" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Temperature Sensor 1",
    "device_type": "sensor",
    "location": "Living Room",
    "mac_address": "AA:BB:CC:DD:EE:FF"
  }'
```

### Ví dụ: Gửi dữ liệu cảm biến

```bash
curl -X POST "http://localhost:8000/api/v1/sensors" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": 1,
    "sensor_type": "temperature",
    "value": 25.5,
    "unit": "°C",
    "location": "Living Room"
  }'
```

### Ví dụ: Tạo cảnh báo

```bash
curl -X POST "http://localhost:8000/api/v1/alerts" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": 1,
    "alert_type": "warning",
    "severity": "high",
    "title": "High Temperature",
    "message": "Temperature exceeded threshold"
  }'
```

## 🐳 Docker (Optional)

Tạo file `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build và chạy:

```bash
docker build -t iot-backend .
docker run -p 8000:8000 iot-backend
```

## 📝 Notes

- Database mặc định là SQLite, phù hợp cho development
- Với production, nên sử dụng PostgreSQL hoặc MySQL
- Đừng quên thay đổi `SECRET_KEY` trong file `.env`
- CORS đã được cấu hình cho phát triển local

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón!

## 📄 License

MIT License

