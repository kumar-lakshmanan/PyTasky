'''
@name: WebCall
@author:  kayma
@createdon: 21-Apr-2025
@description:

Will can web service and gives the response
url - must
method - can be post or get
body - used if post

#PTS_NODE
'''
__created__ = "2025-04-21" 
__updated__ = "2025-07-25"
__author__ = "kayma"

NAME = "WebCall"

TAGS = ["custom"]

INPUTS = [ "body" ]

PROPS = {}
PROPS["url"] = "-"
PROPS["method"] = "post"
PROPS["headers"] = '{"Content-Type":"text"}'

import kTools; tls = kTools.KTools()
import requests

def ACTION(input):
    res = None
    
    url = PROPS["url"]
    method = PROPS["method"]
    headers = PROPS["headers"]

    print(PROPS)
    print(headers['Content-Type'])
    
    if PROPS["method"] == "get":
        res = requests.get(url, headers=headers)
        #res.raise_for_status()

    return (res.status_code, res.text)

if __name__ == '__main__':
    tls.info("Starting...")
    
    headers = {
        "x-access-token": "goldapi-22parlg03crlj-io",
        "Content-Type": "application/json"
    }    

    inp = {}
    PROPS["url"] = "https://www.goldapi.io/api/XAU/USD"
    PROPS["method"] = "get"
    PROPS["headers"] = headers

    ret = ACTION(inp)

    print(ret)
    tls.info("Done!")
