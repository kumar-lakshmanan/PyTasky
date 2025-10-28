'''
@name: ShowVariable
@author:  kayma
@createdon: 16-Apr-2025
@description:

Display the given input to the log.
STYLE 1: Will simply prints between line formated with "----"
STYLE 2: Will simply prints between line formated with "<<>>"

#PTS_NODE
'''
__created__ = "16-Apr-2025"
__updated__ = "2025-10-08"
__author__ = "kayma"

NAME = "ShowVariable"

TAGS = ["custom", "iponly", "nooveride"]

PROPS = {}
PROPS["STYLE"] = "1"

import kTools; tls = kTools.KTools()

def ACTION(input):
    
    print("-----------------------------")
    print("Showing variable and values available")
    print("-----------------------------")
    
    print("NAME")
    print(NAME)
    print("-------")    
    
    print("INPUT")
    print(input)
    print("-------")
    
    print("PROPS")
    print(PROPS)
    print("-------")    

    print("FLOWPROPS")
    print(FLOWPROPS)
    print("-------")        
    
    print("FLOWDATA")
    print(FLOWDATA)
    print("-------")

    print("COMMON")
    print(COMMON)
    print("-------")
    
    print("PTS")
    print(PTS)
    print("-------")    
          
    return None

