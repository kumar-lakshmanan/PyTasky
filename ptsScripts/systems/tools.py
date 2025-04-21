'''
Created on 01-Apr-2025

This is a collection of pytasky provided system tools for users to build their custom tools.
If you modify any of these scritps , It may impact the system's usual execution.
So Wrap this with your custom scripts and use them as you wish.

Important Note:
This tool collection will be used for independent execution inside ui-less unix style servers too.
So no PyQt UI elements or related object should be used here

@author: kayma
'''
# print("")
# print("------------------------")
# print("")
# print("This is just a tool lib")
# print("")
# print(__doc__)
# print("")
# print("------------------------")
# print("")

import ast
import json
import kTools
tls = kTools.GetKTools()

def convertStrToObject(inpStr):
    return ast.literal_eval(inpStr)
    
def getTls():
    return tls
    
def info(msg):
    tls.info(msg)
    
def getCustomModule(modulePackage):
    return tls.console.getModule(modulePackage)
    
def addToSystemPaths(paths):
    '''
    Add list of paths (string) to the system paths.
    '''
    tls.console.cleanAndUpdateSysPaths(paths)

def getDictFromStr(strDict):
    return tls.convertDictStrToDict(strDict)
        
if __name__ == "__main__":
    print("Local Test")
    d = '{"Prop1":"Val1", "Prop2":"Val2"}'
    d = """{ "NAME" : "Sample" ,  "INPUTS" : ["in1","in2"] , "PROPS" : {}}"""
    r = getDictFromStr(d)
    print(r)
