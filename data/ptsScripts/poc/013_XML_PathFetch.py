'''
@name: xmlpather
@author:  unknown
@createdon: 2025-10-01
@description:

xmlpather DESC 

'''
__created__ = "2025-10-01" 
__updated__ = "2025-10-01"
__author__ = "unknown"

import kTools; tls = kTools.KTools()
import xml.etree.ElementTree as ET

xml_text = """
<store>
  <book category="fiction">
    <title>Harry Potter</title>
  </book>
  <book category="sci-fi">
    <title>Dune</title>
  </book>
</store>
"""

root = ET.fromstring(xml_text)

# XPath style queries
# Get all book titles
titles = root.findall(".//book/title")
print([t.text for t in titles])  # ['Harry Potter', 'Dune']

# Get book with category="sci-fi"
sci_fi_book = root.find('.//book[@category="sci-fi"]/title')
print(sci_fi_book.text)  # Dune
