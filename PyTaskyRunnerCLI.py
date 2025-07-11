__appname__ = "PyTasky"
__author__  = "Kumaresan"
__created__ = "2025-03-07"
__updated__ = "2025-07-11"

'''

Check kTools document for basic config
'''

import os, sys
K_PYLIB = 'G:/pyworkspace/kpylib'
K_CONFIGFILE = 'pytasky_config.json'
K_CONFIG = os.path.abspath(K_CONFIGFILE)
if not ('K_PYLIB' in os.environ and os.path.exists(os.environ['K_PYLIB'])): os.environ['K_PYLIB'] = K_PYLIB
if not ('K_PYLIB' in os.environ and os.path.exists(os.environ['K_PYLIB'])): sys.exit("K_PYLIB not found!")
for eachDependency in os.environ['K_PYLIB'].split(';'): sys.path.append(eachDependency.strip())
if not ('K_CONFIG' in os.environ and os.path.exists(os.environ['K_CONFIG'])): os.environ['K_CONFIG'] = K_CONFIG
if not ('K_CONFIG' in os.environ and os.path.exists(os.environ['K_CONFIG'])): sys.exit("K_CONFIG not found!")

import atexit
import argparse

import kTools
import kCodeExecuter
import PyTaskyLookUps

from ptsLib import ptsExecFlowRunner
from ptsLib import ptsNodeModuleScanner

#----------------------

class core():

    def __init__(self):
        self.tls = kTools.KTools(__appname__, PyTaskyLookUps, K_CONFIGFILE)
        self.tls.share['console'] = kCodeExecuter.KCodeExecuter()
        self.tls.createNewSignalSetup("flowevent")
        self.tls.subscribeToSignal("flowevent", self.floweventHandler)
        self.console = self.tls.share['console']
    
        self.pns = ptsNodeModuleScanner.PTSNodeModuleScanner()
        self.pns.ptsNodesPath = self.tls.getSafeConfig(['pts','nodesPath'], './ptsNodes')
        self.pns.scanNodeModuleFolder()
        
        self.setupCLI()
        
    def setupCLI(self):
        self.parser = argparse.ArgumentParser(description="PyTaskyRunner will execute the flow.")
        
        # Create subparsers for each core-action
        self.subparsers = self.parser.add_subparsers(dest='core_action', required=True, help="Core actions")
        
        # --- runflow subcommand ---
        run_parser = self.subparsers.add_parser('runflow', help='Run a flow using a flow file')
        run_parser.add_argument('--flowfile', '-f', type=str, required=True, help='Path to the flow file')
        
        # --- listflow subcommand ---
        self.subparsers.add_parser('listflow', help='List all flows')
        
        # --- listmods subcommand ---
        self.subparsers.add_parser('listnodemods', help='List all node modules')
        
        # Parse arguments
        self.args = self.parser.parse_args()
        
    def processCLIArg(self):
        if self.args.core_action == 'runflow':
            flowFile = self.args.flowfile
            if not self.tls.isFileExists(flowFile):
                defaultFlowPath = self.tls.getSafeConfig(['pts','flowsPath'])
                flowFile = self.tls.pathJoin(defaultFlowPath, flowFile)
            self.runFlow(flowFile)

        elif self.args.core_action == 'listflow':
            print("Listing all available flows...")
            self.listflow()
        
        elif self.args.core_action == 'listnodemods':
            print("Listing all node mods...")     
            self.listnodemods()
        
    def runFlow(self, flowFile):
        if flowFile and self.tls.isFileExists(flowFile):
            runner = ptsExecFlowRunner.PTSExecFlowRunner(self)
            runner.flowFile =  flowFile
            runner.preSetup()
            runner.run()
            del(runner)
            self.tls.doCleanMemory()
        else:
            self.tls.error(f"Unable to run the flow: {flowFile}")
         
    def listflow(self):
        defaultFlowPath = self.tls.getSafeConfig(['pts','flowsPath'])
        flowList = self.tls.getFileList(defaultFlowPath, ext=".flow")
        for each in flowList:
            self.tls.info(each)

    def listnodemods(self):
        for each in self.pns.allNodes:
            self.tls.info(f"{each}, {self.pns.allNodes[each]}")
                    
    def floweventHandler(self, flowEvent):
        lst = self.tls.getSafeDictValue(flowEvent, "lst", [])
        msg = self.tls.getSafeDictValue(flowEvent, "msg", None)
        if msg:
            self.tls.info(f"{msg}")
            
        if len(lst):
            act = lst[0]
            if act == "fetch_node":
                n = lst[1]
                node = lst[2]                                
                # print(f"{n}.Processing {node}... ",end='')
                # tls.info(f"{n} Pushing back [{node}], No input ready.")                
            if act == "pushback": 
                n = lst[1]
                node = lst[2]                                
                self.tls.info(f"{n}.Waiting {node}!")            
            if act == "pushback_loopnode": 
                n = lst[1]
                node = lst[2]                                
                self.tls.info(f"{n}.Waiting {node}!")                   
            if act == "executing": 
                n = lst[1]
                node = lst[2]                                
                self.tls.info(f"{n}.Executing {node}...")   
            if act == "scan_node":
                n = lst[1]
                self.tls.info(f"Scanning [{n}]...")           

    def __enter__(self):
        self.tls.info('PyTasky startup actions initiated...')
        return self

    def __exit__(self, *arg):
        self.tls.info('PyTasky exit actions initiated...')

if __name__ == "__main__":
    appCore = core()
    appCore.processCLIArg()
    atexit.register(appCore.__exit__)
    sys.exit()
