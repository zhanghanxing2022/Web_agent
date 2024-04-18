from Env.Env import Env
from decision.OutputParser import *
from action import Action, ActionType
from decision.SingletonMeta import Observation
from decision.prompt import *
from decision.llm import Modal
# Define a SearchAgent class that summarizes current page and related information


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

    def call(self, summary):
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

    def call(self, plan):
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


class SelectLLM:
    def __init__(self, llm: Modal) -> None:
        self.llm = llm
        self.parser = ActionOutputParser()
        self.message = Message()
        pass

    def call(self, plan):
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


def run(llm_model_path, llm_port, url, task):
    # Initialize environment
    env = Env(url, headless=True)
    try:
        # Perceive the initial state of the page
        env.perceive()
        # Method to retrieve observation from the environment
        observation = env.get_observation()

        # Use SearchAgent to get page summary and related info
        search_agent = SearchLLM()
        summary = search_agent.summarize(observation.current_web_html)

        # Use PlanAgent to draft a plan
        plan_agent = PlanLLM()
        plan = plan_agent.create_plan(summary)

        action = None
        action_agent = ActionLLM()
        output_parser = ActionOutputParser()

        # Execute plan step-by-step
        while True:
            # Use ActionAgent to decide on an action
            if action is None:
                action_str = action_agent.generate_action(plan)
                action = output_parser.process(action_str)
            if action.action_type == ActionType.STOP:
                print("Task completed with answer:",
                      action.kwargs.get('answer', 'N/A'))
                break

            # Perform action using the environment
            env.execute_action(action)

            # Update the observation after executing the action
            env.perceive()
            observation = env.get_observation()

            # Check if the plan needs to be updated based on new observation
            new_summary = search_agent.summarize(observation.current_web_html)
            plan = plan_agent.create_plan(new_summary)

            # Decide next action
            action_str = action_agent.generate_action(plan)
            action = output_parser.process(action_str)

    finally:
        # Close the environment
        env.close()


# Run the web task
if __name__ == "__main__":
    run(llm_model_path='path-to-llm-model',
        llm_port=8091,
        url='https://example.com',
        task='Complete the web-based task')
