from decision.OutputParser import ActionOutputParser
from Env.Env import Env
import asyncio
from decision.SingletonMeta import *
env = Env("https://ehall.fudan.edu.cn/ywtb-portal/fudan/index.html#/hall")
env.perceive()
observation = Observation()
selectors_storage = SelectorsStorage()
print(selectors_storage)

output_parser = ActionOutputParser()
action0 = output_parser.process("```click [click#4]```")
env.execute_action(action0)
env.perceive()
print(selectors_storage)

action1 = output_parser.process("```type [input#0] [20302010045] [0]```")
env.execute_action(action1)
env.perceive()
llm_output_click = "In summary, the next action I will perform is ```click [click#4]```."
llm_output_new_tab = "In summary, the next action I will perform is ```new_tab```."
llm_output_tab_focus = "In summary, the next action I will perform is ```tab_focus [1]```."
llm_output_close_tab = "In summary, the next action I will perform is ```close_tab```."
llm_output_goto = "In summary, the next action I will perform is ```goto [https://hf-mirror.com/]```."
llm_output_go_back = "In summary, the next action I will perform is ```go_back```."
llm_output_go_forward = "In summary, the next action I will perform is ```go_forward```."
llm_output_stop_with_answer = "In summary, the next action I will perform is ```stop [answer]```."
llm_output_stop_no_answer = "In summary, the next action I will perform is ```stop [N/A]```."
env.execute_action(output_parser.process(llm_output_new_tab))
env.perceive()

env.execute_action(output_parser.process(llm_output_new_tab))
env.perceive()

env.execute_action(output_parser.process(llm_output_tab_focus))
env.perceive()

env.execute_action(output_parser.process(llm_output_goto))
env.perceive()

env.execute_action(output_parser.process(llm_output_click))
env.perceive()

env.execute_action(output_parser.process(llm_output_go_back))
env.perceive()

env.execute_action(output_parser.process(llm_output_go_forward))
env.perceive()

env.execute_action(output_parser.process(llm_output_new_tab))
env.perceive()
env.execute_action(output_parser.process(llm_output_tab_focus))
env.perceive()


env.execute_action(output_parser.process(llm_output_stop_with_answer))
env.perceive()

