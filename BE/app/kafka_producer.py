import csv
import json
import time
from typing import Dict, Any

from app.config import settings
from kafka import KafkaProducer

def get_producer() -> KafkaProducer:
    
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    return producer

def row_to_message(row: Dict[str, str]) -> Dict[str, Any]:
    
    msg: Dict[str, Any] = dict(row)

    # cột 'time' đang là epoch (vd: 1451624400)
    if "time" in msg and msg["time"] != "":
        try:
            msg["timestamp"] = int(float(msg["time"]))
        except ValueError:
            msg["timestamp"] = msg["time"]

    return msg

def run_producer(csv_path: str, sleep_seconds: float = 0.05) -> None:
    
    producer = get_producer()

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            msg = row_to_message(row)
            producer.send(settings.KAFKA_TOPIC, msg)
            print(f"[PRODUCER] Sent #{i} timestamp={msg.get('timestamp')}")
            time.sleep(sleep_seconds)

    producer.flush()
    print("Producer finished sending all messages.")

if __name__ == "__main__":
    
    csv_path = "/app/data/raw/HomeC.csv"
    run_producer(csv_path, sleep_seconds=0.01)