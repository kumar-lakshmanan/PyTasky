'''
@name: UiLaunch
@author:  kayma
@createdon: 21-Apr-2025
@description:

Will launch an ui window which provided at UIFile.
Then will make use of script mentioned in UILogicScript.
And will run the function mentioned in UICustomizerFunction.
You can use it to customize your UI like button action,  input text box writing and many more.
When you close the window by any means. 
Function mentioned in UIDataFetcherFunction will be called. 
You can read text box value form value and other values and compose your return statement and return to next node.
 
#PTS_NODE
'''
__created__ = "2025-04-21" 
__updated__ = "2025-07-07"
__author__ = "kayma"

NAME = "UiLaunch"

TAGS = ["custom","ui"]

PROPS = {}
PROPS["UIFile"] = "G:/pyworkspace/PyTasky/ptsUIs/createNode.ui"
PROPS["UILogicScript"] = "systems.customize.nodeCreaterCustoms"
PROPS["UICustomizerFunction"] = "CustomizingAction"
PROPS["UIDataFetcherFunction"] = "GetUIData"

# import syslib.tools as stls
# import syslib.uitools as utls
import kTools; tls = kTools.KTools()

def ACTION(input):
    uiDataFetcherFn = None
    output = {}
    def winClose():
        nonlocal output
        nonlocal uiDataFetcherFn
        nonlocal input
        nonlocal uiWin
        output = uiDataFetcherFn(uiWin, input)
        
    if PROPS["UILogicScript"]:
        logicModule = stls.getCustomModule(PROPS["UILogicScript"])
        if hasattr(logicModule, PROPS["UICustomizerFunction"]) and hasattr(logicModule, PROPS["UIDataFetcherFunction"]):
            uiWin = utls.createUiWindow(PTS.ui, PROPS["UIFile"])
            uiWin.finished.connect(winClose)
            uiCustomizerFn = getattr(logicModule, PROPS["UICustomizerFunction"])
            uiDataFetcherFn = getattr(logicModule, PROPS["UIDataFetcherFunction"])
            uiCustomizerFn(uiWin, input)
            tls.publishSignal("flowevent", f"--------------UI WINDOW OPEN... {PROPS}")
            utls.showUiWindow(uiWin)
            tls.publishSignal("flowevent", f"--------------UI WINDOW CLOSE... {PROPS}")
        else:
            stls.info(f'Error! No fn {PROPS["UICustomizerFunction"]} or {PROPS["UICustomizerFunction"]} found in {logicModule}')
    else:
        stls.info(f'Error! No logic script mentioned {PROPS["UILogicScript"]}')
    
    return output
