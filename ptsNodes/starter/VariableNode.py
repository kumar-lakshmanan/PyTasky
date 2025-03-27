"""
Auto Generated Node
"""
from NodeGraphQt import BaseNode

class VariableNode(BaseNode):
    
    NODE_NAME = "Variable"
    NODE_DESC = """
Created on 21-Mar-2025



@author: kayma
"""

    def __init__(self):
        super(VariableNode, self).__init__()
        
        
        self.add_output('out',multi_output=1)
        
        self.props = {}
        self.props['Value'] = 'Some Value'
