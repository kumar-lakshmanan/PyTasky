'''
Created on 12-Mar-2025

@author: kayma
'''
import os, sys
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
from ptsLib import ptsFlowRunner
from ptsLib import ptsNodeModuleScanner
from NodeGraphQt.base.node import NodeObject


class EmittingStream(QtCore.QObject):
    text_written = QtCore.pyqtSignal(str)

    def write(self, text):
        if text.strip():  # avoid empty lines
            self.text_written.emit(str(text) + "\n")

    def flush(self):
        pass  # Required for compatibility


class PTSFlows(object):

    def __init__(self, parent):
        self.tls = kTools.KTools()
        self.qttls = kQtTools.KQTTools()
        self.PTS = parent
        self.parentUi = self.PTS.ui
        self.console = self.PTS.console
        self.ndGraph = None
        self.canvas = self.parentUi.wgCanvas

        self.tls.createNewSignalSetup("flowevent")
        self.tls.subscribeToSignal("flowevent", self.flowSignalsHndl)
        self.tls.publishSignal("flowevent", { "msg": "Flow signalling ready", "lst": [] })

        self.ptsNodesPath = self.tls.getSafeConfig(['pts', 'nodesPath'])
        self.ptsFlowsPath = self.tls.getSafeConfig(['pts', 'flowsPath'])

        self.uiNodeCollection = {}
        self.coreNodeCollection = {}
        self.lastNodeSelected = None
        self.threadStream = None
        self.selectedNode = None
        
        self.isFlowRunning = False
        self.isFlowDebugging = False
        self.isFlowEdited = 0
        self.currentLoadedFlowName = None
        self.currentLoadedFlowFile = None
        
        self.convertGenerateUINodeCollections()
        self.doClearAndInitalizeFlowChartArea()

        self.createNewFlowRunner(self.PTS)

        # Additional info
        self.tls.info(f"----Available Nodes----")
        for each in self.uiNodeCollection.keys():
            self.tls.info(f"{each} - {self.uiNodeCollection[each]}")
        
    def createNewFlowRunner(self, parent=None):        
        if hasattr(self, "flowRunner") and self.flowRunner:
            self.flowRunner.terminate()
            del(self.flowRunner)
            self.tls.doCleanMemory()
        self.flowRunner = ptsFlowRunner.PTSFlowRunner(parent)
        self.flowRunner.PTS_UI = self.parentUi
        self.flowRunner.nodeExecutionInprogress.connect(self.doNodeExecutionInProgress)
        self.flowRunner.nodeRejected.connect(self.doNodeDisable)
        self.flowRunner.flowExecutionCompleted.connect(self.doFlowExecutionCompleted)
        self.flowRunner.flowExecutionStatus.connect(self.doFlowExecutionStatus)
        self.flowRunner.executeUINodeAction.connect(self.doExecuteUINodeExecution)

    def flowSignalsHndl(self, data):

        lst = self.tls.getSafeDictValue(data, "lst", [])
        msg = self.tls.getSafeDictValue(data, "msg", None)
        if msg:
            self.tls.info(f"{msg}")
            
        if len(lst):
            act = lst[0]
            if act == "fetch_node":
                n = lst[1]
                node = lst[2]                                
                # print(f"{n}.Processing {node}... ",end='')
                # self.tls.info(f"{n} Pushing back [{node}], No input ready.")                
            if act == "pushback": 
                n = lst[1]
                node = lst[2]                                
                self.tls.info(f"{n}.Waiting {node}!")            
            if act == "pushback_loopnode": 
                n = lst[1]
                node = lst[2]                                
                self.tls.info(f"{n}.Waiting {node}!")                   
            if act == "executing": 
                n = lst[1]
                node = lst[2]                                
                self.tls.info(f"{n}.Executing {node}...")   
            if act == "scan_node":
                n = lst[1]
                self.tls.info(f"Scanning [{n}]...")                  
        
    def stdStreamSwap(self, reverse=False):
        if reverse:
            if not self.threadStream is None:
                sys.stdout = self.original_stdout
                sys.stderr = self.original_stderr
                self.threadStream.deleteLater()
                self.threadStream = None
            self.PTS.logDisplayer.grabStdOut()
        else:
            self.PTS.logDisplayer.reset()
            self.original_stdout = sys.stdout
            self.original_stderr = sys.stderr
            self.threadStream = EmittingStream()
            self.threadStream.text_written.connect(self.PTS.logTextDisplayUpdate)
            sys.stdout = self.threadStream
            sys.stderr = self.threadStream

    def doExecuteUINodeExecution(self, modToExecute, request, callBackPassingResult):
        try:
            res = modToExecute.ACTION(request)
            callBackPassingResult(res)
        except Exception as e:
            lstError = self.tls.getLastErrorInfo()
            print('----------------------------------')
            self.tls.error(lstError)
            print('----------------------------------')
            self.flowRunner.terminateFlow("Node execution failed.")
            self.doFlowExecutionCompleted(None)

    def doFlowKeyPressed(self, eve):
        if (eve.key() == QtCore.Qt.Key_Delete):

            selectedNodes = self.ndGraph.selected_nodes()
            selectedPipes = self.ndGraph.viewer().selected_pipes()

            for eachNode in selectedNodes:
                self.tls.debug(f"Deleting node... {eachNode.NODE_NAME}")
                self.ndGraph.remove_node(eachNode)
                self.tls.info(f"Done")
                self.refreshFlow()
                self.doClearProps()
                #self.tls.doCleanMemory()

            if len(selectedPipes) == 1:
                selPipe = selectedPipes[0]
                # selPipe.delete() #TODO: After delete unable to recreate the flow from same src to dst

    def doClearProps(self):
        self.doClearNodeDesc()
        self.doNodePropsClear()        

    def doFlowNodeSelectionChanged(self, newNode, oldNode):
        newNode = newNode[0] if len(newNode) else None
        oldNode = oldNode[0] if len(oldNode) else None
        if not newNode and oldNode: self.doClearProps()

    def doFlowNodeSelected(self, nodeObj):
        self.doClearProps()
        self.doNodePropsPopulate(nodeObj)
        self.doLoadNodeDesc(nodeObj)

    def doNodePropsClear(self):
        parent = self.parentUi.propsHolder
        if parent.layout():
            while parent.layout().count():
                item = parent.layout().takeAt(0)
                parent.layout().removeWidget(item.widget())
                del(item)

    def doNodePropsPopulate(self, nodeObj):
        newDict = {}
        newDict["Node Name"] = nodeObj.NODE_NAME
        if not self.flowRunner._isTagPresentInTags('sys', nodeObj.NODE_TAGS) and self.flowRunner._isTagPresentInTags('custom', nodeObj.NODE_TAGS) and hasattr(nodeObj.NODE_MODULE, "ACTION"):
            newDict["Node Script"] = "default"
        for eachKey in nodeObj.props.keys():
            newDict[eachKey] = nodeObj.props[eachKey]
        self.qttls.createPropEditor(self.parentUi.propsHolder, newDict, self.doNodePropsUpdate, nodeObj)

    def doNodePropsUpdate(self, table, nodeObj):
        self.tls.debug(f"Updated Node: { nodeObj.name() }")
        self.tls.debug(f"Updated Flow: { self.getCurrentSession() }")        
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
        self.doFlowEdited()

    def doLoadNodeDesc(self, nodeObj):
        html = ""
        html += f"<b>Node Name: </b>{nodeObj.model.name}"
        html += "<br>"
        html += f"<b>Node Type: </b>{nodeObj.model.type_}".replace('nodeGraphQt.nodes.', '')
        html += "<br>"
        html += f"<b>Node Tags: </b>{','.join(nodeObj.NODE_TAGS)}"
        html += "<hr>"
        html += nodeObj.NODE_DESC.replace("\n", "<br>")
        html += "<hr>"
        html += f"<b>Last Updated On: </b>{nodeObj.NODE_MODULE.__updated__}"
        self.parentUi.infoView.setHtml(html)

    def doClearNodeDesc(self):
        self.parentUi.infoView.setHtml("")

    def doFlowNodeDropped(self, event, pos):
        nodeItem = event.source().selectedItems()[0]
        nodeName = str(nodeItem.text(0))
        nodePath = str(nodeItem.data(0, QtCore.Qt.UserRole))
        x = pos.x()
        y = pos.y()
        if nodeName in self.uiNodeCollection:
            nodeObj = self.uiNodeCollection[nodeName]
            node = self.ndGraph.create_node(nodeObj.type_, pos=[x, y])
            self.tls.debug(f"Node added {node.NODE_NAME}")
            self.doFlowEdited()
        else:
            self.tls.error(f"Node {nodeName} is not valid. Not pre-loaded valid node.")

    def doNodeExecutionInProgress(self, nodeName):
        if self.lastNodeSelected:
            self.lastNodeSelected.set_selected(False)

        if nodeName:
            for each in self.ndGraph.model.nodes.keys():
                cur = self.ndGraph.model.nodes[each]
                if str(cur.NODE_NAME).strip() == str(nodeName).strip():
                    cur.set_selected(True)
                    self.lastNodeSelected = cur

    def doNodeDisable(self, nodeName):
        for each in self.ndGraph.model.nodes.keys():
            cur = self.ndGraph.model.nodes[each]
            if str(cur.NODE_NAME).strip() == str(nodeName).strip():
                cur.set_disabled(True)

    def doNodeEnableAll(self):
        for each in self.ndGraph.model.nodes.keys():
            cur = self.ndGraph.model.nodes[each]
            cur.set_disabled(False)
        
    def convertGenerateUINodeCollections(self):
        '''
        Scan node folder and convert it to qt nodes:
        '''
        self.uiNodeCollection = {}
        
        self.tls.info(f"Scan and Prepare node collections...")
        pts = ptsNodeModuleScanner.PTSNodeModuleScanner(self.console)
        pts.scanNodeModuleFolder()

        for clsName in pts.allNodes:
            self.uiNodeCollection[clsName] = pts.allNodes[clsName]

    def centerViewFlow(self):
        allNodes = self.ndGraph.all_nodes()
        if allNodes: self.ndGraph.center_on(allNodes)
        self.doClearProps()

    def refreshFlow(self):
        self.tls.debug("Refreshing flow view")
        self.ndGraph.viewer().update()
        self.ndGraph.viewer().force_update()
        self.ndGraph.viewer().repaint()
        self.ndGraph.viewer()._update_scene()
        zoomVal = self.ndGraph._viewer.get_zoom()
        self.ndGraph._viewer.set_zoom(zoomVal + 0.0000000000001)
        self.ndGraph._viewer.set_zoom(zoomVal)
        QApplication.processEvents()
        if hasattr(self, 'flowRunner'): self.flowRunner.initializer()

    def getCurrentSession(self):
        return self.ndGraph._model.session
    
    def isFlowFileOpen(self):
        return self.ndGraph and self.ndGraph._model.session and self.currentLoadedFlowFile and self.currentLoadedFlowName
    
    def doNewFlow(self):
        if self.isFlowFileOpen():
            if self.isFlowEdited:
                doSave = self.qttls.showYesNoBox(self.tls.getAppName(), "Do you want to save the change?")
                if doSave:
                    self.doSaveFlow()
        else:
            if self.isFlowEdited:
                doSave = self.qttls.showYesNoBox(self.tls.getAppName(), "Do you want to save this to file?")
                if doSave:
                    self.doSaveFlowAs()
        self.doClearFlowForNew()
          
    def doOpenFlow(self):
        if self.isFlowFileOpen():
            if self.isFlowEdited:
                doSave = self.qttls.showYesNoBox(self.tls.getAppName(), "Do you want to save the change?")
                if doSave:
                    self.doSaveFlow()
        else:
            if self.isFlowEdited:
                doSave = self.qttls.showYesNoBox(self.tls.getAppName(), "Do you want to save this to file?")
                if doSave:
                    self.doSaveFlowAs()  
        
        flowFile = self.qttls.getFile('Select a flow file to open...', self.ptsFlowsPath, 'Flow Files (*.flow);;All Files (*)')
        if flowFile:                        
            self.coreLoadFlow(flowFile)

    def doSaveFlow(self):
        if self.isFlowFileOpen():
            if self.isFlowEdited:
                self.coreSaveFlow(self.currentLoadedFlowFile)
            else:
                self.tls.info("Nothing to save!")
        else:
            if self.isFlowEdited:
                self.doSaveFlowAs()
            else:
                self.tls.info("Nothing to save!")

    def doSaveFlowAs(self):
        if self.isFlowEdited:
            flowFile = self.qttls.getFileToSave('Select a folder to save flow as...', FileName=self.ptsFlowsPath, FileType='Flow Files (*.flow);;All Files (*)')
            if flowFile:
                self.coreSaveFlow(flowFile)
            else:
                self.tls.info("Nothing to save!")
        else:
            self.tls.info("Nothing to save!")

    def doClearAndInitalizeFlowChartArea(self):
        
        if hasattr(self, "ndGraph") and self.ndGraph:
            self.ndGraph.blockSignals(True)
            self.ndGraph.scene().blockSignals(True)
            self.ndGraph.scene().viewer().blockSignals(True)        
            self.ndGraph.scene().viewer().all_nodes().clear()        
            self.ndGraph.scene().viewer().all_pipes().clear()
            self.ndGraph.delete_nodes(self.ndGraph.all_nodes(), push_undo=False)                        
            self.ndGraph.clear_selection()
            self.ndGraph.clear_session()
            self.ndGraph.clear_undo_stack()
            self.ndGraph.undo_stack().clear()
            self.ndGraph.reset_zoom()
            self.doClearProps()          
            self.qttls.swapWidget(self.parentUi.lytCanvasHolder, self.ndGraph.widget, self.parentUi.wgCanvas)
            self.ndGraph.close()
            self.ndGraph.blockSignals(False)
            self.ndGraph.scene().blockSignals(False)
            self.ndGraph.scene().viewer().blockSignals(False)
            self.ndGraph.widget.deleteLater()
            del(self.ndGraph)
            self.tls.doCleanMemory()

        self.tls.info(f"Prepare new nodegraph canvas...")
        self.ndGraph = NodeGraph(undo_stack = None)

        self.ndGraph.register_nodes(list(self.uiNodeCollection.values()))
        self.qttls.swapWidget(self.parentUi.lytCanvasHolder, self.parentUi.wgCanvas, self.ndGraph.widget, delete=0)

        #Node graph signal connectors initializing
        self.ndGraph.node_selected.connect(self.doFlowNodeSelected)
        self.ndGraph.node_selection_changed.connect(self.doFlowNodeSelectionChanged)
        self.ndGraph.nodes_deleted.connect(self.doFlowEdited)
        self.ndGraph.port_connected.connect(self.doFlowEdited)
        self.ndGraph.port_disconnected.connect(self.doFlowEdited)
        self.ndGraph.widget.currentWidget().custom_data_dropped.connect(self.doFlowNodeDropped)
        self.ndGraph.widget.currentWidget().custom_key_pressed.connect(self.doFlowKeyPressed)
        self.refreshFlow()        
                    
    def doClearFlowForNew(self):
        self.doClearAndInitalizeFlowChartArea()

        self.currentLoadedFlowName = None
        self.currentLoadedFlowFile = None
        self.lastNodeSelected = None
        self.isFlowRunning = False
        self.isFlowDebugging = False
        self.isFlowEdited = False
        
        self.PTS.doSetTitle(isEdited=0)
        self.PTS.doSetTitle(flowName="New")  
        self.PTS.disableAllToolBarAction() 
        self.PTS.enableToolBarActionsFor("clear")      
    
    def doFlowEdited(self, *arg):
        self.isFlowEdited = 1
        self.PTS.doSetTitle(isEdited=1)   
        self.PTS.disableAllToolBarAction()    
        self.PTS.enableToolBarActionsFor("edited")

    def doRunFlow(self):
        self.tls.info(f"Flow execution requested for: {self.getCurrentSession()}")
        if self.isFlowFileOpen() and not self.isFlowEdited and not self.isFlowRunning and not self.isFlowDebugging :
            self.PTS.bringConsoleToFocus()
            self.stdStreamSwap()
            self.doNodeEnableAll()
            self.createNewFlowRunner(self.PTS)
            self.flowRunner.initializer()
            self.flowRunner.debugMode = 0
            self.flowRunner.flowFile = self.currentLoadedFlowFile
            self.flowRunner.preSetup()
            self.flowRunner.start()
            self.isFlowRunning = 1
            self.isFlowDebugging = 0
            self.PTS.disableAllToolBarAction()    
            self.PTS.enableToolBarActionsFor("running")            
        else:
            self.tls.info("Unable to debug flow. Either no flow loaded, or already another flow running / debugging, or flow edited not saved.")

    def doDebugFlow(self):
        self.tls.info("Debugging flow...")
        if self.isFlowFileOpen() and not self.isFlowEdited and not self.isFlowRunning and not self.isFlowDebugging:
            self.PTS.bringConsoleToFocus()
            self.stdStreamSwap()
            self.createNewFlowRunner(self.PTS)
            self.doNodeEnableAll()
            self.flowRunner.initializer()
            self.flowRunner.debugMode = 1
            self.flowRunner.flowFile = self.currentLoadedFlowFile
            self.flowRunner.preSetup()
            self.flowRunner.start()
            self.isFlowRunning = 0
            self.isFlowDebugging = 1
            self.PTS.disableAllToolBarAction()    
            self.PTS.enableToolBarActionsFor("debugging")                        
        else:
            self.tls.info("Unable to debug flow. Either no flow load,or already another flow running / debugging, or flow edited not saved.")

    def doDebugProceed(self):
        if self.isFlowDebugging:
            self.flowRunner.stepNext()

    def doDebugResume(self):
        if self.isFlowDebugging:
            self.flowRunner.resume()

    def doTerminateExecution(self):
        if self.isFlowDebugging or self.isFlowRunning:
            self.flowRunner.terminateFlow("Requested")
            self.isFlowDebugging = 0
            self.isFlowRunning = 0
            self.flowRunner.stop()
            self.PTS.disableAllToolBarAction()    
            self.PTS.enableToolBarActionsFor("executiondone")               

    def doFlowExecutionStatus(self, msg):
        # self.tls.info(msg)
        pass

    def doFlowExecutionCompleted(self, param):
        # self.PTS.logDisplayer.grabStdOut()
        self.stdStreamSwap(reverse=True)
        self.tls.info(f"Flow execution completed, {self.getCurrentSession()}")
        if self.lastNodeSelected: self.lastNodeSelected.set_selected(False)
        # self.PTS.logDisplayer.grabStdOut()
        self.isFlowRunning = 0
        self.isFlowDebugging = 0
        self.PTS.disableAllToolBarAction()    
        self.PTS.enableToolBarActionsFor("executiondone")            
                
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
        
        if self.currentLoadedFlowFile:
            savedToNewFile = not (os.path.abspath(file_path.strip()) ==  os.path.abspath(self.currentLoadedFlowFile.strip()))
        else:
            savedToNewFile = True
            
        self.currentLoadedFlowName = os.path.basename(file_path).lower().replace('.flow', '')
        self.currentLoadedFlowFile = os.path.abspath(file_path)
        self.lastNodeSelected = None
        self.isFlowRunning = False
        self.isFlowDebugging = False
        self.isFlowEdited = False
               
        #self.tls.doCleanMemory()
        self.PTS.doSetTitle(isEdited=0)
        if savedToNewFile: self.PTS.doSetTitle(flowName=self.currentLoadedFlowName)   

        if savedToNewFile: self.PTS.doLoadFlowTree()
        self.PTS.disableAllToolBarAction() 
        self.PTS.enableToolBarActionsFor("saved")               

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

        self.doClearAndInitalizeFlowChartArea()
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
        self.doNodeEnableAll()
        
        self.currentLoadedFlowName = os.path.basename(file_path).lower().replace('.flow', '')
        self.currentLoadedFlowFile = os.path.abspath(file_path)
        self.lastNodeSelected = None
        self.isFlowRunning = False
        self.isFlowDebugging = False
        self.isFlowEdited = False
               
        #self.tls.doCleanMemory()
        self.PTS.doSetTitle(isEdited=0, flowName=self.currentLoadedFlowName)    
        self.PTS.disableAllToolBarAction()        
        self.PTS.enableToolBarActionsFor("loaded")
