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


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver.get('https://www.bybit.com/trade/usdt/BTCUSDT')

# 값 찾기
price = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[2]/table/tr[1]/td[2]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div/div')
print(price.text)

while True:
    print(price.text, time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))
    
# indicator / ma 보면 된다 ^_^

