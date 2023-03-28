

from matplotlib import pyplot as plt

from constants import INTERVALS


class Draw:

    def histogram(self, data, title, tag):
        # 绘制柱状图
        labels, values = get_interval(data)

        p = plt.bar(labels, values)
        plt.bar_label(p, label_type='edge')
        plt.title(title)
        if tag == "$":
            plt.xlabel("Price")
        plt.ylabel("Freq")
        # plt.savefig("data/{}.png".format(title))
        plt.show()

    def line_chart(self):
        """"""
        pass


def search_border(nums, target):
    """
    二分查找
    :param nums: 进行查找的数组
    :param target: 要查找的数
    :return: 索引位置
    """
    # print(nums)
    try:
        for i in range(1, len(nums)):
            if target < nums[i]:
                # print(len(nums[:i]), nums[:i])
                return len(nums[:i]), nums[:i]
    except Exception as e:
        print("获取边界失败，发生错误：{}".format(e))


def get_interval(info):
    """"""
    x = list(INTERVALS.keys())
    y = []
    for item in info:
        y.append(float(item[-1]))
    y = sorted(y)

    def get_value(nums):
        """
        有序列表的边界
        :param nums: 有序列表
        :return:
        """
        m, l = 0, 0
        interval_value = []
        for k, v in INTERVALS.items():
            if v[1] != -1:
                l, n = search_border(nums, v[1])
                interval_value.append(l - m)
                m = l
            else:
                interval_value.append(len(nums) - l)
        return interval_value
    return x, get_value(y)


draw = Draw()

# if __name__ == '__main__':
#     draw.histogram(labels, prices, "laptop", "$")
#     # print(658+2986+1044+397+559)
