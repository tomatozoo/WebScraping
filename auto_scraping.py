# -*- coding: utf-8 -*-
'''
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
    # 아이디 입력 #
    ID.send_keys('') # 아이디 입력하기
    PW = driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[2]/input')
    # 패스워드 입력 #
    PW.send_keys('') # 비밀번호 입력하기
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/main/div/div/div/div/div[1]/div[2]/div/div[2]/div/a')))

    driver.find_element_by_xpath('//*[@id="__layout"]/div/main/div/div/div/div/div[1]/div[2]/div/div[2]/div/a').click()


    
    # 이미지를 허용해두어야 함
    try:
        # 게시판 접근
        log_page = 'https://www.bybit.com/trade/usdt/BTCUSDT' #https://www.bybit.com/trade/usdt/BTCUSDT
        driver.get(log_page)
        
        # 값 찾기
        price = driver.find_element_by_xpath('//*[@id="root"]/main/div[1]/aside/div[1]/div[1]/div/span')

        while True:
            print(price.text, time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
    except:
        print('보안 강화 : ex - 그림 찾기 등')


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
    
    
    # print(date_list)
