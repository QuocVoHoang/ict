"""
Simple test script to verify API endpoints
Run: python test_api.py
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"📋 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, default=str)}")
    except:
        print(f"Response: {response.text}")


def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_create_device():
    """Test device creation"""
    device_data = {
        "name": "Test Temperature Sensor",
        "device_type": "sensor",
        "location": "Test Room",
        "ip_address": "192.168.1.100",
        "mac_address": "AA:BB:CC:DD:EE:99"
    }
    response = requests.post(f"{BASE_URL}/api/v1/devices", json=device_data)
    print_response("Create Device", response)
    return response.json() if response.status_code == 201 else None


def test_get_devices():
    """Test get all devices"""
    response = requests.get(f"{BASE_URL}/api/v1/devices")
    print_response("Get All Devices", response)
    return response.json() if response.status_code == 200 else []


def test_create_sensor_data(device_id):
    """Test sensor data creation"""
    sensor_data = {
        "device_id": device_id,
        "sensor_type": "temperature",
        "value": 23.5,
        "unit": "°C",
        "location": "Test Room",
        "quality": "good"
    }
    response = requests.post(f"{BASE_URL}/api/v1/sensors", json=sensor_data)
    print_response("Create Sensor Data", response)
    return response.json() if response.status_code == 201 else None


def test_get_sensors():
    """Test get all sensor data"""
    response = requests.get(f"{BASE_URL}/api/v1/sensors")
    print_response("Get All Sensor Data", response)
    return response.json() if response.status_code == 200 else []


def test_create_alert(device_id):
    """Test alert creation"""
    alert_data = {
        "device_id": device_id,
        "alert_type": "warning",
        "severity": "medium",
        "title": "Test Alert",
        "message": "This is a test alert from test script"
    }
    response = requests.post(f"{BASE_URL}/api/v1/alerts", json=alert_data)
    print_response("Create Alert", response)
    return response.json() if response.status_code == 201 else None


def test_get_alerts():
    """Test get all alerts"""
    response = requests.get(f"{BASE_URL}/api/v1/alerts")
    print_response("Get All Alerts", response)
    return response.json() if response.status_code == 200 else []


def test_sensor_stats(device_id):
    """Test sensor statistics"""
    response = requests.get(
        f"{BASE_URL}/api/v1/sensors/device/{device_id}/stats",
        params={"sensor_type": "temperature", "hours": 24}
    )
    print_response("Sensor Statistics", response)


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 IoT Dashboard API Test Suite")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test 1: Health check
        if not test_health():
            print("\n❌ Health check failed! Is the server running?")
            return
        
        # Test 2: Create device
        device = test_create_device()
        if not device:
            print("\n❌ Failed to create device")
            return
        
        device_id = device.get("id")
        print(f"\n✅ Created device with ID: {device_id}")
        
        # Test 3: Get all devices
        devices = test_get_devices()
        print(f"\n✅ Found {len(devices)} device(s)")
        
        # Test 4: Create sensor data
        sensor_data = test_create_sensor_data(device_id)
        if sensor_data:
            print(f"\n✅ Created sensor data with ID: {sensor_data.get('id')}")
        
        # Test 5: Get all sensor data
        sensors = test_get_sensors()
        print(f"\n✅ Found {len(sensors)} sensor data entry(ies)")
        
        # Test 6: Create alert
        alert = test_create_alert(device_id)
        if alert:
            print(f"\n✅ Created alert with ID: {alert.get('id')}")
        
        # Test 7: Get all alerts
        alerts = test_get_alerts()
        print(f"\n✅ Found {len(alerts)} alert(s)")
        
        # Test 8: Get sensor statistics (if we have data)
        if sensors:
            test_sensor_stats(device_id)
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server!")
        print("Make sure the server is running at:", BASE_URL)
        print("\nStart server with: python main.py")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

