import asyncio
import json
from datetime import datetime
from aiokafka import AIOKafkaConsumer
from app.database import SessionLocal
from app.repositories.devices import DeviceRepository
from app.repositories.sensor_datas import SensorDataRepository
from app.schemas.sensor import SensorDataCreate
from app.services.device_mapper import get_device_info_from_column


async def consume():
    consumer = AIOKafkaConsumer(
        "smart-home-data",
        bootstrap_servers="kafka:9092",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    await consumer.start()
    
    # Create database session
    db = SessionLocal()
    device_repo = DeviceRepository(db)
    sensor_data_repo = SensorDataRepository(db)
    
    try:
        async for msg in consumer:
            row = msg.value
            
            # Extract timestamp
            timestamp_str = row.get("time")
            if timestamp_str:
                try:
                    # Convert Unix timestamp to datetime
                    timestamp = datetime.fromtimestamp(float(timestamp_str))
                except (ValueError, TypeError):
                    timestamp = datetime.now()
            else:
                timestamp = datetime.now()
            
            # Process each column (except time)
            for column_name, value in row.items():
                if column_name == "time":
                    continue
                
                # Skip None, empty, or invalid values
                if value is None or value == "" or (isinstance(value, str) and value.lower() in ["nan", "none", "null"]):
                    continue
                
                try:
                    # Convert value to float
                    float_value = float(value)
                except (ValueError, TypeError):
                    # Skip non-numeric values (like "icon", "summary")
                    continue
                
                # Get device info from column name
                device_info = get_device_info_from_column(column_name)
                if not device_info:
                    continue
                
                # Get or create device
                device = device_repo.get_or_create_by_metric_name(
                    metric_name=device_info["metric_name"],
                    name=device_info["name"],
                    sensor_type=device_info["sensor_type"],
                    category=device_info["category"],
                    device_type="sensor",
                    location=None
                )
                
                # Create sensor data
                sensor_data = SensorDataCreate(
                    device_id=device.id,
                    sensor_type=device_info["sensor_type"],
                    value=float_value,
                    unit=device_info["unit"],
                    location=None,
                    quality="good"
                )
                
                sensor_data_repo.create(sensor_data, timestamp=timestamp)
                print(f"✓ Saved: {device_info['name']} = {float_value} {device_info.get('unit', '')} at {timestamp}")
            
            print(f"✓ Processed row at {timestamp}")
            
    except Exception as e:
        print(f"Error processing message: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await consumer.stop()
        db.close()

