"""Service for mapping CSV column names to device properties"""


def get_device_info_from_column(column_name: str):
    """Map CSV column names to device properties
    
    Args:
        column_name: The name of the CSV column
        
    Returns:
        dict: Dictionary containing device properties (metric_name, name, sensor_type, category, unit)
              or None if the column should be skipped
    """
    column_lower = column_name.lower()
    
    # Power consumption columns
    if "[kw]" in column_lower or "power" in column_lower:
        metric_name = column_name.split("[")[0].strip()
        sensor_type = "power"
        unit = "kW"
        
        # Determine category based on device name
        if any(x in column_lower for x in ["dishwasher", "fridge", "microwave", "kitchen"]):
            category = "kitchen"
        elif any(x in column_lower for x in ["furnace", "heating"]):
            category = "heating"
        elif "solar" in column_lower or "gen" in column_lower:
            category = "energy"
        elif "office" in column_lower:
            category = "office"
        elif "living room" in column_lower:
            category = "living"
        elif "wine cellar" in column_lower:
            category = "storage"
        elif "garage" in column_lower:
            category = "garage"
        elif "barn" in column_lower or "well" in column_lower:
            category = "outdoor"
        else:
            category = "general"
        
        return {
            "metric_name": metric_name,
            "name": column_name,
            "sensor_type": sensor_type,
            "category": category,
            "unit": unit
        }
    
    # Weather columns
    elif "temperature" in column_lower:
        return {
            "metric_name": "temperature",
            "name": "Temperature Sensor",
            "sensor_type": "temperature",
            "category": "weather",
            "unit": "°C"
        }
    elif "humidity" in column_lower:
        return {
            "metric_name": "humidity",
            "name": "Humidity Sensor",
            "sensor_type": "humidity",
            "category": "weather",
            "unit": "%"
        }
    elif "pressure" in column_lower:
        return {
            "metric_name": "pressure",
            "name": "Pressure Sensor",
            "sensor_type": "pressure",
            "category": "weather",
            "unit": "Pa"
        }
    elif "windspeed" in column_lower:
        return {
            "metric_name": "windSpeed",
            "name": "Wind Speed Sensor",
            "sensor_type": "wind",
            "category": "weather",
            "unit": "m/s"
        }
    elif "visibility" in column_lower:
        return {
            "metric_name": "visibility",
            "name": "Visibility Sensor",
            "sensor_type": "visibility",
            "category": "weather",
            "unit": "km"
        }
    elif "dewpoint" in column_lower:
        return {
            "metric_name": "dewPoint",
            "name": "Dew Point Sensor",
            "sensor_type": "temperature",
            "category": "weather",
            "unit": "°C"
        }
    elif "precip" in column_lower:
        if "intensity" in column_lower:
            return {
                "metric_name": "precipIntensity",
                "name": "Precipitation Intensity Sensor",
                "sensor_type": "precipitation",
                "category": "weather",
                "unit": "mm/h"
            }
        elif "probability" in column_lower:
            return {
                "metric_name": "precipProbability",
                "name": "Precipitation Probability Sensor",
                "sensor_type": "precipitation",
                "category": "weather",
                "unit": "%"
            }
    elif "windbearing" in column_lower or "wind_bearing" in column_lower:
        return {
            "metric_name": "windBearing",
            "name": "Wind Bearing Sensor",
            "sensor_type": "wind",
            "category": "weather",
            "unit": "degrees"
        }
    elif "cloudcover" in column_lower or "cloud_cover" in column_lower:
        return {
            "metric_name": "cloudCover",
            "name": "Cloud Cover Sensor",
            "sensor_type": "cloud",
            "category": "weather",
            "unit": "%"
        }
    elif "apparenttemperature" in column_lower:
        return {
            "metric_name": "apparentTemperature",
            "name": "Apparent Temperature Sensor",
            "sensor_type": "temperature",
            "category": "weather",
            "unit": "°C"
        }
    
    # Skip time, icon, summary columns
    elif column_lower in ["time", "icon", "summary"]:
        return None
    
    # Default for unknown columns
    return {
        "metric_name": column_name,
        "name": column_name,
        "sensor_type": "unknown",
        "category": "general",
        "unit": None
    }

