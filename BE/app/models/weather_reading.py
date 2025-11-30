"""

- WeatherReading: lưu thông tin thời tiết (weather) để so sánh với dữ liệu SensorData trong nhà.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class WeatherReading(Base):
    """
    WeatherReading:
    - Lưu thông tin thời tiết bên ngoài tại từng thời điểm (timestamp)
    - Dựa trên các cột trong dataset:
      time, temperature, humidity, visibility, summary, apparentTemperature,
      pressure, windSpeed, cloudCover, windBearing, precipIntensity,
      dewPoint, precipProbability, icon
    """

    __tablename__ = "weather_readings"

    id = Column(Integer, primary_key=True, index=True)

    # Thời điểm của bản ghi thời tiết
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Các trường weather chính (đặt tên gần giống dataset)
    temperature = Column(Float)             # temperature
    apparent_temperature = Column(Float)    # apparentTemperature
    humidity = Column(Float)                # humidity (0–1 hoặc 0–100 tùy cách bạn scale)
    visibility = Column(Float)              # visibility
    pressure = Column(Float)                # pressure
    wind_speed = Column(Float)              # windSpeed
    wind_bearing = Column(Float)            # windBearing
    cloud_cover = Column(Float)             # cloudCover
    precip_intensity = Column(Float)        # precipIntensity
    precip_probability = Column(Float)      # precipProbability
    dew_point = Column(Float)               # dewPoint

    # Mô tả thời tiết
    summary = Column(String)                # summary (text mô tả: "Partly Cloudy", "Clear", ...)
    icon = Column(String)                   # icon (mã icon: "clear-day", "rain", ...)

    def __repr__(self) -> str:
        return (
            f"<WeatherReading(id={self.id}, ts={self.timestamp}, "
            f"temp={self.temperature}, hum={self.humidity})>"
        )
