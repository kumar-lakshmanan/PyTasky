'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:

PyQt based Kafka Listener works inside PyQt app Only.

'''

__created__ = "2025-10-25"
__updated__ = "2025-10-25"
__author__  = "kayma"
import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from kafka import KafkaConsumer
from types import SimpleNamespace

my_bootstrap_servers = 'localhost:9094'
my_topic_name = 'maintopic'
my_group_id = 'pytasky-custom-msgs'

class MyKafkaListener(QObject):
    message_received = pyqtSignal(str)

    def run(self):
        consumer = KafkaConsumer(
            my_topic_name,
            bootstrap_servers=my_bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id=my_group_id,
            value_deserializer=lambda v: v.decode('utf-8')
        )
        print(f"[Kafka] Listener started, listening {my_topic_name} @ {my_bootstrap_servers}...")
        for msg in consumer:
            self.message_received.emit(msg.value)

def createListener(qObjParent):
    print("[Kafka] Creating listener")
    qObjParent.mykafka = QObject()
    qObjParent.mykafka.thread = QThread()
    qObjParent.mykafka.worker = MyKafkaListener()
    qObjParent.mykafka.worker.moveToThread(qObjParent.mykafka.thread)
    qObjParent.mykafka.thread.started.connect(qObjParent.mykafka.worker.run)
    qObjParent.mykafka.worker.message_received.connect(onMessage)
    qObjParent.mykafka.thread.start()    

def onMessage(msg):
    print(f"[Kafka] Received a message in {my_topic_name}")
    print("-")
    print(msg)
    print("-") 
    
if __name__ == '__main__':
    # Running stand-alone, PTS object not available.
    if not "PTS" in locals().keys(): 
    #if not hasattr(__import__(__name__), "PTS"): 
        localQObj = QtWidgets.QApplication(sys.argv)
        createListener(localQObj)
        sys.exit(localQObj.exec_())
    else:
        createListener(PTS)
