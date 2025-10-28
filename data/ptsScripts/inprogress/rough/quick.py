'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-25"
__author__  = "kayma"



#PTS.sch.every(3).seconds.do(hello).tag("first-task")
#PTS.sch.every(10).minutes.do(job)
#PTS.sch.every().hour.do(job)
#PTS.sch.every().day.at("10:30").do(job)
#PTS.sch.every().monday.do(job)
#PTS.sch.every().wednesday.at("13:15").do(job)
#PTS.sch.every().day.at("12:42", "Europe/Amsterdam").do(job)
#PTS.sch.every().minute.at(":17").do(job)
#https://schedule.readthedocs.io/en/stable/examples.html


#PTS.doExecuteScript(r'G:\pyworkspace\PyTasky\data\ptsScripts\mytestscript.py')

#PTS.doExecuteFlow(r"G:\pyworkspace\PyTasky\data\ptsFlows\arithmatic.flow")


#PTS.sch.jobs
#PTS.sch.cancel_job(PTS.sch.jobs[0])
#PTS.sch.clear()
#PTS.sch.clear("first-task")



##
##import sys
##sys.path.append("G:/pyworkspace/PyTasky/ptsPack/dist/PyTasky/ptsExtLib")
##
####for each in sys.path:
####    print (each)
##
####import os
####print(os.path.abspath(os.path.curdir))
##
##for each in sys.modules:
##    print(each)
##
##from selenium.webdriver import common
##print("ok1")
##print(common)
##
##from selenium.webdriver.common.keys import Keys
##
##print("ok")
##
##
###PTS.console.getModule('selenium.webdriver.common.keys')
##
##
##
####
####from ptsLib import ptsNodeModuleScanner
####pts = ptsNodeModuleScanner.PTSNodeModuleScanner()
####pts.scanNodeModuleFolder()
####
##### for each in PTS.flows.uiNodeCollection:
#####     print (each)
#####
####adv={}
####adv['showErrors'] = 1
####print("--")
####nodeModFiles = PTS.tls.console.scanModuleFiles(PTS.tls.getSafeConfig(['pts', 'nodesPath']), ['__init__'], adv)
####for nodeModName in nodeModFiles.keys():
####    _module =  nodeModFiles[nodeModName][0]
####    _modName = _module.__name__
####    _name = _module.NAME
####    _desc = _module.__doc__
####    _tags = _module.TAGS if hasattr(_module, 'TAGS') else ['custom']
####    _ips = _module.INPUTS if hasattr(_module, 'INPUTS') else []
####    _ops = _module.OUTPUTS if hasattr(_module, 'OUTPUTS') else pts._getDefaultOutputs(_tags)
####    _props = _module.PROPS if hasattr(_module, 'PROPS') else {}
####    _splProps = _module.SPLPROPS if hasattr(_module, 'SPLPROPS') else {}
####    print(_modName, _module)