from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models.sensor import SensorData
from app.schemas.sensor import SensorDataCreate, SensorDataResponse

router = APIRouter()


@router.get("/", response_model=List[SensorDataResponse])
async def get_sensor_data(
    skip: int = 0,
    limit: int = 100,
    device_id: Optional[int] = None,
    sensor_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get sensor data with optional filters"""
    query = db.query(SensorData)
    
    if device_id:
        query = query.filter(SensorData.device_id == device_id)
    
    if sensor_type:
        query = query.filter(SensorData.sensor_type == sensor_type)
    
    if start_date:
        query = query.filter(SensorData.timestamp >= start_date)
    
    if end_date:
        query = query.filter(SensorData.timestamp <= end_date)
    
    sensor_data = query.order_by(SensorData.timestamp.desc()).offset(skip).limit(limit).all()
    return sensor_data


@router.get("/{sensor_data_id}", response_model=SensorDataResponse)
async def get_sensor_data_by_id(sensor_data_id: int, db: Session = Depends(get_db)):
    """Get specific sensor data by ID"""
    sensor_data = db.query(SensorData).filter(SensorData.id == sensor_data_id).first()
    if not sensor_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor data with id {sensor_data_id} not found"
        )
    return sensor_data


@router.post("/", response_model=SensorDataResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor_data(sensor_data: SensorDataCreate, db: Session = Depends(get_db)):
    """Create new sensor data entry"""
    db_sensor_data = SensorData(**sensor_data.model_dump())
    db.add(db_sensor_data)
    db.commit()
    db.refresh(db_sensor_data)
    return db_sensor_data


@router.get("/device/{device_id}/latest", response_model=List[SensorDataResponse])
async def get_latest_sensor_data(
    device_id: int,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get latest sensor data for a specific device"""
    sensor_data = (
        db.query(SensorData)
        .filter(SensorData.device_id == device_id)
        .order_by(SensorData.timestamp.desc())
        .limit(limit)
        .all()
    )
    return sensor_data


@router.get("/device/{device_id}/stats")
async def get_sensor_stats(
    device_id: int,
    sensor_type: str,
    hours: int = Query(24, ge=1, le=168),  # Last 24 hours by default, max 1 week
    db: Session = Depends(get_db)
):
    """Get statistics for sensor data (avg, min, max) for a device"""
    from sqlalchemy import func
    
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    stats = (
        db.query(
            func.avg(SensorData.value).label("average"),
            func.min(SensorData.value).label("minimum"),
            func.max(SensorData.value).label("maximum"),
            func.count(SensorData.id).label("count")
        )
        .filter(
            SensorData.device_id == device_id,
            SensorData.sensor_type == sensor_type,
            SensorData.timestamp >= start_time
        )
        .first()
    )
    
    if stats.count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No sensor data found for device {device_id} and type {sensor_type}"
        )
    
    return {
        "device_id": device_id,
        "sensor_type": sensor_type,
        "period_hours": hours,
        "average": float(stats.average) if stats.average else None,
        "minimum": float(stats.minimum) if stats.minimum else None,
        "maximum": float(stats.maximum) if stats.maximum else None,
        "data_points": stats.count
    }

