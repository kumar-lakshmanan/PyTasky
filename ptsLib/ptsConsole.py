'''
Created on Aug 27, 2017

@author: npn
'''
import os
import sys
import importlib
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

        self.tls.info('Adding custom logger...')
        self.tls.addCustomLogPrinter(self.customLogPrinter)
        
        self.tls.info('Initializing custom python interpreter...')       
        self.console = self.tls.console
        self.console.updateLocals('PTS',self.PTS)
        self.console.updateLocals('PTS_UI',self.PTS.ui)
        
        self.grabStdOut()
        
    def grabStdOut(self):
        self.tls.info('Redirecting StdOut/Err to Console...')
        sys.stderr = sys.stdout = self

    def reset(self):
        sys.stdout = self.originalStdOut
        sys.stderr = self.originalStdErr
        self.tls.info('StdOut/Err Reverted back to original.')           
        
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
    
     
