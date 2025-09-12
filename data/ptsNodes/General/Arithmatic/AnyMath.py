'''
@name: AnyMath
@author:  kayma
@createdon: 21-Apr-2025
@description:

Do logical any math operations. 
Set 1 to any one operation. First operation with 1 will take the precedence.
 
#PTS_NODE
'''
__created__ = "2025-04-21" 
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "AnyMath"

TAGS = ["custom"]

INPUTS = [ "in1", "in2" ]

PROPS = {}
PROPS["ADD"] = "1"
PROPS["SUB"] = "0"
PROPS["MUL"] = "0"
PROPS["DIV"] = "0"

import kTools; tls = kTools.KTools()

def ACTION(input):
    
    in1 = input["in1"]
    in2 = input["in2"]
    
    if PROPS['ADD'] == "1":
        output = in1 + in2

    if PROPS['SUB'] == "1":
        output = in1 - in2

    if PROPS['MUL'] == "1":
        output = in1 * in2

    if PROPS['DIV'] == "1":
        output = in1 / in2                
    
    return output
