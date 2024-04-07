from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from icecream import ic
from time import sleep

opts = Options()
#opts.set_headless()
#assert opts.headless  # Operating in headless mode
#https://selenium-python.readthedocs.io/waits.html
browser = Firefox(options=opts)
browser.get('https://discord.gg/7WsZTtcd')


button = browser.find_elements(By.XPATH, '//button') 
ic(button)

button[-1].click() 

try:
    element = WebDriverWait(browser, 100).until(
        EC.title_contains("Test server")
    )
finally:
    print("yaay")


