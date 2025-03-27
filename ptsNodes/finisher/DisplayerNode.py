"""
Auto Generated Node
"""
from NodeGraphQt import BaseNode

class DisplayerNode(BaseNode):
    
    NODE_NAME = "Displayer"
    NODE_DESC = """
Created on 21-Mar-2025

STYLE
1 - LOG STYLE
2 - SIMPLE STYLE

@author: kayma
"""

    def __init__(self):
        super(DisplayerNode, self).__init__()
        
        self.add_input('in1',multi_input=False)
        
        
        self.props = {}
        self.props['STYLE'] = '1'
