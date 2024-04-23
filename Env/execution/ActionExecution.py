from decision.SingletonMeta import SelectorsStorage
from action import Action, ActionType
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import os
import re
from selenium.webdriver.common.by import By
# 此处os.path.dirname()可以获得上一级目录，也就是当前文件或文件夹的父目录
# 将目录加入到sys.path即可生效，可以帮助python定位到文件（注：这种方法仅在运行时生效，不会对环境造成污染）
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def execute_action(driver, action: Action, map=True):
    selectorsStorage = SelectorsStorage()
    if action.action_type == ActionType.CLICK:
        if map:
            element = driver.find_element(
                By.CSS_SELECTOR, selectorsStorage.selector_list_btn[int(re.findall(r'\d+', action.kwargs['id'])[0])])
            element.click()
        else:
            element = driver.find_element(
                By.CSS_SELECTOR, action.kwargs['id'])
            element.click()
    elif action.action_type == ActionType.TYPE:
        element = driver.find_element(
            By.CSS_SELECTOR, selectorsStorage.selector_list_text[int(re.findall(r'\d+', action.kwargs['id'])[0])])
        element.send_keys(action.kwargs['content'])
        if action.kwargs['press_enter_after']:
            element.send_keys(Keys.ENTER)
    elif action.action_type == ActionType.SELECT:
        # 假设select是通过点击下拉菜单中的选项来实现的
        option = driver.find_element(
            By.CSS_SELECTOR, action.kwargs['id'])
        option.click()
    elif action.action_type == ActionType.NEW_TAB:
        driver.execute_script(
            "window.open('about:blank', 'new_tab');")
        driver.switch_to.window(
            driver.window_handles[-1])
        for i in action.kwargs.get("url", []):
            driver.get(action.kwargs['url'])
            driver.switch_to.window(
                driver.window_handles[-1])
    elif action.action_type == ActionType.TAB_FOCUS:
        driver.switch_to.window(
            driver.window_handles[int(action.kwargs['tab_index'])])
    elif action.action_type == ActionType.CLOSE_TAB:
        driver.close()
    elif action.action_type == ActionType.GOTO:
        driver.get(action.kwargs['url'])
        driver.switch_to.window(
            driver.window_handles[-1])

    elif action.action_type == ActionType.GO_BACK:
        driver.back()
    elif action.action_type == ActionType.GO_FORWARD:
        driver.forward()
    elif action.action_type == ActionType.STOP:
        # 这里假设stop操作是用来打印信息的
        print(
            f"Action stopped with answer: {action.kwargs.get('answer', 'N/A')}")
        driver.quit()
