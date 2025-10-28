#For Sachathya

import json
from data.ptsScripts.syslib import weblib

src = 'btc'	#btc , eur
url = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{}.min.json'.format(src)
# https://github.com/fawazahmed0/exchange-api?tab=readme-ov-file

print(url)
resp = weblib.requestGet(url)
print(resp)
data = json.loads(resp)
print(data[src]["inr"])
