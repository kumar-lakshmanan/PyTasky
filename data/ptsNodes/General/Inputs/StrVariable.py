'''
@name: StrVariable
@author:  kayma
@createdon: 24-Apr-2025
@description:

StrVariable's will hold String value , allow users to enter the value in it and it can be passed as input to any node that accepts integer.

#PTS_NODE
'''
__created__ = "24-Apr-2025"
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "StrVariable"

TAGS = [ "custom" , "oponly", "nooveride" ]

PROPS = {}
PROPS["Value"] = "Text"

import kTools; tls = kTools.KTools()

def ACTION(input):
    return str(PROPS["Value"])

