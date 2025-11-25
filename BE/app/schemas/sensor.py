from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SensorDataBase(BaseModel):
    """Base sensor data schema"""
    device_id: int
    sensor_type: str = Field(..., description="Type of sensor (temperature, humidity, etc.)")
    value: float
    unit: Optional[str] = None
    location: Optional[str] = None
    quality: Optional[str] = "good"


class SensorDataCreate(SensorDataBase):
    """Schema for creating sensor data"""
    pass


class SensorDataResponse(SensorDataBase):
    """Schema for sensor data response"""
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

