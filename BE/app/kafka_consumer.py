import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from kafka import KafkaConsumer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models.device import Device
from app.models.weather_reading import WeatherReading
from app.models.sensor import SensorData


ENERGY_COLUMN_MAPPING = {
    "use [kW]": ("Total Usage", "power", "kW"),
    "gen [kW]": ("Generation", "power", "kW"),
    "House overall [kW]": ("House Overall", "power", "kW"),
    "Dishwasher [kW]": ("Dishwasher", "power", "kW"),
    "Furnace 1 [kW]": ("Furnace 1", "power", "kW"),
    "Furnace 2 [kW]": ("Furnace 2", "power", "kW"),
    "Home office [kW]": ("Home Office", "power", "kW"),
    "Fridge [kW]": ("Fridge", "power", "kW"),
    "Wine cellar [kW]": ("Wine Cellar", "power", "kW"),
    "Garage door [kW]": ("Garage Door", "power", "kW"),
    "Kitchen 12 [kW]": ("Kitchen 12", "power", "kW"),
    "Kitchen 14 [kW]": ("Kitchen 14", "power", "kW"),
    "Kitchen 38 [kW]": ("Kitchen 38", "power", "kW"),
    "Barn [kW]": ("Barn", "power", "kW"),
    "Well [kW]": ("Well", "power", "kW"),
    "Microwave [kW]": ("Microwave", "power", "kW"),
    "Living room [kW]": ("Living Room", "power", "kW"),
    "Solar [kW]": ("Solar", "power", "kW"),
}


def epoch_to_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    try:
        # chấp nhận cả string/float/int
        ts = int(float(value))
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except (ValueError, TypeError):
        return None
    
def str_to_float(value: Any) -> Optional[float]:
    
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none", "cloudcover"}:
        # dataset có thể có chữ "cloudCover" trong cột numeric (row lỗi)
        return None
    try:
        return float(s)
    except ValueError:
        return None

def get_or_create_device(
    db: Session,
    name: str,
    device_type: str = "sensor",
    location: str = "home",
) -> Device:
    
    device = db.query(Device).filter(Device.name == name).first()
    if not device:
        device = Device(
            name=name,
            device_type=device_type,
            location=location,
            status="active",
            is_online=True,
        )
        db.add(device)
        db.commit()
        db.refresh(device)
    return device

def get_consumer() -> KafkaConsumer:
    """Khởi tạo KafkaConsumer đọc JSON từ topic raw."""
    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="smart_home_group",
    )
    return consumer

def process_energy_columns(db: Session, data: Dict[str, Any], ts: datetime) -> None:
    """
    Tạo SensorData cho các cột power trong dataset.
    """
    for col, (device_name, sensor_type, unit) in ENERGY_COLUMN_MAPPING.items():
        if col not in data:
            continue

        value = str_to_float(data.get(col))
        if value is None:
            continue

        device = get_or_create_device(
            db,
            name=device_name,
            device_type="sensor",
            location="home",
        )

        sensor_data = SensorData(
            device_id=device.id,
            sensor_type=sensor_type,  # "power"
            value=value,
            unit=unit,                # "kW"
            timestamp=ts,
            location=device.location,
            quality="good",
        )
        db.add(sensor_data)
def process_weather(db: Session, data: Dict[str, Any], ts: datetime) -> None:
    """
    Tạo WeatherReading từ các cột weather trong message.

    Cột dataset hiện tại:
    - temperature, icon, humidity, visibility, summary, apparentTemperature,
      pressure, windSpeed, cloudCover, windBearing, precipIntensity,
      dewPoint, precipProbability
    """

    weather_kwargs: Dict[str, Any] = {
        "timestamp": ts,
        "temperature": str_to_float(data.get("temperature")),
        "apparent_temperature": str_to_float(data.get("apparentTemperature")),
        "humidity": str_to_float(data.get("humidity")),
        "visibility": str_to_float(data.get("visibility")),
        "pressure": str_to_float(data.get("pressure")),
        "wind_speed": str_to_float(data.get("windSpeed")),
        "wind_bearing": str_to_float(data.get("windBearing")),
        "cloud_cover": str_to_float(data.get("cloudCover")),
        "precip_intensity": str_to_float(data.get("precipIntensity")),
        "precip_probability": str_to_float(data.get("precipProbability")),
        "dew_point": str_to_float(data.get("dewPoint")),
        "summary": data.get("summary"),
        "icon": data.get("icon"),
    }

    numeric_fields = [
        "temperature",
        "apparent_temperature",
        "humidity",
        "visibility",
        "pressure",
        "wind_speed",
        "wind_bearing",
        "cloud_cover",
        "precip_intensity",
        "precip_probability",
        "dew_point",
    ]

    # Nếu tất cả numeric field None → bỏ qua
    if all(weather_kwargs.get(f) is None for f in numeric_fields):
        return

    weather = WeatherReading(**weather_kwargs)
    db.add(weather)

def run_consumer() -> None:
    """
    Đọc message từ Kafka và ghi vào DB.
    """
    consumer = get_consumer()
    db: Session = SessionLocal()

    print("Kafka consumer started. Waiting for messages...")

    try:
        for msg in consumer:
            data: Dict[str, Any] = msg.value

            # Ưu tiên dùng trường 'timestamp' (epoch); fallback là 'time'
            raw_ts = data.get("timestamp", data.get("time"))
            ts = epoch_to_datetime(raw_ts)

            if ts is None:
                print(f"[CONSUMER] Skip message (invalid timestamp): {raw_ts}")
                continue

            # Ghi dữ liệu power (SensorData)
            process_energy_columns(db, data, ts)

            # Ghi dữ liệu thời tiết (WeatherReading)
            process_weather(db, data, ts)

            db.commit()
            print(f"[CONSUMER] Stored data for ts={ts.isoformat()}")
    except KeyboardInterrupt:
        print("Consumer stopped by user.")
    finally:
        db.close()


if __name__ == "__main__":
    run_consumer()