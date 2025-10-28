'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-27"
__author__  = "kayma"

import sys
import time
import queue
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


#Valid action list
validActions = []
validActions.append("print")
validActions.append("exec_flow")
validActions.append("exec_script")


class PTSEventActionManager(QObject):
# PTS.MainQueue.put({ "action" : "print" , "params" :  "this is sample text to print" })
# PTS.MainQueue.put({ "action" : "exec_flow" , "params" :  {"flowFile" : 'G:/pyworkspace/PyTasky/data/ptsFlows/arithmatic.flow'} })
                
    def __init__(self, pyTaskyObj):
        super().__init__()
        self.PTS = pyTaskyObj
     
    def doAction(self, action, params):

        if action == "print":
            print(params)

        if action == "exec_flow":
            flowFile = params['flowFile']
            self.PTS.doExecuteFlow(flowFile)

        if action == "exec_script":
            scriptFile = params['scriptFile']
            self.PTS.doExecuteScript(scriptFile)

            
                   
# To send message : PTS.MainQueue.put("Hello world")
class PTSEventQueueManager(QObject):
    
    ACTION_REQUESTED = pyqtSignal(str, dict)  # signal to update UI safely
    ACTION_REQUESTED2 = pyqtSignal(str, str)  # signal to update UI safely

    def __init__(self, pyTaskyObj):
        super().__init__()
        self.PTS = pyTaskyObj
        self.main_queue = self.PTS.MainQueue
        self.running = True

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self.running:
            try:
                msg = self.main_queue.get(timeout=0.1)
                if msg == "__quit__":
                    break
                # Dispatch message
                self.process_message(msg)
                self.main_queue.task_done()
            except queue.Empty:
                continue

    def process_message(self, msg):
        """All message handling logic here."""
        print(f"[MainQueue] Received: {msg}")
        
        try:
            if type(msg) == type(""):
                msg = dict(msg)
        except:
            print("Received message is not valid, Unable to decode to dict.")
            return
            
        if self._isRequestMsgValid(msg):
            action = msg['action']
            params = msg['params']
            if type(params) == type(""):
                self.ACTION_REQUESTED2.emit(action, params)
            else:
                self.ACTION_REQUESTED.emit(action, params)
        else:
            print(f"Queue message {msg} ignored.")
            return

    def _isRequestMsgValid(self, msg):
        """
        Main Queue Message Processing Rules
        
        - msg should be dict
        - dict should have following top level keys
            - "action":
              a enum string, denotes what action to be done. check below for list of enum and desc 
            - "params":            
              a dict value, will be given to appropriate action. its the input to the action.
              this will be validated , is it only a dict or not.
        
        - actions:        
        all action should be in small case and for multiple word split by "_"
        
        * flow_start: {"flowFile" : "<<<flowfile>>>"}
        
        
        - example:
        { "action" : "flow_start" , "params" :  {"flowFile" : r"G:\pyworkspace\PyTasky\data\ptsFlows\arithmatic.flow"} }
        { "action" : "print" , "params" :  "this is sample text to print" }
        
        """
             
        r1 = type({}) == type(msg)
        if not r1: print("Queue msg is not valid, Not a dict") 
        
        r2 = r1 and "action" in msg.keys()
        if not r2: print("Queue msg is not valid, action missing!")
        
        r3 = r1 and "params" in msg.keys()
        if not r3: print("Queue msg is not valid, params missing!")
        
        r4 = r1 and msg["action"] in validActions
        if not r4: print(f"Queue msg is not valid, action:{msg['action']} given is invalid")
                
        return r1 and r2 and r3 and r4