'''
Created on 21-Mar-2025


@author: kayma
'''
import kTools; tls = kTools.GetKTools()

NAME = "Mathers"

INPUTS = [ "in1", "in2" ]
OUTPUTS = [ ("out",1) ]

PROPS = {}
PROPS["ADD"] = "1"
PROPS["SUB"] = "0"
PROPS["MUL"] = "0"
PROPS["DIV"] = "0"

def action(request={}):
    tls.info(f"Action Started {NAME}")
    
    in1 = int(request["in1"] if 'in1' in request else 1)
    in2 = int(request["in2"] if 'in2' in request else 1)
    tls.info(f"Mather {NAME} processing {in1} and {in2}")
    
    if PROPS['ADD'] == "1":
        output = in1 + in2

    if PROPS['SUB'] == "1":
        output = in1 - in2

    if PROPS['MUL'] == "1":
        output = in1 * in2

    if PROPS['DIV'] == "1":
        output = in1 / in2                
    
    return {'out' : output}
