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
        try:
            to_scroll=driver.find_element(By.XPATH,'/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]')
        except:
            continue

    #review 총 몇개 크롤링할지
    review_total=1000

    #리뷰 데이터 쓴 사람 아이디
    result_list_name = []
    #리뷰 데이터 쓴사람의 별점
    result_list_user_grade = []

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

    #닉네임갖고오기
    to_adds_names=driver.find_elements(By.CLASS_NAME,'d4r55')
    #유저별점갖고오기
    to_user_grade=driver.find_elements(By.CLASS_NAME,'hCCjke.vzX5Ic')

    for add_name in to_adds_names:
        result_list_name.append(add_name.text)

    filled_star_url = "//maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_14.png"
    #유저별점갖고오기

    aaa = driver.find_elements(By.CLASS_NAME, 'kvMYJc')
    for add_grade in aaa:
        soup = BeautifulSoup(add_grade.get_attribute('innerHTML'), 'html.parser')
        filled_star_count = len(soup.find_all('img', {'src': filled_star_url}))
        result_list_user_grade.append(filled_star_count)

    # csv로 저장
    df1 = pd.DataFrame(result_list_name)
    df2 = pd.DataFrame(result_list_user_grade)
    df1.to_csv(names[i]+"_ID.csv",index=False)
    df2.to_csv(names[i]+"_user_grade",index=False)
    print(names[i])
