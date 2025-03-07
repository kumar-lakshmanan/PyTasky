'''
Created on 20-Jan-2025

@author: kayma
'''
from NodeGraphQt import BaseNode

class NDOutputs(BaseNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = f'nodes'

    # initial default node name.
    NODE_NAME = f'nodeNDOutputs'

    def __init__(self):
        super(NDOutputs, self).__init__()

        # create node inputs.
        self.add_input('in A',multi_input=True)
        self.add_input('in B',multi_input=True)