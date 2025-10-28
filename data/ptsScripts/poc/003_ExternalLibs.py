'''
@name: lib-chk
@author:  unknown
@createdon: 2025-10-14
@description:

external lib-chk pd DESC 

'''
__created__ = "2025-10-14" 
__updated__ = "2025-10-24"
__author__ = "unknown"

import pandas as pd
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import kTools; tls = kTools.KTools()

def fnDolib_chk():
	tls.info("Calling my lib-chk")
	tls.info(pd)
	tls.info(OpenAI)
	tls.info(webdriver)
		
if __name__ == "__main__":
	fnDolib_chk()