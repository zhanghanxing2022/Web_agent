from Env.Env import Env
from decision.OutputParser import *
from action import Action, ActionType
from decision.SingletonMeta import Observation, SelectorsStorage
from decision.Prompt import *
from decision.Model import *
# Define a SearchAgent class that summarizes current page and related information
from decision.Similar import find_similar_elements
from concurrent.futures import ThreadPoolExecutor, as_completed
from Mutitask.manager import *
from Website import *

import argparse

# 加入过程记录
def run(llm, env, task, file="none",create=False):
    # Initialize environment
    webste = WebsiteNavigation()
    answer = ""
    try:
        # Perceive the initial state of the page
        env.perceive()
        # Method to retrieve observation from the environment
        observation = Observation()
        observation.task = task

        # Use SearchAgent to get page summary and related info
        search_agent = SearchLLM(llm)
        summary = search_agent.call()
        tf, page = webste.get_page_node(observation.current_web_url,
                                        observation.current_web_title,
                                        observation.current_web_source
                                        )
        page.description = summary
        if tf:
            observation.current_web_action_history = page.get_actions_description()
        else:
            observation.current_web_action_history = []

        # Use PlanAgent to draft a plan
        plan_agent = PlanLLM(llm)
        plan = plan_agent.call()

        action = None
        action_agent = ActionLLM(llm)
        action = action_agent.call()

        select_agent = SelectLLM(llm)

        # Execute plan step-by-step
        while True:
            if action.action_type == ActionType.STOP:
                print("Task completed with answer:",
                      action.kwargs.get('answer', 'N/A'))
                answer = action.kwargs.get('answer', 'N/A')
                break
            if action.action_type == ActionType.CLICK and create:
                selectorsStorage = SelectorsStorage()
                css_selector = selectorsStorage.selector_list_btn[int(
                    re.findall(r'\d+', action.kwargs['id'])[0])]

                similar_elements, similar_elements_css = find_similar_elements(
                    css_selector, observation.current_web_source)

                def process_in_batches(elements, element_css, batch_size, process_function):
                    """
                    分批处理元素，并对每批元素执行给定的处理函数。

                    :param elements: 要处理的元素列表。
                    :param batch_size: 每批的最大元素数量。
                    :param process_function: 对元素批次进行处理的函数。
                    :return: 各批处理结果列表。
                    """
                    # 将元素列表拆分为指定大小的批次
                    for i in range(0, len(elements), batch_size):
                        batch = elements[i:i + batch_size]
                        batch_css = element_css[i:i + batch_size]
                        # 对当前批次执行处理函数
                        yield process_function(batch, batch_css)

                # 示范性的处理函数，这个函数会对每批CSS选择器进行处理
                def process_batch(batch, batch_css):
                    # 对于 batch 中的每个 CSS 选择器，select_agent 和 search_agent 执行相关处理
                    # 这里假设有函数 select_action 和 search_action 来调用代理
                    select_agent._set_selector(batch_css)
                    select_agent._set_elem(batch)
                    return select_agent.call()
                batch_size = 10  # 或根据需要调整
                batches_results = list(process_in_batches(
                    similar_elements, similar_elements_css, batch_size, process_batch))

                # 合并批次结果
                final_results = [
                    item for batch in batches_results for item in batch]
                max_workers = 5  # 限制最大线程数
                if final_results >= 5:
                    # 使用 ThreadPoolExecutor 来管理线程
                    serialized_state = serialize_state(
                        Observation(), Memory(), SelectorsStorage())
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        futures = []

                        for css_selector, task in final_results:
                            # 提交任务到线程池
                            future = executor.submit(
                                thread_worker, serialized_state, env.driver.current_url, css_selector, task, run)
                            futures.append(future)

                        # 等待所有线程完成，你可以处理每个线程的返回结果
                        for future in as_completed(futures):
                            try:
                                result = future.result()  # 如果线程函数中有返回值，这里可以获取
                                print(result)
                                task = TaskLLM()
                            except Exception as exc:
                                print(f'Generated an exception: {exc}')

                # to do
                # 如果similar_elements, similar_elements_css，那么需要分批交给llm处理，最后整合结果，首先执行动作，之后根据任务启动多线程处理，处理完之后要整合各个线程结果。
                # 注意使用父进程的Observation，等数据初始化子进程的Observation等数据

            # Perform action using the environment
            env.execute_action(action)

            # Update the observation after executing the action
            observation.previous_web_description = summary
            observation.previous_web_title = observation.current_web_title
            observation.previous_web_url = observation.current_web_url
            env.perceive()
            tf, next_page = webste.get_page_node(observation.current_web_url,
                                                 observation.current_web_title,
                                                 observation.current_web_source
                                                 )
            page.add_action(action, "", next_page)

            # Check if the plan needs to be updated based on new observation
            summary = search_agent.call()
            next_page.description = summary
            plan_agent.call()

            # Decide next action
            action = action_agent.call()
    except Exception as e:
        print(f"An error occurred: {e}")
        answer = "An error occurred: {e}"
    finally:
        # Close the environment
        env.close()
        return answer


# Run the web task
if __name__ == "__main__":
    args = parser.parse_args()
    # 使用从命令行接收的参数
    env = Env(args.url, headless=True)
    llm = Modal(args.llm_model_path, args.llm_port)
    run(llm,
        env=env,
        task=args.task)
