'''
Created on 21-Mar-2025



@author: kayma
'''
import kTools; tls = kTools.GetKTools()

NAME = "Variable"

TAGS = ["custom", "multiop"]

PROPS = {}
PROPS["Value"] = "Some Value"

def ACTION(request):
    return PROPS["Value"]
