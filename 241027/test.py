from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import logging

logging.disable(logging.CRITICAL)
opt = Options()
opt.add_argument("--headless")
opt.add_argument("--disable-gpu")
opt.add_argument("log-leve1=3")
opt.add_argument("disable-blink-features=AutomationControlled")
myChrome = Chrome(options=opt)
myChrome.close()