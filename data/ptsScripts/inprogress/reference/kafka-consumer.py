'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-25"
__author__  = "kayma"
from kafka import KafkaConsumer

bootstrap_servers = 'localhost:9094'
topic_name = 'maintopic'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',   # start from earliest message
    enable_auto_commit=True,
    group_id='python-consumer-group',
    value_deserializer=lambda v: v.decode('utf-8')
)

print("Listening for messages...\n(Press Ctrl+C to stop)\n")

try:
    for msg in consumer:
        print(f"Received message: {msg.value} (partition={msg.partition}, offset={msg.offset})")
except KeyboardInterrupt:
    print("\nStopped by user")
finally:
    consumer.close()
    
print("Thank you")
