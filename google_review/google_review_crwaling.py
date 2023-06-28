import pandas as pd
from bs4 import element, BeautifulSoup
from seleniumwire import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import time

# 웹 드라이버 실행
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--start-maximized") # add
chrome_options.add_argument("--window-size=1920,1080") # add

urls = ['https://www.google.com/maps/place/Shibuya+Center-Street/@35.6600499,139.6975946,17z/data=!4m8!3m7!1s0x60188ca83757a153:0x6f4231232abaf7d1!8m2!3d35.6600456!4d139.6997833!9m1!1b1!16s%2Fg%2F121cxml3']
names = ['Shibuya Center-Street']

for i in range(1):
    driver = webdriver.Chrome('chromedriver', options=chrome_options)

    driver.get(urls[i])
    sleep(20)
    #확정..!
    try:
        to_scroll=driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
    except:
        to_scroll=driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]')

    #review 총 몇개 크롤링할지
    review_total=1000
    #리뷰 데이터 담을 리스트
    result_list = []

    while(True):
        driver.execute_script("arguments[0].scrollBy(0,2000)", to_scroll)
        time.sleep(2)
        breaks = driver.find_elements(By.CLASS_NAME, 'wiI7pd')

        #긴 리뷰의 더보기 클릭
        to_pushs=driver.find_elements(By.CLASS_NAME,'w8nwRe.kyuRq')
        for push in to_pushs:
            push.click()
            time.sleep(0.5)

        print(len(breaks))
        if (len(breaks)>=review_total):
            break
    #리뷰 담기
    to_adds=driver.find_elements(By.CLASS_NAME,'wiI7pd')

    for add in to_adds:
        result_list.append(add.text)

    # csv로 저장
    df = pd.DataFrame(result_list)
    df.to_csv(names[i]+".csv",index=False)
    print(names[i])
