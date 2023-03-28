import os
import random

"""基础目录"""
BASE_URL = "https://www.jd.com"
BASE = os.path.abspath(os.path.dirname(__file__))
STATIC = os.path.join(BASE, "static\\")

COOKIE = os.path.join(BASE, "static\\cookie.txt")

"""可操作集合"""
# TODO 可修改区间范围
COMPUTER = {
    "laptop": "670%2C671%2C672",
    "desktop": "670%2C671%2C673",
    "gameBook": "670%2C671%2C1105",
    "server": "670%2C671%2C674"
}

INTERVALS = {
    "0-3000": (0, 3000),
    "3000-7000": (3000, 7000),
    "7000-9000": (7000, 9000),
    "9000-11000": (9000, 11000),
    "11000-?": (11000, -1),
    # "20-": (20, -1),
}

# """数据文件（TXT）"""
# LAPTOP = os.path.join(BASE, "static\\laptop.txt")

"""数据库相关"""
DATABASE = os.path.join(BASE, "static\\fish.db")

THREAD_NUM = 20

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 "
    "Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; "
    ".NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 "
    "Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET "
    "CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
    "Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
    "Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
    "Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) "
    "Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 ("
    "KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 "
    "Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile "
    "Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 "
    "Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) "
    "AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 "
    "Mobile/10A5376e Safari/8536.25",

]

USER_AGENT = random.choice(USER_AGENTS)

# TODO 阿布云代理，使用前  先验证-->是否可用
PROXIES = {
    "http": "http://%(user)s:%(pass)s@%(host)s:%(port)s".format(
        "H2ZR95V4DXA7J21D",
        "10F2522DB4FA0D64",
        "http-dyn.abuyun.com",
        "9020"
    ),

    "https": "https://%(user)s:%(pass)s@%(host)s:%(port)s".format(
        "H2ZR95V4DXA7J21D",
        "10F2522DB4FA0D64",
        "http-dyn.abuyun.com",
        "9020"
    )
}

# 可灵活添加
SHOP = [
    "华为", "联想", "苹果", "华硕", "惠普", "荣耀", "Apple", "微星", "海尔", "宏碁", "Acer", "Huawei",
    "ThinkPad", "小米", "LG", "雷蛇", "机械师", "拯救者", "壹号本", "Surface", "攀升", "神舟", "雷神",
    "清华同方", "HUAWEI", "APPLE", "GPD", "国行", "戴尔", "Dynabook", "Daysky", "GAVX", "toposh",
    "外星人", "机械革命", "松下", "格莱富", "Grefu", "驰为", "NUC", "VAIO", "战神", "整机", "酷比魔方",
    "Thunderobot", "雷神", "新华三", "H3C", "澳典", "戴睿", "品弘本", "优和", "UHOO", "HUWI", "酷提",
    "武极", "得峰", "七彩虹", "ROG", "雷蛇", "火影游戏本", "悟空", "WOOKING", "iru", "三星", "狄瑟", "领睿",
    "英特尔", "intel", "玄派", "HONOR", "系能", "巅峰玩家", "未来人类"
]
