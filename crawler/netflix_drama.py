import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# 브라우저 열기
browser = webdriver.Chrome()
url = "https://www.netflix.com/browse/genre/2638104?bc=83&so=su&locale=ko-KR"
browser.get(url)
browser.maximize_window()

# time.sleep(3)
login = browser.find_element_by_class_name("authLinks")  
login.click()

# login 과정 진행
id = browser.find_element_by_name("userLoginId").send_keys("2ee10@naver.com")
pw = browser.find_element_by_name("password").send_keys("yeng0912%$")
browser.find_element_by_class_name("btn-submit").click()
time.sleep(3)
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[3]/div/a/div/div').click()
# time.sleep(5)
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/input[1]').send_keys("2")
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/input[2]').send_keys("0")
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/input[3]').send_keys("0")
browser.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/input[4]').send_keys("2")

# 크롤링 진행하기
# 일단 페이지를 모두 로드한다.
interval = 2
prev_height = browser.execute_script("return document.body.scrollHeight")

# 높이 변화가 없을 때 까지 스크롤을 내린다.
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(interval)
    curr_height = browser.execute_script("return document.body.scrollHeight")

    if prev_height == curr_height:
        break

    prev_height = curr_height
print('scroll end')


curr_html = browser.page_source
soup = BeautifulSoup(curr_html, "html.parser")
dummys = soup.find_all("a", attrs={"class":"slider-refocus"})
name_ls = []
for idx, dummy in enumerate(dummys):
    name = dummy.get_text()
    name_ls.append(name)
    # image_url = dummy.img["src"]
    # print(image_url)

    # image_res = requests.get(image_url)
    # image_res.raise_for_status()

    # try:
    #     with open("{0}.jpg".format(name), 'wb') as f:
    #         f.write(image_res.content)
    #         # time.sleep(0.3)
    # except:
    #     pass

# csvfile gen
f = open("netflix_movie.csv", "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
title = ["index", "name", "synopsis", "genre", "netflix", "tiving"]
writer.writerow(title)

# 한개 씩 클릭가능한 코드 만들기
elems = browser.find_elements_by_class_name('slider-item')
for i, elem in enumerate(elems):
    try:
        # if i in [3, 12, 26, 29, 30, 41, 42, 53, 54, 63, 68, 69, 87, 89, 90, 96, 114, 121, 124, 140, 169, 174, 175]:
        data = []
        data.append(i)
        data.append(name_ls[i])
        elem.click()
        time.sleep(2)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        synopsis = soup.find("p", attrs={"class":"preview-modal-synopsis"}).get_text()
        genre = soup.find("div", attrs={"data-uia":"previewModal--tags-genre"}).get_text().replace('장르: ', '')

        data.append(synopsis)
        data.append(genre)
        # netflix 는 2번째 인덱스를 1
        data.append(1)
        # Tving 은 3번째 인덱스를 1
        data.append(0)
        writer.writerow(data)
        print(data) # csv file로 저장하기 전 테스트 출력
        browser.find_element_by_class_name("previewModal-close").click()
        time.sleep(2)
    except:
        print("pass")
        try:
            browser.find_element_by_class_name("previewModal-close").click()
        except:
            pass