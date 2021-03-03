import os
import dictfier
import uuid
import urllib.request
from bs4 import BeautifulSoup
import bs4
import json
import requests
import shutil
import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import dictfier
from selenium.webdriver import ActionChains
''' option install  '''
chrome_options = Options()
chrome_options.add_argument("--headless")  # hide popup
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
# original link
def GetHomePageShoppee():
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)
    driver.get("https://shopee.vn/")
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'home-page')))
        # print("Page is ready!")
    except TimeoutException:
        print("Loading took too much")
    scrolls = 4
    while True:
        scrolls -= 1
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 1080)")
        if scrolls < 0:
            break
    _page = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    product_link_field = "URL"
    product_name_field = "Name"
    product_price_field = "Price"
    product_like_field = "Like"
    product_percent_reduce_field = " Reduce Percent"
    product_img_link_field = "ImgLink"
    cate_name_field = "NameCate"
    cate_url_field = "URLCate"
    cate_id_field = "IDCate"

    class Product:
        def __init__(self, url, name, price,like,percent, imgLink):
            self.URL = url
            self.Name = name
            self.Price = price
            self.Like = like
            self.Percent = percent
            self.ImgLink = imgLink


    class Category:
        def __init__(self, name, cateId,url):
            self.CateName = name
            self.CateId = cateId
            self.URL = url

    class DataHomePage:
        def __init__(self, products, categories):
            self.Products = products
            self.Categories = categories


    list_product=[]
    product_today = _page.findAll("div",{"class","K8sUwg"})
    for i in product_today: 
        product_link = "https://shopee.vn" +i.a['href'] 
        product_name = i.findAll("div",{"class":"_1NoI8_ _1co5xN"})[0].text
        product_img_link = i.findAll("div",{"class":"_39-Tsj _1tDEiO"})[0].img['src']
        product_price = i.findAll("span",{"class":"djJP_7"})
        product_price = product_price[0].text if len(product_price) > 0 else ""
        product_like = i.findAll("span",{"class":"_1DeDTg"})
        product_like = product_like[0].text if len(product_like) > 0 else ""
        product_percent_reduce = i.findAll("span",{"class":"percent"})
        product_percent_reduce = product_percent_reduce[0].text + " Giảm" if len(product_percent_reduce) > 0 else ""
        product = Product(product_link,product_name,product_price,product_like,product_percent_reduce,product_img_link)
        list_product.append(product)
    list_cate = []
    cate = _page.findAll("a",{"class":"home-category-list__category-grid"})
    for i in cate:
        cate_url = "https://shopee.vn" + i["href"]
        cate_name = i.findAll("div",{"class":"_1NLLsA"})[0].text
        cate_id = cate_url.split(".")[-1]
        cate = Category(cate_name,cate_id,cate_url)
        list_cate.append(cate)
    data = DataHomePage(list_product, list_cate)
    query = [
        {
            "Products": [
                [       
                    "URL",
                    "Name",
                    "Price",
                    "Like",
                    "Percent",
                    "ImgLink"
                ]
            ]
        },
        {
            "Categories": [
                [
                    "CateName",
                    "CateId",
                    "URL"
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
GetHomePageShoppee()