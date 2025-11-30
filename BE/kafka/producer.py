import pandas as pd
import json
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import time

# Read CSV
df = pd.read_csv("HomeC.csv")
df = df.head(10)  # Limit to first 10 records

print(f"Streaming {len(df)} records to Kafka...")

# Check if topic exists and create it if it doesn't
admin_client = KafkaAdminClient(
    bootstrap_servers="kafka:9092",
    client_id='admin'
)

topic_name = "smart-home-data"

# Get list of existing topics
existing_topics = admin_client.list_topics()

if topic_name not in existing_topics:
    print(f"Topic '{topic_name}' does not exist. Creating it...")
    topic = NewTopic(
        name=topic_name,
        num_partitions=1,
        replication_factor=1
    )
    try:
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        print(f"✓ Topic '{topic_name}' created successfully!")
    except TopicAlreadyExistsError:
        print(f"Topic '{topic_name}' already exists (race condition).")
else:
    print(f"Topic '{topic_name}' already exists.")

admin_client.close()

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for _, row in df.iterrows():
    data = row.to_dict()  # convert row to dict
    producer.send(topic_name, value=data)
    time.sleep(0.1)  # optional: slow down for testing

producer.flush()
print(f"✓ Successfully streamed {len(df)} records to Kafka!")
