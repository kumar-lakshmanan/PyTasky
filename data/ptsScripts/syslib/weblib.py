#For Sachathya

import requests
import json

def requestGet(url):
	webContent = requests.get(url,verify=True).text
	return webContent
