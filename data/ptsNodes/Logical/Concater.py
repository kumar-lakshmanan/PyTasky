'''
@name: Concater
@author:  kayma
@createdon: 21-Apr-2025
@description:

String concater will concate two input.
Will use the concater props while concating.

#PTS_NODE
'''
__created__ = "2025-04-21"
__updated__ = "2025-07-07"
__author__ = "kayma"

NAME = "Concater"

TAGS = ["custom"]

INPUTS = [ "in1", "in2" ]

PROPS = {}
PROPS["ConcaterString"] = "-"

import kTools; tls = kTools.KTools()

def ACTION(input):
    output = str(input['in1']) + str(PROPS["ConcaterString"]) + str(input['in2'])
    return output
