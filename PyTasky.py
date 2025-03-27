__appname__ = "PyTasky"
__author__  = "Kumaresan"
__created__ = "2025-03-07"
__updated__ = "2025-03-27"

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
        self.logDisplayer = ptsConsole.PTSConsole(self)
                
        #ReArrange UI
        self.doGUIRearrange()

        self.doLoadNodeTree()
        self.doLoadScriptTree()  
        self.doLoadFlowTree()      
        self.doToolBars()

        self.doSignalConnects()   
        
        self.flows = ptsFlows.PTSFlows(self)        

    def showUI(self):
        self.ui.show()
    
    def doSignalConnects(self):
        self.ui.lineEdit.returnPressed.connect(self.doExecuteCommandLine)            

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
        
        #Props Window Resetup
        self.ui.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.ui.propContainerLayout.addWidget(self.ui.splitter)        
        self.ui.splitter.addWidget(self.ui.propsHolder)
        self.ui.splitter.addWidget(self.ui.propsDesc)        
        
    def doToolBars(self):        
        self.tb01 = self.ui.addToolBar('Flow Tools')
        self.tb01.setObjectName('flowToolBar')
        self.tb01.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
                
        self.tb01a01 = self.qttls.createAction("New", self.ui, icon="new document.ico", fn=self.doToolClicked)
        self.tb01a04 = self.qttls.createAction("Open", self.ui, icon="Open Folder.ico", fn=self.doToolClicked)
        self.tb01a02 = self.qttls.createAction("Save", self.ui, icon="save.ico", fn=self.doToolClicked)
        self.tb01a03 = self.qttls.createAction("Save As", self.ui, icon="save_as.ico", fn=self.doToolClicked)
                
        self.tb01.addAction(self.tb01a01)
        self.tb01.addSeparator()
        self.tb01.addAction(self.tb01a04)
        self.tb01.addAction(self.tb01a02)
        self.tb01.addAction(self.tb01a03)        

        self.tb02 = self.ui.addToolBar('Execute Tools')
        self.tb02.setObjectName('executeToolBar')
        self.tb02.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)        

        self.tb02a01 = self.qttls.createAction("Run", self.ui, icon="control_play_blue.ico", fn=self.doToolClicked)
        self.tb02a02 = self.qttls.createAction("Debug", self.ui, icon="control_cursor_blue.ico", fn=self.doToolClicked)
        self.tb02a03 = self.qttls.createAction("Step Next", self.ui, icon="control_end_blue.ico", fn=self.doToolClicked)
        self.tb02a04 = self.qttls.createAction("Resume", self.ui, icon="control_fastforward_blue.ico", fn=self.doToolClicked)
        self.tb02a05 = self.qttls.createAction("Terminate", self.ui, icon="control_stop_blue.ico", fn=self.doToolClicked)

        self.tb02.addAction(self.tb02a01)        
        self.tb02.addAction(self.tb02a02)
        self.tb02.addSeparator()        
        self.tb02.addAction(self.tb02a03) 
        self.tb02.addAction(self.tb02a04)
        self.tb02.addAction(self.tb02a05)
        
        self.tb03 = self.ui.addToolBar('Custom Tools')
        self.tb03.setObjectName('customTools')
        self.tb03.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)    

        self.tb03a01 = self.qttls.createAction("Dummy", self.ui, icon="rubber_duck.ico", fn=self.doToolClicked)
        
        self.tb03.addAction(self.tb03a01)
        
        iconSize = 16   #16 or 32
        self.tb01.setIconSize(self.tb01.iconSize().scaled(iconSize, iconSize, 1))
        self.tb02.setIconSize(self.tb02.iconSize().scaled(iconSize, iconSize, 1))
        self.tb03.setIconSize(self.tb03.iconSize().scaled(iconSize, iconSize, 1))
        
        self.coreToolBarActionRestricter(1)
        
    def coreToolBarActionRestricter(self, mode):
        
        if mode == 1:  
            # mode = 1 
            # No flow loaded
            # Ok new, open
            # No save/saveas/run/debug/debugsteps/terminate
                        
            #Enable
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(0)   #Save
            self.tb01a03.setEnabled(0)   #Save As
            #Disable
            self.tb02a01.setEnabled(0)   #Run
            self.tb02a02.setEnabled(0)   #Debug As
            self.tb02a03.setEnabled(0)   #Step As
            self.tb02a04.setEnabled(0)   #Resume As
            self.tb02a05.setEnabled(0)   #Terminate As
            
        if mode == 2:  
            # mode = 2 
            # Flow loaded
            # Ok new, open, save/saveas/run/debug
            # No debugsteps/terminate
                        
            #Enable
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(1)   #Save
            self.tb01a03.setEnabled(1)   #Save As
            #Disable
            self.tb02a01.setEnabled(1)   #Run
            self.tb02a02.setEnabled(1)   #Debug As
            self.tb02a03.setEnabled(0)   #Step As
            self.tb02a04.setEnabled(0)   #Resume As
            self.tb02a05.setEnabled(0)   #Terminate As    
            
        if mode == 3:  
            # mode = 3 
            # Flow loaded - flow running
            # Ok new, open, save/saveas/terminate
            # No run/debug/debugsteps
                        
            #Enable
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(1)   #Save
            self.tb01a03.setEnabled(1)   #Save As
            #Disable
            self.tb02a01.setEnabled(0)   #Run
            self.tb02a02.setEnabled(0)   #Debug As
            self.tb02a03.setEnabled(0)   #Step As
            self.tb02a04.setEnabled(0)   #Resume As
            self.tb02a05.setEnabled(1)   #Terminate As   
            
        if mode == 4:  
            # mode = 4
            # Flow loaded - flow debugging 
            # Ok new, open, save/saveas/debugsteps/terminate
            # No run/debug/debugsteps
                        
            #Enable
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(1)   #Save
            self.tb01a03.setEnabled(1)   #Save As
            #Disable
            self.tb02a01.setEnabled(0)   #Run
            self.tb02a02.setEnabled(0)   #Debug As
            self.tb02a03.setEnabled(1)   #Step As
            self.tb02a04.setEnabled(1)   #Resume As
            self.tb02a05.setEnabled(1)   #Terminate As                                   
            
    def doToolClicked(self, *arg):
        btnName = self.ui.sender().text()        
       
       # File Toolbar
        if (btnName == "New"):
            self.flows.clearFlow()
            self.coreToolBarActionRestricter(1)

        if (btnName == "Open"):
            self.tls.debug("Open")
            self.flows.openFlow()
            self.coreToolBarActionRestricter(2)
                   
        if (btnName == "Save"):            
            self.tls.debug("Save")

        if (btnName == "Save As"):
            self.tls.debug("Save As")
            
        # Execution Toolbar
        if (btnName == "Run"):
            self.flows.doRunFlow()  
            self.coreToolBarActionRestricter(3)          

        if (btnName == "Debug"):
            self.flows.doDebugFlow()
            self.coreToolBarActionRestricter(4)            

        if (btnName == "Step Next"):
            self.flows.doDebugProceed()

        if (btnName == "Resume"):
            self.flows.doDebugResume()
            
        if (btnName == "Terminate"):
            self.flows.doTerminateExecution()
                                    
        #Custom
        if (btnName == "Dummy"):            
            self.tls.debug("Dummy")      

    def doLoadFlowTree(self):
        config = {}
        config['type'] = 'Flow'
        config['filePath'] = 'G:/pyworkspace/PyTasky/ptsFlows'
        config['disallowedFolder'] = ['__','.git']
        config['allowedFiles'] = ['.flow','.FLOW']
        config['fileContentShouldHave'] = "pipe_collision"
        config['targetTreeObject'] = self.ui.treePtsFlows     
        config['contextMenuOpenSpace'] = ['Create Folder...','Open Scripts Folder','','Refresh']
        config['contextMenuFileItems'] = ['Execute','','Edit Script','','Delete']
        config['contextMenuDirItems'] = ['Create New Script...','','Create Folder...']       
        config['menuSelectedFn'] = None
        config['dblClickFn'] = self.doFlowsTreeDblClicked            
        self.treeFlow = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeFlow.loadTree()

    def doLoadScriptTree(self):
        config = {}
        config['type'] = 'Script'
        config['filePath'] = 'G:/pyworkspace/PyTasky/ptsScripts'
        config['disallowedFolder'] = ['__','.git']
        config['allowedFiles'] = ['.py']
        config['fileContentShouldHave'] = "created"
        config['targetTreeObject'] = self.ui.treePtsScripts     
        config['contextMenuOpenSpace'] = ['Create Folder...','Open Scripts Folder','','Refresh']
        config['contextMenuFileItems'] = ['Execute','','Edit Script','','Delete']
        config['contextMenuDirItems'] = ['Create New Script...','','Create Folder...']       
        config['menuSelectedFn'] = self.doScriptTreeOptionSelected
        config['dblClickFn'] = self.doScriptTreeDblClicked            
        self.treeScript = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeScript.loadTree()
        
    def doLoadNodeTree(self):
        config = {}
        config['type'] = 'Node'
        config['filePath'] = 'G:/pyworkspace/PyTasky/ptsNodes'
        config['disallowedFolder'] = ['__','.git','Template']
        config['allowedFiles'] = ['.py']
        config['fileContentShouldHave'] = "Auto Generated Node"
        config['targetTreeObject'] = self.ui.treePtsNodes    
        config['contextMenuOpenSpace'] = ['Create Folder...','Open Nodes Folder','','Refresh']
        config['contextMenuFileItems'] = ['Edit Node','','Delete']
        config['contextMenuDirItems'] = ['Create New Node...','','Create Folder...']
        config['menuSelectedFn'] = self.doNodeTreeOptionSelected                 
        config['dblClickFn'] = self.doNodeTreeDblClicked
        self.treeNode = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeNode.loadTree()

    def doFlowsTreeDblClicked(self, label, fileFolder, typ, item):
        if typ == "file":
            self.flows.doLoadFlow(label, fileFolder)
            self.coreToolBarActionRestricter(2)
        
    def doScriptTreeDblClicked(self, label, fileFolder, typ, item):
        if typ == "file":
            self.console.runScript(fileFolder)
                
    def doNodeTreeDblClicked(self, label, fileFolder, typ, item):
        self.tls.debug(f"{label}, {fileFolder}, {typ}, {item}")
    
    def doNodeTreeOptionSelected(self, opt, dummy):
        self.tls.debug(opt)

    def doScriptTreeOptionSelected(self, opt, dummy):
        cmd = opt[0]
        if cmd == "Execute":
            script = opt[3][2]
            self.console.runScript(script)
        elif cmd == "Edit Script":
            script = opt[3][2]
            cmd = f'D:\Akelpads\AkelPad.exe /Call("Scripts::Main", 1,"Startup.js" ) {script}'
            self.tls.shellExecute(cmd)
        else:
            self.tls.info(opt)
        
    def doExecuteCommandLine(self):
        val = str(self.ui.lineEdit.text()).strip()
        self.console.runCommand(val)
        self.ui.lineEdit.setText('')
        self.ui.lineEdit.setFocus()         
        

    # def doAction(self, *arg):
    #     self.tls.info(f"This is action {arg}")
    #     self.console.runCommand("print('test')")        
    #     wins = self.qttls.createVerticalWindow(self.ui)
    #     wins[0].show()

if __name__ == "__main__":
    tls = kTools.GetKTools("PYTASKY", PyTaskyLookUps)    
    app = QtWidgets.QApplication(sys.argv)
    appCore = core(app)
    appCore.showUI()
    sys.exit(app.exec_())
