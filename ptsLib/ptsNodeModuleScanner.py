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

    def __init__(self):        
        self.tls = kTools.GetKTools()
        self.ptsNodesPath = "G:/pyworkspace/PyTasky/ptsNodes"
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
        nodeModFiles = self.tls.console.scanModuleFiles(self.ptsNodesPath, ignoreFileNameHasText=['__init__'], advConfig=advConfig)
        for nodeModName in nodeModFiles.keys():
            _module =  nodeModFiles[nodeModName][0]
            _modName = _module.__name__            
            _name = _module.NAME
            _desc = _module.__doc__
            _tags = _module.TAGS if hasattr(_module, 'TAGS') else ['custom']
            _ips = _module.INPUTS if hasattr(_module, 'INPUTS') else []
            _ops = _module.OUTPUTS if hasattr(_module, 'OUTPUTS') else self._getDefaultOutputs(_tags)
            _props = _module.PROPS if hasattr(_module, 'PROPS') else {}      
            _splProps = _module.SPLPROPS if hasattr(_module, 'SPLPROPS') else {} 
            newClass = self.generateNodeModule(_modName, _name, _desc, _ips, _ops, _props, _tags, _splProps)
            setattr(newClass, 'NODE_MODULE', _module)
            self.tls.addOnlyUniqueToDict(self.allNodes, _name, newClass, forceAddLatest=1)
            if self._isItSystemNode(_tags):
                 self.tls.addOnlyUniqueToDict(self.sysNodes, _name, newClass, forceAddLatest=1)
            else:
                 self.tls.addOnlyUniqueToDict(self.customNodes, _name, newClass, forceAddLatest=1)

    def _getDefaultOutputs(self, tagList):
        DefaultOutPortName = self.tls.cfg['pts']['defaultOutPortName']
        if not self._isTagPresentInTags('noop', tagList):
            if self._isTagPresentInTags('multiop', tagList):
                return [(DefaultOutPortName,1)]
            else:
                return [DefaultOutPortName]
        return []

if __name__ == "__main__":

    import os, sys
    KCONFIG = 'G:/pyworkspace/PyTasky/config.json'
    KDEPENDS = 'G:/pyworkspace/kpylib;G:/pyworkspace/PyTasky/ptsScripts;G:/pyworkspace/PyTasky'
    if not 'KDEPENDS' in os.environ : os.environ['KDEPENDS'] = KDEPENDS
    if not 'KCONFIG' in os.environ : os.environ['KCONFIG'] = KCONFIG
    for eachDependency in os.environ['KDEPENDS'].split(';'): sys.path.append(eachDependency.strip())
    
    print("test")    
    nm = PTSNodeModuleScanner()
    nm.scanNodeModuleFolder()
    print(nm.sysNodes)
    print(nm.customNodes)
    print(nm.allNodes['Adder'])
    mod = nm.allNodes['Adder'].NODE_MODULE
    nm.tls.console.getModule(mod)
    
    
    
    
    
    