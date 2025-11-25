from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class SensorData(Base):
    """Sensor data model for storing IoT sensor readings"""
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, index=True)
    sensor_type = Column(String, nullable=False)  # temperature, humidity, pressure, etc.
    value = Column(Float, nullable=False)
    unit = Column(String)  # °C, %, Pa, etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Optional metadata
    location = Column(String)
    quality = Column(String)  # good, fair, poor
    
    def __repr__(self):
        return f"<SensorData(id={self.id}, type='{self.sensor_type}', value={self.value})>"

