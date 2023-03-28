import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from math import ceil

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

from constants import USER_AGENT, THREAD_NUM
from controller.tools import get_key
from model.sqlite_dao import Computer


class Crawling:
    """
    数据爬取类
    """

    def __init__(self, url):
        self.t1 = time.time()

        self.url = url
        self.options = Options()
        # 使用隐身模式（无痕模式）
        self.options.add_argument('--headless')
        self.options.add_argument('--incognito')
        # 设置防检测
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.driver = webdriver.Edge(options=self.options)

        self.cookie = None
        self.headers = {
            'authority': 'search.jd.com',

            'method': 'GET',

            'scheme': 'https',

            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',

            'cookie': self.cookie,

            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.computer = Computer()
        self.table_name = None

    def login(self):
        """
        登录京东
        """
        try:
            # 打开浏览器
            self.driver.get(self.url)

            print("开始登陆京东，请稍等...")
            # 定位登录button
            self.driver.find_element(By.CLASS_NAME, "link-login").click()
            # 定位账户登录
            self.driver.find_element(By.XPATH, '//*[@id="kbCoagent"]/ul/li[1]/a').click()
            iframe = self.driver.find_element(By.XPATH, '//*[@id="ptlogin_iframe"]')
            self.driver.switch_to.frame(iframe)
            self.driver.find_element(By.XPATH, '//*[@id="qlogin_list"]/a').click()
            time.sleep(2)
        except Exception as e:
            print("账号登陆失败...发生错误：{}".format(e.__cause__))

    def get(self, table_name, prod):
        """
        爬取电脑数据并且存入数据库
        :param prod: 爬取的产品
        :param table_name: 创建的表名称 --> 用于存储电脑数据
        """
        self.computer.create(table_name)
        self.table_name = table_name

        """判断cookie是否为空，为空的话，调用登录函数，获取登录的cookie信息"""
        if not self.cookie:
            self.login()  # 登录京东
        try:
            # 获取该页面的cookie
            self.cookie = self.driver.get_cookies()
            cookie_str = ""
            for cookie in self.cookie:
                cookie_str += cookie["name"] + "=" + cookie["value"] + ";"
            # 请求头的构造，传入cookie
            self.headers['cookie'] = cookie_str
        except Exception as e:
            print("cookie获取失败，构造header失败...发生错误：{}".format(e.__context__))

        print("开始爬取--{}--的数据，请稍等...".format(table_name))
        url_lst = Crawling.get_url_lst(100, prod)

        try:
            """线程池插入数据"""
            with ThreadPoolExecutor(max_workers=THREAD_NUM) as pool:
                # for url in url_lst:
                pool.map(self.parse_page, url_lst)
        except Exception as e:
            print("多线程执行失败...发生错误：{}".format(e))

        # 多线程插入失败的数据重新插入
        if self.computer.tmp:
            for item in self.computer.tmp:
                self.computer.insert(item)
        else:
            self.close()
        print("{}---的数据存储结束...".format(table_name))
        print("总共耗时：{}s".format(ceil(time.time() - self.t1))+"\n")

    def parse_page(self, url):
        """
        解析页面数据并存储
        :param url: 商品页面的URL
        :return:
        """
        page_pattern = re.compile(r'.*page=(\d*)')
        page = ceil(int(page_pattern.search(url).group(1)) / 2)

        self.headers['user-agent'] = USER_AGENT  # 请求头构造，使用随机的user_agent
        info = []

        try:
            html = requests.get(url, headers=self.headers)
            tree = etree.HTML(html.text)

            if "click" in url:
                li_lst = tree.xpath('//*[@id="J_goodsList"]/ul/li')
            else:
                li_lst = tree.xpath('/html/body/li')
            # print(len(li_lst))
            if len(li_lst) < 30:
                return self.parse_page(url)
            else:
                for li in li_lst:
                    price = li.xpath('.//div/div[2]/strong/i/text()')[0]
                    prod = li.xpath('.//div/div[3]/a/em/text()')[0].replace("\n", "").lstrip()
                    config = ",".join(li.xpath('.//div/div[3]/span/span/b/text()'))
                    shop = ",".join(li.xpath('.//div/div[5]/span/a/text()'))
                    if not shop:
                        shop = "京东店铺"
                    prod = get_key(prod, shop)

                    if prod == "HUWI":
                        prod = "华为"
                    if prod == "0":
                        prod = "其他"
                    if not config:
                        config = li.xpath('.//div/div[3]/a/em/text()')[0].replace("\n", "").lstrip()
                    info.append((prod, config, shop, price))

        except Exception as e:
            print("解析URL失败，发生错误：{}".format(e))
        self.computer.insert(list(info))
        # print(info)
        print("{}--的第{}页共有{}数据存储完成...".format(self.table_name, page, len(info)))

    def close(self):
        """
        关闭类中开启的连接
        """
        self.driver.close()
        self.computer.close()

    @staticmethod
    def get_url_lst(pages, prod):
        """
        构造搜索产品的所有页面
        :return: 所有的页面列表
        """
        search_urls = []

        for i in range(1, pages + 1):
            search_urls.append("https://list.jd.com/listNew.php?cat={}&page={}&s={}&click=0"
                               .format(prod, (i - 1) * 2 + 1, 58 + (i - 1) * 60))

            search_urls.append("https://list.jd.com/listNew.php?cat={}&page={}&s={}&scrolling=y&log_id={}"
                               .format(prod, i * 2, 87 + (i - 1) * 30, '%.4f' % time.time()))

        return search_urls


# if __name__ == "__main__":
#     crawl = Crawling(BASE_URL)
#     # get_data.get(COMPUTER[0], "laptop")
#     crawl.get(COMPUTER[1], "desktop")
