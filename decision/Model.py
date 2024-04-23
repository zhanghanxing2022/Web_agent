from decision.Prompt import *
from decision.SingletonMeta import Observation, SingletonMeta
from decision.OutputParser import *
from openai import OpenAI
import datetime
MESSAGE_FILE = 'message.txt'


class Modal(metaclass=SingletonMeta):
    def __init__(self, model='/data2/huangwenhao/hf_model/Mistral-7B-Instruct-v0.2', port=8091):
        # 确保初始化只进行一次
        if not hasattr(self, 'initialized'):
            self.initialized = True
            openai_api_key = "EMPTY"
            openai_api_base = f"http://10.176.40.140:{port}/v1"
            self.model = model

            # 假设这里的 OpenAI 是已经被定义好的客户端类
            self.client = OpenAI(
                api_key=openai_api_key,
                base_url=openai_api_base,
            )

    def call_with_messages(self, query):
        # mess = [{"role": "user", "content": " "}]
        # mess[0]['content'] = query[0]['content']+query[1]['content']
        chat_response = self.client.chat.completions.create(
            model=self.model,
            messages=query,

            temperature=0.5,
        )
        current_time = datetime.datetime.now()
        with open(MESSAGE_FILE, 'a+') as f:
            f.write(str(current_time)+'\t' + str(chat_response.usage)+'\n')
        return chat_response.choices[0].message


class SearchLLM:
    def __init__(self, llm: Modal) -> None:
        self.llm = llm
        self.parser = OutputParser()
        self.message = Message()
        pass

    def call(self):
        # Logic to summarize the page and extract necessary information

        observation = Observation()
        self.message.set_sys(description_block)
        self.message.set_usr(
            f"Observation:\n"
            f" Task: {observation.task}\n"
            f" Current Web URL: {observation.current_web_url}\n"
            f" Current Web HTML:{observation.current_web_html}\n"
            f" Current Web TITLE:{observation.current_web_title}\n"
        )
        res = self.llm.call_with_messages(self.message)
        return self.parser.process(res)


# Define a PlanAgent class that creates a plan based on the page summary


class PlanLLM:
    def __init__(self, llm: Modal) -> None:
        self.llm = llm
        self.parser = PlanOperationProcessor()
        self.message = Message()
        pass

    def call(self):
        observation = Observation()

        self.message.set_sys(plan_sys)
        self.message.set_usr(
            f"Observation:\n"
            f" Task: {observation.task}\n"
            f" Current Web URL: {observation.current_web_url}\n"
            f" Current Web HTML:{observation.current_web_html}\n"
            f" Current Web TITLE:{observation.current_web_title}\n"
            f" Current Open Tabs:{observation.open_tabs}\n"
            f" Current Web Operation History:{observation.current_web_action_history}\n"
            f" Last Web Title:{observation.previous_web_title}\n"
            f" Last Web Description:{observation.previous_web_description}\n"
            + Memory()
        )
        # Logic to create a plan based on the input summary
        res = self.llm.call_with_messages(self.message)
        return self.parser.process(res)

# Define an ActionAgent class that generates actions from the plan


class ActionLLM:
    def __init__(self, llm: Modal) -> None:
        self.llm = llm
        self.parser = ActionOutputParser()
        self.message = Message()
        pass

    def call(self):
        # Logic to generate next action from the plan
        observation = Observation()

        self.message.set_sys(action_sys)
        self.message.set_usr(
            f"Observation:\n"
            f" Task: {observation.task}\n"
            f" Current Web URL: {observation.current_web_url}\n"
            f" Current Web HTML:{observation.current_web_html}\n"
            f" Current Web TITLE:{observation.current_web_title}\n"
            f" Current Open Tabs:{observation.open_tabs}\n"
            f" Current Web Operation History:{observation.current_web_action_history}\n"
            f" Last Web Title:{observation.previous_web_title}\n"
            f" Last Web Description:{observation.previous_web_description}\n"
            + Memory()
        )
        # Logic to create a plan based on the input summary
        res = self.llm.call_with_messages(self.message)
        return self.parser.process(res)

# Main run function that uses the agents to execute a task


class TaskLLM():
    def __init__(self, llm: Modal) -> None:
        self.llm = llm
        self.parser = OutputParser()
        self.message = Message()
        pass

    def _set_sub_task(self, task):
        self.sub_task = task

    def call(self):
        # Logic to summarize the page and extract necessary information

        observation = Observation()
        self.message.set_sys(description_block)
        self.message.set_usr(
            f"Observation:\n"
            f" Task: {observation.task}\n"
            f" Current Web URL: {observation.current_web_url}\n"
            f" Current Web HTML:{observation.current_web_html}\n"
            f" Current Web TITLE:{observation.current_web_title}\n"
            f" The sub-task and result:{self.sub_task}"
            + Memory()
        )
        res = self.llm.call_with_messages(self.message)
        return self.parser.process(res)


class SelectLLM:
    def __init__(self, llm: Modal) -> None:
        self.llm = llm
        self.parser = SelectParser()
        self.message = Message()
        pass

    def _set_selector(self, selector):
        self.selector = selector

    def _set_elem(self, elems):
        self.elems = elems

    def call(self):
        observation = Observation()

        self.message.set_sys(action_sys)
        self.message.set_usr(
            f"Observation:\n"
            f" Task: {observation.task}\n"
            f" Current Web URL: {observation.current_web_url}\n"
            f" Current Web HTML:{observation.current_web_html}\n"
            f" Current Web TITLE:{observation.current_web_title}\n"
            f" Current Web Operation History:{observation.current_web_action_history}\n"
            f" Recommended clickable elements:{self.elems}\n"
            + Memory()
        )
        res = self.llm.call_with_messages(self.message)
        output = self.parser.process(res)

        return [(self.selector[i], task) for (i, task) in output]
