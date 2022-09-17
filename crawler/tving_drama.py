import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv

# 브라우저 열기
browser = webdriver.Chrome()
url = "https://www.tving.com/list/program?genre=PCA"
browser.get(url)
browser.maximize_window()

# time.sleep(3)
browser.find_element_by_xpath('//*[@id="scroll-section-0"]/div/button').click()
time.sleep(0.5)
browser.find_element_by_xpath('//*[@id="locLogin"]').click()

# login 과정 진행
time.sleep(0.5)
id = browser.find_element_by_xpath('//*[@id="a"]').send_keys("**********")  # 개인 패스워드 아이디 입력
pw = browser.find_element_by_xpath('//*[@id="b"]').send_keys("***********")
browser.find_element_by_xpath('//*[@id="doLoginBtn"]').click()
time.sleep(3)
browser.find_element_by_xpath('//*[@id="266434412"]/img').click()
time.sleep(0.5)
browser.find_element_by_xpath('//*[@id="__next"]/header/a[3]/div').click()
time.sleep(0.5)
browser.find_element_by_class_name('css-1g181ci').click()

# 크롤링 진행하기
# 일단 페이지를 모두 로드한다.
interval = 2
# 높이 변화가 없을 때 까지 스크롤을 내린다.
for _ in range(6):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(interval)
print('scroll end')


curr_html = browser.page_source
soup = BeautifulSoup(curr_html, "html.parser")
images = soup.find_all("img", attrs={"class":"loaded"})
titles = soup.find_all("p", attrs={"class":"item__title"})
name_ls = []
for image, title in zip(images[2:-1], titles):
    name = title.get_text()
    name_ls.append(name)
    # image_url = image["src"]

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
elems = browser.find_elements_by_class_name('execn1x0')[2:-1]
elems_len = len(elems)
for i in range(elems_len):
    elems = browser.find_elements_by_class_name('execn1x0')[2:-1]
    try:
        # if i in [3, 12, 26, 29, 30, 41, 42, 53, 54, 63, 68, 69, 87, 89, 90, 96, 114, 121, 124, 140, 169, 174, 175]:
        data = []
        data.append(i)
        data.append(name_ls[i])
        elems[i].click()
        time.sleep(1)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        synopsis = " ".join(soup.find("p", attrs={"class":"e9icmb82"}).get_text().split())
        genre = ""

        data.append(synopsis)
        data.append(genre)
        # netflix 는 2번째 인덱스를 1
        data.append(0)
        # Tving 은 3번째 인덱스를 1
        data.append(1)
        writer.writerow(data)
        print(data) # csv file로 저장하기 전 테스트 출력
        browser.back()
        time.sleep(1)
    except:
        print("pass")
        try:
            browser.find_element_by_class_name("previewModal-close").click()
        except:
            pass