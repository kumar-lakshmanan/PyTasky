'''
@name: Adder
@author:  kayma
@createdon: 21-Apr-2025
@description:

Do logical math operations. 
Set 1 to any one operation. First operation with 1 will take the precedence.
 
#PTS_NODE
'''
__created__ = "2025-04-21" 
__updated__ = "2025-07-07"
__author__ = "kayma"

NAME = "Adder"

TAGS = ["custom"]

INPUTS = [ "in1", "in2" ]
OUTPUTS = [ "out" ]

PROPS = {}

import kTools; tls = kTools.KTools()

def ACTION(input):
    tls.publishSignal("flowevent", f"--Adder Running {input}--")
    
    in1 = input["in1"]
    in2 = input["in2"]
    
    output = in1 + in2                
    
    return output
