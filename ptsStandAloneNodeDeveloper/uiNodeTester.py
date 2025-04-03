'''

'''
import os, sys
KCONFIG = 'G:/pyworkspace/PyTasky/config.json'
KDEPENDS = 'G:/pyworkspace/kpylib;G:/pyworkspace/PyTasky/ptsScripts'
if not 'KDEPENDS' in os.environ  : os.environ['KDEPENDS'] = KDEPENDS
if not 'KCONFIG' in os.environ  : os.environ['KCONFIG'] = KCONFIG
for eachDependency in os.environ['KDEPENDS'].split(';'): sys.path.append(eachDependency.strip())

from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5.Qt import QLineEdit
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt,)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.QtWidgets import (QAction, QLabel, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget,)
from PyQt5.uic import loadUi
from kQt import kQtTools
import kTools

#------------------

import sys

#fileToTest = 'ptsScripts/helloworld_ui.py'
fileToTest = sys.argv[1] if len(sys.argv)>1 else 'G:/pyworkspace/PyTasky/ptsNodes/uinodes/UiLaunch.py'
fileToTest = 'ptsNodes/uinodes/UiLaunch.py'

workingDir = 'G:/pyworkspace/PyTasky'

#------------------
if __name__ == "__main__":
    tls = kTools.GetKTools()
    app = QtWidgets.QApplication(sys.argv)
    PTS = QtWidgets.QMainWindow()
    PTS.show()

    PTS.setWindowTitle("Dummy Window")
    PTS.setGeometry(100, 100, 400, 300)

    label = QLabel("Close to Exit!", PTS)
    label.move(150, 130)

    tls.console.runCode(f'import os; os.chdir("{workingDir}")')
    tls.console.updateLocals('PTS_UI', PTS)
    tls.console.runScript(fileToTest)
    sys.exit(app.exec_())