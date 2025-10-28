__appname__ = "PyTasky"
__author__  = "Kumaresan"
__created__ = "2025-03-07"
__updated__ = "2025-10-27"

'''

Check kTools document for basic config
'''

import os, sys
K_PYLIB = 'G:/pyworkspace/kpylib'
K_CONFIG = os.path.abspath('config.json')
if not ('K_PYLIB' in os.environ and os.path.exists(os.environ['K_PYLIB'])): os.environ['K_PYLIB'] = K_PYLIB
if not ('K_PYLIB' in os.environ and os.path.exists(os.environ['K_PYLIB'])): sys.exit("K_PYLIB not found!")
for eachDependency in os.environ['K_PYLIB'].split(';'): sys.path.append(eachDependency.strip())
if not ('K_CONFIG' in os.environ and os.path.exists(os.environ['K_CONFIG'])): os.environ['K_CONFIG'] = K_CONFIG
if not ('K_CONFIG' in os.environ and os.path.exists(os.environ['K_CONFIG'])): sys.exit("K_CONFIG not found!")

from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5.Qt import QLineEdit
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt,)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget,)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from schedule import Scheduler
from PyQt5.uic import loadUi
import threading
import time
import schedule
import queue
import atexit

from kQt import kQtTools
import kTools
import kCodeExecuter
    
from ptsLib.ptsUi import ptsMainWindow
from ptsLib import ptsScriptEditor
from ptsLib import ptsScheduler
from ptsLib import ptsSearch
from ptsLib import ptsTreeUIHandler
from ptsLib import ptsConsole
from ptsLib import ptsFlows
from ptsLib import ptsEventQueueActionManager
import PyTaskyLookUps


#----------------------

