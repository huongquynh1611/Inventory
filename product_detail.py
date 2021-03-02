import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import bs4
import json
import requests
import urllib.request
import shutil
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import sys
from crawl_aliexpress import GetHomePage,GetProductList
from selenium.webdriver import ActionChains

chrome_options = Options()  
chrome_options.add_argument("--headless") # hide popup 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
website = "https://best.aliexpress.com/?lan=en"
import sys

product_url = "https://vi.aliexpress.com/item/1005001580718099.html?spm=a2g0o.productlist.0.0.37c75e70EJMPtG&algo_pvid=86e296db-d7f9-41e0-995e-24feef766b74&algo_expid=86e296db-d7f9-41e0-995e-24feef766b74-22&btsid=0b0a555d16146483278244410e8133&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
def GetProductDetail(product_url):     
    driver = webdriver.Chrome(executable_path = "C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)   
    print(" >> ",product_url)
    driver.get(product_url)
    
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID , 'root')))
        print("Page is ready!")
    except TimeoutException:
        print ("Loading took too much") 

    scrolls = 3
    while True:
        scrolls -= 1
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 1080)")
        if scrolls < 0:
            break
    p1=None
    p1 = driver.find_elements_by_xpath('//*[@id="product-detail"]/div[2]/div/div[1]/ul/li[3]')[0]
    try:
        p1.click()
        time.sleep(3)
    except ElementClickInterceptedException:

        print("Click failed, error InterceptedException")
    # Lấy html từ page source 
    _page = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    i=_page.findAll("div",{"class":"glodetail-wrap"})[0]
    
    title = i.findAll("div",{"class":"product-title"})[0].h1.text.strip()
    price_current = i.findAll("div",{"class":"product-price-current"})[0].span.text.strip()
    price_original = i.findAll("div",{"class":"product-price-original"})
    price_original = price_original[0].findAll("span",{"class":"product-price-value"}) if len(price_original)> 0 else '' 
    price_original =price_original[0].text.strip() if len(price_original) > 0 else ""
    price_discount = i.findAll("div",{"class":"product-price-original"})
    price_discount = price_discount[0].findAll("span",{"class":"product-price-mark"}) if len(price_discount) > 0 else ""
    price_discount = price_discount[0].text.strip() if len(price_discount) >0 else ""
    coupon = i.findAll("div",{"class":"coupon-mark-new"})
    coupon = coupon[0].text.strip if len(coupon) > 0 else ""
    sku = i.findAll("div",{"class":"sku-wrap"})[0].findAll('div',{"class":"sku-property"})
    for j in sku:
        sku_name = j.findAll("div",{"class":"sku-title"})[0].text.strip()
        print(sku_name)
        sku_value = j.findAll("li",{"class":"sku-property-item"})
        for k in sku_value: 
            # print(k)
            value = k.find('img')
            # print(value)
            if value is not None:
                value_name = value['alt']
                print(value_name)
                value_url = value['src'].replace(".jpg_50x50","")
                print(value_url)
            else:
                value_name = k.text.strip()
                value_url = ''
                print(value_name)
                print(value_url)
            
    shipping = i.findAll("div",{"class":"product-shipping-price"})
    shipping = shipping[0].text.strip() if len(shipping) >0 else ("Please select the country you want to ship from")
    print(shipping)
    store = i.findAll("div",{"class":"shop-name"})
    store_name = store[0].text.strip() if len(store) > 0 else ""
    store_link = store[0].a["href"] if len(store) > 0 else ""
    store_positive = i.findAll("div",{"class":"positive-fdbk"})
    store_positive = store_positive[0].text if len(store_positive) > 0 else ""
    store_folower_num = i.findAll("div",{"class":"follower-num"})
    store_folower_num = store_folower_num[0].text.strip() if len(store_folower_num) > 0 else ""
    store_contact = i.findAll("div",{"class":"store-info-contact"})
    store_contact = store_contact[0].a["href"] if len(store_contact) > 0 else ""
    store_top = i.findAll("div",{"class":"top-seller-label"}) 
    store_top = store_top[0].text.strip() if len(store_top) > 0 else ""
    detail = i.findAll("ul",{"class":"product-specs-list util-clearfix"})
    print(detail)
    print(store_contact)
    print(store_top )
    print(store_folower_num)
GetProductDetail(product_url)
