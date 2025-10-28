'''
@name: pyTaskyCustomizer
@author:  kumar
@createdon: 2025-10-15
@description:

pyTaskyCustomizer DESC 

'''
__created__ = "2025-10-15" 
__updated__ = "2025-10-16"
__author__ = "kumar"

print("")
print("PyTasky Customized")
print("")
print(__doc__)

import kTools 
from kQt import kQtTools
import kCodeExecuter

tls = kTools.KTools()
qttls = kQtTools.KQTTools()


winObj, uiObj = qttls.createUiDialog("data/ptsUIs/tools/pyTaskyCustomizer.ui", PTS.ui)

#doRefreshTrees()
#doConsoleClean()
print(winObj, uiObj)

def doConsoleClean():	
	PTS.ui.qsciPtsStreamOut.setText("")
	print("Console Cleaned")

def doRefreshTrees():
	PTS.MainQueue.put({ "action" : "flow_start" , "params" :  {"flowFile" : 'G:/pyworkspace/PyTasky/data/ptsFlows/arithmatic.flow'} })
	print("Refresh Tree")
uiObj.pushButton.clicked.connect(doConsoleClean)
uiObj.pushButton_2.clicked.connect(doRefreshTrees)

qttls.showUiDialog(winObj)