from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class Device(Base):
    """Device model for IoT devices"""
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    device_type = Column(String, nullable=False)  # e.g., "sensor", "actuator", "controller"
    location = Column(String)
    status = Column(String, default="active")  # active, inactive, error
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Device specific attributes (can be JSON in production)
    ip_address = Column(String)
    mac_address = Column(String, unique=True)
    firmware_version = Column(String)
    battery_level = Column(Float)  # percentage
    
    def __repr__(self):
        return f"<Device(id={self.id}, name='{self.name}', type='{self.device_type}')>"

