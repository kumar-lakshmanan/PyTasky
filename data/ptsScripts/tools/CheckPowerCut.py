'''
@name: 
@author: kayma
@createdon: "2025-09-17"
@description:
'''

__created__ = "2025-09-17"
__updated__ = "2025-09-17"
__author__  = "kayma"


import requests
from bs4 import BeautifulSoup
import re
    
lookForPowerCutIn = []
lookForPowerCutIn.append('valmiki nagar')
lookForPowerCutIn.append('kalakshetra road')
lookForPowerCutIn.append('tiruvalluvar nagar')
lookForPowerCutIn.append('kottivakkam kuppam')
lookForPowerCutIn.append('kottivakkam')

url = "https://www.dtnext.in/advance-search?search=Power%20shutdown"

def urlReadGetSoup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/128.0.0.0 Safari/537.36"
    }
    
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.content, "html.parser") 
    return soup   

def safe_select_one(node, selector, err_msg):
    el = node.select_one(selector) if node else None
    if not el:
        raise ValueError(err_msg)
    return el

def getArticleTitleAndLink(articleNode):
    figure = safe_select_one(articleNode, "figure", "figure not found in article")
    a_tag = safe_select_one(figure, "a", "link <a> not found in figure")
    if "title" not in a_tag.attrs:
        raise ValueError("title attribute missing in <a>")    
    title = a_tag["title"]
    link = a_tag["href"]
    month, date = getMonthDateInfo(title)
    isPowercut, area = readPowerCutAreas(link)
    if month and date: return ( month, date, isPowercut, area, title, link)
    return (None, None, None)

def getArticle(base):
    article = safe_select_one(base, "article", "article not found")
    return getArticleTitleAndLink(article)

def getAllArticles(base):
    secs = base.select_one("section")
    articles = secs.select("article")
    res = []
    for each in articles:
        res.append(getArticleTitleAndLink(each))
    return res

def getMonthDateInfo(inputMsg):
    # Regex to capture month + date
    pattern = re.compile(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\b")
    if "power" in inputMsg.lower() and "shutdown" in inputMsg.lower():
        match = pattern.search(inputMsg)
        if match:
            month, day = match.groups()
            #print(f"{month} {day}")
            return (month, day)
    return (None,None)

def readPowerCutAreas(url):
    soup = urlReadGetSoup(url)
    content = soup.select_one("div.story_content.details-content-story")
    powerCutAreas = content.get_text()
    powerCutAreas = powerCutAreas.lower()    
    for eachWord in lookForPowerCutIn:
        if eachWord in powerCutAreas:
            return (True, eachWord)
    return (False, None)

soup = urlReadGetSoup(url)

latest = getArticle(soup)
print(latest)

allold = getAllArticles(soup)
for each in allold:
    print(each)
