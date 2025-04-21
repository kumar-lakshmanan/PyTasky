'''
Loops response will be dict of looped items eg:

{'item1': {'out': 'Some Value-item1'}, 'item2': {'out': 'Some Value-item2'}, 'item3': {'out': 'Some Value-item3'}}
it will be converted to list ignoreing the top key

Created on 21-Mar-2025


@author: kayma
'''
import kTools; tls = kTools.GetKTools()

NAME = "LoopResponseToList"

TAGS = ["custom"]

INPUTS = [ "in" ]

PROPS = {}

def ACTION(request):
    ret = list(request['in'].values())
    return ret
    