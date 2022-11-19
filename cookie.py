import time,json
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('http://www.luogu.com.cn/auth/login')
time.sleep(20)
cookies = driver.get_cookies()
with open('.\\data\\cookies.json', 'w') as f:
    f.write(json.dumps(cookies))
driver.quit()
