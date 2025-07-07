'''
@name: LoopResponseToList
@author:  kayma
@createdon: 16-Apr-2025
@description:

Loops response will be dict of looped items eg:

{'item1': {'out': 'Some Value-item1'}, 'item2': {'out': 'Some Value-item2'}, 'item3': {'out': 'Some Value-item3'}}
it will be converted to list ignoreing the top key

#PTS_NODE
'''
__created__ = "16-Apr-2025" 
__updated__ = "2025-07-07"
__author__ = "kayma"

NAME = "LoopResponseToList"

TAGS = ["custom"]

INPUTS = [ "in" ]

OUTPUTS = [ "out" ]

PROPS = {}

import kTools; tls = kTools.KTools()

def ACTION(input):
    ret = list(input['in'].values())
    return ret
    