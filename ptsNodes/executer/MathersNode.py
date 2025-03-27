"""
Auto Generated Node
"""
from NodeGraphQt import BaseNode

class MathersNode(BaseNode):
    
    NODE_NAME = "Mathers"
    NODE_DESC = """
Created on 21-Mar-2025


@author: kayma
"""

    def __init__(self):
        super(MathersNode, self).__init__()
        
        self.add_input('in1',multi_input=False)
        self.add_input('in2',multi_input=False)
        
        self.add_output('out',multi_output=1)
        
        self.props = {}
        self.props['ADD'] = '1'
        self.props['SUB'] = '0'
        self.props['MUL'] = '0'
        self.props['DIV'] = '0'
