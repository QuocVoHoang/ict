from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate


class DeviceRepository:
    """Repository for Device CRUD operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, device_data: DeviceCreate) -> Device:
        """Create a new device"""
        db_device = Device(**device_data.model_dump())
        self.db.add(db_device)
        self.db.commit()
        self.db.refresh(db_device)
        return db_device

    def read(self, device_id: int) -> Optional[Device]:
        """Get a device by ID"""
        return self.db.query(Device).filter(Device.id == device_id).first()

    def update(self, device_id: int, device_update: DeviceUpdate) -> Optional[Device]:
        """Update a device"""
        db_device = self.read(device_id)
        if not db_device:
            return None

        update_data = device_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_device, field, value)

        self.db.commit()
        self.db.refresh(db_device)
        return db_device

    def delete(self, device_id: int) -> bool:
        """Delete a device"""
        db_device = self.read(device_id)
        if not db_device:
            return False

        self.db.delete(db_device)
        self.db.commit()
        return True

    def get_by_metric_name(self, metric_name: str) -> Optional[Device]:
        """Get a device by metric_name"""
        return self.db.query(Device).filter(Device.metric_name == metric_name).first()

    def get_or_create_by_metric_name(
        self, 
        metric_name: str, 
        name: str,
        sensor_type: str,
        category: str,
        device_type: str = "sensor",
        location: Optional[str] = None
    ) -> Device:
        """Get a device by metric_name or create it if it doesn't exist"""
        device = self.get_by_metric_name(metric_name)
        if device:
            # Update last_seen and is_online
            device.is_online = True
            self.db.commit()
            self.db.refresh(device)
            return device
        
        # Create new device
        device = Device(
            name=name,
            metric_name=metric_name,
            sensor_type=sensor_type,
            category=category,
            device_type=device_type,
            location=location,
            status="active",
            is_online=True
        )
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

