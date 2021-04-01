# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 13:06:33 2021

@author: m.siddharthan
"""
#Packages to scrape
import requests
from bs4 import BeautifulSoup
import pandas as pd

##Packages to scrape infinite scrolling
#import time
#from selenium import webdriver
#from urllib.parse import urljoin
#
##Code to get URL from inifinte scrolling
#driver = webdriver.Chrome(executable_path=r"E:\Chromedriver\chromedriver_win32_chrome83\chromedriver.exe")
#driver.get("https://shop.lululemon.com/c/sale/_/N-1z0xcuuZ8t6")
#time.sleep(2)  # Allow 2 seconds for the web page to open
#scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
#screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
#i = 1
#
#while True:
#    # scroll one screen height each time
#    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
#    i += 1
#    time.sleep(scroll_pause_time)
#    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
#    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
#    # Break the loop when the height we need to scroll to is larger than the total scroll height
#    if (screen_height) * i > scroll_height:
#        break 
#
###### Extract Reddit URLs #####
#urls = []
#baseurl = "https://shop.lululemon.com"
#soup = BeautifulSoup(driver.page_source, "html.parser")
#productlist = soup.find_all("div",{"class":"product-tile__details"})
##Getting links
#productlinks = []
#for product in productlist:
#    link = product.find("a",{"class":"link lll-font-weight-medium"}).get('href')
#    productlinks.append(baseurl+link)

baseurl = "https://shop.lululemon.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

overall_df = pd.DataFrame()
for x in range(2):
    k = requests.get('https://shop.lululemon.com/c/sale/_/N-1z0xcuuZ8t6?page='+str(x)).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("div",{"class":"product-tile__details"})
    #Getting links
    productlinks = []
    for product in productlist:
            link = product.find("a",{"class":"link lll-font-weight-medium"}).get('href')
            productlinks.append(baseurl+link)
    #Getting product info
    data=[]
    for link in productlinks:
        f = requests.get(link,headers=headers).text
        hun=BeautifulSoup(f,'html.parser')
        try:
            price=hun.find("span",{"class":"price-1SDQy price"}).text.replace("\xa0"," ").replace("USD","")
        except:
            price=None
        try:
            color=hun.find("div",{"class":"purchase-attributes__color-details"}).text
        except:
            color=None
        try:
            size=hun.find("div",{"class":"swiper-wrapper"}).text.replace('\n',"")
        except:
            size=None
        try:
            name=hun.find("div",{"itemprop":"name"}).text.replace('\n',"")
        except:
            name=None
        sale = price[price.find('Sale Price ')+11:price.find('  Regular Price ')]
        original = price[price.find('Regular Price ')+14:]
        clothes={"name":name, "original price":original, "sale price":sale, "color":color, "size":size, "product link":link}
        data.append(clothes)
        df = pd.DataFrame(data)
        overall_df = overall_df.append(df)
overall_df = overall_df.drop_duplicates(['name'])
overall_df.to_csv('LLL-WMTM-today.csv',index=False)
#text = """ 
#<div class="swiper-wrapper" style="transform: translate3d(0px, 0px, 0px);">
#<div role="radio" tabindex="-1" aria-checked="false" aria-label="Violet Verbena" class="swiper-slide swatch available swiper-slide-next" style="margin-right: 12px;">
#<div role="radio" tabindex="-1" aria-checked="false" aria-label="Black" class="swiper-slide swatch available swiper-slide-next" style="margin-right: 12px;">
#<div role="radio" tabindex="-1" aria-checked="false" aria-label="Coral" class="swiper-slide swatch available swiper-slide-next" style="margin-right: 12px;">
#</div>"""
#text1=BeautifulSoup(text,'html.parser')
#text1.find_all(lambda tag: tag.name == 'div' and tag.get('role') == ['product'])