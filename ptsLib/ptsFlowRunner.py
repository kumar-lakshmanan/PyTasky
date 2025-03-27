'''
Created on 21-Mar-2025

@author: kayma
'''

import os, sys, time, json
import code
import kTools

class PTSFlowRunner(object):
    """
    Only flow execution . No node mode refs.
    Read the flow file and execute
    """
    
    def __init__(self, parent):        
        self.tls = kTools.GetKTools()    
        self.console = self.tls.console
                
        paths = []
        paths.append("G:/pyworkspace/PyTasky/ptsNodes")
        paths.append("G:/pyworkspace/PyTasky/ptsNodes/executer")
        paths.append("G:/pyworkspace/PyTasky/ptsNodes/finisher")
        paths.append("G:/pyworkspace/PyTasky/ptsNodes/starter")
        paths.append("G:/pyworkspace/PyTasky/ptsScripts")

        self.console.cleanAndUpdateSysPaths(paths)  
        
    def executeFlow(self, flowFile = "TEST2.FLOW"):
        self.tls.info(f'Scanning flow... {flowFile}')
        
        self.nodes = {}
        self.starterNodes = []        
        
        self.currentExecutionNodes = []
        self.nodesOutputData = {}        
        
        flowStrData = self.tls.getFileContent(flowFile)
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
        for each in flowData["connections"]:
            fromNodeId = each['out'][0]
            fromPortName = each['out'][1]
            fromNodeName = self.getNodeById(fromNodeId)['name']   
            toNodeId = each['in'][0]
            toNodeName = self.getNodeById(toNodeId)['name']   
            toPortName = each['in'][1]  
            self.nodes[fromNodeName]['connectedop'][fromPortName] = (toNodeName, toPortName)
            self.nodes[toNodeName]['connectedip'][toPortName] = (fromNodeName, fromPortName)
            self.tls.debug(f'Fetching connection info {fromNodeName}.{fromPortName} -> {toNodeName}.{toPortName}')
            
        #Scan Props
        for each in flowData["nodeProps"]:
            nd = flowData["nodeProps"][each]
            tmp_ = nd.pop("Node Name") if "Node Name" in nd else ''
            self.nodes[each]['props'] = nd
            self.tls.debug(f'Fetching props info {nd}')

        #---------------------------------------------------
        self.tls.info(f'-----Data prepared, Flow Ready for execution-----')
        self.tls.debug(f'Executing the flow...')

        self.currentExecutionNodes = []
        self.nodeInputs = {}          
        
        self.currentExecutionNodes = self.starterNodes        
        self.currentExecutionNodes.reverse()
                
        while len(self.currentExecutionNodes):
            currentNode = self.currentExecutionNodes.pop()
            self.tls.debug(f'Processing node.... {currentNode["name"]}')
             
            #Step 1: Is IP Ready for Processing this Node
            if not self.isInputReadyForNode(currentNode):
                self.currentExecutionNodes.insert(0,currentNode)
                self.tls.debug('PushBack node, Input not yet ready.... ', currentNode['name'])
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
        mod = node['module']
        mod.PROPS = node['props']
        output = mod.action(request)
        return output
            
    def getNextNodes(self, node):
        nextNodes = []
        outputConnections = node['connectedop']
        for eachOutputPort in outputConnections.keys():
            nextNodeName = outputConnections[eachOutputPort][0]
            nextNodes.append( self.getNodeByName(nextNodeName) )
        return nextNodes
            
    def getInputForNode(self, node):
        input = {}
        if node['type'] == 'STARTER': return input
        nodeName = node['name']
        inps = node['connectedip']
        for eachInp in inps:
            currentPortName = eachInp
            srcNode = inps[currentPortName][0]
            srcNodePort = inps[currentPortName][1]
            currentPortData = self.getNodeOutput(srcNode, srcNodePort)
            input[currentPortName] = currentPortData
        return input
        
    def isInputReadyForNode(self, node):
        '''
        node['connectedip']
        {'in1': ('Variable', 'out'), 'in2': ('Variable 1', 'out')}
        '''

        if node['type'] == 'STARTER': return True
        connectedIp = node['connectedip']
        connections = list(connectedIp.values())
        for eachConnection in connections:
            if not self.isNodeOutputAvailable(eachConnection[0], eachConnection[1]):
                return False
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
    