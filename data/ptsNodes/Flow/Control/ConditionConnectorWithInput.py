'''
@name: Condition
@author:  kayma
@createdon: 16-Apr-2025
@description:

Check condition and use only the true path and ignore the false path
Will use the inp in properity "condition" and helps you decide boolean true or false.
data["Variable-out1"]=='addx'

#PTS_NODE
'''
__created__ = "2025-04-16" 
__updated__ = "2025-07-07"
__author__ = "kayma"

NAME = "Condition"

TAGS = ["sys","condition"]

INPUTS = [ "inp" ]

OUTPUTS = [ "True", "False"  ]

PROPS = {"condition":"data['Variable-out1']=='add'"}

SPLPROPS = {}
SPLPROPS["NodeStyle"] = "Circle"   #Default or Box or Circle
