import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import pandas as pd
from selenium.webdriver.common.keys import Keys

# data read
data = pd.read_csv("C:/Users/SAMSUNG/Desktop/STOLIO AICon/ott_info/data.csv", engine='python', encoding='CP949')
print(data.shape)

data_title = data['name']

# automation
browser = webdriver.Chrome(executable_path="C:/Users/SAMSUNG/Desktop/STOLIO AICon/ott_info/chromedriver.exe")
url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query="
browser.get(url)
browser.maximize_window()

f = open("ott_info.csv", "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
title = ["title", "seezn", "series_on", "watcha", "wavve", "netflix"]
writer.writerow(title)

for item in data_title[100:]:
    elem = browser.find_element_by_id("nx_query")
    elem.send_keys(item + " 보러 가기")
    elem.send_keys(Keys.ENTER)
    time.sleep(1)

    try:
        ott = []
        ott.append(item)
        try:
            browser.find_element_by_class_name("seezn")
            ott.append(1)
        except:
            ott.append(0)

        try:
            browser.find_element_by_class_name("series_on")
            ott.append(1)
        except:
            ott.append(0)

        try:
            browser.find_element_by_class_name("watcha")
            ott.append(1)
        except:
            ott.append(0)

        try:
            browser.find_element_by_class_name("wavve")
            ott.append(1)
        except:
            ott.append(0)

        try:
            browser.find_element_by_class_name("netflix")
            ott.append(1)
        except:
            ott.append(0)
        
        if sum(ott[1:-1]) == 0:
            ott=[item, 0,0,0,0,1]
            print("find fail")

        print(ott)
        writer.writerow(ott)
    
    except:
        print("F")
        writer.writerow([item, "", "", "", "", ""])

    browser.back() 

