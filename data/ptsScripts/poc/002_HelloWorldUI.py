'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting
@author: kayma
'''


import kTools 
from kQt import kQtTools
import kCodeExecuter

tls = kTools.KTools()
qttls = kQtTools.KQTTools()
console = kCodeExecuter.KCodeExecuter()

def btnClicked():
    print("ok")

uiWin = qttls.createUiDialog("data/ptsUIs/mywin.ui", PTS.ui)
            
print(uiWin)

uiWin.pushButton.clicked.connect(btnClicked)

qttls.showUiDialog(uiWin[0])