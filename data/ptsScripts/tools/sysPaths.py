#For Sachathya
'''
Created on Oct 14, 2014

@author: Mukundan
'''
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
import sys,os
import sysPaths

class sysPathsCls(QtWidgets.QMainWindow):

	def __init__(self,parent):
		'''
		Constructor
		'''
		QtWidgets.QMainWindow.__init__(self)		

		loadUi("ptsUIs/listWin.ui", self)
		self.setWindowTitle(self.__class__.__name__.replace('Cls',''))

		for path in sys.path:
			itm = QtWidgets.QListWidgetItem(path)
			self.listWidget.addItem(itm)
	
if '__main__' == __name__:
	sysPathsObj = sysPathsCls(PTS)
	sysPathsObj.show()
	sysPathsObj.raise_()