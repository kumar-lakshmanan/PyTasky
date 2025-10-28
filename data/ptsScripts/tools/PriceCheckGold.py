from playwright.sync_api import sync_playwright, Playwright
import time

#Get playwright manager
with sync_playwright() as pw:
    
    #Open Browser
    browser = pw.chromium.launch(headless=False)
    
    #Open Tab
    page = browser.new_page()
    
    #Navigate to
    page.goto("https://www.grtjewels.com/", timeout=50000)
    
    #Wait for element and click that (ID LOCATING)
    dropdownbox = page.locator("#dropdown-basic-button1")
    dropdownbox.click()
    
    #Wait for element and get that (CLASS LOCATING)
    data = page.locator(".dropdown-menu.show")
    
    #If found do this...
    if data.count()==1:
        #Get all text inside it    
        content = data.all_inner_texts()[0]
        
        #String process them
        content = content.split('\n')
        #['GOLD 24 KT/1g - ₹ 12844', 'GOLD 22 KT/1g - ₹ 11765', 'GOLD 18 KT/1g - ₹ 9633', 'GOLD 14 KT/1g - ₹ 7492', 'PLATINUM 1g - ₹ 5755', 'SILVER 1g - ₹ 206']
        
        lst = {}
        print(content)
        for each in content:
            if "KT" in each:
                itemTypes = each.split("KT")
                itemName = itemTypes[0]
                itemPrice = each.split(" ")
                itemPrice = itemPrice[-1]
                print(itemName, itemPrice)
            elif "1g":
                itemTypes = each.split("1g")
                itemName = itemTypes[0]
                itemPrice = each.split(" ")
                itemPrice = itemPrice[-1]
                print(itemName, itemPrice)
            else:
                print(each)
        
    # Close the browser
    browser.close()
