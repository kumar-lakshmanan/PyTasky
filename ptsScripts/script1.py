'''
Created on 10-Mar-2025

@author: kayma
'''
import os,sys,importlib

paths = []
paths.append("G:/pyworkspace/PyTasky/ptsNodes")
paths.append("G:/pyworkspace/PyTasky/ptsNodes/executer")
paths.append("G:/pyworkspace/PyTasky/ptsNodes/finisher")
paths.append("G:/pyworkspace/PyTasky/ptsNodes/starter")
paths.append("G:/pyworkspace/PyTasky/ptsScripts")

PTS.console.cleanAndUpdateSysPaths(paths)

for each in sys.path:
    print(each)
    
import Adder
importlib.reload(Adder)
print (Adder.z)