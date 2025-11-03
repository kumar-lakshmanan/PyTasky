'''
@name: 
@author: kayma
@createdon: "2025-10-25"
@description:
'''

__created__ = "2025-10-25"
__updated__ = "2025-10-30"
__author__  = "kayma"


key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyOTY2MjE4ZS1jMTAzLTQ3YmUtYmY3ZS04ZWU0YTU1ZTU0NjAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYxNzM0NDczfQ.Q73op9_jF0uKwxb3Emwj1UCu9ol58CSljU0xP01diok"


import http.client

conn = http.client.HTTPSConnection("http://localhost:5678")

headers = { 'X-N8N-API-KEY': key }

conn.request("POST", "/api/v1/workflows/RNHuoPRVrZeZhx6R/activate", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))