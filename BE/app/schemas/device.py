from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DeviceBase(BaseModel):
    """Base device schema"""
    name: str = Field(..., min_length=1, max_length=100)
    device_type: str
    location: Optional[str] = None
    status: Optional[str] = "active"
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    firmware_version: Optional[str] = None


class DeviceCreate(DeviceBase):
    """Schema for creating a device"""
    pass


class DeviceUpdate(BaseModel):
    """Schema for updating a device"""
    name: Optional[str] = None
    device_type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    is_online: Optional[bool] = None
    ip_address: Optional[str] = None
    firmware_version: Optional[str] = None
    battery_level: Optional[float] = None


class DeviceResponse(DeviceBase):
    """Schema for device response"""
    id: int
    is_online: bool
    battery_level: Optional[float] = None
    last_seen: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

