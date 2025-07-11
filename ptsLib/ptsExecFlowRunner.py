'''
Created on 21-Mar-2025

@author: kayma
'''

import os, sys, time, json
import code
import kTools
import kCodeExecuter

class PTSExecFlowRunner():

    def __init__(self, parent=None):
        super().__init__()
        self.PTS = parent
        self.tls = self.PTS.tls
        self.console = self.PTS.console
        self.ui = None
        self.initializer()

    def initializer(self):
        
        self.nodes = {}
        self.currentExecutionNodes = []
        self.rejectedNodes = []
        self.nodesOutputData = {}
    
    def preSetup(self):
        '''
            FLOW Reading
            ------------
            1. Read flow file
            2. Scan for all nodes in it for some flow specific props and infos
                2.1 Read node module for some static node infos like style1    /Default, Circle, Box
                2.2 Scan the i/p and o/p connections
                2.3 Based on it Determine node style2 - starter/executer/finisher/system
            3. Scan the connections
            4. Scan the node props

            FLOW Execution Preparation
            ---------------------------
            1. Clear
                    currentExecutionNodes,
                    rejectedNodes,
                    nodeOutputData,
               before starting the execution.
            2. Fetch all STARTER style2 nodes (and not system nodes) and add them to currentExecutionNodes

            3. Reverse the currentExecutionNodes

            4. System ready for execution now. (Read RUN for next step)

        '''
        self.tls.publishSignal("flowevent",  { "msg" : f"Scanning flow {self.flowFile}" })

        self.nodes = {}
        self.currentExecutionNodes = []
        self.rejectedNodes = []
        self.nodesOutputData = {}

        flowStrData = self.tls.getFileContent(self.flowFile)
        flowData = json.loads(flowStrData)
        
        #Scan Nodes - #!!!!!wont have special io port infos - nodeModule - rebuilt them with tags - will have file info!!!!!
        for each in flowData["nodes"]:
            id = each
            name = flowData["nodes"][each]['name']
            typ_ = flowData["nodes"][each]['type_']
            nodeModName = typ_.replace('nodeGraphQt.nodes.','')
            
            nodeModule = self.console.getModule(nodeModName)
            if not nodeModule: self.tls.errorAndExit(f"Missing module {nodeModName} for Node {name}")

            self.nodes[name] = {}
            self.nodes[name]['id'] = id
            self.nodes[name]['name'] = name
            self.nodes[name]['module'] = nodeModule
            self.nodes[name]['modname'] = nodeModName
            self.nodes[name]['tags'] = nodeModule.TAGS if hasattr(nodeModule, 'TAGS') else ['custom']
            if self.nodes[name]['tags'] == []: self.nodes[name]['tags'].append('custom')
            self.nodes[name]['splprops'] = nodeModule.SPLPROPS if hasattr(nodeModule, 'SPLPROPS') else {}
            _ips = nodeModule.INPUTS if hasattr(nodeModule, 'INPUTS') else []
            _ops = nodeModule.OUTPUTS if hasattr(nodeModule, 'OUTPUTS') else []
            self.nodes[name]['actualip'] = nodeModule.INPUTS if hasattr(nodeModule, 'INPUTS') else []
            self.nodes[name]['actualop'] = nodeModule.OUTPUTS if hasattr(nodeModule, 'OUTPUTS') else []
            if not _ips or _ips == "" or len(_ips): _ips = self._getDefaultInputPorts(nodeModule.TAGS)
            if not _ops or _ops == "" or len(_ops): _ops = self._getDefaultOutputPorts(nodeModule.TAGS)   
            self.nodes[name]['actualip'] = _ips
            self.nodes[name]['actualop'] = _ops                    
            self.nodes[name]['connectedip'] = {}
            self.nodes[name]['connectedop'] = {}
            self.nodes[name]['style1'] = self.getNodeStyle1(self.nodes[name]['splprops'])   #Default, Box, Circle
            self.nodes[name]['style2'] = self.getNodeStyle2(self.nodes[name]['actualip'], self.nodes[name]['actualop'])
            
            #Starter nodes should be added to mainnode list
            if not self._isItSystemNodeForNode(self.nodes[name]) and self._getNodeStyle2(self.nodes[name]) == "STARTER": 
                self.currentExecutionNodes.append(self.nodes[name])
            #Loop nodes should be added to rejected node collection
            #if self._isItSystemNode(self.nodes[name]['tags']) and self._isTagPresentInTags("Loop", self.nodes[name]['tags']): self.rejectedNodes.append(self.nodes[name])
            #self.tls.debug(f'Fetching node {name} info...')
            self.tls.publishSignal("flowevent", { "lst" : ["scan_node",name] })
                                    
        self.currentExecutionNodes.reverse()
        self.rejectedNodes.reverse()

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

        #self.tls.info('PreSetup Completed!')
        self.tls.publishSignal("flowevent", self.tls.publishSignal("flowevent", { "msg" : "PreSetup Completed!" }))
    
    def debugNodeOutput(self, item):
        label = item.text()        
        data = self.nodesOutputData[label]
        dataType = str(type(data))
        self.ui.txtData.setPlainText(f"{data} ( {dataType} )")
        
    def debugInfoUpdater(self, executeNodeList, nodeData, currentNode, other, completedNode):
        #pass
    
        if currentNode:
            self.ui.lblCurrentNode.setText(currentNode['name'])
    
        if executeNodeList!=None:
            self.ui.lstQueue.clear()
            for each in executeNodeList:
                self.ui.lstQueue.addItem(each['name'])

        if nodeData:
            self.ui.lstOutputs.clear()
            for each in nodeData:
                self.ui.lstOutputs.addItem(each)   
        
        if completedNode:
            self.ui.lstCompleted.addItem(completedNode['name'])
            
    def run(self):
        '''
        1. Clean the nodesOutputData = {}
        2. Run till currentExecutionNodes is empty.
            2.1    Pop 1 node from currentExecutionNodes
            2.2
        '''

        #---------------------------------------------------
        self.tls.info(f'-----Starting flow execution-----')
        self.tls.publishSignal("flowevent", { "msg": "Executing the flow..." })

        self.nodesOutputData = {}
        inputForNode = None
        currentNode = None

        self.cnt = 0
        while len(self.currentExecutionNodes):
            self.cnt = self.cnt + 1
            currentNode = self.currentExecutionNodes.pop()
            self.tls.publishSignal("flowevent", { "lst" : ["fetch_node", self.cnt, currentNode['name'] ] })

            #Is not IP Ready for proceeding and its not a starter node to ignore ip.
            if not self.isInputReadyForNode(currentNode):
                self.currentExecutionNodes.insert(0,currentNode)
                self.tls.publishSignal("flowevent", { "lst" : ["pushback", self.cnt, currentNode['name'] ] })               
                continue

            #Get the input data for running the node also to confirm all are ready for execution
            inputForNode = self.getInputForNode(currentNode)

            #Is it Custom Node and Not Sys Node
            if self._isItCustomNodeForNode(currentNode) and not self._isItSystemNodeForNode(currentNode):

                #Execute the node
                nodeOutput = self.executeNode(currentNode, inputForNode)

                #Store O/P
                self.addNodeOutputWithValue(currentNode, nodeOutput)

                #Fetch Next Node
                nextNodes = self.getNextNodes(currentNode)
                for eachNextNode in nextNodes:
                    if not eachNextNode in self.currentExecutionNodes and not eachNextNode in self.rejectedNodes:
                        self.currentExecutionNodes.append(eachNextNode)

            #If its Sys Node
            elif self._isItSystemNodeForNode(currentNode) and not self._isItCustomNodeForNode(currentNode):

                #Sys Node - Control
                if self._isTagPresentInTags("condition", currentNode['tags']):
                    conNodeName = currentNode['name']
                    conInpPortName = 'inp'
                    conTruePortName = 'True'
                    conFalsePortName = 'False'
                    conditionStr = str(currentNode['props']['condition']).strip()
                    conditionStatus = self.console.runCommand(conditionStr)
                    self.tls.publishSignal("flowevent", { "lst" : ["executing", self.cnt, currentNode['name'] ] })
                    if conditionStatus:
                        #Save Condition True Output for later use
                        self.addNodeOutput(conNodeName, conTruePortName, inputForNode[conInpPortName])

                        #Scan and Reject all false connections
                        nodesToReject = self.scanChainOfNodesFrom(currentNode, conFalsePortName)
                        for eachNodeToReject in nodesToReject:
                            if not eachNodeToReject in self.rejectedNodes:
                                self.rejectedNodes.append(eachNodeToReject)

                        #If any reject node present in mainlist remove it
                        for eachNodeToReject in nodesToReject:
                            if eachNodeToReject in self.currentExecutionNodes:
                                self.currentExecutionNodes.remove(eachNodeToReject)

                        nextNode = self.getNextNodeInNodeAndPort(currentNode, conTruePortName)
                        if not nextNode in self.currentExecutionNodes: 
                            self.currentExecutionNodes.append(nextNode)

                    else:
                        #Save Condition True Output for later use
                        self.addNodeOutput(conNodeName, conFalsePortName, inputForNode[conInpPortName])

                        #Scan and Reject all false connections
                        nodesToReject = self.scanChainOfNodesFrom(currentNode, conTruePortName)
                        for eachNodeToReject in nodesToReject:
                            if not eachNodeToReject in self.rejectedNodes:
                                self.rejectedNodes.append(eachNodeToReject)

                        #If any reject node present in mainlist remove it
                        for eachNodeToReject in nodesToReject:
                            if eachNodeToReject in self.currentExecutionNodes:
                                self.currentExecutionNodes.remove(eachNodeToReject)

                        nextNode = self.getNextNodeInNodeAndPort(currentNode, conFalsePortName)
                        if not nextNode in self.currentExecutionNodes: 
                            self.currentExecutionNodes.append(nextNode)

                #Sys Node - Loop
                if self._isTagPresentInTags("loop", currentNode['tags']):

                    ipPort = self.tls.lookUp.inputPortName
                    opPort = self.tls.lookUp.outputPortName
                    self.tls.publishSignal("flowevent", { "lst" : ["executing", self.cnt, currentNode['name'] ] })
                    loopCoreNode = self.getNextNodeInNodeAndPort(currentNode, opPort)
                    if loopCoreNode in self.rejectedNodes: continue

                    #Verify IP is proper list else stop
                    if type(inputForNode[ipPort]) == type([]):
                        lst = inputForNode[ipPort]
                    else:
                        lst = self.console.runCommand(inputForNode[ipPort])

                    if lst and type(lst)==type([]):
                        finalResponse = {}
                        #----------------------------
                        self.cnt = self.cnt + 1
                        stopLoopProcessing = False
                        for eachIP in lst:
                            #Push current ip outputbank so that loopCoreNode input use them
                            self.addNodeOutput(currentNode['name'], opPort, eachIP)
                            #Is not IP Ready for proceeding and its not a starter node to ignore ip.
                            if not self.isInputReadyForNode(loopCoreNode):
                                self.currentExecutionNodes.insert(0,currentNode)
                                self.tls.publishSignal("flowevent", { "lst" : ["pushback_loopnode", self.cnt, loopCoreNode['name'] ] })                                
                                stopLoopProcessing = True
                                break
                            #Get the input data for running the node also to confirm all are ready for execution
                            inputForLoopCoreNode = self.getInputForNode(loopCoreNode)
                            ret = self.executeNode(loopCoreNode, inputForLoopCoreNode)
                            finalResponse[str(eachIP)] = ret
                        #----------------------------
                        if stopLoopProcessing:
                            self.removeNodeOutputEntry(currentNode['name'], opPort)
                            continue

                        #Completed execution the loopCoreNode n times. results consolidated and ready.
                        #Now in current node exec list make sure loopCoreNode is not there . if presetn remove it. it might have added by some other path.
                        #So remove it and scan the next node of loopCoreNode and add to main list and continue the work.
                        #And for that next node it may need the inputdata. So input data is consolidate response of loop+loopCoreNodefor loopeditems  which we collected now.
                        #Store that in nodeOutput for next node to process.

                        #Remove loopCoreNode from main list
                        if loopCoreNode in self.currentExecutionNodes: 
                            self.currentExecutionNodes.remove(loopCoreNode)

                        self.addNodeOutputWithValue(loopCoreNode, finalResponse)

                        nextNodes = self.getNextNodes(loopCoreNode)

                        for eachNextNode in nextNodes:
                            if not eachNextNode in self.currentExecutionNodes and not eachNextNode in self.rejectedNodes:
                                self.currentExecutionNodes.append(eachNextNode)
            else:
                self.terminateFlow(f"Unknown node. Node should be either system or custom. But this is not valid: {currentNode['name']}")
            
        self.tls.publishSignal("flowevent", { "msg" : "Flow executed!" })
        
    def terminateFlow(self, msg="Flow Terminated"):
        self.tls.info(">>>>>> Terminating Flow <<<<<<<")
        self.tls.info(msg)

    def getNextNodeInNodeAndPort(self, node, portName):
        outputConnections = node['connectedop']
        for eachConnection in outputConnections[portName]:
            connectedNodeName = eachConnection[0]
            connectedNodePort = eachConnection[1]
            nextNode = self.getNodeByName(connectedNodeName)
        return nextNode

    def scanChainOfNodesFrom(self, node, portName):
        parentNode = self.getNextNodeInNodeAndPort(node, portName)
        allConnectedNodes = []
        def getConnectedNodesFor(inNode, allConnectedNodes):
            ##----
            allConnectedNodes.append(inNode)
            outputConnections = inNode['connectedop']
            for eachOutputPort in outputConnections.keys():
                for eachConnection in outputConnections[eachOutputPort]:
                    connectedNodeName = eachConnection[0]
                    connectedNodePort = eachConnection[1]
                    connectedNode = self.getNodeByName(connectedNodeName)
                    getConnectedNodesFor(connectedNode, allConnectedNodes)
            ##-----
            return allConnectedNodes
        getConnectedNodesFor(parentNode, allConnectedNodes)
        return allConnectedNodes

    def addNodeOutputWithValue(self, node, value):
        nodeName = node['name']
        ops = node['actualop']
        for eachOp in ops:
            opPortName = self.getOutputPortName(eachOp)
            self.addNodeOutput(nodeName, opPortName, value)

    def executeNode(self, node, request):
        modToExecute = None
        if 'Node Script' in node['props'] and node['props']['Node Script'] != 'default':
            nodescript = node['props']['Node Script']
            customModule = self.console.getModule(nodescript)
            customModule.NAME = node['name']
            customModule.PROPS = node['props']
            customModule.PTS = self.PTS if hasattr(self, 'PTS') else None
            if hasattr(customModule, 'ACTION'):
                self.tls.info(f"Custom module found: {customModule}")
                modToExecute = customModule
            else:
                msg = f"Custom module [{customModule}] has no fn named ACTION."
                self.tls.error(msg)
                self.terminateFlow(msg)
                output = {}
        else:
            defaultMod = node['module']
            defaultMod.NAME = node['name']
            defaultMod.PROPS = node['props']
            defaultMod.PTS = self.PTS if hasattr(self, 'PTS') else None
            modToExecute = defaultMod
        #--------------------------------------------------
        response = None
        try:
            #ui nodes are little tricky, they should exceute in main window only. not in thread
            #so we emit signal to them and they will execute. and call back our method.
            #that method will grab the result and set as output.
            #we will wait till the ui window get closed in node execution and will wait till we get a call back invoked.

            #Updating console so that users can use this variables to see the values
            self.tls.publishSignal("flowevent", { "lst" : ["executing", self.cnt, node['name']] })            
            self.updateExecutionLocalsWithNeededInput(request)
            if self._isTagPresentInTags('ui', node['tags']):
                def resultReadyFn(result):
                    nonlocal response
                    response = result
            else:
                if hasattr(modToExecute, "ACTION"):
                    response = modToExecute.ACTION(request)
                else:
                    self.tls.warn(f">> WARNING! No action available for {node['name']}")
                    response = None
        except Exception as e:
            print(e)
            self.terminateFlow(e)

        return response

    def updateExecutionLocalsWithNeededInput(self, inputForNode):
        '''
        Users can provide quick inputport name as variable and get the value. in executions
        '''
        #Updating all output data:
        self.console.updateLocals('data', self.nodesOutputData)

        #Each inp with its values.
        for eachKey in inputForNode:
            self.console.updateLocals(eachKey, inputForNode[eachKey])

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
        if self._getNodeStyle2(node) == 'STARTER': return input
        connectedIps = node['connectedip']
        for eachIPPort in connectedIps:
            connectionsInCurrntPort = connectedIps[eachIPPort]
            if self._isTagPresentInTags('multiip', node['tags']): input[eachIPPort] = []
            for eachConn in connectionsInCurrntPort:
                connectedNodeName = eachConn[0]
                connectedPortName = eachConn[1]
                data = self.getNodeOutput(connectedNodeName, connectedPortName)
                if self._isTagPresentInTags('multiip', node['tags']):
                    input[eachIPPort].append(data)
                else:
                    input[eachIPPort] = data
        return input

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

    def getNodeStyle1(self, nodeStyle):
        #Default or Box or Circle
        if nodeStyle:
            return nodeStyle
        else:
            return "Default"

    def getNodeStyle2(self, inputs, outputs):
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
        return f'{nodeName}-{portName}'

    def addNodeOutput(self, nodeName, portName, data):
        tag = self.getOutputTag(nodeName, portName)
        self.nodesOutputData[tag] = data

    def removeNodeOutputEntry(self, nodeName, portName):
        tag = self.getOutputTag(nodeName, portName)
        self.nodesOutputData.pop(tag,None)

    def getNodeOutput(self, nodeName, portName):
        tag = self.getOutputTag(nodeName, portName)
        return self.nodesOutputData[tag]

    def isNodeOutputAvailable(self, nodeName, portName):
        tag = self.getOutputTag(nodeName, portName)
        return tag in self.nodesOutputData

    def isInputReadyForNode(self, node):
        '''
        node['connectedip']
        {'in1': ('Variable', 'out'), 'in2': ('Variable 1', 'out')}
        '''
        if self._getNodeStyle2(node) == 'STARTER': return True
        connectedIps = node['connectedip']
        for eachIPPort in connectedIps:
            connectionsInCurrntPort = connectedIps[eachIPPort]
            for eachConn in connectionsInCurrntPort:
                connectedNodeName = eachConn[0]
                connectedPortName = eachConn[1]
                if not self.isNodeOutputAvailable(connectedNodeName, connectedPortName): return False
        return True

    def _getNodeStyle2(self, node):
        return node['style2']

    def _isItSystemNodeForNode(self, node):
        nodeTags = node['tags']
        return self._isItSystemNode(nodeTags)

    def _isItCustomNodeForNode(self, node):
        nodeTags = node['tags']
        return self._isTagPresentInTags("custom", nodeTags)

    def _isItSystemNode(self, nodeTags):
        return self._isTagPresentInTags('sys', nodeTags) and not self._isTagPresentInTags('custom', nodeTags)

    def _isTagPresentInTags(self, searchTag, tagList):
        return searchTag.strip().lower() in (s.strip().lower() for s in tagList)

    def _getDefaultOutputPorts(self, tagList):
        DefaultOutPortName = self.tls.lookUp.outputPortName
        if self._isTagPresentInTags('iponly', tagList):
            return []
        if self._isTagPresentInTags('shareop', tagList):
            return [(DefaultOutPortName,1)]
        return [DefaultOutPortName]

    def _getDefaultInputPorts(self, tagList):
        DefaultInputPortName = self.tls.lookUp.inputPortName
        if self._isTagPresentInTags('oponly', tagList):
            return []
        if self._isTagPresentInTags('multiip', tagList):
            return [(DefaultInputPortName,1)]
        return [DefaultInputPortName]

