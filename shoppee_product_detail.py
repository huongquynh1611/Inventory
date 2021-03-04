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
import uuid
import os,dictfier
chrome_options = Options()  
chrome_options.add_argument("--headless") # hide popup 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')

import sys
class Porperty:
    def __init__(self, name, value):
        self.Name = name
        self.Value = value
class Product:
     def __init__(self,title, rating,priceCurrent,priceOrigin,priceDiscount):
        self.Title = title
        self.Rating = rating
      
        self.PriceCurrent = priceCurrent
        self.PriceOrigin = priceOrigin
        self.PriceDiscount = priceDiscount

class Store: 
    def __init__(self,link,ava,name,time,info):
        self.Link = link
        self.Ava = ava
        self.Name = name
        self.Time = time
        self.Info = info

class ProductInfo:
    def __init__(self,infoName,infoValue):
        self.InfoName = infoName
        self.InfoValue = infoValue
class Img:
     def __init__(self,imgLink):
        self.ImgLink = imgLink
class ShoppeeProductDetail:
    def __init__(self, porperties,products,stores,productinfos,imglinks):
        self.Porperties = porperties
        self.Products = products
        self.Stores = stores
        self.ProductInfos = productinfos
        self.ImgLinks = imglinks








product_url = "https://shopee.vn/-NH%E1%BA%ACP-WASTWA1-GI%E1%BA%A2M-10K-%C4%90%C6%A0N-B%E1%BA%A4T-K%C3%8C-SI%C3%8AU-HOT-Qu%E1%BA%A7n-legging-%C4%91%C3%B9i-si%C3%AAu-hot-i.65519999.2016528890"
def GetProductDetail(product_url):     
    driver = webdriver.Chrome(executable_path = "C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)   
    print(" >> ",product_url)
    driver.get(product_url)  
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME , 'container')))
        print("Page is ready!")
    except TimeoutException:
        print ("Loading took too much") 

    scrolls = 4
    while True:
        scrolls -= 1
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 1080)")
        if scrolls < 0:
            break
    _page = BeautifulSoup(driver.page_source, "html.parser")

    product_list=[]
    title = _page.findAll("div",{"class":"_3ZV7fL"})[0].text
    rating = _page.findAll("div",{"class":"_3WXigY _22cC7R"})
    rating = rating[0].text if len(rating) > 0 else ""
    
    
    price_current = _page.findAll("div",{"class":"AJyN7v"})
    price_current = price_current[0].text if len(price_current) > 0 else ""
    price_origin = _page.findAll("div",{"class":"bBOoii"})
    price_origin = price_origin[0].text if len(price_origin) > 0 else ""
    price_discount = _page.findAll("div",{"class":"_3ghar9"})
    price_discount = price_discount[0].text if len(price_discount) > 0 else ""
   
    product = Product(title,rating,price_current,price_origin,price_discount)
    product_list.append(product)
    _porperty = _page.findAll("div",{"class":"flex _1nb0l8 _2J8-Qs"})
    
    porperty_list = []
    for i in _porperty:
        name = i.findAll("div",{"style":"margin-bottom: 8px; align-items: baseline;"})
        for k in name: 
            porperty_name = k.label.text
            list_value = []      
            value = k.findAll("button")
            for j in value:
                list_value.append( j.text)
            porperty = Porperty(porperty_name,list_value)
            porperty_list.append(porperty)
    # store 
    store_list = []
    store_link ="https://shopee.vn"+ _page.findAll("div",{"class":"_3XjqaB"})[0].a["href"]
    store_ava = _page.findAll("div",{"class":"shopee-avatar _3sZdoP"})[0].img['src']
    store_name = _page.findAll("div",{"class":"_3KP9-e"})[0].text
    store_time = _page.findAll("div",{"class":"_2QJIt0"})[0].text
    _inf = _page.findAll("div",{"class":"dos2U- eTrFKz"})
    store_info = []
    for inf in _inf:
        inf_name = inf.label.text
       
        inf_value = inf.span.text
      
        list_info = {}
        list_info[inf_name] = inf_value
        
        store_info.append(list_info)
    store = Store(store_link,store_ava,store_name,store_time,store_info)    
    store_list.append(store)
  
    # thông tin sản phẩm
    info_list = []
    product_inf = _page.findAll("div",{"class":"UjOlxf"})
    info = product_inf[0].findAll("div",{"class":"_2gVYdB"})
    for i in info:
        name_info = i.label.text
        value_info = i.a
        value_info = i.a.text if value_info is not None  else i.div.text

        productinfo = ProductInfo(name_info,value_info)
        info_list.append(productinfo)
    # hình ảnh 
    img_list = []
    product_img = _page.findAll("div",{"class":"_2wBoeW V1Fpl5"})
    for img in product_img:
        img_link = (img["style"].split('"')[1])
        link = Img(img_link)
        img_list.append(link)


    data = ShoppeeProductDetail(porperty_list,product_list,store_list,info_list,img_list)
    query = [
        {
            "Porperties": [
                [       
                    "Name",
                    "Value"
                ]
            ]
        },
        {
            "Products":[
                [
                "Title",
                "Rating",
               
                "PriceCurrent",
                "PriceOrigin",
                "PriceDiscount"
                ]
            ]
        },
        {
            "Stores":[
                [
                "Link",
                "Ava",
               
                "Name",
                "Time",
                "Info"
                ]
            ]
        },
        {
            "ProductInfos":[
                [
               "InfoName",
               "InfoValue"
                ]
            ]
        },
        {
            "ImgLinks":[
                [
               "ImgLink" 
                ]
            ]
        }
    ]
    std_info = dictfier.dictfy(data, query)

    file_name = uuid.uuid4().hex + ".json"

    completeName = os.path.join(os.getcwd(), file_name)

    file = open(completeName, "w", encoding="utf8")
    file.write(json.dumps(std_info))
    file.close()
GetProductDetail(product_url)   
