"""
Initialize database tables
Run this script to create all tables in the database
"""
from app.database import engine, Base
from app.models import Device, SensorData, Alert

def init_database():
    """Create all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("\nTables created:")
    print("- devices")
    print("- sensor_data")
    print("- alerts")

if __name__ == "__main__":
    init_database()

