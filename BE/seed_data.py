"""
Seed database with sample data for testing
"""
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.device import Device
from app.models.sensor import SensorData
from app.models.alert import Alert
import random


def seed_devices(db):
    """Create sample devices"""
    devices = [
        Device(
            name="Smart Thermostat",
            device_type="sensor",
            location="Living Room",
            is_online=True,
            mac_address="AA:BB:CC:DD:EE:01",
            firmware_version="1.2.0",
            battery_level=95.0
        ),
        Device(
            name="Temperature Sensor",
            device_type="sensor",
            location="Bedroom",
            is_online=True,
            mac_address="AA:BB:CC:DD:EE:02",
            firmware_version="1.1.0",
            battery_level=82.0
        ),
        Device(
            name="Humidity Sensor",
            device_type="sensor",
            location="Kitchen",
            is_online=False,
            mac_address="AA:BB:CC:DD:EE:03",
            firmware_version="1.0.5",
            battery_level=45.0
        ),
        Device(
            name="Air Quality Monitor",
            device_type="sensor",
            location="Living Room",
            is_online=True,
            mac_address="AA:BB:CC:DD:EE:04",
            firmware_version="2.0.1",
            battery_level=100.0
        ),
    ]
    
    db.add_all(devices)
    db.commit()
    print(f"✅ Created {len(devices)} devices")
    return devices


def seed_sensor_data(db, devices):
    """Create sample sensor data"""
    sensor_data = []
    base_time = datetime.utcnow() - timedelta(days=1)
    
    for device in devices[:3]:  # First 3 devices
        for i in range(24):  # 24 hours of data
            timestamp = base_time + timedelta(hours=i)
            
            # Temperature data
            sensor_data.append(SensorData(
                device_id=device.id,
                sensor_type="temperature",
                value=20 + random.uniform(-3, 5),
                unit="°C",
                timestamp=timestamp,
                location=device.location,
                quality="good"
            ))
            
            # Humidity data
            if device.name != "Temperature Sensor":
                sensor_data.append(SensorData(
                    device_id=device.id,
                    sensor_type="humidity",
                    value=50 + random.uniform(-10, 15),
                    unit="%",
                    timestamp=timestamp,
                    location=device.location,
                    quality="good"
                ))
    
    db.add_all(sensor_data)
    db.commit()
    print(f"✅ Created {len(sensor_data)} sensor data entries")


def seed_alerts(db, devices):
    """Create sample alerts"""
    alerts = [
        Alert(
            device_id=devices[0].id,
            alert_type="warning",
            severity="medium",
            title="High Temperature Detected",
            message="Temperature in Living Room exceeded 25°C",
            is_read=False,
            is_resolved=False
        ),
        Alert(
            device_id=devices[2].id,
            alert_type="error",
            severity="high",
            title="Device Offline",
            message="Humidity Sensor in Kitchen is offline",
            is_read=True,
            is_resolved=False
        ),
        Alert(
            device_id=devices[1].id,
            alert_type="info",
            severity="low",
            title="Low Battery",
            message="Temperature Sensor battery below 85%",
            is_read=True,
            is_resolved=True,
            resolved_at=datetime.utcnow() - timedelta(hours=2)
        ),
        Alert(
            device_id=None,
            alert_type="info",
            severity="low",
            title="System Update Available",
            message="A new firmware update is available for your devices",
            is_read=False,
            is_resolved=False
        ),
    ]
    
    db.add_all(alerts)
    db.commit()
    print(f"✅ Created {len(alerts)} alerts")


def seed_database():
    """Main function to seed all data"""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding database with sample data...\n")
        
        # Check if data already exists
        existing_devices = db.query(Device).count()
        if existing_devices > 0:
            print("⚠️  Database already contains data. Clear it first if you want to reseed.")
            return
        
        devices = seed_devices(db)
        seed_sensor_data(db, devices)
        seed_alerts(db, devices)
        
        print("\n✅ Database seeding completed successfully!")
        print("\nYou can now start the API server and test the endpoints.")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

