'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:

send a msg to specific topic

'''

__created__ = "2025-10-25"
__updated__ = "2025-10-25"
__author__  = "kayma"
from kafka import KafkaProducer
import kTools; tls = kTools.KTools()

# Kafka connection
my_bootstrap_servers = 'localhost:9094'
my_topic_name = 'maintopic'
debugger = 1 

def sendMsg(msg):
    # Create Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=my_bootstrap_servers,
        value_serializer=lambda v: v.encode('utf-8')
    )
    
    # Send message
    print("Sending message...")
    if debugger: print(f"-\n{msg}\n-")
    future = producer.send(my_topic_name, value=msg)
    result = future.get(timeout=10)
    print(f"Message sent to {result.topic} partition {result.partition} offset {result.offset}")
    
    producer.flush()
    producer.close()

if __name__ == '__main__':
    msg = "My Msg Hello Kafka, send on: " + tls.getDateTime()  
    sendMsg(msg)
