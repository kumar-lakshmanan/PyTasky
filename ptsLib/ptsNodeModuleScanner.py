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
from inspect import getmodule
from PyQt5.uic import loadUi
from NodeGraphQt import NodeGraph
from NodeGraphQt import BaseNode
from NodeGraphQt import BaseNodeCircle
from NodeGraphQt import GroupNode

from pathlib import Path
from kQt import kQtTools
import kTools
import json

class PTSNodeModuleScanner(object):

    def __init__(self, console=None):
        self.tls = kTools.KTools()
        self.console = console
        self.ptsNodesPath = self.tls.getSafeConfig(['pts', 'nodesPath'])
        self.allNodes = {}
        self.sysNodes = {}
        self.customNodes = {}

    def _getQTBaseNode(self, name=""):
        if name == "Circle":
            return BaseNodeCircle
        elif name == "Box":
            return GroupNode
        else:
            return BaseNode

    def _isItSystemNode(self, nodeTags):
        return self._isTagPresentInTags('sys', nodeTags) and not self._isTagPresentInTags('custom', nodeTags)

    def _isTagPresentInTags(self, searchTag, tagList):
        return searchTag.strip().lower() in (s.strip().lower() for s in tagList)

    def _generateDynamicConstructor(self, ips, ops, props):
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

    def generateNodeModule(self, nodeModuleName, nodeName, nodeDesc, ips, ops, props, tags=["custom"], splprops={}):
        attrb = {}
        attrb['NODE_MODULENAME'] = nodeModuleName
        attrb['NODE_NAME'] = nodeName
        attrb['NODE_DESC'] = nodeDesc
        attrb['NODE_TAGS'] = tags
        attrb['NODE_SPLPROPS'] = splprops
        attrb['__init__'] = self._generateDynamicConstructor(ips, ops, props)
        qtNodeModule = self._getQTBaseNode(splprops['NodeStyle'] if 'NodeStyle' in splprops else None)
        return type(nodeModuleName, (qtNodeModule,), attrb)

    def scanNodeModuleFolder(self):
        advConfig = {}
        advConfig['silentIgnoredFileInfo'] = 1
        nodeModFiles = self.console.scanModuleFiles(self.ptsNodesPath, ignoreFileNameHasText=['__init__'], advConfig=advConfig)
        for nodeModName in nodeModFiles.keys():
            _module =  nodeModFiles[nodeModName][0]
            _modName = _module.__name__
            _name = _module.NAME
            _desc = _module.__doc__
            _tags = _module.TAGS if hasattr(_module, 'TAGS') else ['custom']
            _ips = _module.INPUTS if hasattr(_module, 'INPUTS') else []
            _ops = _module.OUTPUTS if hasattr(_module, 'OUTPUTS') else []
            if len(_ips) == 0 and len(_ops) == 0:
                self.tls.error(f"Node [{_name}] has no info about INPUT or OUTPUT. Unable to add it.")
                continue
            _props = _module.PROPS if hasattr(_module, 'PROPS') else {}
            _splProps = _module.SPLPROPS if hasattr(_module, 'SPLPROPS') else {}
            newClass = self.generateNodeModule(_modName, _name, _desc, _ips, _ops, _props, _tags, _splProps)
            setattr(newClass, 'NODE_MODULE', _module)
            self.tls.addOnlyUniqueToDict(self.allNodes, _name, newClass, forceAddLatest=1)
            if self._isItSystemNode(_tags):
                self.tls.addOnlyUniqueToDict(self.sysNodes, _name, newClass, forceAddLatest=1)
            else:
                self.tls.addOnlyUniqueToDict(self.customNodes, _name, newClass, forceAddLatest=1)


if __name__ == "__main__":

    import os, sys
    KLIBPATH = 'G:/pyworkspace/kpylib'
    KCONFIG = 'G:/pyworkspace/PyTasky/config.json'
    if not 'KCONFIG' in os.environ : os.environ['KCONFIG'] = KCONFIG
    if not 'KLIBPATH' in os.environ : os.environ['KLIBPATH'] = KLIBPATH
    for eachDependency in os.environ['KLIBPATH'].split(';'): sys.path.append(eachDependency.strip())

    print("test")
    nm = PTSNodeModuleScanner()
    nm.scanNodeModuleFolder()
    print(nm.sysNodes)
    print(nm.customNodes)
    print(nm.allNodes['Adder'])
    mod = nm.allNodes['Adder'].NODE_MODULE
    nm.console.getModule(mod)





