'''
Created on 21-Mar-2025

@author: kayma
'''

import os, sys
import kCodeExecuter
import kTools
        
nodesDir = "G:/pyworkspace/PyTasky/ptsNodes"
nodeTemplate = "G:/pyworkspace/PyTasky/ptsNodes/NodeTemplate.py"

tls = kTools.GetKTools()

k = kCodeExecuter.KCodeExecuter()
k.cleanAndUpdateSysPaths([nodesDir])
nodeModFiles = k.scanModuleFiles(nodesDir, ignoreFileNameHasText=['__init__','Compiler','Template', 'Node'])

for nodeModName in nodeModFiles.keys():
    nodeModObj = nodeModFiles[nodeModName][0]
    nodeModFilePath = os.path.dirname(nodeModFiles[nodeModName][1])
    
    newNodeModName = nodeModName.replace('Core', 'Node')
    newNodeModFile = os.path.join(nodeModFilePath, newNodeModName + '.py')
    
    templateData = tls.getFileContent(nodeTemplate)
    templateData = templateData.replace('[NODEMODNAME]', newNodeModName, 2)
    templateData = templateData.replace('[NODENAME]', nodeModObj.NAME)
    templateData = templateData.replace('[NODEDESC]', nodeModObj.__doc__)
    
    inputs = ""
    if hasattr(nodeModObj, 'INPUTS'):    
        for eachInp in nodeModObj.INPUTS:
            name = eachInp[0] if type(eachInp)==type(()) else eachInp 
            multi = eachInp[1] if type(eachInp)==type(()) and len(eachInp)>0 else False
            inputs += f"\n        self.add_input('{name}',multi_input={multi})"
    templateData = templateData.replace('[ADDINPUTS]', inputs)
    
    outputs = ""
    if hasattr(nodeModObj, 'OUTPUTS'):
        for eachOut in nodeModObj.OUTPUTS:
            name = eachOut[0] if type(eachOut)==type(()) else eachOut 
            multi = eachOut[1] if type(eachOut)==type(()) and len(eachOut)>0 else False
            outputs += f"\n        self.add_output('{name}',multi_output={multi})"
    templateData = templateData.replace('[ADDOUTPUTS]', outputs)
    
    props = "\n        self.props = {}"
    for eachProp in nodeModObj.PROPS:
        name = eachProp
        value = nodeModObj.PROPS[name]

        props += f"\n        self.props['{name}'] = '{value}'"
    templateData = templateData.replace('[PROPS]', props)   
    tls.info(f"Generated node module {newNodeModFile}!") 

    tls.writeFileContent(newNodeModFile, templateData)
