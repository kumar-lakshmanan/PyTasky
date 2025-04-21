'''
Created on 21-Mar-2025



@author: kayma
'''
import systems.tools as stls
import systems.uitools as utls

NAME = "UiLaunch"

TAGS = ["custom","ui"]

PROPS = {}
PROPS["UIFile"] = "G:/pyworkspace/PyTasky/ptsUIs/createNode.ui"
PROPS["UILogicScript"] = "systems.customize.nodeCreaterCustoms"
PROPS["UICustomizerFunction"] = "CustomizingAction"
PROPS["UIDataFetcherFunction"] = "GetUIData"

def ACTION(request):
    uiDataFetcherFn = None
    output = {}
    def winClose():
        nonlocal output
        nonlocal uiDataFetcherFn
        nonlocal request
        nonlocal uiWin
        output = uiDataFetcherFn(uiWin, request)
        
    if PROPS["UILogicScript"]:
        logicModule = stls.getCustomModule(PROPS["UILogicScript"])
        if hasattr(logicModule, PROPS["UICustomizerFunction"]) and hasattr(logicModule, PROPS["UIDataFetcherFunction"]):
            uiWin = utls.createUiWindow(PTS.ui, PROPS["UIFile"])
            uiWin.finished.connect(winClose)
            uiCustomizerFn = getattr(logicModule, PROPS["UICustomizerFunction"])
            uiDataFetcherFn = getattr(logicModule, PROPS["UIDataFetcherFunction"])
            uiCustomizerFn(uiWin, request)
            utls.showUiWindow(uiWin)
        else:
            stls.info(f'Error! No fn {PROPS["UICustomizerFunction"]} or {PROPS["UICustomizerFunction"]} found in {logicModule}')
    else:
        stls.info(f'Error! No logic script mentioned {PROPS["UILogicScript"]}')
    
    return output
