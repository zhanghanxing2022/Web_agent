from decision.SingletonMeta import SelectorsStorage, Observation
from Env.perception.processer import *
import re
import sys
import os
import json
# 此处os.path.dirname()可以获得上一级目录，也就是当前文件或文件夹的父目录
# 将目录加入到sys.path即可生效，可以帮助python定位到文件（注：这种方法仅在运行时生效，不会对环境造成污染）
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def perceive(driver):

    # 执行select.js脚本
    with open('Env/perception/script/select.js', 'r') as file:
        select_script = file.read()

    # 执行input.js脚本并获取selector_list_btn
    with open('Env/perception/script/input.js', 'r') as file:
        input_script = select_script+file.read()
    selector_list_text = driver.execute_script(input_script)

    # 执行option.js脚本并获取selector_list_text
    with open('Env/perception/script/option.js', 'r') as file:
        option_script = select_script+file.read()
    selector_list_select = driver.execute_script(option_script)

    # 执行pointer.js脚本并获取selector_list_select
    with open('Env/perception/script/pointer.js', 'r') as file:
        pointer_script = select_script+file.read()
    selector_list_btn = driver.execute_script(pointer_script)

    # 将获取到的选择器列表保存在SelectorsStorage单例中
    selectors_storage = SelectorsStorage()
    selectors_storage.update_selectors(
        selector_list_btn, selector_list_text, selector_list_select)

    with open("Env/perception/config/reserve.json") as f:
        config = json.loads(f.read())

    # 获取Observation实例并更新信息
    observation = Observation()
    observation.update(
        current_web_source=driver.page_source,
        current_web_html=process_html(config, driver.page_source),
        current_web_url=driver.current_url,
        current_web_title=driver.title,
        # 其他需要更新的信息...
    )
    current_tab_handle = driver.current_window_handle

    # 存储所有标签页的标题和URL
    tabs_info = []

    # 获取所有打开的标签页的句柄
    for handle in driver.window_handles:
        # 切换到每个标签页
        driver.switch_to.window(handle)
        # 获取当前标签页的标题和URL
        title = driver.title
        url = driver.current_url
        # 将标题和URL添加到列表中
        tabs_info.append((title, url))

    observation.open_tabs = tabs_info

    # 切换回最初的标签页
    driver.switch_to.window(current_tab_handle)

    # 返回选择器存储和观察实例
    return selectors_storage, observation
