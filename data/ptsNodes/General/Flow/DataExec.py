'''
@name: DataExec
@author:  kayma
@createdon: 26-Jun-2025
@description:

Evaluvates and fetch the date and transfers as output. 
Can convert data type , select any past output data and send as output.

#PTS_NODE
'''
__created__ = "16-Apr-2025"
__updated__ = "2025-08-07"
__author__ = "kayma"

NAME = "DataExec"

TAGS = ["custom","shareop", "nooveride"]

PROPS = {"output": "int(data['Variable 1-out'])"}

import kTools 
import kCodeExecuter
tls = kTools.KTools()
console = kCodeExecuter.KCodeExecuter()

def ACTION(input):    
    return PTS.console.runCommand(PROPS["output"])