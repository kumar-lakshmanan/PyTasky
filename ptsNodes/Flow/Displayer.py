'''
Created on 21-Mar-2025

STYLE
1 - LOG STYLE
2 - SIMPLE STYLE

@author: kayma
'''
import kTools; tls = kTools.GetKTools()

NAME = "Displayer"

TAGS = ["custom","noop"]

INPUTS = [ "in" ]

PROPS = {}
PROPS["STYLE"] = "1"

def ACTION(request):
    if PROPS['STYLE'] == "1":
        tls.info(f"[Disp]: {request['in']}")

    if PROPS['STYLE'] == "2":
        print(f"[Disp] >> {request['in']}")
    return None

