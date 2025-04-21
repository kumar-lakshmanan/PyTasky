'''
Created on 21-Mar-2025

@author: kayma
'''
import kTools; tls = kTools.GetKTools()

NAME = "Concater"

TAGS = ["custom"]

INPUTS = [ "in1", "in2" ]

PROPS = {}
PROPS["ConcaterString"] = "-"

def ACTION(request):
    output = str(request['in1']) + str(PROPS["ConcaterString"]) + str(request['in2'])
    return output
