'''
Created on 21-Mar-2025

@author: kayma
'''

import os, sys, time, json
from PyQt5 import QtCore, QtWidgets
import code
import kTools
from PyQt5.uic import loadUi

class PTSQtFlowRunner(QtCore.QThread):
    """
    Only flow execution . No node mode refs.
    Read the flow file and execute
    """
    
    flowExecutionCompleted = QtCore.pyqtSignal(str)
    flowExecutionStatus = QtCore.pyqtSignal(str)
    nodeExecutionInprogress = QtCore.pyqtSignal(str)
    executeUINodeAction = QtCore.pyqtSignal(object, object, object)
    
    def __init__(self):        
        super().__init__()
        self.PTS = None            
        self.PTS_UI = None        
        self.paused = False  # Pause flag
        self.running = True  # Stop flag
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()

        # default_stdout = sys.__stdout__  # Use the original stdout
        # print("Thread is running", file=default_stdout)  # Safe print
        
        self.tls = kTools.GetKTools()    
        self.console = self.tls.console
                
        paths = []
        paths.append("G:/pyworkspace/PyTasky/ptsNodes")
        paths.append("G:/pyworkspace/PyTasky/ptsNodes/executer")
        paths.append("G:/pyworkspace/PyTasky/ptsNodes/finisher")
        paths.append("G:/pyworkspace/PyTasky/ptsNodes/starter")
        paths.append("G:/pyworkspace/PyTasky/ptsScripts")
        
        self.flowExecutionStatus.emit('Flow Started')
        self.console.cleanAndUpdateSysPaths(paths) 
        
        self.flowFile = None
        
        self.debugMode = 0            

    def preSetup(self):
        self.tls.info(f'Scanning flow {self.flowFile}')
        
        self.nodes = {}
        self.starterNodes = []        
        
        self.currentExecutionNodes = []
        self.nodesOutputData = {}        

        flowStrData = self.tls.getFileContent(self.flowFile)
        flowData = json.loads(flowStrData)
                        
        #Scan Nodes
        for each in flowData["nodes"]:
            id = each
            name = flowData["nodes"][each]['name']
            typ_ = flowData["nodes"][each]['type_']
            nodeModName = typ_.replace('nodeGraphQt.nodes.','').replace('Node','Core')
            
            nodeModule = self.console.getModule(nodeModName)
            if not nodeModule: self.tls.errorAndExit(f"Missing module {nodeModName} for Node {name}")
            
            self.nodes[name] = {}
            self.nodes[name]['id'] = id
            self.nodes[name]['name'] = name
            self.nodes[name]['modname'] = nodeModName
            self.nodes[name]['module'] = nodeModule
            self.nodes[name]['actualip'] = nodeModule.INPUTS if hasattr(nodeModule, 'INPUTS') else []
            self.nodes[name]['actualop'] = nodeModule.OUTPUTS if hasattr(nodeModule, 'OUTPUTS') else []
            self.nodes[name]['connectedip'] = {}
            self.nodes[name]['connectedop'] = {}
            self.nodes[name]['type'] = self.determineNodeType(self.nodes[name]['actualip'], self.nodes[name]['actualop'])
            if self.nodes[name]['type'] == "STARTER": self.starterNodes.append(self.nodes[name])

            self.tls.debug(f'Fetching node {name} info...')

        #Scan Connection
        if "connections" in flowData:
            for each in flowData["connections"]:
                fromNodeId = each['out'][0]
                fromPortName = each['out'][1]
                fromNodeName = self.getNodeById(fromNodeId)['name']   
                toNodeId = each['in'][0]
                toNodeName = self.getNodeById(toNodeId)['name']   
                toPortName = each['in'][1]
                if not fromPortName in self.nodes[fromNodeName]['connectedop'].keys():  
                    self.nodes[fromNodeName]['connectedop'][fromPortName]=[]
                if not toPortName in self.nodes[toNodeName]['connectedip'].keys():  
                    self.nodes[toNodeName]['connectedip'][toPortName]=[]
                self.nodes[fromNodeName]['connectedop'][fromPortName].append((toNodeName, toPortName))
                self.nodes[toNodeName]['connectedip'][toPortName].append((fromNodeName, fromPortName))
    
                self.tls.debug(f'Fetching connection info {fromNodeName}.{fromPortName} -> {toNodeName}.{toPortName}')
            
        #Scan Props
        if "nodeProps" in flowData:
            for each in flowData["nodeProps"]:
                nd = flowData["nodeProps"][each]
                tmp_ = nd.pop("Node Name") if "Node Name" in nd else ''            
                self.nodes[each]['props'] = nd
                self.nodes[each]['props']['Node Script'] = nd['Node Script'] if 'Node Script' in nd else 'default'
                self.tls.debug(f'Fetching props info {nd}')
            
        self.tls.info('PreSetup Completed!')

    def run(self):
        #---------------------------------------------------
        self.tls.info(f'-----Starting flow execution-----')
        self.flowExecutionStatus.emit(f'Executing the flow...')

        self.currentExecutionNodes = []
        self.nodeInputs = {}          
        
        self.currentExecutionNodes = self.starterNodes        
        self.currentExecutionNodes.reverse()
        cnt = 0        
        while len(self.currentExecutionNodes):                       
            cnt = cnt + 1
            ttl = len(self.currentExecutionNodes)                  
            
            currentNode = self.currentExecutionNodes.pop()
            self.flowExecutionStatus.emit(f'{cnt}/{ttl} Node to be processed.... {currentNode["name"]}')
            self.nodeExecutionInprogress.emit(f'{currentNode["name"]}')
            
            #-------Thread Hold and Resume OnDemand - For Debugging------
            if self.debugMode: self.pause()
            self.mutex.lock()
            while self.paused:
                #"Flow waiting for debugging
                self.condition.wait(self.mutex)
            self.mutex.unlock()       
            if not self.running: break
            #-------Thread Hold and Resume OnDemand - For Debugging------            
                         
            #Step 1: Is IP Ready for Processing this Node
            if not self.isInputReadyForNode(currentNode):
                self.currentExecutionNodes.insert(0,currentNode)
                self.flowExecutionStatus.emit(f"{cnt}/{ttl} PushBack node, Input not yet ready for this.... {currentNode['name']}")
                continue
            
            inputForNode = self.getInputForNode(currentNode)
                        
            #Step 2:   Execute Core
            nodeOutput = self.executeNode(currentNode, inputForNode)
            
            #Step 3:   Set OP
            status = self.verifyAndSaveNodeOutput(currentNode, nodeOutput)
            
            #Step 4:   Fetch Next Node            
            nextNodes = self.getNextNodes(currentNode)
            for eachNextNode in nextNodes:
                if not eachNextNode in self.currentExecutionNodes:
                    self.currentExecutionNodes.append(eachNextNode)
                    
        self.flowExecutionCompleted.emit(None)
        self.flowExecutionStatus.emit(f'-----Flow execution completed successfully!-----')
        
    def pause(self):
        """Pause execution"""
        self.paused = True

    def stepNext(self):
        """temp step next execution"""
        self.paused = False
        self.condition.wakeAll()  # Resume thread execution

    def resume(self):
        """Resume execution"""
        self.debugMode = False
        self.stepNext()

    def stop(self):
        """Stop execution"""
        self.running = False
        self.resume()  # Ensure thread exits        
            
    def verifyAndSaveNodeOutput(self, node, output):
        #{'id': '0x180c937c250', 'name': 'Variable', 'modname': 'VariableCore', 'module': <module 'VariableCore' from 'G:\\pyworkspace\\PyTasky\\ptsNodes\\starter\\VariableCore.py'>, 'actualip': [], 'actualop': [('out', 1)], 'connectedip': {}, 'connectedop': {'out': ('Mathers', 'in1')}, 'type': 'STARTER', 'props': {'Value': 'Some Value'}}        
        nodeName = node['name']
        ops = node['actualop']
        for eachOp in ops:
            opPortName = self.getOutputPortName(eachOp)
            #Expect it output
            if not opPortName in output.keys():
                print(f"Not valid output. Output from node {node[name]} is missing the info for port {opPortName}.")
                return False
            else:
                self.addNodeOutput(nodeName, opPortName, output[opPortName])
                return True
            
    def executeNode(self, node, request):
        modToExecute = None
       
        if 'Node Script' in node['props'] and node['props']['Node Script'] != 'default':            
            nodescript = node['props']['Node Script']
            self.tls.debug(f"Executing custom node script for {node['name']} - {nodescript}")
            customModule = self.console.getModule(nodescript)
            customModule.NAME = node['name']
            customModule.PROPS = node['props']
            if hasattr(customModule, 'ACTION'):
                modToExecute = customModule
            else:
                self.tls.error(f"Custom module [ {customModule}] has no fn named ACTION.")
                output = {}
        else:
            defaultMod = node['module']
            defaultMod.NAME = node['name']
            defaultMod.PROPS = node['props']
            defaultMod.PTS = self.PTS
            modToExecute = defaultMod            

        
        #--------------------------------------------------
        
        response = {}      
        try:
            #ui nodes are little tricky, they should exceute in main window only. not in thread
            #so we emit signal to them and they will execute. and call back our method. 
            #that method will grab the result and set as output. 
            #we will wait till the ui window get closed in node execution and will wait till we get a call back invoked.
            if "ISUI" in dir(modToExecute) and modToExecute.ISUI:
                def resultReadyFn(result):
                    nonlocal response
                    response.update(result)
                    loop.quit()
                loop = QtCore.QEventLoop()
                self.executeUINodeAction.emit(modToExecute, request, resultReadyFn)
                loop.exec_()
            else:                        
                response = modToExecute.ACTION(request)
        except Exception as e:
            print("-------Error executing node-----")
            print(e)
            print("-------Error executing node-----")
        
        return response
            
    def getNextNodes(self, node):
        nextNodes = []
        outputConnections = node['connectedop']
        for eachOutputPort in outputConnections.keys():
            for eachConnection in outputConnections[eachOutputPort]:
                connectedNodeName = eachConnection[0]
                connectedNodePort = eachConnection[1]
                nextNodes.append( self.getNodeByName(connectedNodeName) )
        return nextNodes
            
    def getInputForNode(self, node):
        '''
        Get Consolidated Inputs for executing the node
        '''
        input = {}
        if node['type'] == 'STARTER': return input
        nodeName = node['name']
        connectedIps = node['connectedip']

        for eachIPPort in connectedIps:
            connectionsInCurrntPort = connectedIps[eachIPPort]
            for eachConn in connectionsInCurrntPort:
                connectedNodeName = eachConn[0]
                connectedPortName = eachConn[1]
                data = self.getNodeOutput(connectedNodeName, connectedPortName)        
                input[eachIPPort] = data
        
        return input
        
    def isInputReadyForNode(self, node):
        '''
        node['connectedip']
        {'in1': ('Variable', 'out'), 'in2': ('Variable 1', 'out')}
        '''

        if node['type'] == 'STARTER': return True
        connectedIps = node['connectedip']
        for eachIPPort in connectedIps:
            connectionsInCurrntPort = connectedIps[eachIPPort]
            for eachConn in connectionsInCurrntPort:
                connectedNodeName = eachConn[0]
                connectedPortName = eachConn[1]
                if not self.isNodeOutputAvailable(connectedNodeName, connectedPortName): return False
        return True
                        
    def getOutputPortName(self, opObj):
        if type(opObj) == type(()):
            return opObj[0] 
        if type(opObj) == type(""):
            return str(opObj)

    def getInputPortName(self, ipObj):
        if type(ipObj) == type(()):
            return ipObj[0] 
        if type(ipObj) == type(""):
            return str(ipObj)
                
    def getNodeModuleForNode(self, node):
        if node["module"]: return node["module"] 
                    
    def getNodeById(self, nodeId=""):
        for each in self.nodes:
            if self.nodes[each]['id'] == nodeId:
                return self.nodes[each]        

    def getNodeByName(self, nodeName = ""):
        for each in self.nodes:
            if self.nodes[each]['name'] == nodeName:
                return self.nodes[each]
        return None
    
    def determineNodeType(self, inputs, outputs):
        if len(inputs) == 0 and len(outputs) > 0:
            return "STARTER"
        elif len(inputs) > 0 and len(outputs) == 0:
            return "FINISHER"
        elif len(inputs) > 0 and len(outputs) > 0:
            return "EXECUTER"
        elif len(inputs) == 0 and len(outputs) == 0:
            return "INVALID"

    #Node Outputs
    def cleanNodeOutputs(self):
        self.nodesOutputData = {}

    def getOutputTag(self, nodeName, portName):
        return f'[{nodeName}][{portName}]'          
        
    def addNodeOutput(self, nodeName, portName, data):
        tag = self.getOutputTag(nodeName, portName)
        self.nodesOutputData[tag] = data
    
    def getNodeOutput(self, nodeName, portName):
        tag = self.getOutputTag(nodeName, portName)
        return self.nodesOutputData[tag]
    
    def isNodeOutputAvailable(self, nodeName, portName):
        tag = self.getOutputTag(nodeName, portName)
        return tag in self.nodesOutputData
        
if __name__ == "__main__":

    d = """
import ConcaterCore
print(ConcaterCore.action)
    """

    t = PTSFlowRunner(None)    
    t.executeFlow("G:/pyworkspace/PyTasky/TEST2.FLOW")
    
    #t.console.runCode(d)
    