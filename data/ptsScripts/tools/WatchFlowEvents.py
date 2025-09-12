'''
@name:
@author:  kayma
@createdon: 05-May-2025
@description:




'''
__created__ = "05-May-2025"
__updated__ = "2025-07-22"
__author__ = "kayma"

import kTools; tls = kTools.KTools()
from kQt import kQtTools; qttls = kQtTools.KQTTools()

advParam = {}
advParam['isModel'] = False

winObj,uiObj = qttls.createUiDialog("data/ptsUIs/listWin.ui", None, "Watch Flow Events")

qttls.showUiDialog(winObj, advParam)

def flowEventCapture(data):
    if data:
        qttls.listAdder(uiObj.listWidget, data)

tls.subscribeToSignal("flowevent", flowEventCapture)
