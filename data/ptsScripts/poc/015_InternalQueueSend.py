'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting
@author: kayma

CHeck PTSEventActionManager for more info

'''
import kTools; tls = kTools.KTools()

PTS.MainQueue.put({ "action" : "print" , "params" :  "this is sample text to print" })
# PTS.MainQueue.put({ "action" : "exec_flow" , "params" :  {"flowFile" : 'G:/pyworkspace/PyTasky/data/ptsFlows/arithmatic.flow'} })
# PTS.MainQueue.put({ "action" : "exec_script" , "params" :  {"scriptFile" : r'G:\pyworkspace\PyTasky\data\ptsScripts\poc\jsonpather.py' } })
# PTS.MainQueue.put({ "action" : "exec_script" , "params" :  {"scriptFile" : r'G:\pyworkspace\PyTasky\data\ptsScripts\tools\goldprice.py' } })
# PTS.MainQueue.put({ "action" : "exec_script" , "params" :  {"scriptFile" : r'G:\pyworkspace\PyTasky\data\ptsScripts\tools\cryptprice.py' } })
# PTS.MainQueue.put({ "action" : "exec_script" , "params" :  {"scriptFile" : r'G:\pyworkspace\PyTasky\data\ptsScripts\poc\xmlpather.py' } })