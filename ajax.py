import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Process
import pandas as pd
import bs4
import multiprocessing
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

# chrome_options.binary_location = "/usr/lib/chromium-browser/chromium-browser"
chrome_options.add_argument("--headless") # hide popup 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
website = "https://best.aliexpress.com/?lan=en"
import sys


product_url = "https://vi.aliexpress.com/item/32891519001.html?spm=a2g0o.productlist.0.0.6ca067c4UItzEr&algo_pvid=87827a6d-d056-47a1-8416-b03c6bd4fb1a&algo_expid=87827a6d-d056-47a1-8416-b03c6bd4fb1a-8&btsid=0bb0622a16145949365402963e5a53&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
def GetProductDetail(product_url):

    max_num_pages = 1
    for ele in range(1,max_num_pages+1):              
            driver = webdriver.Chrome(executable_path = "C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)   
            print(" >> ",product_url + str(ele) )
            driver.get(product_url + str(ele))
            try:
                WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID , 'root')))
                print("Page is ready!")
            except TimeoutException:
                print ("Loading took too much")
                continue
            scrolls = 6
            while True:
                scrolls -= 1
                time.sleep(1)
                driver.execute_script("window.scrollBy(0, 1080)")
                if scrolls < 0:
                    break
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
            # for i in sku:
            #     sku_property = i.findAll("div",{"class":"sku-title"})[0].text.strip() 
            #     # if sku_property != "Màu"
            #     sku_value = i.findAll("div",{"class":"sku-property-text"})
            #     for j in sku_value: 
            #         value = j.text.strip() 
            #         print(value)
            #     print(sku_property)
            
            
            

            # print(store_name)
            # print(store_link)
            # sku_1  = sku[0].findAll("div",{"class":"sku-property-image"})
            # for i in color_link:
            #     sku_color_link = i.img["src"].replace(".jpg_50x50","")
            #     sku_color_name = i.img['alt']
            # size_link = sku[1].findAll("div",{"class":"sku-property-image"})
            
            shipping = i.findAll("div",{"class":"product-shipping-price"})
            shipping = shipping[0].text.strip() if len(shipping) >0 else ("Please select the country you want to ship from")
        
            store = i.findAll("div",{"class":"shop-name"})
            store_name = store[0].text.strip() if len(store) > 0 else ""
            store_link = store[0].a["href"] if len(store) > 0 else ""
            store_positive = i.findAll("div",{"class":"positive-fdbk"})[0].text
            store_folower_num = i.findAll("div",{"class":"follower-num"})[0].text
            store_contact = i.findAll("div",{"class":"store-info-contact"})[0].a["href"]
            store_top = i.findAll("div",{"class":"top-seller-label"})
            store_top = store_top[0].text if len(store_top) > 0 else ""
            print(store_contact)
            print(store_top )
GetProductDetail(product_url)
