'''
@name: Displayer
@author:  kayma
@createdon: 16-Apr-2025
@description:

Display the given input to the log.
STYLE 1: Will simply prints between line formated with "----"
STYLE 2: Will simply prints between line formated with "<<>>"

#PTS_NODE
'''
__created__ = "16-Apr-2025"
__updated__ = "2025-07-17"
__author__ = "kayma"

NAME = "Displayer"

TAGS = ["custom", "iponly", "nooveride"]

PROPS = {}
PROPS["STYLE"] = "1"

import kTools; tls = kTools.KTools()

def ACTION(input):
    
    if PROPS['STYLE'] == "1":
        print("----------------------------")
        print(str(input))
        print("----------------------------")

    if PROPS['STYLE'] == "2":
        print("<<<<<<<<<<<<>>>>>>>>>>>>>")
        print(f"{input}")
        print("<<<<<<<<<<<<>>>>>>>>>>>>>")

    return None

