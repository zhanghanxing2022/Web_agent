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
    def __init__(self, url, headless=False):
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


    def execute_action(self, action, map=True):
        print(action)
        execute_action(self.driver, action, map)
        time.sleep(1)

    def copy_browser_state(self, new_driver):
        # 打开原来的页面URL保持同步
        new_driver.get(self.driver.current_url)

        # 复制所有Cookies
        for cookie in self.driver.get_cookies():
            new_driver.add_cookie(cookie)

        # 这里需要重新加载页面，以确保Cookies完全生效
        new_driver.get(self.driver.current_url)
        source_code = self.driver.page_source
        script = "arguments[0].innerHTML = arguments[1];"
        html_element = new_driver.find_element(By.CSS_SELECTOR, 'html')
        new_driver.execute_script(script, html_element, source_code)

    def clone(self, headless=False):
        # 提供一个方法用于「复制」Env的实例
        # 注意：这并非复制driver的状态，而是根据原始实例的url和headless状态创建一个新的实例
        new_instance = Env(self.driver.current_url, headless)
        self.copy_browser_state(new_instance.driver)
        return new_instance

    def close(self):
        # 关闭Selenium
        self.driver.quit()


def initialize_and_click(action):
    """
    初始化子进程的Env对象和执行操作。
    在这个例子中，'action'可以是一个选择器或一个动作说明，依据你的execute_action函数定义。
    """
    # 假设这里我们正在使用特定的URL和headless模式初始化
    url = "https://example.com"
    env_instance = Env(url, headless=True)
    env_instance.execute_action(action)
    env_instance.close()
