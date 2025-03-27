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
from ptsLib import ptsQtFlowRunner

class PTSFlows(object):

    def __init__(self, parent):        
        self.tls = kTools.GetKTools()    
        self.qttls = kQtTools.KQTTools()
        self.PTS = parent
        self.parentUi = self.PTS.ui
        self.console = self.tls.console

        self.ptsNodesPath = "G:/pyworkspace/PyTasky/ptsNodes"
        self.ptsFlowsPath = "G:/pyworkspace/PyTasky/ptsFlows"

        self.doFlowInitializer()
        
        self.currentLoadedFlowName = None
        self.currentLoadedFlowFile = None
        self.lastNodeSelected = None
        self.isFlowRunning = False
        self.isFlowDebugging = False
        
        self.flowRunner = ptsQtFlowRunner.PTSQtFlowRunner()
        self.flowRunner.flowExecutionCompleted.connect(self.flowExecutionCompleted)
        self.flowRunner.flowupdate.connect(self.flowStatusChange)
        self.flowRunner.nodeinprogress.connect(self.nodePickedForExecution)
    
    def flowExecutionCompleted(self, param):
        self.tls.info("Flow execution completed")
        if self.lastNodeSelected: self.lastNodeSelected.set_selected(False)
        self.PTS.logDisplayer.grabStdOut()
        self.isFlowRunning = 0
        self.isFlowDebugging = 0
        self.PTS.coreToolBarActionRestricter(2)
        
        
    def doRunFlow(self):
        self.tls.info("Running flow...")
        if self.currentLoadedFlowName and not self.isFlowRunning and not self.isFlowDebugging:
            self.PTS.logDisplayer.reset()
            self.flowRunner.debugMode = 0
            self.flowRunner.preSetup()
            self.flowRunner.start()
            self.isFlowRunning = 1
            self.isFlowDebugging = 0            
        else:
            self.tls.info("Unable to debug flow. Either no flow load, or already another flow running / debugging")
        
    def doDebugFlow(self):
        self.tls.info("Debugging flow...")
        if self.currentLoadedFlowName and not self.isFlowRunning and not self.isFlowDebugging:
            self.PTS.logDisplayer.reset()
            self.flowRunner.debugMode = 1
            self.flowRunner.preSetup()
            self.flowRunner.start()
            self.isFlowRunning = 0
            self.isFlowDebugging = 1            
        else:
            self.tls.info("Unable to debug flow. Either no flow load, or already another flow running / debugging")        
        #self.flowRunner.resume()
    
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
                    
    def nodePickedForExecution(self, nodeName):
        self.doNodeSelect(nodeName)
            
    def flowStatusChange(self, msg):
        self.tls.info(msg)
        if "Flow execution completed successfully" in msg:            
            self.PTS.logDisplayer.grabStdOut()
            self.tls.info("all done")
    
    def doNodeSelect(self, nodeName):
        if self.lastNodeSelected:
            self.lastNodeSelected.set_selected(False)

        if nodeName:
            for each in self.ndGraph.model.nodes.keys():
                c = self.ndGraph.model.nodes[each]
                if str(c.NODE_NAME).strip() == str(nodeName).strip():
                    c.set_selected(True)
                    self.lastNodeSelected = c
                
    def doFlowInitializer(self):
        self.nodeModeCollection = {}

        self.tls.info(f"Preparing node graph setup...")
        
        self.tls.info(f"Preload the valid node from local collection...")
        nodeCores = self.tls.getFileList(self.ptsNodesPath, ".py", ["Node"], ["Core","Template","NodeCoreCompiler"])
        for file in nodeCores:
            fileName = os.path.basename(file).replace(".py","")
            if fileName in list(self.nodeModeCollection.keys()): 
                self.tls.debug(f"{file} can't be loaded, Might be duplicate.") 
            else:
                modImported = self.console.loadModule(fileName, file)
                mod = getattr(modImported, fileName)
                self.nodeModeCollection[fileName] = mod       

        self.tls.info(f"Creating node graph ui objects...")
        self.ndGraph = NodeGraph()        
        self.ndGraph.register_nodes(list(self.nodeModeCollection.values()))        
        self.qttls.swapWidget(self.parentUi.lytCanvasHolder, self.parentUi.wgCanvas, self.ndGraph.widget)
    
        self.tls.info(f"Node graph signal connectors initializing.")
        self.ndGraph.node_selected.connect(self.doFlowNodeSelected)
        self.ndGraph.widget.currentWidget().custom_data_dropped.connect(self.doFlowNodeDropped)
        self.ndGraph.widget.currentWidget().custom_key_pressed.connect(self.doFlowKeyPressed)    

                       
    def doFlowKeyPressed(self, eve):
        #self.ndGraph.viewer().selected_items()
        if (eve.key() == QtCore.Qt.Key_Delete):
            
            selectedNodes = self.ndGraph.selected_nodes()
            selectedPipes = self.ndGraph.viewer().selected_pipes()
            
            for eachNode in selectedNodes:
                self.tls.debug(f"Deleting... {eachNode.NODE_NAME}")
                self.ndGraph.remove_node(eachNode)
                self.tls.info(f"Done")                
                self.refreshFlow()
                
            if len(selectedPipes) == 1:
                selPipe = selectedPipes[0]
                #selPipe.delete() #TODO: After delete unable to recreate the flow from same src to dst
           
    def doFlowNodeSelected(self, nodeObj):
        self.tls.debug(f"Node Selected {nodeObj}")
        newDict = {}
        newDict["Node Name"] = nodeObj.NODE_NAME 
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
        if nodeName in self.nodeModeCollection:
            nodeObj = self.nodeModeCollection[nodeName]
            node = self.ndGraph.create_node(nodeObj.type_, pos=[x,y])
            self.tls.debug(f"Node added {node.NODE_NAME}")
        else:
            self.tls.error(f"Node {nodeName} is not valid. Not pre-loaded valid node.")

    def centerViewFlows(self):
        allNodes = self.ndGraph.all_nodes()
        if allNodes : self.ndGraph.center_on(allNodes)        

    def clearFlow(self):
        self.ndGraph.clear_selection()
        self.ndGraph.clear_session()
        self.ndGraph.clear_undo_stack()
        #self.ndGraph.close()        
        #self.refreshFlow()
        self.nodeModeCollection = {}
        self.currentLoadedFlowName = None
        self.currentLoadedFlowFile = None
        self.lastNodeSelected = None
                        
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

    def doSaveFlow(self):
        if self.currentLoadedFlowName:
            flowName = self.qttls.showInputBox('Save flow', "Save the flow with name", self.currentLoadedFlowName)
        #self.ptsFlowsPath + flowName + '.flow'
        self.currentFlowFileLoaded = os.path.join(self.ptsFlowsPath, flowName, '.flow')
        self.coreSaveFlow(self.currentFlowFileLoaded)
        
    def doSaveFlowAs(self):
        flowName = self.qttls.showInputBox('Save flow', "Save the flow with name", self.currentLoadedFlowName + "Copy")
        self.currentFlowFileLoaded = os.path.join(self.ptsFlowsPath, flowName, '.flow')
        self.coreSaveFlow(self.currentFlowFileLoaded)
    
    def openFlow(self):
        flowFile = self.qttls.getFile('Select a flow file to open...', 'default.flow', 'Flow Files (*.flow);;All Files (*)')
        if flowFile:
            self.currentLoadedFlowName = os.path.basename(flowFile).lower().replace(".flow" , "")
            self.currentLoadedFlowFile = flowFile
            self.coreLoadFlow(flowFile)        
        
    def doLoadFlow(self, flowName, flowFile):
        self.currentLoadedFlowName = flowName
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
        #self.ndGraph.auto_layout_nodes() 
        self.centerViewFlows()
        
        self.flowRunner.flowFile = file_path
