from selenium import webdriver
import time, json

wb = webdriver.Chrome()
wb.implicitly_wait(3)
wb.get('https://weibo.com')

time.sleep(60)  # 这期间手动执行登录操作

cookies = wb.get_cookies()  # 拉下来登录获得的cookies
with open('weibocookies.json', 'w') as f:
    json.dump(cookies, f)

wb.close()
