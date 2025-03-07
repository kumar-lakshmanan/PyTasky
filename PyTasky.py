'''
Created on 07-Mar-2025

@author: kayma
'''
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
from ptsLib.ptsUi import ptsMainWindow
from ptsLib.ptsNodes import ndInputs
from ptsLib.ptsNodes import ndOutputs
from ptsLib.ptsNodes import ndWebCall 

class core():

    def __init__(self, parent = None):
        super().__init__()
        self.tls = kTools.GetKTools()
        self.qttls = kQtTools.KQTTools()
        
        #Loading UI...
        self.ui = ptsMainWindow.core()
    
    def showUI(self):
        self.ui.show()

if __name__ == "__main__":
    tls = kTools.GetKTools("pytasky")    
    app = QtWidgets.QApplication(sys.argv)
    appCore = core()
    appCore.showUI()
    sys.exit(app.exec_())
