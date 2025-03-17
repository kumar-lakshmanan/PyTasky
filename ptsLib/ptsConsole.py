'''
Created on Aug 27, 2017

@author: npn
'''
import os
import sys
import importlib.util
import code
from code import InteractiveConsole
import time
import kTools

class PTSConsole(object):
    '''
    Console core will do...
    - Capture all stdouot print redirects and use its fn to write them to custom ui object
    - Ask our tools logger to add one more handler, 
      that will start capturing logs to stdout and use above setup to display in our ui.    
    
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''       
        #Support Modules ready
        self.tls = kTools.GetKTools()     
        self.PTS = parent
        self.parentUi = self.PTS.ui
                                
        self.tls.info('Backup StdOut/Err...')
        self.originalStdOut = sys.stdout 
        self.originalStdErr = sys.stderr
        self.tls.info('Redirecting StdOut/Err to Console...')
        sys.stderr = sys.stdout = self
        self.tls.info('Adding custom logger...')
        self.tls.addCustomLogPrinter(self.customLogPrinter)
        
        self.tls.info('Initializing custom python interpreter...')       
        self.ptsConsole = code.InteractiveConsole(locals())
        
    def customLogPrinter(self, msg):
        #This fn is connected to custom log printer.
        print(msg)
    
    def write(self, data):
        #To Capture the StdOut/Err Redirects
        self.parentUi.qsciPtsStreamOut.setCursorPosition(self.parentUi.qsciPtsStreamOut.lines(), 0)
        self.parentUi.qsciPtsStreamOut.insertAt(data, self.parentUi.qsciPtsStreamOut.lines(), 0)
        vsb = self.parentUi.qsciPtsStreamOut.verticalScrollBar()
        vsb.setValue(vsb.maximum())    
        hsb = self.parentUi.qsciPtsStreamOut.horizontalScrollBar()
        hsb.setValue(0)   
    
    def flush(self):
        pass  # While Stdout Redirect happens, Required for file-like compatibility
        
    # def toFile(self, fileName = lookups.stdLogFile):
    #     sys.stderr = sys.stdout = open(fileName,'w')     
    #     self.tls.info('StdOut/Err Redirected to file {0}'.format(fileName))   
    
    def reset(self):
        sys.stdout = self.originalStdOut
        sys.stderr = self.originalStdErr
        self.tls.info('StdOut/Err Reverted back to original.')        

    def simpleCLI(self, callback=None):
        self.tls.info('Starting simple evaluvator...')
        for eachInput in sys.stdin:
            eachInput = str(eachInput).strip().lower()
            if(eachInput):
                if eachInput in ['quit','exit','stop']:                
                    self.tls.info('Interactive interpreter closing!')
                    break;
                elif callback:
                    res = self._simpleEval(eachInput)
                    callback(res)
                else:
                    res = self._simpleEval(eachInput)
                    print(res)

    def _simpleEval(self, code):
        self.tls.info('Eval Running...')
        try:
            return eval(code)
        except:
            self.tls.getLastErrorInfo()
    
    def simpleConsole(self):
        self.tls.info('Starting console...')
        try:
            self.ptsConsole.locals=locals()  
            self.ptsConsole.locals['PTS'] = self.PTS
            self.ptsConsole.locals['__name__'] = '__main__'          
            self.ptsConsole.interact()
        except SyntaxError:
            self.ptsConsole.showsyntaxerror()
            self.tls.getLastErrorInfo()
        except SystemExit:
            self.ptsConsole.showtraceback()
            self.tls.getLastErrorInfo()
        except:
            self.ptsConsole.showtraceback()
            self.tls.getLastErrorInfo()           

    def runCommand(self, codeStr):        
        codeStr = codeStr.strip()
        self.tls.info(f'{codeStr}')
        if(codeStr):
            try:
                self.ptsConsole.locals['PTS'] = self.PTS
                self.ptsConsole.locals['__name__'] = '__main__'
                self.ptsConsole.runsource(codeStr, "<console>", "single")
                time.sleep(.01)             
            except SyntaxError:
                self.ptsConsole.showsyntaxerror()
                self.tls.getLastErrorInfo()
            except SystemExit:
                self.ptsConsole.showtraceback()
                self.tls.getLastErrorInfo()
            except:
                self.ptsConsole.showtraceback()
                self.tls.getLastErrorInfo()  
    
    def runCode(self, codeStr='', fileName="<input>"):
        self.tls.info('Executing code string...')
        codeStr = codeStr.strip()
        if(codeStr):
            try:
                self.ptsConsole.locals['PTS'] = self.PTS
                self.ptsConsole.locals['__name__'] = '__main__'
                self.ptsConsole.runsource(codeStr, fileName, 'exec')
                time.sleep(.01)            
            except SyntaxError:
                print(sys.exc_info())
            except SystemExit:
                print(sys.exc_info())
            except:
                print(sys.exc_info())
                
    def runScript(self, scriptFile=None):
        self.tls.info('Trying to execute script file... %s' % scriptFile)
        if scriptFile and os.path.exists(scriptFile):
            basePath = os.path.dirname(scriptFile)
            fName = os.path.basename(scriptFile)
            data = self.tls.getFileContent(scriptFile)            
            self.addToSysPath(basePath)
            self.runCode(data,fName)
        else:
            self.tls.info('Script file missing...' + str(scriptFile))          
                
    def getUpdatedLocals(self):
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame.f_back
        namespace = frame.f_globals.copy()
        namespace.update(frame.f_locals)
        namespace['__name__'] = '__main__'
        return namespace          

    def addToSysPath(self, path):
        path = os.path.abspath(path)
        if('\.' in path): return None                
        if path not in sys.path and os.path.exists(path):
            self.tls.info("Adding path to system... " + str(path))
            sys.path.append(path)   

    def loadModule(self, modName, modFilePath):
        """Dynamically loads a Python module from an absolute file path.
    
        Args:
            module_name (str): The name to assign to the module.
            file_path (str): The absolute path of the Python file.
    
        Returns:
            module: The loaded module.
            
if hasattr(loaded_module, "some_function"):
    loaded_module.some_function()
                
        """
        spec = importlib.util.spec_from_file_location(modName, modFilePath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    