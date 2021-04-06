# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 13:06:33 2021
Referenced:
1. Scraping tutorial: https://www.freecodecamp.org/news/scraping-ecommerce-website-with-python/
2. Continous scrolling scraping: https://morioh.com/p/3d46c0077e45
3. Getting labels for multiple options: https://stackoverflow.com/questions/63946115/extract-text-from-an-aria-label-selenium-webdriver-python
4. Working with bs4 element: https://stackoverflow.com/questions/20968562/how-to-convert-a-bs4-element-resultset-to-strings-python
Author: MeenaSiddharthan @ Github
"""
#Packages to scrape
import requests
from bs4 import BeautifulSoup
import pandas as pd
#from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support import expected_conditions as EC

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
###### Extract URLs #####
#urls = []
#baseurl = "https://shop.lululemon.com"
#soup = BeautifulSoup(driver.page_source, "html.parser")
#productlist = soup.find_all("div",{"class":"product-tile__details"})
##Getting links
#productlinks = []
#for product in productlist:
#    link = product.find("a",{"class":"link lll-font-weight-medium"}).get('href')
#    productlinks.append(baseurl+link)
#Specify main website to scrape from
baseurl = "https://shop.lululemon.com"
#driver = webdriver.Chrome()
overall_df = pd.DataFrame()
#Loop over range of pages to get all product links
for x in range(2):
    #Reading HTML
    #You can apply size filters on the actual website and paste below between (' to ?page=
    k = requests.get('https://shop.lululemon.com/c/sale/_/N-1z0xcuuZ8t6?page='+str(x)).text
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find_all("div",{"class":"product-tile__details"})
    #Getting links for all products
    productlinks = []
    for product in productlist:
            link = product.find("a",{"class":"link lll-font-weight-medium"}).get('href')
            productlinks.append(baseurl+link)
    #Getting product info for each product
    data=[]
    for link in productlinks:
        f = requests.get(link).text
        hun=BeautifulSoup(f,'html.parser')
        try:
            price=hun.find("span",{"class":"price-1SDQy price"}).text.replace("\xa0"," ").replace("USD","")
        except:
            price=None
        try:
            color=hun.find("div",{"class":"purchase-attributes__color-details"}).text
#            color = [my_elem.get_attribute("aria-label") for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.swiper-wrapper>div[aria-label]")))]
        except:
            color=None
        try:
            category=hun.find("ul",{"class":"breadcrumbs-1Pb7p breadcrumbs"}).text.replace("Women's Clothes","")
        except:
            category=None
        try:
            name=hun.find("div",{"itemprop":"name"}).text.replace('\n',"")
        except:
            name=None
        sale = price[price.find('Sale Price ')+11:price.find('  Regular Price ')]
        original = price[price.find('Regular Price ')+14:]
        clothes={"category":category, "name":name, "original price":original, "sale price":sale, "color":color, "product link":link}
        data.append(clothes)
        df = pd.DataFrame(data)
        overall_df = overall_df.append(df)

overall_df = overall_df.drop_duplicates(['name'])

#Saves product info as excel file in same directory
overall_df.to_csv('LLL-WMTM-today.csv',index=False)

##DC scraping
## Import packages
#import requests
#from bs4 import BeautifulSoup
#
## Specify url
#url = 'https://shop.lululemon.com/p/womens-leggings/Wunder-Train-HR-Tight-25-MD/_/prod9860128'
#r = requests.get(url).text
#soup = BeautifulSoup(r)
#color = soup.find_all('purchase-attributes__color-details')
#for i in color:
#    print()
## Package the request, send the request and catch the response: r
#r = requests.get(url)
#
## Extracts the response as html: html_doc
#html_doc = r.text
#
## create a BeautifulSoup object from the HTML: soup
#soup = BeautifulSoup(html_doc)
#
## Print the title of Guido's webpage
#print(soup.title)
#
## Find all 'a' tags (which define hyperlinks): a_tags
#a_tags = soup.find_all('a')
#
## Print the URLs to the shell
#for link in a_tags:
#    print(link.get('href'))