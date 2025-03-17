'''
Created on 12-Mar-2025

@author: kayma
'''
'''
Created on 20-Jan-2025

@author: kayma
'''
from NodeGraphQt import BaseNode

class IntOutput(BaseNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = f'nodes'

    # initial default node name.
    NODE_NAME = f'ndIntOutput'
    
    NODE_DESC = '''
    This is node OutputNode
    This will add 
    <br>
    And More
    '''    

    def __init__(self):
        super(IntOutput, self).__init__()

        # create node inputs.
        self.add_input('in A',multi_input=True)
        
        self.props = {}
        self.props['outpxs'] = "hhhe vsdfsaluie"
        self.props['outp4_spl_vaeer'] = "rrre and more"        
    
    def nodeAction(self):
        print("nodeAction" + NODE_NAME)