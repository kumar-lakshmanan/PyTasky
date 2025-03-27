'''
Created on 21-Mar-2025

@author: kayma
'''
import kTools; tls = kTools.GetKTools()

NAME = "Concater"

INPUTS = [ "in1", "in2" ]
OUTPUTS = [ ("out",1) ]

PROPS = {}
PROPS["ConcaterString"] = "-"

def action(request={}):
    tls.info(f"Action Started {NAME}")
    output = request['in1'] + request['in2']
    return {'out': output}
