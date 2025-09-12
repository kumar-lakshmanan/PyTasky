'''
@name: IntVariable
@author:  kayma
@createdon: 24-Apr-2025
@description:

IntVariable's will hold integer value , allow users to enter the value in it and it can be passed as input to any node that accepts integer.

#PTS_NODE
'''
__created__ = "24-Apr-2025"
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "IntVariable"

TAGS = [ "custom" , "oponly", "nooveride" ]

PROPS = {}
PROPS["Value"] = "150"

import kTools; tls = kTools.KTools()

def ACTION(input):
    return int(PROPS["Value"])

