'''
Created on 21-Mar-2025



@author: kayma
'''
import ast
import systems.tools as stls
import systems.uitools as utls

NAME = "CreateNodeData"

TAGS = ["custom"]

INPUTS = [ "inp" ]

PROPS = {}

def ACTION(request):
    data = request["inp"]
    
    nodename = data['NAME']
    nodeinp = data['INPUTS']
    nodeinp = stls.convertStrToObject(nodeinp)
    nodeprops = data['PROPS']
    nodeprops = stls.convertStrToObject(nodeprops)
    
    nodeStr = f"""
'''
Created on today
'''
    
NAME = "{nodename}"

INPUTS = {nodeinp}

PROPS = {nodeprops}

def ACTION(request):

    return None
    """
    return nodeStr
