'''
@name: SeleniumCall
@author:  kayma
@createdon: 25-Apr-2025
@description:



#PTS_NODE
'''
__created__ = "25-Apr-2025" 
__updated__ = "2025-07-07"
__author__ = "kayma"

NAME = "SeleniumCall"

TAGS = ["custom","ui"]

INPUTS = [ "body" ]

PROPS = {}
PROPS["url"] = "-"
PROPS["method"] = "post"
PROPS["headers"] = {"Content-Type":"text"}

import kTools; tls = kTools.KTools()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def ACTION(input):
    res = None
    
    driver = webdriver.Chrome()
    driver.get("http://www.python.org")
    title = driver.title
    assert "Python" in title
    elem = driver.find_element(By.NAME, "q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    print(elem)
    assert "No results found." not in driver.page_source
    driver.close()

    return title

if __name__ == '__main__':
    tls.info("Starting...")

    inp = {}
    PROPS["url"] = "https://www.goldapi.io/api/XAU/USD"
    PROPS["method"] = "get"
    PROPS["headers"] = {"x-access-token" , "goldapi-22parlg03crlj-io"}

    ret = ACTION(inp)

    print(ret)
    tls.info("Done!")
