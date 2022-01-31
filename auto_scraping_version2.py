#Code Description

import scrapy
import time
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

variable = driver.current_url
print(variable)

# 값 찾기
driver.switch_to.frame('tradingview_e4436')
wait =  WebDriverWait(driver, 10)

price = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div/div')
print(price.text) 

while True:
    print(price.text, time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
    