from .ptsNodeModuleScanner import PTSNodeModuleScanner
from . import PyTaskyLookUps 
from types import SimpleNamespace

def flowSignalsHndl(data):
    tls = kTools.KTools()
    lst = tls.getSafeDictValue(data, "lst", [])
    msg = tls.getSafeDictValue(data, "msg", None)
    if msg:
        tls.info(f"{msg}")
        
    if len(lst):
        act = lst[0]
        if act == "fetch_node":
            n = lst[1]
            node = lst[2]                                
            # print(f"{n}.Processing {node}... ",end='')
            # tls.info(f"{n} Pushing back [{node}], No input ready.")                
        if act == "pushback": 
            n = lst[1]
            node = lst[2]                                
            tls.info(f"{n}.Waiting {node}!")            
        if act == "pushback_loopnode": 
            n = lst[1]
            node = lst[2]                                
            tls.info(f"{n}.Waiting {node}!")                   
        if act == "executing": 
            n = lst[1]
            node = lst[2]                                
            tls.info(f"{n}.Executing {node}...")   
        if act == "scan_node":
            n = lst[1]
            tls.info(f"Scanning [{n}]...")   

if __name__ == "__main__":

    tls = kTools.KTools("KMXExec", PyTaskyLookUps, "G:/pyworkspace/PyTasky/pytasky_config.json")
    tls.share['console'] = kCodeExecuter.KCodeExecuter()
    
    tls.createNewSignalSetup("flowevent")
    tls.subscribeToSignal("flowevent", flowSignalsHndl)

    PTS = SimpleNamespace()
    PTS.tls = tls
    PTS.console = tls.share['console']

    PNS = PTSNodeModuleScanner()
    PNS.ptsNodesPath = "G:/pyworkspace/PyTasky/data/ptsNodes"
    PNS.scanNodeModuleFolder()  
        
    localRunner = PTSExecFlowRunner(PTS)
    localRunner.flowFile =  "G:/pyworkspace/PyTasky/data/ptsFlows/simple2-datatrans.flow" 
    localRunner.preSetup()
    localRunner.run()    
     
    