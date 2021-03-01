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
chrome_options.add_argument("--headless") # hide popup 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
# original link 
driver = webdriver.Chrome(executable_path = "C:\\Users\\tlhqu\\Downloads\\chromedriver_win32\\chromedriver.exe", chrome_options=chrome_options)
driver.get("https://best.aliexpress.com/?lan=en")
try:
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME , 'categories')))
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
_page = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()
product_more =  _page.findAll("ul",{"class" : "_2nJnr"})[0].findAll("li")
product_url_field = "URL"
product_name_field = "Name"
product_price_field = "Price"
product_img_link_field = "ImgLink"
list_str = []
for i in product_more:
    product_url = i.a['href']
    product_name = i.findAll("div",{"class":"jareR"})[0].text.strip().replace('"','')
    product_price = i.findAll("div",{"class":"_2mGMG"})
    product_price = product_price[0].text.replace("₫ ","").strip() if len( product_price)>0 else ""

    img_link = i.a.img['src'].replace("jpg_350x350.","")
    product_str = "{\"" + product_name_field  + "\":\"" + product_name + "\",\"" + product_url_field   + "\":\"" + product_url  + "\",\"" + product_price_field  + "\":\"" + product_price + "\",\"" + product_img_link_field  + "\":\"" + img_link + "\"}"
    print(product_str)
    list_str.append(product_str)

categories_list=_page.findAll("dt",{"class":"cate-name"})
cate_name_field = "CateName"
cate_id_field = "CateID"
list_cate_str = []
for cate in categories_list: 
    url = cate.a["href"]
    cate_name = url.split("/")[-1].replace('.html','')
    cate_id = url.split("/")[-2]
    cate_str = "{\"" + cate_name_field + "\":\"" + cate_name + "\",\"" + cate_id_field + "\":\"" + cate_id + "\"}"
    print(cate_str)
    list_cate_str.append(cate_str)
cate = "{\"Product\":[" + ",".join(list_str) + "] ,\"Cate\":[" + ",".join(list_cate_str) + "]}"
file = open("cate.json", "w",encoding="utf8")
file.write(cate)


