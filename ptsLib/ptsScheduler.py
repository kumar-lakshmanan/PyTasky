'''
Created on 21-Mar-2025

@author: kayma
'''

import os, sys, time, schedule, threading,json
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
import code, importlib
import kTools
import kCodeExecuter
from ptsLib import ptsNodeModuleScanner
from schedule import Scheduler

class PTSSchedulerThread(threading.Thread):
    def __init__(self, scheduler, info_callback, error_callback):
        super().__init__(daemon=True)   # daemon=True so it dies with app
        self.scheduler = scheduler
        self.info_callback = info_callback
        self.error_callback = error_callback
        self._running = True

    def run(self):
        while self._running:
            try:
                self.scheduler.exec_jobs()
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                self.error_callback(f"Scheduler error: {e}\n{tb}")
            time.sleep(1)

    def stop(self):
        self._running = False