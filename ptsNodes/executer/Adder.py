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
        self.add_input('in1',multi_input=False)
        self.add_input('in2',multi_input=False)

        # create node outputs.
        self.add_output('out', multi_output=True)
        
        self.props = {}
        self.props['doAdder'] = 1
        self.props['doSub'] = 0
        self.props['doMultiply'] = 0
        self.props['doDivide'] = 0
    
        
    def nodeAction(self, reqData={}):
        print("Performing nodeAction for " + self.NODE_NAME)
        resp = {}
        inpPortData1 = reqData['in1']
        inpPortData2 = reqData['in2']

        n1 = int(inpPortData1)
        n2 = int(inpPortData2)
        print(f"DOing operation {n1} and {n2}")

        if int(self.props['doAdder']):
            print(f"DOing add operation {n1} and {n2}")
            output = n1 + n2
            
        if int(self.props['doSub']):
            print(f"DOing sub operation {n1} and {n2}")
            output = n1 - n2            

        if int(self.props['doMultiply']):
            print(f"DOing mul operation {n1} and {n2}")
            output = n1 * n2
                
        if int(self.props['doDivide']):
            print(f"DOing div operation {n1} and {n2}")
            output = n1 / n2                

        print("Completed nodeAction for " + self.NODE_NAME) 
        return {'out': output}
                   
        