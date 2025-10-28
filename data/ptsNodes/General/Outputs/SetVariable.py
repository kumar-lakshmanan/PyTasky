'''
@name: SetVariable
@author:  unknown
@createdon: 2025-10-08
@description:

This will set the COMMON variable with given value for the sub-variable mentioned in VariableName
 
#PTS_NODE
'''
__created__ = "2025-10-08" 
__updated__ = "2025-10-08"
__author__ = "unknown"

NAME = "SetVariable"

TAGS = ["custom","iponly","nooveride"]

INPUTS = [ "data" ]

PROPS = { "VariableName" : "var1" }

import kTools; tls = kTools.KTools()

def ACTION(input):
	tls.info(f"Setting variable {PROPS['VariableName']} with value {input['data']}")
	tls.info(f"COMMON[\"{PROPS['VariableName']}\"] should have value {input['data']}")
	COMMON[PROPS["VariableName"]] = input["data"]
	return None