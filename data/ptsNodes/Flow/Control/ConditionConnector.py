'''
@name: ConditionConnector
@author:  kayma
@createdon: 16-Apr-2025
@description:

ConditionConnector use after condition and run on your flow as usual. 
No processing. Simply continue the flow after your condition either true side or false side

#PTS_NODE
'''
__created__ = "2025-04-24" 
__updated__ = "2025-07-07"
__author__ = "kayma"


NAME = "ConditionConnector"

TAGS = ["connector",]

INPUTS = [ "inp" ]

OUTPUTS = [ "True", "False"  ]

PROPS = {"condition":"data['Variable-out1']=='add'"}

SPLPROPS = {}
SPLPROPS["NodeStyle"] = "Circle"   #Default or Box or Circle
