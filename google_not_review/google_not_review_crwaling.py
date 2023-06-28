from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

import time
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm.notebook import tqdm
import re
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 명소 이름을 담을 빈 리스트 생성
list_names = []

# 명소 평점을 담을 빈 리스트 생성
list_grade = []

# 주소나 전화번호 전체
list_alls=[]

# 영업시간_월요일
list_running_Mon = []
# 영업시간_화요일
list_running_Tue = []
# 영업시간_수요일
list_running_Wed = []
# 영업시간_목요일
list_running_Thur = []
# 영업시간_금요일
list_running_Fri = []
# 영업시간_토요일
list_running_Sat = []
# 영업시간_일요일
list_running_Sun = []

# 영어 주소
list_Address_eng = []
# 영어 주소 아님
list_Address_not_eng = []
#인터넷 주소
list_Address_Internet = []
#전화번호
list_Phone_Number = []
#추가공간
list_bonus_1 = []
list_bonus_2 = []
list_bonus_3 = []

# 웹 드라이버 실행
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')

driver = webdriver.Chrome('chromedriver', options=chrome_options)
driver.maximize_window()

urls=['https://www.google.co.kr/maps/place/%EB%8F%84%EC%BF%84+%ED%83%80%EC%9B%8C/@35.6585848,139.7432389,17z/data=!3m2!4b1!5s0x60188bbd90bf26cf:0x4ceb5b05598646d0!4m6!3m5!1s0x60188bbd9009ec09:0x481a93f0d2a409dd!8m2!3d35.6585805!4d139.7454329!16zL20vMDEzMl94?hl=ko',
'https://www.google.co.kr/maps/place/%EB%A9%94%EC%9D%B4%EC%A7%80+%EC%8B%A0%EA%B6%81/@35.6587083,139.6752104,12z/data=!4m10!1m2!2m1!1z66mU7J207KeAIOyLoOq2gQ!3m6!1s0x60188cb79a4c26e5:0x8fca893849103f73!8m2!3d35.6763976!4d139.6993259!15sChDrqZTsnbTsp4Ag7Iug6raBWhIiEOuplOydtOyngCDsi6DqtoGSAQ1zaGludG9fc2hyaW5l4AEA!16zL20vMDFxX2s5?hl=ko',
'https://www.google.co.kr/maps/place/%EB%8F%84%EC%BF%84+%EC%8A%A4%EC%B9%B4%EC%9D%B4%ED%8A%B8%EB%A6%AC/@35.7103194,139.8089334,17z/data=!3m1!5s0x60188ed6f9e7acb7:0x486cece4c5ab3730!4m10!1m2!2m1!1z64-E7L-EIOyKpOy5tOydtO2KuOumrA!3m6!1s0x60188ed0d12f9adf:0x7d1d4fb31f43f72a!8m2!3d35.7100627!4d139.8107004!15sChbrj4Tsv4Qg7Iqk7Lm07J207Yq466asWhkiF-uPhOy_hCDsiqTsubTsnbQg7Yq466askgEQb2JzZXJ2YXRpb25fZGVja-ABAA!16zL20vMDd0aGty?hl=ko',
'https://www.google.co.kr/maps/place/%EB%8F%84%EC%BF%84+%EB%94%94%EC%A6%88%EB%8B%88%EB%9E%9C%EB%93%9C/@35.6329007,139.8782003,17z/data=!3m1!4b1!4m6!3m5!1s0x60187d03114737b3:0xe4d93636d509d3cb!8m2!3d35.6328964!4d139.8803943!16zL20vMDQ0ejFu?hl=ko',
'https://www.google.co.kr/maps/place/%EC%84%BC%EC%86%8C%EC%A7%80/@35.7147694,139.7944613,17z/data=!3m1!4b1!4m6!3m5!1s0x60188ec1a4463df1:0x6c0d289a8292810d!8m2!3d35.7147651!4d139.7966553!16zL20vMDNrOTg3?hl=ko']

