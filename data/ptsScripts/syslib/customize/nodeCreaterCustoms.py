'''
Created on 03-Apr-2025

@author: kayma
'''
uiWin = None

def CustomizingAction(*arg):
    uiWin = arg[0]
    print("Customizing", arg)

def GetUIData(*arg):
    uiWin = arg[0]    
    val = uiWin.lineEdit.displayText()
    print("Fetchign data", arg)
    return {"more": f"This is output {arg}, {val}"}