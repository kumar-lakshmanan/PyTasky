'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-31"
__author__  = "kayma"


import docker

client = docker.from_env()

services = []

#n8n
service_n8n = {
    "name": "n8n",
    "image": "n8nio/n8n:latest",
    "ports": {"5678/tcp": 5678},  # important: use tcp and int
    "env": {},
    "volumes": {
        r"G:\appdata\n8n": {
            "bind": "/home/node/.n8n",
            "mode": "rw"
        }
    }
}

services.append(service_n8n)

# Kafka Service
service_kafka = {
    "name": "kafka",
    "image": "bitnami/kafka:latest",
    "ports": {
        "9094/tcp": 9094,
        "9092/tcp": 9092
    },
    "env": {
        "KAFKA_ENABLE_KRAFT": "yes",
        "KAFKA_CFG_NODE_ID": "1",
        "KAFKA_KRAFT_CLUSTER_ID": "abcdefghijklmnopqrstuvwx",
        "KAFKA_CFG_PROCESS_ROLES": "broker,controller",
        "KAFKA_CFG_CONTROLLER_LISTENER_NAMES": "CONTROLLER",
        "KAFKA_CFG_LISTENERS": "PLAINTEXT://:9092,EXTERNAL://:9094,CONTROLLER://:9093",
        "KAFKA_CFG_ADVERTISED_LISTENERS": "PLAINTEXT://kafka:9092,EXTERNAL://localhost:9094",
        "KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP": "PLAINTEXT:PLAINTEXT,EXTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT",
        "KAFKA_CFG_CONTROLLER_QUORUM_VOTERS": "1@kafka:9093",
        "KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR": "1",
        "ALLOW_PLAINTEXT_LISTENER": "yes"
    },
    "volumes": {
        "./kafka-data": {
            "bind": "/bitnami/kafka",
            "mode": "rw"
        }
    }
}

services.append(service_kafka)

# Kafka UI Service
service_kafka_ui = {
    "name": "kafka-ui",
    "image": "provectuslabs/kafka-ui:latest",
    "ports": {
        "8080/tcp": 8080
    },
    "env": {
        "KAFKA_CLUSTERS_0_NAME": "local",
        "KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS": "kafka:9092",
        "KAFKA_CLUSTERS_0_ZOOKEEPER": "",
        "DYNAMIC_CONFIG_ENABLED": "true"
    },
    "volumes": {},
    "depends_on": ["kafka"]
}

services.append(service_kafka_ui)

# Network (optional)
network_name = "kafka-net"


def createContainer(service):
    print(f"Creating container: {service['name']}")    
    serviceName=service['name'] 
    image=service['image']
    ports=service['ports']
    env=service['env']
    vol=service['volumes']
    return client.containers.run(
                                    image,
                                    name=serviceName,
                                    ports=ports,
                                    environment=env,
                                    volumes=vol,
                                    detach=True
                                 )
def createAllContainers():
    for svc in services:
        try:
            container = createContainer(svc)
            net = client.networks.get(network_name)
            net.connect(container)        
        except docker.errors.APIError as e:
            print(f"Error creating {svc['name']}: {e.explanation}")
        
def getAllContainers():
    all_containers = client.containers.list(all=True)
    if all_containers:
        print("Available Docker containers:")
        for container in all_containers:
            print(f"  ID: {container.id[:12]}, Name: {container.name}, Status: {container.status}")
    else:
        print("No Docker containers found.")
    return all_containers

def createNetork():
    # Ensure the network exists
    try:
        client.networks.get(network_name)
    except docker.errors.NotFound:
        client.networks.create(network_name, driver="bridge")

def startContainer(container_name_or_id):    
    try:
        container = client.containers.get(container_name_or_id)
        if container.status == "exited":
            container.start()
            print(f"Container '{container_name_or_id}' started successfully.")
        else:
            print(f"Container '{container_name_or_id}' is not in a stopped state.")
    except docker.errors.NotFound:
        print(f"Container '{container_name_or_id}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")    
        
def startAllContainers(): 
    all_containers = getAllContainers()
    for eachContainer in all_containers:
        startContainer(eachContainer.name)

startAllContainers()
        