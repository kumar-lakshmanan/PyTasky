__appname__ = "PyTasky"
__author__  = "Kumaresan"
__created__ = "2025-03-07"
__updated__ = "2025-03-19"

import os, sys
KCONFIG = 'G:/pyworkspace/PyTasky/config.json'
KDEPENDS = 'G:/pyworkspace/kpylib;G:/pyworkspace/thirdparties/NodeGraphQt'
if not 'KDEPENDS' in os.environ or not __appname__ in os.environ['KDEPENDS'] : os.environ['KDEPENDS'] = KDEPENDS
if not 'KCONFIG' in os.environ or not __appname__ in os.environ['KCONFIG'] : os.environ['KCONFIG'] = KCONFIG
for eachDependency in os.environ['KDEPENDS'].split(';'): sys.path.append(eachDependency.strip())

from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5.Qt import QLineEdit
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt,)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget,)
from PyQt5.uic import loadUi

from ptsLib.ptsUi import ptsMainWindow
from ptsLib import ptsTreeUIHandler
from ptsLib import ptsConsole
from ptsLib import ptsFlows

from kQt import kQtTools
import kTools 

import PyTaskyLookUps

#----------------------

class core():

    def __init__(self,qapp):
        super(core, self).__init__()
        
        self.qapp = qapp
        
        #Support Modules ready
        self.tls = kTools.GetKTools()
        self.qttls = kQtTools.KQTTools()
        self.tls.qapp = qapp
                
        #Main UI ready
        self.ui = ptsMainWindow.PTSMainWindow()
                
        #Console UI ready - Along with custom  logger std err redirect and interpreter readying
        self.console = ptsConsole.PTSConsole(self)
                
        #ReArrange UI
        self.doGUIRearrange()

        self.doLoadNodeTree()
        self.doLoadScriptTree()        
        self.doToolBar()

        self.doSignalConnects()   
        
        self.flows = ptsFlows.PTSFlows(self)        
        #self.flows.doLoadFlow("TEST2.FLOW")

    def doGUIRearrange(self):
        # Output window tweak
        self.ui.qsciPtsStreamOut.setEolMode(Qsci.QsciScintilla.EolUnix)
        self.ui.qsciPtsStreamOut.setMarginWidth(1, 0)        
        self.ui.qsciPtsStreamOut.setUtf8(True)
        self.ui.qsciPtsStreamOut.setEolVisibility(False)      
        self.ui.qsciPtsStreamOut.setReadOnly(True)
        self.ui.qsciPtsStreamOut.setFont(QFont("Courier", 8))
        self.ui.qsciPtsStreamOut.setColor(QColor('#ffffff'))
        self.ui.qsciPtsStreamOut.setPaper(QColor('#000000'))        
        self.ui.qsciPtsStreamOut.setSelectionForegroundColor(QColor('#000000'))
        self.ui.qsciPtsStreamOut.setSelectionBackgroundColor(QColor('#ffffff'))
        self.ui.qsciPtsStreamOut.SendScintilla(self.ui.qsciPtsStreamOut.SCI_SETHSCROLLBAR, 0)
        
        self.ui.setWindowFlag(QtCore.Qt.WindowType.Window, True)
        self.ui.setWindowIcon(self.qttls.getIcon('user_samurai.png'))
        
        self.ui.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.ui.propContainerLayout.addWidget(self.ui.splitter)        
                
        self.ui.splitter.addWidget(self.ui.propsHolder)
        self.ui.splitter.addWidget(self.ui.propsDesc)        
        
    def doToolBar(self):
        self.tlBr = self.ui.addToolBar('Custom Tools')
        self.tlBr.setObjectName('customTools')
        self.tlBr.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)    
        
        act1 = self.qttls.createAction("Run", self.ui, icon="control_play_blue.ico", fn=self.doToolClicked)
        act12 = self.qttls.createAction("Debug", self.ui, icon="file_save_as.ico", fn=self.doToolClicked)
        act2 = self.qttls.createAction("Save", self.ui, icon="file_save_as.ico", fn=self.doToolClicked)
        act3 = self.qttls.createAction("Load", self.ui, icon="saved_exports.ico", fn=self.doToolClicked)
        act4 = self.qttls.createAction("Dummy", self.ui, icon="ax.ico", fn=self.doToolClicked)
        
        self.tlBr.addAction(act1)
        self.tlBr.addAction(act12)
        self.tlBr.addSeparator()
        self.tlBr.addAction(act2)
        self.tlBr.addAction(act3)
        self.tlBr.addSeparator()
        self.tlBr.addAction(act4)

    def doToolClicked(self, *arg):
        btnName = self.ui.sender().text()        
       
        if (btnName == "Run"):
            print("RUN")
            self.flows.doRunFlow()
                   
        if (btnName == "Debug"):            
            print("Dummy")
            self.flows.doDebugFlow()

        if (btnName == "Save"):
            print("Save") 
            self.flows.doSaveFlow("TEST2.FLOW")
            
        if (btnName == "Load"):            
            print("Load")      
            self.flows.doLoadFlow("TEST2.FLOW")
            
        if (btnName == "Dummy"):            
            print("Dummy")      
            #self.flows.ndGraph.all_nodes()[0].set_selected(True)
            #self.flows.ndGraph.clear_session()
                                       

    def showUI(self):
        self.ui.show()
    
    def doSignalConnects(self):
        self.ui.lineEdit.returnPressed.connect(self.doExecuteCommandLine)        

    def doLoadScriptTree(self):
        config = {}
        config['type'] = 'Script'
        config['filePath'] = 'G:/pyworkspace/PyTasky/ptsScripts'
        config['disallowedFolder'] = ['__','.git']
        config['allowedFiles'] = ['.py']
        config['fileContentShouldHave'] = "created"
        config['targetTreeObject'] = self.ui.treePtsScripts        
        self.treeScript = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeScript.loadTree()
        
    def doLoadNodeTree(self):
        config = {}
        config['type'] = 'Node'
        config['filePath'] = 'G:/pyworkspace/PyTasky/ptsNodes'
        config['disallowedFolder'] = ['__','.git']
        config['allowedFiles'] = ['.py']
        config['fileContentShouldHave'] = "created"
        config['targetTreeObject'] = self.ui.treePtsNodes        
        self.treeLoad = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeLoad.loadTree()
        
    def doExecuteCommandLine(self):
        val = str(self.ui.lineEdit.text()).strip()
        self.console.runCommand(val)
        self.ui.lineEdit.setText('')
        self.ui.lineEdit.setFocus()        

    def doAction(self, *arg):
        self.tls.info(f"This is action {arg}")
        self.console.runCommand("print('test')")        
        wins = self.qttls.createVerticalWindow(self.ui)
        wins[0].show()

if __name__ == "__main__":
    tls = kTools.GetKTools("PYTASKY", PyTaskyLookUps)    
    app = QtWidgets.QApplication(sys.argv)
    appCore = core(app)
    appCore.showUI()
    sys.exit(app.exec_())
