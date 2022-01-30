# -*- coding: utf-8 -*-
'''
1. 로그인
2. BTCUSDT
3. INDICATOR 실시간으로 받아오기
4. 시각화/DataFrame으로 저장도 해주면 좋을 듯함

* 각 단계에서 assert 진행하기

'''

import json
import os
import re
import pickle
import time
import datetime
from queue import Full
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sys import platform
from tqdm import tqdm
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_opt = webdriver.ChromeOptions()

prefs = {"profile.managed_default_content_settings.images": 2}  # to unable image
chrome_opt.add_experimental_option("prefs", prefs)


print('Current OS : ', platform)
if 'darwin' in platform:
    selen_path = '/chromedriver/chromedriver.exe'
    chrome_opt.add_argument('--kiosk')

elif 'win32' in platform:
    selen_path = os.path.join(os.getcwd(), 'chromedriver', 'chromedriver.exe') 
    chrome_opt.add_argument('--start-maximized')
    chrome_opt.add_experimental_option('excludeSwitches', ['enable-logging'])


# main crawler 
def crawler_D1():
    # firefox
    Result = {}

    # 로그인
    global driver
    driver.get('https://www.bybit.com/en-US/login')
    time.sleep(1)
        
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/main/div/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/input')))

    ID = driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/input')
    ID.send_keys('enkeejuniour@naver.com') # 아이디 입력하기
    PW = driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[2]/input')
    PW.send_keys('Qkrdydwn1*') # 비밀번호 입력하기
    driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/div/div/div/div[1]/div[2]/div/div[2]/div').send_keys(Keys.ENTER)

    # 게시판 접근
    log_page = 'https://www.bybit.com/trade/usdt/BTCUSDT'
    driver.get(log_page)
    
    # 이미지를 허용해두어야 함
    # 굴뚝 허용하기 문제를 해결해야 함 - 이때는 그냥 다시 시도하는 편이 나음. 
    Table_box_ = driver.find_element_by_css_selector(
            '#posts-filter > table')
    Table_box = Table_box_.find_element_by_id('the-list')

    try:  # 맨 마지막 페이지 핸들링용
        for idx in range(1, 21):  # 테이블 긁어오기
            href = Table_box.find_element_by_xpath(
                f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{idx}]/td[1]/strong/a')
            link = href.get_attribute('href')
            actor = Table_box.find_element_by_xpath(
                f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{idx}]/td[2]/a').text

            date = Table_box.find_element_by_xpath(
                f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{idx}]/td[3]').text
            # 맨 앞은 2022/, 쉼표 뒤는 시간이므로
            date_cleaned = date[9: date.find(',')]
            date_cleaned = re.sub('/', '', date_cleaned)

            # print(date_cleaned)

            if (date_cleaned in DATE_range) and (actor in SEED_ls):  # 스누씨드가 아닌 경우에 굳이 긁을 필요 없음
                Result['href_ls'].append(link)
                Result['Actor_name'].append(actor)
                Result['Date'].append(date)
    except NoSuchElementException:
            print(f'Crawling End in page..{page_num}')
            break  # 가장 마지막 페이지일 것이므로
        # Next_page = driver.find_element_by_class_name('pagination_links')
        # Next_page.click()
    Next_page = log_page + r'&' + f'paged={page_num}'
    driver.get(Next_page)

    # 엑셀에 저장한다. 
    save_folder = 'SNURO_Homepage'
    Full_path = os.path.join(os.getcwd(), save_folder, result_name)
    df = pd.DataFrame.from_dict(Result)
    assert df.shape[0] > 1
    df.to_excel(Full_path)

    return Result  # dictionary"""


def crawler_D2(dframe,  # 매칭정보
               output1,  # D1 크롤링 결과 엑셀
               result_name,  # 저장 파일 명
               ):
    # 내용 시각화하기
    global driver
    Result = {'href_ls': output1['href_ls'].values,
              'Actor_name': output1['Actor_name'].values
              }

    json_ls = []
    slug_ls = []
    for link in tqdm(Result['href_ls'], desc='>>>> Crawling'):
        driver.get(link)
        Log_box = driver.find_element_by_id('snuro_logs_box')
        slug_data = Log_box.find_element_by_css_selector(
            'div.inside > input[type=text]')
        slug_data = slug_data.get_attribute('value')
        assert slug_data != 'None', print(slug_data)
        json_data = driver.find_element_by_css_selector('#xApi').text
        json_ls.append(json_data)
        slug_ls.append(slug_data)

    Result['json'] = json_ls
    Result['slug'] = slug_ls

    save_folder = 'SNURO_Homepage'
    Full_path = os.path.join(os.getcwd(), save_folder, result_name)
    with open(Full_path, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(Result,
                    outp, pickle.HIGHEST_PROTOCOL)

    return Result  # dictionary


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=selen_path,
                              chrome_options=chrome_opt)
    RS1 = crawler_D1()
    print('>>>>> Crawling RS: ', len(RS1['href_ls']))

    RS2 = crawler_D2(dframe=df,
                     output1=pd.read_excel(os.path.join(
                         os.getcwd(), 'SNURO_Homepage', '스누로_크롤링 D1.xlsx')),
                     result_name='220130_week3_xAPI.pkl')
    print('>>>>> Crawling RS2: ', len(RS2['href_ls']))

    # print(date_list)
