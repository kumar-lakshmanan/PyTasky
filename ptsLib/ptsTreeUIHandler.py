'''
Created on 10-Mar-2025

@author: kayma
'''
import os

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, QSizePolicy)
from PyQt5.QtGui import ( QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython, QsciAPIs)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
import functools

from kQt import kQtTools
from kQt import kQtTreeWidget
import kTools

class TreeUIHandler():
    '''
        Will populate given treewidget with files.
        Allow interactions.
        Apply icons.
        APply custom file . folder filters.
    '''
    def __init__(self, parent=None, params={}):

        self.PTS = parent
        self.parentUi = self.PTS.ui
        self.tls = kTools.KTools()
        self.qttls = kQtTools.KQTTools()

        self.qtTree = kQtTreeWidget.TreeWidget()
        self.iconFolder = 'folder.png'
        self.iconScript = 'code.png'
        # self.contextMenuOpenSpace = ['Create Folder...','Open Scripts Folder','Open Sachthya Folder','','Refresh']
        # self.contextMenuFileItems = ['Execute','','Edit Script','|Edit GUI','','Delete']
        # self.contextMenuDirItems = ['Create GUI Script...','Create Console Script...','','Create Folder...']

        self.type = params['type']
        self.filePath = params['filePath']
        self.disallowedFolder = params['disallowedFolder'] #['__','.git']
        self.allowedFiles = params['allowedFiles'] #['.py']
        self.fileContentShouldHave = params['fileContentShouldHave']

        # self.enableDragDrop = params['enableDragDrop']
        # self.dragDropFn = params['dragDropFn']
        self.contextMenuOpenSpace = params['contextMenuOpenSpace']
        self.contextMenuFileItems = params['contextMenuFileItems']
        self.contextMenuDirItems = params['contextMenuDirItems']

        self.targetTreeWidget = params['targetTreeObject'] #self.parentUi.treePtsScripts

        self.menuSelectedFn = params['menuSelectedFn']
        self.dblClickFn = params['dblClickFn']

        self.targetTreeWidget.setDragEnabled(True)
        self.qttls.connectToRightClick(self.targetTreeWidget, self.popUpMenuBuilder)
        self.targetTreeWidget.itemDoubleClicked.connect(self.itemDblClicked)

    def itemDblClicked(self, item):
        label = str(item.text(0))
        fileFolder = str(item.data(0, QtCore.Qt.UserRole))
        typ = str(item.data(0, QtCore.Qt.UserRole+1))
        self.dblClickFn(label, fileFolder, typ, item)

    def popUpMenuBuilder(self, point):
        if not self.menuSelectedFn:
            self.tls.info("No context option!")
            return
        menu = self.contextMenuOpenSpace
        self.itm = self.targetTreeWidget.itemAt(point)
        label = None
        fileFolder = None
        typ = None
        if self.itm:
            label = str(self.itm.text(0))
            fileFolder = str(self.itm.data(0, QtCore.Qt.UserRole))
            typ = str(self.itm.data(0, QtCore.Qt.UserRole+1))
            if(typ=='file'):
                menu = self.contextMenuFileItems
            elif(typ=='dir'):
                menu = self.contextMenuDirItems
        else:
            self.itm = self.targetTreeWidget
        self.qttls.popUpMenu(self.targetTreeWidget, point, menu, self.menuSelectedFn, [self.type, label, fileFolder, typ, self.itm])

    def popUpMenuItemClicked(self, *arg):
        '''
    (['Execute', 0, <PyQt5.QtWidgets.QAction object at 0x0000026DF8E78040>, ['Script', 'script2', 'G:\\pyworkspace\\PyTasky\\ptsScripts\\servers\\rough\\script2.py', 'file', <PyQt5.QtWidgets.QTreeWidgetItem object at 0x0000026DF8E781F0>]], False)
    (['Create Folder...', 3, <PyQt5.QtWidgets.QAction object at 0x0000026DF8E78D30>, ['Script', 'servers', 'G:\\pyworkspace\\PyTasky\\ptsScripts\\servers\\rough\\servers', 'dir', <PyQt5.QtWidgets.QTreeWidgetItem object at 0x0000026DF8E78280>]], False)
    (
        ['Execute',
         0,
         <PyQt5.QtWidgets.QAction object at 0x0000026DF8E793F0>,
         ['Node', 'ndWebCall', 'G:\\pyworkspace\\PyTasky\\ptsLib\\ptsNodes\\ndWebCall.py', 'file', <PyQt5.QtWidgets.QTreeWidgetItem object at 0x0000026DF8E57A30>]
        ],

        False
    )
        '''
        optionName = arg[0]
        optionName = arg[0]
        print(arg)
        obj = arg[0][2]
        obj2 = arg[0][3][1]
        print(obj2)

    def _runFolderFilter(self, folderpath):
        for eachFilter in self.disallowedFolder:
            if (eachFilter.lower() in folderpath.lower()):
                return False
        return True

    def _runFileFilter(self, filepath):
        ext = os.path.splitext(filepath)
        return ext[1] in self.allowedFiles

    def loadTree(self):
        self.targetTreeWidget.clear()
        scriptsPath = self.filePath
        self.tls.info(f'Populating {self.type}(s)...')
        if not self.tls.isFolderExists(scriptsPath): self.tls.errorAndExit(f"Unable to populate: {scriptsPath}")
        for eachItem in os.listdir(scriptsPath):
            currentDirName = eachItem
            currentDirPath = os.path.join(scriptsPath,currentDirName)
            currentDirPath = os.path.abspath(currentDirPath)
            if self._runFolderFilter(currentDirPath):
                if os.path.isdir(currentDirPath):
                    rItem = self.qtTree.createItem(currentDirName, currentDirPath)
                    rItem.setData(0, QtCore.Qt.UserRole+1,  QtCore.QVariant('dir'))
                    self.qtTree.addNewRoot(self.targetTreeWidget, rItem)
                    self.qttls.setIconForItem(rItem,self.iconFolder)
                    self.populateCore(rItem, currentDirPath)
                else:
                    self.createScriptItem(currentDirPath)
        self.tls.info(f"{self.type}(s) Populated!")

    def populateCore(self, parentItem, searchPath):
        for eachItem in os.listdir(searchPath):
            currentDirName = eachItem
            currentDirPath = os.path.join(searchPath,currentDirName)
            if self._runFolderFilter(currentDirPath):
                if os.path.isdir(currentDirPath):
                    rItem = self.qtTree.createItem(currentDirName,currentDirPath)
                    rItem.setData(0, QtCore.Qt.UserRole+1,  QtCore.QVariant('dir'))
                    self.qttls.setIconForItem(rItem,self.iconFolder)
                    self.qtTree.addChild(rItem, parentItem)
                    self.populateCore(rItem, currentDirPath)
                else:
                    self.createScriptItem(currentDirPath, parentItem)

    def createScriptItem(self, plugFile, parentTreeItem=None):
        plugFile = os.path.abspath(plugFile)
        modName = os.path.basename(plugFile).replace(os.path.splitext(plugFile)[1], '')
        content = self.tls.getFileContent(plugFile)
        expecting = self.fileContentShouldHave
        if(expecting.lower() in content.lower() and self._runFileFilter(plugFile)):
            item = self.qtTree.createItem(modName, plugFile)
            item.setData(0, QtCore.Qt.UserRole+1, QtCore.QVariant('file'))
            self.qttls.setIconForItem(item,self.iconScript)
            self.tls.info(f'Adding {self.type}...' + str(plugFile))
            if(parentTreeItem is None):
                plugTreeItem = self.qtTree.addNewRoot(self.targetTreeWidget, item)
            else:
                plugTreeItem = self.qtTree.addChild(item, parentTreeItem)
        else:
            plugTreeItem = None
        return plugTreeItem