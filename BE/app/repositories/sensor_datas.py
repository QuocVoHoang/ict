from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.sensor import SensorData
from app.schemas.sensor import SensorDataCreate
from datetime import datetime


class SensorDataRepository:
    """Repository for SensorData CRUD operations"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, sensor_data: SensorDataCreate, timestamp: Optional[datetime] = None) -> SensorData:
        """Create a new sensor data entry"""
        db_sensor_data = SensorData(**sensor_data.model_dump())
        if timestamp:
            db_sensor_data.timestamp = timestamp
        self.db.add(db_sensor_data)
        self.db.commit()
        self.db.refresh(db_sensor_data)
        return db_sensor_data

    def create_batch(self, sensor_data_list: List[SensorDataCreate], timestamp: Optional[datetime] = None) -> List[SensorData]:
        """Create multiple sensor data entries in batch"""
        db_sensor_data_list = []
        for sensor_data in sensor_data_list:
            db_sensor_data = SensorData(**sensor_data.model_dump())
            if timestamp:
                db_sensor_data.timestamp = timestamp
            db_sensor_data_list.append(db_sensor_data)
        
        self.db.add_all(db_sensor_data_list)
        self.db.commit()
        for sensor_data in db_sensor_data_list:
            self.db.refresh(sensor_data)
        return db_sensor_data_list

    def read(self, sensor_data_id: int) -> Optional[SensorData]:
        """Get sensor data by ID"""
        return self.db.query(SensorData).filter(SensorData.id == sensor_data_id).first()

    def get_by_device(self, device_id: int, limit: int = 100) -> List[SensorData]:
        """Get sensor data by device ID"""
        return self.db.query(SensorData).filter(
            SensorData.device_id == device_id
        ).order_by(SensorData.timestamp.desc()).limit(limit).all()

