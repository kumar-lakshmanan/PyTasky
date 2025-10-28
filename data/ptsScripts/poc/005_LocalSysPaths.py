'''

@name: mysyspaths

@author:  unknown

@createdon: 2025-09-24

@description:

mysyspaths DESC 


'''
__created__ = "2025-09-24" 
__updated__ = "2025-10-24"
__author__ = "unknown"


import kTools; tls = kTools.KTools()
import sys

def fnDomysyspaths():
	tls.info("Calling my mysyspaths")
	for each in sys.path:
		print(each)

if __name__ == "__main__":
	fnDomysyspaths()