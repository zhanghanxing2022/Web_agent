import threading
import json
from decision.SingletonMeta import *
from selenium.webdriver.common.by import By
from Env.Env import Env
from decision.OutputParser import ActionOutputParser

from decision.Model import Modal


def thread_worker(serialized_state, env: Env, css_selctor, task, fn):
    # 反序列化状态
    deserialize_state(
        *serialized_state)
    actionOutputParser = ActionOutputParser()
    action = actionOutputParser.process(f"click [{css_selctor}]")
    env.execute_action(action, False)
    llm = Modal()
    answer = fn(llm, env, task)
    return answer


if __name__ == '__main__':
    # 启动主浏览器并获取状态
    env = Env("https://blog.csdn.net/m0_49349071/article/details/133642269")
    env.perceive()

    # 序列化状态
    serialized_state = serialize_state(
        Observation(), Memory(), SelectorsStorage())

    # 假设你已经有了一个 filled final_results
    final_results = [...]  # 这里应该是填充了实际任务的数组

    # 创建线程池
    threads = []

    def fn():
        return ""
    for css_selector, task in final_results:

        t = threading.Thread(target=thread_worker, args=(
            serialized_state, env.clone(), css_selector, task, fn))
        t.start()
        threads.append(t)

    # 等待所有线程完成
    for t in threads:
        t.join()

    # 清理主 Env
    env.close()
