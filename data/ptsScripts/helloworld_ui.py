'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting
@author: kayma
'''
print("This is just a tool lib")
print("")
print(__doc__)

import kTools 
from kQt import kQtTools
import kCodeExecuter

tls = kTools.KTools()
qttls = kQtTools.KQTTools()
console = kCodeExecuter.KCodeExecuter()

# Simple Print
print(PTS.ui)

def btnClicked():
    print("ok")

uiWin = qttls.createUiDialog("data/ptsUIs/mywin.ui", PTS.ui)
            
print(uiWin)

#uiWin.pushButton.clicked.connect(btnClicked)

qttls.showUiDialog(uiWin)