from bs4 import BeautifulSoup, NavigableString
from decision.SingletonMeta import SelectorsStorage, Observation
from bs4 import BeautifulSoup, Comment
import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import sys
# 此处os.path.dirname()可以获得上一级目录，也就是当前文件或文件夹的父目录
# 将目录加入到sys.path即可生效，可以帮助python定位到文件（注：这种方法仅在运行时生效，不会对环境造成污染）
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def remove_empty_tags(soup):
    def clean_tag(tag):
        # 检查当前标签是否没有属性，并且所有子节点都是NavigableString
        if not tag.attrs and all(isinstance(child, NavigableString) for child in tag.contents):
            tag.extract()
    for tag in soup.find_all():
        clean_tag(tag)
    return soup


def process_html(config, html):
    selectors_storage = SelectorsStorage()
    soup = BeautifulSoup(html, 'html.parser')

    # 去除配置中标明的无关元素
    for tag_name in config.get("remove", []):
        [tag.extract() for tag in soup.find_all(tag_name)]

    # 为特殊元素设置id，并记录需要保留的元素和当前的属性
    preserved_elements = {}
    for index, selector in enumerate(selectors_storage.selector_list_btn):
        elements = soup.select(selector)
        for element in elements:
            preserved_elements[element] = {'id': f'click#{index}'}

    for index, selector in enumerate(selectors_storage.selector_list_text):
        elements = soup.select(selector)
        for element in elements:
            preserved_elements[element] = {'id': f'input#{index}'}

    for i, selectors in enumerate(selectors_storage.selector_list_select):
        for j, selector in enumerate(selectors[1:]):
            option = soup.select(selector)
            if option:
                preserved_elements[option[0]] = {'id': f'option#{i}_{j}'}

    # 去除所有元素的所有属性，保留配置文件指定的属性和特殊元素的id和class属性
    for element in soup.find_all():
        attrs_to_keep = config.get(element.name, []) + config.get('*', [])
        if element in preserved_elements.keys():
            attrs_to_keep += config.get('-', [])
        preserved_attrs = preserved_elements.get(element, {})
        for attr in list(element.attrs):
            if attr not in attrs_to_keep and attr not in preserved_attrs:
                del element[attr]

        # 重新为特殊元素添加保存的属性
        for attr, value in preserved_attrs.items():
            element[attr] = value

    # 处理select元素，记录select元素中被选中的文本
    selects = soup.find_all('select')
    for select in selects:
        selected_option = select.find('option', selected=True)
        if selected_option:
            select['selected_item_text'] = selected_option.get_text()

    # 去除comment
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    return soup.prettify()


class ImageExtractor:
    def __init__(self):
        self.unique_id = 1  # 初始唯一编号

    def _generate_unique_id(self):
        unique_id = self.unique_id
        self.unique_id += 1
        return unique_id

    def process_website(self, url, output_folder):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_viewport_size({"width": 1200, "height": 800})
            page.goto(url)
            # 查询所有可能包含图片的元素
            image_elements = page.query_selector_all('img, svg, p, i')
            image_paths = []
            for element in image_elements:
                # 获取元素的截图
                img_data = element.screenshot()
                # 生成保存路径
                image_path = os.path.join(
                    output_folder, f"image_{self._generate_unique_id()}.png")
                # 将截图保存到文件中
                with open(image_path, 'wb') as f:
                    f.write(img_data)
                image_paths.append(image_path)
            browser.close()
        return image_paths


# 示例用法
if __name__ == "__main__":
    extractor = ImageExtractor()
    url = input("Enter website URL: ")
    output_folder = "/Users/zhanghanxing/Desktop/chatgpt4/agent/perception/output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    image_paths = extractor.process_website(url, output_folder)
    if image_paths:
        print("Images saved to:", image_paths)
        # 在这里调用多模态模型，并处理图片
        # 处理后的结果保存为 PNG 格式
