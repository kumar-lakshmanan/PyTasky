'''
@name: jsonpather
@author:  unknown
@createdon: 2025-10-01
@description:

jsonpather DESC 

'''
__created__ = "2025-10-01" 
__updated__ = "2025-10-01"
__author__ = "unknown"

import kTools; tls = kTools.KTools()

from jsonpath_ng import parse

data = {
    "store": {
        "book": [
            {"category": "fiction", "title": "Harry Potter"},
            {"category": "sci-fi", "title": "Dune"}
        ]
    }
}

# Path like XPath, but for JSON
expr = parse('$.store.book[1]')   # $ = root
match = expr.find(data)

print([m.value for m in match])  # ['Dune']