class core():

    def __init__(self,qapp):
        super(core, self).__init__()

        self.qapp = qapp

        #Support Modules ready
        self.tls = kTools.KTools()
        self.qttls = kQtTools.KQTTools()
        self.console = kCodeExecuter.KCodeExecuter()
        self.tls.share['console'] = self.console
        self.tls.qapp = qapp        
        self.disableLogDisplay = 0

        #Main UI ready
        self.ui = ptsMainWindow.PTSMainWindow()
        self.qttls.CallingUI = self.ui

        #Console UI ready - Along with custom  logger std err redirect and interpreter readying
        self.logDisplayer = ptsConsole.PTSConsole(self)

        #ReArrange UI
        self.doGUIRearrange()

        #Load Trees
        self.doLoadNodeTree()
        self.doLoadScriptTree()
        self.doLoadFlowTree()
        self.doLoadUITree()
        self.doToolBars()
        
        #UI Signals
        self.doSignalConnects()

        #Core Objects
        self.flows = ptsFlows.PTSFlows(self)
        
        self.tls.share["PTS_UI"] = self.ui
        self.tls.share["PTS_FLOWS"] = self.flows

        self.qttls.uiLayoutRestore()
        self.searchWin = None
        
        #Tray       
        self.qapp.setQuitOnLastWindowClosed(False)        
        self.tray = QtWidgets.QSystemTrayIcon(self.ui)
        self.tray.setIcon(self.qttls.getIcon("user_ninja.ico"))
        self.tray.setVisible(True)      
        self.tray.activated.connect(self.doTrayClicked)
        
        #Tray Menu
        exit_action = self.qttls.createAction("Exit PyTasky", self.ui, icon="cross.ico", fn=self.qapp.quit)
        self.traymenu = QtWidgets.QMenu()
        self.traymenu.addAction(exit_action)
        self.tray.setContextMenu(self.traymenu) 
        
        #UI Scheduler
        self.doSchedulerSetup()
        
        #EventQueueManger
        self.MainQueue = queue.Queue()
        self.queueListener = ptsEventQueueActionManager.PTSEventQueueManager(self)
        self.queueListener.ACTION_REQUESTED.connect(self.onQueueActionRequested)
        self.queueListener.ACTION_REQUESTED2.connect(self.onQueueActionRequested)
        self.queueListener.start()
        
        self.actionProcessor = ptsEventQueueActionManager.PTSEventActionManager(self)

        self.tls.info("System Ready!")
      
    def onQueueActionRequested(self, action, param):
        # Via main queue user requested some action, lets perform the action.
        self.actionProcessor.doAction(action, param)

    # def make_threaded(self, func, prevent_overlap=False):
    #     """
    #     Wraps `func` to run in a background thread.
    #     If prevent_overlap=True, ensures the same job doesn't overlap.
    #     """
    #     if not prevent_overlap:
    #         def wrapper(*args, **kwargs):
    #             threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
    #         return wrapper
    #     else:
    #         lock = threading.Lock()
    #         def wrapper(*args, **kwargs):
    #             if lock.locked():
    #                 return  # skip if still running
    #             def run():
    #                 with lock:
    #                     func(*args, **kwargs)
    #             threading.Thread(target=run, daemon=True).start()
    #         return wrapper        
                
    def doSchedulerSetup(self):
        self.sch = schedule
        original_do = self.sch.Job.do
        
        def make_threaded(func, prevent_overlap=False):
            """
            Wraps `func` to run in a background thread.
            If prevent_overlap=True, ensures the same job doesn't overlap.
            """
            if not prevent_overlap:
                def wrapper(*args, **kwargs):
                    threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True).start()
                return wrapper
            else:
                lock = threading.Lock()
                def wrapper(*args, **kwargs):
                    if lock.locked():
                        return  # skip if still running
                    def run():
                        with lock:
                            func(*args, **kwargs)
                    threading.Thread(target=run, daemon=True).start()
                return wrapper           
    
        def threaded_do(job, job_func, *args, **kwargs):
            # Wrap the job function
            wrapped = make_threaded(job_func, prevent_overlap=False)
            return original_do(job, wrapped, *args, **kwargs)
    
        self.sch.Job.do = threaded_do        
        self.schExecuter = QtCore.QTimer()
        self.schExecuter.timeout.connect(self.sch.run_pending)
        self.schExecuter.start(1000)  # every 1 sec        
        self.tls.info("Scheduler Ready!")
            
    def doTrayClicked(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger: # Single click (left click)
            if self.ui.isVisible():
                self.ui.hide()
            else:
                self.ui.show()
        elif reason == QtWidgets.QSystemTrayIcon.DoubleClick: # Double click
            self.ui.show() # Always show on double click
    
    def refreshNodes(self):
        self.doLoadNodeTree()        
        self.flows.convertGenerateUINodeCollections()
        self.flows.doClearAndInitalizeFlowChartArea()
        
    def doExecuteFlow(self, flowFile):
        if flowFile and os.path.exists(flowFile):                        
            self.flows.coreLoadFlow(flowFile)
            self.flows.doRunFlow()

    def doExecuteScript(self, scriptFile):
        if scriptFile and os.path.exists(scriptFile):                        
            self.console.runScript(scriptFile)
        
    def showUI(self):
        self.ui.show()

    def doSignalConnects(self):
        self.ui.lineEdit.returnPressed.connect(self.doExecuteCommandLine)
        self.ui.closeEvent = self.closeEvent

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
        
        #Debug Window Resetup
        # self.ui.splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        # self.ui.debugTreeHolderLayout.addWidget(self.ui.splitter2)
        # self.ui.splitter2.addWidget(self.ui.debugListHolder)
        # self.ui.splitter2.addWidget(self.ui.debugInfoHolder)

    def doToolBars(self):
        self.tb01 = self.ui.addToolBar('Flow Tools')
        self.tb01.setObjectName('flowToolBar')
        self.tb01.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        self.tb01a01 = self.qttls.createAction("New", self.ui, icon="newspaper.ico", fn=self.doToolClicked)
        self.tb01a04 = self.qttls.createAction("Open", self.ui, icon="Open Folder.ico", fn=self.doToolClicked)
        self.tb01a02 = self.qttls.createAction("Save", self.ui, icon="file_save_as.ico", fn=self.doToolClicked)
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

        self.tb03a01 = self.qttls.createAction("Search", self.ui, icon="google_custom_search.ico", fn=self.doToolClicked)
        self.tb03a02 = self.qttls.createAction("Dummy", self.ui, icon="rubber_duck.ico", fn=self.doToolClicked)
        
        self.tb03.addAction(self.tb03a01)
        self.tb03.addAction(self.tb03a02)

        iconSize = 16   #16 or 32
        self.tb01.setIconSize(self.tb01.iconSize().scaled(iconSize, iconSize, 1))
        self.tb02.setIconSize(self.tb02.iconSize().scaled(iconSize, iconSize, 1))
        self.tb03.setIconSize(self.tb03.iconSize().scaled(iconSize, iconSize, 1))

        self.disableAllToolBarAction()
        
    def disableAllToolBarAction(self):
        self.tb01a01.setEnabled(0)   #New
        self.tb01a04.setEnabled(0)   #Open
        self.tb01a02.setEnabled(0)   #Save
        self.tb01a03.setEnabled(0)   #Save As

        self.tb02a01.setEnabled(0)   #Run
        self.tb02a02.setEnabled(0)   #Debug As
        self.tb02a03.setEnabled(0)   #Step As
        self.tb02a04.setEnabled(0)   #Resume As
        self.tb02a05.setEnabled(0)   #Terminate As
        
    def enableToolBarActionsFor(self, actionName=None):
        if actionName == "clear":
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(0)   #Save
            self.tb01a03.setEnabled(0)   #Save As
            self.tb02a01.setEnabled(0)   #Run
            self.tb02a02.setEnabled(0)   #Debug As
            self.tb02a03.setEnabled(0)   #Step As
            self.tb02a04.setEnabled(0)   #Resume As
            self.tb02a05.setEnabled(0)   #Terminate As   
        if actionName == "edited":
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(1)   #Save
            self.tb01a03.setEnabled(1)   #Save As
            self.tb02a01.setEnabled(0)   #Run
            self.tb02a02.setEnabled(0)   #Debug As
            self.tb02a03.setEnabled(0)   #Step As
            self.tb02a04.setEnabled(0)   #Resume As
            self.tb02a05.setEnabled(0)   #Terminate As  
        if actionName == "saved":
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(0)   #Save
            self.tb01a03.setEnabled(1)   #Save As
            self.tb02a01.setEnabled(1)   #Run
            self.tb02a02.setEnabled(1)   #Debug As
            self.tb02a03.setEnabled(0)   #Step As
            self.tb02a04.setEnabled(0)   #Resume As
            self.tb02a05.setEnabled(0)   #Terminate As  
        if actionName == "loaded":
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(0)   #Save
            self.tb01a03.setEnabled(1)   #Save As
            self.tb02a01.setEnabled(1)   #Run
            self.tb02a02.setEnabled(1)   #Debug As
            self.tb02a03.setEnabled(0)   #Step As
            self.tb02a04.setEnabled(0)   #Resume As
            self.tb02a05.setEnabled(0)   #Terminate As      
        if actionName == "running":
            self.tb01a01.setEnabled(0)   #New
            self.tb01a04.setEnabled(0)   #Opem
            self.tb01a02.setEnabled(0)   #Save
            self.tb01a03.setEnabled(0)   #Save As
            self.tb02a01.setEnabled(0)   #Run
            self.tb02a02.setEnabled(0)   #Debug As
            self.tb02a03.setEnabled(1)   #Step As
            self.tb02a04.setEnabled(1)   #Resume As
            self.tb02a05.setEnabled(1)   #Terminate As               
        if actionName == "debugging":
            self.tb01a01.setEnabled(0)   #New
            self.tb01a04.setEnabled(0)   #Opem
            self.tb01a02.setEnabled(0)   #Save
            self.tb01a03.setEnabled(0)   #Save As
            self.tb02a01.setEnabled(0)   #Run
            self.tb02a02.setEnabled(0)   #Debug As
            self.tb02a03.setEnabled(1)   #Step As
            self.tb02a04.setEnabled(1)   #Resume As
            self.tb02a05.setEnabled(1)   #Terminate As   
        if actionName == "executiondone":                     
            self.tb01a01.setEnabled(1)   #New
            self.tb01a04.setEnabled(1)   #Opem
            self.tb01a02.setEnabled(0)   #Save
            self.tb01a03.setEnabled(1)   #Save As
            self.tb02a01.setEnabled(1)   #Run
            self.tb02a02.setEnabled(1)   #Debug As
            self.tb02a03.setEnabled(0)   #Step As
            self.tb02a04.setEnabled(0)   #Resume As
            self.tb02a05.setEnabled(0)   #Terminate As

    def doToolClicked(self, *arg):
        btnName = self.ui.sender().text()

        # File Toolbar
        if (btnName == "New"):
            self.flows.doNewFlow()

        if (btnName == "Open"):         
            self.flows.doOpenFlow()

        if (btnName == "Save"):
            self.flows.doSaveFlow()

        if (btnName == "Save As"):
            self.flows.doSaveFlowAs()

        # Execution Toolbar
        if (btnName == "Run"):
            self.flows.doRunFlow()

        if (btnName == "Debug"):
            self.flows.doDebugFlow()

        if (btnName == "Step Next"):
            self.flows.doDebugProceed()

        if (btnName == "Resume"):
            self.flows.doDebugResume()

        if (btnName == "Terminate"):
            self.flows.doTerminateExecution()

        #Custom
        if (btnName == "Search"):
            self.doLaunchSearchWindow()
            
    def doLaunchSearchWindow(self):
        # config
        searchConfig = {
            "fileTypesToSearch": ["py", "txt", "ui"],
            "foldersToSearch": {
                "Flow": self.tls.getSafeConfig(['pts', 'flowsPath']),
                "Node": self.tls.getSafeConfig(['pts', 'nodesPath']),
                "Script": self.tls.getSafeConfig(['pts', 'scriptsPath']),
                "UI": self.tls.getSafeConfig(['pts', 'uisPath'])
            }
        }
        
        if not self.searchWin: 
            self.searchWin = ptsSearch.SearchWindow(searchConfig)
            ico = self.qttls.getIcon('google_custom_search.ico')
            self.searchWin.setWindowIcon(ico)
        self.searchWin.show()
        if self.searchWin.isMinimized():
            self.searchWin.showNormal()     # restores from minimized/maximized to normal
            self.searchWin.activateWindow() # bring window to front
            self.searchWin.raise_()         # make sure it’s on top        

    def doSetTitle(self, isEdited=0, flowName=None):
        currentName = self.ui.windowTitle()
        if isEdited==1 and flowName==None:
            updatedName = currentName + "*" if not "*" in currentName else currentName
        elif isEdited==0 and flowName==None:
            updatedName = currentName.replace("*",'')
        elif isEdited==0 and flowName:
            updatedName = "PyTask - " + flowName if not flowName in currentName else currentName
        elif isEdited==1 and flowName!="":
            updatedName = "PyTask"
        self.ui.setWindowTitle(updatedName)

    def doLoadUITree(self):
        config = {}
        config['type'] = 'UIs'
        config['filePath'] = self.tls.getSafeConfig(['pts', 'uisPath'])
        config['disallowedFolder'] = ['__','.git']
        config['allowedFiles'] = ['.ui','.UI', '.uI','.Ui']
        config['fileContentShouldHave'] = '<ui version="4.0">'
        config['targetTreeObject'] = self.ui.treePtsUIs
        config['contextMenuOpenSpace'] = []
        config['contextMenuFileItems'] = ['Edit UI...', 'Edit in text editor', '' ,'Open this folder']
        config['contextMenuDirItems'] = ['Create new UI...','','Open this folder']
        config['menuSelectedFn'] = self.doUITreeOptionSelected
        config['dblClickFn'] = self.doUITreeDblClicked
        self.treeUI = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeUI.loadTree()

    def doLoadFlowTree(self):
        config = {}
        config['type'] = 'Flow'
        config['filePath'] = self.tls.getSafeConfig(['pts', 'flowsPath'])
        config['disallowedFolder'] = ['__','.git']
        config['allowedFiles'] = ['.flow','.FLOW']
        config['fileContentShouldHave'] = "pipe_collision"
        config['targetTreeObject'] = self.ui.treePtsFlows
        config['contextMenuOpenSpace'] = []
        config['contextMenuFileItems'] = ['Load flow...','Edit in text editor','','Open this folder']
        config['contextMenuDirItems'] = ['Open this folder']
        config['menuSelectedFn'] = self.doFlowTreeOptionSelected
        config['dblClickFn'] = self.doFlowsTreeDblClicked
        self.treeFlow = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeFlow.loadTree()

    def doLoadScriptTree(self):
        config = {}
        config['type'] = 'Script'
        config['filePath'] = self.tls.getSafeConfig(['pts', 'scriptsPath'])
        config['disallowedFolder'] = ['__','.git']
        config['allowedFiles'] = ['.py']
        config['fileContentShouldHave'] = ":"
        config['targetTreeObject'] = self.ui.treePtsScripts
        config['contextMenuOpenSpace'] = []
        config['contextMenuFileItems'] = ['Execute','Execute in Thread','Edit script...','Edit in text editor','','Open this folder']
        config['contextMenuDirItems'] = ['Create new script...','','Open this folder']
        config['menuSelectedFn'] = self.doScriptTreeOptionSelected
        config['dblClickFn'] = self.doScriptTreeDblClicked
        self.treeScript = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeScript.loadTree()

    def doLoadNodeTree(self):
        config = {}
        config['type'] = 'Node'
        config['filePath'] = self.tls.getSafeConfig(['pts', 'nodesPath'])
        config['disallowedFolder'] = ['__','.git']
        config['allowedFiles'] = ['.py']
        config['fileContentShouldHave'] = "#PTS_NODE"
        config['targetTreeObject'] = self.ui.treePtsNodes
        config['contextMenuOpenSpace'] = ['Refresh']
        config['contextMenuFileItems'] = ['Edit node...','Edit in text editor','','Open this folder']
        config['contextMenuDirItems'] = ['Create new node...','','Open this folder']
        config['menuSelectedFn'] = self.doNodeTreeOptionSelected
        config['dblClickFn'] = self.doNodeTreeDblClicked
        self.treeNode = ptsTreeUIHandler.TreeUIHandler(self, config)
        self.treeNode.loadTree()

    def doFlowsTreeDblClicked(self, label, fileFolder, typ, item):
        if typ == "file":
            self.flows.coreLoadFlow(fileFolder)

    def doUITreeDblClicked(self, label, fileFolder, typ, item):
        if typ == "file":
            bin = self.tls.getSafeConfig(['pts','qtDesignerBin'])
            self.tls.info(f"Opening the file {bin} with {fileFolder}")
            self.tls.fileLauncherWithBin(bin, fileFolder)

    def doScriptTreeDblClicked(self, label, fileFolder, typ, item):
        if typ == "file":
            self.console.runScript(fileFolder)
            #self.console.runScriptThreaded(fileFolder)

    def doNodeTreeDblClicked(self, label, fileFolder, typ, item):
        #self.tls.debug(f"{label}, {fileFolder}, {typ}, {item}")
        pass

    def getTemplateFileContent(self, templateFile, name, desc, username="unknown" ):
        templatePath = self.tls.getSafeConfig(['pts','templatesPath'])
        srcFile = self.tls.pathJoin(templatePath, templateFile)
        if self.tls.isFileExists(srcFile):
            content = self.tls.getFileContent(srcFile)
            content = content.replace("[NAME]", name)
            content = content.replace("[DESC]", desc)
            content = content.replace("[YOURNAME]", username)
            content = content.replace("[TODAY]", tls.getDateTimeStamp("%Y-%m-%d"))
            return content
        else:
            self.tls.error(f"Template file not found {srcFile}")
        return None

    def doUITreeOptionSelected(self, opt, dummy):             
        cmd = opt[0]
        if cmd == "Edit UI...":
            fileToOpenWith = opt[3][2]
            bin = self.tls.getSafeConfig(['pts','qtDesignerBin'])
            self.tls.info(f"Opening the file {fileToOpenWith} with {bin}")
            self.tls.fileLauncherWithBin(bin, fileToOpenWith)
                                
        elif cmd == "Edit in text editor":
            fileToOpenWith = opt[3][2]
            binary = self.tls.getSafeConfig(['pts','externalTextEditorBin'])
            self.tls.info(f"Opening the file {fileToOpenWith} with {binary}")
            self.tls.fileLauncherWithBin(binary, fileToOpenWith)
            
        elif cmd == "Open this folder":
            fileToOpenWith = opt[3][2]
            if self.tls.isFileExists(fileToOpenWith) and os.path.isfile(fileToOpenWith):
                fileToOpenWith = os.path.dirname(fileToOpenWith)        
            self.tls.info(f"Opening location {fileToOpenWith}")
            self.tls.fileLauncherWithBin("explorer", fileToOpenWith)

        elif cmd == "Create new UI...":
            fileToOpenWith = opt[3][2]
            if self.tls.isFileExists(fileToOpenWith) and os.path.isfile(fileToOpenWith):
                fileToOpenWith = os.path.dirname(fileToOpenWith) 
            newFileName = self.qttls.showInputBox("New UI", "Create new UI with name:", "new_ui.ui")
            if newFileName:
                newFileNameAlone = newFileName.replace('.ui','').replace('.UI','')
                newFile = self.tls.pathJoin(fileToOpenWith, newFileName)            
                if newFile and not self.tls.isFileExists(newFile):
                    newNodeContent = self.getTemplateFileContent("UITemplate.txt", newFileNameAlone, newFileNameAlone + "DESC", "unknown" )
                    self.tls.writeFileContent(newFile, newNodeContent)  
                    self.treeUI.loadTree()     
                    bin = self.tls.getSafeConfig(['pts','qtDesignerBin'])
                    self.tls.info(f"Opening the file {newFile} with {bin}")
                    self.tls.fileLauncherWithBin(bin, newFile)

    def doNodeTreeOptionSelected(self, opt, dummy):       
        cmd = opt[0]
        if cmd == "Edit node...":
            fileToOpenWith = opt[3][2]
            if (self.tls.getSafeConfig(['pts','scriptEditor']) == "internal"):
                self.showInternalScriptEditor(fileToOpenWith)
            else:
                binary = self.tls.getSafeConfig(['pts','externalScriptEditorBin'])
                self.tls.info(f"Opening the file {fileToOpenWith} with {binary}")
                self.tls.fileLauncherWithBin(binary, fileToOpenWith)
                                
        elif cmd == "Edit in text editor":
            fileToOpenWith = opt[3][2]
            binary = self.tls.getSafeConfig(['pts','externalTextEditorBin'])
            self.tls.info(f"Opening the file {fileToOpenWith} with {binary}")
            self.tls.fileLauncherWithBin(binary, fileToOpenWith)
            
        elif cmd == "Open this folder":
            fileToOpenWith = opt[3][2]
            if self.tls.isFileExists(fileToOpenWith) and os.path.isfile(fileToOpenWith):
                fileToOpenWith = os.path.dirname(fileToOpenWith)        
            self.tls.info(f"Opening location {fileToOpenWith}")
            self.tls.fileLauncherWithBin("explorer", fileToOpenWith)

        elif cmd == "Create new node...":
            fileToOpenWith = opt[3][2]
            if self.tls.isFileExists(fileToOpenWith) and os.path.isfile(fileToOpenWith):
                fileToOpenWith = os.path.dirname(fileToOpenWith) 
            newFileName = self.qttls.showInputBox("New node", "Create new node with name:", "new_node.py")
            if newFileName:
                if not newFileName.endswith(".py") or not newFileName.endswith(".PY"): newFileName =newFileName + '.py'
                newFileNameAlone = newFileName.replace('.py','').replace('.PY','')
                newFile = self.tls.pathJoin(fileToOpenWith, newFileName)            
                if newFile and not self.tls.isFileExists(newFile):
                    newNodeContent = self.getTemplateFileContent("NodeTemplate.txt", newFileNameAlone, newFileNameAlone + " DESC", "unknown" )
                    self.tls.writeFileContent(newFile, newNodeContent)  
                    self.treeNode.loadTree()     
                    if (self.tls.getSafeConfig(['pts','scriptEditor']) == "internal"):
                        self.showInternalScriptEditor(newFile)
                    else:
                        binary = self.tls.getSafeConfig(['pts','externalScriptEditorBin'])
                        self.tls.info(f"Opening the file {binary} with {fileToOpenWith}")
                        self.tls.fileLauncherWithBin(binary, newFile)     
        
        elif cmd == "Refresh":
            self.refreshNodes()               
    
    def doFlowTreeOptionSelected(self, opt, dummy):
        cmd = opt[0]
        if cmd == "Load flow...":
            fileToOpenWith = opt[3][2]
            self.flows.coreLoadFlow(fileToOpenWith)
                                
        elif cmd == "Edit in text editor":
            fileToOpenWith = opt[3][2]
            binary = self.tls.getSafeConfig(['pts','externalTextEditorBin'])
            self.tls.info(f"Opening the file {fileToOpenWith} with {binary}")
            self.tls.fileLauncherWithBin(binary, fileToOpenWith)
            
        elif cmd == "Open this folder":
            fileToOpenWith = opt[3][2]
            if self.tls.isFileExists(fileToOpenWith) and os.path.isfile(fileToOpenWith):
                fileToOpenWith = os.path.dirname(fileToOpenWith)        
            self.tls.info(f"Opening location {fileToOpenWith}")
            self.tls.fileLauncherWithBin("explorer", fileToOpenWith)
                            
    def doScriptTreeOptionSelected(self, opt, dummy):       
        cmd = opt[0]
        if cmd == "Execute":
            script = opt[3][2]
            self.console.runScript(script)
            
        if cmd == "Execute in Thread":            
            script = opt[3][2]
            self.console.runScriptThreaded(script)            
            
        elif cmd == "Edit script...":
            fileToOpenWith = opt[3][2]
            if (self.tls.getSafeConfig(['pts','scriptEditor']) == "internal"):
                self.showInternalScriptEditor(fileToOpenWith)
            else:
                binary = self.tls.getSafeConfig(['pts','externalScriptEditorBin'])
                self.tls.info(f"Opening the file {binary} with {fileToOpenWith}")
                self.tls.fileLauncherWithBin(binary, fileToOpenWith)

        elif cmd == "Edit in text editor":
            fileToOpenWith = opt[3][2]
            binary = self.tls.getSafeConfig(['pts','externalTextEditorBin'])
            self.tls.info(f"Opening the file {fileToOpenWith} with {binary}")
            self.tls.fileLauncherWithBin(binary, fileToOpenWith)
            
        elif cmd == "Open this folder":
            fileToOpenWith = opt[3][2]
            if self.tls.isFileExists(fileToOpenWith) and os.path.isfile(fileToOpenWith):
                fileToOpenWith = os.path.dirname(fileToOpenWith)        
            self.tls.info(f"Opening location {fileToOpenWith}")
            self.tls.fileLauncherWithBin("explorer", fileToOpenWith)

        elif cmd == "Create new script...":
            fileToOpenWith = opt[3][2]
            if self.tls.isFileExists(fileToOpenWith) and os.path.isfile(fileToOpenWith):
                fileToOpenWith = os.path.dirname(fileToOpenWith) 
            newFileName = self.qttls.showInputBox("New script", "Create new script with name:", "new_script.py")                             
            if newFileName:
                if not newFileName.endswith(".py") or not newFileName.endswith(".PY"): newFileName = newFileName + '.py'                
                newFileNameAlone = newFileName.replace('.py','').replace('.PY','')
                newFile = self.tls.pathJoin(fileToOpenWith, newFileName)            
                if newFile and not self.tls.isFileExists(newFile):
                    newScriptContent = self.getTemplateFileContent("ScriptTemplate.txt", newFileNameAlone, newFileNameAlone + " DESC", "unknown" )
                    self.tls.writeFileContent(newFile, newScriptContent)   
                    self.treeScript.loadTree()   
                    if (self.tls.getSafeConfig(['pts','scriptEditor']) == "internal"):
                        self.showInternalScriptEditor(newFile)
                    else:
                        binary = self.tls.getSafeConfig(['pts','externalScriptEditorBin'])
                        self.tls.info(f"Opening the file {binary} with {fileToOpenWith}")
                        self.tls.fileLauncherWithBin(binary, newFile)                  

    def doExecuteCommandLine(self):
        val = str(self.ui.lineEdit.text()).strip()
        try:
            res = self.console.runCommand(val)
            if res: self.tls.info(res)
        except Exception as e:
            self.tls.error(e)
        self.ui.lineEdit.setText('')
        self.ui.lineEdit.setFocus()

    def __enter__(self):
        self.tls.info('PyTasky startup actions initiated...')
        #self.schDoInstanceFirstAction()
        return self

    def __exit__(self, *arg):
        #self.schDoInstanceLastAction()
        #log.warning('Thank you for using sachathya!')
        self.exitCleanUpActivity(None)

    def closeEvent(self, event):
        #self.exitCleanUpActivity(event)
        if event: event.accept()
    
    def exitCleanUpActivity(self, event):
        self.tls.info('PyTasky exit actions initiated...')
        
        self.qttls.uiLayoutSave()
        self.tls.info('PyTasky ui saved!')
        
        self.schExecuter.stop()
        self.tls.info('PyTasky scheduler shutdown!')
        
        self.MainQueue.put("__quit__")
        self.queueListener.running = False
        self.tls.info('PyTasky event queue shutdown!')
        
        self.tls.info('PyTasky shutdown completed!')   
        
        event.accept()    

    def bringConsoleToFocus(self):
        # Make sure it's visible
        self.ui.dckPtsStreamOut.show()
        # Raise it to front
        self.ui.dckPtsStreamOut.raise_()
        # Optionally set focus to its child widget
        self.ui.dckPtsStreamOut.widget().setFocus()

    def logTextDisplayUpdate(self, text):
        if not self.disableLogDisplay:
            self.ui.qsciPtsStreamOut.setCursorPosition(self.ui.qsciPtsStreamOut.lines(), 0)
            self.ui.qsciPtsStreamOut.insertAt(text, self.ui.qsciPtsStreamOut.lines(), 0)
            vsb = self.ui.qsciPtsStreamOut.verticalScrollBar()
            vsb.setValue(vsb.maximum())
            hsb = self.ui.qsciPtsStreamOut.horizontalScrollBar()
            hsb.setValue(0)
            
    def showInternalScriptEditor(self, scriptFile):
        self.currentScriptFile = scriptFile
        self.currentScriptContent = self.tls.getFileContent(self.currentScriptFile)
        self.currentScriptEditor = ptsScriptEditor.ScriptEditorWindow(self)
        self.currentScriptEditor.setWindowModality(Qt.ApplicationModal)
        self.currentScriptEditor.setText(self.currentScriptContent)
        self.currentScriptEditor.setWindowTitle(f"Editing - {self.currentScriptFile}")
        self.currentScriptEditor.show()        


if __name__ == "__main__":
    tls = kTools.KTools("PYTASKY", PyTaskyLookUps, "pytasky_config.json")
    app = QtWidgets.QApplication(sys.argv)
    appCore = core(app)
    appCore.showUI()
    atexit.register(appCore.__exit__)
    sys.exit(app.exec_())
