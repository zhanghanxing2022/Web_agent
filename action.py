from enum import Enum


class ActionType(Enum):
    CLICK = "click"
    TYPE = "type"
    SELECT = "select"
    NEW_TAB = "new_tab"
    TAB_FOCUS = "tab_focus"
    CLOSE_TAB = "close_tab"
    GOTO = "goto"
    GO_BACK = "go_back"
    GO_FORWARD = "go_forward"
    STOP = "stop"


class Action:
    def __init__(self, action_type,action_str, **kwargs):
        self.action_type = action_type
        self.kwargs = kwargs
        self.action_str = action_str

    def __str__(self):
        kargs_str = ', '.join([f"{key}={value}" for key, value in self.kwargs.items()])
        return f"{self.action_type.value} {kargs_str}"
