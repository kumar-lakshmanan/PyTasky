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
        self.add_input('in',multi_input=True)
        
        self.props = {}
        self.props['simpleDisplay'] = 1
        self.props['logStyleDisplay'] = 1        
    
    def nodeAction(self, reqData={}):
        print("Performing nodeAction for " + self.NODE_NAME)
        
        inpPortData = reqData['in']
                
        if int(self.props['logStyleDisplay']):
            pass
            print(f"Answer is : {inpPortData}")
        else:
            pass
            print(f"Got data: {reqData}")

        print("Completed nodeAction for " + self.NODE_NAME)
        
        return {}
        