from bs4 import BeautifulSoup  # 需要提前安装 beautifulsoup4 和 lxml
from bs4 import BeautifulSoup
import requests

# 假设 soup 是 BeautifulSoup 对象，已经加载了 HTML 内容


def GetPage(url):
    # return requests.get(url).text.encode('utf-8').decode('utf-8')
    response = requests.get(url)
    response.encoding = 'utf-8'  # 手动指定编码方式为 UTF-8
    return response.text


def find_similar_elements(css_selector, soup):
    original_element = soup.select(css_selector)[0]  # 获取 CSS 选择器匹配的第一个元素
    similar_elements = []  # 用来存储找到的相似元素
    all_elements = soup.find_all(True)  # 获取页面上的所有元素

    for elem in all_elements:
        if Similar(soup, original_element, elem):  # 假定 Similar 函数已适配 BeautifulSoup 对象
            similar_elements.append(elem)
            print(elem)

    return similar_elements


# 以下函数需要根据实际的 Similar 函数进行适配和改写

# 假设你已经有了一个 BeautifulSoup 对象 `soup`
# soup = BeautifulSoup(your_html_content_here, 'lxml')

def select_child(soup, child, verbose=False):
    # 获取元素的直接父元素
    par = child.parent
    par_select = 'body'
    if par and par.name != '[document]' and par.name.upper() != 'BODY':
        par_select = select_child(soup, par, verbose)
        if verbose:
            print("par_select:", par_select)
        if not par_select:
            return ""

    iname = child.name.upper()
    fea = iname
    res = f'{par_select} > {fea}'

    # 获取 id，如果存在的话
    idd = child.attrs.get('id', "")
    if idd:
        res = f'#{idd}'

    # 为了模拟 querySelectorAll 的行为，我们可以尝试找到所有符合当前选择器的元素
    # 注意：BeautifulSoup 不支持直接读取 > 子元素选择器，下面的方式仅是一个简化的尝试
    try:
        testlist = soup.select(res)
    except Exception as error:
        idd = ""
        res = f'{par_select} > {iname}'
        testlist = soup.select(res)

    if verbose:
        print(res)
        print(len(testlist))

    if not testlist:
        return ''
    elif len(testlist) > 1:
        idd = ""
        res = f'{par_select} > {iname}'
        testlist = soup.select(res)
        # 由于 BeautifulSoup 没有 querySelectorAll 方法，我们无法方便地获取元素的索引
        # 不过，可以通过比较对象进行定位
        target_index = next(
            (i for i, elem in enumerate(testlist) if elem == child), -1)
        if target_index == -1:
            return ""
        res += f':nth-of-type({target_index + 1})'

    return res


def EditDist(xx, yy):
    f = [[max(x, y) for y in range(1+len(yy))] for x in range(1+len(xx))]
    for i in range(1, len(xx)+1):
        for j in range(1, len(yy)+1):
            if xx[i-1] == yy[j-1]:
                f[i][j] = f[i-1][j-1]
            else:
                f[i][j] = min(f[i][j-1], f[i-1][j], f[i-1][j-1]) + 1
    return f[-1][-1]


def Similar(soup, original_element, current_element):
    if original_element.name != current_element.name:
        return False
    nodec = original_element.attrs.get('class', [])
    sibc = current_element.attrs.get('class', [])
    if 'active' in nodec:
        nodec.remove('active')
    if 'active' in sibc:
        sibc.remove('active')
    if len(nodec) > 0:
        comm = [x for x in nodec if x in set(sibc)]
        clsdist = 1 - len(comm) / max(len(nodec), len(sibc))
    else:
        clsdist = 1
    ntree = select_child(soup, original_element)
    stree = select_child(soup, current_element)
    treedist = EditDist(ntree, stree)
    treedist = treedist / min(len(ntree), len(stree))
    if treedist * clsdist < 0.25:
        return True
    return False


if __name__ == '__main__':
    url = 'https://cs.fudan.edu.cn/24826/list.htm'
    url ="https://hkss.huijiwiki.com/wiki/Boss_(%E7%A9%BA%E6%B4%9E%E9%AA%91%E5%A3%AB)#Boss"
    url="https://terraria.wiki.gg/zh/wiki/Terraria_Wiki"
    selector='#wp_news_w6 > ul > li > ul > li.news.n4.clearfix > div > a'
    selector='#mw-content-text > div > div:nth-child(6) > div:nth-child(1) > a'
    selector="#box-items > div.main-heading > div.hgroup > div > a"
    page = GetPage(url)
    soup = BeautifulSoup(page, 'html.parser')
    find_similar_elements(selector, soup)
