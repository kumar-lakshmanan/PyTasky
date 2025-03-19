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
from ptsLib import ptsFlowExecuter

class PTSFlows(object):

    def __init__(self, parent):        
        self.tls = kTools.GetKTools()    
        self.qttls = kQtTools.KQTTools()
        self.PTS = parent
        self.parentUi = self.PTS.ui
        self.console = self.PTS.console

        self.ptsNodesPath = "G:/pyworkspace/PyTasky/ptsNodes"

        self.doFlowInitializer()
            
    def doFlowInitializer(self):
        self.loadNodeModules()
        self.nodeGraphSetup()
        self.nodeGraphSignalConnectors()
        self.ndGraph.auto_layout_nodes()
        self.flowExecuterInitalizer()
    
    def flowExecuterInitalizer(self):
        self.flowExec = ptsFlowExecuter.PTSFlowExecuter(self)  
        
    def refreshFlow(self):
        self.tls.info("Refreshed")
        self.ndGraph.viewer().update()
        self.ndGraph.viewer().force_update()
        self.ndGraph.viewer().repaint()
        self.ndGraph.viewer()._update_scene()
        zoomVal = self.ndGraph._viewer.get_zoom()
        self.ndGraph._viewer.set_zoom(zoomVal+0.0000000000001)
        self.ndGraph._viewer.set_zoom(zoomVal)
        QApplication.processEvents()
         
    def doRunFlow(self):
        print("Running flow...")
        self.flowExec.doExecuteCurrentFlow()
        
    def doDebugFlow(self):
        self.flowExec.debugWait = 0
                       
    def nodeGraphSignalConnectors(self):
        self.tls.info(f"Node graph signal connectors initializing.")
        self.ndGraph.node_selected.connect(self.doFlowNodeSelected)
        self.ndGraph.widget.currentWidget().custom_data_dropped.connect(self.doFlowNodeDropped)
        self.ndGraph.widget.currentWidget().custom_key_pressed.connect(self.doFlowKeyPressed)
                
    def nodeGraphSetup(self):
        self.tls.info(f"Setting node graph...")
        self.ndGraph = NodeGraph()        
        self.ndGraph.register_nodes(list(self.ptsNodeModCollections.values()))        
        self.qttls.swapWidget(self.parentUi.lytCanvasHolder, self.parentUi.wgCanvas, self.ndGraph.widget)
        
    def loadNodeModules(self):
        self.tls.info(f"Loading node modules from {self.ptsNodesPath}...")
        self.ptsNodeModCollections = {}
        nodesMods = self.tls.getFileList(self.ptsNodesPath,".py")
        
        for file in nodesMods:
            fileName = os.path.basename(file).replace(".py","")
            if fileName == "__init__": 
                self.tls.debug(f"{file} not a valid node.")
            elif fileName in list(self.ptsNodeModCollections.keys()): 
                self.tls.debug(f"{file} can't be loaded, Might be duplicate.") 
            else:
                modImported = self.console.loadModule(fileName, file)
                mod = getattr(modImported, fileName)
                self.ptsNodeModCollections[fileName] = mod 
        
    def doFlowKeyPressed(self, eve):
        #self.ndGraph.viewer().selected_items()
        if (eve.key() == QtCore.Qt.Key_Delete):
            
            selectedNodes = self.ndGraph.selected_nodes()
            selectedPipes = self.ndGraph.viewer().selected_pipes()
            
            for eachNode in selectedNodes:
                self.tls.info(f"Deleting... {eachNode.NODE_NAME}")
                self.ndGraph.remove_node(eachNode)
                self.tls.info(f"Done")                
                self.refreshFlow()
                
            if len(selectedPipes) == 1:
                selPipe = selectedPipes[0]
                #selPipe.delete() #TODO: After delete unable to recreate the flow from same src to dst
           
    def doFlowNodeSelected(self, nodeObj):
        print(f"---node select {nodeObj}")
        newDict = {}
        newDict["Node Name"] = nodeObj.NODE_NAME 
        for eachKey in nodeObj.props.keys():
            newDict[eachKey] = nodeObj.props[eachKey]                
        self.qttls.createPropEditor(self.parentUi.propsHolder, newDict, self.doNodePropsUpdate, nodeObj)        
        self.doLoadNodeDesc(nodeObj)
        
    def doNodePropsUpdate(self, table, nodeObj):        
        updated_dict = {}
        for row in range(table.rowCount()):
            key = table.item(row, 0).text()  # Property name (column 1)
            value = table.item(row, 1).text()  # User-edited value (column 2)
            updated_dict[key] = value            
        nodeObj.props = updated_dict
        nodeObj.set_name(updated_dict['Node Name'])
        updated_dict['Node Name'] = nodeObj.name()
        nodeObj.NODE_NAME = nodeObj.name()
        print("Updated Properties:", updated_dict)
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
        if nodeName in self.ptsNodeModCollections:
            nodeObj = self.ptsNodeModCollections[nodeName]
            node = self.ndGraph.create_node(nodeObj.type_, pos=[x,y])
            self.tls.info(f"Node added {node.NODE_NAME}")
        else:
            self.tls.error(f"Node {nodeName} is not valid. Not pre-loaded valid node.")

    def doSaveFlow(self, file_path):
        sessionInfo = self.ndGraph.serialize_session()
        print(sessionInfo)
        
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

        # update the current session.
        self.ndGraph._model.session = file_path
                
    def doLoadFlow(self, file_path):

        file_path = file_path.strip()
        if not os.path.isfile(file_path):
            raise IOError('file does not exist: {}'.format(file_path))

        try:
            with open(file_path) as data_file:
                fileContent = json.load(data_file)
        except Exception as e:
            fileContent = None
            print('Cannot read data from file.\n{}'.format(e))  
            
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
                
        self.ndGraph.session_changed.emit(file_path)    

