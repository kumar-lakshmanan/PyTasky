'''
Created on 21-Mar-2025

STYLE
1 - LOG STYLE
2 - SIMPLE STYLE

@author: kayma
'''
import kTools; tls = kTools.GetKTools()

NAME = "Displayer"

INPUTS = [ "in1" ]

PROPS = {}
PROPS["STYLE"] = "1"

def ACTION(request):
    tls.info(f"Action Started {NAME}")
    
    in1 = request["in1"] 
    
    if PROPS['STYLE'] == "1":
        tls.info(f"[Disp]: {in1}]]")

    if PROPS['STYLE'] == "2":
        print(f"[Disp] >> {in1}")
    
    return {'out' : None}

