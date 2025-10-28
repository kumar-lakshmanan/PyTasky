'''
@name: yamlpather
@author:  unknown
@createdon: 2025-10-01
@description:

yamlpather DESC 

'''
__created__ = "2025-10-01" 
__updated__ = "2025-10-01"
__author__ = "unknown"

import kTools; tls = kTools.KTools()

import yaml

import re

from jsonpath_ng import parse



def get_by_path(data, path):

    # Split path into keys, handling [index]

    parts = re.findall(r'\w+|\[\d+\]', path)

    cur = data

    for part in parts:

        if part.startswith('['):  # list index

            idx = int(part[1:-1])

            cur = cur[idx]

        else:  # dict key

            cur = cur[part]

    return cur



# Example YAML

yaml_text = """

store:

  book:

    - category: fiction

      title: Harry Potter

    - category: sci-fi

      title: Dune

"""



# Load YAML into Python dict

data = yaml.safe_load(yaml_text)



print(get_by_path(data, "store.book[0].title"))     # Harry Potter

print(get_by_path(data, "store.book[1].category"))  # sci-fi






import jmespath

yaml_text = """
store:
  book:
    - category: fiction
      title: Harry Potter
    - category: sci-fi
      title: Dune
"""

data = yaml.safe_load(yaml_text)

expr = "store.book[?category=='sci-fi'].title"
print(jmespath.search(expr, data))  # ['Dune']

