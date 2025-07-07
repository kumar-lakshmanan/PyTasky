'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting 
@author: kayma
'''
import kTools; tls = kTools.KTools()

# MAKING Use of custom path
paths = []
paths.append("G:/pyworkspace/PyTasky/data/ptsNodes")
tls.addSysPaths(multiPaths=paths)

# Simple Print
print("Helo World")

# MAKING Use of node modules
import Logical.Mathers as mm
res = mm.ACTION({})
print(res)






