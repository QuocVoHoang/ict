from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AlertBase(BaseModel):
    """Base alert schema"""
    device_id: Optional[int] = None
    alert_type: str = Field(..., description="Type of alert (warning, error, info, critical)")
    severity: str = Field(default="medium", description="Severity level (low, medium, high, critical)")
    title: str = Field(..., min_length=1, max_length=200)
    message: str


class AlertCreate(AlertBase):
    """Schema for creating an alert"""
    pass


class AlertUpdate(BaseModel):
    """Schema for updating an alert"""
    is_read: Optional[bool] = None
    is_resolved: Optional[bool] = None


class AlertResponse(AlertBase):
    """Schema for alert response"""
    id: int
    is_read: bool
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

