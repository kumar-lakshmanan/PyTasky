'''
@name: Arithmatic
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

NAME = "Arithmatic"

TAGS = ["custom"]

INPUTS = [ "in1", "in2" ]
OUTPUTS = [ "out" ]

PROPS = {}
PROPS["ADD"] = "1"
PROPS["SUB"] = "0"
PROPS["MUL"] = "0"
PROPS["DIV"] = "0"

import kTools; tls = kTools.KTools()

def ACTION(input):
    tls.publishSignal("flowevent", f"--Arithmatic Running {input}--")
    
    in1 = int(input["in1"] if 'in1' in input else 1)
    in2 = int(input["in2"] if 'in2' in input else 2)
    
    if PROPS['ADD'] == "1":
        output = in1 + in2

    if PROPS['SUB'] == "1":
        output = in1 - in2

    if PROPS['MUL'] == "1":
        output = in1 * in2

    if PROPS['DIV'] == "1":
        output = in1 / in2                
    
    return output
