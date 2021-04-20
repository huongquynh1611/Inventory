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
website = "https://shopee.vn/"
import sys

URL = []
class Product:
    def __init__(self, name,url, priceCurrent,priceOriginal, priceDiscount,priceText1,priceText2,priceText3,priceText4,priceText5,location,shipping, imgLink,productLike):
        self.Name = name
        self.URL = url
        self.PriceCurrent = priceCurrent
        self.PriceOriginal = priceOriginal
        self.PriceDiscount = priceDiscount
        self.PriceText1 = priceText1
        self.PriceText2 = priceText2
        self.PriceText3 = priceText3
        self.PriceText4 = priceText4
        self.PriceText5 = priceText5
        self.Location = location
        self.Shipping = shipping
        self.ImgLink = imgLink
        self.ProductLike = productLike
class SubCategory:
    def __init__(self, name, url,id):
        self.SubCateName = name
        self.SubCateURL = url
        self.SubCateID = id
class DataProductList:
    def __init__(self, products, subcategories):
        self.Products = products
        self.SubCategories = subcategories
cate_url = "https://shopee.vn/T%E1%BA%AFm-Ch%C4%83m-s%C3%B3c-c%C6%A1-th%E1%BB%83-cat.160.2818?page="
def GetProductList(cate_url,max_num_pages):
    list_product = []   
    url = cate_url   
    for ele in range(0,max_num_pages+1):              
        driver = webdriver.Chrome(executable_path = "C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)   
        print(" >> ",url + str(ele) )
        driver.get(url + str(ele))
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME , '_2eoI9r')))
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
        subcate_list = []
        
        sub = _page.findAll("a",{"class":"shopee-category-list__sub-category"})
        for i in sub: 
            subcate_name = i.text
            subcate_link = "https://shopee.vn" + i['href']
            subcate_id = subcate_link.split(".")[-1]
            subcate = SubCategory(subcate_name,subcate_link,subcate_id)
            subcate_list.append(subcate)

        product_list = []
        product = _page.findAll("div",{"data-sqe":"item"})
        for j in product:
            product_url =  "https://shopee.vn" +j.a['href']
            product_name = j.findAll("div",{"class":"_1NoI8_ A6gE1J _1co5xN"})[0].text.strip()
            # giá hiển thị 
            product_price_current = j.findAll("div",{"class":"_1w9jLI _1DGuEV _7uLl65"})[0].text
            # giá hiển thị bị gạch
            product_price_origin = j.findAll("div",{"class":"_1w9jLI _1y3E4O _2vQ-UF"})
            product_price_origin = product_price_origin[0].text if len(product_price_origin) > 0 else ""
            # giá discount
            product_price_discount = j.findAll("span",{"class":"percent"})
            product_price_discount = product_price_discount[0].text if len(product_price_discount) > 0 else ""
            # thông tin như : mua giá bán buôn/ sỉ, rẻ vô địch ,...
            product_price_text_1 = j.findAll("div",{"class","Lj2P-3"})
            product_price_text_1 = product_price_text_1[0].text if len(product_price_text_1) > 0 else ""
            product_price_text_2 = j.findAll("div",{"class","_2CgHpG"})
            product_price_text_2 = product_price_text_2[0].text if len(product_price_text_2) > 0 else ""
            product_price_text_3 = j.findAll("div",{"class","E9F8gz"})
            product_price_text_3 = product_price_text_3[0].text if len(product_price_text_3) > 0 else ""
            product_price_text_4 = j.findAll("div",{"class","_1FKkT"})
            product_price_text_4 = product_price_text_4[0].text if len(product_price_text_4) > 0 else ""
            product_price_text_5 = j.findAll("div",{"class","_1tJDR9"})
            product_price_text_5 = product_price_text_5[0].text if len(product_price_text_5) > 0 else ""
            # thông tn tỉnh/thành phố
            product_location = j.findAll("div",{"class":"_41f1_p"})
            product_location = product_location[0].text if len(product_location) > 0 else ""
            # Yêu thích 
            product_like = j.findAll("span",{"class":"_1DeDTg"})
            product_like = product_like[0].text if len(product_like) > 0 else ""
            # thông tin có áp dung freehship
            product_icon_freeship = j.findAll("div",{"class":"_3c2vFv"})
            product_icon_freeship = "Yes" if len(product_icon_freeship) > 0 else "No"
            product_img_link = j.findAll("div",{"class":"_39-Tsj _1tDEiO"})[0].img['src']
            product = Product(product_name,product_url,product_price_current,product_price_origin,product_price_discount,product_price_text_1,product_price_text_2,product_price_text_3,product_price_text_4,product_price_text_5,product_location,product_icon_freeship,product_img_link,product_like)
            product_list.append(product)
        data = DataProductList(product_list,subcate_list)
        query = [
            {
                "Products": [
                    [       
                        "Name",
                        "URL",
                        "PriceCurrent",
                        "PriceOriginal",
                        "PriceDiscount",
                        "PriceText1",
                        "PriceText2",
                        "PriceText3",
                        "PriceText4",
                        "PriceText5",
                        "Location",
                        "Shipping",
                        "ImgLink",
                        "ProductLike"
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

GetProductList(cate_url,max_num_pages=1)               
           









