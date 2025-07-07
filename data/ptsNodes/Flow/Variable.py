'''
@name: Variable
@author:  kayma
@createdon: 24-Apr-2025
@description:

Variable's value can be anything.
You shall have any values (everything will be considered string)
And it will be passed to connected nodes.
In Connected nodes. Make sure you use int() or str() explict conversion as per need.

#PTS_NODE
'''
__created__ = "24-Apr-2025"
__updated__ = "2025-07-07"
__author__ = "kayma"

NAME = "Variable"

TAGS = [ "custom" ]

OUTPUTS = ["out"]

PROPS = {}
PROPS["Value"] = "150"

import kTools; tls = kTools.KTools()

def ACTION(input):
    return PROPS["Value"]
