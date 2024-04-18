import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from decision.SingletonMeta import Memory
import re
from action import Action, ActionType


# 此处os.path.dirname()可以获得上一级目录，也就是当前文件或文件夹的父目录
# 将目录加入到sys.path即可生效，可以帮助python定位到文件（注：这种方法仅在运行时生效，不会对环境造成污染）


class OutputParser:
    def __init__(self):
        super().__init__()

    def process(self, llm_output):
        # 这里可以添加解析LLM输出的逻辑
        return llm_output


class PlanOperationProcessor:
    def __init__(self):
        self.memory = Memory()

        # Patterns for different operations
        self.patterns = {
            'define_plan': re.compile(r'`define_plan \[(.*?)\] \[(.*?)\]`'),
            'maintain_plan': re.compile(r'`maintain_plan \[(.*?)\]`'),
            'alter_plan': re.compile(r'`alter_plan \[(.*?)\] \[(.*?)\]`'),
        }
        self.record = re.compile(r'`record \[(.*?)\]`')

    def process(self, operation_str):
        
        record = re.search(self.record, operation_str)
        if record:
            self._process_record(record.group(1))
        # Check each operation pattern to find a match
        for operation, pattern in self.patterns.items():
            match = pattern.search(operation_str)
            if match:
                if operation == 'define_plan':
                    self._process_define_plan(match.group(1), match.group(2))
                elif operation == 'maintain_plan':
                    self._process_maintain_plan(match.group(1))
                elif operation == 'alter_plan':
                    self._process_alter_plan(match.group(1), match.group(2))
                break
        else:
            print("No valid operation found in the input.")
        return ""

    def _process_record(self, milestone):
        self.memory.milestones.append(milestone)

    def _process_define_plan(self, plan, stage_tag):
        self.memory.plan = plan
        self.memory.current_stage_in_plan = stage_tag

    def _process_maintain_plan(self, stage_tag):
        # Assuming maintaining a plan means updating the stage tag
        self.memory.current_stage_in_plan = stage_tag

    def _process_alter_plan(self, plan, stage_tag):
        self.memory.plan = plan
        self.memory.current_stage_in_plan = stage_tag


class ActionOutputParser(OutputParser):
    def __init__(self):
        super().__init__()

    def process(self, llm_output):
        # 使用正则表达式匹配被``````包裹的部分
        pattern = r"```(.*?)```"
        match = re.search(pattern, llm_output, re.DOTALL)

        if not match:
            raise ValueError("No valid action found in LLM output.")

        # 获取匹配的动作字符串
        action_str = match.group(1).strip()

        # 分割动作类型和参数
        parts = action_str.split(maxsplit=1)
        if not parts:
            raise ValueError("Action string is empty.")

        action_type_str = parts[0].upper()
        args_str = parts[1] if len(parts) > 1 else ""

        # 根据动作类型确定参数键
        action_type = ActionType[action_type_str]
        args_dict = self._parse_args(action_type, args_str)

        # 创建Action对象
        action = Action(action_type, action_str, **args_dict)
        return action

    def _parse_args(self, action_type, args_str):
        # 使用正则表达式匹配方括号内的内容
        pattern = r"\[([^\]]+)\]"
        args_list = re.findall(pattern, args_str)

        args_dict = {}
        if action_type == ActionType.CLICK or action_type == ActionType.SELECT:
            if len(args_list) != 1:
                raise ValueError(
                    f"Invalid number of arguments for action type {action_type}.")
            args_dict['id'] = args_list[0]
        elif action_type == ActionType.TYPE:
            if not (len(args_list) == 2 or len(args_list) == 3):
                raise ValueError(
                    f"Invalid number of arguments for action type {action_type}.")
            args_dict['id'] = args_list[0]
            args_dict['content'] = args_list[1]
            args_dict['press_enter_after'] = True
            if len(args_list) == 3 and '0' in args_list[2]:
                args_dict['press_enter_after'] = False

        elif action_type == ActionType.TAB_FOCUS:
            if len(args_list) != 1:
                raise ValueError(
                    f"Invalid number of arguments for action type {action_type}.")
            args_dict['tab_index'] = args_list[0]
        elif action_type == ActionType.GOTO:
            if len(args_list) != 1:
                raise ValueError(
                    f"Invalid number of arguments for action type {action_type}.")
            args_dict['url'] = args_list[0]
        elif action_type == ActionType.STOP:
            if len(args_list) != 1:
                raise ValueError(
                    f"Invalid number of arguments for action type {action_type}.")
            args_dict['answer'] = args_list[0]
        elif action_type in [ActionType.NEW_TAB, ActionType.CLOSE_TAB, ActionType.GO_BACK, ActionType.GO_FORWARD]:
            if args_list:
                raise ValueError(
                    f"Invalid number of arguments for action type {action_type}.")
        else:
            raise ValueError(f"Unsupported action type {action_type}.")
        return args_dict


# 示例使用
if __name__ == "__main__":
    parser = ActionOutputParser()
    llm_output_click = "In summary, the next action I will perform is ```click [1234]```."
    llm_output_type = "In summary, the next action I will perform is ```type [input_field] [text to type]```."
    llm_output_select = "In summary, the next action I will perform is ```select [option1]```."
    llm_output_new_tab = "In summary, the next action I will perform is ```new_tab```."
    llm_output_tab_focus = "In summary, the next action I will perform is ```tab_focus [2]```."
    llm_output_close_tab = "In summary, the next action I will perform is ```close_tab```."
    llm_output_goto = "In summary, the next action I will perform is ```goto [https://example.com]```."
    llm_output_go_back = "In summary, the next action I will perform is ```go_back```."
    llm_output_go_forward = "In summary, the next action I will perform is ```go_forward```."
    llm_output_stop_with_answer = "In summary, the next action I will perform is ```stop [answer]```."
    llm_output_stop_no_answer = "In summary, the next action I will perform is ```stop [N/A]```."

    print(parser.process(llm_output_click))
    print(parser.process(llm_output_type))
    print(parser.process(llm_output_select))
    print(parser.process(llm_output_new_tab))
    print(parser.process(llm_output_tab_focus))
    print(parser.process(llm_output_close_tab))
    print(parser.process(llm_output_goto))
    print(parser.process(llm_output_go_back))
    print(parser.process(llm_output_go_forward))
    print(parser.process(llm_output_stop_no_answer))
    print(parser.process(llm_output_stop_with_answer))
    processor = PlanOperationProcessor()

    # Simulate receiving an operation string
    operation_str = "`define_plan [1. Click the submit button. 2. Check the confirmation message.] [0]`"
    processor.process_operation(operation_str)

    memory = Memory()

    operation_str_2 = "`record [User logged in successfully]` `maintain_plan [1]`"

    processor.process_operation(operation_str_2)

    print(memory)
