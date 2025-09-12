'''
@name: DictVariable
@author:  kayma
@createdon: 24-Apr-2025
@description:

DictVariable's will holds a dictonary (key/value pair) , allow users to enter the value in it and it can be passed as input to any node that accepts integer.

#PTS_NODE
'''
__created__ = "24-Apr-2025"
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "DictVariable"

TAGS = [ "custom" , "oponly", "nooveride" ]

PROPS = {}
PROPS["Value"] = '{"myjson":{"response":200}}'

import kTools; tls = kTools.KTools()

def ACTION(input):
    return dict(PTS.console.runCommand(PROPS["Value"]))

