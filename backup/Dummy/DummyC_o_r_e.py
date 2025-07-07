'''
Add a good description of your node 
@author: your_good_name
'''

'''
Add any import module you want to use. Make sure system path has info to reach that module.
''' 
import kTools
tls = kTools.KTools()

'''
Your Node Name - Good to be small (Max 15)
'''
NAME = "AGoodNodeName"  

'''
INPUTS what your node will take. 
in, in1, in2 are different input ports via you will get input from different nodes. 
which you can process in your core action.
'''
INPUTS = [ "in", "in1", "in2" ]

'''
OUTPUTS what your node will give out as return. 
[out, out1, out2] are different output ports via your outputs are seperated and send to other node ports. 
this can be  also be like : OUTPUTS = [ ("out",1),("out2",1),("out3",0) ] its little advance one.
Where ("out",1) is one set of output port. In this first val is portname. and second val is boolean.  
which tell that output data from that port can be shared to many nodes from it when it set as 1,
else output from that port can be given to only one node.
'''
OUTPUTS = [ ("out",1),("out2",1),("out3",0) ]

'''
PROPS Node properties are important feature for customization. You can customize your core action with properties values.
These props are available for editing in GUI while building flow.   
Important. All values are serializable strings. Core action should convert as per thier need.
'''
PROPS = {}
PROPS["Value"] = "Some Value"

'''
ACTION: Core Fn that will be executed. with given INPUT and PROPS, And will give its OUTPUT as return.
inputs param will have key name of your node INPUTS.
And the value will be some object from the connected node.
Check inside the function for understanding more.
''' 
def ACTION(inputs={}):
    '''
    inputs - will be dict with values for your input ports. like
    print(inputs['in'])
    print(inputs['in1'])
    
    if it's missing connection to 'in' port , you action will throw error.
    '''
    
    tls.info(f"Variable processing {PROPS['Value']}") 
    
    
    '''
    output - should be a dict with value for all your output ports. 
    return { 'out' : "Some value" , 'myanotheroutport' : "value2"}
   
    if any of your port is  missing in the return, flow will throw error.
    '''
    return {'out' : PROPS["Value"]}

