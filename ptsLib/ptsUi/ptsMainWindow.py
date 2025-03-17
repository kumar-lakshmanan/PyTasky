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
import Qt

import kTools 
from kQt import kQtTools


class PTSMainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        super().__init__()
        self.tls = kTools.GetKTools()
        self.qttls = kQtTools.KQTTools()
        
        self.tls.info('Preparing GUI...')
        QtWidgets.QMainWindow.__init__(self)		
        self.uiFile = sys.modules[__name__].__file__
        self.uiFile = self.uiFile.replace(".py", ".ui")        
        loadUi(self.uiFile, self)

if __name__ == "__main__":
    tls = kTools.GetKTools("pytasky")    
    app = QtWidgets.QApplication(sys.argv)
    appwin = PTSMainWindow()
    appwin.show()
    sys.exit(app.exec_())
