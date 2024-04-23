import hashlib

class ActionNode:
    def __init__(self, action, result, next_page):
        self.action = action
        self.result = result
        self.next_page = next_page # 指向下一个页面节点的引用

class PageNode:
    def __init__(self, url, title,source_code, description=None):
        self.url = url
        self.title = title
        self.source_code_hash = hashlib.sha256(source_code.encode()).hexdigest()
        self.actions = [] # 记录在该页面上执行过的操作
        self.parent = None # 指向父页面节点的引用
        self.description = description # 页面的描述

    def add_action(self, action, result, next_page):
        action = ActionNode(action, result, next_page)
        self.actions.append(action)
        if next_page!=self and not next_page.parent:
            next_page.parent = self

    def get_actions_description(self):
        actions_description = []
        a = 0
        for action in self.actions:
            next_page_title = action.next_page.title if action.next_page else None
            # next_page_description = action.next_page.get_page_description()
            actions_description.append({
                # "动作id":"{a+1}",
                "动作描述": action.action,
                # "result": action.result,
                "进入页面": next_page_title,
                # "进入页面": next_page_description
            })
            a+=1
        return actions_description

    def get_page_description(self):
        if self.description:
            return self.description
        elif self.actions:
            # 如果当前页面没有描述，尝试拼接所有子页面的描述
            descriptions = []
            for action in self.actions:
                if action.next_page and action.next_page.description:
                    descriptions.append(action.next_page.description)
            return " ".join(descriptions) if descriptions else "No description available"
        else:
            return "No description available"


class WebsiteNavigation:
    def __init__(self):
        self.pages = {} # 用于存储页面节点，键是由URL和源代码哈希值组成的字符串

    def get_page_node(self, url, title,source_code,description=None):
        key = f"{url}-{hashlib.sha256(source_code.encode()).hexdigest()}"
        if key not in self.pages:
            self.pages[key] = PageNode(url, title,source_code,description)
            return False,self.pages[key]
        return True,self.pages[key]

        

