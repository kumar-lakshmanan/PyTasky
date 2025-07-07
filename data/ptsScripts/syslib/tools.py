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
tls = kTools.KTools()

import kCodeExecuter
console = kCodeExecuter.KCodeExecuter()



def getTls():
    return tls

def info(msg):
    tls.info(msg)

def getCustomModule(modulePackage):
    return console.getModule(modulePackage)

def addToSystemPaths(paths):
    '''
    Add list of paths (string) to the system paths.
    '''
    console.cleanAndUpdateSysPaths(paths)

def getDictFromStr(strDict):
    return tls.convertDictStrToDict(strDict)

def getFileContent(fileName):
    return tls.getFileContent(fileName)

def setFileContent(fileName, content):
    return tls.writeFileContent(fileName, content)

if __name__ == "__main__":
    print("Local Test")
    d = '{"Prop1":"Val1", "Prop2":"Val2"}'
    d = """{ "NAME" : "Sample" ,  "INPUTS" : ["in1","in2"] , "PROPS" : {}}"""
    r = getDictFromStr(d)
    print(r)
