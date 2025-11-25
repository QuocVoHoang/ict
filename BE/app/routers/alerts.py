from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate, AlertResponse

router = APIRouter()


@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    skip: int = 0,
    limit: int = 100,
    device_id: Optional[int] = None,
    alert_type: Optional[str] = None,
    severity: Optional[str] = None,
    is_read: Optional[bool] = None,
    is_resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all alerts with optional filters"""
    query = db.query(Alert)
    
    if device_id:
        query = query.filter(Alert.device_id == device_id)
    
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    if is_read is not None:
        query = query.filter(Alert.is_read == is_read)
    
    if is_resolved is not None:
        query = query.filter(Alert.is_resolved == is_resolved)
    
    alerts = query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """Get a specific alert by ID"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {alert_id} not found"
        )
    return alert


@router.post("/", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """Create a new alert"""
    db_alert = Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.patch("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db)
):
    """Update an alert (mark as read or resolved)"""
    from datetime import datetime
    
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {alert_id} not found"
        )
    
    update_data = alert_update.model_dump(exclude_unset=True)
    
    # If marking as resolved, set resolved_at timestamp
    if update_data.get("is_resolved") and not db_alert.is_resolved:
        db_alert.resolved_at = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(db_alert, field, value)
    
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """Delete an alert"""
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with id {alert_id} not found"
        )
    
    db.delete(db_alert)
    db.commit()
    return None


@router.get("/unread/count")
async def get_unread_count(db: Session = Depends(get_db)):
    """Get count of unread alerts"""
    count = db.query(Alert).filter(Alert.is_read == False).count()
    return {"unread_count": count}


@router.post("/mark-all-read", status_code=status.HTTP_200_OK)
async def mark_all_read(db: Session = Depends(get_db)):
    """Mark all alerts as read"""
    db.query(Alert).filter(Alert.is_read == False).update({"is_read": True})
    db.commit()
    return {"message": "All alerts marked as read"}

