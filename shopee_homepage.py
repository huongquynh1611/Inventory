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
driver = webdriver.Chrome(
    executable_path="C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)
driver.get("https://shopee.vn/")
try:
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'home-page')))
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
product_today = _page.findAll("div",{"class","K8sUwg"})
for i in product_today: 
    if type(i.a['href']) != "NoneType":
      product_link = i.a['href'] 
# product_name = product_link.split(".")[0]
# print(product_name)
      print(product_link)
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

