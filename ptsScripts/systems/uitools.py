'''
Created on 01-Apr-2025

This is a collection of pytasky provided system tools for users to build their custom tools. 
If you modify any of these scritps , It may impact the system's usual execution.
So Wrap this with your custom scripts and use them as you wish.

Important Note:
This tool collection will be used only within windows as it containts PyQt UI elements.
So if you use this collection, It wont run in ui-less unix style servers.

@author: kayma
'''
print("")
print("------------------------")
print("")
print("This is just a tool lib")
print("")
print(__doc__)
print("")
print("------------------------")
print("")

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt,)
from PyQt5.QtWidgets import (QAction, QDialog, QApplication, QTableWidget, QVBoxLayout, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget,)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5.Qt import QLineEdit
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
import Qt

import kTools
from kQt import kQtTools

tls = kTools.GetKTools()
qttls = kQtTools.KQTTools()

def getQtls():
    return qttls

def getFormInput(parent, inputDictForm):
    outputDict = {}
    def dataFetcher(tbl, winObj):
        nonlocal outputDict        
        for row in range(table.rowCount()):
            key = table.item(row, 0).text()  # Property name (column 1)
            value = table.item(row, 1).text()  # User-edited value (column 2)
            outputDict[key] = value  
        winObj.close()
    winObj = QtWidgets.QDialog(parent)
    winObj.setWindowTitle("PyTasky")
    layout = QVBoxLayout()
    winObj.setLayout(layout)
    qttls.createPropEditor(winObj, inputDictForm, dataFetcher, winObj) 
    winObj.exec_()
    return outputDict

def createUiWindow(parent, uiFileName):
    winObj = QtWidgets.QDialog(parent)
    winObj.setWindowTitle("PyTasky")
    uiObject = loadUi(uiFileName, winObj)
    uiObject.setModal(True)
    return winObj

def showUiWindow(uiObject):
    try:
        uiObject.exec_()
    except Exception as e:
        print("error", e )