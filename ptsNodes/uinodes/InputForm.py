'''
Created on 21-Mar-2025



@author: kayma
'''
import systems.tools as stls
import systems.uitools as utls

NAME = "InputForm"

ISUI = True

OUTPUTS = [ ("out",1) ]

PROPS = {}
PROPS["FormNameValuePairs"] = '{"Prop1":"Val1", "Prop2":"Val2"}'

def ACTION(request):
    stls.info(f"Action Started {NAME}")
    formPairs = stls.getDictFromStr(PROPS["FormNameValuePairs"])
    output = utls.getFormInput(PTS.ui, formPairs)
    return {'out' : output}
