'''
Created on 21-Mar-2025



@author: kayma
'''
import kTools; tls = kTools.GetKTools()

NAME = "Variable"

OUTPUTS = [ ("out",1) ]

PROPS = {}
PROPS["Value"] = "Some Value"

def ACTION(request):
    tls.info(f"Action Started {NAME}")  
    return {'out' : PROPS["Value"]}

if "__main__" == __name__:
    tls.info("Runnign local test")
    request = {}
    res = action(request)
    print(res)