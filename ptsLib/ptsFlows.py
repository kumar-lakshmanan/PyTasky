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

class PTSFlows(object):

    def __init__(self, parent):
        
        self.tls = kTools.GetKTools()    
        self.qttls = kQtTools.KQTTools()
        self.PTS = parent
        self.parentUi = self.PTS.ui
        self.console = self.PTS.console
        self.nodeSelectedFn = None
        
        self.ptsNodesPath = "G:/pyworkspace/PyTasky/ptsLib/ptsNodes"

        self.ptsNodeCollections = {}
        self.ptsCurrentNodes = []
        
        self.ptsNodeProps = {}

        self.doFlowUISetup()
        
    
    def doFlowUISetup(self):
        self.nodesMods = self.tls.getFileList(self.ptsNodesPath,".py")
        
        for file in self.nodesMods:
            fileName = os.path.basename(file).replace(".py","")
            if fileName != "__init__" or fileName in list(self.ptsNodeCollections.keys()):
                modImported = self.console.loadModule(fileName, file)
                mod = getattr(modImported, fileName)
                self.ptsNodeCollections[fileName] = mod 
            else:
                self.tls.error(f'{fileName} cant be node to load might be duplicate. {file}')
        
        self.ndGraph = NodeGraph()        
        self.ndGraph.register_nodes(list(self.ptsNodeCollections.values()))        
        self.qttls.swapWidget(self.parentUi.lytCanvasHolder, self.parentUi.wgCanvas, self.ndGraph.widget)
                
        self.ndGraph.node_selected.connect(self.doFlowNodeSelected)
                
        self.ndGraph.auto_layout_nodes()
        
        
        self.ndGraph.widget.currentWidget().custom_data_dropped.connect(self.doFlowNodeDropped)
        self.ndGraph.widget.currentWidget().custom_key_pressed.connect(self.doFlowKeyPressed)
        
        
    def doFlowKeyPressed(self, eve):
        if (eve.key() == QtCore.Qt.Key_Delete):
            if len(self.ndGraph.selected_nodes()) == 1:
                selNode = self.ndGraph.selected_nodes()[0]
                self.ndGraph.remove_node(selNode)
           
    
    def doFlowNodeSelected(self, nodeObj):
        if self.nodeSelectedFn: self.nodeSelectedFn(nodeObj)     

    def doFlowNodeDropped(self, event, pos):
        nodeItem = event.source().selectedItems()[0]
        nodeName = str(nodeItem.text(0))
        nodePath = str(nodeItem.data(0, QtCore.Qt.UserRole))
        x = pos.x()
        y = pos.y()
        nodeObj = self.ptsNodeCollections[nodeName]
        node = self.ndGraph.create_node(nodeObj.type_, pos=[x,y])
        self.ptsCurrentNodes.append(node)        
    
    def doRunFlow(self):
        print("Running flow...")
        
        flowName = self.ndGraph.current_session()        
        print(flowName)
        
        nds = self.ndGraph.all_nodes()
        nd = self.ndGraph.model.nodes
        for eachKey in nd:
            nwnd = nd[eachKey]
        print(nwnd)
        
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
    
    def getNodeByNodeName(self, nodeName):
        for eachNode in self.ndGraph.all_nodes():
            if nodeName.strip() == eachNode.NODE_NAME.strip():
                return eachNode
        return None
        
        
                   