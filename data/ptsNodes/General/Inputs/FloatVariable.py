'''
@name: FloatVariable
@author:  kayma
@createdon: 24-Apr-2025
@description:

FloatVariable's will hold floating (decimal) value , allow users to enter the value in it and it can be passed as input to any node that accepts integer.

#PTS_NODE
'''
__created__ = "24-Apr-2025"
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "FloatVariable"

TAGS = [ "custom" , "oponly", "nooveride" ]

PROPS = {}
PROPS["Value"] = "150.6"

import kTools; tls = kTools.KTools()

def ACTION(input):
    return float(PROPS["Value"])

