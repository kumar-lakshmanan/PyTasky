'''
@name: CreateNodeData
@author:  kayma
@createdon: 21-Apr-2025
@description:

Will launch an ui window which provided at UIFile.
Then will make use of script mentioned in UILogicScript.
And will run the function mentioned in UICustomizerFunction.
You can use it to customize your UI like button action,  input text box writing and many more.
When you close the window by any means. 
Function mentioned in UIDataFetcherFunction will be called. 
You can read text box value form value and other values and compose your return statement and return to next node.
 
#PTS_NODE
'''
__created__ = "2025-04-21" 
__updated__ = "2025-07-07"
__author__ = "kayma"

NAME = "CreateNodeData"

TAGS = ["custom"]

INPUTS = [ "inp" ]

PROPS = {}

# import syslib.tools as stls
# import syslib.uitools as utls

def ACTION(input):
    data = input["inp"]
    
    nodename = data['NAME']
    nodeinp = data['INPUTS']
    nodeinp = stls.convertStrToObject(nodeinp)
    nodeprops = data['PROPS']
    nodeprops = stls.convertStrToObject(nodeprops)
    
    content = stls.getFileContent("simpleNodeTemplate.txt")
    content = content.replace("{nodename}", nodename)
    content = content.replace("{nodeinp}", nodeinp)
    content = content.replace("{nodeprops}", nodeprops)
    
    return content
