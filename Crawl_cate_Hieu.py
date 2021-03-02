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
from selenium.webdriver import ActionChains
''' option install  '''
chrome_options = Options()
chrome_options.add_argument("--headless")  # hide popup
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
# original link
driver = webdriver.Chrome(
    executable_path="C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)
driver.get("https://best.aliexpress.com/?lan=en")
try:
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'categories')))
    # print("Page is ready!")
except TimeoutException:
    print("Loading took too much")
scrolls = 3
while True:
    scrolls -= 1
    time.sleep(1)
    driver.execute_script("window.scrollBy(0, 1080)")
    if scrolls < 0:
        break
_page = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
product_more = _page.findAll("ul", {"class": "_2nJnr"})[0].findAll("li")
product_url_field = "URL"
product_name_field = "Name"
product_price_field = "Price"
product_img_link_field = "ImgLink"
list_str = []


class Product:
    def __init__(self, url, name, price, imgLink):
        self.URL = url
        self.Name = name
        self.Price = price
        self.ImgLink = imgLink


class Category:
    def __init__(self, name, cateId):
        self.CateName = name
        self.CateId = cateId

class DataHomePage:
    def __init__(self, products, categories):
        self.Products = products
        self.Categories = categories
    

for i in product_more:
    product_url = i.a['href']
    product_name = i.findAll("div", {"class": "jareR"})[
        0].text.strip().replace('"', '')
    product_price = i.findAll("div", {"class": "_2mGMG"})
    product_price = product_price[0].text.replace(
        "₫ ", "").strip() if len(product_price) > 0 else ""

    img_link = i.a.img['src'].replace("jpg_350x350.", "")
    #product_str = "{\"" + product_name_field  + "\":\"" + product_name + "\",\"" + product_url_field   + "\":\"" + product_url  + "\",\"" + product_price_field  + "\":\"" + product_price + "\",\"" + product_img_link_field  + "\":\"" + img_link + "\"}"
    # print(product_str)

    product = Product(product_url, product_name, product_price, img_link)
    list_str.append(product)

categories_list = _page.findAll("dt", {"class": "cate-name"})
cate_name_field = "CateName"
cate_id_field = "CateID"
list_cate_str = []
for cate in categories_list:
    url = cate.a["href"]
    cate_name = url.split("/")[-1].replace('.html', '')
    cate_id = url.split("/")[-2]
    # cate_str = "{\"" + cate_name_field + "\":\"" + cate_name + \
    #     "\",\"" + cate_id_field + "\":\"" + cate_id + "\"}"
    
    category = Category(cate_name, cate_id)
    list_cate_str.append(category)
#cate = "{\"Product\":[" + ",".join(list_str) + "] ,\"Cate\":[" + ",".join(list_cate_str) + "]}"

data = DataHomePage(list_str, list_cate_str)
query = [
    {
        "Products": [
            [       
                "Name",
                "URL",
                "Price",
                "ImgLink"
            ]
        ]
    },
    {
        "Categories": [
            [
                "CateName",
                "CateId"
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