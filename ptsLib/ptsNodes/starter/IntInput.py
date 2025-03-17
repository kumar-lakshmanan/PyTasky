'''
Created on 12-Mar-2025

@author: kayma
'''
'''
Created on 20-Jan-2025

@author: kayma
'''
from NodeGraphQt import BaseNode

class IntInput(BaseNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = f'nodes'

    # initial default node name.
    NODE_NAME = f'ndIntInput'
    
    NODE_DESC = '''
    This is node InputNode
    <hr>
    This ddme content you give
    <br>
    And More
    <br>
    sswjuanad next line
    give liek
    this 
    this is new line
    and htis is new linev too
    '''    

    def __init__(self):
        super(IntInput, self).__init__()

        # create node outputs.
        self.add_output('out A', multi_output=True)
        
        self.props = {}
        self.props['input1'] = "some valuie"
        self.props['input2'] = "some moree"
        self.props['input3_spl_var'] = "some moree and more"
    
    def nodeAction(self):
        print("nodeAction" + NODE_NAME)