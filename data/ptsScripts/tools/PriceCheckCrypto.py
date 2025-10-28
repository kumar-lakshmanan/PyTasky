from playwright.sync_api import sync_playwright, Playwright

baseSite = "https://messari.io/project/cardano/"

def scrappingLogic(page):
    returnValue = None
    
    # #--------------------------------
    # print("Scrapping logic...")
    # ftdTag = page.locator("span:has-text('Cardano')")       
    # print(ftdTag)
    # grandparent = ftdTag.locator("..").locator("..")  
    # children = grandparent.locator(":scope > *")
    # print(children)
    # count = children.count()
    # print(count)
    # if count==2:
    #     child = children.nth(1)
    #     if child.evaluate('el => el.tagName') == "SPAN":
    #         returnValue = child.text_content()
    # #--------------------------------
    
    #--------------------------------
    print("Scrapping logic...")
    dataTag = page.locator("//div[contains(@class, 'projectSnapshotHeader_assetMetric')]")       #.all_inner_texts()[0] - Expected: 'ADA\n#11\nMcap\n$26.78B\n$0.733\n4.55%'
    data = dataTag.all_inner_texts()
    print("Data: ", data)
    if len(data):
        data = data[0]
        dataParts = data.split("\n")
        name = dataParts[0]
        pos = dataParts[1]
        mCap = dataParts[3]
        price = dataParts[4]
        changePercent = dataParts[5]
        returnValue = (name, pos, mCap, price, changePercent)
    #--------------------------------    

    return returnValue



def scrapAndGetData(baseSite, headelesss=True):
    data = None 
    
    #Get playwright manager
    with sync_playwright() as pw:
        
        #Open Browser
        browser = pw.chromium.launch(headless=True)
        
        #Open Tab
        page = browser.new_page()
        
        #Navigate to
        page.goto(baseSite)
        
        data = scrappingLogic(page)
            
        # Close the browser
        browser.close()
        
    return data

print("Wait fetching data..." )
print("Fetched data: ", scrapAndGetData(baseSite))
print( "Done" )