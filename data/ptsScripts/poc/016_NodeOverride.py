"""
THis script is used for overriding the exisiting node 

Override exisitng node logic with custom script.
"""
import kTools; tls = kTools.KTools()

def ACTION(input):
    in1 = input["in1"]
    in2 = input["in2"]
    output = in1 + in2 + 250
    return output
