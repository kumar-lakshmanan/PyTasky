'''
@name: InputForm
@author:  kayma
@createdon: 21-Apr-2025
@description:

Will display UI InputForm with Name-Value pair mentioned in props.
When you close the ui form, New updated value will be returned and can be used in next node.

#PTS_NODE
'''
__created__ = "2025-04-21" 
__updated__ = "2025-07-24"
__author__ = "kayma"

NAME = "InputForm"

TAGS = ["custom","ui"]

PROPS = {}
PROPS["FormNameValuePairs"] = '{"Prop1":"Val1", "Prop2":"Val2"}'

import kTools 
from kQt import kQtTools

tls = kTools.KTools()
qttls = kQtTools.KQTTools()

def ACTION(input):
    tls.info(PROPS["FormNameValuePairs"] )
    formPairs = tls.convertDictStrToDict(PROPS["FormNameValuePairs"])
    output = qttls.getFormInput(formPairs, PTS.ui)
    return output
