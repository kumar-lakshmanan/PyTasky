'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting
@author: kayma
'''
print("This is just a tool lib")
print("")
print(__doc__)

import os, sys, importlib
import kTools; tls = kTools.KTools()
from syslib import mytools
importlib.reload(mytools)

# Simple Print
print(PTS)

def btnClicked():
    print("ok")

parent = mytools.getSharedObj("PTS_UI")
uiWin = mytools.createUiWindow(parent,"data/ptsUIs/mywin.ui")
print(uiWin)

uiWin.pushButton.clicked.connect(btnClicked)

mytools.showUiWindow(uiWin)
