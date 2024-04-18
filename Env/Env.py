from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from Env.perception.Perception import perceive
from execution.ActionExecution import execute_action
import time
class Env:
    def __init__(self,url,headless=False):
        # 启动Selenium
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(20)
        self.driver.implicitly_wait(10) 
        self.driver.get(url)

    def perceive(self):
        perceive(self.driver)

    def execute_action(self, action):
        print(action)
        execute_action(self.driver, action)
        time.sleep(1)
        

    def close(self):
        # 关闭Selenium
        self.driver.quit()