for url in urls:
    driver.get(url)
    driver.implicitly_wait(100)

    #이름
    print(driver.find_element(By.CLASS_NAME,"DUwDvf.fontHeadlineLarge").text)
    list_names.append(driver.find_element(By.CLASS_NAME,"DUwDvf.fontHeadlineLarge").text)
    #별점
    print(driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]').text)
    list_grade.append(driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]').text)
    ####### 영업시간 명소이름 명소평점 말고 모두 갖고오기
    current_list_alls = driver.find_elements(By.CLASS_NAME, "Io6YTe.fontBodyMedium")
    #운영시간
    ###### 운행시간없는 장소의 예외 처리!!
    print('89start')
    element_schedule = driver.find_elements(By.CLASS_NAME, "MkV9")
    print('where?')
    element_schedule_insane = driver.find_elements(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(15) > div.RcCsl.fVHpi.w4vB1d.NOE9ve.AG25L.lk2Rcf > button > div.AeaXub")
    print('89end')
    if len(element_schedule) == 0 and len(element_schedule_insane) == 0:
        try:
            list_Address_eng.append(current_list_alls[0].text)
        except:
            list_Address_eng.append("없음")
        try:
            list_Address_not_eng.append(current_list_alls[1].text)
        except:
            list_Address_not_eng.append("없음")
        try:
            list_Address_Internet.append(current_list_alls[2].text)
        except:
            list_Address_Internet.append("없음")
        try:
            list_Phone_Number.append(current_list_alls[3].text)
        except:
            list_Phone_Number.append("없음")
        try:
            list_bonus_1.append(current_list_alls[4].text)
        except:
            list_bonus_1.append("없음")
        try:
            list_bonus_2.append(current_list_alls[4].text)
        except:
            list_bonus_2.append("없음")
        try:
            list_bonus_3.append(current_list_alls[4].text)
        except:
            list_bonus_3.append("없음")
        list_running_Mon.append("운행정보 없음")
        list_running_Tue.append("운행정보 없음")
        list_running_Wed.append("운행정보 없음")
        list_running_Thur.append("운행정보 없음")
        list_running_Fri.append("운행정보 없음")
        list_running_Sat.append("운행정보 없음")
        list_running_Sun.append("운행정보 없음")
    ###### 운행시간 갖고오기(클릭해서 간단하게 나오는곳)
    if len(element_schedule) != 0:
        print('131')
        element_schedule[0].click()
        # for e_s in element_schedule:
        #     print('wtf')
        #     driver.implicitly_wait(100)
        #     e_s.click()
        #     driver.implicitly_wait(100)
        print('131 end')
        driver.implicitly_wait(10)
        try:
            list_Address_eng.append(current_list_alls[0].text)
        except:
            list_Address_eng.append("없음")
        try:
            list_Address_not_eng.append(current_list_alls[1].text)
        except:
            list_Address_not_eng.append("없음")
        try:
            list_Address_Internet.append(current_list_alls[2].text)
        except:
            list_Address_Internet.append("없음")
        try:
            list_Phone_Number.append(current_list_alls[3].text)
        except:
            list_Phone_Number.append("없음")
        try:
            list_bonus_1.append(current_list_alls[4].text)
        except:
            list_bonus_1.append("없음")
        try:
            list_bonus_2.append(current_list_alls[4].text)
        except:
            list_bonus_2.append("없음")
        try:
            list_bonus_3.append(current_list_alls[4].text)
        except:
            list_bonus_3.append("없음")
        current_list_running_times = driver.find_elements(By.CLASS_NAME, "G8aQO")
        list_running_Mon.append(current_list_running_times[6].text)
        list_running_Tue.append(current_list_running_times[0].text)
        list_running_Wed.append(current_list_running_times[1].text)
        list_running_Thur.append(current_list_running_times[2].text)
        list_running_Fri.append(current_list_running_times[3].text)
        list_running_Sat.append(current_list_running_times[4].text)
        list_running_Sun.append(current_list_running_times[5].text)
        # for list_running_time in current_list_running_times:
        #     list_running_times.append(list_running_time.text)


    ###### 운행시간 갖고오기(클릭해서 길게 나오는곳)
    if len(element_schedule_insane) != 0:
        print('181')
        for e_s in element_schedule_insane:
            print('181 wtf')
            driver.implicitly_wait(100)
            e_s.click()
            driver.implicitly_wait(100)
        print('181 end')
        driver.implicitly_wait(10)
        try:
            list_Address_eng.append(current_list_alls[0].text)
        except:
            list_Address_eng.append("없음")
        try:
            list_Address_not_eng.append(current_list_alls[1].text)
        except:
            list_Address_not_eng.append("없음")
        try:
            list_Address_Internet.append(current_list_alls[3].text)
        except:
            list_Address_Internet.append("없음")
        try:
            list_Phone_Number.append(current_list_alls[4].text)
        except:
            list_Phone_Number.append("없음")
        try:
            list_bonus_1.append(current_list_alls[4].text)
        except:
            list_bonus_1.append("없음")
        try:
            list_bonus_2.append(current_list_alls[4].text)
        except:
            list_bonus_2.append("없음")
        try:
            list_bonus_3.append(current_list_alls[4].text)
        except:
            list_bonus_3.append("없음")
        current_list_running_times = driver.find_elements(By.CLASS_NAME, "G8aQO")
        time.sleep(1)
        list_running_Mon.append(current_list_running_times[6].text)
        list_running_Tue.append(current_list_running_times[0].text)
        list_running_Wed.append(current_list_running_times[1].text)
        list_running_Thur.append(current_list_running_times[2].text)
        list_running_Fri.append(current_list_running_times[3].text)
        list_running_Sat.append(current_list_running_times[4].text)
        list_running_Sun.append(current_list_running_times[5].text)
        time.sleep(3)

total = pd.concat([pd.DataFrame(list_names),pd.DataFrame(list_Address_eng),pd.DataFrame(list_Address_not_eng),pd.DataFrame(list_Address_Internet),pd.DataFrame(list_Phone_Number),pd.DataFrame(list_grade),pd.DataFrame(list_bonus_1),pd.DataFrame(list_bonus_2),pd.DataFrame(list_bonus_3),pd.DataFrame(list_running_Sun),pd.DataFrame(list_running_Mon),pd.DataFrame(list_running_Tue),pd.DataFrame(list_running_Wed),pd.DataFrame(list_running_Thur),pd.DataFrame(list_running_Fri),pd.DataFrame(list_running_Sat)],axis = 1)
total.columns = ['Name', 'Address', 'Local_Address', 'Internet_Address', 'Call_Number', 'Rating', 'Bonus1', 'Bonus2', 'Bonus3', 'Sun', 'Mon', 'Tues', 'Wedn', 'Thur', 'Fri', 'Sat']
total.to_csv("Total_info_dokyo.csv",index=False)
driver.quit()