'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting
@author: kayma

Internal Obj - gives sample glimps of internal objects and how to access them.

Mostly use like this
import kTools; tls = kTools.KTools()
import kCodeExecuter; console = kCodeExecuter.KCodeExecuter()

'''
import kTools; 
import kCodeExecuter;

tls = kTools.KTools()
console = kCodeExecuter.KCodeExecuter()

print("About this script")
print(__doc__)

# Adding custom lib path
paths = []
paths.append(r"G:\pyworkspace\PyTasky\data\ptsNodes")
tls.sysPathUpdater(paths)

#Access tools - tls
tls.helloworld()
tls.info("Tools Info Printing")
tls.warn("Tools Warn Printing")
tls.error("Tools error Printing")
tls.info(tls.getTimeStamp())
tls.info(tls.getCurrentUser())
tls.info(tls.getCurrentPath())
tls.info(tls.getSystemName())


#Access PTS obj
print("--------PTS - Internal Object----------")
print(PTS)
print(PTS.ui)   #PTS UI
print(PTS.sch.jobs)   #PTS UI

#Console execute
codeStr = r"""
k = 10
print(k+20)
z=k+30
print(z)
"""
console.runCode(codeStr)