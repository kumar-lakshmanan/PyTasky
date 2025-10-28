'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-25"
__author__  = "kayma"
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import time

# Kafka connection
bootstrap_servers = 'localhost:9094'
topic_name = 'maintopic'

# Create Kafka Admin client
admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers, client_id='python-admin')

# Check & create topic if not exists
existing_topics = admin.list_topics()
if topic_name not in existing_topics:
    print(f"Creating topic '{topic_name}' ...")
    topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
    try:
        admin.create_topics([topic])
        print(f"Topic '{topic_name}' created successfully.")
        time.sleep(2)  # give broker a moment to register topic
    except TopicAlreadyExistsError:
        print(f"Topic '{topic_name}' already exists.")
else:
    print(f"Topic '{topic_name}' already exists.")

admin.close()

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: v.encode('utf-8')
)

# Send message
message = "Hello Kafka - auto topic create from Python!"
print("Sending message...")
future = producer.send(topic_name, value=message)
result = future.get(timeout=10)
print(f"Message sent to {result.topic} partition {result.partition} offset {result.offset}")

producer.flush()
producer.close()
