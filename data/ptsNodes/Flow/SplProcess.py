'''
@name: SplProcess
@author:  kayma
@createdon: 26-Jun-2025
@description:

WaitAndGo helps to extend the flow with out doing any action, instead of,
it will wait for all inputs to complete and then only it will go.

Use it for combining all inputs and go to next step.
in next step you will get all your inputs.

#PTS_NODE
'''
__created__ = "16-Apr-2025"
__updated__ = "2025-07-10"
__author__ = "kayma"

NAME = "SplProcess"

TAGS = ["custom"]

import kTools; tls = kTools.KTools()

def ACTION(input):
    print(input)    
    return input