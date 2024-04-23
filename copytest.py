from decision.OutputParser import ActionOutputParser
from Env.Env import Env
import asyncio
from decision.SingletonMeta import *
output_parser = ActionOutputParser()
env = Env("https://ehall.fudan.edu.cn/ywtb-portal/fudan/index.html#/work?role=1__0&type=2")
env.perceive()
observation = Observation()
selectors_storage = SelectorsStorage()
print(observation.current_web_html)
llm_output_click = "In summary, the next action I will perform is ```click [click#137]```."
env.execute_action(output_parser.process(llm_output_click))
env.perceive()
print("before:")
with open("before.html", "w") as f:
    f.write(observation.current_web_html)
env2=env.clone()
env2.perceive()
print("after:")
with open("after.html", "w") as f:
    f.write(observation.current_web_html)
