'''
@name: Subract
@author:  kayma
@createdon: 21-Apr-2025
@description:

Do logical math subract operations.  in1 - in2
 
#PTS_NODE
'''
__created__ = "2025-04-21" 
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "Subract"

TAGS = ["custom"]

INPUTS = [ "in1", "in2" ]

PROPS = {}

import kTools; tls = kTools.KTools()

def ACTION(input):
    in1 = input["in1"]
    in2 = input["in2"]
    
    output = in1 - in2                
    
    return output
