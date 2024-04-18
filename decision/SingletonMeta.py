class SingletonMeta(type):
    """
    这是一个单例元类，所有使用这个元类创建的类都会成为单例。
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def __str__(self):
        return "SingletonMeta: Manages singleton instances."


class Observation(metaclass=SingletonMeta):
    def __init__(self):
        self.task = None
        self.previous_web_title = None
        self.previous_web_description = None
        self.current_web_html = None
        self.current_web_url = None
        self.current_web_title = None
        self.current_web_action_history = []
        self.open_tabs = []

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __str__(self):
        return f"Observation:\n" \
            f" Task: {self.task}\n" \
            f" Current Web URL: {self.current_web_url}\n" \
            f" Current Web HTML:{self.current_web_html}\n" \
            f" Current Web TITLE:{self.current_web_title}\n" \
            f" Action History: {self.current_web_action_history}"


class Memory(metaclass=SingletonMeta):
    def __init__(self):
        self.previous_actions = []
        self.plan = None
        self.current_stage_in_plan=None
        self.milestones = []

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '{key}'")

    def __str__(self):
        return f"Memory:\n" \
            f" Previous Actions: {self.previous_actions}\n" \
            f" Plan: {self.plan}\n" \
            f" current_stage_in_plan:{self.current_stage_in_plan}\n" \
            f" Milestones: {self.milestones}"


class SelectorsStorage(metaclass=SingletonMeta):
    def __init__(self):
        self.selector_list_btn = []
        self.selector_list_text = []
        self.selector_list_select = []

    def update_selectors(self, btn_list, text_list, select_list):
        self.selector_list_btn = btn_list
        self.selector_list_text = text_list
        self.selector_list_select = select_list

    def __str__(self):
        return f"SelectorsStorage:\n" \
            f" Button Selectors: {self.selector_list_btn}\n" \
            f" Text Selectors: {self.selector_list_text}\n" \
            f" Select Selectors: {self.selector_list_select}"


# 使用示例
# 创建或获取Observation实例
if __name__ == "__main__":
    observation = Observation()

    # 更新任务
    observation.update(task="Complete the web-based task")

    # 更新上一个网页的标题和描述
    observation.update(previous_web_title="Previous Page Title",
                       previous_web_description="Description of the previous page")

    # 更新当前网页的信息
    observation.update(current_web_html="<html></html>",
                       current_web_url="http://currentpage.com", current_web_title="Current Page Title")

    # 添加动作历史记录
    observation.current_web_action_history.append("Clicked button")

    # 更新标签页
    observation.open_tabs.append("Tab 1")

    # 从另一个地方访问Observation实例
    another_observation_reference = Observation()

    # another_observation_reference 将访问到相同的数据
    # 输出: Complete the web-based task
    print(another_observation_reference.task)
    print(another_observation_reference.open_tabs)
    observation.open_tabs.clear()
    print(another_observation_reference.open_tabs)

    memory = Memory()

    # 更新先前动作
    memory.previous_actions.append("Clicked on the Submit button")

    # 更新计划
    memory.update(plan="Follow the steps to complete the task")

    # 添加里程碑
    memory.milestones.append("Login completed")

    # 从另一个地方访问Memory实例
    another_memory_reference = Memory()

    # another_memory_reference 将访问到相同的数据
    # 输出: ['Clicked on the Submit button']
    print(another_memory_reference.previous_actions)
    # 输出: Follow the steps to complete the task
    print(another_memory_reference.plan)
    print(another_memory_reference.milestones)  # 输出: ['Login completed']
