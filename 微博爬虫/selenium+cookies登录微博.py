from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time,json

opt = Options()
opt.add_argument("log-leve1=3")
opt.add_argument("disable-blink-features=AutomationControlled")
opt.add_experimental_option('excludeSwitches', ['enable-automation'])
# opt.add_argument(r'user-data-dir=C:\Users\username\AppData\Local\Google\Chrome\User Data1')
# 给浏览器实例添加userdata（复制一份userdata用，不要共用）
# 用了cookies就不用这个了
web = Chrome(options=opt)


f=open("weibocookies.json", "r")
cookies=json.load(f)
f.close()

web.get("https://s.weibo.com/weibo?q=%23%E6%9D%A8%E5%88%A9%E4%BC%9F%E7%9A%84%E5%A4%AA%E7%A9%BA%E4%B8%80%E6%97%A5%23&nodup=1")
web.delete_all_cookies()
for cookie in cookies:
    web.add_cookie(cookie)
web.refresh()
web.get("https://s.weibo.com/weibo?q=%23%E6%9D%A8%E5%88%A9%E4%BC%9F%E7%9A%84%E5%A4%AA%E7%A9%BA%E4%B8%80%E6%97%A5%23&nodup=1")

# # 找到某个元素. 点击它
# from selenium.webdriver.common.action_chains import ActionChains
# span1 = web.find_element(By.XPATH,'/html/body/div/div/div/div[2]/div[2]/ul/li[2]/a/span[2]')
# actions = ActionChains(web)
# actions.click(span1).perform()

# 拖动滚动条至底部
web.execute_script('window.scrollTo(0,document.body.scrollHeight)')

web.get("https://s.weibo.com/weibo?q=%23%E6%9D%A8%E5%88%A9%E4%BC%9F%E7%9A%84%E5%A4%AA%E7%A9%BA%E4%B8%80%E6%97%A5%23&nodup=1&page=8")
web.delete_all_cookies()
for cookie in cookies:
    web.add_cookie(cookie)
web.refresh()
web.get("https://s.weibo.com/weibo?q=%23%E6%9D%A8%E5%88%A9%E4%BC%9F%E7%9A%84%E5%A4%AA%E7%A9%BA%E4%B8%80%E6%97%A5%23&nodup=1&page=8")

# # 拖动滚动条到指定位置
# driver.execute_script('document.documentElement.scrollTop=6000')
# # 利用js来滚动对应数值的距离
# driver.execute_script('window.scrollTo(0,1000)')
# element = driver.find_element(By.ID, "element_id")
# driver.execute_script("arguments.click();", element)

input("quit:")