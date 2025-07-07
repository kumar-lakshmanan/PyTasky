'''
Created on 10-Mar-2025

@author: kayma
'''
from playwright.sync_api import sync_playwright, Playwright
import time
def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.grtjewels.com/")
    dropdownbox = page.locator("#dropdown-basic-button1")
    dropdownbox.click()

    data = page.locator(".dropdown-menu.show")
    if data.count()==1:
        content = data.all_inner_texts()[0]
        content = content.split('\n')
        lst = {}
        for each in content:
            each = each.replace(" KT/1g - ₹ "," + ")
            each = each.replace(" 1g - ₹ "," + ")
            print(each)
            #k,v = each.split(" + ")
            #lst[k] = v
            #print(k,"  = " ,v)

    # other actions...
    browser.close()

with sync_playwright() as playwright:
    run(playwright)