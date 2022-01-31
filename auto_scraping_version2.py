#Code Description

import scrapy
import time
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = os.path.join(os.getcwd(), 'chromedriver', 'chromedriver.exe') 
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

# 값 찾기
price = driver.find_element_by_xpath('//*[@id="root"]/main/div[1]/aside/div[1]/div[1]/div/span')

while True:
    print(price.text, time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
    
# indicator / ma 보면 된다 ^_^