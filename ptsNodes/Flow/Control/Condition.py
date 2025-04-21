'''
Check condition and use only the true path and ignore the false path

Created on 16-Apr-2025
@author: kayma
'''
NAME = "Condition"

TAGS = ["sys","condition"]

INPUTS = [ ("inp",0) ]

OUTPUTS = [ "True", "False"  ]

PROPS = {"condition":True}

SPLPROPS = {}
SPLPROPS["NodeStyle"] = "Circle"   #Default or Box or Circle 

def ACTION(request):
    return None