'''
@name: FetchVariable
@author:  kayma
@createdon: 2025-10-08
@description:

Fetch a selected variable and output the value

#PTS_NODE
'''
__created__ = "2025-10-08"
__updated__ = "2025-10-08"
__author__ = "kayma"

NAME = "FetchVariable"

TAGS = ["custom", "oponly", "nooveride"]

PROPS = {}
PROPS["Variable"] = "COMMON"

import kTools; tls = kTools.KTools()

def ACTION(input):    
    return PTS.console.runCommand(PROPS["Variable"])

