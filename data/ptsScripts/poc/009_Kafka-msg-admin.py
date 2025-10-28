'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:

this script creates topics for listener and producer to send/recieve msg
 
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-25"
__author__  = "kayma"

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import time

# Kafka connection
my_bootstrap_servers = 'localhost:9094'
my_topic_name = 'maintopic'
my_admin_name = 'my-kafka-admin'

def createTopic():
    # Create Kafka Admin client
    admin = KafkaAdminClient(bootstrap_servers=my_bootstrap_servers, client_id=my_admin_name)
    
    # Check & create topic if not exists
    existing_topics = admin.list_topics()
    if my_topic_name not in existing_topics:
        print(f"Creating topic '{my_topic_name}' ...")
        topic = NewTopic(name=my_topic_name, num_partitions=1, replication_factor=1)
        try:
            admin.create_topics([topic])
            print(f"Topic '{my_topic_name}' created successfully.")
            time.sleep(2)  # give broker a moment to register topic
        except TopicAlreadyExistsError:
            print(f"Topic '{my_topic_name}' already exists.")
    else:
        print(f"Topic '{my_topic_name}' already exists.")
    admin.close()

if __name__ == '__main__':  
    createTopic()
