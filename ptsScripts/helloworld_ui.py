'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting 
@author: kayma
'''
print("This is just a tool lib")
print("")
print(__doc__)

import importlib, os, sys

import systems.tools as stls
import systems.uitools as utls

importlib.reload(stls)
importlib.reload(utls)

print(os.path.abspath(os.path.curdir))



# MAKING Use of custom path
paths = []
paths.append("G:/pyworkspace/PyTasky/ptsNodes")
stls.addToSystemPaths(paths)

# Simple Print
print(PTS_UI)



def btnClicked():
    print("ok")





# MAKING Use of node modules
uiWin = utls.readyUiWindow(PTS_UI,"ptsScripts/users/mywin.ui")
print(uiWin)

uiWin.pushButton.clicked.connect(btnClicked)

utls.showUiWindow(uiWin)


