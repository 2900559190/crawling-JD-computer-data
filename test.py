import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

from constants import USER_AGENT


def get_url_lst(pages):
    """
    构造搜索产品的所有页面
    :return: 所有的页面列表
    """
    search_urls = []

    for i in range(1, pages + 1):
        search_urls.append("https://list.jd.com/listNew.php?cat=670%2C671%2C672&page={}&s={}&click=0"
                           .format((i - 1) * 2 + 1, 58 + (i - 1) * 60))

        search_urls.append("https://list.jd.com/listNew.php?cat=670%2C671%2C672&page={}&s={}&scrolling=y&log_id={}"
                           .format(i * 2, 87 + (i - 1) * 30, '%.4f' % time.time()))
    print(search_urls)

    return search_urls


url = "https://www.jd.com"
options = Options()
# 使用隐身模式（无痕模式）
options.add_argument('--headless')
options.add_argument('--incognito')
driver = webdriver.Edge(options=options)

driver.get(url)
# time.sleep(10)
# driver.get(url2)
# time.sleep(10)
driver.find_element(By.XPATH, '//*[@id="ttbar-login"]/a[1]').click()
# 定位账户登录
driver.find_element(By.XPATH, '//*[@id="kbCoagent"]/ul/li[1]/a').click()
time.sleep(2)
iframe = driver.find_element(By.XPATH, '//*[@id="ptlogin_iframe"]')
driver.switch_to.frame(iframe)
driver.find_element(By.XPATH, '//*[@id="qlogin_list"]/a').click()
time.sleep(2)

# 模拟JS将浏览器滚动到最底部
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(2)

cookies = driver.get_cookies()
print(cookies)
cookie_str = ""
for cookie in cookies:
    cookie_str += cookie["name"] + "=" + cookie["value"] + ";"

print(cookie_str)

headers = {
    'authority': 'search.jd.com',

    'method': 'GET',

    'scheme': 'https',

    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

    'cookie': cookie_str,

    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

# page = driver.current_url
url_lst = get_url_lst(100)

"""
爬虫爬取网页数据，需要登陆的情况
1. 先用selenium库模拟登录，登录之后进入需要批量爬取数据的网页（第一页即可）
2. 获取当前页的cookie，一般取cookie的某个key的值进行拼接，京东的是cookie[name]的值进行拼接
3. 构造需要爬取的URL列表（需要浏览器抓包分析）
4. 构造header（请求头）， 传入重新拼接的cookie和使用随机的user_agent
5. 使用requests库的get方法，传入url和构造的header
6. 开始解析网页，获取数据
7. 数据库使用的是sqlite的话，插入数据时需要上锁 --> (针对的是多线程爬取数据的情况)
"""


def parse_page(url, headers):
    """
    解析页面数据并存储
    :param headers: 构造的请求头
    :param url: 商品页面的URL
    :return:
    """
    info = []
    html = requests.get(url, headers=headers)
    tree = etree.HTML(html.text)
    if "click" in url:
        li_lst = tree.xpath('//*[@id="J_goodsList"]/ul/li')
    else:
        li_lst = tree.xpath('/html/body/li')

    for li in li_lst:
        price = li.xpath('.//div/div[2]/strong/i/text()')[0]
        prod = ",".join(li.xpath('.//div/div[3]/a/em/text()'))
        config = ",".join(li.xpath('.//div/div[3]/span/span/b/text()'))
        shop = ",".join(li.xpath('.//div/div[5]/span/a/@title'))
        info.append((price, prod, config, shop))
        # print(price, prod, config, shop)

    return info


for url in url_lst:
    headers['user-agent'] = USER_AGENT
    info = parse_page(url, headers)
    print(len(info))
