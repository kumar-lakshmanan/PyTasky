'''
@name: WaitAndGo
@author:  kayma
@createdon: 26-Jun-2025
@description:

WaitAndGo helps to extend the flow with out doing any action, instead of,
it will wait for all inputs to complete and then only it will proceed next.
Use it for combining all inputs and go to next step.
in next step you will get all your inputs as tuple.

#PTS_NODE
'''
__created__ = "16-Apr-2025"
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "WaitAndGo"

TAGS = ["custom", "nooveride"]

INPUTS = [ "in1", "in2"]

PROPS = {}

import kTools; tls = kTools.KTools()

def ACTION(input):    
    return (input['in1'][tls.lookUp.inputPortName], input['in2'][tls.lookUp.inputPortName])

