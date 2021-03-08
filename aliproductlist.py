import urllib.request
from bs4 import BeautifulSoup
import bs4
import json
import requests
import urllib.request
import shutil
import time
import uuid
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import dictfier
from selenium.webdriver import ActionChains
''' option install  '''
chrome_options = Options()  
# chrome_options.binary_location = "/usr/lib/chromium-browser/chromium-browser"
chrome_options.add_argument("--headless") # hide popup 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
# original link 
website = "https://best.aliexpress.com/?lan=en"
import sys
class Product:
    def __init__(self, name,url, priceCurrent,priceOriginal, priceDiscount,shipping,rate,storeName,storeLink, imgLink):
        self.Name = name
        self.URL = url
        self.PriceCurrent = priceCurrent
        self.PriceOriginal = priceOriginal
        self.PriceDiscount = priceDiscount
        self.Shipping = shipping
        self.Rate = rate
        self.StoreName = storeName
        self.StoreLink = storeLink
        self.ImgLink = imgLink
class SubCategory:
    def __init__(self, name, url,id):
        self.SubCateName = name
        self.SubCateURL = url
        self.SubCateID = id
class DataProductList:
    def __init__(self, products, subcategories):
        self.Products = products
        self.SubCategories = subcategories
def GetProductList(max_num_pages,url):
    list_product = []   
    url =  url
    for ele in range(1,max_num_pages+1):              
        driver = webdriver.Chrome(executable_path = "C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)   
        print(" >> ",url + str(ele) + "&isrefine=y" )
        driver.get(url + str(ele) + "&isrefine=y" )
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME , 'product-container')))
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
        scate_list = []
        scate_name_field = "Subcate_name"
        scate_link_field = "Subcate_link"
        sub = _page.findAll("ul",{"class":"child-menu"})
        sub = sub[0].findAll("li") if len(sub) > 0 else ""
        for i in sub: 
            scate_id = i['ae_object_value']
            print(scate_id)
            scate_name = i.a.text.strip()
            scate_url = i.a["href"]
            scate_str = SubCategory(scate_name,scate_url,scate_id)
            scate_list.append(scate_str)

        post=_page.findAll("li",{"class":"list-item"})
    
        list_product_str = []
       
        for i in post:
            
            product_url = i.a["href"]
            product_title = i.text.strip()
            product_price_current = i.findAll("span",{"class":"price-current"})
            product_price_current = product_price_current[0].text.strip() if len(product_price_current)>0 else ""
            product_price_origin =  i.findAll("span",{"class":"price-original"})
            product_price_origin = product_price_origin[0].text.strip() if len(product_price_origin)>0 else ""         
            product_price_discount = i.findAll("span",{"class":"price-discount"})
            product_price_discount = product_price_discount[0].text.strip() if len( product_price_discount)>0 else ""
            product_shipping = i.findAll("span",{"class":"shipping-value"})
            product_shipping = product_shipping[0].text.strip() if len( product_shipping)>0 else ""
            product_rate = i.findAll("span",{"class":"rating-value"})
            product_rate = product_rate[0].text.strip() if len(product_rate)>0 else ""
            product_store = i.findAll("div",{"class":"item-store-wrap"})
            product_store = product_store[0].a.text.strip() if len(product_store)>0 else ""
            product_store_link = i.findAll("div",{"class":"item-store-wrap"})
            product_store_link = product_store_link[0].a['href'] if len(product_store_link)>0 else ""
            product_img_link = i.findAll("div",{"class":"product-img"})[0].a.img["src"].replace(".jpg_220x220xz","")
            product_img_name = i.findAll("div",{"class":"product-img"})[0].a.img["alt"]
            
            product_str = Product(product_title,product_url,product_price_current,product_price_origin,product_price_discount,product_shipping,product_rate,product_store,product_store_link,product_img_link)
            list_product_str.append(product_str)
        
           
        data = DataProductList(list_product_str,scate_list)

 
        query = [
            {
                "Products": [
                    [       
                        "Name",
                        "URL",
                        "PriceCurrent",
                        "PriceOriginal" ,
                        "PriceDiscount",
                        "Shipping",
                        "Rate",
                        "StoreName",
                        "StoreLink",
                        "ImgLink"
                    ]
                ]
            },
            {
                "SubCategories": [
                    [
                        "SubCateName",
                        "SubCateURL",
                        "SubCateID"
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


url = "https://vi.aliexpress.com/af/category/200003455.html?trafficChannel=af&catName=parkas&CatId=200003455&ltype=affiliate&SortType=default&page="
GetProductList(max_num_pages=2,url=url)               
           









