'''
@name: InputCopier
@author:  kayma
@createdon: 26-Jun-2025
@description:

Simple node duplicates the input and provide them as output via two output port.

#PTS_NODE
'''
__created__ = "16-Apr-2025"
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "InputCopier"

TAGS = ["custom", "nooveride"]

OUTPUTS = [ "out1", "out2" ]

PROPS = {}

import kTools; tls = kTools.KTools()

def ACTION(input):
    return input

