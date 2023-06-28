from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm.notebook import tqdm
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 웹 드라이버 실행
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')

driver = webdriver.Chrome('chromedriver', options=chrome_options)

### 관광지 ID 찾기
start = 0
page = 5
default = 30



name1 = [] ## 관광지 명
star = []
num = [] ## 조회수
id1 = []
loid = []
ttype = []
address = []
image = []


ok = []
nstar = [] #빈 리스트를 확인
nnum = []
ntype = []
nname = []
pageno = [1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 32, 33, 34, 35, 36] ## 이 번호에만 data 존재함

for i in tqdm(range(start * default, (page * default) + start * default, default),
              desc='관광지'):  ## 트립어드바이저 홈페이지의 페이지 단위가 30임
    if (i == 0):
        url = (
                    'https://www.tripadvisor.co.kr/Search?q=%EC%98%A4%EC%82%AC%EC%B9%B4&searchSessionId=C165D459AF7899A50A6C2D661B1149A91678970275509ssid&searchNearby=false&geo=14135010&sid=A47DD1D5D4684054883832BE97B9463E1679018171102&blockRedirect=true&ssrc=A&rf=' + str(
                i))
    elif (i == 30):
        url = 'https://www.tripadvisor.co.kr/Search?q=%EC%98%A4%EC%82%AC%EC%B9%B4&searchSessionId=C165D459AF7899A50A6C2D661B1149A91678970275509ssid&searchNearby=false&geo=14135010&sid=A47DD1D5D4684054883832BE97B9463E1679018171102&blockRedirect=true&ssrc=A&rf=32&o=30'
    elif (i == 60):
        url = 'https://www.tripadvisor.co.kr/Search?q=%EC%98%A4%EC%82%AC%EC%B9%B4&searchSessionId=C165D459AF7899A50A6C2D661B1149A91678970275509ssid&searchNearby=false&geo=14135010&sid=A47DD1D5D4684054883832BE97B9463E1679018171102&blockRedirect=true&ssrc=A&rf=33&o=60'
    elif (i == 90):
        url = 'https://www.tripadvisor.co.kr/Search?q=%EC%98%A4%EC%82%AC%EC%B9%B4&searchSessionId=C165D459AF7899A50A6C2D661B1149A91678970275509ssid&searchNearby=false&geo=14135010&sid=A47DD1D5D4684054883832BE97B9463E1679018171102&blockRedirect=true&ssrc=A&rf=34&o=90'
    print(url)
    driver.get(url)
    time.sleep(1)

    alln = []
    n1 = []
    n2 = []
    n3 = []
    n4 = []
    d = 0
    for k in tqdm((pageno), desc='페이지'):
        notices = driver.find_elements(By.CSS_SELECTOR,
                                       'div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div:nth-child(' + str(
                                           k) + ') > div > div > div > div.ui_column.is-9-desktop.is-8-mobile.is-9-tablet.content-block-column > div > div.result-title')
        notices2 = driver.find_elements(By.XPATH,
                                        '/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[' + str(
                                            k) + ']/div/div/div/div[2]/div[1]/div[2]/div/span')  # 별점
        notices3 = driver.find_elements(By.XPATH,
                                        '/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[' + str(
                                            k) + ']/div/div/div/div[2]/div[1]/div[2]/div/a')  # 조회수
        notices4 = driver.find_elements(By.XPATH,
                                        '/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div[' + str(
                                            k) + ']/div/div/div/div[1]/div/div[2]/span[2]')  # type
        notices5 = driver.find_elements(By.CSS_SELECTOR,
                                        'div.prw_rup.prw_search_search_results.ajax-content > div > div.main_content.ui_column.is-12 > div > div:nth-child(2) > div > div > div:nth-child(' + str(
                                            k) + ') > div > div > div > div.ui_column.is-3-desktop.is-3-tablet.is-4-mobile.thumbnail-column > div > div.frame > div > div.aspect.is-shown-at-tablet.is-hidden-desktop > div')
        notices6 = driver.find_elements(By.CSS_SELECTOR, ' div.location-meta-block > div.address')

        alln.append(k)
        if not notices:
            n1.append(k)
        if not notices2:
            n2.append(k)
        if not notices3:
            n3.append(k)
        if not notices4:
            n4.append(k)

        try:
            for link in notices4:
                ttype.append(link.text.strip())

        except:
            print("error10")
            ttype.append('')
            continue

        star2 = []
        star3 = []
        for link in notices:
            a = link.get_attribute('onclick')
            star2.append(re.sub("[,}');-edR]", '', str(a)[70:78]))
        for link in notices:
            a = link.get_attribute('onclick')
            star3.append(re.sub("[,}');-edR]", '', str(a)[78:87]))
        star2 = list(filter(None, star2))
        star3 = list(filter(None, star3))  ## None값 제거

        for i in range(len(star2)):
            loid.append(star2[i].strip("-"))
            id1.append(star3[i].strip("-"))

        for n in notices:
            name1.append(n.text.strip())
            ## 가져온 관광지 명의 text를 strip (분리)

        star1 = []

        for link in notices2:
            t = link.get_attribute('alt')
            star1.append((str(t)[7:]))  ## 8번째 글자부터 가져오기
        star1 = list(filter(None, star1))  ## None값 제거
        star1 = list(map(float, star1))  ## 문자열을 숫자로

        for i in star1:
            star.append(i * 10)
        star = list(map(int, star))

        b = []
        for link in notices3:
            b.append(link.text.strip()[:-5])  ##뒤에서 5번째 글짜부터 가져오기
            num.append(re.sub('[,]', '', b[0]))
        num = list(map(int, num))

        for link in notices5:
            b = link.get_attribute('style')
            image.append(b.strip()[23:-3])

        b = []
        for link in notices6:
            b.append(link.text.strip())
        address.append(b[d].strip()[:-9])
        d = d + 1

    ok.append(alln)
    nstar.append(n1)
    nnum.append(n2)
    ntype.append(n3)
    nname.append(n4)

print(loid)
print(id1)
print(name1)
print(star)
print(num)
print(ttype)
print(address)
print(image)