'''
Created on 21-Mar-2025



@author: kayma
'''
import systems.tools as stls
import systems.uitools as utls

NAME = "InputForm"

TAGS = ["custom","ui"]

PROPS = {}
PROPS["FormNameValuePairs"] = '{"Prop1":"Val1", "Prop2":"Val2"}'

def ACTION(request):
    stls.info(PROPS["FormNameValuePairs"] )
    formPairs = stls.getDictFromStr(PROPS["FormNameValuePairs"])
    output = utls.getFormInput(PTS.ui, formPairs)
    return output
