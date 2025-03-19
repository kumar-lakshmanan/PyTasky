'''
Created on 12-Mar-2025

@author: kayma
'''
import os,sys
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5.Qt import QLineEdit
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt,)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget,)

from NodeGraphQt import NodeGraph

from kQt import kQtTools
import kTools 
import json

class PTSFlowExecuter(object):

    def __init__(self, parent):
        
        self.tls = kTools.GetKTools()    
        self.qttls = kQtTools.KQTTools()
        self.flow = parent
        self.PTS = self.flow.PTS
        self.parentUi = self.PTS.ui
        self.console = self.PTS.console
        
        self.commonDataCollector = {} #To hold all output data
        
        # self.debugging = 0
        # self.debugWait = 0
    
    def getDataId(self, nodeName, portName):
        return f"[{nodeName}][{portName}]"
    
    def getCommonData(self, dataId):
        return self.commonDataCollector[dataId] if dataId in self.commonDataCollector else None
    
    def setCommonData(self, dataId, data):
        if not dataId in self.commonDataCollector:
            self.commonDataCollector[dataId] = data
    
    def getRequestData(self, node):
        """
            For given node, fetch all incoming request clean data by reading all node ports
            and fetching the data from commonDataCollector        
        """
        reqData = {}
        ipPorts = node.inputs()
        for ipName in ipPorts:
            reqData[ipName] = None
            ipPort = ipPorts[ipName]            
            connectedPorts = ipPort.connected_ports()
            if len(connectedPorts) == 1:
                connectedPort = connectedPorts[0]
                cPortName = connectedPort.name()
                cNodeName = connectedPort.node().name()
                dataId = self.getDataId(cNodeName, cPortName)
                cdata = self.getCommonData(dataId)
                if cdata:
                    reqData[ipName] = cdata
                else:
                    self.tls.warn("No data available")               
            else:
                self.tls.warn("Multiple input not ready")
        return reqData

    def processResponseData(self, node, respData):
        """
            Return data will be verified whtr its in valid format.
            Like . for that node... these many output port there.. so return should 
            have those portname and its value (ouput) so that it can be saved in common data lib.
            and will be used for later use by other node.
        """
        isAllGood = False
        opPorts = node.outputs()
        if len(opPorts)==0: isAllGood = True
        for opPortName in opPorts:
            if not opPortName in respData:
                self.tls.error(f"Response from the node {node.NODE_NAME} is invalid. No data for {opPortName} found.")                
            else:
                dataId = self.getDataId(node.NODE_NAME, opPortName)
                self.setCommonData(dataId, respData[opPortName])
                isAllGood = True        
        return isAllGood
        
    def getNodeCat(self, node):
        #Starter, Executer, Finisher
        nodeCat = 'UNKNOWN'
        ipPorts = node.input_ports()
        opPorts = node.output_ports()
        if len(opPorts)>0 and len(ipPorts)==0:
            nodeCat = 'STARTER'
        if len(opPorts)==0 and len(ipPorts)>0:
            nodeCat = 'FINISHER'
        if len(opPorts)>0 and len(ipPorts)>0:
            nodeCat = 'EXECUTER'
        return nodeCat
    
    def isInputReadyForNode(self, node):
        if node in self.starterNodes:
            return True
        else:
            inpData = self.getRequestData(node)
            for each in inpData.keys():
                if inpData[each] == None: return False
            return True

    def getNextNodes(self, node):
        nxtNodes = []
        if node in self.finisherNodes: return nxtNodes
        opPortsDict = dict(node.connected_output_nodes())
        for portObj in opPortsDict.keys():
            for eachTargetNodes in opPortsDict[portObj]:
                nxtNodes.append(eachTargetNodes)
        return nxtNodes    

    def analysisAndPrepareNodes(self):
        self.tls.info(f"Analaysing nodes... ")

        self.commonDataCollector = {}       #To hold all output data
        self.currentProcessing = []                          

        self.starterNodes = []
        self.executerNodes = []
        self.finisherNodes = []
                
        for eachNode in self.flow.ndGraph.all_nodes():
            nodeName = eachNode.NODE_NAME
            nodeCat = self.getNodeCat(eachNode)             #Starter, Executer, Finisher
            if eachNode in self.starterNodes or eachNode in self.executerNodes or eachNode in self.finisherNodes:  
                self.tls.error(f"Duplicate node {nodeName}, Already node available")
                continue;
            if nodeCat == "STARTER":
                self.starterNodes.append(eachNode)
            if nodeCat == "EXECUTER":
                self.executerNodes.append(eachNode)
            if nodeCat == "FINISHER":
                self.finisherNodes.append(eachNode)

                                    
    def doExecuteCurrentFlow(self):
        self.tls.info(f"Flow started... ")
                
        self.analysisAndPrepareNodes()
              
        self.starterNodes.reverse()
        self.currentProcessing = self.starterNodes
        
        self.doCoreExecution()
        
        # self.debugging = 1
        # self.debugWait = 0
        #
        # class Worker(QtCore.QRunnable):
        #     def __init__(self, parent):
        #         super().__init__()
        #         self.parent = parent
        #
        #     def run(self):
        #         self.parent.doCoreExecution()  # Call function in thread
        #         self.parent.tls.info(f"Flow completed.")
        #
        # self.worker = Worker(self)
        # QtCore.QThreadPool.globalInstance().start(self.worker)        
                                    
    def doCoreExecution(self):
        
        while (len(self.currentProcessing)>0):
            QApplication.processEvents()
            # if self.debugging and self.debugWait:
            #     if nowNode: nowNode.set_selected(False)                
            #     continue
            nowNode = self.currentProcessing.pop()
            nowNode.set_selected(True)
            if not self.isInputReadyForNode(nowNode):
                self.currentProcessing.append(nowNode)
            else:
                inpData = self.getRequestData(nowNode)
                print('-----------')                
                respData = nowNode.nodeAction(inpData)
                print('-----------')
                if self.processResponseData(nowNode, respData):
                    nextNodes = self.getNextNodes(nowNode)
                    for eachNextNodes in nextNodes:
                        if not eachNextNodes in self.currentProcessing: self.currentProcessing.insert(0,eachNextNodes)                        
                else:
                    self.tls.error(f"Response invalid for {inpData} : {respData}")
                    break;
            nowNode.set_selected(False)
            # self.debugWait = 1          
