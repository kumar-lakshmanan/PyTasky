'''
Created on 20-Jan-2025

@author: kayma
'''
from NodeGraphQt import BaseNode

class NDInputs(BaseNode):
    """
    A node class with 2 inputs and 2 outputs.
    """

    # unique node identifier.
    __identifier__ = f'nodes'

    # initial default node name.
    NODE_NAME = f'nodeNDInputs'

    def __init__(self):
        super(NDInputs, self).__init__()

        # create node outputs.
        self.add_output('out A', multi_output=True)
        self.add_output('out B', multi_output=True)