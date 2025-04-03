'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting 
@author: kayma
'''
import systems.tools as stls

# MAKING Use of custom path
paths = []
paths.append("G:/pyworkspace/PyTasky/ptsNodes")
stls.addToSystemPaths(paths)

# Simple Print
print("Helo World")

# MAKING Use of node modules
import executer.Mathers as mm
res = mm.ACTION({})
print(res)






