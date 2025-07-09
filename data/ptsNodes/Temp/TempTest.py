'''
@name: 
@author: kayma
@createdon: "2025-07-25"
@description:

#PTS_NODE
'''
__created__ = "2025-04-21" 
__updated__ = "2025-07-09"
__author__ = "kayma"

NAME = "TempTest"

TAGS = ["custom"]

INPUTS = [ "in1", "in2" ]
OUTPUTS = [ "out" , "out2" ]

PROPS = {}

import kTools; tls = kTools.KTools()

def ACTION(input):
    
    in1 = input["in1"]
    in2 = input["in2"]
    
    output = in1 + in2                
    
    return output
