# For DevConsole
import inspect
import os
import sys

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt,)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget,)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5.Qt import QLineEdit
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets


import kTools 
import kQtTools

#----------------------
from NodeGraphQt import NodeGraph

from ptsLib.ptsNodes import ndInputs
from ptsLib.ptsNodes import ndOutputs
from ptsLib.ptsNodes import ndWebCall 

#----------------------

# from nodeeditor.node_node import Node
# from nodeeditor.node_scene import Scene, InvalidFile
# from nodeeditor.node_edge import Edge, EDGE_TYPE_BEZIER
# from nodeeditor.node_graphics_view import QDMGraphicsView
# from nodeeditor.node_editor_window import NodeEditorWindow
#----------------------

# from ptsLib.SampleNodes.constant import ConstantNode
# from ptsLib.SampleNodes.operation import OperationNode
# from ptsLib.SampleNodes.output import OutputNode
# from ptsLib.SampleNodes.mySpl import MySpl

# from QNodeEditor.editor import NodeEditor
# from QNodeEditor import themes


class core(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        super().__init__()
        self.tls = kTools.GetKTools()
        self.qttls = kQtTools.KQTTools()
        
        self.tls.info('Preparing GUI...')
        QtWidgets.QMainWindow.__init__(self)		
        self.uiFile = sys.modules[__name__].__file__
        self.uiFile = self.uiFile.replace(".py", ".ui")
        loadUi(self.uiFile, self)
                
        #---------------------------------------
        #
        # self.neWin = NodeEditor()
        # self.qttls.swapWidget(self.lytCanvasHolder, self.wgCanvas, self.neWin)
        #
        # self.neScene = self.neWin.scene
        #
        # node_constant = ConstantNode('Constant')
        # node_output = OutputNode('Output')
        # ms = MySpl('mspl')
        #
        # node_constant.graphics.setPos(-200, 0)
        # node_output.graphics.setPos(200, 0)
        #
        # self.neScene.add_node(node_constant)
        # self.neScene.add_node(node_output)
        # self.neScene.add_node(ms)                
        #
        # self.neWin.theme = themes.light.LightTheme

                
        #---------------------------------------
        
        nodeCollection = []
        nodeCollection.append(ndInputs.NDInputs)
        nodeCollection.append(ndOutputs.NDOutputs)
        nodeCollection.append(ndWebCall.NDWebCall)
        
        self.grp = NodeGraph()        
        self.grp.register_nodes(nodeCollection)        
        self.qttls.swapWidget(self.lytCanvasHolder, self.wgCanvas, self.grp.widget)
                
        self.nIp1 = self.grp.create_node('nodes.NDInputs')
        self.nIp2 = self.grp.create_node('nodes.NDInputs')
        self.nOp = self.grp.create_node('nodes.NDOutputs')
        self.nWc = self.grp.create_node('nodes.NDWebCall')
        
        self.grp.auto_layout_nodes()
        
        #Node Locked not movable
        self.nWc.view.text_item.setEnabled(0)
                
        
        #
        # self.anode = self.grp.create_node(
        # 'nodes.basic.BasicNodeA',color='#e4dd93', text_color='#58520b', pos=(300, 440))
        #
        # self.bnode = self.grp.create_node(
        # 	'nodes.basic.BasicNodeB', name='custom icon')
        #

                
        self.treePtsNodes.itemDoubleClicked.connect(self.temp)		
        
        #---------------------------------------

    def temp(self, *arg):
        itm = arg[0]
        inx = arg[1]
        # self.tls.info(arg)
        # self.graph.auto_layout_nodes()
        # self.graph.center_on()
        #self.graph.fit_to_selection()
        #self.neWin.view.align_selection(Qt.Horizontal, Qt.AlignLeft)
        
        print(self.grp)
        self.grp.set_background_color(255, 255, 255)
        self.grp.set_grid_color(200, 200, 200)
        
        self.tls.info('done')

if __name__ == "__main__":
    tls = kTools.GetKTools("pytasky")    
    app = QtWidgets.QApplication(sys.argv)
    appwin = core()
    appwin.show()
    sys.exit(app.exec_())
