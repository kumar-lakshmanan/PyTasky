'''
Created on 12-Mar-2025

@author: kayma
'''
'''
Created on 20-Jan-2025

@author: kayma
'''
from NodeGraphQt import BaseNode

class Adder(BaseNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = f'nodes'

    # initial default node name.
    NODE_NAME = f'ndAdder'
    
    NODE_DESC = '''
    This is node Adder.
    This will add some content you give
    <br>
    And More
    '''

    def __init__(self):
        super(Adder, self).__init__()

        # create node inputs.
        self.add_input('in A',multi_input=True)
        self.add_input('in B',multi_input=True)

        # create node outputs.
        self.add_output('out A', multi_output=True)
        
        self.props = {}
        self.props['adder'] = "sdfe vsdfsaluie"
        self.props['outp2'] = "ffdfdsome moree"
        self.props['outp3_spl_var'] = "ffdsofdme moree and more"
        self.props['outp4_spl_var'] = "fdme moree and more"
    
        
    def nodeAction(self):
        print("nodeAction" + NODE_NAME)