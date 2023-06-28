from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

# 웹 드라이버 실행
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome('chromedriver', options=chrome_options)

# 첫번째 페이지부터 31번째 페이지까지 순회
for page in range(10):
    # 리뷰 페이지 접근
    url = f"https://www.tripadvisor.co.kr/Attraction_Review-g14134278-d479268-Reviews-or{page * 10}-National_Museum_of_Western_Art-Uenokoen_Taito_Tokyo_Tokyo_Prefecture_Kanto.html"
    driver.get(url)
    time.sleep(2)

    # 클래스 이름이 'yCeTE'인 모든 요소 찾기
    elements = driver.find_elements(By.CLASS_NAME, 'yCeTE')

    directory = '국립 서양 미술관'
    # directory = f'reviews_03_21/page{page}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 각 요소의 텍스트를 파일로 저장
    for idx, elem in enumerate(elements):
        with open(os.path.join(directory, f'{page*20 + idx + 1}.txt'), 'w', encoding='utf-8') as f:
            f.write(elem.text)

# 웹 드라이버 종료
driver.quit()



###########################10개#####################