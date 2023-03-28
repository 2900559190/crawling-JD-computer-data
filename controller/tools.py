from constants import SHOP


def split_info(info, sep):
    """
    获取字符串中的数据
    :param sep: 分隔符
    :param info: 处理的字符串
    :return: 数据列表
    """
    info = info.replace("京品电脑", "")
    info = info.replace("爱心东东", "")
    _ = info.split(sep)
    prod_name = "".join(_[1].split(" ")[0:2])
    config = ",".join(_[1].split(" ")[2:])
    comment_num = _[2].replace("条评价", "")
    shop = _[3]
    price = _[0][1:]
    # print(prod_name, config, comment_num, shop, price)
    return [prod_name, config, comment_num, shop, price]


def pop_element(lst):
    # print(len(lst))
    if lst and ("\n" in lst):
        lst.remove("\n")
        return pop_element(lst)
    elif lst and ("套装2件" in lst):
        lst.remove("套装2件")
        return pop_element(lst)
    elif lst and ("爱心东东" in lst):
        lst.remove("爱心东东")
        return pop_element(lst)
    elif lst and ("京品电脑" in lst):
        lst.remove("京品电脑")
        return pop_element(lst)
    elif lst and ("去看二手" in lst):
        lst.remove("去看二手")
        return pop_element(lst)
    elif lst and ("线下同款" in lst):
        lst.remove("线下同款")
        return pop_element(lst)
    elif lst and ("2人拼" in lst):
        lst.remove("2人拼")
        return pop_element(lst)
    elif lst and ("店" not in lst[-1]):
        del lst[-1]
        return pop_element(lst)
    else:
        return lst


def get_key(prod, shop):
    """
    返回字符串中特定字符
    :param shop: 字符串
    :param prod: 字符串
    :return: 特定字符
    """
    for item in SHOP:
        if item in prod:
            # print("1---------"+"prod"+"---------"+item)
            return item
        if item in shop:
            # print("0---------"+"shop"+"----------"+item)
            return item

    return "0"


# if __name__ == '__main__':
#     info = "￥3599.00,惠普HP 星15青春版 15英寸大屏网课轻薄笔记本电脑(8核锐龙R7处理器 16G 512G 高速WIFI6 7×24h在线服务 银),2万+条评价,惠普京东自营官方旗舰店"
#     _ = ['￥5398.00', '拍拍', '宏碁(Acer)暗影骑士·擎 酷睿i5 微边框 高性能电竞学生吃鸡游戏本二手笔记本电脑 99新 擎i5-11400H 3050 144hz
#     16G内存+512G固态', '京品电脑', '500+条评价',
#      '丫丫二手电脑专营店','自营','秒杀','券99-10','对比','关注','加入购物车']
#     # split_info(info, ",")
#     lst = pop_element(_)
#     print(lst)
