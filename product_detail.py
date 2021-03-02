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
# chrome_options.add_argument("--headless") # hide popup 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
website = "https://best.aliexpress.com/?lan=en"
import sys

product_url = "https://vi.aliexpress.com/item/1005001580718099.html?spm=a2g0o.productlist.0.0.37c75e70EJMPtG&algo_pvid=86e296db-d7f9-41e0-995e-24feef766b74&algo_expid=86e296db-d7f9-41e0-995e-24feef766b74-22&btsid=0b0a555d16146483278244410e8133&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
def GetProductDetail(product_url):     
    file_csv = open("output.csv", "w", newline='', encoding='utf-8-sig') #open write file
    header = ["Title","PriceCurrent","PriceOriginal","PriceDiscount","Coupon","Shipping","StoreName","StoreLink","StorePositive","StoreFollowerNum","StoreContact","StoreTop","SkuName"]
    writer = csv.writer(file_csv)
    writer.writerow(header) #write header for each file
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
    script = "document.querySelector(\"#product-detail > div.product-detail-tab > div > div.detail-tab-bar > ul > li:nth-child(3)\").click()"
    driver.execute_script(script)

    _page = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    i=_page.findAll("div",{"class":"glodetail-wrap"})[0]
    
    # tìm thông tin 
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
    detail = {}
    Price ={}
    Shipping={}
    detail['Price'] = Price
    
    Price["Curent"] = price_current
    Price["Original"] = price_original
    Price["Discount"] = price_discount
    Price["Coupon"] = coupon

    shipping = i.findAll("div",{"class":"product-shipping-price"})
    shipping = shipping[0].text.strip() if len(shipping) >0 else ("Please select the country you want to ship from")
    detail["Shipping"] = Shipping
    
    Shipping["Shipping fee"] = shipping

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

    
    # thông tin sku: hình dạng, kích thước, size,...
 
    sku = i.findAll("div",{"class":"sku-wrap"})[0].findAll('div',{"class":"sku-property"})
    for j in sku:
        sku_name = j.findAll("div",{"class":"sku-title"})[0].text.strip()

        sku_value = j.findAll("li",{"class":"sku-property-item"})
        for k in sku_value: 
            value = k.find('img')
            if value is not None:
                value_name = value['alt']
                value_url = value['src'].replace(".jpg_50x50","") 
            else:
                value_name = k.text.strip()
                value_url = ''
       
    # thông số kĩ thuật 
    name_detail = i.findAll("span",{"class":"property-title"})
    for name in name_detail: 
        detail_name = name.text.strip()
    value_detail = i.findAll("span",{"class":"property-desc line-limit-length"})
    for value in value_detail:
        detail_value = value.text.strip()

    # hình ảnh
    image = i.findAll("div",{"class":"images-view-item"})
    for index in image:
        img_link = index.img['src'].replace(".jpg_50x50","")
        img_name = index.img['alt']
    print(detail)
GetProductDetail(product_url)   

