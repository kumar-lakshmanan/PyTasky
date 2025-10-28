import requests
from bs4 import BeautifulSoup
import re
    
#JIO PLANS - COPY PRINTS TO EXCEL AND DO COMPARE

url = "https://www.jio.com/api/jio-mdmdata-service/mdmdata/recharge/plans?productType=MOBILITY&billingType=1"

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


soup = urlReadGetSoup(url)
import json
json.loads(soup.text)['planCategories']

allcats = json.loads(soup.text)['planCategories']

for each in allcats:
    planType = each['type']
    allsubcat = each['subCategories']
    for eachsubcat in allsubcat:
        pname = eachsubcat['type']
        allplans = eachsubcat['plans']
        for eachplan in allplans:
            amount = eachplan['amount']
            desc = eachplan['description']
            desc = desc.replace("\n","")
            d1 = eachplan['primeData']['offerBenefits1'] if 'offerBenefits1' in eachplan['primeData'] else None
            d2 = eachplan['primeData']['offerBenefits2'] if 'offerBenefits2' in eachplan['primeData'] else None
            d3 = eachplan['primeData']['offerBenefits3'] if 'offerBenefits3' in eachplan['primeData'] else None
            d4 = eachplan['primeData']['offerBenefits4'] if 'offerBenefits4' in eachplan['primeData'] else None
            #print(planType,'\t',pname, '\t', amount, '\t', d1,d2,'-',d3,d4, ',', desc)
            
            print(f""" "{planType}","{pname}","{amount}","{d1}", "{d2}","{d3}", "{d4}""")
            
            
        

