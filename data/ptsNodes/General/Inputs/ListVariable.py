'''
@name: ListVariable
@author:  kayma
@createdon: 24-Apr-2025
@description:

ListVariable's will hold list of values , allow users to enter the value in it and it can be passed as input to any node that accepts integer.

#PTS_NODE
'''
__created__ = "24-Apr-2025"
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "ListVariable"

TAGS = [ "custom" , "oponly", "nooveride" ]

PROPS = {}
PROPS["Value"] = "[1,2,3,4,'abc','xyz']"

import kTools; tls = kTools.KTools()

def ACTION(input):    
    return list(PTS.console.runCommand(PROPS["Value"]))

