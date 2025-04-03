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
from PyQt5.uic import loadUi
from NodeGraphQt import NodeGraph
from NodeGraphQt import BaseNode

from kQt import kQtTools
import kTools 
import json
from ptsLib import ptsQtFlowRunner

class PTSFlows(object):

    def __init__(self, parent):        
        self.tls = kTools.GetKTools()    
        self.qttls = kQtTools.KQTTools()
        self.PTS = parent
        self.parentUi = self.PTS.ui
        self.console = self.tls.console
        self.ndGraph = None

        self.ptsNodesPath = "G:/pyworkspace/PyTasky/ptsNodes"
        self.ptsFlowsPath = "G:/pyworkspace/PyTasky/ptsFlows"

        self.uiNodeCollection = {}
        self.coreNodeCollection = {}                        
        self.currentLoadedFlowName = None
        self.currentLoadedFlowFile = None
        self.isFlowEdited = 0
        self.lastNodeSelected = None
        self.isFlowRunning = False
        self.isFlowDebugging = False        

        self.doFlowInitializer()
        
        self.flowRunner = ptsQtFlowRunner.PTSQtFlowRunner()
        self.flowRunner.PTS = self.PTS
        self.flowRunner.PTS_UI = self.parentUi
        self.flowRunner.nodeExecutionInprogress.connect(self.doNodeExecutionInProgress)
        self.flowRunner.flowExecutionCompleted.connect(self.doFlowExecutionCompleted)
        self.flowRunner.flowExecutionStatus.connect(self.doFlowExecutionStatus)
        self.flowRunner.executeUINodeAction.connect(self.doExecuteUINodeExecution)
    
    def doExecuteUINodeExecution(self, modToExecute, request, callBackPassingResult):
        # print(modToExecute)
        # print(request)
        # print(callBackPassingResult)
        # uiFileName = "G:/pyworkspace/PyTasky/ptsUIs/dictEditor.ui"
        # winObj = QtWidgets.QDialog(self.PTS.ui)
        # uiObject = loadUi(uiFileName, winObj)
        #
        # result = winObj.exec_()  # Run the dialog and get return value (e.g., QDialog.Accepted/Rejected)
        # print("Window closed")
        # callBackPassingResult({"out":"myspl"})       
        res = modToExecute.ACTION(request)
        callBackPassingResult(res)
         
    
                        
    def doRunFlow(self):
        self.tls.info(f"Flow execution started, {self.getCurrentSession()}")
        if self.isSessionInProgress() and not self.isFlowRunning and not self.isFlowDebugging:
            self.PTS.logDisplayer.reset()
            self.flowRunner.debugMode = 0
            self.flowRunner.preSetup()
            self.flowRunner.start()
            self.isFlowRunning = 1
            self.isFlowDebugging = 0            
        else:
            self.tls.info("Unable to debug flow. Either no flow loaded, or already another flow running / debugging.")
        
    def doDebugFlow(self):
        self.tls.info("Debugging flow...")
        if self.isSessionInProgress() and not self.isFlowRunning and not self.isFlowDebugging:
            self.PTS.logDisplayer.reset()
            self.flowRunner.debugMode = 1
            self.flowRunner.preSetup()
            self.flowRunner.start()
            self.isFlowRunning = 0
            self.isFlowDebugging = 1            
        else:
            self.tls.info("Unable to debug flow. Either no flow load, or already another flow running / debugging")        

    def doDebugProceed(self):
        if self.isFlowDebugging:
            self.flowRunner.stepNext()

    def doDebugResume(self):
        if self.isFlowDebugging:
            self.flowRunner.resume()

    def doTerminateExecution(self):
        if self.isFlowDebugging or self.isFlowRunning:
            self.isFlowDebugging = 0
            self.isFlowRunning = 0
            self.flowRunner.stop()
                
    def doFlowInitializer(self):
        self.tls.info(f"Preparing node graph setup...")
        self.convertGenerateUINodeCollections()
  
        self.tls.info(f"Creating node graph ui objects...")
        self.ndGraph = NodeGraph()        
        self.ndGraph.register_nodes(list(self.uiNodeCollection.values()))        
        self.qttls.swapWidget(self.parentUi.lytCanvasHolder, self.parentUi.wgCanvas, self.ndGraph.widget)
    
        self.tls.info(f"Node graph signal connectors initializing.")
        self.ndGraph.node_selected.connect(self.doFlowNodeSelected)
        self.ndGraph.nodes_deleted.connect(self.doFlowEdited)
        self.ndGraph.port_connected.connect(self.doFlowEdited)
        self.ndGraph.port_disconnected.connect(self.doFlowEdited)
        self.ndGraph.widget.currentWidget().custom_data_dropped.connect(self.doFlowNodeDropped)
        self.ndGraph.widget.currentWidget().custom_key_pressed.connect(self.doFlowKeyPressed)    

    def doFlowKeyPressed(self, eve):
        if (eve.key() == QtCore.Qt.Key_Delete):
            
            selectedNodes = self.ndGraph.selected_nodes()
            selectedPipes = self.ndGraph.viewer().selected_pipes()
            
            for eachNode in selectedNodes:
                self.tls.debug(f"Deleting node... {eachNode.NODE_NAME}")
                self.ndGraph.remove_node(eachNode)
                self.tls.info(f"Done")                
                self.refreshFlow()
                
            if len(selectedPipes) == 1:
                selPipe = selectedPipes[0]
                #selPipe.delete() #TODO: After delete unable to recreate the flow from same src to dst
           
    def doFlowNodeSelected(self, nodeObj):
        newDict = {}
        newDict["Node Name"] = nodeObj.NODE_NAME 
        newDict["Node Script"] = "default"
        for eachKey in nodeObj.props.keys():
            newDict[eachKey] = nodeObj.props[eachKey]                
        self.qttls.createPropEditor(self.parentUi.propsHolder, newDict, self.doNodePropsUpdate, nodeObj)        
        self.doLoadNodeDesc(nodeObj)
        
    def doNodePropsUpdate(self, table, nodeObj):
        self.tls.debug(f"Props updating {nodeObj}")        
        updated_dict = {}
        for row in range(table.rowCount()):
            key = table.item(row, 0).text()  # Property name (column 1)
            value = table.item(row, 1).text()  # User-edited value (column 2)
            updated_dict[key] = value            
        nodeObj.props = updated_dict
        nodeObj.set_name(updated_dict['Node Name'])
        updated_dict['Node Name'] = nodeObj.name()
        nodeObj.NODE_NAME = nodeObj.name()
        self.doFlowNodeSelected(nodeObj)
        self.PTS.doSetTitle(isEdited=1)     
        self.PTS.coreToolBarActionRestricter(2)

    def doFlowEdited(self, *arg):
        self.isFlowEdited = 1
        self.PTS.doSetTitle(isEdited=1)
                
    def doLoadNodeDesc(self, nodeObj):        
        html = ""
        html += f"<b>Name: </b>{nodeObj.model.name}"
        html += "<br>"
        html += f"<b>Type: </b>{nodeObj.model.type_}"
        html += "<hr>"
        html += nodeObj.NODE_DESC                
        self.parentUi.infoView.setHtml(html)        

    def doFlowNodeDropped(self, event, pos):
        nodeItem = event.source().selectedItems()[0]
        nodeName = str(nodeItem.text(0))
        nodePath = str(nodeItem.data(0, QtCore.Qt.UserRole))
        x = pos.x()
        y = pos.y()
        if nodeName in self.uiNodeCollection:
            nodeObj = self.uiNodeCollection[nodeName]
            node = self.ndGraph.create_node(nodeObj.type_, pos=[x,y])
            self.tls.debug(f"Node added {node.NODE_NAME}")
            self.PTS.coreToolBarActionRestricter(1.5)
            self.isFlowEdited = 1
            self.PTS.doSetTitle(isEdited=1)     
        else:
            self.tls.error(f"Node {nodeName} is not valid. Not pre-loaded valid node.")
               
    def doSaveFlow(self):
        if self.isSessionInProgress():
            if self.currentFlowFileLoaded and self.currentLoadedFlowName and self.currentLoadedFlowFile:
                self.coreSaveFlow(self.currentFlowFileLoaded)
        else:
            self.doSaveFlowAs()
    
    def doSaveFlowAs(self):
        if self.isSessionInProgress():
            flowFile = self.qttls.getFileToSave('Select a folder to save flow as...', FileName=self.ptsFlowsPath, FileType='Flow Files (*.flow);;All Files (*)')
        else:
            flowFile = self.qttls.getFileToSave('Select a folder to save flow as...', FileName=self.ptsFlowsPath, FileType='Flow Files (*.flow);;All Files (*)')
        self.currentFlowFileLoaded = os.path.abspath(flowFile)
        self.coreSaveFlow(self.currentFlowFileLoaded)
           
    def doLoadFlow(self, flowName, flowFile):
        self.currentLoadedFlowName = flowName
        self.currentLoadedFlowFile = flowFile 
        self.coreLoadFlow(flowFile)

    def doFlowExecutionStatus(self, msg):
        self.tls.info(msg)

    def doFlowExecutionCompleted(self, param):
        self.PTS.logDisplayer.grabStdOut()
        self.tls.info(f"Flow execution completed, {self.getCurrentSession()}")
        if self.lastNodeSelected: self.lastNodeSelected.set_selected(False)
        self.PTS.logDisplayer.grabStdOut()
        self.isFlowRunning = 0
        self.isFlowDebugging = 0
        self.PTS.coreToolBarActionRestricter(2)
            
    def doNodeExecutionInProgress(self, nodeName):
        if self.lastNodeSelected:
            self.lastNodeSelected.set_selected(False)

        if nodeName:
            for each in self.ndGraph.model.nodes.keys():
                cur = self.ndGraph.model.nodes[each]
                if str(cur.NODE_NAME).strip() == str(nodeName).strip():
                    cur.set_selected(True)
                    self.lastNodeSelected = cur

    def openFlow(self):
        flowFile = self.qttls.getFile('Select a flow file to open...', self.ptsFlowsPath, 'Flow Files (*.flow);;All Files (*)')
        if flowFile:
            self.currentLoadedFlowName = os.path.basename(flowFile).lower().replace(".flow" , "")
            self.currentLoadedFlowFile = flowFile
            self.coreLoadFlow(flowFile)  
                           
    def coreSaveFlow(self, file_path):
        self.tls.debug(f"Save flow {file_path}")
        sessionInfo = self.ndGraph.serialize_session()
        sessionInfo['nodeProps'] = {}
        for eachNode in self.ndGraph.all_nodes():
            name = eachNode.NODE_NAME
            props = eachNode.props
            sessionInfo['nodeProps'][name] = props
        file_path = file_path.strip()
        def default(obj):
            if isinstance(obj, set):
                return list(obj)
            return obj
        with open(file_path, 'w') as file_out:
            json.dump(
                sessionInfo,
                file_out,
                indent=2,
                separators=(',', ':'),
                default=default
            )
        self.ndGraph._model.session = file_path        
        self.flowRunner.flowFile = file_path       

        self.currentLoadedFlowName = os.path.basename(file_path).lower().replace('.flow','')        
        self.currentFlowFileLoaded = os.path.abspath(file_path)   
        self.PTS.doSetTitle(isEdited=0)     
        self.isFlowEdited = 0
        
        self.PTS.coreToolBarActionRestricter(2)
        self.PTS.doLoadFlowTree()
                
    def coreLoadFlow(self, file_path):
        self.tls.debug(f"Load flow {file_path}")
        file_path = file_path.strip()
        if not os.path.isfile(file_path):
            raise IOError('file does not exist: {}'.format(file_path))
        try:
            with open(file_path) as data_file:
                fileContent = json.load(data_file)
        except Exception as e:
            fileContent = None
            self.tls.debug('Cannot read data from file.\n{}'.format(e))  
        if not fileContent: return                
        self.ndGraph.clear_session()
        self.ndGraph.deserialize_session(
            fileContent,
            clear_session=False,
            clear_undo_stack=True
        )
        self.ndGraph._model.session = file_path
        for eachNode in self.ndGraph.all_nodes():
            eachNode.props = fileContent['nodeProps'][eachNode.NODE_NAME]
            eachNode.props['Node Name'] = str(eachNode.NODE_NAME)
        self.ndGraph.session_changed.emit(file_path)        
        self.flowRunner.flowFile = file_path
        self.centerViewFlow()
        self.isFlowEdited = 0
        
        self.currentLoadedFlowName = os.path.basename(file_path).lower().replace('.flow','')        
        self.currentFlowFileLoaded = os.path.abspath(file_path)    
        self.PTS.doSetTitle(isEdited=0, flowName=self.currentLoadedFlowName)     


    def convertGenerateUINodeCollections(self):
        '''
        Read node folder and convert it to ui nodes:
        '''        
        self.uiNodeCollection = {}
        self.coreNodeCollection = {}

        advConfig = {}
        advConfig['silentIgnoredFileInfo'] = 1
        nodeModFiles = self.console.scanModuleFiles(self.ptsNodesPath, ignoreFileNameHasText=['__init__','Compiler','Template', 'Node', 'Generator','DummyC_o_r_e'], advConfig=advConfig)
        for nodeModName in nodeModFiles.keys():
            nodeModObj = nodeModFiles[nodeModName][0]
         
            modName = nodeModObj.__name__
            name = nodeModObj.NAME
            desc = nodeModObj.__doc__
            ips = nodeModObj.INPUTS if hasattr(nodeModObj, 'INPUTS') else []
            ops = nodeModObj.OUTPUTS if hasattr(nodeModObj, 'OUTPUTS') else []
            props = nodeModObj.PROPS if hasattr(nodeModObj, 'PROPS') else {}
            
            def generateDynamicConstructor(ips, ops, props):
                def dynamicConstructor(self):
                    super(self.__class__, self).__init__()
                    
                    if ips:
                        for each in ips:
                            if type(each) == type(()):
                                portName = each[0]
                                portMulti = each[1]
                            else:
                                portName = each
                                portMulti = 0
                            self.add_input(portName, multi_input=portMulti)
        
                    if ops:
                        for each in ops:
                            if type(each) == type(()):
                                portName = each[0]
                                portMulti = each[1]
                            else:
                                portName = each
                                portMulti = 0
                            self.add_output(portName, multi_output=portMulti)
                                        
                    self.props = props
                return dynamicConstructor
                
            attrb = {}
            attrb['NODE_NAME'] = name
            attrb['NODE_DESC'] = desc
            attrb['__init__'] = generateDynamicConstructor(ips, ops, props)
        
            genereatedUiNodeClass = type(nodeModName, (BaseNode,), attrb)
            if not nodeModName in self.uiNodeCollection.keys(): 
                self.uiNodeCollection[nodeModName] = genereatedUiNodeClass
            if not nodeModName in self.coreNodeCollection.keys(): 
                self.coreNodeCollection[nodeModName] = nodeModObj

    def centerViewFlow(self):
        allNodes = self.ndGraph.all_nodes()
        if allNodes : self.ndGraph.center_on(allNodes)        

    def clearFlow(self):
        self.ndGraph.clear_selection()
        self.ndGraph.clear_session()
        self.ndGraph.clear_undo_stack()
        
        self.currentLoadedFlowName = None
        self.currentLoadedFlowFile = None
        self.lastNodeSelected = None
        self.isFlowRunning = False
        self.isFlowDebugging = False        
                        
    def refreshFlow(self):
        self.tls.debug("Refreshing flow view")
        self.ndGraph.viewer().update()
        self.ndGraph.viewer().force_update()
        self.ndGraph.viewer().repaint()
        self.ndGraph.viewer()._update_scene()
        zoomVal = self.ndGraph._viewer.get_zoom()
        self.ndGraph._viewer.set_zoom(zoomVal+0.0000000000001)
        self.ndGraph._viewer.set_zoom(zoomVal)
        QApplication.processEvents()
    
    def isSessionInProgress(self):
        return self.ndGraph and self.ndGraph._model.session and self.currentLoadedFlowName and self.currentLoadedFlowName

    def getCurrentSession(self):
        return self.ndGraph._model.session
    
    
    