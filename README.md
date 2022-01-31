# WebScraping
간단한 web scraping 프로그램

* chrome version : 버전 97.0.4692.99(공식 빌드) (64비트)
* chrome driver version : 버전 97.0.4692

* step 1. cmd에서 chrome.exe 위치로 이동한 뒤 다음 명령어 실행
mkdir folderUser
chrome.exe --explicitly-allowed-ports=9222 -remote-debugging-port=9222 -user-data-dir='folderUser'
pip install webdriver-manager

* step 2. auto_scraping_version2.py 실행