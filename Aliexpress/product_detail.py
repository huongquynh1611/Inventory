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
website = "https://best.aliexpress.com/?lan=en"
import sys

product_url = "https://vi.aliexpress.com/item/1005002223429433.html?spm=a2g0o.productlist.0.0.140e7370bBw0bq&algo_pvid=f55b4ac0-6295-4b9d-a9c5-21bc4b1d1c8f&algo_expid=f55b4ac0-6295-4b9d-a9c5-21bc4b1d1c8f-6&btsid=0bb0624216147556764928774e7c7d&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
class ProductDetail:
    def __init__(self, proName, rate,priceCurrent,priceOrigin,priceDiscount,coupon,shipping):
        self.ProName = proName
        self.Rate = rate
        self.PriceCurrent = priceCurrent
        self.PriceOrigin = priceOrigin
        self.PriceDiscount = priceDiscount
        self.Coupon = coupon
        self.Shipping = shipping
class Store: 
    def __init__(self,storeName, url,storePositive,storeFollowerNum,storeContact,storeTop):
        self.StoreName = storeName
        self.URL = url
        self.StorePositive = storePositive
        self.StoreFollowerNum = storeFollowerNum
        self.StoreContact = storeContact
        self.StoreTop = storeTop
class SKU:
    def __init__(self, skuName, skuValue):
        self.SKUName = skuName
        self.SKUValue = skuValue

class Img:
    def __init__(self, imgName, imgLink):
        self.ImgName = imgName
        self.ImgLink = imgLink


class Specification:
    def __init__(self, detailName, detailValue):
        self.DetailName = detailName
        self.DetailValue = detailValue

class DataProductDetail:
    def __init__(self, productDetails, stories,skus,imgs,specifications):
        self.ProductDetails = productDetails
        self.Stories = stories
        self.SKUs = skus
        self.Imgs = imgs
        self.Specifications = specifications


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
        
    script = "document.querySelector(\"#product-detail > div.product-detail-tab > div > div.detail-tab-bar > ul > li:nth-child(3)\").click()"
    driver.execute_script(script)

    _page = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    i=_page.findAll("div",{"class":"glodetail-wrap"})[0]
    list_pro = []
    # tìm thông tin 
    title = i.findAll("div",{"class":"product-title"})[0].h1.text.strip()
    rate = i.findAll("span",{"class":"overview-rating-average"})
    rate = rate[0].text if len(rate) > 0 else ""
    price_current = i.findAll("div",{"class":"product-price-current"})[0].span.text.strip()
    price_original = i.findAll("div",{"class":"product-price-original"})
    price_original = price_original[0].findAll("span",{"class":"product-price-value"}) if len(price_original)> 0 else '' 
    price_original =price_original[0].text.strip() if len(price_original) > 0 else ""
    price_discount = i.findAll("div",{"class":"product-price-original"})
    price_discount = price_discount[0].findAll("span",{"class":"product-price-mark"}) if len(price_discount) > 0 else ""
    price_discount = price_discount[0].text.strip() if len(price_discount) >0 else ""
    coupon = i.findAll("div",{"class":"coupon-mark-new"})
    coupon = coupon[0].text.strip() if len(coupon) > 0 else ""
    shipping = i.findAll("div",{"class":"product-shipping-price"})
    shipping = shipping[0].text.strip() if len(shipping) >0 else ("Please select the country you want to ship from")
    productDetail=ProductDetail(title,rate,price_current,price_original,price_discount,coupon,shipping)
    list_pro.append(productDetail)

    # thông tin store
    list_store = []
    store = i.findAll("div",{"class":"shop-name"})
    store_name = store[0].text.strip() if len(store) > 0 else ""
    store_link = store[0].a["href"] if len(store) > 0 else ""
    store_positive = i.findAll("div",{"class":"positive-fdbk"})
    store_positive = store_positive[0].text if len(store_positive) > 0 else ""
    store_follower_num = i.findAll("div",{"class":"follower-num"})
    store_follower_num = store_follower_num[0].text.strip() if len(store_follower_num) > 0 else ""
    store_contact = i.findAll("div",{"class":"store-info-contact"})
    store_contact = store_contact[0].a["href"] if len(store_contact) > 0 else ""
    store_top = i.findAll("div",{"class":"top-seller-label"}) 
    store_top = store_top[0].text.strip() if len(store_top) > 0 else ""
    store = Store(store_name,store_link,store_positive,store_follower_num,store_contact,store_top)
    list_store.append(store)
    # thông tin sku: hình dạng, kích thước, size,...
    sku_list =[]
    sku_ = i.findAll("div",{"class":"sku-wrap"})[0].findAll('div',{"class":"sku-property"})
    for j in sku_:
        sku_name = j.findAll("div",{"class":"sku-title"})[0].text.strip()
        sku_value = []
        _sku_value = j.findAll("li",{"class":"sku-property-item"})
        for k in _sku_value: 
            value = k.find('img')
            if value is not None:
                value_name = value['alt']
                value_url = value['src'].replace(".jpg_50x50","") 
            else:
                value_name = k.text.strip()
                value_url = ''
            list_value = {}
            list_value["Name"] = value_name
            list_value["Url"] = value_url
            sku_value.append(list_value)
        sku = SKU(sku_name,sku_value)
        sku_list.append(sku)
    # thông số kĩ thuật 
    list_detail = []
    
    detail = i.findAll("ul",{"class":"product-specs-list util-clearfix"})[0].findAll("li")
    for q in detail: 
        q=q.text.split(":")
        detail_name = q[0]
        detail_value = q[1]
        detail = Specification(detail_name,detail_value)
        list_detail.append(detail)
    # # hình ảnh
    list_img = []
    image = i.findAll("div",{"class":"images-view-item"})
    for index in image:
        img_link = index.img['src'].replace(".jpg_50x50","")
        img_name = index.img['alt']
    # print(detail)
        img = Img(img_name,img_link)
        list_img.append(img)
    data = DataProductDetail(list_pro,list_store,sku_list, list_img,list_detail)
    query = [
        {
            "ProductDetails": [
                [       
                    "ProName",
                    "Rate",
                    "PriceCurrent",
                    "PriceOrigin",
                    "PriceDiscount",
                    "Coupon",
                    "Shipping"
                ]
            ]
        },
        {
            "Stories": [
                [
                    "StoreName",
                    "URL",
                    "StorePositive",
                    "StoreFollowerNum",
                    "StoreContact",
                    "StoreTop"
                ]
            ]
        },

        {
            "SKUs": [
                [
                    "SKUName",
                    "SKUValue"
                ]
            ]
        },
                {
            "Specifications": [
                [
                    "DetailName",
                    "DetailValue"
                ]
            ]
        },

        {
            "Imgs": [
                [
                    "ImgName",
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

    print(completeName)
GetProductDetail(product_url)   

